"""FYM v87 catalog adds (Tiffany Oct 25):
- Bespoke Mahjong regular-size tile sets (15:19 "I don't want their mega tiles in, but they have other tiles that definitely should be in").
  Root cause they were missing: the first catalog harvest only took listings with 'tiles' in the title; Bespoke names sets
  "LUCKY CHARMS - MARSHMALLOW PINK" (product_type 'Mahjong Sets'), so only Mega/collab listings came in, and the Megas were hidden Oct 23.
  In-stock regular sets only (sold-out colours wait for restock). Photos picked by eye from each listing (tiles in that colourway).
- Tala Mahj (non-partner, ShopMy, no MAHJMATCH code -> ncn=1 'No code available at this time'): Tradewind tile sets + woven racks
  that are in her ShopMy 'Tala Mahj Favorites' collection (config/tala-shopmy-links.json).
Usage: python3 v87_adds.py <build_dir>"""
import sys, os, io, json, base64, hashlib, re
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
from skimage.color import rgb2lab, lab2rgb
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
T, R, sets = D['tiles'], D['racks'], D['sets']
BSP = 'www.bespokemahjong.com'; REF = '10217561.eoZg0pKJHSf8IQSE'
# handle, set name, photo index, tile-door colour group, title colour
BESPOKE = [
 ('lucky-charms-marshmallow', 'Lucky Charms (Marshmallow Pink)', 1, 'Pink', '#e58fb0'),
 ('popdivacottoncandy', 'Pop Diva (Cotton Candy Pearl)', 4, 'Pink', '#e58fb0'),
 ('pop-diva', 'Pop Diva (Bright White)', 1, 'Ivory', '#d6568a'),
 ('springtimesafaripetalpink', 'Springtime Safari (Petal Pink)', 1, 'Pink', '#d6568a'),
 ('springtimesafariskyblue', 'Springtime Safari (Sky Blue)', 1, 'Blue', '#2f9fa0'),
 ('chalettiles', 'The Chalet (Frosty Lilac)', 2, 'Purple', '#8a6fc0'),
 ('the-chalet-frostypearlwhite', 'The Chalet (Frosty Pearl White)', 2, 'Ivory', '#2f55c8'),
 ('pearlcream', 'Year of the Horse (Pearl Cream)', 1, 'Ivory', '#b0466b'),
 ('yearofhorsesaddlepink', 'Year of the Horse (Saddle Pink)', 1, 'Pink', '#d6568a'),
 ('gardenglowtiles', 'Garden Glow (Matcha Pearl)', 1, 'Green', '#3c9a55'),
 ('bespoke-x-gray-malin-getaway-dogs-mahjong-tiles-beverly-hills-pink', 'Gray Malin Getaway Dogs (Beverly Hills Pink)', 4, 'Pink', '#e57aa3'),
 ('bespoke-x-gray-malin-getaway-dogs-mahjong-tiles-aspen-blue', 'Gray Malin Getaway Dogs (Icy Blue)', 4, 'Blue', '#2f9fc8'),
 ('bespoke-x-gray-malin-getaway-dogs-mahjong-tiles-bright-white', 'Gray Malin Getaway Dogs (Bright White)', 1, 'Ivory', '#e57aa3'),
 ('gray-malin-beach-club-set-cabana-blue', 'Gray Malin Beach Club (Cabana Blue)', 1, 'Blue', '#2f6fc8'),
 ('bespoke-x-corey-paige-color-crush-set-pearl', 'Corey Paige Color Crush (Pearl Crush)', 1, 'Ivory', '#d6247f'),
 ('bespoke-x-corey-paige-color-crush-set-white', 'Corey Paige Color Crush (Bright White)', 1, 'Ivory', '#d6247f'),
 ('bespoke-x-grateful-dead-mahjong-tiles-rose-pink', 'Grateful Dead (Rose Pink Tie Dye Pearl)', 1, 'Pink', '#d6568a'),
 ('bespoke-x-grateful-dead-mahjong-tiles-sunshine-daydream', 'Grateful Dead (Sunshine Daydream Tie Dye Pearl)', 1, 'Yellow & Orange', '#d49a00'),
 ('bespoke-x-grateful-dead-mahjong-tiles-stealie-blue', 'Grateful Dead (Stealie Blue Tie Dye Pearl)', 1, 'Blue', '#2f55c8'),
]
TL = json.load(open(REPO + 'config/tala-shopmy-links.json'))
TALA_T = [('tradewind-mahjong-tiles-aqua-copy', 'Tradewind (Sage Jade)', 5, 'Green', '#2f7a5c'),
          ('tradewind-mahjong-tiles-emerald-jade', 'Tradewind (Emerald Jade)', 5, 'Green', '#0f6b4c'),
          ('tradewind-tiles-tortoise', 'Tradewind (Tortoise)', 2, 'Brown', '#6b3a1f'),
          ('tradewind-mahjong-tiles-aqua', 'Tradewind (Aqua)', 3, 'Blue', '#2f9fa0'),
          ('tradewind-tiles-pink', 'Tradewind (Petal)', 3, 'Pink', '#d6568a')]
TALA_R = [('horizon-rack', 'Tala Mahj Horizon Woven Rattan', 1, '#c8a274', ['neutral', 'wood']),
          ('shoreline-mahjong-rack-wavy-pusher-20-inches-set-of-4-ships-oct-1-chocolate-woven-rattan', 'Tala Mahj Shoreline Chocolate Woven Rattan', 0, '#5a3a26', ['dark', 'wood'])]
