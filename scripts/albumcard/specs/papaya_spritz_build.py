"""Papaya Spritz (Oh My Mahjong) album: 53 cards in her approved order (scripts/albumcard/specs/papaya_spritz_album.json,
= Ready to Ship group c5-papaya-order; no saved db reorder exists, so the built default order stands).
Tile racks: final_lists 'papaya-spritz' (PLM Oak, PLM Chartreuse, B&B Lavender; her Oct 18 swap Lime Green -> Chartreuse).
Mat racks: config/mat-racks-picks.json registry when the mat is listed (Preppy Pink Garden, Larkspur), else matpick.py.
Zoom: her closer-crop list (album json 'zoom'). Goldie uses goldie-color-corrected.jpg (her approved photo);
Spring Fling uses spring-fling.png (her photo). Title colour #ec6f2d (same as the live Papaya + Preppy Pink Garden card).
Usage: python3 papaya_spritz_build.py <workdir>; then gen2.py <workdir>/spec.json <workdir>/cards"""
import json, io, base64, re, os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from matpick import pick
R = '/home/claude/mahjmatchmaker-data/'
W = sys.argv[1]
A = json.load(open(R + 'scripts/albumcard/specs/papaya_spritz_album.json'))
REG = {k: v for k, v in json.load(open(R + 'config/mat-racks-picks.json')).items() if isinstance(v, dict)}
TRACKS = json.load(open(R + 'config/tile-racks-picks.json'))['final_lists']['papaya-spritz']
PARTNERS = {b[0] for b in json.load(open(R + 'work/pub/catalog.json'))['B']}
PCT = {'Britt Mills': '15%', 'Amanda Toppe': '20%', 'Royal Mahjong Society': '15%'}
NOPCT = {'Anders Ruff', 'Mahjong Register', 'The Mahjong Press'}
SRC = {'Goldie (retired)': 'assets/mats/clean/goldie-omm.png', 'Spring Fling (retired)': 'assets/mats/omm-retired/spring-fling.png'}
def footer(b, retired):
    if retired or b not in PARTNERS: return '10% OFF  USE CODE : MAHJMATCH'  # Oct 18 rule: no SHOP THE MATCH footers; every card carries MAHJMATCH (the code works on the Oh My Mahjong tiles)
    if b in NOPCT: return 'SAVE WITH CODE : MAHJMATCH'
    return f"{PCT.get(b, '10%')} OFF  USE CODE : MAHJMATCH"
def flat(im):
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA'); bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[3]); return bg
    return im.convert('RGB')
def uri(im, maxs=1400):
    im = im.copy(); im.thumbnail((maxs, maxs)); b = io.BytesIO(); im.convert('RGB').save(b, 'JPEG', quality=90)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
def crop(im, box=None):
    im = flat(im)
    if box:
        im = im.crop(tuple(box)); Wd, H = im.size
        cw = min(Wd, int(H * .973)); ch = int(cw / .973); x0 = (Wd - cw) // 2; y0 = (H - ch) // 2
        return im.crop((x0, y0, x0 + cw, y0 + ch))
    Wd, H = im.size; z = .72 if Wd >= 900 else 1.0
    cw = int(Wd * z); ch = int(cw / .973)
    if ch > H: ch = H; cw = int(ch * .973)
    return im.crop((0, H - ch, cw, H))
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower().replace('&', 'and').replace("'", '')).strip('-')
def reg_for(path, name):
    for k, v in REG.items():
        if path in v.get('files', []) or slug(name) == k: return k, v['racks']
    return None, None
cards, man = [], []
for c in A['order']:
    nm = c['name']; brand = c['brand']; retired = '(retired)' in nm; clean = re.sub(r'\s*\(.*', '', nm)
    path = SRC.get(nm, c['img']); src = Image.open(path if path.startswith('/') else R + path)
    box = A['zoom'].get(nm) or c.get('mat_crop')
    m = crop(src, box)
    rk, mr = reg_for(path, clean)
    if not mr: mr = pick(m, exclude=TRACKS)
    fn = f"papaya-spritz-mahjong-tiles-{slug(brand)}-{slug(clean)}-mat.jpg"
    code = footer(brand, retired); n = len(cards) + 1
    cards.append({'slug': f'pap{n:02d}', 'title': f'Papaya Spritz + {clean}', 'col': '#ec6f2d', 'tile_file': 'assets/tiles/album/papaya-spritz.jpg',
                  'tilefit': 'cover', 'racks': TRACKS, 'mat_racks': mr, 'file': fn, 'code': code, 'mat': uri(m)})
    man.append({'order': n, 'vote_id': c['id'], 'tier': c['tier'], 'mat': clean, 'brand': brand, 'retired_mat': retired, 'holiday': False,
                'file': fn, 'code': code, 'src': path, 'zoom': bool(box), 'racks': TRACKS, 'mat_racks': mr, 'mat_reg': rk,
                'caption_note': 'Pair mat' if clean == 'Vivienne' else None})
json.dump({'_note': 'Papaya Spritz album v1 (Oct 18)', 'cards': cards, 'max_racks': 4, 'tile_brand': 'Oh My Mahjong'}, open(W + '/spec.json', 'w'))
json.dump({'set': 'Papaya Spritz', 'cards': man, 'title_color': '#ec6f2d', 'tile': 'assets/tiles/album/papaya-spritz.jpg',
           'racks_note': 'tile racks final_lists papaya-spritz; mat racks registry or matpick'}, open(W + '/manifest.json', 'w'), indent=1)
print(len(cards), 'cards')
