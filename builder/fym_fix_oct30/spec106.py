"""v106 spec builder (Oct 30 eve): YOLO Mahjong full catalog + Noli June public mats (missed NEW PARTNER handoffs, Tiffany 5:16pm),
from the LIVE store feeds (refreshed vs data/brands/*-catalog). Writes config/fym-partner-adds-oct30c.json + assets/mats/v106/*.jpg.
Holiday by PHOTO (CLAUDE.md: only Christmas / Hanukkah / winter snowy-ski). Usage: python3 spec106.py <feed dir with yolo1..3.json, noli.json, img/>"""
import sys, json, os, shutil
import numpy as np
from PIL import Image
def trimcopy(src, dst):  # gate [89]: trim the white margin around the flat render (mat fills the frame)
    im = Image.open(src).convert('RGB'); a = np.asarray(im).astype(int); nw = ~((a.min(2) > 238))
    ys, xs = np.where(nw)
    if len(xs): im = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    im.save(dst, quality=92)
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
F = sys.argv[1]
YREF = '12572562.5IBLjBHZ1vuX4J'  # UpPromote ref (MATCH-INBOX Oct 29 2pm)
y = json.load(open(REPO + 'data/brands/yolo-mahjong-catalog-2026-10-28.json'))
nc = json.load(open(REPO + 'data/brands/noli-june-catalog-2026-10-30.json'))
ya = []
for p in (1, 2, 3): ya += json.load(open(f'{F}/yolo{p}.json'))['products']
yb = {p['handle']: p for p in ya}
NAMES = {
 'pre-order-neoprene-heritage-christmas-tartan-mahjong-mat-ship-rolled-up': 'Heritage Christmas Tartan',
 'preorder-neoprene-winter-ski-resort-square-mahjong-mat-ship-rolled-up': 'Winter Ski Resort',
 'journey-to-the-west-collection-mat-31-5-shipped-rolled': 'Journey to the West',
 'terracotta-diamond-mahjong-mat': 'Terracotta Diamond', 'loop-border-mahjong-mat': 'Loop Border', 'ivory-scroll-mahjong-mat': 'Ivory Scroll',
 'lavender-scroll-mahjong-mat': 'Lavender Scroll', 'golden-hour-ripple-mahjong-mat': 'Golden Hour Ripple', 'sage-ripple-mahjong-mat': 'Sage Ripple',
 'mocha-ripple-mahjong-mat': 'Mocha Ripple', 'blush-ripple-mahjong-mat': 'Blush Ripple', 'colorful-watercolor-peacock-mahjong-mat': 'Colorful Watercolor Peacock',
 'halloween-mandala-mahjong-mat': 'Halloween Mandala', 'plum-scallop-mahjong-mat': 'Plum Scallop',
 'blue-coral-watercolor-mahjong-mat': 'Blue Coral Watercolor', 'sage-pink-watercolor-mahjong-mat': 'Sage Pink Watercolor',
 'modern-abstract-watercolor-mahjong-mat': 'Modern Abstract Watercolor', 'blue-chinoiserie-peacock-mahjong-mat': 'Blue Chinoiserie Peacock',
 'whale-shark-coastal-mahjong-mat': 'Whale Shark Coastal', 'serene-pastel-turtles-mahjong-mat': 'Serene Pastel Turtles',
 'pastel-chinese-garden-mahjong-mat': 'Pastel Chinese Garden', 'scandinavian-green-leaf-mahjong-mat': 'Scandinavian Green Leaf',
 'pastel-parrot-square-mahjong-mat': 'Pastel Parrot', 'pastel-rainbow-round-mahjong-mat': 'Pastel Rainbow Round',
 'blue-chinoiserie-mahjong-mat': 'Blue Chinoiserie Village', 'pastel-parrot-round-mahjong-mat': 'Pastel Parrot Round',
 'botanical-garden-round-mahjong-mat': 'Botanical Garden Round', 'scalloped-pink-purple-mahjong-mat': 'Scalloped Pink and Purple',
 'scalloped-blue-green-mahjong-mat': 'Scalloped Blue and Green', 'pink-hydrangea-mahjong-mat': 'Pink Hydrangea',
 'pink-tropical-mahjong-mat': 'Pink Tropical', 'tropical-palm-beach-mahjong-mat': 'Tropical Palm Beach',
 'mahjong-mat-31-5x31-5-ship-rolled-up-blue-pastel-hydrangea-mahjong-mat-with-watercolor-floral-design': 'Blue Pastel Hydrangea',
 'pastel-hydrangea-mahjong-mat': 'Pastel Hydrangea',
 'mahjong-mat-31-5x31-5-ship-rolled-up-blue-hydrangea-mahjong-mat-with-soft-yellow-floral-border': 'Blue Hydrangea Yellow Floral',
 'mahjong-mat-31-5x31-5-ship-rolled-up-blue-chinoiserie-mahjong-mat-with-hydrangea-floral-design': 'Blue Chinoiserie Hydrangea',
 'mahjong-mat-green-dragon-scales-print-31-5-square-non-slip-table-mat': 'Green Dragon Scales', 'mahjong-mat-31-5x31-5-ship-folded-4': 'Hot Pink Crocodile',
 'mahjong-mat-31-5x31-5-ship-folded-3': 'Leopard Print', 'mahjong-mat-31-5x31-5-ship-folded-2': 'Tiger Print', 'mahjong-mat-martini-mahjong-mat-pink-orange': 'Martini',
 'mahjong-mat-miami-beach-vibes': 'Miami Beach Vibes', 'crane-moon-mahjong-mat-floral-chinese-mahjong-table-mat-for-mahjong-set-31-5-x-31-5-inch': 'Crane & Moon',
 'mahjong-mat-31-5x31-5-ship-rolled-up-2': 'Green Pickleball', 'mahjong-mat-blue-pool-float-mahjong-mat-summer-pool-party-mahjong-game-mat': 'Blue Pool Float',
}
HOL = {'pre-order-neoprene-heritage-christmas-tartan-mahjong-mat-ship-rolled-up', 'preorder-neoprene-winter-ski-resort-square-mahjong-mat-ship-rolled-up',
       'christmas-cat-square-mahjong-mat-ship-rolled-up', 'evergreen-christmas-plaid-mahjong-mat-ship-rolled-up', 'golden-christmas-mahjong-mat',
       'christmas-knit-mahjong-mat', 'christmas-botanical-bow-mahjong-mat', 'classic-christmas-plaid-mahjong-mat', 'christmas-holly-mahjong-mat'}
