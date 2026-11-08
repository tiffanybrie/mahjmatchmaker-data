"""Juniper (Oh My Mahjong, launches Wed 11/11 10am CT) album match cards, DRAFT (Nov 6).
33 cards in Claude's round-2 order (scripts/albumcard/specs/juniper_round2.json, from
site/livepatch/juniper-picks-nov04/build_r2.py; Tiffany's Nov 5 notes applied: Garden Glow #1, Palm Royale #2,
Lotus Cove #3, Esme + Enchanted back in as Retired). Drafts until she confirms the order.
Same pipeline as Papaya Spritz (papaya_spritz_build.py -> gen2.py, card2.html layout).
Tile racks (MATCH THE TILES): config/colorcards.json sets.juniper racks (Miss Mahjong Jade & Brass, OMM Hot Pink,
OMM Pink Quartz), pending her OK like the rest.
Mat racks (MATCH THE MAT): the mat's round-2 racks that are not already tile racks and have a REAL photo (racks.py rule:
My Fair Malachite Dapple + Mahjong Register Emerald Pearl have none, so they are skipped), filled to 2 with matpick.py
(nearest B&B colours). config/mat-racks-picks.json registry wins when the mat is listed.
Code band: 10% floor everywhere (Oct 21 rule), 'SAVE WITH CODE' for the no-% brands. Title colour #225d36 (set colour,
same as the FYM title colour fix in v115).
Nov 6 round 3 (Tiffany 2:26am notes): spec = juniper_round3.json (her order, outs, Camellia candidate, weak at the bottom), mat 'box'
crops on the hi-res Crane & Moon / Day Dreamer photos, the tile PILE photo (assets/tiles/album/juniper.jpg, rebuilt from OMM
06-Tile_Juniper_F), the current flame-heart wordmark in the navy box (card_navy_logo_v3.png) and racks at TRUE relative length
(spec true_len -> config/rack-lengths.json). JUNIPER_SPEC=<path> picks another spec.
Usage: python3 juniper_build.py <workdir>; then python3 scripts/albumcard/gen2.py <workdir>/spec.json assets/cards/juniper"""
import json, io, base64, re, os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from matpick import pick
import racks as RKS
R = '/home/claude/mahjmatchmaker-data/'
W = sys.argv[1]; os.makedirs(W, exist_ok=True)
A = json.load(open(os.environ.get('JUNIPER_SPEC', R + 'scripts/albumcard/specs/juniper_round3.json')))
CC = json.load(open(R + 'config/colorcards.json'))['sets']['juniper']
TRACKS = CC['racks']
REG = {k: v for k, v in json.load(open(R + 'config/mat-racks-picks.json')).items() if isinstance(v, dict)}
NOPCT = {'Anders Ruff', 'Mahjong Register', 'The Mahjong Press'}
PARTNERS = set(json.load(open(R + 'config/code-truth.json'))['pct']) | NOPCT  # work/pub/catalog.json is gone; code-truth = live partner list
KEYS = dict(A['rack_keys'], bbk='Bird & Bamboo Kelly Green', bbhp='Bird & Bamboo Hot Pink', bbj='Bird & Bamboo Jade',
            bblp='Bird & Bamboo Light Pink', bbfg='Bird & Bamboo Forest Green', owa='Oh My Mahjong White Acrylic')
def footer(b, retired):
    if retired or b not in PARTNERS: return '10% OFF  USE CODE : MAHJMATCH'
    if b in NOPCT: return 'SAVE WITH CODE : MAHJMATCH'
    return '10% OFF  USE CODE : MAHJMATCH'
def flat(im):
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA'); bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[3]); return bg
    return im.convert('RGB')
def uri(im, maxs=1400):
    im = im.copy(); im.thumbnail((maxs, maxs)); b = io.BytesIO(); im.convert('RGB').save(b, 'JPEG', quality=90)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
def crop(im):  # same default framing as Papaya: the whole mat for small photos, a 72% bottom-left zoom for big ones
    im = flat(im); Wd, H = im.size; z = .72 if Wd >= 900 else 1.0
    cw = int(Wd * z); ch = int(cw / .973)
    if ch > H: ch = H; cw = int(ch * .973)
    return im.crop((0, H - ch, cw, H))
