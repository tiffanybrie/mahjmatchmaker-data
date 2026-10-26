"""Update locks.json for tile photos Tiffany approved on Oct 26 (CMC 8:43am faces|straight-up backs; Virora grid3 9:00am).
Only locked tiles listed in those configs; writes build's full/pile into locks + a _changes line. Usage: v94_lockupdate.py <build>"""
import sys, os, json
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
h = open(sys.argv[1] + '/index.html').read(); i = h.index('const D=') + 8; D, _ = json.JSONDecoder().raw_decode(h[i:])
LP = R + 'builder/fym_flags/locks.json'; L = json.load(open(LP)); n = 0
keys = list(json.load(open(R + 'config/fym-cmc-splits-oct26.json'))['splits']) + list(json.load(open(R + 'config/fym-virora-backs-oct26.json'))['splits'])
for k in keys:
    if k in L['tiles'] and k in D['tiles']:
        for f in ('full', 'pile'):
            if f in L['tiles'][k] and L['tiles'][k][f] != D['tiles'][k].get(f): L['tiles'][k][f] = D['tiles'][k][f]; n += 1
if n: L['_changes'].append('2026-10-26: tile photos for CMC (Tiffany 8:43am yes) + Virora grid3 (9:00am yes) -> new full/pile')
json.dump(L, open(LP, 'w'), indent=1, ensure_ascii=False); print('locks updated', n)
