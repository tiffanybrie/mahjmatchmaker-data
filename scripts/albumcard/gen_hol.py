"""Holiday album cards from the holiday rack picker data (Claude's default rack picks).
Usage: python3 gen_hol.py <picker data5.json> <outdir> [group:mat ...]
Same card layout as gen.py (card.html). Footer code follows the MAT brand's code rules."""
import json, sys, os, io, base64, re, subprocess, glob
from PIL import Image
R = '/home/claude/mahjmatchmaker-data/'
D = json.load(open(sys.argv[1])); out = sys.argv[2]; only = set(sys.argv[3:])
os.makedirs(out, exist_ok=True); os.makedirs('/tmp/holcards/html', exist_ok=True)
M = json.load(open('/tmp/hol/mats.json'))
BB = {x['name']: x['hex'] for x in json.load(open(R + 'work/bbracks.json'))}
logos = json.load(open(R + 'builder/logos/map.json'))
dom = {}
for l in open(R + 'work/domains.tsv'):
    p = l.strip().split('\t')
    if len(p) == 2: dom[p[1].replace('www.', '')] = p[0]

def uri(im, fmt='JPEG', q=88, maxs=None):
    if isinstance(im, str): im = Image.open(im)
    if maxs: im = im.copy(); im.thumbnail((maxs, maxs))
    b = io.BytesIO()
    if fmt == 'PNG': im.save(b, 'PNG')
    else: im.convert('RGB').save(b, 'JPEG', quality=q)
    return f'data:image/{fmt.lower()};base64,' + base64.b64encode(b.getvalue()).decode()
def dimg(s): return Image.open(io.BytesIO(base64.b64decode(s.split(',', 1)[1])))
def lum(h):
    h = h.lstrip('#'); r, g, b = [int(h[k:k+2], 16) for k in (0, 2, 4)]; return .299*r + .587*g + .114*b

# --- mat photos: hi-res product photo if we have it, else picker BIG, else the row thumbnail
OVR = {'bespoke-chalet': R + 'assets/mats/holiday/bespoke-chalet.png'}
def mat_image(m, row):
    if m in OVR: return Image.open(OVR[m])
    for v in M.values():
        h = v.get('handle', '')
        if h and (h == m or h.startswith(m) or m.startswith(h)) and os.path.exists(v.get('hi', '')):
            return Image.open(v['hi'])
    if m in D['BIG']: return dimg(D['BIG'][m])
    if row.get('img','').startswith('data:'): return dimg(row['img'])
    return None
def trim(im):
    """cut plain white/near-white margins around a product photo"""
    g = im.convert('L').point(lambda p: 255 if p < 235 else 0)
    bb = g.getbbox()
    return im.crop(bb) if bb else im
def flat(im):
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA'); bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[3]); return bg
    return im.convert('RGB')
def mat_crop(im):
    """close-up of the lower-left part of the mat (her album style); card mat area is 1080x1000.
    Small source photos show the whole mat instead (zooming them goes blurry)."""
    im = trim(flat(im)); W, H = im.size
    z = .72 if W >= 900 else 1.0
    cw = int(W * z); ch = int(cw / 0.973)
    if ch > H: ch = H; cw = int(ch * 0.973)
    return im.crop((0, H - ch, cw, H))

# --- tile images (album tile shots; holiday sets use their studio pile shots)
TILE = {'cypress-forest': 'assets/tiles/album/cypress.jpg', 'tortoise': 'assets/tiles/album/classic-tortoise-zoom.jpg',
        'december-1994': 'assets/tiles/sunday_mahjong_december_1994_tilebox_CARD-ONLY-edited.jpg',
        'sunday': 'assets/tiles/sunday-tile-set.png',
        'holly-jolly-red': 'assets/tiles/holiday/holly-jolly-red-pile.jpg', 'holly-jolly-pink': 'assets/tiles/holiday/holly-jolly-pink-pile.jpg'}  # Tiffany Oct 15: Bam!'s pile shots
def tile_image(g):
    t = g['t']
    if t in TILE and os.path.exists(R + TILE[t]): return R + TILE[t]
    for ext in ('jpg', 'png'):
        p = R + f'assets/tiles/album/{t}.{ext}'
        if os.path.exists(p): return p
    p = f'/tmp/xt/pile_{t}.jpg'
    if os.path.exists(p): return p
    return dimg(g['img'])

# --- footer: code rules by MAT brand
PCT = {'Britt Mills': '15%', 'Amanda Toppe': '20%', 'Royal Mahjong Society': '15%'}
NOPCT = {'Anders Ruff', 'Mahjong Register', 'The Mahjong Press'}
NOCODE = {'Sunday Mahjong', 'Luxe Mahjong', 'Maison Mahj', 'Lucky Daughters', 'Mahjong Studios', 'I Love Mahj', 'Mahjong by SI', "Let's Be Besties", 'Mahj Tile Haus', 'Ozark Mahjongg', ''}  # no code on the hub
def footer(brand, tileset):
    if tileset == 'coquette' or brand in NOCODE: return 'SHOP THE MATCH : MAHJMATCHMAKER.COM'
    if brand in NOPCT: return 'SAVE WITH CODE : MAHJMATCH'
    return f"{PCT.get(brand, '10%')} OFF  USE CODE : MAHJMATCH"

