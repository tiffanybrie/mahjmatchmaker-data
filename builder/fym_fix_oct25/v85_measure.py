"""FYM v85 colour fix, step 1: re-measure every mat and tile set WITHOUT blending colours, plus a clean/earthy tone.
Why (Tiffany Oct 25, Ash Burl got a pink floral first): the old mat swatches (D.mats[*].ms) came from a 5-colour median-cut that
AVERAGES neighbours, so Let's Be Besties Green Bright Floral (hot pink + red flowers) was stored as dusty rose / tan / sage, close to
Ash Burl's burl browns. And the ranking never used her clean-vs-earthy rule (doc 76).
Mats: k-means (k=8) in Lab on the mat photo (pulled out of the app's own image chunks), clusters >= 3% kept as they are (no merging),
tone from scripts/colors/families.read_image (bright / pastel / muted / blend).
Tiles: palette from config/tile-tones.json when it exists (white faces masked, doc 76), else k-means on the tile photo with near-white
faces dropped; tone from tile-tones (clean / transitional / earthy) else measured from the photo the same way.
Usage: python3 v85_measure.py <build_dir>  -> config/fym-colour-oct25.json"""
import sys, os, io, json, struct, re, base64
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
from skimage.color import rgb2lab, lab2rgb
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, REPO + '/scripts/colors')
from families import read_image, fam_arr
B = sys.argv[1]
h = open(B + '/index.html').read(); i = h.index('const D=') + 8; D, _ = json.JSONDecoder().raw_decode(h[i:])
TMP = '/tmp/v85img'; os.makedirs(TMP, exist_ok=True)

# --- mat images from the chunks
imgs = {}
for fn in os.listdir(B + '/mc'):
    p = B + '/mc/' + fn
    if fn.endswith('.webp'):
        raw = open(p, 'rb').read(); n = struct.unpack('<I', raw[-4:])[0]; hdr = json.loads(raw[-4 - n:-4])
        for f, (a, l) in hdr.items(): imgs[f] = raw[a:a + l]
    elif fn.endswith('.json'):
        for f, v in json.load(open(p)).items():
            if isinstance(v, str) and v.startswith('data:'): imgs[f] = base64.b64decode(v.split(',', 1)[1])

def kmeans_sw(a, k=8, minw=.03):
    """a: (N,3) rgb 0-1 -> [[hex, share]] unblended clusters"""
    if len(a) < 50: return []
    L = rgb2lab(a.reshape(-1, 1, 3)).reshape(-1, 3)
    km = KMeans(n_clusters=k, n_init=3, random_state=0).fit(L)
    cnt = np.bincount(km.labels_, minlength=k) / len(L)
    out = []
    for j in np.argsort(-cnt):
        if cnt[j] < minw: continue
        rgb = np.clip(lab2rgb(km.cluster_centers_[j].reshape(1, 1, 3)).reshape(3), 0, 1)
        out.append(['#%02x%02x%02x' % tuple(int(round(x * 255)) for x in rgb), round(float(cnt[j]), 3)])
    return out

def px(im, N=72):
    return np.asarray(im.convert('RGB').resize((N, N))).astype(float).reshape(-1, 3) / 255

res = {'about': __doc__.split('\n')[0], 'mats': {}, 'sets': {}}
for k, o in D['mats'].items():
    raw = imgs.get(o['f'])
    if raw is None: continue
    path = f"{TMP}/{re.sub(r'[^a-z0-9]+', '_', k.lower())[:90]}.png"
    im = Image.open(io.BytesIO(raw)).convert('RGB'); im.save(path)
    a = px(im)
    a = a[~((a.min(1) > .94))]  # drop pure white product background only
    _, tone, _ = read_image(path)
    res['mats'][k] = {'sw': kmeans_sw(a), 'tone': tone}
print('mats measured', len(res['mats']), 'of', len(D['mats']))

TT = json.load(open(REPO + '/config/tile-tones.json'))['sets']
nm = lambda x: re.sub(r'[^a-z0-9]', '', (x or '').lower())
TBN = {nm(v.get('name')) + '|' + nm(v.get('brand')): v for v in TT.values() if isinstance(v, dict)}
TBN1 = {}
for v in TT.values():
    if isinstance(v, dict): TBN1.setdefault(nm(v.get('name')), []).append(v)
def tile_tone_from_photo(im):
    a = px(im); f, hh, l, s = fam_arr(a)
    face = (a.min(1) > .82) & (a.max(1) - a.min(1) < .12)  # ivory/white tile faces
    keep = ~face
    if keep.sum() < 50: return 'clean'
    ff, ss, ll = f[keep], s[keep], l[keep]
    earthy = np.isin(ff, ['brown', 'gold']) | ((ss < .3) & (ll > .15) & (ll < .7)) | ((ll < .3) & (ss >= .25))
    clean = ~earthy & (ss >= .45) & (ll >= .35)
    e, c = earthy.mean(), clean.mean()
    return 'earthy' if e >= .55 and c < .2 else ('clean' if c >= .35 and e < .4 else 'transitional')
for s in D['sets']:
    tt = TT.get(s['slug']) or TBN.get(nm(s['name']) + '|' + nm(s['maker']))
    if not tt and len(TBN1.get(nm(s['name']), [])) == 1: tt = TBN1[nm(s['name'])][0]
    t = D['tiles'].get(s['tile']) or {}; f = t.get('full'); im = None
    if f and os.path.exists(B + '/' + f): im = Image.open(B + '/' + f).convert('RGB')
    if tt and tt.get('palette'): sw = [[hx, w] for hx, w in tt['palette'] if w >= .04]; src = 'tile-tones'
    elif im is not None:
        a = px(im); a = a[~((a.min(1) > .82) & (a.max(1) - a.min(1) < .12))]; sw = kmeans_sw(a, 6, .05); src = 'photo'
    else: sw, src = [], 'none'
    tone = (tt or {}).get('tone') or (tile_tone_from_photo(im) if im is not None else None)
    res['sets'][s['slug']] = {'sw': sw, 'tone': tone, 'src': src, 'tone_src': 'tile-tones' if (tt or {}).get('tone') else 'photo'}
json.dump(res, open(REPO + '/config/fym-colour-oct25.json', 'w'), indent=0, ensure_ascii=False)
from collections import Counter
print('set tones', Counter(v['tone'] for v in res['sets'].values()), 'src', Counter(v['src'] for v in res['sets'].values()))
print('mat tones', Counter(v['tone'] for v in res['mats'].values()))
