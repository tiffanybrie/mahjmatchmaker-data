"""Nov 7 ShopMy cross-check (Tiffany 7:45pm: "It doesn't appear that all of my Luna EK studio mats were brought in ... This needs a
cross check"). Writes the FYM pending spec config/fym-shopmy-nov07.json + photos assets/mats/shopmy-nov07/ + contact sheet
assets/qa/shopmy-nov07/adds.jpg for the ShopMy mats that are in neither FYM nor the Mat Gallery (scripts/checks/shopmy_sync_check.py).
Photos: the brand's own flat render (Shopify /products/<handle>.json, full size) where one exists, else the ShopMy pin photo
(static.shopmy.us/pins/<file>), cropped to the mat. LOOKED at on the contact sheet. Holiday calls from the full-size photos.
Run once; idempotent (re-downloads only missing files). Usage: python3 builder/fym_fix_nov07/prep_shopmy_nov07.py"""
import os, io, json, subprocess, urllib.request
from PIL import Image, ImageDraw, ImageChops
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
OUT = REPO + 'assets/mats/shopmy-nov07/'; QA = REPO + 'assets/qa/shopmy-nov07/'
os.makedirs(OUT, exist_ok=True); os.makedirs(QA, exist_ok=True)
PIN = 'https://static.shopmy.us/pins/'
CDN_CM = 'https://cdn.shopify.com/s/files/1/0347/8496/8840/files/'
# (shelf, brand, store label b, name, pin id, product url (key source), photo url, crop | 'trim' | None, hol, hid, reason, note)
A = [
 # Mahj & Moon (Etsy shop MahjandMoonCo) - pinned Oct 27 (docs/SHOPMY-MAHJ-MOON-oct27.md) but never paired to an FYM mat
 ('Mahj & Moon (Etsy)', 'Mahj & Moon', 'Etsy', 'Tropical Toucan Pink Palm', 98067338, 'https://www.etsy.com/listing/4524615723',
  PIN + 'zoom-98067338.jpg', [0.06, 0.02, 0.94, 0.93], False, False, '', 'pin photo (overhead, pink racks on the edges); FYM key mahjandmoon.com/tropical-toucan-mahjong-mat now shows French Country Estate, so the toucan was never in FYM'),
 ('Mahj & Moon (Etsy)', 'Mahj & Moon', 'Etsy', 'Palm Tree Retro Tropical', 98073830, 'https://www.etsy.com/listing/4577957885',
  PIN + 'zoom-98073830.jpg', [0.07, 0.15, 0.94, 0.81], False, False, '', 'pin mockup on a table, cropped to the mat'),
 ('Mahj & Moon (Etsy)', 'Mahj & Moon', 'Etsy', 'Vintage Floral Pink', 98073909, 'https://www.etsy.com/listing/4575845329',
  PIN + 'zoom-98073909.jpg', [0.07, 0.15, 0.94, 0.81], False, False, '', 'pin mockup on a table, cropped to the mat'),
 ('Mahj & Moon (Etsy)', 'Mahj & Moon', 'Etsy', 'Lobster Coastal', 98074016, 'https://www.etsy.com/listing/4566953251',
  PIN + 'zoom-98074016.jpg', [0.05, 0.15, 0.94, 0.81], False, False, '', 'pin mockup on a table, cropped to the mat'),
 ('Mahj & Moon (Etsy)', 'Mahj & Moon', 'Etsy', 'Scalloped Pink Floral', 98074048, 'https://www.etsy.com/listing/4600985202',
  PIN + 'zoom-98074048.jpg', [0.10, 0.12, 0.90, 0.90], False, False, '', 'pin mockup, cropped to the mat'),
 # Rebecca Illustrated (ShopMy 15%, Tiffany Oct 22 "add her in"; whole shelf never added)
 ('Rebecca Illustrated Mats', 'Rebecca Illustrated', 'Rebecca Illustrated', 'Pool Pawty', 96620624, 'https://rebeccaillustrated.com/products/pool-pawty-mahjong-mat-preorder', 'shopify:1', None, False, False, '', 'brand flat render'),
 ('Rebecca Illustrated Mats', 'Rebecca Illustrated', 'Rebecca Illustrated', 'Canaries', 96620667, 'https://rebeccaillustrated.com/products/canaries-mahjong-mat-preorder', 'shopify:1', None, False, False, '', 'brand flat render'),
 ('Rebecca Illustrated Mats', 'Rebecca Illustrated', 'Rebecca Illustrated', 'Chinoiserie & Citrus', 96620673, 'https://rebeccaillustrated.com/products/chinoiserie-citrus-mahjong-mat-preorder', 'shopify:1', None, False, False, '', 'brand flat render'),
 ('Rebecca Illustrated Mats', 'Rebecca Illustrated', 'Rebecca Illustrated', 'White Sailboats', 96620684, 'https://rebeccaillustrated.com/products/white-sailboats-mahjong-mat-preorder', 'shopify:1', None, False, False, '', 'brand flat render'),
 ('Rebecca Illustrated Mats', 'Rebecca Illustrated', 'Rebecca Illustrated', 'Maxine', 96620690, 'https://rebeccaillustrated.com/products/maxine-mahjong-mat-preorder', 'shopify:0', None, False, False, '', 'brand flat render'),
 ('Rebecca Illustrated Mats', 'Rebecca Illustrated', 'Rebecca Illustrated', 'Pink Gingham', 96620594, 'https://rebeccaillustrated.com/products/pink-gingham-mahjong-mat-preorder', 'shopify:1', None, False, False, '', 'brand flat render'),
 ('Rebecca Illustrated Mats', 'Rebecca Illustrated', 'Rebecca Illustrated', 'Girly Bar Cart', 96620635, 'https://rebeccaillustrated.com/products/girly-bar-cart-mahjong-mat', 'shopify:0', None, False, True,
  'Only in-play photos: hands, tiles and drinks over the mat, angled (Oct 26 audit: Questionable). Needs a flat render from Rebecca.', ''),
 ('Rebecca Illustrated Mats', 'Rebecca Illustrated', 'Rebecca Illustrated', 'Pickle Ball', 96620638, 'https://rebeccaillustrated.com/products/pickle-ball-mahjong-mat', 'shopify:0', None, False, True,
  'Only in-play photos: hands and tiles over the mat (Oct 26 audit: Questionable). Needs a flat render from Rebecca.', ''),
 # Waiting On Martha Home
 ('Waiting on Martha', 'Waiting On Martha', 'Waiting On Martha', 'Cocktails Double Sided', 97201552, 'https://www.waitingonmarthahome.com/products/cocktails-double-sided-mahjong-mat-pre-order', 'shopify:0', 'trim', False, False, '', 'brand render (side A, side B wave stripe shows on the turned corner); also pinned on More Mahjong Mats (97598044)'),
 ('Merry Mahjong', 'Waiting On Martha', 'Waiting On Martha', 'Vintage Twinkle Double Sided', 97201863, 'https://www.waitingonmarthahome.com/products/vintage-twinkle-double-sided-mahjong-mat-pre-order', 'shopify:0', 'trim', True, False, '', 'pink/green Christmas trees = Holiday'),
 ('More Mahjong Mats', 'Waiting On Martha', 'Waiting On Martha', "Tasslin' Double Sided", 97597942, 'https://www.waitingonmarthahome.com/products/tasslin-double-sided-mahjong-mat-pre-order', 'shopify:0', 'trim', False, False, '', 'brand render; pre-order'),
 # The Mahjong House
 ('The Mahjong House', 'The Mahjong House', 'The Mahjong House', 'Ruby Table Double-Sided', 97678570, 'https://themahjonghouse.com/products/ruby-table-double-sided-mahjong-mat', 'shopify:2', 'trim', False, False, '', 'brand flat render (solid red, vegan leather type: lower bar)'),
 # Southern Living at Dillard's (ShopMy)
 ('More Mahjong Mats', 'Southern Living', "Dillard's", 'Green Ikat', 96621246, 'https://www.dillards.com/p/southern-living-mahjong-green-ikat-mat/521254772', PIN + '@96621246', 'trim', False, False, '', 'pin photo = brand flat render'),
 ('More Mahjong Mats', 'Southern Living', "Dillard's", 'Status Cats Pink', 96621255, 'https://www.dillards.com/p/southern-living-mahjong-status-cats-pink-mat/521231215', PIN + '@96621255', 'trim', False, False, '', 'pin photo = brand flat render'),
 ('More Mahjong Mats', 'Southern Living', "Dillard's", 'Bird Floral', 96621244, 'https://www.dillards.com/p/southern-living-mahjong-bird-floral-mat/521254771', PIN + '@96621244', 'trim', False, False, '', 'pin photo = brand flat render'),
 # Case-Mate (one ShopMy pin, 4 colourways on the product page; each colourway is its own FYM mat, same link)
 ('More Mahjong Mats', 'Case-Mate', 'Case-Mate', 'Classic Tortoiseshell', 96620523, 'https://case-mate.com/products/mahjong-mats?variant=67665869209736', 'cm:67665869209736', 'trim', False, False, '', 'variant render; link opens the product page (pick the colour there)'),
 ('More Mahjong Mats', 'Case-Mate', 'Case-Mate', 'Classic Carolina Blue', 96620523, 'https://case-mate.com/products/mahjong-mats?variant=67665869242504', 'cm:67665869242504', 'trim', False, False, '', 'variant render'),
 ('More Mahjong Mats', 'Case-Mate', 'Case-Mate', 'Classic Ballet Pink', 96620523, 'https://case-mate.com/products/mahjong-mats?variant=67665869275272', 'cm:67665869275272', 'trim', False, False, '', 'variant render'),
 ('More Mahjong Mats', 'Case-Mate', 'Case-Mate', 'Classic Cabana Stripe', 96620523, 'https://case-mate.com/products/mahjong-mats?variant=67665869406344', 'cm:67665869406344', 'trim', False, False, '', 'variant render'),
 # Tuckernuck x Oh My Mahjong collab (sold by Tuckernuck through ShopMy, no OMM code)
 ('Collab Mats', 'Tuckernuck', 'Tuckernuck', 'In Full Bloom (Oh My Mahjong x Tuckernuck)', 96621282, 'https://tnuck.com/products/in-full-bloom-mat-in-tube', 'shopify:0', 'trim', False, False, '', 'brand photo on a beige ground, trimmed to the mat'),
]
FIXES = {
 'hide': {'www.etsy.com/listing/4547277502/mahjong-mat-non-slip-tabletop-mat-home': {
     'name': 'Hummingbird Floral Frame (Mint)', 'brand': 'Luna EK Studio',
     'reason': 'The photo (ShopMy pin + Etsy listing photo) shows a koi + bamboo pond mat, not the mint hummingbird frame in the name (different product). The Mat Gallery already holds it (config/mat-gallery-photo-holds.json). Hidden + Questionable until a photo of the right mat exists.'}},
 'link': {'rebecca:rainbow-row': {'u': 'https://go.shopmy.us/p-96620630', 'why': "Rainbow Row (her album mat) has NO shop link in FYM or the gallery; her ShopMy Rebecca Illustrated pin earns 15% (Tiffany Oct 22). Link-only fix."},
          'mahjandmoon.com/blue-pastel-palm-beach-mahjong-mat': {
     'u': 'https://go.shopmy.us/p-98067163', 'etsy_url': 'https://www.etsy.com/listing/4350720810',
     'why': "Her ShopMy pin 'Palm Beach Preppy Mahjong Mat' (Mahj & Moon (Etsy), Oct 27) is this mat (matched by eye Nov 7: pale-blue edge, pink/green palm scenes, pink lattice centre). mahjandmoon.com links earn no commission; the Etsy pin earns 6%."}},
}

