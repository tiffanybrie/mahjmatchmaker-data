"""Album match cards in the live-album layout (card2.html).
Usage: python3 gen2.py spec.json outdir
spec: {mat_file, mat_crop, code?, cards:[{slug,title,col,tile_file,racks:[labels...],bb:[B&B labels],file,code?}]}
Racks drawn: up to 3, one copy each — drawable non-B&B racks first, then B&B racks in order.
B&B chart (top right) = the card's other B&B picks that aren't drawn."""
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
jobs = []
for c in spec['cards']:
    drawn = []
    labels = [l for l in c['racks'] if not l.startswith('Bird & Bamboo')] + [l for l in c['racks'] if l.startswith('Bird & Bamboo')] + c.get('bb', [])
    seen = set()
    for l in labels:
        if l in seen or len(drawn) >= spec.get('max_racks', 3): continue
        seen.add(l); r = RK.by_label(l)
        if r: drawn.append({'img': uri(r[0], 'PNG'), 'label': r[1]})
    dl = {d['label'] for d in drawn}
    chart = []
    for l in c.get('bb', []) + [x for x in c['racks'] if x.startswith('Bird & Bamboo')]:
        n = l[len('Bird & Bamboo '):]
        if l in dl or n in [x['name'] for x in chart] or n not in RK.BBHEX: continue
        chart.append({'name': n, 'hex': RK.BBHEX[n], 'light': lum(RK.BBHEX[n]) > 185})
    data = {'title': c['title'], 'col': c['col'], 'mat': c.get('mat') or MAT, 'tile': uri(R + c['tile_file'], maxs=900) if not c['tile_file'].startswith('data:') else c['tile_file'],
            'racks': drawn, 'bb': chart[:3], 'bblogo': BBLOGO, 'navy': NAVY,
            'code': c.get('code', spec.get('code', '10% OFF  USE CODE : MAHJMATCH')), 'hol': c.get('hol', False), 'flame': c.get('flame')}
    hf = f"/tmp/cards2/{c['slug']}.html"; open(hf, 'w').write(tpl.replace('__DATA__', json.dumps(data)))
    jobs.append((hf, os.path.join(out, c['file'])))
NP = subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True).stdout.strip()
js = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shot.js')
for i in range(0, len(jobs), 40):
    subprocess.run(['node', js] + [x for p in jobs[i:i+40] for x in p], check=True, env={**os.environ, 'NODE_PATH': NP}, stdout=subprocess.DEVNULL)
print(len(jobs), 'cards ->', out)
