"""Bam Bird Boutique Deco (Lagoon) / Deco (Mulberry) album match cards, DRAFT (Nov 7; Tiffany 7:03pm: "You take them, just
like you did this one"). Same pipeline as Juniper round 3 (juniper_build.py -> gen2.py, card2.html): tile PILE photo
(assets/tiles/album/deco-<colour>.jpg), current navy wordmark (card_navy_logo_v3.png), racks at TRUE relative length
(config/rack-lengths.json: Bam Bird racks are 19in).
Tile racks (MATCH THE TILES) = config/colorcards.json sets.<key>.racks: Bam Bird Boutique's own wood racks, one per tile
colour (Lagoon Wood + Mulberry Wood), same shape so they lie the same.
Mat racks (MATCH THE MAT) = matpick.py nearest Bird & Bamboo colours (2), skipping the tile racks.
Code band (Tiffany Nov 8 10:11am, HARD RULE): every Deco card has Bam Bird tiles (a partner), so EVERY card carries the code
band: partner mat with a % = '10% OFF  USE CODE : MAHJMATCH'; a no-% partner OR a non-partner mat = 'SAVE WITH CODE : MAHJMATCH'.
Never 'NOT A PARTNER : NO CODE' on a card; 'no code' notes go in captions only (manifest partner=false + caption_note).
Tile inset (Nov 8): assets/tiles/album/inset/deco-<c>-flowers.jpg (deco_inset.py: flower columns 3-4 | FYM backs). Spec mat 'holiday': true -> holiday card (hol band + flame-heart), own section.
Usage: python3 deco_build.py <deco-lagoon|deco-mulberry> <workdir>; then python3 scripts/albumcard/gen2.py <workdir>/spec.json assets/cards/<key>"""
import json, io, base64, re, os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from matpick import pick
R = '/home/claude/mahjmatchmaker-data/'
KEY, W = sys.argv[1], sys.argv[2]; os.makedirs(W, exist_ok=True)
A = json.load(open(R + f'scripts/albumcard/specs/{KEY}_nov07.json'))
CC = json.load(open(R + 'config/colorcards.json'))['sets'][KEY]
TRACKS = CC['racks']
INSET = f"assets/tiles/album/inset/deco-{KEY.split('-')[1]}-flowers.jpg"  # Nov 8: flower columns, not 9/joker
SISTER = {'Deco Dragon (Mulberry)', 'Deco Dragon (Lagoon)', 'Deco Dragon (Indigo)', 'Deco Neoprene'}
def flat(im):
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA'); bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[3]); return bg
    return im.convert('RGB')
def uri(im, maxs=1400):
    im = im.copy(); im.thumbnail((maxs, maxs)); b = io.BytesIO(); im.convert('RGB').save(b, 'JPEG', quality=90)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
def crop(im):  # Juniper/Papaya default framing: whole mat for small photos, a 72% bottom-left zoom for big ones
    im = flat(im); Wd, H = im.size; z = .72 if Wd >= 900 else 1.0
    cw = int(Wd * z); ch = int(cw / .973)
    if ch > H: ch = H; cw = int(ch * .973)
    return im.crop((0, H - ch, cw, H))
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower().replace('&', 'and').replace("'", '').replace('–', '-')).strip('-')
SNAP = json.load(open(R + 'config/fym-mats-snapshot.json'))['mats']
NOPCT = {'Anders Ruff', 'Mahjong Register', 'The Mahjong Press'}
import base64 as _b64
FLAME = 'data:image/png;base64,' + _b64.b64encode(open(R + 'assets/brand/flame-heart-holiday.png', 'rb').read()).decode()
def is_partner(c):
    m = SNAP.get(c.get('fym'), {})
    return bool(m.get('pa')) and not m.get('nc')
def footer(c):  # Nov 8 HARD RULE: the tiles are a partner, so the code band is ALWAYS on; non-partner mats get no % promise
    if not is_partner(c): return 'SAVE WITH CODE : MAHJMATCH'
    return 'SAVE WITH CODE : MAHJMATCH' if c['brand'] in NOPCT else '10% OFF  USE CODE : MAHJMATCH'
cards, man = [], []
for c in A['mats']:
    nm, brand = c['name'], c['brand']
    src = Image.open(R + c['img']); m = flat(src).crop(tuple(c['box'])) if c.get('box') else crop(src)
    mr = []
    for l in pick(m, exclude=TRACKS):
        if l not in mr and len(mr) < 2: mr.append(l)
    fn = f"{KEY}-mahjong-tiles-{slug(brand)}-{slug(nm)}-mat.jpg"; n = len(cards) + 1
    code = footer(c); hol = bool(c.get('holiday'))
    cards.append({'slug': f'{KEY[:6]}{n:02d}', 'title': f"{CC['name']} + {nm}", 'col': CC['col'], 'tile_file': INSET,
                  'tilefit': 'cover', 'racks': TRACKS, 'mat_racks': mr, 'file': fn, 'code': code, 'mat': uri(m), 'hol': hol, 'flame': FLAME if hol else None})
    note = 'TNT rec' if c.get('tnt') else 'Sister mat' if nm in SISTER else ('Holiday match' if c.get('holiday') else ('Retired' if c['retired'] else None))
    man.append({'order': n, 'group': c['group'], 'mat': nm, 'brand': brand, 'retired_mat': c['retired'], 'holiday': hol, 'partner': is_partner(c), 'file': fn,
                'code': code, 'src': c['img'], 'racks': TRACKS, 'mat_racks': mr, 'why': c['why'], 'fym': c['fym'], 'lowres': c['lowres'],
                'caption_note': note})
json.dump({'_note': f'{KEY} album DRAFT (Nov 7)', 'cards': cards, 'max_racks': 4, 'tile_brand': 'Bam Bird Boutique',
           'navy': 'assets/brand/card_navy_logo_v3.png', 'true_len': True}, open(W + '/spec.json', 'w'))
json.dump({'set': CC['name'], 'status': "DRAFT: Claude's own picks, pending Tiffany's review", 'groups': A['groups'], 'cards': man,
           'title_color': CC['col'], 'tile': CC['tile'],
           'racks_note': 'tile racks = colorcards racks (Bam Bird Lagoon Wood + Mulberry Wood); mat racks = matpick B&B nearest colours'},
          open(W + '/manifest.json', 'w'), indent=1, ensure_ascii=False)
print(len(cards), 'cards')
