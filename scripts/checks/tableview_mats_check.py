"""Table view mats check (Tiffany Nov 7 10:22pm: OMM's new Lotus Cove wasn't in Table view; 334 mats added since Nov 1 had never
been classified). FAILS when a visible mat has no Table view class (D.tv.cls), when a D.tv.mo vendor photo / fa crop / pf fill
belongs to a mat that is not full-table class, or when config/tableview-mats-nov07.json names a mat the build doesn't carry as
classed the same. Prints usable X of N. Run on every FYM build after tableview_v118.py (or its successor).
Usage: python3 scripts/checks/tableview_mats_check.py <build dir | index.html>"""
import sys, os, json, pathlib
R = pathlib.Path(__file__).resolve().parents[2]
A = sys.argv[1]; P = A if A.endswith('.html') else os.path.join(A, 'index.html')
h = open(P).read(); i = h.index('const D=') + 8; D, _ = json.JSONDecoder().raw_decode(h[i:])
M = D['mats']; TV = D['tv']; cls = TV.get('cls', {}); C = json.load(open(R / 'config/tableview-mats-nov07.json'))
vis = [k for k, m in M.items() if not m.get('hid')]
F = [f"[tv-mats] no Table view class: {M[k]['bn']} | {M[k]['n']} (classify it: builder/table_view/vendor_cands_nov07.py + apply_picks_nov07.py)" for k in vis if k not in cls]
for sec in ('mo', 'fa', 'pf'):
    F += [f"[tv-mats] {sec} on a mat that is not class A: {k}" for k in TV.get(sec, {}) if cls.get(k) != 'A' and k in M and not (sec == 'pf' and cls.get(k) == 'B')]
F += [f"[tv-mats] config says {v}, build has {cls.get(k)}: {k}" for k, v in C['cls'].items() if k in M and cls.get(k) != v]
if 'TVD.mo&&TVD.mo[mat]' not in h: F.append('[tv-mats] render() not patched for vendor photos (run builder/fym_fix_nov07/tableview_v118.py)')
u = sum(1 for k in vis if cls.get(k) in ('A', 'B'))
print(f"Table view mats usable {u} of {len(vis)} visible; unclassified {sum(1 for k in vis if k not in cls)}; grayed {sum(1 for k in vis if cls.get(k) == 'C')}")
for f in F[:40]: print(f)
print('PASS' if not F else f'FAIL ({len(F)})'); sys.exit(1 if F else 0)
