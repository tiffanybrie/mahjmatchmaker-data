"""Nov 22 daily ShopMy check: stages the 49 ShopMy mats found missing (config/shopmy-crosscheck-2026-11-22.json) as the FYM pending spec
config/fym-shopmy-nov22.json (same format as fym-shopmy-nov07.json; build with builder/fym_fix_nov07/shopmy_nov07.py after pointing SP at this spec)
+ photos assets/mats/shopmy-nov22/ + contact sheet assets/qa/shopmy-nov22/adds.jpg (LOOKED at). Run builder/fym_fix_nov22/fetch_shopmy_nov22.py first.
Photos = brand flat renders (Shopify product JSON), trimmed to the mat; Rebecca: image #1 (Apres, Tennis) is the flat render, #0 is lifestyle/held.
5 non-mats (matches, note card, watercolor kit/cards) go to config/shopmy-sync-skips.json."""
import os, re, json, sys
from PIL import Image, ImageChops, ImageDraw
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
sys.path.insert(0, REPO + 'scripts/colors')
from build_accents import measure
P = json.load(open(REPO + 'assets/qa/shopmy-nov22/products.json')); RAW = REPO + 'assets/qa/shopmy-nov22/raw/'
OUT = REPO + 'assets/mats/shopmy-nov22/'; os.makedirs(OUT, exist_ok=True)
NOTMAT = {'108973652', '108973831', '108973991', '108974191', '108975549'}
USE = {'108972069': (1, [0.03, 0.02, 0.99, 0.99]), '108972566': (1, [0.02, 0.02, 0.99, 0.99])}  # Rebecca: flat render image + crop
TO = {'teal': 'blue', 'earthy': 'dark', 'brown': 'dark', 'gold': 'yellow'}
def trim(im):
    bg = Image.new('RGB', im.size, im.getpixel((2, 2)))
    box = ImageChops.difference(im, bg).convert('L').point(lambda v: 255 if v > 28 else 0).getbbox()
    return im if not box else im.crop((max(0, box[0] - 4), max(0, box[1] - 4), min(im.width, box[2] + 4), min(im.height, box[3] + 4)))
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
EYE = {'108989670': ['neutral', 'blue'], '108994532': ['green', 'dark'], '108995034': ['pink', 'green'], '108972766': ['neutral', 'blue', 'green']}  # by-eye colours, contact sheet LOOKED at Nov 22 (light grey / dark teal / dusty pink+teal / white+blue)
mats, sheet = [], []
for pid, r in P.items():
    if pid in NOTMAT: continue
    mh = 'themahjonghouse.com' in r['url']; brand = 'The Mahjong House' if mh else 'Rebecca Illustrated'
    name = re.sub(r'\s*\(40% off.*$', '', r['title']).strip()
    if not mh: name = name.replace('APRÉS', 'Après').title().replace('-Mahjong Mat', '').replace(' Mahjong Mat', '').strip()
    k, crop = USE.get(pid, (0, 'trim'))
    im = Image.open(f'{RAW}{pid}_{k}.jpg').convert('RGB')
    if crop == 'trim': im = trim(im)
    else: W, H = im.size; im = im.crop((int(crop[0] * W), int(crop[1] * H), int(crop[2] * W), int(crop[3] * H)))
    im.thumbnail((1200, 1200)); fn = f'{slug(brand)}-{slug(name)}-{pid}.jpg'; im.save(OUT + fn, quality=90)
    sh = {}
    for fam, p in measure(OUT + fn): fam = TO.get(fam, fam); sh[fam] = sh.get(fam, 0) + p
    fams = [c for c, p in sorted(sh.items(), key=lambda kv: -kv[1]) if p >= 8][:4] or [max(sh, key=sh.get)]
    if pid in EYE: fams = EYE[pid]
    u = r['url'].split('?')[0]; key = re.sub(r'^https?://(www\.)?', '', u).replace('/products/', '/')
    mats.append(dict(key=key, name=name, brand=brand, b=brand, u=f'https://go.shopmy.us/p-{pid}', product_url=r['url'], img=f'assets/mats/shopmy-nov22/{fn}',
                     src=r['imgs'][k], crop=crop, hol=False, hid=False, reason='', **({'mf': EYE[pid], 'eye_why': 'by eye on the Nov 22 contact sheet'} if pid in EYE else {}), shopmy_id=int(pid), shelf='The Mahjong House' if mh else 'Rebecca Illustrated Mats',
                     measured=fams, note='brand flat render' if k == 0 and mh else 'brand render, trimmed'))
    sheet.append((name, brand, im, fams))
json.dump({'_note': "Nov 22 ShopMy daily check (scripts/checks/shopmy_sync_check.py, report config/shopmy-crosscheck-2026-11-22.json): 54 new ShopMy pins, 49 mats = 46 The Mahjong House (new shelf additions: Texas school mats, Double-Sided, Gem/Table/Trellis/Garden, travel sizes, Deco, solids) + 3 Rebecca Illustrated (Apres, Tennis in Paradise, Blue Hydrangeas). 5 pins are not mats (matches/note card/watercolor kit+cards) -> config/shopmy-sync-skips.json. All ShopMy-affiliated; link = go.shopmy.us, no code claim. Holiday: none judged from the full-size photos (Apres = ski chalet with garland/wreaths + champagne, winter not Christmas, kept year-round; flagged for Tiffany's eye). Photos LOOKED at: assets/qa/shopmy-nov22/adds.jpg. Goes into the next FYM release + Mat Gallery sync (gallery_sync.py). Not published.",
           'mats': mats, 'fixes': {}}, open(REPO + 'config/fym-shopmy-nov22.json', 'w'), indent=1, ensure_ascii=False)
T = 230; cols = 7; rows = (len(sheet) + cols - 1) // cols
S = Image.new('RGB', (T * cols, (T + 30) * rows), (24, 30, 58)); d = ImageDraw.Draw(S)
for j, (n, b, im, f) in enumerate(sheet):
    x, y = (j % cols) * T, (j // cols) * (T + 30); t = im.copy(); t.thumbnail((T - 8, T - 8)); S.paste(t, (x + 4, y + 28))
    d.text((x + 4, y + 2), f'#{j+1} {n}'[:38], fill=(255, 255, 255)); d.text((x + 4, y + 14), ','.join(f), fill=(255, 230, 120))
S.save(REPO + 'assets/qa/shopmy-nov22/adds.jpg', quality=82); print(len(mats), 'mats')
