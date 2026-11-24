"""Beaumont (Oh My Mahjong) album cards, DRAFT (Nov 24 2026): sadie_jane_build.py adapted. Tile racks = colorcards beaumont racks (OMM Tortoise Shell = the tile brand's own rack for tortoise backs + My Fair Indigo Blue for the cobalt stripe). Mat racks: partner racks preferred (Playbook Nov 23: diversify rack brands), else nearest Bird & Bamboo. Tile racks = config/colorcards.json
sadie-jane racks (Bird & Bamboo Shell Pink + French Blue: nearest to the blush back and the denim stripe; OMM is the tile brand).
Mat racks = matpick nearest Bird & Bamboo colours (2). Usage: python3 sadie_jane_build.py sadie-jane <workdir>; then gen2.py <workdir>/spec.json assets/cards/sadie-jane"""
import json, io, base64, re, os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from matpick import pick
R = '/home/claude/mahjmatchmaker-data/'
KEY, W = sys.argv[1], sys.argv[2]; os.makedirs(W, exist_ok=True)
A = json.load(open(R + f'scripts/albumcard/specs/{KEY}_nov24.json'))
CC = json.load(open(R + 'config/colorcards.json'))['sets'][KEY]
TRACKS = CC['racks']
MEM = json.load(open(R + 'config/mat-rack-memory.json'))['mats']
NEVER = {(x['brand'], x['name']) for x in json.load(open(R + 'config/album-never-show.json'))['mats']}
A['mats'] = [m for m in A['mats'] if (m.get('brand'), m.get('name')) not in NEVER]  # Nov 23: e.g. YOLO Christmas Cat
INSET = "assets/tiles/album/beaumont.jpg"  # Tiffany Nov 16 11:37pm: the card gets the CENTER crop of the FYM split photo
BAMBIRD = {'Bam Bird Boutique Walnut': '#8c5529', 'Bam Bird Boutique Lagoon Wood': '#16494d', 'Bam Bird Boutique Indigo': '#39486a', 'Bam Bird Boutique Slate Blue': '#859fb1'}
# Tiffany Nov 17 9:02am: Bam Bird INDIGO is their navy: use it everywhere instead of Mahjong Register Navy; Bam Bird Slate Blue for slate/light-blue tones.  # measured from assets/racks/card PNGs
# Nov 8 2:12pm (Tiffany): use partners with big rack lines more (Mahjong Register, Anders Ruff) and their NEW colourways; a sold-out
# new rack may go on a card with a note, never a card full of out-of-stock racks. Stock checked on the brand's .js Nov 8.
PARTNER_RACKS = {'Bird & Bamboo Forest Green': '#007E61', 'Peace Love Mahjong Acrylic Burl': '#9b6a45', 'Oh My Mahjong Burl': '#d77e4d',
                 'Peace Love Mahjong Oak': '#d9a86a'}
# Tiffany Nov 17 1:28am (Origami Timber): B&B Forest Green = a really good green for these tiles; Mahjong Register Navy looks good;
# wood tones (PLM Acrylic Burl, PLM Oak, OMM Burl) beat one-off colours like mustard; NO tortoise, NO teal, NO Miss Mahjong Jade & Brass,
# NO PLM Dark Green (too deep). Olive is out.
NOT_FOR_TIMBER = ['Bird & Bamboo ' + n for n in ('Retro Mustard', 'Dijon', 'Mango', 'Butter', 'Sunshine', 'Yellow', 'Glowstick', 'Teal', 'Dark Teal',
                  'Turquoise Blue', 'Turks Blue', 'Tiffany Dusk', 'Mermaid', 'Jade', 'Icy Mint', 'Lime Green', 'Carrot', 'Orange', 'Persimmon',
                  'True Black', 'Blackboard Black', 'Dark Navy')]  # 9:02am: no black racks on these mats; navy = Bam Bird Indigo
SOLDOUT = {}

# Nov 24 (Playbook Nov 23 rack rules): diversify rack brands; partner racks measured from their real card PNGs
import numpy as _np
_IDX = json.load(open(R + 'assets/racks/card/index.json'))['racks']
PREF = {}
for _n in ['Peace Love Mahjong Chartreuse', 'Peace Love Mahjong Navy', 'Peace Love Mahjong Pink', 'Peace Love Mahjong White', 'My Fair Mahjong Indigo Blue',
           'My Fair Mahjong Teal', 'My Fair Mahjong Macaron Green', 'My Fair Mahjong Macaron Blue', 'My Fair Mahjong Macaron Pink', 'Mahjong Register Peacock Teal',
           'Mahjong Register Admiral Navy', 'Virora Maldives Green', 'Virora Spring Jade', 'Bam Bird Boutique Olive', 'Bam Bird Boutique Indigo',
           'Bam Bird Boutique Slate Blue', 'Miss Mahjong Cornflower Blue Scalloped', 'Oh My Mahjong Tortoise Shell']:
    _e = _IDX.get(_n)
    _f = (_e.get('file') if isinstance(_e, dict) else _e) if _e else None
    if not _f: continue
    try:
        _a = _np.asarray(Image.open(R + 'assets/racks/card/' + os.path.basename(_f)).convert('RGBA')).reshape(-1, 4)
        _a = _a[_a[:, 3] > 200][:, :3]; _c = _np.median(_a, 0).astype(int); PREF[_n] = '#%02x%02x%02x' % tuple(_c)
    except Exception: pass
SISTER = {'Lily'}
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
    if 'partner' in c: return bool(c['partner'])  # Nov 8: catalog-refresh adds not in FYM yet carry their own partner flag
    m = SNAP.get(c.get('fym'), {})
    return bool(m.get('pa')) and not m.get('nc')
