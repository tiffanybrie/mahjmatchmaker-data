"""Nov 4 2026: Tiffany's late holiday picks (config/late-holiday-picks-nov03.json, 33 on 10 mats) + her 12 Santa Baby's
Cocktail Hour swipe-book yeses (config/swipe-yeses/holiday-oct21.json 'santababy'; Tiffany Nov 4 2:33pm "a yes is a yes")
into the holiday albums. Same card layout as every holiday card (card2.html via gen2.py, hol + flame), same figure markup
as the live holiday sections.
Racks (Tiffany Nov 3 STANDING): at most ONE painted colour per rack group, the rest wood/pearl/acrylic, never orange at
Christmas. Tile side = her locked list for the set (config/tile-racks-picks.json final_lists / holiday picker), trimmed to
its first painted colour; mat side = one B&B colour (matpick, excluding the tile-side colours) + one neutral real rack.
Usage: python3 late_holiday_build.py <workdir> <matsdir> <D.json (FYM const D)>  -> <workdir>/spec.json + cards.json
then: python3 scripts/albumcard/gen2.py <workdir>/spec.json assets/cards/holiday-late-nov04"""
import json, sys, os, io, base64, re, html
from PIL import Image
R = '/home/claude/mahjmatchmaker-data/'
sys.path.insert(0, R + 'scripts/albumcard')
from matpick import pick as MATPICK
from tdt_policy import card_code, shop_url
W, MD, DJ = sys.argv[1], sys.argv[2], sys.argv[3]; os.makedirs(W, exist_ok=True)
FD = json.load(open(DJ)); SETS = {s['slug']: s for s in FD['sets']}
e = lambda s: html.escape(s, quote=True)

PICKS = json.load(open(R + 'config/late-holiday-picks-nov03.json'))['picks']
SB = json.load(open(R + 'config/swipe-yeses/holiday-oct21.json'))['books']['santababy']['yes']
NAME2SLUG = {'Miss Classic Malachite': 'malachite', 'Miss Classic Jade': 'jade', 'Dear Santa': 'dear-santa', 'Nutcracker Ballet': 'nutcracker-ballet',
             'Dandy': 'dandy', 'Palm Royale': 'palm-royale', 'Limoncello': 'limoncello', 'Holly Jolly (Sugarplum Pink)': 'holly-jolly-pink',
             'Holly Jolly (Rudolph Red)': 'holly-jolly-red', 'La Fete': 'la-fete', 'Luminaire': 'luminaire', 'Hummingbird': 'hummingbird',
             'Osler': 'osler', 'Lola': 'lola', 'Moonlight': 'moonlight', 'Tinselle (Emerald Green)': 'tinselle-emerald', 'Nantucket': 'nantucket',
             "Rackin' Rudolph": 'rackin-rudolph', 'Amara': 'amara', 'Glitterville': 'glitterville'}
SBSLUG = {'vault-spring-love': 'spring-love', 'vault-shangri-la': 'shangri-la'}

# mats: key -> (name, brand, photo file, shop url, brand page, partner)
MATS = {
 'Soirée All Day | Toasty & Tipsy': ('Toasty & Tipsy', 'Soirée All Day', 's_toasty-and-tipsy-mahjong-mat.img', 'soireeallday.co/toasty-and-tipsy-mahjong-mat'),
 'Soirée All Day | Poinsettia Party': ('Poinsettia Party', 'Soirée All Day', 's_poinsettia-party-mahjong-mat.img', 'soireeallday.co/poinsettia-party-mahjong-mat'),
 'Soirée All Day | Color Me Merry': ('Color Me Merry', 'Soirée All Day', 's_color-me-merry-mahjong-mat.img', 'soireeallday.co/color-me-merry-mahjong-mat'),
 'Soirée All Day | Pretty in Pink': ('Pretty in Pink', 'Soirée All Day', 's_pretty-in-pink-mahjong-mat.img', 'soireeallday.co/pretty-in-pink-mahjong-mat'),
 'Soirée All Day | Home for the Holidays': ('Home for the Holidays', 'Soirée All Day', 's_home-for-the-holidays-mahjong-mat.img', 'soireeallday.co/home-for-the-holidays-mahjong-mat'),
 'Soirée All Day | Star of David Hanukkah': ('Star of David Hanukkah', 'Soirée All Day', 's_star-of-david-hanukkah-mat.img', 'soireeallday.co/star-of-david-hanukkah-mat'),
 'House of Hearts Studio | Peace on Earth': ('Peace on Earth', 'House of Hearts Studio', 'h_peace-on-earth.img', 'houseofheartsstudio.com/peace-on-earth-mahjong-mat-full-table-size-leatherette'),
 'My Fair Mahjong | Plaid Tidings': ('Plaid Tidings', 'My Fair Mahjong', 'm_plaid-tidings.img', 'myfairmahjong.com/mahjong-mat-plaid-tidings'),
 'My Fair Mahjong | Peppermint Wishes': ('Peppermint Wishes', 'My Fair Mahjong', 'm_peppermint-wishes.img', 'myfairmahjong.com/mahjong-mat-peppermint-wishes'),
 "Bespoke Mahjong | It's a Vibe Holiday": ("It's a Vibe Holiday", 'Bespoke Mahjong', 'b_vibe-holiday.img', 'www.bespokemahjong.com/mahjholidaymat'),
 "Splash of Color | Santa Baby's Cocktail Hour": ("Santa Baby's Cocktail Hour", 'Splash of Color', 'sb_mat.png', None),
}
SB_URL = 'https://splashofcolorco.com/discount/MAHJMATCH?redirect=%2Fproducts%2Fsanta-baby-s-cocktail-hour-mahjong-mat-sleek-surface'
BRANDPAGE = {'Soirée All Day': '/soiree-all-day-discount-code', 'My Fair Mahjong': '/my-fair-mahjong-discount-code',
             'Bespoke Mahjong': '/bespoke-mahjong-discount-code', 'Splash of Color': '/splash-of-color-discount-code'}
