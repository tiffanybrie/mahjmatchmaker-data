"""Oct 16 rebuild (gen_hol3): Tiffany's tile-side picks (picker db + locked final_lists), HD mats, mat-side picks
from the sharp mat photo (matpick, no B&B woods). Prep: prep_hol3.py writes data6.json.
Holiday album cards from the holiday rack picker data (Claude's default rack picks).
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
HDOVR = json.load(open(R + 'scripts/albumcard/live_hd/hdovr.json'))
def mat_image(m, row):
    if m in HDOVR: return Image.open(HDOVR[m][0])
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
TILE = {'cypress-forest': 'assets/tiles/album/cypress.jpg', 'tortoise': 'assets/tiles/album/classic-tortoise.png',
        'december-1994': 'assets/tiles/sunday_mahjong_december_1994_tilebox_CARD-ONLY-edited.jpg',
        'sunday': 'assets/tiles/album/sunday-tile-set.png',
        'holly-jolly-red': 'assets/tiles/holiday/holly-jolly-red-pile.jpg', 'cmc-apres-ski': 'assets/tiles/holiday/cmc-apres-ski.jpg', 'dear-santa': 'assets/tiles/holiday/dear-santa.jpg', 'holly-jolly-green': 'assets/tiles/holiday/holly-jolly-green.jpg', 'nivalee-blue': 'assets/tiles/holiday/nivalee-blue.jpg', 'nutcracker-ballet': 'assets/tiles/holiday/nutcracker-ballet.jpg', 'rackin-rudolph': 'assets/tiles/holiday/rackin-rudolph.jpg', 'tinselle-emerald': 'assets/tiles/holiday/tinselle-emerald-3x3.jpg', 'tinselle-ruby': 'assets/tiles/holiday/tinselle-ruby-3x3.jpg', 'holly-jolly-pink': 'assets/tiles/holiday/holly-jolly-pink-pile.jpg'}  # Tiffany Oct 15: Bam!'s pile shots
TBRAND = {'tortoise': 'Bam Bird Boutique', 'jade': 'Miss Mahjong', 'malachite': 'Miss Mahjong', 'cypress-forest': 'Mahjong Row & Co.', 'cmc-apres-ski': 'Charleston Mahjong Club'}  # Oct 17: real tile-set brands (data6 had OMM)
LOOSE_T = {'tortoise', 'hummingbird'}  # Oct 17: transparent tiles lie loose on the mat, no tile box
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
PCT = {}  # Oct 21 (Tiffany): card code bands ALWAYS say 10% (the safe floor: 'it might be more, but it's never less'). Real brand % lives on brand pages. Gate: scripts/albumcard/codeband_lint.py
NOPCT = {'Anders Ruff', 'Mahjong Register', 'The Mahjong Press'}
NOCODE = {'Sunday Mahjong', 'Luxe Mahjong', 'Maison Mahj', 'Lucky Daughters', 'Mahjong Studios', 'I Love Mahj', 'Mahjong by SI', "Let's Be Besties", 'Mahj Tile Haus', 'Ozark Mahjongg', ''}  # no code on the hub
def footer(brand, tileset):
    if tileset == 'coquette' or brand == 'Maison Mahj': return 'SHOP THE MATCH : MAHJMATCHMAKER.COM'
    if brand in NOCODE: return 'SAVE WITH CODE : MAHJMATCH'  # rule Oct 18: every card carries MAHJMATCH (only Coquette / Maison Mahj keep shop-the-match)
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
from matpick import pick as MATPICK

import numpy as _np
import matpick as _MP
from skimage.color import deltaE_ciede2000 as _dE
_RC = {}
def _rack_lab(k):
    if k in _RC: return _RC[k]
    if k.startswith('bb:'):
        h = BB.get(k[3:]); lab = _MP._lab(h) if h else None
    else:
        im = RKS.photo(k)
        if im is None: lab = None
        else:
            a = _np.asarray(im.convert('RGBA')).reshape(-1, 4); a = a[a[:, 3] > 200][:, :3]
            m = _np.median(a, 0).astype(int); lab = _MP._lab('#%02x%02x%02x' % tuple(m))
    _RC[k] = lab; return lab
def near_tile_colours(keys, thr=14):
    labs = [l for l in (_rack_lab(k) for k in keys) if l is not None]
    return [n for n, v in _MP.BBL.items() if any(_dE(v, l) < thr for l in labs)]
LOWRES = []
OMM = uri(R + 'assets/brand/omm_certified.png', 'PNG'); NAVY = uri(R + 'assets/brand/card_navy_logo_v2.png', 'PNG')  # Oct 16: current tagline, 2x
BBLOGO = uri(R + 'builder/logos/' + logos['Bird & Bamboo'], 'PNG')
FLAME = uri(R + 'assets/brand/flame-heart-holiday.png', 'PNG')
COLS = json.load(open(R + 'scripts/albumcard/holiday_title_colors.json')) if os.path.exists(R + 'scripts/albumcard/holiday_title_colors.json') else {}
SKIP = {'omm-dapper-1', 'omm-dapper-2', 'britt-crimson-harvest', 'christmas-solo-play-mahjong-mat', 'snowflake-reindeer-lodge-double-sided-leatherette-mahjong-ma'}
MATREG = json.load(open(R + 'config/mat-racks-picks.json'))
jobs = []; manifest = []
for g in D['G']:
    tile = tile_image(g); loose = g['t'] in LOOSE_T
    tileuri = uri(tile, 'PNG' if loose else 'JPEG', maxs=900 if loose else 800) if isinstance(tile, str) else uri(tile, 'PNG' if loose else 'JPEG')
    for i, r in enumerate(g['rows']):
        if r['m'] in SKIP: continue
        if only and f"{g['t']}:{r['m']}" not in only: continue
        mi = mat_image(r['m'], r)
        if mi is None: print('NO MAT PHOTO', g['t'], r['m']); continue
        if max(mi.size) < 900: LOWRES.append([g['t'], r['m'], mi.size])
        mat = mat_crop(mi)
        if r['m'] in MATREG and isinstance(MATREG[r['m']], dict):  # Oct 18: locked mat racks ("once we've matched the mats, the mats are matched")
            r['mats'] = [('bb:' + x[len('Bird & Bamboo '):]) if x.startswith('Bird & Bamboo ') else x for x in MATREG[r['m']]['racks']]
        if 'tiles' in r and 'mats' not in r:  # mat side from the SHARP full mat photo; colours not already on the tile side
            ex = ['Bird & Bamboo ' + n for n in near_tile_colours(r['tiles'])]  # Oct 15 rule: mat side shows the mat colours NOT already on the tile side
            r['mats'] = ['bb:' + x[len('Bird & Bamboo '):] for x in MATPICK(trim(flat(mi)), exclude=ex, maxn=3)]
        drawn = []; chart = []; mr = []
        def rack(k):
            if k.startswith('bb:'): return RKS.bb(k[3:]), 'Bird & Bamboo ' + k[3:], 1.0
            lab = RKS.P[k]['n'] if k in RKS.P else D.get('RK', {}).get(k, [k])[0]
            return RKS.photo(k), lab, RKS.frac(k)
        if 'tiles' in r:  # Oct 15: explicit tile racks (lower left, up to 4, same angle + length) and mat picks (upper right)
            for k in r['tiles'][:4]:
                im, lab, fr = rack(k)
                if im is None: print('NO REAL PHOTO', r['m'], k); continue
                drawn.append({'img': uri(im, 'PNG'), 'label': lab, 'frac': fr, 'ar': im.width / im.height})
            for k in r.get('mats', []):
                if k.startswith('bb:'):
                    if k[3:] in BB: chart.append({'name': k[3:], 'hex': BB[k[3:]], 'light': lum(BB[k[3:]]) > 185})
                    continue
                im, lab, fr = rack(k)
                if im is None: print('NO REAL PHOTO', r['m'], k); continue
                b = next((b for b in sorted(logos, key=len, reverse=True) if lab.startswith(b + ' ')), None)
                if b is None and lab.startswith('Middle & Main '): b = 'Middle & Main Mahjong'
                nm = lab[len(b) + 1:] if b and lab.startswith(b + ' ') else lab.replace('Middle & Main ', '')
                mr.append({'img': uri(im, 'PNG', maxs=700), 'name': nm, 'full': lab})  # Oct 15 evening: no rack-brand logos on the mat side
        else:
            for k in r['def']:
                if len(drawn) >= 2: break
                im, lab, fr = rack(k)
                if im is not None: drawn.append({'img': uri(im, 'PNG'), 'label': lab, 'frac': fr, 'ar': im.width / im.height})
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
        tl = RKS.tile_logo(TBRAND.get(g['t'], g.get('b'))); tl = uri(tl, 'PNG', maxs=500) if tl else None  # tile set logo flag (Oct 15 evening)
        h = html_tpl.replace('__DATA__', json.dumps({'loose': loose, 'tlogo': tl, 'title': title, 'col': col, 'mat': uri(mat, maxs=1400), 'tile': tileuri,
            'racks': drawn, 'bb': chart[:3], 'mr': mr[:2], 'bblogo': BBLOGO, 'navy': NAVY, 'code': footer(r['b'], g['t']), 'hol': True, 'flame': FLAME}))
        hf = f"/tmp/holcards/html/{slug}.html"; open(hf, 'w').write(h)
        jobs.append((hf, os.path.join(out, fn)))
        manifest.append({'tile': g['t'], 'tileName': g['n'], 'hol': g['hol'], 'mat': r['m'], 'matName': r['n'], 'brand': r['b'],
                         'star': r.get('star', False), 'racks': r.get('tiles', r['def']), 'mat_picks': r.get('mats'), 'file': fn, 'title': title, 'order': i})
json.dump(manifest, open(os.path.join(out, 'manifest.json'), 'w'), indent=1)
json.dump({'lowres': LOWRES, 'missing_racks': sorted(RKS.MISSING)}, open(os.path.join(out, 'flags.json'), 'w'), indent=1)
js = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shot.js')
NP = subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True).stdout.strip()
for i in range(0, len(jobs), 40):
    subprocess.run(['node', js] + [x for p in jobs[i:i+40] for x in p], check=True, env={**os.environ, 'NODE_PATH': NP}, stdout=subprocess.DEVNULL)
print(len(jobs), 'cards ->', out)
