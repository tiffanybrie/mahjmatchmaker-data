"""Album match cards in the live-album layout (card2.html).
Usage: python3 gen2.py spec.json outdir
spec: {mat_file, mat_crop, code?, max_racks?, mat_racks?:[labels], cards:[{slug,title,col,tile_file,racks:[labels...],bb:[B&B labels],file,code?}]}
Lower left (doc 48 sec. 4) = racks that match the TILES: card['racks'] = Tiffany's approved list
(config/tile-racks-picks.json final_lists), drawn in that order, up to max_racks (4), one copy each, each a
REAL photo (racks.py); B&B is the one generated rack. A rack with no real photo is skipped and reported.
Top right = racks that match the MAT: spec mat_racks (same on every card of a mat book). B&B picks are
colour bars under the B&B logo; any other brand's pick is its real photo under that brand's logo.
Without mat_racks, falls back to the old chart (card['bb'] B&B picks not drawn).
Oct 15 evening (Tiffany): tile set brand logo flag left of the tile photo = spec/card 'tile_brand' (default Oh My Mahjong);
no rack-brand logos on the MAT side (B&B bars and other racks are named in full instead)."""
import json, sys, os, io, base64, subprocess
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import racks as RK
R = '/home/claude/mahjmatchmaker-data/'
spec = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True); os.makedirs('/tmp/cards2', exist_ok=True)
def uri(im, fmt='JPEG', q=88, maxs=None):
    if isinstance(im, str): im = Image.open(im)
    if maxs: im = im.copy(); im.thumbnail((maxs, maxs))
    b = io.BytesIO()
    if fmt == 'PNG': im.save(b, 'PNG')
    else: im.convert('RGB').save(b, 'JPEG', quality=q)
    return f'data:image/{fmt.lower()};base64,' + base64.b64encode(b.getvalue()).decode()
def lum(h):
    h = h.lstrip('#'); r, g, b = [int(h[k:k+2], 16) for k in (0, 2, 4)]; return .299*r + .587*g + .114*b
tpl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'card2.html')).read()
logos = json.load(open(R + 'builder/logos/map.json'))
BBLOGO = uri(R + 'builder/logos/' + logos['Bird & Bamboo'], 'PNG'); NAVY = uri(R + 'assets/brand/card_navy_logo.png', 'PNG')
MAT = uri(Image.open(R + spec['mat_file']).convert('RGB').crop(tuple(spec['mat_crop'])), maxs=1400) if spec.get('mat_file') else None
BRANDS = {'Middle & Main': 'Middle & Main Mahjong'}  # rack-name prefix -> builder/logos/map.json key
def brand_of(label):
    for k in sorted(list(logos) + list(BRANDS), key=len, reverse=True):
        if label.startswith(k + ' '): return BRANDS.get(k, k), label[len(k) + 1:]
    return None, label
# Oct 18 (Tiffany): one set of mat racks per mat, on every card -> config/mat-racks-picks.json (spec 'mat_key')
MATREG = json.load(open(R + 'config/mat-racks-picks.json'))
_mk = spec.get('mat_key') if spec.get('mat_key') in MATREG else next((k for k, v in MATREG.items() if isinstance(v, dict) and spec.get('mat_file') in v.get('files', [])), None)
if _mk:
    _reg = MATREG[_mk]; spec['mat_key'] = _mk
    for _c in spec['cards']:
        _set = _c.get('set') or _c['slug'][:-(len(spec['mat_key']) + 1)]
        _c['mat_racks'] = list(_reg['racks'])
def chart_for(c):
    if 'mat_racks' not in spec and 'mat_racks' not in c: return None
    bars, other = [], []
    for l in c.get('mat_racks', spec.get('mat_racks', [])):
        if l.startswith('Bird & Bamboo '):
            n = l[len('Bird & Bamboo '):]; bars.append({'name': n, 'hex': RK.BBHEX[n], 'light': lum(RK.BBHEX[n]) > 185}); continue
        im = RK.photo(l)
        if im is None: RK.MISSING.add(l); continue
        b, n = brand_of(l)
        other.append({'img': uri(im, 'PNG', maxs=700), 'name': n, 'full': l})
    return bars, other
