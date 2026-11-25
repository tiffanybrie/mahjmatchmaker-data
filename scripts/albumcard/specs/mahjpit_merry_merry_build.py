"""Mahj Pit Merry Merry album cards, DRAFT (Nov 25 2026): sadie_jane_build.py adapted. Tile racks = config/colorcards.json
mahjpit-merry-merry racks (Bird & Bamboo Cherry Red + Gold Metallic: nearest to the cherry face resin and the gold confetti
backs; Mahj Pit has no racks of its own in the catalog). Mat racks = matpick nearest Bird & Bamboo colours (2), no prior
rack feedback from her yet on this set so no prefer/exclude tuning beyond the tile racks themselves.
Usage: python3 mahjpit_merry_merry_build.py mahjpit-merry-merry <workdir>; then gen2.py <workdir>/spec.json assets/cards/mahjpit-merry-merry"""
import json, io, base64, re, os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from matpick import pick
R = '/home/claude/mahjmatchmaker-data/'
KEY, W = sys.argv[1], sys.argv[2]; os.makedirs(W, exist_ok=True)
A = json.load(open(R + f'scripts/albumcard/specs/{KEY}_nov25.json'))
CC = json.load(open(R + 'config/colorcards.json'))['sets'][KEY]
TRACKS = CC['racks']
MEM = json.load(open(R + 'config/mat-rack-memory.json'))['mats']
NEVER = {(x['brand'], x['name']) for x in json.load(open(R + 'config/album-never-show.json'))['mats']}
A['mats'] = [m for m in A['mats'] if (m.get('brand'), m.get('name')) not in NEVER]
INSET = "assets/tiles/album/mahjpit-merry-merry.jpg"  # the approved, straightened tile photo itself (no flower/other inset crop for this set)
SNAP = json.load(open(R + 'config/fym-mats-snapshot.json'))['mats']
NOPCT = {'Anders Ruff', 'Mahjong Register', 'The Mahjong Press'}
import base64 as _b64
FLAME = 'data:image/png;base64,' + _b64.b64encode(open(R + 'assets/brand/flame-heart-holiday.png', 'rb').read()).decode()
def is_partner(c):
    if 'partner' in c: return bool(c['partner'])
    m = SNAP.get(c.get('fym'), {})
    return bool(m.get('pa')) and not m.get('nc')
def footer(c):  # Nov 8 HARD RULE: Mahj Pit tiles are a partner (code-truth.json pct.Mahj Pit = 10), so the code band is ALWAYS on
    if not is_partner(c): return 'SAVE WITH CODE : MAHJMATCH'
    return 'SAVE WITH CODE : MAHJMATCH' if c['brand'] in NOPCT else '10% OFF  USE CODE : MAHJMATCH'
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
cards, man = [], []; RUSE = {}
for c in A['mats']:
    nm, brand = c['name'], c['brand']
    src = Image.open(R + c['img']); m = flat(src).crop(tuple(c['box'])) if c.get('box') else crop(src)
    mr = []
    _over = [k for k, v in RUSE.items() if v >= 12]  # no one rack on more than 12 cards: keep the mat matches varied
    for l in pick(m, exclude=list(TRACKS) + _over, prefer={}, prefer_de=10):
        if l not in mr and len(mr) < 2: mr.append(l)
    mr = [l for l in mr if l] or ['Bird & Bamboo Light Pink']
    if c.get('mat_racks'): mr = list(c['mat_racks'])
    elif MEM.get(f"{c.get('brand')}|{c.get('name')}"): mr = list(MEM[f"{c.get('brand')}|{c.get('name')}"]['racks'])  # a mat keeps the racks she approved before, if any
    if len(mr) < 2:
        for l in pick(m, exclude=list(TRACKS) + _over + mr, k=8, maxn=2):
            if l not in mr: mr.append(l); break
    for l in mr: RUSE[l] = RUSE.get(l, 0) + 1
    fn = f"{KEY}-mahjong-tiles-{slug(brand)}-{slug(nm)}-mat.jpg"; n = len(cards) + 1
    code = footer(c); hol = bool(c.get('holiday'))
    cards.append({'slug': f'{KEY[:6]}{n:02d}', 'title': f"{CC['name']} + {c.get('short') or nm}", 'col': CC['col'], 'tile_file': INSET,
                  'tilefit': 'cover', 'racks': TRACKS, 'mat_racks': mr, 'file': fn, 'code': code, 'mat': uri(m), 'hol': hol, 'flame': FLAME if hol else None})
    note = 'Holiday match' if c.get('holiday') else ('Retired' if c['retired'] else None)
    man.append({'order': n, 'group': c['group'], 'mat': nm, 'brand': brand, 'retired_mat': c['retired'], 'holiday': hol, 'partner': is_partner(c), 'file': fn,
                'code': code, 'src': c['img'], 'racks': TRACKS, 'mat_racks': mr, 'why': c['why'], 'fym': c.get('fym'), 'lowres': c.get('lowres'),
                'caption_note': note, 'rack_notes': []})
json.dump({'_note': f'{KEY} album DRAFT (Nov 25)', 'cards': cards, 'max_racks': 4, 'tile_brand': 'Mahj Pit',
           'navy': 'assets/brand/card_navy_logo_v4.png', 'true_len': False}, open(W + '/spec.json', 'w'))
json.dump({'set': CC['name'], 'status': "DRAFT: Claude's own picks, pending Tiffany's review", 'groups': A['groups'], 'cards': man,
           'title_color': CC['col'], 'tile': CC['tile'],
           'racks_note': 'tile racks = Bird & Bamboo Cherry Red + Gold Metallic (no Mahj Pit racks in the catalog); mat racks = matpick nearest Bird & Bamboo colours'},
          open(W + '/manifest.json', 'w'), indent=1, ensure_ascii=False)
print(len(cards), 'cards')
sys.path.insert(0, R + 'scripts/checks'); import rack_colour_check as _RC
_b = _RC.run(R + f'scripts/albumcard/specs/{KEY}_nov25.json')
if _b: sys.exit('REFUSED (rack colour check, Tiffany Nov 23): a mat rack colour is not in the mat:\n  ' + '\n  '.join(_b))
