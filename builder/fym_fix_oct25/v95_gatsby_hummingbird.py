"""FYM v95 (Tiffany Oct 26 8:54 + 8:55am):
(1) Anders Ruff Green Light Gatsby tiles: new swipe photo = Anders Ruff listing image 1 (AR_261016_MAGJONG2023.jpg,
    joker + 2 flowers lying on a tortoise rack) zoomed in for true tile colour (these tiles have no separate back; the
    green tile colour is the point). 1600x700 strip, tiles centred in the match-card circle. Real photo, crop only.
(2) Sunday Mahjong Hummingbird tiles: the pile cutout had cognac/leather mat showing between the tiles; the leather is
    keyed to white (assets/tiles/v95/hbclean.py: large dark reddish-brown regions only, tile art untouched).
t.fo keeps the previous photo for locks. Usage: python3 v95_gatsby_hummingbird.py <build_dir>"""
import sys, os, io, json, base64, hashlib
from PIL import Image, ImageOps
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
FIX = {
    'shop.andersruff.com/green-light-gatsby-mahjong-tile-set': ('assets/tiles/v95/anders-ruff-green-light-gatsby-rack.jpg', 'centre'),
    'sundaymahjong.com/hummingbird-tile-set-1': ('assets/tiles/v95/sunday-mahjong-hummingbird-clean.jpg', 'whole'),
}
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
IMG = {}; os.makedirs(B + '/t95', exist_ok=True)
for k, (src, pile) in FIX.items():
    t = D['tiles'].get(k)
    if not t: print('missing tile', k); continue
    fn = 't95/' + os.path.basename(src)
    if t.get('full') == fn: print('already', k); continue
    im = Image.open(REPO + src).convert('RGB'); im.save(B + '/' + fn, quality=88)
    sq = im.crop((450, 0, 1150, 700)) if pile == 'centre' else ImageOps.fit(im, (360, 360), Image.LANCZOS)
    sq = sq.resize((360, 360), Image.LANCZOS); b = io.BytesIO(); sq.save(b, 'JPEG', quality=84)
    pk = 'p95' + hashlib.md5(fn.encode()).hexdigest()[:10]; IMG[pk] = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
    t.setdefault('fo', t.get('full')); t['full'] = fn; t['pile'] = pk
    if pile == 'centre': t['bf'] = [.5, .5]
    print('new photo', t['n'], '->', fn)
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
if IMG:
    inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMG, separators=(',', ':')) + ');</script>'
    a = '<script src="b24v1.js"></script>'; assert h.count(a) == 1; h = h.replace(a, a + inl, 1)
open(P, 'w').write(h)
