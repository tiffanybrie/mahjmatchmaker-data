"""Turn by-eye picks into config/tableview-mats-nov07.json entries (Nov 7). picks.json: {key: pick}
  pick = 'A'            the FYM photo as is (full-bleed mat; centre square)                         -> cls A
  pick = 'fa'           the FYM photo cropped/straightened to the mat quad found by analyze()        -> cls A + fa
  pick = <int j >= 1>   vendor image j from <cands dir>/cands.json, re-downloaded at 2000px,
                        perspective-straightened to a 1200px all-mat square -> assets/table-view/mats/ -> cls A + mo
  pick = 'B'            corner view (cv from builder/table_view/corner_nov02.py output given with --cv)
  pick = 'C:<reason>'   grayed with that reason
Usage: python3 apply_picks_nov07.py <build dir> <cands dir> <picks.json> [--cv corner_out.json]"""
import sys, os, json, io, re, urllib.request, hashlib, pathlib
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
from matimg import load_D, mat_full
from matfit_nov07 import analyze, warp_square, affine
R = pathlib.Path(__file__).resolve().parents[2]
B, CD, PJ = sys.argv[1:4]; CVJ = sys.argv[sys.argv.index('--cv') + 1] if '--cv' in sys.argv else None
D = load_D(B); M = D['mats']; picks = json.load(open(PJ))
cands = {r['k']: r for r in json.load(open(os.path.join(CD, 'cands.json')))} if os.path.exists(os.path.join(CD, 'cands.json')) else {}
CVD = json.load(open(CVJ)) if CVJ else {}
CP = R / 'config/tableview-mats-nov07.json'; C = json.load(open(CP))
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/130 Safari/537.36'}
slug = lambda k: re.sub(r'[^a-z0-9]+', '-', (M[k]['bn'] + '-' + M[k]['n']).lower()).strip('-')[:60] + '-' + hashlib.md5(k.encode()).hexdigest()[:6]
def clear(k):
    for sec in ('fa', 'mo', 'cv', 'why'): C[sec].pop(k, None)
n = {}
for k, p in picks.items():
    if k not in M: print('not in build:', k); continue
    clear(k)
    if p == 'A': C['cls'][k] = 'A'; C['src'][k] = 'FYM photo (full-bleed, looked at)'
    elif p == 'fa':
        im = mat_full(B, M[k]['f']); a = analyze(im)
        assert a.get('kind') == 'studio', (k, a.get('kind'))
        C['cls'][k] = 'A'; C['fa'][k] = affine(a['quad'], a['W'], a['H']); C['src'][k] = 'FYM photo cropped/straightened to the mat (affine)'
    elif isinstance(p, int):
        src = cands[k]['c'][p]['src']; url = src + ('&' if '?' in src else '?') + 'width=2000'
        im = Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read())).convert('RGB')
        a = analyze(im); assert a.get('quad'), k
        f = f'assets/table-view/mats/{slug(k)}.webp'; warp_square(im, a['quad'], 1200).save(R / f, 'WEBP', quality=88)
        C['cls'][k] = 'A'; C['mo'][k] = f; C['src'][k] = f'vendor product image {p}: {src.split("?")[0]} (straightened to the mat)'
    elif p == 'B':
        C['cls'][k] = 'B'; C['cv'][k] = {'m': CVD[k]['m'], 'f': CVD[k]['f']}; C['src'][k] = 'FYM photo, corner view (corner_nov02 fit)'
    elif isinstance(p, str) and p.startswith('C:'):
        C['cls'][k] = 'C'; C['why'][k] = p[2:]; C['src'][k] = 'no usable top-down vendor photo (product page checked)'
    else: raise SystemExit(f'bad pick {k}: {p}')
    n[str(p)[:2]] = n.get(str(p)[:2], 0) + 1
json.dump(C, open(CP, 'w'), indent=1, ensure_ascii=False)
print('applied', n, '| config cls', len(C['cls']), 'mo', len(C['mo']), 'fa', len(C['fa']))