TLOGO = {}
_IDX = json.load(open(R + 'assets/tiles/album/index.json'))
LOOSE_FILES = {v['file'] for v in _IDX.values() if isinstance(v, dict) and v.get('tile_mode') == 'loose'}  # Oct 17
def tlogo(b):
    if b not in TLOGO:
        f = RK.tile_logo(b); TLOGO[b] = uri(f, 'PNG', maxs=500) if f else None
    return TLOGO[b]
jobs = []; missing = {}; over = {}
for c in spec['cards']:
    drawn = []
    labels = list(c['racks']) if 'mat_racks' in spec or 'mat_racks' in c else [l for l in c['racks'] if not l.startswith('Bird & Bamboo')] + [l for l in c['racks'] if l.startswith('Bird & Bamboo')] + c.get('bb', [])
    seen = set()
    for l in labels:
        if l in seen: continue
        if len(drawn) >= min(4, spec.get('max_racks', 4)): over.setdefault(c['slug'], []).append(l); continue
        seen.add(l); r = RK.by_label(l)
        if r:
            fr = 1.0 if l.startswith('Bird & Bamboo ') else RK.frac(l)  # size by the RACK; an OMM photo's pusher overhangs above it
            drawn.append({'img': uri(r[0], 'PNG', maxs=1400), 'label': r[1], 'frac': fr, 'ar': r[0].width / r[0].height})  # card2: same angle + same length for every rack (Oct 15)
        else: missing.setdefault(c['slug'], []).append(l)
    dl = {d['label'] for d in drawn}
    ch = chart_for(c); other = []
    if ch is not None: chart, other = ch
    else:
        chart = []
        for l in c.get('bb', []) + [x for x in c['racks'] if x.startswith('Bird & Bamboo')]:
            n = l[len('Bird & Bamboo '):]
            if l in dl or n in [x['name'] for x in chart] or n not in RK.BBHEX: continue
            chart.append({'name': n, 'hex': RK.BBHEX[n], 'light': lum(RK.BBHEX[n]) > 185})
    data = {'title': c['title'], 'col': c['col'], 'mat': c.get('mat') or MAT, 'tile': (uri(R + c['tile_file'], 'PNG', maxs=900) if (c.get('tile_mode') == 'loose' or c['tile_file'] in LOOSE_FILES) else uri(R + c['tile_file'], maxs=900)) if not c['tile_file'].startswith('data:') else c['tile_file'], 'loose': c.get('tile_mode') == 'loose' or c['tile_file'] in LOOSE_FILES,
            'racks': drawn, 'bb': chart[:3], 'mr': other[:2], 'bblogo': BBLOGO, 'navy': NAVY,
            'code': c.get('code', spec.get('code', '10% OFF  USE CODE : MAHJMATCH')), 'hol': c.get('hol', False), 'flame': c.get('flame'),
            'tlogo': tlogo(c.get('tile_brand', spec.get('tile_brand', 'Oh My Mahjong')))}
    hf = f"/tmp/cards2/{c['slug']}.html"; open(hf, 'w').write(tpl.replace('__DATA__', json.dumps(data)))
    jobs.append((hf, os.path.join(out, c['file'])))
NP = subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True).stdout.strip()
js = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shot.js')
for i in range(0, len(jobs), 40):
    subprocess.run(['node', js] + [x for p in jobs[i:i+40] for x in p], check=True, env={**os.environ, 'NODE_PATH': NP}, stdout=subprocess.DEVNULL)
print(len(jobs), 'cards ->', out)
if missing: print('NO REAL PHOTO (left off the card):', json.dumps(missing, ensure_ascii=False))
if over: print('OVER THE 4-RACK CAPACITY (left off the card):', json.dumps(over, ensure_ascii=False))
json.dump({'no_real_photo': missing, 'over_capacity': over} if over else missing, open(os.path.join(out, '_missing_racks.json'), 'w'), indent=1, ensure_ascii=False)