PARTNER = {'Soirée All Day', 'My Fair Mahjong', 'Bespoke Mahjong', 'Splash of Color'}

def mat_url(key):
    n, b, f, k = MATS[key]
    if k is None: return SB_URL
    return FD['mats'][k]['u']

# --- tile side
F = json.load(open(R + 'config/tile-racks-picks.json'))['final_lists']
man = json.load(open(R + 'scripts/albumcard/holiday_manifest.json'))
SIB = {}
for x in man: SIB.setdefault(x['tile'], x['racks'])
def full(k): return 'Bird & Bamboo ' + k[3:] if k.startswith('bb:') else k
NEUTRAL_WORDS = ('Oak', 'Walnut', 'Tortoise', 'Opal', 'Milk Glass', 'Beechwood', 'White Acrylic', 'Burl', 'Clear', 'Pearl', 'Lace', 'Brass')
def neutral(l):
    if l.startswith('Bird & Bamboo '): return False
    return any(w in l for w in NEUTRAL_WORDS) and 'Jade' not in l and 'Cornflower' not in l and 'Peach' not in l and 'Oxblood' not in l
def tile_racks(t):
    src = F.get(t) or SIB.get(t)
    if t == 'shangri-la': src = ['Miss Mahjong Scalloped Iridescent Opal', 'Bird & Bamboo Light Blue', 'Middle & Main Milk Glass Scalloped Acrylic']
    out, painted = [], 0
    for l in map(full, src):
        if not neutral(l):
            if painted: continue
            painted += 1
        out.append(l)
    return out[:3]

TILEIMG = {'dear-santa': 'assets/tiles/holiday/dear-santa.jpg', 'nutcracker-ballet': 'assets/tiles/holiday/nutcracker-ballet.jpg',
           'holly-jolly-pink': 'assets/tiles/holiday/holly-jolly-pink-pile.jpg', 'holly-jolly-red': 'assets/tiles/holiday/holly-jolly-red-pile.jpg',
           'tinselle-emerald': 'assets/tiles/holiday/tinselle-emerald-3x3.jpg', 'rackin-rudolph': 'assets/tiles/holiday/rackin-rudolph.jpg',
           'sunday': 'assets/tiles/album/sunday-tile-set.png', 'hummingbird': 'assets/tiles/album/hummingbird.png'}
def tile_img(t):
    if t in TILEIMG: return TILEIMG[t]
    for x in ('jpg', 'png'):
        if os.path.exists(R + f'assets/tiles/album/{t}.{x}'): return f'assets/tiles/album/{t}.{x}'
    raise SystemExit('no tile photo ' + t)
TNAME = {'sunday': ('Sunday Tile Set', 'Sunday Mahjong'), 'hummingbird': ('Hummingbird', 'Sunday Mahjong'),
         'spring-love': ('Spring Love', 'Oh My Mahjong'), 'shangri-la': ('Shangri-La', 'Oh My Mahjong'), 'heritage': ('Heritage', 'Oh My Mahjong')}
def tinfo(t):
    if t in TNAME: return TNAME[t]
    s = SETS[t]; return s['name'], s['maker']
COLS = json.load(open(R + 'scripts/albumcard/holiday_title_colors.json'))
def tcol(t): return COLS.get(t) or (SETS[t]['tc'] if t in SETS else '#a3192e')
def short(n): return re.sub(r'\s*\(.*?\)', '', n).strip()

