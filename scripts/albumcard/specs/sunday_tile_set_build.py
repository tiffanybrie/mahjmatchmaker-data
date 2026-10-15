"""Sunday Tile Set album: one card per YES mat (db sundayswipe, 37 yes), Tiffany's saved order.
Writes spec.json for scripts/albumcard/gen2.py (per-card mat data URI; tile fixed = Sunday)."""
import json, io, base64, re, os
from PIL import Image
R = '/home/claude/mahjmatchmaker-data/'
W = os.path.dirname(os.path.abspath(__file__))
order = json.load(open('/tmp/sun/album_order.json'))
mp = {x['id']: x for x in json.load(open(W + '/map.json'))}
names = [l.split('. ', 1)[1] for l in open('/tmp/sun/sunday_album_order.txt').read().strip().split('\n')]
assert len(names) == len(order) == 37
PCT = {'Britt Mills': '15%'}
TENPCT = {'Mahjong Row & Co', 'Charleston Mahjong Club', 'Mahj Squad'}
NOPCT = {'Anders Ruff'}
def footer(b):
    if b in NOPCT: return 'SAVE WITH CODE : MAHJMATCH'
    if b in PCT: return f'{PCT[b]} OFF  USE CODE : MAHJMATCH'
    if b in TENPCT: return '10% OFF  USE CODE : MAHJMATCH'
    return 'SHOP THE MATCH : MAHJMATCHMAKER.COM'  # Sunday, Luxe, Lucky Daughters, Ozark, Mahjong by SI, Let's Be Besties, Mahj Tile Haus: no code on the hub
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
cards = []; man = []
for i, (mid, nm) in enumerate(zip(order, names)):
    mname, brand = [x.strip() for x in nm.split('·')]
    brand = re.sub(r'\s*\(.*', '', brand)
    if mid == 'sundayma-vegan-leather-premium-mahjong-mat':
        # Oct 11 note in /tmp/sun/sunday_album_order.txt: replaced by Charleston Mahjong Club Brown Vegan Leather.
        # No flat full-mat photo exists; use CMC's close-up product photo (IMG_2810), same style as the live Cypress/Gatsby cards.
        src = Image.open(os.path.dirname(os.path.dirname(W)) + '/bvl_full.jpg').convert('RGB').crop((130, 0, 3120, 3820))
        lowres = False
    elif mid in SRCFIX:
        # the background-removal cut-out ate parts of these mats; use the brand's flat product photo, white margins trimmed
        src = Image.open(SRCFIX[mid]).convert('RGB'); g = src.convert('L').point(lambda p: 255 if p < 235 else 0); src = src.crop(g.getbbox()); lowres = False
    else:
        src = Image.open('/tmp/sun/alb_cut/' + mp[mid]['file']); lowres = src.width < 700
    mat = crop(src)
    fn = f"sunday-mahjong-tiles-{slug(brand)}-{slug(mname)}-mat.jpg"
    cards.append({'slug': f'sun{i+1:02d}', 'title': f'Sunday + {mname}', 'col': '#9a6a1f', 'tile_file': TILE, 'racks': [],
                  'file': fn, 'code': footer(brand), 'mat': uri(mat)})
    man.append({'order': i + 1, 'vote_id': mid, 'mat': mname, 'brand': brand, 'file': fn, 'code': footer(brand),
                'src': 'cmc IMG_2810 close-up' if mid.startswith('sundayma-vegan') else SRCFIX.get(mid, mp[mid]['file']), 'lowres': lowres})
json.dump({'_note': 'Sunday Tile Set album (Sunday Mahjong). 37 yes mats from db sundayswipe, her saved order. No tile racks: no approved Sunday rack list exists.',
           'cards': cards, 'max_racks': 3}, open(W + '/spec.json', 'w'))
json.dump(man, open(W + '/manifest.json', 'w'), indent=1)
print(len(cards))