def footer(c):  # Nov 8 HARD RULE: the tiles are a partner, so the code band is ALWAYS on; non-partner mats get no % promise
    if not is_partner(c): return 'SAVE WITH CODE : MAHJMATCH'
    return 'SAVE WITH CODE : MAHJMATCH' if c['brand'] in NOPCT else '10% OFF  USE CODE : MAHJMATCH'
cards, man = [], []; SO_USED = [0]; RUSE = {}
for c in A['mats']:
    nm, brand = c['name'], c['brand']
    src = Image.open(R + c['img']); m = flat(src).crop(tuple(c['box'])) if c.get('box') else crop(src)
    mr = []
    # Nov 8 1:50pm (Playbook step 8): the tile brand's own racks first. Bam Bird's other cut-out racks (Olive, Walnut, 19in like
    # the set racks, so proportional) win when they match the mat; else Bird & Bamboo colours.
    _pref = PREF
    _over = [k for k, v in RUSE.items() if v >= 12]  # no one rack on more than 12 cards: keep the mat matches varied
    for l in pick(m, exclude=list(TRACKS) + _over, prefer=_pref, prefer_de=10):  # only when the mat really has that colour (Tiffany 1:43am: match the mat)
        if l not in mr and len(mr) < 2: mr.append(l)
    if sum(1 for l in mr if l in SOLDOUT) > 1: mr = [l for l in mr if l not in SOLDOUT][:1] + [l for l in mr if l in SOLDOUT][:1]
    for j, l in enumerate(mr):  # a sold-out new rack: at most 2 cards per album, then its in-stock sibling
        if l in SOLDOUT:
            if SO_USED[0] >= 2: mr[j] = None
            else: SO_USED[0] += 1
    mr = [l for l in mr if l] or ['Bird & Bamboo Light Pink']
    # NEVER two burls on one card (Tiffany Nov 17 2:24am: OMM Burl + PLM Acrylic Burl together 'is stupid')
    BURLS = {'Oh My Mahjong Burl', 'Peace Love Mahjong Acrylic Burl'}
    if sum(1 for l in mr if l in BURLS) > 1: mr = [l for i, l in enumerate(mr) if l not in BURLS or l == next(x for x in mr if x in BURLS)]
    # Mat-specific rack overrides (spec mat 'mat_racks'): e.g. brown leathers get CONTRAST racks, not same-tone burls (2:24am)
    if c.get('mat_racks'): mr = list(c['mat_racks'])
    elif MEM.get(f"{c.get('brand')}|{c.get('name')}"): mr = list(MEM[f"{c.get('brand')}|{c.get('name')}"]['racks'])  # Nov 23: a mat keeps the racks she approved (config/mat-rack-memory.json): 'we should only have to match the mat once'
    pass  # 9:02am: anywhere MR Navy was, Bam Bird Indigo
    # ALWAYS TWO mat racks (Tiffany Nov 17 2:15am: 'You're supposed to pick two racks for the mat')
    if len(mr) < 2:
        for l in pick(m, exclude=list(TRACKS) + _over + mr, k=8, maxn=2):
            if l not in mr: mr.append(l); break
    if all(l in SOLDOUT for l in mr): mr = mr + ['Bird & Bamboo Light Pink']  # never only out-of-stock racks
    rnotes = [f'{l}: {SOLDOUT[l]}' for l in mr if l in SOLDOUT]
    for l in mr: RUSE[l] = RUSE.get(l, 0) + 1
    fn = f"{KEY}-mahjong-tiles-{slug(brand)}-{slug(nm)}-mat.jpg"; n = len(cards) + 1
    code = footer(c); hol = bool(c.get('holiday'))
    cards.append({'slug': f'{KEY[:6]}{n:02d}', 'title': f"{CC['name']} + {c.get('short') or nm}", 'col': CC['col'], 'tile_file': INSET,
                  'tilefit': 'cover', 'racks': TRACKS, 'mat_racks': mr, 'file': fn, 'code': code, 'mat': uri(m), 'hol': hol, 'flame': FLAME if hol else None})
    note = 'TNT rec' if c.get('tnt') else 'Sister mat' if nm in SISTER else ('Holiday match' if c.get('holiday') else ('Retired' if c['retired'] else None))
    man.append({'order': n, 'group': c['group'], 'mat': nm, 'brand': brand, 'retired_mat': c['retired'], 'holiday': hol, 'partner': is_partner(c), 'file': fn,
                'code': code, 'src': c['img'], 'racks': TRACKS, 'mat_racks': mr, 'why': c['why'], 'fym': c.get('fym'), 'lowres': c.get('lowres'),
                'caption_note': note, 'rack_notes': rnotes})
json.dump({'_note': f'{KEY} album DRAFT (Nov 24)', 'cards': cards, 'max_racks': 4, 'tile_brand': 'Oh My Mahjong',
           'navy': 'assets/brand/card_navy_logo_v3.png', 'true_len': False}, open(W + '/spec.json', 'w'))
json.dump({'set': CC['name'], 'status': "DRAFT: Claude's own picks, pending Tiffany's review", 'groups': A['groups'], 'cards': man,
           'title_color': CC['col'], 'tile': CC['tile'],
           'racks_note': 'tile racks = OMM Tortoise Shell + My Fair Indigo Blue (draft); mat racks = partner racks first, else nearest Bird & Bamboo'},
          open(W + '/manifest.json', 'w'), indent=1, ensure_ascii=False)
print(len(cards), 'cards')
sys.path.insert(0, R + 'scripts/checks'); import rack_colour_check as _RC
_b = _RC.run(R + f'scripts/albumcard/specs/{KEY}_nov24.json')
if _b: sys.exit('REFUSED (rack colour check, Tiffany Nov 23): a mat rack colour is not in the mat:\n  ' + '\n  '.join(_b))
