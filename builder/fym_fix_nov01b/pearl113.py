"""v113: Tiffany Nov 1 3:43pm.
 A. PEARL rack finish: rf += 'pearl' for racks whose name matches config/fym-rack-pearl-nov01.json words, or listed by_eye.
    Chip 'Pearl' next to Wood / Tortoise / Metallic / Clear in the rack filters (shared filters() = both doors). Colours kept.
 B. Rack search matches FINISH words too: each rack's search text = name + brand + its finishes and their synonyms
    (wood: wood wooden walnut beechwood oak pine maple; tortoise: tortoise tortoiseshell; clear: clear acrylic lucite;
    metallic: metallic gold silver brass; pearl: pearl pearlescent iridescent opal).
Idempotent. Usage: python3 pearl113.py <build_dir>"""
import sys, os, json, re
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
CF = json.load(open(REPO + 'config/fym-rack-pearl-nov01.json')); W = re.compile(CF['words'], re.I)
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i; n = []
for k, r in D['racks'].items():
    if W.search(r.get('n', '')) or k in CF['by_eye']:
        rf = r.setdefault('rf', [])
        if 'pearl' not in rf: rf.append('pearl')
        if not r.get('hid'): n.append(r['n'])
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
if '/*v113 pearl*/' not in h:
    def rep(a, b):
        global h
        assert h.count(a) == 1, (h.count(a), a[:90]); h = h.replace(a, b)
    rep("RFINN={wood:'Wood',tortoise:'Tortoise',metallic:'Metallic',clear:'Clear'};", "RFINN={wood:'Wood',tortoise:'Tortoise',metallic:'Metallic',clear:'Clear',pearl:'Pearl'};/*v113 pearl*/const RFSYN={wood:'wood wooden walnut beechwood oak pine maple',tortoise:'tortoise tortoiseshell',clear:'clear acrylic lucite',metallic:'metallic gold silver brass',pearl:'pearl pearlescent iridescent opal'};")
    rep("${k==='r'?['wood','tortoise','metallic','clear'].filter(", "${k==='r'?['wood','tortoise','metallic','clear','pearl'].filter(")
    rep("const s=NRM(R[id].n+' '+(R[id].bn||''));return toks.every(t=>s.includes(t));", "const s=NRM(R[id].n+' '+(R[id].bn||'')+' '+(R[id].rf||[]).map(x=>RFSYN[x]||'').join(' '));return toks.every(t=>s.includes(t));")
open(P, 'w').write(h); print('pearl113: visible pearl racks', len(n), n)
