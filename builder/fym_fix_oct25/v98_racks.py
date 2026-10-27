"""FYM v98 (Version 1.2) racks (docs/MATCH-INBOX.md Oct 26 evening), config/fym-rack-split-oct26.json:
1. Mahjong Register (Tiffany 6:04pm): no more stacks of racks in one image. The Signature Collection parent (one entry, photo =
   6 racks stacked) is hidden and split into its colour variants (real product variants, links ?variant=...), each with ONE rack
   cut from Mahjong Register's own group shot; the 4 gold-hardware racks swap their multi-rack infographic for one rack cut from
   the brand's 4-rack group shot. Crystal Clear can't be cut cleanly off white -> shown on white (c:false).
2. Mahjong Row & Co. (Tiffany 7:45pm regression): all 7 racks back to ONE straight-on rack each + clean names.
3. PLM Chartreuse (recoloured approved rack) + Dark Green back to approved card racks (gate [94]).
4. Mahj Mood White Wooden Scalloped (Main 6:01pm): angled single rack cut from Mahj Mood's own photo (straight-on read far too
   long/thin).
Full image -> <build>/r98/<name>.webp (hd index 'file:'), small inline thumbnail IMG['rk98<name>']. All looked at on white + navy.
Idempotent. Gate [92] + [56]. Usage: v98_racks.py <build>"""
import sys, os, io, json, base64, copy
import numpy as np
from PIL import Image
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
R = D['racks']; hd = json.load(open(B + '/hd/index.json')); C = json.load(open(REPO + 'config/fym-rack-split-oct26.json'))
IMG = {}; n = 0; os.makedirs(B + '/r98', exist_ok=True)
def put(src):
    base = os.path.splitext(os.path.basename(src))[0]; key = 'rk98' + ''.join(ch for ch in base if ch.isalnum())
    im = Image.open(REPO + src).convert('RGBA')
    bb = im.getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox()
    if bb: p_ = 6; im = im.crop((max(0, bb[0] - p_), max(0, bb[1] - p_), min(im.width, bb[2] + p_), min(im.height, bb[3] + p_)))  # tight to the rack
    if im.width > 900: im = im.resize((900, round(im.height * 900 / im.width)), Image.LANCZOS)
    im.save(f'{B}/r98/{base}.webp', 'WEBP', quality=90, method=6)
    t = im.resize((360, max(1, round(im.height * 360 / im.width))), Image.LANCZOS); b = io.BytesIO(); t.save(b, 'WEBP', quality=82, method=6)
    IMG[key] = 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()
    a = np.asarray(im).reshape(-1, 4); a = a[a[:, 3] > 200][:, :3]
    if not len(a): a = np.asarray(im).reshape(-1, 4)[:, :3]
    return key, f'file:r98/{base}.webp', '#%02x%02x%02x' % tuple(np.median(a, 0).astype(int))
for k in C['hide']:
    if k in R and not R[k].get('hid'): R[k]['hid'] = True; n += 1
for k, v in C['add'].items():
    if k in R and str(R[k].get('im', '')).startswith('rk98'): continue
    r = copy.deepcopy(R[v['from']]); r.pop('hid', None); r.pop('lo', None); r.pop('wh', None); r.pop('wp', None)
    key, f, hx = put(v['img'])
    base_u = r['u'].split('?')[0]
    r.update(n=v['n'], u=f"{base_u}?variant={v['variant']}", im=key, c=v['c'], pq=5, hx=hx, rf=v['rf'], rs={c: 1.7 for c in v['rf']}, add='oct26-v98')
    R[k] = r; hd['r'][k] = f; n += 1
for k, v in C['replace'].items():
    if k not in R or str(R[k].get('im', '')).startswith('rk98'): continue
    key, f, hx = put(v['img']); R[k].update(im=key, c=v['c']); hd['r'][k] = f; n += 1  # keeps the by-eye photo score pq (gate [79])
    if v.get('n'): R[k]['n'] = v['n']
json.dump(hd, open(B + '/hd/index.json', 'w'), separators=(',', ':'))
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
if IMG:
    inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMG, separators=(',', ':')) + ');</script>'
    a_ = '<script src="b24v1.js"></script>'; assert h.count(a_) == 1; h = h.replace(a_, a_ + inl, 1)
open(P, 'w').write(h); print('v98 racks', n, 'images', len(IMG))
