"""FYM 1.18: refresh the Table view data D.tv inside an EXISTING release build (preview_nov01.py --release only works on a build
that has no Table view yet). Re-runs preview_nov01.py's data part on this build and replaces:
  backs  (walls, config/tableview-back-colors.json: pass --backs <file> to use a committed snapshot, e.g. `git show <rev>:...`)
  pm / pt / price / pr  (prices from config/fym-stock.json + code % from config/fym-code-pct.json, incl. revived items)
Everything else in D.tv (classes, rack types, cut-outs, fills; later patched by racks116.py etc.) is kept as is; new keys that
preview computes for items the old D.tv lacks (e.g. a class for a newly classified mat) are added, never overwritten.
Prints walls X of N visible sets + price coverage. Idempotent.
Usage: python3 builder/fym_fix_nov07/tv118.py <build dir> [--backs <json>]"""
import sys, os, json, pathlib, tempfile
R = pathlib.Path(__file__).resolve().parents[2]
B = sys.argv[1]; P = os.path.join(B, 'index.html')
BK = sys.argv[sys.argv.index('--backs') + 1] if '--backs' in sys.argv else str(R / 'config/tableview-back-colors.json')
src = (R / 'builder/table_view/preview_nov01.py').read_text()
cut = src.index('TVD = dict(')
cut = src.index('\n', cut) + 1
code = src[:cut].replace("json.load(open(R / 'config/tableview-back-colors.json'))", 'json.load(open(_BACKS))')
assert 'json.load(open(_BACKS))' in code
g = {'__name__': 'tv118', '__file__': str(R / 'builder/table_view/preview_nov01.py'), '_BACKS': BK}
old_argv = sys.argv; sys.argv = ['preview_nov01.py', P, tempfile.mkdtemp()]
exec(compile(code, 'preview_nov01.py[data]', 'exec'), g)
sys.argv = old_argv
NEW = g['TVD']
h = open(P).read(); i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:])
TV = D['tv']; rep = {}
for k in ('backs', 'pm', 'pt', 'price', 'pr'):
    a, b = TV.get(k), NEW[k]
    rep[k] = (len(a) if hasattr(a, '__len__') else a, len(b) if hasattr(b, '__len__') else b)
    TV[k] = b
added = {}
for k, v in NEW.items():
    if k in ('backs', 'pm', 'pt', 'price', 'pr'): continue
    if isinstance(v, dict) and isinstance(TV.get(k), dict):
        n = [x for x in v if x not in TV[k]]
        for x in n: TV[k][x] = v[x]
        if n: added[k] = len(n)
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[i + e:]; open(P, 'w').write(h)
vis = [s for s in D['sets'] if not s.get('hid') and not D['tiles'].get(s['tile'], {}).get('hid')]
vm = [k for k, m in D['mats'].items() if not m.get('hid')]; vr = [k for k, r in D['racks'].items() if not r.get('hid')]
print('tv118: replaced', rep, '| added', added)
print(f"tv118: walls {sum(1 for s in vis if s['slug'] in TV['backs'])} of {len(vis)} visible sets (file {sum(1 for k in json.load(open(BK)) if not k.startswith('_'))} backs, "
      f"{len(TV['backs'])} in D.tv.backs); prices mats {sum(1 for k in vm if k in TV['pm'])}/{len(vm)}, tiles {sum(1 for s in vis if s['tile'] in TV['pt'])}/{len(vis)}, racks {sum(1 for k in vr if k in TV['price'])}/{len(vr)}")
