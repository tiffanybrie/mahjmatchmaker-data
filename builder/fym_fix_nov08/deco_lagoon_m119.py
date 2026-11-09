"""FYM 1.19: Deco (Lagoon) (Bam Bird Boutique, slug 'bam-bird-boutique-deco') Tiffany's-match list from her FINAL album order
(review round 1 saved Nov 8 6:19pm + her 6:20-6:25pm bring-ins at colour rank). Source: config/picks/deco-lagoon-fym-m-2026-11-08.json
(41 keys in her order; 3 holiday mats included). Five keys are NEW in 1.19 (pending_keys): Silk Mahjong Crane Cloud, Lemondrop Sapphire
Blooms + Floral Affair, Splash Lady Luck's Teal Lounge (config/fym-catalog-adds-nov08-lagoon.json) and Dreamframer gold fans
(config/fym-shopmy-catalog-refresh-nov08.json): apply those catalog adds FIRST, this script refuses while any key is missing.
Same pattern as builder/fym_fix_nov07/juniper_m118.py (locks + m_hidden_ok). Idempotent.
Usage: python3 builder/fym_fix_nov08/deco_lagoon_m119.py <build dir>   (after the catalog adds + picks, before fym_apply_locks.py)"""
import sys, os, json
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'
h = open(P).read(); i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:]); e += i
C = json.load(open(R + 'config/picks/deco-lagoon-fym-m-2026-11-08.json'))
SET = C['set']; keys = [r['key'] for r in C['m']]
s = next((x for x in D['sets'] if x['slug'] == SET), None)
if s is None: sys.exit(f'{SET} set not in build')
miss = [k for k in keys if k not in D['mats']]
if miss: sys.exit(f'keys not in build (apply the 1.19 catalog adds first): {miss}')
old = {k: r for k, r in (s.get('m') or [])}
s['m'] = [[k, old.get(k, [])] for k in keys]
s['album'] = C['album']
open(P, 'w').write(h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[e:])
L = json.load(open(R + 'builder/fym_flags/locks.json'))
L.setdefault('sets', {}).setdefault(SET, {})['m'] = s['m']
json.dump(L, open(R + 'builder/fym_flags/locks.json', 'w'), indent=1, ensure_ascii=False)
H = json.load(open(R + 'builder/fym_flags/m_hidden_ok.json'))
for r in C['m']:
    if D['mats'][r['key']].get('hid') and not any(a['set'] == SET and a['key'] == r['key'] for a in H['allowed']):
        H['allowed'].append({'set': SET, 'key': r['key'], 'mat': D['mats'][r['key']].get('n'), 'brand': D['mats'][r['key']].get('bn'),
                             'why': "Tiffany's final Deco (Lagoon) album order (Nov 8); hidden in FYM"})
json.dump(H, open(R + 'builder/fym_flags/m_hidden_ok.json', 'w'), indent=1, ensure_ascii=False)
print(f"{SET} m = {len(s['m'])} (her order), album link set; locks + m_hidden_ok updated")