def fetch(url, path):
    if os.path.exists(path): return
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    open(path, 'wb').write(urllib.request.urlopen(req, timeout=60).read())

def shopify_img(url, n):
    import re
    m = re.match(r'https?://([^/]+)/products/([^/?#]+)', url)
    req = urllib.request.Request(f'https://{m.group(1)}/products/{m.group(2)}.json', headers={'User-Agent': 'Mozilla/5.0'})
    return json.load(urllib.request.urlopen(req, timeout=60))['product']['images'][n]['src']

_PINS = {}
def pin_img(pid):
    if _PINS: return _PINS.get(pid)
    req = urllib.request.Request('https://api.shopmy.us/api/Users/username/mahjmatchmaker', headers={'User-Agent': 'Mozilla/5.0'})
    for c in json.load(urllib.request.urlopen(req, timeout=60))['user']['collections']:
        r = urllib.request.Request(f"https://apiv3.shopmy.us/api/Collections/{c['id']}", headers={'User-Agent': 'Mozilla/5.0'})
        for p in json.load(urllib.request.urlopen(r, timeout=60)).get('pins') or []:
            _PINS[p['id']] = PIN + p['image'].split('/')[-1]
    return _PINS.get(pid)

def trim(im):
    bg = Image.new('RGB', im.size, im.getpixel((2, 2)))
    diff = ImageChops.difference(im, bg).convert('L').point(lambda v: 255 if v > 28 else 0)
    box = diff.getbbox()
    if not box: return im
    pad = 4; return im.crop((max(0, box[0] - pad), max(0, box[1] - pad), min(im.width, box[2] + pad), min(im.height, box[3] + pad)))

