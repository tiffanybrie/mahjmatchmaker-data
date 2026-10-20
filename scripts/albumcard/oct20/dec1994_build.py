"""December 1994 (Sunday Mahjong) holiday cards, Oct 20 rebuild from her Ready to Ship notes:
- c5-dec1994 (Oct 16 12:04pm): her saved order of the 31 cards; "You have Bird & Bamboo wood racks matched to the mat, revise.
  There are low res images in some of these, including my #1 pick".
- Tile racks on ALL 31 = her LOCKED Holiday Tile Racks picker picks (config/holiday-picker-picks.json, exported Oct 16 3:22pm,
  after her Oct 15 1pm Red/Evergreen/Oak call): PLM Dark Green + B&B Brick Red + Middle & Main Hawksbill Heritage Tortoise.
  The 5 live cards already use them; the 26 newer cards had Red/Evergreen/Oak and 2 cards had Radish/Almond. Now consistent.
- Mat racks: config/mat-racks-picks.json registry when listed; else the earlier pick UNLESS it is a B&B wood
  (Red Mahogany, Provincial, Weathered Oak, Tudor, Almond, Dark Walnut; banned doc 57), which is re-picked by matpick.py
  (woods excluded). Vintage Oxblood Leather = B&B Wine + PLM Acrylic Burl (her standing rule). Festive Plaid keeps B&B Pink
  Coral (decision o-pinkcoral still open with her). Polo Club keeps Middle & Main Golden Grain Beechwood (real wood photo).
- Photos: brand hi-res where the brand's Shopify page has the same photo bigger (hd_fetch.py), assets/mats/holiday/hd,
  else EDSR x4 super-resolution for the smallest (Festive Plaid #1, Cognac, Hollivia, Vegan Leather, Crimson Harvest).
- Zoom: the album lower-left close-up (72%) only when it still leaves 900px+ of mat; smaller photos show the whole mat.
- Footers: gen_hol.py rule (every card carries MAHJMATCH).
Usage: python3 dec1994_build.py <workdir>; then gen2.py <workdir>/spec.json assets/cards/december-1994-oct20"""
import json, io, base64, re, os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from matpick import pick, BB_WOODS
R = '/home/claude/mahjmatchmaker-data/'; W = sys.argv[1]; os.makedirs(W, exist_ok=True)
S = '/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/'
O = S + 'owedwork/d94/'
L = {x['vote_id']: x for x in json.load(open(O + 'list.json'))}
ORDER = [os.path.basename(x) for x in json.load(open(S + 'rts/ship/c5-dec1994.json'))['order']]
D = json.load(open('/tmp/claude-0/-home-claude-mahjmatchmaker-data/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/dec1994_v1/data_d94.json'))
ROWS = next(g for g in D['G'] if g['t'] == 'december-1994')['rows']
REG = {k: v for k, v in json.load(open(R + 'config/mat-racks-picks.json')).items() if isinstance(v, dict)}
TRACKS = ['Peace Love Mahjong Dark Green', 'Bird & Bamboo Brick Red', 'Middle & Main Hawksbill Heritage Tortoise']
LOCALHD = {'tartan-tidings-mahjong-mat': 'tartan-tidings-mahjong-mat.jpg', 'tartan-toile-noel-mahjong-mat': 'tartan-toile-noel-mahjong-mat.jpg',
           'polo-club': 'luxe-polo-club.jpg', 'classic-very-merry-mahj-mahjong-mat': 'ar-classic-very-merry-mahj.jpg',
           'cmc-ski-club-red-sweater': 'cmc-ski-club-red-sweater.jpg', 'rackin-rudolph-mahjong-mat': 'rackin-rudolph-mahjong-mat.jpg',
           'c-rattan-premium-mahjong-mat': 'sunday-rattan.jpg'}
FIXED = {'s-vintage-oxblood-leather-mahjong-by-si': ['Bird & Bamboo Wine', 'Peace Love Mahjong Acrylic Burl']}
PCT = {'Britt Mills': '15%', 'Amanda Toppe': '20%', 'Royal Mahjong Society': '15%'}
NOPCT = {'Anders Ruff', 'Mahjong Register', 'The Mahjong Press'}
NOCODE = {'Sunday Mahjong', 'Luxe Mahjong', 'Lucky Daughters', 'Mahjong Studios', 'I Love Mahj', 'Mahjong by SI', "Let's Be Besties", 'Mahj Tile Haus', 'Ozark Mahjongg', ''}
def footer(b):
    if b in NOCODE or b in NOPCT: return 'SAVE WITH CODE : MAHJMATCH'
    return f"{PCT.get(b, '10%')} OFF  USE CODE : MAHJMATCH"
def trim(im):
    g = im.convert('L').point(lambda p: 255 if p < 235 else 0); b = g.getbbox(); return im.crop(b) if b else im
def flat(im):
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA'); bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[3]); return bg
    return im.convert('RGB')
