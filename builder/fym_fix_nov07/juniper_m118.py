"""FYM 1.18: Juniper (Oh My Mahjong) Tiffany's-match list from her FINAL album order (Nov 7 11:21pm 'done').
Source: config/picks/juniper-fym-m-2026-11-07.json (42 keys in her order; 5 holiday mats included, the app keeps them in holiday use).
Sets s.m for slug 'juniper' to exactly that list (existing rack picks for a key are kept, else []), writes the same list to
builder/fym_flags/locks.json sets.juniper.m so locks never undo it, and allows the one FYM-hidden pick (LBB Paint Feathers neoprene)
in builder/fym_flags/m_hidden_ok.json (gate [11]). Idempotent.
Usage: python3 builder/fym_fix_nov07/juniper_m118.py <build dir>   (run after picks118.py, before fym_apply_locks.py)"""
import sys, os, json
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'
h = open(P).read(); i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:]); e += i
C = json.load(open(R + 'config/picks/juniper-fym-m-2026-11-07.json'))
keys = [r['key'] for r in C['m']]
s = next((x for x in D['sets'] if x['slug'] == C['set']), None)
if s is None: sys.exit('juniper set not in build')
miss = [k for k in keys if k not in D['mats']]
if miss: sys.exit(f'keys not in build: {miss}')
old = {k: r for k, r in (s.get('m') or [])}
s['m'] = [[k, old.get(k, [])] for k in keys]
open(P, 'w').write(h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[e:])
L = json.load(open(R + 'builder/fym_flags/locks.json'))
L.setdefault('sets', {}).setdefault('juniper', {})['m'] = s['m']
json.dump(L, open(R + 'builder/fym_flags/locks.json', 'w'), indent=1, ensure_ascii=False)
H = json.load(open(R + 'builder/fym_flags/m_hidden_ok.json'))
for r in C['m']:
    if D['mats'][r['key']].get('hid') and not any(a['set'] == 'juniper' and a['key'] == r['key'] for a in H['allowed']):
        H['allowed'].append({'set': 'juniper', 'key': r['key'], 'mat': D['mats'][r['key']].get('n'), 'brand': D['mats'][r['key']].get('bn'),
                             'why': "Tiffany's final Juniper album order (Nov 7 11:21pm); hidden in FYM"})
json.dump(H, open(R + 'builder/fym_flags/m_hidden_ok.json', 'w'), indent=1, ensure_ascii=False)
print(f"juniper m = {len(s['m'])} (her order); locks + m_hidden_ok updated")
