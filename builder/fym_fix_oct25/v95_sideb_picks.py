"""FYM v95: Bespoke double-sided mats - where Tiffany named the OTHER side as the match, add side B to the set's picks right
after side A (same racks). Tiffany Oct 26 11:41: The Chalet Mat's ski-lift side is "a really relevant match for the Apres Ski
Club". Config inline (add only on her word). Idempotent. Run after v95_bespoke2side.py. Usage: python3 v95_sideb_picks.py <build>"""
import sys, json
ADD = {'cmc-apres-ski': ['www.bespokemahjong.com/double-the-fun-chaletmat']}
P = sys.argv[1] + '/index.html'; h = open(P).read(); i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
n = 0
for s in D['sets']:
    for a in ADD.get(s['slug'], []):
        b = a + '#side-b'
        if b not in D['mats'] or any(x[0] == b for x in s['m']): continue
        j = next(k for k, x in enumerate(s['m']) if x[0] == a)
        s['m'].insert(j + 1, [b, list(s['m'][j][1])]); n += 1
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
open(P, 'w').write(h); print('side B picks added', n)
