"""FYM 1.19: add the five Miss Mahjong scalloped acrylic racks that dropped Tue Nov 10 (Bombshell Pink, Butter Yellow,
Pistachio, Peony, Chartreuse). Reads config/fym-rack-adds-nov10-missmahjong.json (adds only).
Same image path as builder/fym_fix_nov08/racks119.py: full -> <build>/r119/<name>.webp (hd index 'file:'), inline 360px
thumbnail IMG['rk119<name>']. The photos are the brand's own featured product photos (c:false, shown on their white
background); every one was looked at on white + navy Nov 10 (rule 6b) and approved in builder/fym_flags/rack_image_review.json.
Run AFTER racks119.py, then `python3 builder/fym_rack_images.py <build>` must print 'all rack images reviewed ok'.
Idempotent. Usage: python3 builder/fym_fix_nov10/racks119_missmahjong.py <build_dir>"""
import sys, os, io, json, base64
from PIL import Image
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
R = D['racks']; hd = json.load(open(B + '/hd/index.json')); hd.setdefault('r', {})
S = json.load(open(REPO + 'config/fym-rack-adds-nov10-missmahjong.json'))
IMG = {}; os.makedirs(B + '/r119', exist_ok=True); log = []
DROP = ('key', 'img', 'price', 'sku', 'product_id', 'variant_id', 'src_image')

def put(src):
    base = os.path.splitext(os.path.basename(src))[0]; key = 'rk119' + ''.join(ch for ch in base if ch.isalnum())
    im = Image.open(REPO + src).convert('RGBA')
    if im.width > 900: im = im.resize((900, round(im.height * 900 / im.width)), Image.LANCZOS)
    im.save(f'{B}/r119/{base}.webp', 'WEBP', quality=90, method=6)
    t = im.resize((360, max(1, round(im.height * 360 / im.width))), Image.LANCZOS); b = io.BytesIO(); t.save(b, 'WEBP', quality=82, method=6)
    IMG[key] = 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()
    return key, f'file:r119/{base}.webp'

for x in S['adds']:
    k = x['key']; o = {f: v for f, v in x.items() if f not in DROP}
    o['im'], hd['r'][k] = put(x['img'])
    log.append(('update' if k in R else 'add', o['n'])); R[k] = o

json.dump(hd, open(B + '/hd/index.json', 'w'), separators=(',', ':'))
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
mark = '<!--racks119mm-->'
if mark in h:  # idempotent: replace the earlier inline block
    a0 = h.index(mark); a1 = h.index('</script>', a0) + 9; h = h[:a0] + h[a1:]
inl = mark + '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMG, separators=(',', ':')) + ');</script>'
a = '<script src="b24v1.js"></script>'; assert h.count(a) == 1; h = h.replace(a, a + inl, 1)
open(P, 'w').write(h)
for l in log: print(*l)
print('racks119_missmahjong:', len(log), 'changes')