def re_etsy_bare(u):
    import re
    return bool(re.match(r'https?://www\.etsy\.com/listing/\d+/?$', u))

def slug(s):
    import re
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

def key_of(url):
    import re
    u = url.split('?')[0]; v = re.search(r'variant=(\d+)', url)
    m = re.match(r'https?://(?:www\.)?(etsy\.com/listing/\d+/[^/?]+)', url)
    if m: return 'www.' + m.group(1)
    m = re.match(r'https?://(?:www\.)?([^/]+)/(?:p|products)/([^/?#]+)', u)
    return f'{m.group(1)}/{m.group(2)}' + (f'?v={v.group(1)}' if v else '')

mats, sheet = [], []
for n, (shelf, brand, b, name, pid, url, photo, crop, hol, hid, reason, note) in enumerate(A, 1):
    fn = f'{slug(brand)}-{slug(name)}.jpg'; raw = OUT + fn + '.src'
    if photo.startswith('shopify:'): src = shopify_img(url, int(photo.split(':')[1]))
    elif photo.startswith('cm:'): src = None
    elif '@' in photo: src = pin_img(pid)
    elif photo.startswith(PIN + 'zoom-'): src = pin_img(pid)
    else: src = photo
    if photo.startswith('cm:'):
        req = urllib.request.Request('https://case-mate.com/products/mahjong-mats.js', headers={'User-Agent': 'Mozilla/5.0'})
        vs = {str(v['id']): v for v in json.load(urllib.request.urlopen(req, timeout=60))['variants']}
        src = vs[photo[3:]]['featured_image']['src']; src = ('https:' + src) if src.startswith('//') else src
    fetch(src + (('&' if '?' in src else '?') + 'width=1600' if 'cdn.shopify' in src else ''), raw)
    im = Image.open(raw).convert('RGB')
    if crop == 'trim': im = trim(im)
    elif crop: W, H = im.size; im = im.crop((int(crop[0] * W), int(crop[1] * H), int(crop[2] * W), int(crop[3] * H)))
    im.thumbnail((1200, 1200)); im.save(OUT + fn, quality=90); os.remove(raw)
    key = key_of(url) if not re_etsy_bare(url) else f'www.etsy.com/listing/{url.rstrip("/").split("/")[-1]}/{slug(name)}-mahjong-mat'
    mats.append(dict(key=key, name=name, brand=brand, b=b, u=f'https://go.shopmy.us/p-{pid}', product_url=url,
                     img=f'assets/mats/shopmy-nov07/{fn}', src=src, crop=crop, hol=hol, hid=hid, reason=reason,
                     shopmy_id=pid, shelf=shelf, sheet=f'adds#{n}', note=note))
    sheet.append((n, name, brand, im, hol, hid))