# --- mat crop (same as gen_hol3.mat_crop: trim white, close-up of the lower-left 72%)
def trim(im):
    g = im.convert('L').point(lambda p: 255 if p < 235 else 0); bb = g.getbbox(); return im.crop(bb) if bb else im
def flat(im):
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA'); bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[3]); return bg
    return im.convert('RGB')
def mat_crop(im):
    im = trim(flat(im)); W_, H = im.size
    z = .72 if W_ >= 900 else 1.0
    cw = int(W_ * z); ch = int(cw / 0.973)
    if ch > H: ch = H; cw = int(ch * 0.973)
    return im.crop((0, H - ch, cw, H))
def uri(im):
    im = im.copy(); im.thumbnail((1600, 1600), Image.LANCZOS); b = io.BytesIO(); im.convert('RGB').save(b, 'JPEG', quality=92)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
FLAME = 'data:image/png;base64,' + base64.b64encode(open(R + 'assets/brand/flame-heart-holiday.png', 'rb').read()).decode()
ORANGE = {x['name'] for x in json.load(open(R + 'builder/bbracks.json')) if x['fam'] == 'orange' or any(w in x['name'] for w in ('Coral', 'Orange', 'Peach', 'Tangerine', 'Rust'))}  # never orange at Christmas (Tiffany Nov 3)
def mat_racks(im, tile_side):
    ex = [l for l in tile_side if l.startswith('Bird & Bamboo ')] + ['Bird & Bamboo ' + o for o in ORANGE]
    p = [x for x in MATPICK(trim(flat(im)), exclude=ex, maxn=2) if x.startswith('Bird & Bamboo ') and x[14:] not in ORANGE][:1]
    import numpy as _n; light = _n.asarray(trim(flat(im)).convert('L').resize((64, 64))).mean() > 150
    for n in (['Middle & Main Milk Glass Scalloped Acrylic', 'Miss Mahjong Scalloped Iridescent Opal', 'Bam Bird Boutique Walnut'] if light
              else ['Bam Bird Boutique Walnut', 'Middle & Main Hawksbill Heritage Tortoise', 'Miss Mahjong Scalloped Iridescent Opal']):
        if n not in tile_side: return p + [n]
    return p

def footer(brand):
    if brand in PARTNER: return '10% OFF  USE CODE : MAHJMATCH'
    return 'SAVE WITH CODE : MAHJMATCH'

pairs = []  # (mat key, tile slug, source)
for k, tl in PICKS.items():
    for t in tl: pairs.append((k, NAME2SLUG[t], 'late-picks-nov03'))
for _, t in SB: pairs.append(("Splash of Color | Santa Baby's Cocktail Hour", SBSLUG.get(t, t), 'santababy-yes'))
assert len(pairs) == 45, len(pairs)

cache = {}
cards, out = [], []
for i, (mk, t, src) in enumerate(pairs, 1):
    mname, brand, f, _ = MATS[mk]
    if f not in cache: cache[f] = Image.open(os.path.join(MD, f))
    im = cache[f]
    tname, tbrand = tinfo(t)
    tr = tile_racks(t); mr = mat_racks(im, tr)
    slug = re.sub(r'[^a-z0-9]+', '-', f"{t}-mahjong-tiles-{brand}-{mname}-mat".lower().replace('é', 'e')).strip('-')
    fn = slug + '.jpg'
    title = f"{short(tname)} + {mname}"
    cards.append({'slug': f'lh{i:02d}', 'title': title, 'col': tcol(t), 'tile_file': tile_img(t), 'racks': tr, 'mat_racks': mr,
                  'file': fn, 'code': footer(brand), 'mat': uri(mat_crop(im)), 'hol': True, 'flame': FLAME, 'tile_brand': tbrand,
                  **({'tile_mode': 'loose'} if t == 'hummingbird' else {})})
    out.append({'n': i, 'tile': t, 'tileName': tname, 'tileBrand': tbrand, 'mat': mname, 'brand': brand, 'file': fn, 'title': title,
                'tile_racks': tr, 'mat_racks': mr, 'url': shop_url(mat_url(mk), brand), 'brandpage': BRANDPAGE.get(brand), 'partner': brand in PARTNER, 'src': src})
json.dump({'_note': 'late holiday picks + Santa Baby yeses Nov 4', 'cards': cards, 'max_racks': 4}, open(W + '/spec.json', 'w'))
json.dump(out, open(W + '/cards.json', 'w'), indent=1, ensure_ascii=False)
for c in out: print(c['n'], c['tile'], '|', c['mat'], '|', c['tile_racks'], '|', c['mat_racks'])
