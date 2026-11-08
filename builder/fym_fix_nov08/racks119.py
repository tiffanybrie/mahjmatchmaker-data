"""FYM 1.19 rack refresh (Tiffany Nov 8 2:12pm: review what's NEW in partner racks so they don't go stale).
Reads config/fym-rack-adds-nov08.json:
  adds     -> new partner rack colourways (in stock Nov 8), one rack photo each (assets/racks/v119/*)
  cutouts  -> the 12 Nov 1 racks hidden pending_review (adds112): set the cut-out, drop hid + pending_review
  fixes    -> data corrections (names, colour, sold-out flags)
Images: full -> <build>/r119/<name>.webp (hd index 'file:'), inline 360px thumbnail IMG['rk119<name>'] (same as v98_racks.py).
Every image was looked at on white + navy Nov 8 (rule 6b); run builder/fym_rack_images.py <build> afterwards: it must say
'all rack images reviewed ok' (the review hashes were recorded from this script's output).
Idempotent. Usage: python3 builder/fym_fix_nov08/racks119.py <build_dir>"""
import sys, os, io, json, base64
import numpy as np
from PIL import Image
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
R = D['racks']; hd = json.load(open(B + '/hd/index.json')); S = json.load(open(REPO + 'config/fym-rack-adds-nov08.json'))
IMG = {}; os.makedirs(B + '/r119', exist_ok=True); log = []

def put(src):
    base = os.path.splitext(os.path.basename(src))[0]; key = 'rk119' + ''.join(ch for ch in base if ch.isalnum())
    im = Image.open(REPO + src).convert('RGBA')
    if im.width > 900: im = im.resize((900, round(im.height * 900 / im.width)), Image.LANCZOS)
    im.save(f'{B}/r119/{base}.webp', 'WEBP', quality=90, method=6)
    t = im.resize((360, max(1, round(im.height * 360 / im.width))), Image.LANCZOS); b = io.BytesIO(); t.save(b, 'WEBP', quality=82, method=6)
    IMG[key] = 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()
    a = np.asarray(im).reshape(-1, 4); a = a[a[:, 3] > 200][:, :3]
    if not len(a): a = np.asarray(im).reshape(-1, 4)[:, :3]
    return key, f'file:r119/{base}.webp', '#%02x%02x%02x' % tuple(np.median(a, 0).astype(int))

for x in S['adds']:
    k = x['key']; o = {f: v for f, v in x.items() if f not in ('key', 'img', 'price')}
    o['im'], hd['r'][k], o['hx'] = put(x['img'])
    R[k] = o; log.append(('add', o['n']))
for k, v in S['cutouts'].items():
    if k not in R: log.append(('MISSING', k)); continue
    r = R[k]; r['im'], hd['r'][k], hx = put(v['img']); r['c'] = v['c']
    r.pop('hid', None); r.pop('pending_review', None); log.append(('cut-out + unhide', r['n']))
for k, v in S['fixes'].items():
    if k in R: R[k].update({f: x for f, x in v.items() if f != 'why'}); log.append(('fix', R[k]['n']))

json.dump(hd, open(B + '/hd/index.json', 'w'), separators=(',', ':'))
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
mark = '<!--racks119-->'
if mark in h:  # idempotent: replace the earlier inline block
    a0 = h.index(mark); a1 = h.index('</script>', a0) + 9; h = h[:a0] + h[a1:]
inl = mark + '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMG, separators=(',', ':')) + ');</script>'
a = '<script src="b24v1.js"></script>'; assert h.count(a) == 1; h = h.replace(a, a + inl, 1)
open(P, 'w').write(h)
for l in log: print(*l)
print('racks119:', len(log), 'changes')