EYE = {'White Sailboats': (['blue', 'neutral'], 'sea + sky blue with large white hydrangeas/sails; measured blue only. LOOKED at the brand render Nov 7'),
       'Cocktails Double Sided': (['green', 'neutral', 'pink'], 'olive-green centre, white border with pink/orange/green bottles; the measured dark is the bottle outlines only. LOOKED at the brand render Nov 7')}
for m in mats:
    if m['name'] in EYE: m['mf'], m['eye_why'] = EYE[m['name']]
json.dump({'_note': "Nov 7 ShopMy cross-check (scripts/checks/shopmy_sync_check.py, report config/shopmy-crosscheck-nov07.json). ShopMy mats in NEITHER FYM 1.17 nor Mat Gallery v117: Mahj & Moon Etsy pins never paired (5), Rebecca Illustrated shelf (approved Oct 22, never added; 6 + 2 Questionable hidden), Waiting On Martha (3), The Mahjong House Ruby Table, Southern Living x3, Case-Mate (4 colourways of one pin), OMM x Tuckernuck In Full Bloom. All ShopMy-affiliated (gate [9]); link = her go.shopmy.us link, no code claim. Holiday: Vintage Twinkle only (Christmas trees). Photos LOOKED at: assets/qa/shopmy-nov07/adds.jpg. Patch: builder/fym_fix_nov07/shopmy_nov07.py (+ the Oct 26 Amazon holiday picks via builder/fym_fix_oct25/v96_amazon_holiday.py; run builder/fym_fix_nov07/adds118.sh). Goes into FYM 1.18 + Mat Gallery v118 (gallery_sync.py drafts the gallery rows from the FYM build at release).",
           'mats': mats, 'fixes': FIXES}, open(REPO + 'config/fym-shopmy-nov07.json', 'w'), indent=1, ensure_ascii=False)
T = 260; cols = 6; rows = (len(sheet) + cols - 1) // cols
S = Image.new('RGB', (T * cols, (T + 34) * rows), (24, 30, 58)); d = ImageDraw.Draw(S)
for j, (n, name, brand, im, hol, hid) in enumerate(sheet):
    x, y = (j % cols) * T, (j // cols) * (T + 34); t = im.copy(); t.thumbnail((T - 8, T - 8))
    S.paste(t, (x + 4, y + 30)); d.text((x + 4, y + 2), f'#{n} {brand}'[:40], fill=(255, 230, 120)); d.text((x + 4, y + 15), (name + (' HOLIDAY' if hol else '') + (' HIDDEN (Questionable)' if hid else ''))[:42], fill=(255, 255, 255))
S.save(QA + 'adds.jpg', quality=82)
print(len(mats), 'mats ->', 'config/fym-shopmy-nov07.json', '; sheet', QA + 'adds.jpg')
