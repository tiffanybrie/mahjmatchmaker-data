"""FYM v94 rack photo quality (Tiffany Oct 26 8:29am: "for whites, clears, anything that's basically a neutral, we want to lead
with our best image... where all things are equal, there's no reason to suggest a rack that isn't photographed well").
Example: Mahjong Studios American + Sophie Klima Whimsical Chinoiserie led with Bam! Let's Mahjong white wooden racks
(vertical, gray background) instead of a single horizontal rack on white (Bird & Bamboo, My Fair Mahjong Bright White Wood).
config/rack-photo-quality.json = {rack key: {score 1-5, why}}; 5 = single horizontal rack on white/solid, 1 = lifestyle/busy.
Scored by heuristics on the deck (sm) photo, corrected by eye on contact sheets; card (HD) photo blended in 60/40 where it differs.
Patch: R[r].pq = score. Small tie-breaker only, her picks and universal racks exempt (never reordered, never penalised):
  - default suggestions (colour distance sort): + (5-pq)*2.5 Lab units (a 5 beats a 2 when colours are within ~7.5 dE)
  - colour chip sort (rs share): + .07*(pq-3) (a 5 beats a 2 only within .21 of the same share; off-colour racks are filtered out first)
Round 2 (Tiffany Oct 26 8:50am, standing rules; her test Corey Paige Pearl Crush + Bespoke Year of the Dragon Amped-Up Grey
led with a Mahjong Studios white rack):
  - Mahjong Studios racks never lead unless the tile set or mat is Mahjong Studios: below every other rack (default + every chip).
  - White: a well-photographed (4+) white WOOD rack leads (R.ww); pearlescent tiles (set name says pearl) lead with a white PEARL rack (R.wp, photo 3+).
    default suggestions: -6 dE (white wood) / -18 dE (pearl white on pearl tiles); White chip: +.25 / +.8 share.
  - Rule 4 (8:58am, Mahjong Row & Co. Lyla + an MRC mat got Mahjong Studios racks): when the tile set or mat is brand X, X's
    colour-matching racks (rackFits and within 30 dE of the mat) come early: the best 2 sit right after any leading picks (and after a leading white pearl rack on pearl tiles)
    (default suggestions), and get +.3 share in colour chips.
  - Otherwise the photo-quality tie-breaker above. Her picks and universal racks are exempt from all of it.
Gate [60] (builder/fym_rackquality_check.js). Usage: python3 v94_rackquality.py <build_dir>"""
import sys, os, json
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
K_LAB, K_RS = 2.5, .07
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
Q = json.load(open(REPO + 'config/rack-photo-quality.json'))
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
def _lab(hx):
    c = [int(hx[j:j + 2], 16) / 255 for j in (1, 3, 5)]; c = [((v + .055) / 1.055) ** 2.4 if v > .04045 else v / 12.92 for v in c]
    x, y, z = c[0] * .4124 + c[1] * .3576 + c[2] * .1805, c[0] * .2126 + c[1] * .7152 + c[2] * .0722, c[0] * .0193 + c[1] * .1192 + c[2] * .9505
    f = lambda v: v ** (1 / 3) if v > .008856 else 7.787 * v + 16 / 116
    x, y, z = f(x / .95047), f(y), f(z / 1.08883); return 116 * y - 16, 500 * (x - y), 200 * (y - z)
def _white(r):
    if 'neutral' not in (r.get('rf') or []): return False
    nm = r['n'].lower()
    if any(w in nm for w in ('white', 'cream', 'ivory')): return True
    if any(w in nm for w in ('blue', 'pink', 'green', 'gray', 'grey', 'silver', 'champagne', 'almond', 'pebble', 'black', 'gold')) or not r.get('hx'): return False
    L, a, b = _lab(r['hx']); return L >= 84 and (a * a + b * b) ** .5 <= 12
n = 0
for k, r in D['racks'].items():
    r['pq'] = Q[k]['score'] if k in Q else 3; n += k in Q
    t = (r['n'] + ' ' + r.get('u0', '')).lower()
    r.pop('ww', None); r.pop('wp', None)
    if _white(r) and any(w in t for w in ('wood', 'beech')): r['ww'] = 1
    if _white(r) and 'pearl' in r['n'].lower(): r['wp'] = 1
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
if 'const pqk=' not in h:
    a = "const pen=r=>(R[r].pa?0:1e5)+(R[r].lo?1e4:0);"; assert h.count(a) == 1
    h = h.replace(a, a + f"/* v94 photo quality tie-breaker + Mahjong Studios last + white wood / pearl lead (Tiffany Oct 26 8:29, 8:50am) */const pqk=r=>hr.includes(r)||U.includes(r)?0:(5-(R[r].pq||3))*{K_LAB}+(rkMS(r)?1e6:0)-(rkW(r)===2?18:6*rkW(r));", 1)
    a = "function rackPool(){"; assert h.count(a) == 1
    h = h.replace(a, "const ownB=()=>[set().maker,(D.tiles[set().tile]||{}).bn,(M[S.fav]||{}).bn];const rkMS=r=>R[r].bn==='Mahjong Studios'&&!ownB().includes('Mahjong Studios');const rkW=r=>R[r].wp&&R[r].pq>=3&&/pearl/i.test(set().name)?2:R[r].ww&&R[r].pq>=4?1:0;"
                  "/* rule 4: own-brand matching racks early */const ownLift=(L,hr,U,sc)=>{const B=ownB(),mine=r=>hr.includes(r)||U.includes(r);const own=L.filter(r=>!mine(r)&&B.includes(R[r].bn)&&rackFits(r)&&sc(r)<=30).slice(0,2);if(!own.length)return L;const rest=L.filter(r=>!own.includes(r));let p=0;while(p<rest.length&&mine(rest[p]))p++;if(p<rest.length&&rkW(rest[p])===2)p++;return [...rest.slice(0,p),...own,...rest.slice(p)];};" + a, 1)
    a = "return [...new Set([...hr,...U,...Object.keys(R).filter(rackOK)])].filter(r=>R[r]).map(r=>[sc(r)+pen(r),r]).sort((a,b)=>a[0]-b[0]).map(x=>x[1]);"; assert h.count(a) == 1
    h = h.replace(a, "return ownLift(" + a[7:-1] + ",hr,U,sc);", 1)
    a = "return [...new Set([...hr,...U,...rest])];"; assert h.count(a) == 1
    h = h.replace(a, "return ownLift([...new Set([...hr,...U,...rest])],hr,U,sc);", 1)
    a = ".map(r=>[sc(r)+pen(r),r])"; assert h.count(a) == 2; h = h.replace(a, ".map(r=>[sc(r)+pen(r)+pqk(r),r])")
    a = "const rk=r=>-((R[r].rs||{})[c]||0);"; assert h.count(a) == 1
    h = h.replace(a, f"const rk=r=>-(((R[r].rs||{{}})[c]||0)+(hr.includes(r)?0:{K_RS}*((R[r].pq||3)-3)-(rkMS(r)?100:0)+(c==='neutral'?[0,.25,.8][rkW(r)]:0)+(ownB().includes(R[r].bn)?.3:0)));", 1)
open(P, 'w').write(h)
print(f"rack photo quality: {n} racks scored from config, {len(D['racks'])-n} default 3; white wood: " + ', '.join(r['n'] for r in D['racks'].values() if r.get('ww')) + '; white pearl: ' + ', '.join(r['n'] for r in D['racks'].values() if r.get('wp')))
