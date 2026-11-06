"""FYM 1.16: dead shop links (config/fym-dead-links.json) get NO shop button and are NOT labelled Retired. u -> '' (old link kept in
u_dead), the auto-apply plain copy u_plain dropped too; rt is left exactly as it was. Locked mats (builder/fym_flags/locks.json) carry
no link fields, so locks are unaffected. Gate [162] curl-checks every visible shop link. Idempotent.
Usage: python3 builder/fym_fix_nov06/deadlinks116.py <build dir>"""
import sys, os, json
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
P = sys.argv[1] + '/index.html'; h = open(P).read(); i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:])
CFG = json.load(open(R + 'config/fym-dead-links.json'))['items']; n = 0; miss = []
for k, x in CFG.items():
    o = D[x['g']].get(k)
    if not o: miss.append(k); continue
    if o.get('u'):
        o['u_dead'] = o['u']; o['u'] = ''; o.pop('u_plain', None); n += 1
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[i + e:]; open(P, 'w').write(h)
print('deadlinks116: blanked', n, 'of', len(CFG), '| not in build', miss)
