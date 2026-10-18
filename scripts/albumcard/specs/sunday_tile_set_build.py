"""Sunday Tile Set album: one card per YES mat (db sundayswipe, 37 yes), Tiffany's saved order.
Writes spec.json for scripts/albumcard/gen2.py (per-card mat data URI; tile fixed = Sunday).
v2 (Tiffany, Oct 15 review): "For Britt Mills don't make duplicate cards. You can make a note in the caption of
the card that the mat is available in leatherette or neoprene. Move Plum Panda before Gaylord. Use Middle & Main
Mahjong Tortoise, Bam Bird Boutique Walnut and Peace Love Mahjong Oak racks."
- Britt Mills Legacy (neoprene) + Legacy Leatherette -> one Legacy card; Savannah card titled "Savannah"
  (Britt Mills sells it in neoprene and leatherette). manifest caption_note carries the material line.
- Tile racks (lower left, real photos from assets/racks/card/) = RACKS on every card.
v3 (Tiffany, Oct 15 6:50pm): layout only (card2.html: racks off the left edge, Sunday Mahjong logo flag left of the
tile photo, condensed MATCH THE MAT group) and "You will pick the mat matches for me": 1-2 Bird & Bamboo colours per
mat nearest the mat's main colours (scripts/albumcard/matpick.py), per card in 'mat_racks'; listed in manifest.json.
Usage: python3 sunday_tile_set_build.py <workdir>; then gen2.py <workdir>/spec.json <outdir>"""
import json, io, base64, re, os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from matpick import pick
R = '/home/claude/mahjmatchmaker-data/'
W = os.path.dirname(os.path.abspath(__file__))
OUTW = sys.argv[1] if len(sys.argv) > 1 else W
order = json.load(open(W + '/sunday_tile_set_order.json'))  # copy of /tmp/sun/album_order.json (her saved order)
mp = {x['id']: x for x in json.load(open(W + '/sunday_tile_set_map.json'))}
names = [l.split('. ', 1)[1] for l in open(W + '/sunday_tile_set_order.txt').read().strip().split('\n')]
assert len(names) == len(order) == 37
RACKS = ['Middle & Main Hawksbill Heritage Tortoise', 'Bam Bird Boutique Walnut', 'Peace Love Mahjong Oak']
DROP = {'brittmil-legacy-mahjong-mat-art-print'}  # Legacy Leatherette: same design as Legacy (neoprene) -> one card
RENAME = {'brittmil-savannah-mahjong-mat-art-print': 'Savannah'}
NOTE = {'brittmil-legacy-britt-mills-mahjong-mat': 'Also available in leatherette',
        'brittmil-savannah-mahjong-mat-art-print': 'Also available in neoprene'}
pairs = [(m, n) for m, n in zip(order, names) if m not in DROP]
pp = next(x for x in pairs if x[0] == 'sundayma-plum-panda-premium-mahjong-mat'); pairs.remove(pp)
pairs.insert(next(i for i, x in enumerate(pairs) if x[0] == 'sundayma-gaylord-premium-mahjong-mat'), pp)  # Plum Panda before Gaylord
PCT = {'Britt Mills': '15%'}
TENPCT = {'Mahjong Row & Co', 'Charleston Mahjong Club', 'Mahj Squad'}
NOPCT = {'Anders Ruff'}
def footer(b):
    if b in NOPCT: return 'SAVE WITH CODE : MAHJMATCH'
    if b in PCT: return f'{PCT[b]} OFF  USE CODE : MAHJMATCH'
    if b in TENPCT: return '10% OFF  USE CODE : MAHJMATCH'
    if b == 'Maison Mahj': return 'SHOP THE MATCH : MAHJMATCHMAKER.COM'
    return 'SAVE WITH CODE : MAHJMATCH'  # rule Oct 18: every card carries MAHJMATCH (only Coquette / Maison Mahj keep shop-the-match)
def uri(im, maxs=1400):
    im = im.copy(); im.thumbnail((maxs, maxs)); b = io.BytesIO(); im.convert('RGB').save(b, 'JPEG', quality=90)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
def flat(im):
    im = im.convert('RGBA'); bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[3]); return bg
def crop(im):
    """lower-left close-up of the mat (album style); card mat area is 1080x1110 (0.973). Small photos show the whole mat."""
    if im.mode == 'RGBA': im = im.crop(im.getbbox())
    im = flat(im); Wd, H = im.size
    z = .72 if Wd >= 900 else 1.0
    cw = int(Wd * z); ch = int(cw / 0.973)
    if ch > H: ch = H; cw = int(ch * 0.973)
    return im.crop((0, H - ch, cw, H))
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower().replace('&', 'and')).strip('-')
tile = Image.open(R + 'assets/tiles/album/sunday-tile-set.png').convert('RGB').crop((18, 18, 582, 700))  # drop the photo's own cream frame edge; the card adds its white border
tb = io.BytesIO(); tile.save(tb, 'JPEG', quality=92); TILE = 'data:image/jpeg;base64,' + base64.b64encode(tb.getvalue()).decode()
SRCFIX = {'letsbebe-tartan-tweed-mahjong-mat': '/tmp/sun/alb_src/letsbebe-tartan-tweed-mahjong-mat_0.jpg',
          'luxemahj-untitled-sep2916-36-07': '/tmp/sun/alb_src/luxemahj-untitled-sep2916-36-07_0.jpg'}