# Lotus Cove: OMM's flat photo has a rack + cards on the right/bottom, so frame the pond left of the rack.
BOX = {'Lotus Cove': (130, 40, 1300, 1242),
       # product shots with a black band / bag / white margin / room around the mat: frame the mat itself
       'Zesty Plume': (100, 150, 1150, 1230), 'Chinoiserie Songbird': (100, 150, 1150, 1230),
       'Cherry Blossom Jade': (230, 10, 1200, 1007), 'Emerald Teal & Celadon Leatherette': (150, 160, 1150, 1188),
       'Green Malachite': (140, 0, 501, 371)}
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower().replace('&', 'and').replace("'", '').replace('–', '-')).strip('-')
def reg_for(path, name):
    for k, v in REG.items():
        if path in v.get('files', []) or slug(name) == k: return k, v['racks']
    return None, None
# Nov 6 2:11am (Tiffany): Juniper tile racks = OMM Hot Pink + OMM Agate only (same OMM shape). Jade & Brass lies differently
# next to OMM racks and Pink Quartz = pink + pink, so neither comes back on the MAT side either.
DROPPED = {'Miss Mahjong Jade & Brass', 'Oh My Mahjong Pink Quartz'}
def drawable(l): return l.startswith('Bird & Bamboo ') or RKS.photo(l) is not None
# Nov 7 (Tiffany 7:42pm, holiday matches in Juniper): spec mat 'holiday': true -> holiday-coded card (gen2/card2 'hol' band +
# flame-heart, same as the holiday album cards) and manifest holiday true. JUNIPER_ORDER_START=<n> numbers appended cards
# after the existing ones (build them in their own workdir and append their manifest rows; never renumber the 32).
import base64 as _b64
FLAME = 'data:image/png;base64,' + _b64.b64encode(open(R + 'assets/brand/flame-heart-holiday.png', 'rb').read()).decode()
OFF = int(os.environ.get('JUNIPER_ORDER_START', '1')) - 1
cards, man = [], []
for c in A['mats']:
    nm, brand, retired = c['name'], c['brand'], c['retired']
    src = Image.open(R + c['img'])
    m = flat(src).crop(tuple(c['box'])) if c.get('box') else (flat(src).crop(BOX[nm]) if nm in BOX else crop(src))
    rk, mr = reg_for(c['img'], nm)
    skipped = []
    if not mr:
        mr = []
        for k in c['racks']:
            l = KEYS[k]
            if l in TRACKS or l in mr or l in DROPPED: continue
            if not drawable(l): skipped.append(l); continue
            mr.append(l)
        if len(mr) < 2:
            for l in pick(m, exclude=TRACKS + mr + sorted(DROPPED)):
                if l not in mr and len(mr) < 2: mr.append(l)
    fn = f"juniper-mahjong-tiles-{slug(brand)}-{slug(nm)}-mat.jpg"
    code = footer(brand, retired); n = len(cards) + 1 + OFF; hol = bool(c.get('holiday'))
    cards.append({'slug': f'jun{n:02d}', 'title': f'Juniper + {nm}', 'col': CC['col'], 'tile_file': CC['tile'],
                  'tilefit': 'cover', 'racks': TRACKS, 'mat_racks': mr, 'file': fn, 'code': code, 'mat': uri(m), 'hol': hol, 'flame': FLAME if hol else None})
    man.append({'order': n, 'group': c['group'], 'mat': nm, 'brand': brand, 'retired_mat': retired, 'holiday': hol,
                'file': fn, 'code': code, 'src': c['img'], 'racks': TRACKS, 'mat_racks': mr, 'mat_reg': rk,
                'skipped_no_photo': skipped, 'why': c['why'],
                'caption_note': 'Holiday match' if hol else 'Pair mat' if nm == 'Lotus Cove' else ('New candidate' if c['group'] == 'new' else ('Weak: yours to cut' if c['group'] == 'weak' else None))})
json.dump({'_note': 'Juniper album DRAFT (Nov 6 round 3)', 'cards': cards, 'max_racks': 4, 'tile_brand': 'Oh My Mahjong',
           'navy': 'assets/brand/card_navy_logo_v3.png', 'true_len': True}, open(W + '/spec.json', 'w'))
json.dump({'set': 'Juniper', 'status': "DRAFT: round 3 = Tiffany's Nov 6 notes applied, pending her final order", 'cards': man, 'title_color': CC['col'], 'tile': CC['tile'],
           'racks_note': 'tile racks = colorcards juniper racks; mat racks = round-2 racks with real photos (not tile racks) + matpick fill'},
          open(W + '/manifest.json', 'w'), indent=1, ensure_ascii=False)
print(len(cards), 'cards')
