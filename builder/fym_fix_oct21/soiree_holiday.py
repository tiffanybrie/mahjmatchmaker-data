"""FYM Oct 21 evening, STAGED ONLY (pending queue -> v71 build): Soirée All Day holiday mats (Squarespace store, partner, code SOIREE via discount page).
Usage: python3 builder/fym_fix_oct21/soiree_holiday.py <site_dir> <out_dir>   (site_dir read only; out_dir copied from it)
Source: https://www.soireeallday.co/the-mahjong-collection?format=json (6 new mats; 5 Soirée mats were already in the app).
Photo verdict (looked at every image, contact sheets): image 0 of each product is the brand's clean flat render of the WHOLE mat, no tiles/props,
all six pass the FYM photo bar. All six are Christmas (4) / Hanukkah (1) / Santa+Christmas (1) = Holiday: hol=true, mf=[], mt=[], combo-only colours in ha.
Hidden-by-default: none. Questionable: none. Locked items touched: none (new keys only)."""
import sys, os, json, shutil, re, io, base64, hashlib, struct
from PIL import Image
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
SITE, OUT = sys.argv[1], sys.argv[2]
if not os.path.exists(OUT): shutil.copytree(SITE, OUT)
SRC = REPO + 'assets/mats/soiree-all-day/'
MATS = [  # handle, name, FYM combo-only colours (by eye + palette)
    ('toasty-and-tipsy-mahjong-mat', 'Toasty & Tipsy', ['pink', 'green', 'dark', 'orange']),
    ('poinsettia-party-mahjong-mat', 'Poinsettia Party', ['green', 'pink']),
    ('color-me-merry-mahjong-mat', 'Color Me Merry', ['pink', 'red', 'green']),
    ('pretty-in-pink-mahjong-mat', 'Pretty in Pink', ['pink', 'green']),
    ('home-for-the-holidays-mahjong-mat', 'Home for the Holidays', ['red', 'green']),
    ('star-of-david-hanukkah-mat', 'Star of David Hanukkah', ['blue', 'green']),
]
h = open(OUT + '/index.html').read(); i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
M = D['mats']
tmpl = M['soireeallday.co/lucky-hand-mahjong-mat']
B = {}; CHUNK = []
maxN = max(int(o['f'].split('/')[1].split('.')[0]) for o in M.values()); N = (maxN // 12 + 1) * 12
mcb = re.search(r'MCB=new Set\(\[([0-9, ]+)\]\);', h); chunk = max(int(x) for x in mcb.group(1).split(',')) + 1
assert N // 12 >= chunk or True
chunk = max(chunk, N // 12)
def palette(im):
    q = im.convert('RGB').resize((96, 96)).quantize(6, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette(); hist = q.histogram()[:6]; tot = sum(hist)
    return [[hx, round(s, 2)] for s, hx in sorted(((hist[j] / tot, '#%02x%02x%02x' % tuple(pal[j * 3:j * 3 + 3])) for j in range(6) if hist[j]), reverse=True)[:5]]
added = []; n0 = chunk * 12
for k, (hd, name, ha) in enumerate(MATS):
    key = 'soireeallday.co/' + hd
    if key in M: continue
    im = Image.open(REPO + 'assets/mats/gallery/soir-e-all-day--' + hd.replace('-mahjong-mat', '').replace('-hanukkah-mat', '-hanukkah') + '.webp').convert('RGB')
    b = io.BytesIO(); im.save(b, 'WEBP', quality=86, method=6); raw = b.getvalue()
    f = f'm/{n0 + k}.webp'; CHUNK.append((f, raw))
    t = im.copy(); t.thumbnail((150, 150)); b = io.BytesIO(); t.save(b, 'JPEG', quality=70)
    v = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode(); th = 'mt' + hashlib.md5(v.encode()).hexdigest()[:8]; B[th] = v
    M[key] = dict(n=name, bn='Soirée All Day', b='soireeallday.co', u=f'https://www.soireeallday.co/the-mahjong-collection/p/{hd}?ref=MAHJMATCH',
                  dc=tmpl['dc'], pa=True, nc=False, rt=False, c=False, ml=False, f=f, th=th, w=im.width, h=im.height, mf=[], ms=palette(im), hol=True,
                  src='soiree-oct21', mt=[], ha=ha, sh=[], add='oct21-soiree')
    D['order'].append(key); added.append(key)
ix = {m: i for i, m in enumerate(D['order'])}
for s in D['sets']:
    for k in added: s['rank'].append(ix[k])
body, hdr = b'', {}
for f, raw in CHUNK: hdr[f] = [len(body), len(raw)]; body += raw
hj = json.dumps(hdr, separators=(',', ':')).encode()
assert not os.path.exists(f'{OUT}/mc/{chunk}.webp')
open(f'{OUT}/mc/{chunk}.webp', 'wb').write(body + hj + struct.pack('<I', len(hj)))
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
h = h.replace(mcb.group(0), 'MCB=new Set([' + mcb.group(1) + f', {chunk}]);', 1)
last = '<script src="b18v1.js"></script>'; assert h.count(last) == 1 and 'b19v1.js' not in h
h = h.replace(last, last + '<script src="b19v1.js"></script>', 1)
open(OUT + '/b19v1.js', 'w').write('window.IMG=Object.assign(window.IMG||{},' + json.dumps(B, separators=(',', ':')) + ');')
open(OUT + '/index.html', 'w').write(h)
print('added', len(added), 'chunk', chunk, 'mats', len(M))
