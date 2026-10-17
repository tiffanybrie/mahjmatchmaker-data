"""Oct 16: Let's Be Besties joins Find Your Match (new affiliate, code MAHJMATCH).
Tiffany screenshotted the 40 mats she wants in (her picks = the curated list); photos come from the shop.
Same mechanics as fym_catalog_add_oct16.py: new m/N numbers in new mc chunks, thumbs in a new IMG bundle,
ranks re-sorted by palette similarity with her matches first.
Usage: python3 fym_lbb_add_oct16.py <live index.html> <products.json> <handles.json> <out dir> <bundle name>"""
import json, sys, io, os, base64, hashlib, subprocess, collections, re
import numpy as np
from PIL import Image
sys.path.insert(0, '/tmp/cc'); sys.path.insert(0, '/tmp/sw')
from profile import prof
from skimage.color import rgb2lab, deltaE_ciede2000
idx_html, PROD, HANDLES, OUT, BUN = sys.argv[1:6]
R = '/home/claude/mahjmatchmaker-data/'
src = open(R + 'builder/fym_catalog_add_oct16.py').read()
# pull helper defs from the sibling script so both stay identical
ns = {}
helpers = src[src.index('def hx('):src.index('os.makedirs(OUT')]
helpers = helpers.replace("names = list(PAL)", "from profile import PAL\nnames = list(PAL)")
exec('import numpy as np, re, os, subprocess\nfrom PIL import Image\nfrom skimage.color import rgb2lab, deltaE_ciede2000\n' + helpers, ns)
t = open(idx_html).read(); i0 = t.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(t[i0:])
P = {p['handle']: p for p in json.load(open(PROD))}
H = list(dict.fromkeys(json.load(open(HANDLES)).values()))
os.makedirs(OUT + '/img', exist_ok=True); os.makedirs(OUT + '/mc', exist_ok=True)
B = {}
def uri(im, fmt, q, w):
    im = im.copy(); im.thumbnail((w, w)); b = io.BytesIO()
    im.convert('RGBA' if fmt in ('WEBP', 'PNG') else 'RGB').save(b, fmt, quality=q)
    v = f'data:image/{fmt.lower()};base64,' + base64.b64encode(b.getvalue()).decode(); h = hashlib.md5(v.encode()).hexdigest()[:10]; B[h] = v; return h
maxN = max(int(v['f'].split('/')[1].split('.')[0]) for v in D['mats'].values())
N = (maxN // 12 + 1) * 12; MCH = collections.defaultdict(dict); added = []; flagged = []
BN = "Let's Be Besties"; HOST = 'letsbebesties.com'; REF = '?sca_ref=12515508.SUyXEjJsqV'
# photo picked by eye where the first listing image is a promo graphic or a table shot (Oct 16)
IMGIDX = {'coral-lake-mahjong-mat': 4, 'tobacco-leaves-blue-neoprene-mahjong-mat': 0, 'winter-jewel-neoprene-mahjong-mat': 3,
          'pink-blooms-mahjong-mat-neoprene': 2, 'royal-peacock-mahjong-mat': 3, 'purple-and-pink-plaid-mahjong-mat': 1, 'talulah-panda-neoprene-mahjong-mat': 2}
D['logos'][BN] = uri(Image.open(R + 'assets/brand/partner-logos/lets-be-besties.png'), 'WEBP', 90, 300)
for h in H:
    p = P.get(h)
    if not p: flagged.append((h, 'not in feed')); continue
    key = f'{HOST}/{h}'
    if key in D['mats']: continue
    im0 = p['images'][IMGIDX[h]] if h in IMGIDX else ns['pick_img'](p)
    if not im0: flagged.append((h, 'no photo')); continue
    s = im0['src'].split('?')[0] + '?width=1400'
    im = ns['get'](s, OUT + '/img/' + hashlib.md5(s.encode()).hexdigest()[:12] + '.jpg').convert('RGB')
    im = ns['trim'](im); full = im.copy(); full.thumbnail((640, 640)); b = io.BytesIO(); full.save(b, 'WEBP', quality=82)
    f = f'm/{N}.webp'; MCH[N // 12][f] = 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode(); N += 1
    pr = prof(im, p['title']) or {'sw': [], 'tone': 'neutral'}
    name = ns['clean_mat'](p['title'])
    name = re.sub(r'\s*(Neoprene|Leatherette|Artist Collab|Tabletop|\(.*?\))', '', name).strip(' ,:-') or name
    D['mats'][key] = dict(n=name, bn=BN, b=BN, u=f'https://{HOST}/products/{h}' + REF, dc='https://mahjmatchmaker.com/lets-be-besties-discount-code', pa=True, nc=False, rt=False, c=False, ml=False,
                          add='oct16lbb', f=f, th=uri(im, 'JPEG', 70, 150), w=full.width, h=full.height,
                          mf=ns['fams'](pr['sw']), ms=[[hh, round(sc, 2)] for n, hh, sc in pr['sw']], hol=pr['tone'] == 'holiday')
    D['order'].append(key); added.append(key)
SWJ = json.load(open('/tmp/sw/swipe.json')); TS = SWJ['ts']; lab = ns['lab']
order = D['order']; ix = {m: i for i, m in enumerate(order)}
ML = {m: [(lab(hh), w) for hh, w in D['mats'][m]['ms']] for m in order if D['mats'][m].get('ms')}
def sim(A, Bv):
    la = np.array([a for a, _ in A]); wa = np.array([w for _, w in A]); lb = np.array([b for b, _ in Bv])
    Dm = deltaE_ciede2000(np.repeat(la, len(lb), 0), np.tile(lb, (len(la), 1))).reshape(len(la), len(lb))
    return float((Dm.min(1) * wa).sum() / wa.sum())
for st in D['sets']:
    her = [m for m, _ in st['m'] if m in ix]
    T = [(lab(hh), w) for hh, w in TS.get(st['slug'], [])]
    if not T: st['rank'] = st['rank'] + [ix[m] for m in added]; continue
    rest = [m for m in order if m not in her]
    sc = sorted(((0.6 * sim(T, ML[m]) + 0.4 * sim(ML[m], T) + (25 if D['mats'][m].get('hol') else 0)) if m in ML else 999, m) for m in rest)
    st['rank'] = [ix[m] for m in dict.fromkeys(her)] + [ix[m] for _, m in sc]
    assert len(st['rank']) == len(order), st['slug']
for c, o in MCH.items(): json.dump(o, open(f'{OUT}/mc/{c}.json', 'w'), separators=(',', ':'))
open(f'{OUT}/{BUN}', 'w').write('window.IMG=Object.assign(window.IMG||{},' + json.dumps(B, separators=(',', ':')) + ');')
t2 = t[:i0] + json.dumps(D, separators=(',', ':'), ensure_ascii=False) + t[i0 + end:]
last = re.findall(r'<script src="b\dv\d+\.js"></script>', t2)[-1]
t2 = t2.replace(last, last + f'<script src="{BUN}"></script>', 1)
open(OUT + '/index.html', 'w').write(t2)
json.dump(dict(added=added, flagged=flagged, chunks=sorted(MCH)), open(OUT + '/added.json', 'w'), indent=1)
print('mats', len(D['mats']), 'added', len(added), 'flagged', flagged, 'chunks', sorted(MCH))
