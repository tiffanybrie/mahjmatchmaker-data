"""Origami (Timber) album cards (Nov 16): deco_build.py adapted (spec _nov16, inset origami-timber-cranes)."""
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
A = json.load(open(R + f'scripts/albumcard/specs/{KEY}_nov16.json'))
CC = json.load(open(R + 'config/colorcards.json'))['sets'][KEY]
TRACKS = CC['racks']
INSET = "assets/tiles/album/inset/origami-timber-winds-2col.jpg"  # Tiffany Nov 21 6:32pm: inset B fixed (was origami-timber-center.jpg)  # Tiffany Nov 16 11:37pm: the card gets the CENTER crop of the FYM split photo
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
SOLDOUT = {'Mahjong Register Admiral Navy': 'brand new (Oct 24), already sold out'}
SISTER = {'Vegan Leather – Caramel'}
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
    _pref = {k: v for k, v in {**BAMBIRD, **PARTNER_RACKS}.items() if RUSE.get(k, 0) < 6}  # no rack on more than 6 cards (stale)
    _over = [k for k, v in RUSE.items() if v >= 12]  # no one rack on more than 12 cards: keep the mat matches varied
    for l in pick(m, exclude=list(TRACKS) + NOT_FOR_TIMBER + _over, prefer=_pref, prefer_de=10):  # only when the mat really has that colour (Tiffany 1:43am: match the mat)
        if l not in mr and len(mr) < 2: mr.append(l)
    if sum(1 for l in mr if l in SOLDOUT) > 1: mr = [l for l in mr if l not in SOLDOUT][:1] + [l for l in mr if l in SOLDOUT][:1]
    for j, l in enumerate(mr):  # a sold-out new rack: at most 2 cards per album, then its in-stock sibling
        if l in SOLDOUT:
            if SO_USED[0] >= 2: mr[j] = None
            else: SO_USED[0] += 1
    mr = [l for l in mr if l] or ['Bam Bird Boutique Walnut']
    # NEVER two burls on one card (Tiffany Nov 17 2:24am: OMM Burl + PLM Acrylic Burl together 'is stupid')
    BURLS = {'Oh My Mahjong Burl', 'Peace Love Mahjong Acrylic Burl'}
    if sum(1 for l in mr if l in BURLS) > 1: mr = [l for i, l in enumerate(mr) if l not in BURLS or l == next(x for x in mr if x in BURLS)]
    # Mat-specific rack overrides (spec mat 'mat_racks'): e.g. brown leathers get CONTRAST racks, not same-tone burls (2:24am)
    if c.get('mat_racks'): mr = list(c['mat_racks'])
    if not c.get('keep_mr_navy'): mr = ['Bam Bird Boutique Indigo' if l == 'Mahjong Register Navy Solid Wood' else l for l in mr]  # 9:02am: anywhere MR Navy was, Bam Bird Indigo
    # ALWAYS TWO mat racks (Tiffany Nov 17 2:15am: 'You're supposed to pick two racks for the mat')
    if len(mr) < 2:
        for l in pick(m, exclude=list(TRACKS) + NOT_FOR_TIMBER + _over + mr + [b for b in BURLS if any(x in BURLS for x in mr)], k=8, maxn=2):
            if l not in mr: mr.append(l); break
    if all(l in SOLDOUT for l in mr): mr = mr + ['Bam Bird Boutique Walnut']  # never only out-of-stock racks
    rnotes = [f'{l}: {SOLDOUT[l]}' for l in mr if l in SOLDOUT]
    for l in mr: RUSE[l] = RUSE.get(l, 0) + 1
    fn = f"{KEY}-mahjong-tiles-{slug(brand)}-{slug(nm)}-mat.jpg"; n = len(cards) + 1
    code = footer(c); hol = bool(c.get('holiday'))
    cards.append({'slug': f'{KEY[:6]}{n:02d}', 'title': f"{CC['name']} + {c.get('short') or nm}", 'col': CC['col'], 'tile_file': INSET,
                  'tilefit': 'cover', 'racks': TRACKS, 'mat_racks': mr, 'file': fn, 'code': code, 'mat': uri(m), 'hol': hol, 'flame': FLAME if hol else None})
    note = 'TNT rec' if c.get('tnt') else 'Sister mat' if nm in SISTER else ('Holiday match' if c.get('holiday') else ('Retired' if c['retired'] else None))
    man.append({'order': n, 'group': c['group'], 'mat': nm, 'brand': brand, 'retired_mat': c['retired'], 'holiday': hol, 'partner': is_partner(c), 'file': fn,
                'code': code, 'src': c['img'], 'racks': TRACKS, 'mat_racks': mr, 'why': c['why'], 'fym': c['fym'], 'lowres': c['lowres'],
                'caption_note': note, 'rack_notes': rnotes})
json.dump({'_note': f'{KEY} album DRAFT (Nov 16)', 'cards': cards, 'max_racks': 4, 'tile_brand': 'Bam Bird Boutique',
           'navy': 'assets/brand/card_navy_logo_v4.png', 'true_len': True}, open(W + '/spec.json', 'w'))
json.dump({'set': CC['name'], 'status': "DRAFT: Claude's own picks, pending Tiffany's review", 'groups': A['groups'], 'cards': man,
           'title_color': CC['col'], 'tile': CC['tile'],
           'racks_note': 'tile racks = colorcards racks (Bam Bird Walnut + Olive); mat racks = matpick nearest colours (Bam Bird + partner racks first)'},
          open(W + '/manifest.json', 'w'), indent=1, ensure_ascii=False)
print(len(cards), 'cards')
