"""FYM v94 rack photo quality (Tiffany Oct 26 8:29am: "for whites, clears, anything that's basically a neutral, we want to lead
with our best image... where all things are equal, there's no reason to suggest a rack that isn't photographed well").
Example: Mahjong Studios American + Sophie Klima Whimsical Chinoiserie led with Bam! Let's Mahjong white wooden racks
(vertical, gray background) instead of a single horizontal rack on white (Bird & Bamboo, My Fair Mahjong Bright White Wood).
config/rack-photo-quality.json = {rack key: {score 1-5, why}}; 5 = single horizontal rack on white/solid, 1 = lifestyle/busy.
Scored by heuristics on the deck (sm) photo, corrected by eye on contact sheets; card (HD) photo blended in 60/40 where it differs.
Patch: R[r].pq = score. Small tie-breaker only, her picks and universal racks exempt (never reordered, never penalised):
  - default suggestions (colour distance sort): + (5-pq)*2.5 Lab units (a 5 beats a 2 when colours are within ~7.5 dE)
  - colour chip sort (rs share): + .07*(pq-3) (a 5 beats a 2 only within .21 of the same share; off-colour racks are filtered out first)
Gate [60] (builder/fym_rackquality_check.js). Usage: python3 v94_rackquality.py <build_dir>"""
import sys, os, json
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
K_LAB, K_RS = 2.5, .07
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
Q = json.load(open(REPO + 'config/rack-photo-quality.json'))
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
n = 0
for k, r in D['racks'].items():
    r['pq'] = Q[k]['score'] if k in Q else 3; n += k in Q
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
if 'const pqk=' not in h:
    a = "const pen=r=>(R[r].pa?0:1e5)+(R[r].lo?1e4:0);"; assert h.count(a) == 1
    h = h.replace(a, a + f"/* v94 photo quality tie-breaker (Tiffany Oct 26 8:29am) */const pqk=r=>hr.includes(r)||U.includes(r)?0:(5-(R[r].pq||3))*{K_LAB};", 1)
    a = ".map(r=>[sc(r)+pen(r),r])"; assert h.count(a) == 2; h = h.replace(a, ".map(r=>[sc(r)+pen(r)+pqk(r),r])")
    a = "const rk=r=>-((R[r].rs||{})[c]||0);"; assert h.count(a) == 1
    h = h.replace(a, f"const rk=r=>-(((R[r].rs||{{}})[c]||0)+(hr.includes(r)?0:{K_RS}*((R[r].pq||3)-3)));", 1)
open(P, 'w').write(h)
print(f"rack photo quality: {n} racks scored from config, {len(D['racks'])-n} default 3")
