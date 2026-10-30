"""FYM v105 (Oct 30, QA): double-sided mats, side B gets its OWN mat-door tile order.
Gate [78] keeps side B right after side A in every s.rank (tiles door: both sides together), but the mat door sorted sets by
s.rank position, so side B always showed side A's tile order (QA: Gray Malin Getaway Dogs Pool vs Ski Lift shared 7 of 8).
Fix: for each visible side-B mat, rank the sets by B's own depth in the full colour scoring (same scorers v104rank.py uses:
v95_matrank non-holiday, v85_colorrank holiday) and store it as M[B].so = [set index, ...] (best first); setsForMat uses it.
Usage: python3 v105so.py <build_dir>"""
import sys, os, json
H = os.path.dirname(os.path.abspath(__file__))
src = open(H + '/v104rank.py').read()
src = src[:src.index('def place(')]
g = {'__file__': H + '/v104rank.py', '__name__': 'v105so'}
exec(compile(src, H + '/v104rank.py', 'exec'), g)
P = g['P']; h, i, end, D = g['load'](P); FULL = g['FULL']
M, O, S = D['mats'], D['order'], D['sets']; OI = {k: j for j, k in enumerate(O)}
n = 0
for k, m in M.items():
    if m.get('side') != 'B' or m.get('hid') or k not in OI: continue
    jb = OI[k]; rows = []
    for si, s in enumerate(S):
        full = FULL.get(s['slug']) or []
        if jb in full: rows.append((full.index(jb) / max(1, len(full)), si))
    m['so'] = [si for _, si in sorted(rows)]; n += 1
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
open(P, 'w').write(h)
print('v105so: side-B mats with own order', n)
