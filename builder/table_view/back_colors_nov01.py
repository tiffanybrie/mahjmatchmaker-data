"""Table view tile BACK colors (Nov 1, Tiffany 3:38pm: Brownstone Bloom walls came out burgundy because the sample used the
match-card TITLE color s.tc; backs must come from a real back). Writes config/tableview-back-colors.json
{set_slug: {back:'#hex', type:'solid|pattern|ivory', src:'back photo measured|album|brand page|Tiffany', patch?: path}}
and pattern texture patches assets/table-view/backs/<slug>.webp. Inputs: builder/table_view/back_boxes_nov01.json
(box inside ONE visible back, picked by eye on gridded contact sheets) + each set's FYM tile photo from the v112 build.
NOTE: config/tile-back-colors.json is a DIFFERENT, older file (color groups -> set names, read by scripts/color/measure.py);
it is not touched. Usage: python3 back_colors_nov01.py <b112 build dir>"""
import sys, json, io, struct, glob, os, pathlib, numpy as np
from PIL import Image
from scipy.cluster.vq import kmeans2
R = pathlib.Path(__file__).resolve().parents[2]; B = sys.argv[1]
h = open(B + '/index.html').read(); i = h.index('const D=') + 8; D, _ = json.JSONDecoder().raw_decode(h[i:])
MC = {}
for f in glob.glob(B + '/mc/*.webp'):
    ab = open(f, 'rb').read(); n = struct.unpack('<I', ab[-4:])[0]
    try: hh = json.loads(ab[-4 - n:-4])
    except Exception: continue
    for k, (a, l) in hh.items(): MC[k] = (f, a, l)
def photo(slug):
    s = next(x for x in D['sets'] if x['slug'] == slug); t = D['tiles'][s['tile']]; p = t['full']
    if p in MC: f, a, l = MC[p]; return Image.open(io.BytesIO(open(f, 'rb').read()[a:a + l])).convert('RGB')
    return Image.open(B + '/' + p).convert('RGB')
hexs = lambda c: '#%02x%02x%02x' % tuple(int(x) for x in c)
def dominant(im, bright=False):
    im = im.copy(); im.thumbnail((240, 240)); a = np.asarray(im).astype(float) / 255
    mx = a.max(2); mn = a.min(2); s = (mx - mn) / (mx + 1e-6); p = a[(s > (.35 if bright else .2)) & (mx < (.9 if bright else .97)) & (mx > .15)]
    cen, lab = kmeans2(p, 5, minit='++', seed=2); q = p[lab == np.bincount(lab).argmax()]
    if bright: v = q.max(1); q = q[v >= np.percentile(v, 60)]
    return np.median(q, 0) * 255
BOX = json.load(open(R / 'builder/table_view/back_boxes_nov01.json'))
OUT = {'_about': 'Table view wall colors. Walls may ONLY use these (never the match-card title color). Built by builder/table_view/back_colors_nov01.py; checked by scripts/tableview_back_check.py. Sets not listed = back color not confirmed -> walls grayed.'}
os.makedirs(R / 'assets/table-view/backs', exist_ok=True)
for slug, v in BOX.items():
    if slug.startswith('_'): continue
    x0, y0, x1, y1, kind = v; im = photo(slug); w, hh_ = im.size
    crop = im.crop((int(x0 * w), int(y0 * hh_), int(x1 * w), int(y1 * hh_)))
    if kind == 'solid-auto':
        OUT[slug] = dict(back=hexs(dominant(im, bright=slug == 'sunday-mahjong-nature-walk')), type='solid', src='back photo measured (dominant back color in the FYM tile photo, checked by eye)')
    elif kind == 'solid':
        OUT[slug] = dict(back=hexs(np.median(np.asarray(crop).reshape(-1, 3), 0)), type='solid', src='back photo measured (box inside one back, FYM tile photo)')
    elif kind == 'ivory':
        OUT[slug] = dict(back=hexs(np.median(np.asarray(crop).reshape(-1, 3), 0)), type='ivory', src='Tiffany (Nov 1: ivory backs matching the face background; color measured from the faces)')
    else:
        pp = R / f'assets/table-view/backs/{slug}.webp'; c2 = crop.copy(); c2.thumbnail((160, 160)); c2.save(pp, 'WEBP', quality=82)
        OUT[slug] = dict(back=hexs(np.median(np.asarray(crop).reshape(-1, 3), 0)), type='pattern', src='back photo measured (pattern patch cut from one back, FYM tile photo)', patch=str(pp.relative_to(R)))
bp = Image.open(R / 'assets/table-view/src/omm-papaya-back-photo.png').convert('RGBA'); a = np.asarray(bp).astype(float)
OUT['oh-my-mahjong-papaya-spritz'] = dict(back=hexs(np.median(a[..., :3][a[..., 3] > 200], 0)), type='solid', src='back photo measured (assets/table-view/src/omm-papaya-back-photo.png)', sprite='assets/table-view/src/omm-papaya-back-photo.png')
OUT['dear-santa'] = dict(back='#efe9dc', type='ivory', src='Tiffany (config/tile-back-colors-proposed.json: "her call: ivory back")')
try:  # Nov 7: keep the sets added by back_colors_nov07.py (a rerun of this script must not wipe their walls)
    for _k, _v in json.load(open(R / 'config/tableview-back-colors.json')).items():
        if _k not in OUT and 'nov07' in (_v.get('src') or ''): OUT[_k] = _v
except Exception: pass
json.dump(OUT, open(R / 'config/tableview-back-colors.json', 'w'), indent=1, ensure_ascii=False)
print(len(OUT) - 1, 'sets'); [print(k, v['type'], v['back']) for k, v in OUT.items() if not k.startswith('_')]
