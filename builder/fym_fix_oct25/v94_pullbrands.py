"""FYM v94: pull Mahjong Studios + Splash of Color out of Find Your Mat-ch for now (Tiffany Oct 26 9:23am; may come back,
revisit together). Exception (9:24am): Splash mats that are on her own album matches (sets' m lists) stay visible.
Hidden = hid:true on sets/mats/racks (data kept, reversible). Idempotent. Gate [67]. Usage: v94_pullbrands.py <build>"""
import sys, json
BR = {'Mahjong Studios', 'Splash of Color'}
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
keep = {x[0] for s in D['sets'] for x in s.get('m', [])}
n = {'sets': 0, 'mats': 0, 'racks': 0, 'kept_picks': 0}
for s in D['sets']:
    if s.get('maker') in BR and not s.get('hid'): s['hid'] = True; n['sets'] += 1
for k, m in D['mats'].items():
    if m.get('bn') in BR:
        if k in keep: n['kept_picks'] += 1; continue
        if not m.get('hid'): m['hid'] = True; n['mats'] += 1
for k, r in D['racks'].items():
    if r.get('bn') in BR and not r.get('hid'): r['hid'] = True; n['racks'] += 1
print('pulled', n)
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]; open(P, 'w').write(h)