SKIP = {'mahjong-mat-preppy-pink-floral-mahjong-mat-watercolor-peony-hydrangea-game-mat': 'same artwork as Pink Hydrangea (pixel-identical image 0); one entry',
        'pink-tiger-mahjong-mat-floral-chinese-mahjong-table-mat-for-mahjong-set-31-5-x-31-5-inch': 'already in FYM as yolo:pink-tiger (her pick): relinked, not duplicated'}
def nm(h, t):
    if h in NAMES: return NAMES[h]
    import re
    t = re.sub(r'\(.*?\)', '', t); t = re.sub(r'(?i)\b(square|mahjong|mat|shipped|rolled|ship|up)\b', '', t)
    return re.sub(r'\s+', ' ', t).strip(' -')
mats, skipped = [], []
for h in y['mats']:
    if h in SKIP: skipped.append([h, SKIP[h]]); continue
    p = yb[h]; avail = any(v['available'] for v in p['variants'])
    src = f'{F}/img/yolo__{h}__0.jpg'; dst = f'assets/mats/v106/yolo-{h[:80]}.jpg'; trimcopy(src, REPO + dst)
    mats.append(dict(key=f'www.yolomahjong.com/{h}', name=nm(h, p['title']), bn='YOLO Mahjong', b='yolomahjong.com',
        u=f'https://www.yolomahjong.com/discount/MAHJMATCH?redirect=%2Fproducts%2F{h}%3Fsca_ref%3D{YREF}',
        u0=f'https://www.yolomahjong.com/products/{h}?sca_ref={YREF}', dc=y['dc'], pa=True, img=dst, hol=h in HOL, hid=not avail,
        reason='' if avail else 'sold out on yolomahjong.com', photo_note='brand image 0: clean flat render (corner curl), fills the frame'))
NB = {p['handle']: p for p in json.load(open(f'{F}/noli.json'))['products']}
NOLI_HOL = set()  # the 5 public mats: fall/Thanksgiving/Halloween/florals -> colour sections (falaladies Hanukkah/winter drop still hidden on nolijune.com)
for h in nc['mats_public']:
    p = NB[h]; src = f'{F}/img/noli__{h}__0.jpg'; dst = f'assets/mats/v106/noli-june-{h}.jpg'; trimcopy(src, REPO + dst)
    mats.append(dict(key=f'nolijune.com/{h}', name=p['title'], bn='Noli June', b='nolijune.com',
        u=f'https://nolijune.com/discount/MAHJMATCH?dt_id=3655694&redirect=%2Fproducts%2F{h}', u0=f'https://nolijune.com/products/{h}',
        dc=nc['dc'], pa=True, img=dst, hol=h in NOLI_HOL, hid=False, reason='', photo_note='brand image 0: clean flat render'))
json.dump(dict(_about=__doc__, made='2026-10-30', mats=mats, skipped=skipped, yolo_ref=YREF,
               bmin={'Noli June': '10% off $100+ with code MAHJMATCH'}), open(REPO + 'config/fym-partner-adds-oct30c.json', 'w'), indent=1, ensure_ascii=False)
print(len(mats), 'mats;', sum(m['hol'] for m in mats), 'holiday;', sum(m['hid'] for m in mats), 'hidden;', 'skipped', len(skipped))
