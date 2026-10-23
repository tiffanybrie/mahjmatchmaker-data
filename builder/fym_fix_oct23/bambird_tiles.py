"""Bam Bird Boutique: every tile set, one row per colorway (Tiffany Oct 23 2:58pm).
Source: bambirdboutique.com Game Essentials > Tiles (products.json). No travel sets, no replacement tiles, no decor/event items.
 Classic: Rose, Lavender, Teal | East Meets West: Emerald, Periwinkle | Origami: Azure, Timber
 Deco: Lagoon, Mulberry, Indigo | MCM: Navy/Olive, Olive/Pink | Boots & Bubbles: Blue Swirl, Pink Swirl
 + Classic Tortoise (album set, photo unchanged until her Canva file) + East Meets West Tortoise (kept).
Photos: picked by eye from each product's own images (tile backs + faces in that colorway), Oct 23.
Existing keys keep their place (first colorway); the other colorways get key '<host>/<handle>?v=<variant id>'.
Usage: python3 bambird_tiles.py <build_dir> <products.json> <img dir>"""
import sys, os, io, json, base64, hashlib
import numpy as np
from PIL import Image
from skimage.color import rgb2lab, deltaE_ciede2000
def lab(hx): return rgb2lab(np.array([[[int(hx[k:k + 2], 16) / 255 for k in (1, 3, 5)]]]))[0, 0]
def swatches(im, n=5):
    sm = im.copy(); sm.thumbnail((240, 240)); a = np.asarray(sm.convert('RGB')).reshape(-1, 3)
    a = a[(a.min(1) < 225)]  # drop the white/clear background and acrylic glare
    if not len(a): return []
    q = Image.fromarray(a.reshape(-1, 1, 3).astype('uint8')).quantize(n, method=Image.Quantize.MEDIANCUT); pal = q.getpalette()[:n * 3]
    cnt = np.bincount(np.asarray(q).ravel(), minlength=n); tot = cnt.sum()
    return [('#%02x%02x%02x' % tuple(pal[k * 3:k * 3 + 3]), cnt[k] / tot) for k in np.argsort(-cnt) if cnt[k] / tot > .04]
def sim(A, Bv):
    la = np.array([a for a, _ in A]); wa = np.array([w for _, w in A]); lb = np.array([b for b, _ in Bv])
    Dm = deltaE_ciede2000(np.repeat(la, len(lb), 0), np.tile(lb, (len(la), 1))).reshape(len(la), len(lb))
    return float((Dm.min(1) * wa).sum() / wa.sum())
