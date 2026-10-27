"""FYM v99 (Version 1.3) rack photo pass (Tiffany Oct 26 10:07pm: vertical racks -> horizontal, backgrounds removed where
possible, ONE rack isolated from every multi-rack photo where possible). Cut-outs are made by v99_cut.py from the brands'
own photos (config/fym-rack-singles-oct26.json -> assets/racks/v99/<name>.webp). Each listed rack gets:
  full image -> <build>/r99/<name>.webp (hd index 'r' = 'file:r99/...'), inline thumbnail IMG['rk99<name>'], c flag from config
  (c:false = brand photo kept on its white background; the card draws the white box).
Keeps every other rack field (names, links, match lists, pq). Idempotent. Gate [97] + [56]. Usage: v99_racksingles.py <build>"""
import sys, os, io, json, base64
from PIL import Image
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
R = D['racks']; hd = json.load(open(B + '/hd/index.json')); C = json.load(open(REPO + 'config/fym-rack-singles-oct26.json'))['cuts']
IMG = {}; n = 0; os.makedirs(B + '/r99', exist_ok=True)
for name, c in C.items():
    k = c['key']; src = REPO + 'assets/racks/v99/' + name + '.webp'
    if k in R and 'hx' in c: R[k]['hx'] = c['hx']
    if k in R and 'rf' in c: R[k]['rf'] = c['rf']
    if k not in R or R[k].get('hid') or not os.path.exists(src): print('skip', name); continue
    key = 'rk99' + ''.join(ch for ch in name if ch.isalnum())
    if R[k].get('im') == key: continue
    im = Image.open(src).convert('RGBA')
    if im.width > 900: im = im.resize((900, round(im.height * 900 / im.width)), Image.LANCZOS)
    im.save(f'{B}/r99/{name}.webp', 'WEBP', quality=90, method=6)
    t = im.resize((360, max(1, round(im.height * 360 / im.width))), Image.LANCZOS); b = io.BytesIO(); t.save(b, 'WEBP', quality=82, method=6)
    IMG[key] = 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()
    R[k]['im'] = key; R[k]['c'] = bool(c['c']); hd['r'][k] = f'file:r99/{name}.webp'; n += 1
json.dump(hd, open(B + '/hd/index.json', 'w'), separators=(',', ':'))
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
if IMG:
    inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMG, separators=(',', ':')) + ');</script>'
    a_ = '<script src="b24v1.js"></script>'; assert h.count(a_) == 1; h = h.replace(a_, a_ + inl, 1)
open(P, 'w').write(h); print('v99 rack singles', n)