def kmeans_sw(im, k=6, minw=.05):
    a = np.asarray(im.convert('RGB').resize((72, 72))).astype(float).reshape(-1, 3) / 255
    a = a[~((a.min(1) > .82) & (a.max(1) - a.min(1) < .12))]
    if len(a) < 50: return []
    L = rgb2lab(a.reshape(-1, 1, 3)).reshape(-1, 3); km = KMeans(n_clusters=k, n_init=3, random_state=0).fit(L)
    cnt = np.bincount(km.labels_, minlength=k) / len(L); out = []
    for j in np.argsort(-cnt):
        if cnt[j] < minw: continue
        rgb = np.clip(lab2rgb(km.cluster_centers_[j].reshape(1, 1, 3)).reshape(3), 0, 1)
        out.append(['#%02x%02x%02x' % tuple(int(round(x * 255)) for x in rgb), round(float(cnt[j]), 3)])
    return out
os.makedirs(B + '/t87', exist_ok=True); IMG = {}; groups = {}; added = []; colour = {}
tmpl_s = next(s for s in sets if s['maker'] == 'Bespoke Mahjong')
def thumb(im, key, sz=360):
    w, hh = im.size; q = min(w, hh); pp = im.crop(((w - q) // 2, (hh - q) // 2, (w - q) // 2 + q, (hh - q) // 2 + q)).resize((sz, sz), Image.LANCZOS)
    b = io.BytesIO(); pp.save(b, 'JPEG', quality=84); IMG[key] = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
def add_tile(key, name, maker, imgpath, grp, tc, t):
    im = Image.open(imgpath).convert('RGB'); slug = re.sub(r'[^a-z0-9]+', '-', (maker + ' ' + name).lower()).strip('-')[:80]
    full = im.copy(); full.thumbnail((1000, 1000)); fn = f't87/{slug}.jpg'; full.save(f'{B}/{fn}', quality=88)
    pk = 'p87' + hashlib.md5(slug.encode()).hexdigest()[:10]; thumb(im, pk)
    t.update(n=name, bn=maker, full=fn, pile=pk, cat=True); t.pop('soon', None); t.pop('hid', None); t.pop('cs', None); T[key] = t
    s = next((x for x in sets if x['tile'] == key), None)
    if s is None: s = dict(tmpl_s); s.update(slug=slug, tile=key, m=[], album='', tag='', cat=True); s.pop('cr', None); sets.append(s)
    s.update(name=name, maker=maker, tc=tc); s.pop('hid', None)
    groups.setdefault(grp, []).append(name); added.append((maker, name, key)); colour[s['slug']] = {'sw': kmeans_sw(im), 'tone': None, 'src': 'photo', 'back': None}
for hnd, name, idx, grp, tc in BESPOKE:
    key = f'{BSP}/{hnd}'
    t = dict(T.get(key) or {}); t.update(u=f'https://bespokemahjong.com/discount/MAHJMATCH?redirect=%2Fproducts%2F{hnd}%3Fsca_ref%3D{REF}',
        u0=f'https://www.bespokemahjong.com/products/{hnd}?sca_ref={REF}', dc='https://mahjmatchmaker.com/bespoke-mahjong-discount-code', pa=True, nc=False, rt=False)
    add_tile(key, name, 'Bespoke Mahjong', f'/tmp/bsp/img/{hnd}-{idx}.jpg', grp, tc, t)
for hnd, name, idx, grp, tc in TALA_T:
    key = f'talamahj.com/{hnd}'
    t = dict(u=TL['tiles'][hnd], u0=f'https://talamahj.com/products/{hnd}', dc='', pa=False, nc=False, rt=False, ncn=1)
    add_tile(key, name, 'Tala Mahj', f'/tmp/tala/img/{hnd}-{idx}.jpg', grp, tc, t)
for hnd, name, idx, hx, rf in TALA_R:
    key = f'talamahj.com/{hnd}'; im = Image.open(f'/tmp/tala/img/{hnd}-{idx}.jpg').convert('RGB')
    rk = 'rk87' + hashlib.md5(key.encode()).hexdigest()[:8]; t = im.copy(); t.thumbnail((700, 700)); b = io.BytesIO(); t.save(b, 'JPEG', quality=84)
    IMG[rk] = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
    R[key] = dict(n=name, bn='Tala Mahj', b='Tala Mahj', u=TL['racks'][hnd], dc='', pa=False, nc=False, rt=False, c=False, ml=False, add='oct25',
                  sk=False, hx=hx, rf=rf, im=rk, ncn=1, u0=f'https://talamahj.com/products/{hnd}')
    added.append(('Tala Mahj', name, key))
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
j = h.index('const BACKG=') + len('const BACKG='); BG, bend = json.JSONDecoder().raw_decode(h[j:]); bend += j
for g, names in groups.items():
    BG.setdefault(g, [])
    for n in names:
        if n not in BG[g]: BG[g].append(n)
h = h[:j] + json.dumps(BG, ensure_ascii=False) + h[bend:]
inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMG, separators=(',', ':')) + ');</script>'
a = '<script src="b24v1.js"></script>'; assert h.count(a) == 1; h = h.replace(a, a + inl, 1)
open(P, 'w').write(h)
C = json.load(open(REPO + 'config/fym-colour-oct25.json')); C['sets'].update(colour); json.dump(C, open(REPO + 'config/fym-colour-oct25.json', 'w'), indent=0, ensure_ascii=False)
for x in added: print(*x)
print('added', len(added))
