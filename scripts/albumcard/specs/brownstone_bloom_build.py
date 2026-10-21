"""Brownstone Bloom tiles (Anders Ruff) album: one card per YES mat from her swipe book
(artifact SP7dZ1aMohojH3mMf2fsQ4, db brownstoneswipe), in the live-album card layout (gen2.py).

Votes: the page merges the Oct 11 summary doc ('brownstone-bloom', v map) with the per-mat docs
(Oct 12-15), per-mat wins. That gives 48 yeses. Her 7 stars (brownstoneswipe_notes) lead the album,
then the rest in deck order.
Tile photo: her pick in the tile picker (db bbtilepick, 'pile-fixed-e2') =
  assets/tiles/anders_ruff_brownstone_bloom_tilebox_CARD-ONLY-edited.jpg
Racks: none. config/tile-racks-picks.json final_lists has no Brownstone Bloom entry.

Left out (see manifest 'held'):
- Jardin de Los Jefes Printed Needlepoint Canvas: a needlepoint canvas, not a mat (the mat itself has a card).
- YEAR OF THE DRAGON - PERIWINKLE (2nd listing): same mat as YOTD Periwinkle, one card.
- Tigre de Tartan Domino Oxblood, Mantel Mates, Domino Faded Carolina, Cannage Blonde: every brand photo
  has tiles/racks/props on the mat (doc 49); on the Needs a photo list. Faded Carolina: her note
  "Photo absolutely does not work".
- El Ultimo Refresco (Tigre x Miss Mahjong): every brand photo has tiles/racks on the mat; Needs a photo.
Close-up photos (clean pattern, no props; same approach as the CMC vegan leather Sunday card):
  El Tigre (photo 2), Jardin de Los Jefes (photo 5), Plum Peony (photo 7, top 70%: the catalog's flat photo
  has racks on it) from tigredetartan.com. Mac + Miller Chinoiserie Round: lower-left quarter only, below the
  photo's '(c) Mac and Miller' watermark.

Usage: python3 brownstone_bloom_build.py <workdir>   (expects <workdir>/src/<vote id>.jpg,
       <workdir>/items.json, <workdir>/yes_ids.json, <workdir>/stars.json, <workdir>/deck_ids.json)
then:  python3 scripts/albumcard/gen2.py <workdir>/spec.json <workdir>/cards"""
import json, io, base64, re, os, sys
from PIL import Image
R = '/home/claude/mahjmatchmaker-data/'
W = sys.argv[1]
items = json.load(open(W + '/items.json'))
yes = json.load(open(W + '/yes_ids.json'))
stars = json.load(open(W + '/stars.json'))
deck = json.load(open(W + '/deck_ids.json'))
DROP = {'503bc75c0d': 'needlepoint canvas, not a mat', '5f55ea2070': 'duplicate listing of YOTD Periwinkle'}
HOLD = {'163d9309bc': 'needs a photo: every brand photo has tiles/racks on the mat',
        'c9ec08ccad': 'needs a photo: every brand photo has tiles/racks on the mat',
        '7214bf991a': 'needs a photo: her note "Photo absolutely does not work"; every brand photo has racks on it',
        'bfe45abb2a': 'needs a photo: every brand photo has tiles/props on the mat',
        'd1475a1f87': 'needs a photo: every brand photo has tiles/racks on the mat'}
CLOSEUP = {'a38d0c3d6c', '9c5f1f84f2', '9df40a7c15', 'f371dd8b2e'}
NAME = {'163d9309bc': 'Domino Oxblood', '1cfc31f15e': 'Neutre Blanc', '2f38172384': 'Vanderbilt', '4253a9caa9': 'Burgundy Grove',
        '464ad0d570': 'Hawthorne', '4902a2e342': 'Ivy Reverie', '4fba011322': 'Dapper', '5035168913': 'Midnight Garden',
        '9c5f1f84f2': 'Jardin de Los Jefes', '5dc892df42': 'YOTD Periwinkle', '65735ba283': 'Palomino', '67ccd89587': 'Fall Fling',
        '70babe42bc': 'Toile de los Muertos', '77c02a2c7e': 'Marigold', '85c523e3fb': 'Sedona', '9df40a7c15': 'Plum Peony',
        'a38d0c3d6c': 'El Tigre', 'a4ffcdcbdc': 'Handbook Plaid', 'ad62877a0e': 'Moss Grove', 'b17f4655be': 'Regency Scalloped',
        'bf65e4ec69': 'Nantucket Basket', 'd1475a1f87': 'El Ultimo Refresco', 'de5d3b888d': 'Nantucket Rope',
        'e23d52423c': 'Saddles & Silk', 'fb983976ea': 'Brownstone Bloom', 'dab98cb673': 'The Hunt Club', 'ce5df54837': 'Tova',
        'fb00f4a65a': 'Hydrangea', '51f9a839dc': 'Eden', '0969fba7bf': 'Cognac', '8771340224': 'Harvest Plaid',
        '65e2015566': 'YOTD White', '4b07d0fda0': 'Mocha Bloom Light', '265eb1579c': 'YOTD Black', 'a7c6718d71': 'Scarlett',
        'c5d059f78e': 'Rattan', 'f371dd8b2e': 'Chinoiserie Round', 'fd8ed0a8e9': 'Autumn Bloom', '64923f39fd': 'Autumn Saffron',
        'c37c64e7dc': 'Pineapple Palms', 'e007d7fb4f': 'Flourish', '56b9042394': 'Walk in the Park', 'bc66c3bd51': 'Radiance'}
