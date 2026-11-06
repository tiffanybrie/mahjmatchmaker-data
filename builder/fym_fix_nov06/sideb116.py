"""FYM 1.16: Bespoke double-sided mats keep side B right after side A in every set's rank / cr (gate [78]) after the v116 re-run of
v92_coordinated.py (Juniper top 3) moved coordinated side-A mats to the front. Same logic as builder/fym_fix_nov05/misc115.py step 5.
Idempotent. Usage: python3 sideb116.py <build dir>"""
import sys, json
P = sys.argv[1] + '/index.html'; h = open(P).read(); i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:])
OI = {m: j for j, m in enumerate(D['order'])}; n = 0
pairs = [(OI[k.split('#')[0]], OI[k]) for k in D['mats'] if k.endswith('#side-b') and k.split('#')[0] in OI]
for s in D['sets']:
    for fld in ('rank', 'cr'):
        L = s.get(fld)
        if not L: continue
        for ja, jb in pairs:
            if ja in L and jb in L and L.index(jb) != L.index(ja) + 1: L.remove(jb); L.insert(L.index(ja) + 1, jb); n += 1
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[i + e:]; open(P, 'w').write(h); print('sideb116: moved', n)
