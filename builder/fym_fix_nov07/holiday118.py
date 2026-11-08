"""FYM 1.18 (gate [74], Tiffany Oct 26 11:16am: partner brands keep preferential order over ShopMy Amazon mats): after
builder/fym_fix_oct30/v104rank.py colour-ranks the 28 Amazon holiday picks, some landed in a Holiday tile set's first 6 non-pick places.
On every Holiday set (BACKG Holiday) where a partner holiday mat sits in the visible top 30 of s.cr, each Amazon mat found among the first
6 non-pick visible mats moves to right after the 6th non-pick, non-Amazon visible mat (their own order kept). Nothing else moves.
Idempotent. Usage: python3 builder/fym_fix_nov07/holiday118.py <build dir>"""
import sys, json, re
P = sys.argv[1] + '/index.html'; h = open(P).read(); i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:]); e += i
HOL = set(json.loads(re.search(r'BACKG=(\{.*?\});', h).group(1)).get('Holiday', []))
O, M = D['order'], D['mats']; moved = {}
for s in D['sets']:
    if s.get('hid') or s['name'] not in HOL or 'cr' not in s: continue
    pk = {x[0] if isinstance(x, list) else x for x in (s.get('m') or [])}
    vis = [j for j in s['cr'] if not M[O[j]].get('hid')]
    if not any(M[O[j]].get('pa') and M[O[j]].get('hol') for j in vis[:30]): continue
    seen, cut, out = 0, None, []
    for p, j in enumerate(s['cr']):
        k = O[j]
        if M[k].get('hid') or k in pk: continue
        if M[k].get('b') == 'Amazon': out.append(j); continue
        seen += 1
        if seen == 6: cut = j; break
    first6_amz = [j for j in out]
    if not first6_amz or cut is None: continue
    rest = [j for j in s['cr'] if j not in first6_amz]
    at = rest.index(cut) + 1
    s['cr'] = rest[:at] + first6_amz + rest[at:]
    moved[s['name']] = [M[O[j]]['n'] for j in first6_amz]
open(P, 'w').write(h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[e:])
print('holiday118: Amazon mats moved below the first 6 on', len(moved), 'holiday sets')
