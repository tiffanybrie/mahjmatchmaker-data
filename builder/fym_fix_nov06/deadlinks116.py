"""FYM 1.16: dead shop links (config/fym-dead-links.json) get NO shop button and are NOT labelled Retired. u -> '' (old link kept in
u_dead), the auto-apply plain copy u_plain dropped too; rt is left exactly as it was. Locked mats (builder/fym_flags/locks.json) carry
no link fields, so locks are unaffected. Gate [162] curl-checks every visible shop link. Idempotent.
Usage: python3 builder/fym_fix_nov06/deadlinks116.py <build dir>"""
import sys, os, json
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
P = sys.argv[1] + '/index.html'; h = open(P).read(); i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:])
CFG = json.load(open(R + 'config/fym-dead-links.json'))['items']; n = 0; miss = []
# Nov 7 2026 (Ozark): never blank a link because its WHOLE DOMAIN failed (parked / wrong host): check the brand's real domain first
# (scripts/checks/domain_check.py, config/brand-domains.json). Such an entry is refused here (no shop button is NOT the fix).
sys.path.insert(0, R + 'scripts/checks'); import domain_check as DCK
bad = []
for k, x in CFG.items():
    o = D[x['g']].get(k) or {}; u = o.get('u') or o.get('u_dead') or ''
    v = DCK.verdict(u, o.get('bn')) if u.startswith('http') else None
    if v: bad.append(f"{x.get('name')}: {v}")
if bad:
    print('deadlinks116: REFUSED (whole-domain failure: re-point to the real domain, do not mark dead):'); [print('  ', b_) for b_ in bad]; sys.exit(1)
for k, x in CFG.items():
    o = D[x['g']].get(k)
    if not o: miss.append(k); continue
    if o.get('u'):
        o['u_dead'] = o['u']; o['u'] = ''; o.pop('u_plain', None); n += 1
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[i + e:]; open(P, 'w').write(h)
print('deadlinks116: blanked', n, 'of', len(CFG), '| not in build', miss)