B, PJ, IMGD = sys.argv[1:4]
P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
prods = {p['handle']: p for p in json.load(open(PJ))['products']}
HOST = 'www.bambirdboutique.com'
# (handle, colour, set name, photo index, crop (top,bottom fractions) or None, title colour, tile-door colour group, reuse existing key?)
ROWS = [
 ('tiles-box-die', 'Rose', 'Classic (Rose)', 4, None, '#d9868c', 'Pink', True),
 ('tiles-box-die', 'Lavender', 'Classic (Lavender)', 0, (.29, .715), '#9a7fd1', 'Purple', False),
 ('tiles-box-die', 'Teal', 'Classic (Teal)', 5, None, '#3a9a98', 'Green', False),
 ('east-meets-west-tile-set', 'Emerald', 'East Meets West (Emerald)', 2, None, '#0f7a5c', 'Green', False),
 ('east-meets-west-tile-set', 'Periwinkle', 'East Meets West (Periwinkle)', 3, None, '#2f55d4', 'Blue', False),
 ('origami-tile-set', 'Azure', 'Origami (Azure)', 2, None, '#1d6fa3', 'Blue', True),
 ('origami-tile-set', 'Timber', 'Origami (Timber)', 3, None, '#8b3f1f', 'Brown', False),
 ('deco-tile-set', 'Lagoon', 'Deco (Lagoon)', 10, None, '#0d6b6e', 'Green', True),
 ('deco-tile-set', 'Mulberry', 'Deco (Mulberry)', 9, None, '#a3195b', 'Pink', False),
 ('deco-tile-set', 'Indigo', 'Deco (Indigo)', 15, None, '#2a3a7a', 'Blue', False),
 ('mcm-mahjong-tile-set', 'Navy/Olive', 'MCM (Navy/Olive)', 16, None, '#1f2a5a', 'Blue', True),
 ('mcm-mahjong-tile-set', 'Olive/Pink', 'MCM (Olive/Pink)', 14, None, '#7d8b2a', 'Green', False),
 ('boots-bubbles-mahjong-tile-set', 'Blue Swirl', 'Boots & Bubbles (Blue Swirl)', 10, None, '#6f8fe6', 'Blue', True),
 ('boots-bubbles-mahjong-tile-set', 'Pink Swirl', 'Boots & Bubbles (Pink Swirl)', 6, None, '#d0287a', 'Pink', False),
]
T = D['tiles']; sets = D['sets']
tmpl_t = T[HOST + '/deco-tile-set']; tmpl_s = next(s for s in sets if s['tile'] == HOST + '/deco-tile-set')
order = D['order']; ix = {m: k for k, m in enumerate(order)}
ML = {m: [(lab(hx), w_) for hx, w_ in D['mats'][m]['ms']] for m in order if D['mats'][m].get('ms')}
os.makedirs(B + '/t78', exist_ok=True); IMGS = {}; added = []; groups = {}
for hnd, col, name, idx, crop, tc, grp, reuse in ROWS:
    p = prods[hnd]; v = next(v for v in p['variants'] if v.get('option1') == col)
    key = HOST + '/' + hnd if reuse and (HOST + '/' + hnd) in T else HOST + f'/{hnd}?v={v["id"]}'
    im = Image.open(f'{IMGD}/{hnd}-{idx}.jpg').convert('RGB')
    if crop: w, hh = im.size; im = im.crop((0, int(hh * crop[0]), w, int(hh * crop[1])))
    full = im.copy(); full.thumbnail((1000, 1000)); slug = 'bam-bird-boutique-' + name.lower().replace('&', 'and').replace('/', '-').replace('(', '').replace(')', '').replace(' ', '-')
    fn = f't78/{slug}.jpg'; full.save(f'{B}/{fn}', quality=88)
    w, hh = im.size; q = min(w, hh); pp = im.crop(((w - q) // 2, (hh - q) // 2, (w - q) // 2 + q, (hh - q) // 2 + q)).resize((360, 360), Image.LANCZOS)
    b = io.BytesIO(); pp.save(b, 'JPEG', quality=84); pk = 'p78' + hashlib.md5(slug.encode()).hexdigest()[:10]
    IMGS[pk] = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
    base_u = tmpl_t['u'].split('?')[0] + '?redirect=' + f'%2Fproducts%2F{hnd}%3Fvariant%3D{v["id"]}%26sca_ref%3D10069575.cf1ZUJEgbaOpCDgy'
    t = dict(T.get(key) or tmpl_t); t.update(n=name, full=fn, pile=pk, u=base_u, u0=f'https://www.bambirdboutique.com/products/{hnd}?variant={v["id"]}', cat=True)
    t.pop('soon', None); t.pop('hid', None); T[key] = t
    s = next((x for x in sets if x['tile'] == key), None)
    if s is None:
        s = {k: v_ for k, v_ in tmpl_s.items()}; s.update(slug=slug, tile=key, m=[], album='', tag=''); sets.append(s)
    sw = swatches(im); TL = [(lab(hx), w_) for hx, w_ in sw]
    sc = sorted(((0.6 * sim(TL, ML[m]) + 0.4 * sim(ML[m], TL) + (25 if D['mats'][m].get('hol') else 0)) if m in ML else 999, m) for m in order)
    s.update(name=name, tc=tc, maker='Bam Bird Boutique', rank=[ix[m] for _, m in sc]); s.pop('hid', None)
    groups.setdefault(grp, []).append(name); added.append((name, key, fn))
# not tile sets: Giant decor tile, Mischief Mahj tasting event -> hidden (no set rows show them anyway)
for k in (HOST + '/giant-mahjong-tiles-set-of-3-for-decor', HOST + '/mischief-mahj-tiles-tastings-event-wed-oct-21'):
    if k in T: T[k]['hid'] = True
# rank for new sets = same as their template (catalog sets have no Tiffany matches; mats rank by colour)
open(f'{B}/b23v1.js', 'w').write('window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMGS) + ');')
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
if 'b23v1.js' not in h:
    assert h.count('<script src="b22v1.js"></script>') == 1
    h = h.replace('<script src="b22v1.js"></script>', '<script src="b22v1.js"></script><script src="b23v1.js"></script>', 1)
# tile-door colour groups (names are matched exactly)
j = h.index('const BACKG=') + len('const BACKG='); BG, bend = json.JSONDecoder().raw_decode(h[j:]); bend += j
for g, names in groups.items():
    BG.setdefault(g, [])
    for n in names:
        if n not in BG[g]: BG[g].append(n)
h = h[:j] + json.dumps(BG, ensure_ascii=False) + h[bend:]
open(P, 'w').write(h)
for a in added: print(*a)
print('sets now Bam Bird:', sum(1 for s in sets if s.get('maker') == 'Bam Bird Boutique' and not s.get('hid')))