def mat_crop(im, full=False):
    im = trim(flat(im)); Wd, H = im.size; z = 1.0 if full or Wd * .72 < 900 else .72  # Oct 20: never zoom a photo below ~900px of mat (her low-res note)
    cw = int(Wd * z); ch = int(cw / 0.973)
    if ch > H: ch = H; cw = int(ch * 0.973)
    return im.crop((0, H - ch, cw, H))
def source(m):
    if os.path.exists(O + f'sr/{m}.jpg'): return Image.open(O + f'sr/{m}.jpg'), 'EDSR x4', True  # keep the whole-mat framing she reviewed
    best = None
    for p, how in [(O + f'img/{m}.jpg', 'brand hi-res'), (R + 'assets/mats/holiday/hd/' + LOCALHD.get(m, '-'), 'hd library')]:
        if os.path.exists(p):
            im = Image.open(p)
            if best is None or im.width > best[0].width: best = (im, how)
    if best:
        orig = Image.open(O + f'src/{m}.jpg').width
        return best[0], f'{best[1]} {best[0].width}px', orig < 900  # small originals were shown whole; keep that framing
    return Image.open(O + f'src/{m}.jpg'), 'original', False
def uri(im, maxs=1600):
    im = im.copy(); im.thumbnail((maxs, maxs), Image.LANCZOS); b = io.BytesIO(); im.convert('RGB').save(b, 'JPEG', quality=92)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
def mname(r):
    n = re.sub(r'\s*\((retired|Nantucket pair|double-sided|Dapper 2)\)', '', r['n'], flags=re.I)
    n = re.sub(r'\s*\((.*?)\)', r' \1', n).replace(' Mat', '').replace(' Center', '').replace(' Border', '').strip()
    if n == 'Holiday': n = {'Peace Love Mahjong': 'Peace Love Holiday', 'Bam Bird Boutique': 'Bam Bird Holiday'}.get(r['b'], n)
    return n
def fslug(r): return re.sub(r'[^a-z0-9]+', '-', f"december-1994-mahjong-tiles-{r['b']}-{mname(r)}-mat".lower()).strip('-') + '.jpg'
BYFILE = {fslug(r): r for r in ROWS}
def nm_bb(k): return 'Bird & Bamboo ' + k[3:] if k.startswith('bb:') else ('Middle & Main Golden Grain Beechwood' if 'golden-grain' in k else k)
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower().replace('&', 'and').replace("'", '')).strip('-')
TILE = 'assets/tiles/sunday_mahjong_december_1994_tilebox_CARD-ONLY-edited.jpg'
COLS = json.load(open(R + 'scripts/albumcard/holiday_title_colors.json')); COL = COLS.get('december-1994', '#a3192e')
cards, man = [], []
for i, fn in enumerate(ORDER, 1):
    r = BYFILE[fn]; m = r['m']; im, how, full = source(m); mat = mat_crop(im, full)
    nm = mname(r); rk = next((k for k in REG if k in (slug(nm), slug(r['b']) + '-' + slug(nm))), None)
    old = [nm_bb(k) for k in r.get('mats', [])]
    if m in FIXED: mr, why = FIXED[m], 'her standing rule'
    elif rk: mr, why = REG[rk]['racks'], f'registry {rk}'
    elif any(o.replace('Bird & Bamboo ', '') in BB_WOODS for o in old): mr, why = pick(mat, exclude=TRACKS + ['Radish', 'Almond', 'Red', 'Cherry Red']), f'B&B wood {old} re-picked'  # as in specs/december_1994_build.py: never repeat the red/green tile racks
    else: mr, why = old, 'earlier pick kept'
    cards.append({'slug': f'd94-{i:02d}', 'title': f'December 1994 + {nm}', 'col': COL, 'tile_file': TILE, 'racks': TRACKS, 'mat_racks': mr,
                  'file': fn, 'code': footer(r['b']), 'mat': uri(mat), 'hol': True})
    man.append({'order': i, 'mat': nm, 'brand': r['b'], 'file': fn, 'photo': how, 'crop_px': mat.size[0], 'mat_racks': mr, 'why': why, 'code': footer(r['b'])})
FLAME = 'data:image/png;base64,' + base64.b64encode(open(R + 'assets/brand/flame-heart-holiday.png', 'rb').read()).decode()
for c in cards: c['flame'] = FLAME
json.dump({'_note': 'December 1994 Oct 20', 'cards': cards, 'max_racks': 4, 'tile_brand': 'Sunday Mahjong'}, open(W + '/spec.json', 'w'))
json.dump({'set': 'December 1994', 'tile_racks': TRACKS, 'cards': man}, open(W + '/manifest.json', 'w'), indent=1)
for c in man: print(c['order'], c['mat'], '|', c['photo'], c['crop_px'], '|', c['mat_racks'], '|', c['why'])