# Oct 18 (Tiffany 01:44-01:58): no B&B woods; no bright painted racks (Carrot, Radish, Red) on moody/brown/burgundy/leather mats.
# Hand-checked per card; these override matpick. Sunday Cola / Tigre Oxblood: no clean product photo yet (see rack index notes).
MATFIX = {'sunday-mahjong-tiles-anders-ruff-brownstone-bloom-mat.jpg': ['Peace Love Mahjong Acrylic Burl', 'Bird & Bamboo Matcha'], 'sunday-mahjong-tiles-sunday-mahjong-rattan-mat.jpg': ['Bird & Bamboo Matcha', 'Peace Love Mahjong Acrylic Burl'], 'sunday-mahjong-tiles-mahjong-by-si-vintage-oxblood-leather-mat.jpg': ['Bird & Bamboo Wine', 'Peace Love Mahjong Acrylic Burl'], 'sunday-mahjong-tiles-charleston-mahjong-club-brown-vegan-leather-mat.jpg': ['Peace Love Mahjong Acrylic Burl'], 'sunday-mahjong-tiles-mahjong-row-and-co-autumn-saffron-mat.jpg': ['Bird & Bamboo Matcha', 'Peace Love Mahjong Acrylic Burl', 'Bird & Bamboo Wine'], 'sunday-mahjong-tiles-let-s-be-besties-tartan-tweed-mat.jpg': ['Bird & Bamboo Wine', 'Peace Love Mahjong Acrylic Burl'], 'sunday-mahjong-tiles-ozark-mahjongg-winslow-1920-rouge-mat.jpg': ['Bird & Bamboo Wine', 'Bird & Bamboo Cream'], 'sunday-mahjong-tiles-britt-mills-legacy-mat.jpg': ['Bird & Bamboo Evergreen', 'Peace Love Mahjong Acrylic Burl'], 'sunday-mahjong-tiles-let-s-be-besties-fall-flowers-mat.jpg': ['Bird & Bamboo Mango', 'Peace Love Mahjong Acrylic Burl'], 'sunday-mahjong-tiles-mahjong-by-si-the-hunt-club-mat.jpg': ['Peace Love Mahjong Acrylic Burl', 'Bird & Bamboo Evergreen'], 'sunday-mahjong-tiles-mahjong-by-si-the-lodge-mat.jpg': ['Peace Love Mahjong Acrylic Burl', 'Bird & Bamboo Graphite'], 'sunday-mahjong-tiles-sunday-mahjong-coastal-grandma-mat.jpg': ['Bird & Bamboo Cream', 'Peace Love Mahjong Acrylic Burl']}
cards = []; man = []
for i, (mid, nm) in enumerate(pairs):
    mname, brand = [x.strip() for x in nm.split('·')]
    mname = RENAME.get(mid, mname)
    brand = re.sub(r'\s*\(.*', '', brand)
    if mid == 'sundayma-vegan-leather-premium-mahjong-mat':
        # Oct 11 note in /tmp/sun/sunday_album_order.txt: replaced by Charleston Mahjong Club Brown Vegan Leather.
        # No flat full-mat photo exists; use CMC's close-up product photo (IMG_2810), same style as the live Cypress/Gatsby cards.
        src = Image.open('/tmp/claude-0/-home-claude-mahjmatchmaker-data/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/bvl_full.jpg').convert('RGB').crop((130, 0, 3120, 3820))
        lowres = False
    elif mid in SRCFIX:
        # the background-removal cut-out ate parts of these mats; use the brand's flat product photo, white margins trimmed
        src = Image.open(SRCFIX[mid]).convert('RGB'); g = src.convert('L').point(lambda p: 255 if p < 235 else 0); src = src.crop(g.getbbox()); lowres = False
    else:
        src = Image.open('/tmp/sun/alb_cut/' + mp[mid]['file']); lowres = src.width < 700
    mat = crop(src)
    fn = f"sunday-mahjong-tiles-{slug(brand)}-{slug(mname)}-mat.jpg"
    mp_ = MATFIX.get(fn) or pick(mat, exclude=RACKS)
    cards.append({'slug': f'sun{i+1:02d}', 'title': f'Sunday + {mname}', 'col': '#9a6a1f', 'tile_file': TILE, 'racks': RACKS,
                  'file': fn, 'code': footer(brand), 'mat': uri(mat), 'mat_racks': mp_, 'tile_brand': 'Sunday Mahjong'})
    man.append({'order': i + 1, 'vote_id': mid, 'mat': mname, 'brand': brand, 'file': fn, 'code': footer(brand),
                'src': 'cmc IMG_2810 close-up' if mid.startswith('sundayma-vegan') else SRCFIX.get(mid, mp[mid]['file']), 'lowres': lowres, 'caption_note': NOTE.get(mid), 'racks': RACKS, 'mat_racks': mp_})
json.dump({'_note': 'Sunday Tile Set album v3 (Sunday Mahjong; Oct 15 evening layout + Claude B&B mat picks). 37 yes mats from db sundayswipe, her saved order; Britt Mills Legacy merged (36 cards); tile racks per her Oct 15 note.',
           'cards': cards, 'max_racks': 3}, open(OUTW + '/spec.json', 'w'))
json.dump(man, open(OUTW + '/manifest.json', 'w'), indent=1)
print(len(cards))
