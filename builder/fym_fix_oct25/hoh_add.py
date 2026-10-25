"""FYM Oct 25: House of Hearts Studio (houseofheartsstudio.com, artist Jenni Horne; Wix store) whole mat line.
Tiffany Oct 25 11:06: NOT an affiliate brand, but add ALL its mats; label them "No code available at this time"; FYM only for now
(no existing albums), candidates for new albums later. Whole-line non-partner allow (builder/fym_flags/nonpartner_allow.json brands).
One row per design, full table size listing (travel sizes are a catalog skip, like every brand). Scarves ("One Size Available") are not mats.
Photos: image 0 of each listing = the brand's flat shot of the whole mat (small name label in one corner on 7 of 8), passes the FYM photo bar.
Colours: measured FYM-family shares (scripts/colors/build_accents.measure, pooled teal->blue, earthy->dark) + by-eye primary.
Peace on Earth = Holiday (snowflakes + the Christmas 'Peace on Earth' dove; brand sells it for the holiday season): hol, colours combo-only (ha).
App: new mat field ncn=1 -> shop row line "No code available at this time" (only these mats carry it).
Usage: python3 builder/fym_fix_oct25/hoh_add.py <site_dir> <out_dir>"""
import sys, os, json, shutil, re, io, base64, hashlib, struct
from PIL import Image
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
sys.path.insert(0, REPO + 'scripts/colors')
from build_accents import measure
SITE, OUT = sys.argv[1], sys.argv[2]
if not os.path.exists(OUT): shutil.copytree(SITE, OUT)
SRC = REPO + 'assets/mats/house-of-hearts-studio/'
BRAND = 'House of Hearts Studio'
# file, listing handle (full table size), name, mf (by eye + measured), mt tiers, hol, ha
MATS = [
    ('galene', 'galene-mahjong-mat-full-table-size-leatherette', 'Galene', ['blue'], [0], False, []),
    ('imago', 'imago-mahjong-mat', 'Imago', ['green', 'dark', 'yellow'], [0, 1, 1], False, []),
    ('peace-on-earth', 'peace-on-earth-mahjong-mat-full-table-size-leatherette', 'Peace on Earth', [], [], True, ['blue', 'green', 'red', 'pink']),
    ('rain-on-the-peonies', 'rain-on-the-peonies-mahjong-mat-full-table-mat', 'Rain on the Peonies', ['green', 'blue'], [0, 2], False, []),
    ('ruth', 'ruth-mahjong-mat-full-table-size-leatherette', 'Ruth', ['dark', 'green'], [0, 2], False, []),
    ('stella', 'stella-full-table-mahjong-matt-leatherette', 'Stella', ['green', 'red', 'dark'], [0, 1, 1], False, []),
    ('tabitha', 'tabitha-mahjong-mat-full-table-mat', 'Tabitha', ['orange', 'dark', 'red'], [0, 1, 2], False, []),
    ('vibrant-symphony', 'vibrant-symphony-mahjong-mat-full-table-size', 'Vibrant Symphony', ['blue', 'pink'], [0, 2], False, []),
]
TO = {'teal': 'blue', 'earthy': 'dark', 'brown': 'dark', 'gold': 'yellow'}
h = open(OUT + '/index.html').read(); i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
M = D['mats']
mcb = re.search(r'MCB=new Set\(\[([0-9, ]+)\]\);', h)
chunk = max(int(x) for x in mcb.group(1).split(',')) + 1
maxN = max(int(o['f'].split('/')[1].split('.')[0]) for o in M.values())
chunk = max(chunk, maxN // 12 + 1); n0 = chunk * 12
def palette(im):
    q = im.convert('RGB').resize((96, 96)).quantize(6, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette(); hist = q.histogram()[:6]; tot = sum(hist)
    return [[hx, round(s, 2)] for s, hx in sorted(((hist[j] / tot, '#%02x%02x%02x' % tuple(pal[j * 3:j * 3 + 3])) for j in range(6) if hist[j]), reverse=True)[:5]]
B = {}; CHUNK = []; added = []
for k, (fn, hd, name, mf, mt, hol, ha) in enumerate(MATS):
    key = 'houseofheartsstudio.com/' + hd
    if key in M: continue
    path = SRC + fn + '.jpg'
    im = Image.open(path).convert('RGB'); im.thumbnail((640, 640))
    b = io.BytesIO(); im.save(b, 'WEBP', quality=86, method=6); raw = b.getvalue()
    f = f'm/{n0 + k}.webp'; CHUNK.append((f, raw))
    t = im.copy(); t.thumbnail((150, 150)); b = io.BytesIO(); t.save(b, 'JPEG', quality=72)
    v = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode(); th = 'hh' + hashlib.md5(v.encode()).hexdigest()[:8]; B[th] = v
    shares = {}
    for fam, p in measure(path):
        fam = TO.get(fam, fam); shares[fam] = shares.get(fam, 0) + p
    M[key] = dict(n=name, bn=BRAND, b=BRAND, u=f'https://www.houseofheartsstudio.com/product-page/{hd}', dc='', pa=False, nc=False, rt=False,
                  c=False, ml=False, f=f, th=th, w=im.width, h=im.height, mf=mf, ms=palette(im), hol=hol, src='hoh-oct25', mt=mt,
                  sh=[round(shares.get(c, 0), 1) for c in mf], add='oct25-hoh', ncn=1)
    if ha: M[key]['ha'] = ha
    D['order'].append(key); added.append(key)
ix = {m: j for j, m in enumerate(D['order'])}
for s in D['sets']:
    for k in added: s['rank'].append(ix[k])
body, hdr = b'', {}
for f, raw in CHUNK: hdr[f] = [len(body), len(raw)]; body += raw
hj = json.dumps(hdr, separators=(',', ':')).encode()
assert not os.path.exists(f'{OUT}/mc/{chunk}.webp')
open(f'{OUT}/mc/{chunk}.webp', 'wb').write(body + hj + struct.pack('<I', len(hj)))
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
h = h.replace(mcb.group(0), 'MCB=new Set([' + mcb.group(1) + f', {chunk}]);', 1)
# thumbnails inline (no new jsDelivr file for the website copy)
last = '<script src="b24v1.js"></script>'
inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(B, separators=(',', ':')) + ');</script>'
if last in h: h = h.replace(last, last + inl, 1)
else:
    k2 = h.index('const D='); k2 = h.rfind('<script', 0, k2); h = h[:k2] + inl + h[k2:]
# shop row: "No code available at this time" for ncn mats
a = "${o.dc?`<a class=\"dc\" href=\"${esc(o.dc)}\" target=\"_blank\" rel=\"noopener\">Discount code ›</a>`:''}"
assert h.count(a) == 1, h.count(a)
h = h.replace(a, a + "${o.ncn&&!o.dc?'<em class=\"ncn\">No code available at this time</em>':''}", 1)
css = '.si a.dc{'
assert css in h
h = h.replace(css, '.si em.ncn{display:block;font-size:11.5px;color:var(--mute);font-style:normal;margin-top:2px} ' + css, 1)
open(OUT + '/index.html', 'w').write(h)
print('added', len(added), 'chunk', chunk, 'mats', len(M))
for k in added: o = M[k]; print(' ', o['n'], o['mf'], o['mt'], o['sh'], 'hol' if o['hol'] else '', o.get('ha', ''))