NOTE = {'51f9a839dc': 'Also available in neoprene', '56b9042394': 'Also available in leatherette'}
BRAND = {'Mahjong Row & Co.': 'Mahjong Row & Co', 'Tigre de Tartan': 'Tigre de Tartan'}
PCT = {}  # Oct 21 (Tiffany): card code bands ALWAYS say 10% (the safe floor: 'it might be more, but it's never less'). Real brand % lives on brand pages. Gate: scripts/albumcard/codeband_lint.py
NOPCT = {'Anders Ruff', 'Mahjong Register', 'The Mahjong Press'}
NOCODE = {'Sunday Mahjong', 'Luxe Mahjong', 'Maison Mahj', 'Lucky Daughters', 'Mahjong Studios', 'I Love Mahj',
          'Mahjong by SI', "Let's Be Besties", 'Mahj Tile Haus', 'Ozark Mahjongg', ''}
def footer(b):
    if b == 'Maison Mahj': return 'SHOP THE MATCH : MAHJMATCHMAKER.COM'
    if b in NOCODE: return 'SAVE WITH CODE : MAHJMATCH'  # rule Oct 18: every card carries MAHJMATCH (only Coquette / Maison Mahj keep shop-the-match)
    if b in NOPCT: return 'SAVE WITH CODE : MAHJMATCH'
    return f"{PCT.get(b, '10%')} OFF  USE CODE : MAHJMATCH"
def uri(im, maxs=1400):
    im = im.copy(); im.thumbnail((maxs, maxs)); b = io.BytesIO(); im.convert('RGB').save(b, 'JPEG', quality=90)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
def crop(im, closeup=False):
    """card mat area is 1080x1110 (0.973). Flat photos: lower-left close-up (album style). Close-up photos: centre."""
    im = im.convert('RGB'); Wd, H = im.size
    if closeup:
        cw = min(Wd, int(H * 0.973)); ch = int(cw / 0.973)
        x0 = (Wd - cw) // 2; y0 = (H - ch) // 2
        return im.crop((x0, y0, x0 + cw, y0 + ch))
    z = .72 if Wd >= 900 else 1.0
    cw = int(Wd * z); ch = int(cw / 0.973)
    if ch > H: ch = H; cw = int(ch * 0.973)
    return im.crop((0, H - ch, cw, H))
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower().replace('&', 'and')).strip('-')
TILE = 'assets/tiles/anders_ruff_brownstone_bloom_tilebox_CARD-ONLY-edited.jpg'
COL = '#7b2d3b'  # burgundy from the tile faces (Brownstone Bloom: blush, lavender, olive, burgundy)
order = [k for k in stars if k in yes] + [k for k in deck if k in yes and k not in stars]
order += [k for k in yes if k not in order]
cards, man, held = [], [], []
for k in order:
    if k in DROP or k in HOLD:
        held.append({'vote_id': k, 'mat': items[k]['label'], 'brand': items[k].get('sub'), 'why': DROP.get(k) or HOLD[k]}); continue
    brand = BRAND.get(items[k].get('sub', ''), items[k].get('sub', ''))
    nm = NAME[k]; src = Image.open(f'{W}/src/{k}.jpg')
    fn = f"brownstone-bloom-mahjong-tiles-{slug(brand)}-{slug(nm)}-mat.jpg"
    n = len(cards) + 1
    cards.append({'slug': f'bb{n:02d}', 'title': f'Brownstone Bloom + {nm}', 'col': COL, 'tile_file': TILE, 'racks': [],
                  'file': fn, 'code': footer(brand), 'mat': uri(crop(src, k in CLOSEUP))})
    man.append({'order': n, 'vote_id': k, 'star': k in stars, 'mat': nm, 'brand': brand, 'file': fn, 'code': footer(brand),
                'src_size': list(src.size), 'closeup': k in CLOSEUP, 'caption_note': NOTE.get(k), 'racks': []})
json.dump({'_note': 'Brownstone Bloom tiles (Anders Ruff) album v1. Yes mats from db brownstoneswipe, stars first. No racks (no final_lists entry).',
           'cards': cards, 'max_racks': 3}, open(W + '/spec.json', 'w'))
json.dump({'cards': man, 'held': held, 'tile': TILE, 'title_color': COL}, open(W + '/manifest.json', 'w'), indent=1)
print(len(cards), 'cards;', len(held), 'held')
