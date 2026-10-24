"""Brownstone Bloom album, Oct 24 revision (Tiffany: RTS l-brownstone-v2 note Oct 23 ~10:46pm + chat Oct 24 2:56am).
- Tile racks (final_lists brownstone-bloom): Anders Ruff Tortoise + Bam Bird Boutique Olive + Bird & Bamboo Wine.
  Out: PLM Oak, B&B Lilac, B&B Moss.
- Order: Britt Mills Scarlett -> #2, Autumn Saffron -> #4, rest unchanged; her 8 round-2 hearts appended (#32-39) for
  her to rank in.
- Mat racks: config/mat-racks-picks.json when listed (Brownstone Bloom mat = AR Tortoise + PLM Acrylic Burl, Oct 24),
  else the Oct 20 card's mat racks (unchanged), else matpick for the new mats.
- Photos: the Oct 20 sources lived in another session's scratch and are gone, so each mat is re-sourced: the brand's own
  Shopify image that matches the Find Your Mat-ch photo (largest copy), else the Find Your Mat-ch photo. Same crop rule
  as Oct 20 (72% lower-left close-up when >= 900px of mat survive, else the whole mat).
Usage: python3 brownstone_oct24.py <workdir> <srcdir with src.json>; then gen2.py <workdir>/spec.json assets/cards/brownstone-bloom-oct24"""
import json, io, base64, re, os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from matpick import pick
R = '/home/claude/mahjmatchmaker-data/'; W = sys.argv[1]; SD = sys.argv[2]; os.makedirs(W, exist_ok=True)
OLD = json.load(open(R + 'assets/cards/brownstone-bloom-oct20/manifest.json'))['cards']
SRC = json.load(open(SD + '/src.json'))
TRACKS = json.load(open(R + 'config/tile-racks-picks.json'))['final_lists']['brownstone-bloom']
REG = {k: v for k, v in json.load(open(R + 'config/mat-racks-picks.json')).items() if isinstance(v, dict)}
NOCODE = {'Sunday Mahjong', 'Luxe Mahjong', 'Lucky Daughters', 'Mahjong Studios', 'I Love Mahj', 'Mahjong by SI', "Let's Be Besties", 'Mahj Tile Haus', 'Ozark Mahjongg', 'Tala Mahj', ''}
NOPCT = {'Anders Ruff', 'Mahjong Register', 'The Mahjong Press'}
def footer(b): return 'SAVE WITH CODE : MAHJMATCH' if (b in NOCODE or b in NOPCT) else '10% OFF  USE CODE : MAHJMATCH'
def uri(im, maxs=1600):
    im = im.copy(); im.thumbnail((maxs, maxs), Image.LANCZOS); b = io.BytesIO(); im.convert('RGB').save(b, 'JPEG', quality=92)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
def trim(im):
    g = im.convert('L').point(lambda p: 255 if p < 238 else 0); b = g.getbbox(); return im.crop(b) if b else im
def crop(im):
    im = trim(im.convert('RGB')); Wd, H = im.size
    z = .72 if Wd * .72 >= 900 else 1.0
    cw = int(Wd * z); ch = int(cw / 0.973)
    if ch > H: ch = H; cw = int(ch * 0.973)
    return im.crop((0, H - ch, cw, H)) if z < 1 else im.crop(((Wd - cw) // 2, (H - ch) // 2, (Wd - cw) // 2 + cw, (H - ch) // 2 + ch))
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower().replace('&', 'and')).strip('-')
names = [c['mat'] for c in OLD]
for nm in ('Scarlett', 'Autumn Saffron'): names.remove(nm)
names.insert(1, 'Scarlett'); names.insert(3, 'Autumn Saffron')
BY = {c['mat']: c for c in OLD}
NEW = [c for c in json.load(open(R + 'site/livepatch/brownstone-bloom-oct20/review/missing-mats-round2.json'))['candidates']
       if c['id'] in {'bbr2-01', 'bbr2-02', 'bbr2-05', 'bbr2-06', 'bbr2-07', 'bbr2-09', 'bbr2-10', 'bbr2-11', 'bbr2-15'}]
TILE = 'assets/tiles/anders_ruff_brownstone_bloom_tilebox_CARD-ONLY-edited.jpg'; COL = '#7b2d3b'
cards, man = [], []
def add(nm, brand, img, mat_racks, code, extra):
    m = crop(img); n = len(cards) + 1; fn = f"brownstone-bloom-mahjong-tiles-{slug(brand)}-{slug(nm)}-mat.jpg"
    cards.append({'slug': f'bb{n:02d}', 'title': f'Brownstone Bloom + {nm}', 'col': COL, 'tile_file': TILE, 'racks': TRACKS, 'mat_racks': mat_racks,
                  'file': fn, 'code': code, 'mat': uri(m)})
    man.append(dict({'order': n, 'mat': nm, 'brand': brand, 'file': fn, 'code': code, 'crop_px': m.size[0], 'racks': TRACKS, 'mat_racks': mat_racks}, **extra))
for nm in names:
    c = BY[nm]; rk = next((k for k in REG if k in (slug(nm), slug(c['brand']) + '-' + slug(nm))), None)
    mr = REG[rk]['racks'] if rk else c['mat_racks']
    add(nm, c['brand'], Image.open(SD + '/' + SRC[nm]), mr, c['code'], {'vote_id': c.get('vote_id'), 'mat_reg': rk, 'photo': SRC[nm]})
for c in NEW:
    im = Image.open(R + 'site/livepatch/brownstone-bloom-oct20/review/' + c['img'])
    mr = pick(im, exclude=TRACKS + ['Wine'])
    add(c['mat'], c['brand'], im, mr, footer(c['brand']), {'round2': c['id'], 'new': True, 'fym_key': c['fym_key'], 'shop': c.get('shop')})
json.dump({'_note': 'Brownstone Bloom album Oct 24', 'cards': cards, 'max_racks': 4, 'tile_brand': 'Anders Ruff'}, open(W + '/spec.json', 'w'))
json.dump({'set': 'Brownstone Bloom', 'cards': man, 'tile': TILE, 'title_color': COL, 'racks': TRACKS,
           'note': 'Oct 24: racks + order per Tiffany; #32+ are her round-2 hearts, to be ranked in by her'}, open(W + '/manifest.json', 'w'), indent=1)
print(len(cards), 'cards'); [print(c['order'], c['mat'], c['brand'], c['crop_px'], c['mat_racks']) for c in man]