def brand_logo(key, name):
    d = key.split('/')[0].replace('www.', '') if '/' in key else ''
    cands = []
    if key.startswith('plm:'): cands = ['Peace Love Mahjong']
    else:
        page = dom.get(d, '')
        for b in logos:
            slug = re.sub(r'[^a-z0-9]+', '-', b.lower()).strip('-')
            if slug and slug in page: cands.append(b)
        cands += [b for b in logos if name.startswith(b) or name.startswith(b.replace(' Mahjong', '') + ' ')]
    for b in cands:
        if b in logos: return uri(R + 'builder/logos/' + logos[b], 'PNG')
    return None

html_tpl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'card2.html')).read()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import racks as RKS
OMM = uri(R + 'assets/brand/omm_certified.png', 'PNG'); NAVY = uri(R + 'assets/brand/card_navy_logo.png', 'PNG')
BBLOGO = uri(R + 'builder/logos/' + logos['Bird & Bamboo'], 'PNG')
FLAME = uri(R + 'assets/brand/flame-heart-holiday.png', 'PNG')
COLS = json.load(open(R + 'scripts/albumcard/holiday_title_colors.json')) if os.path.exists(R + 'scripts/albumcard/holiday_title_colors.json') else {}
SKIP = {'omm-dapper-1', 'omm-dapper-2', 'britt-crimson-harvest', 'christmas-solo-play-mahjong-mat', 'snowflake-reindeer-lodge-double-sided-leatherette-mahjong-ma'}
jobs = []; manifest = []
for g in D['G']:
    tile = tile_image(g); tileuri = uri(tile, maxs=800) if isinstance(tile, str) else uri(tile)
    for i, r in enumerate(g['rows']):
        if r['m'] in SKIP: continue
        if only and f"{g['t']}:{r['m']}" not in only: continue
        mi = mat_image(r['m'], r)
        if mi is None: print('NO MAT PHOTO', g['t'], r['m']); continue
        mat = mat_crop(mi)
        drawn = []; chart = []
        for k in r['def']:
            if len(drawn) >= 2: break
            if k.startswith('bb:'):
                im = RKS.bb(k[3:]); lab = 'Bird & Bamboo ' + k[3:]
            else:
                im = RKS.photo(k); lab = RKS.P[k]['n'] if k in RKS.P else D['RK'][k][0]
            if im is not None: drawn.append({'img': uri(im, 'PNG'), 'label': lab})
        dl = {d['label'] for d in drawn}
        for k in r['def']:
            if k.startswith('bb:') and 'Bird & Bamboo ' + k[3:] not in dl and k[3:] in BB:
                chart.append({'name': k[3:], 'hex': BB[k[3:]], 'light': lum(BB[k[3:]]) > 185})
        tname = re.sub(r'\s*\(.*?\)', '', g['n']).strip()
        mname = re.sub(r'\s*\((retired|Nantucket pair|double-sided|Dapper 2)\)', '', r['n'], flags=re.I)
        mname = re.sub(r'\s*\((.*?)\)', r' \1', mname).replace(' Mat', '').replace(' Center', '').replace(' Border', '').strip()
        if mname == 'Holiday': mname = {'Peace Love Mahjong': 'Peace Love Holiday', 'Bam Bird Boutique': 'Bam Bird Holiday'}.get(r['b'], mname)
        title = f"{tname} + {mname}"
        col = COLS.get(g['t'], '#a3192e')
        slug = re.sub(r'[^a-z0-9]+', '-', f"{g['t']}-mahjong-tiles-{r['b']}-{mname}-mat".lower()).strip('-')
        fn = slug + '.jpg'
        h = html_tpl.replace('__DATA__', json.dumps({'title': title, 'col': col, 'mat': uri(mat, maxs=1400), 'tile': tileuri,
            'racks': drawn, 'bb': chart[:3], 'bblogo': BBLOGO, 'navy': NAVY, 'code': footer(r['b'], g['t']), 'hol': True, 'flame': FLAME}))
        hf = f"/tmp/holcards/html/{slug}.html"; open(hf, 'w').write(h)
        jobs.append((hf, os.path.join(out, fn)))
        manifest.append({'tile': g['t'], 'tileName': g['n'], 'hol': g['hol'], 'mat': r['m'], 'matName': r['n'], 'brand': r['b'],
                         'star': r.get('star', False), 'racks': r['def'], 'file': fn, 'title': title, 'order': i})
json.dump(manifest, open(os.path.join(out, 'manifest.json'), 'w'), indent=1)
js = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shot.js')
NP = subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True).stdout.strip()
for i in range(0, len(jobs), 40):
    subprocess.run(['node', js] + [x for p in jobs[i:i+40] for x in p], check=True, env={**os.environ, 'NODE_PATH': NP}, stdout=subprocess.DEVNULL)
print(len(jobs), 'cards ->', out)
