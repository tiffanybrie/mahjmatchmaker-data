"""v112: rack length + tile size data (Tiffany Oct 26 7:37/7:39pm: base rack fit on TILE SIZE, put the LENGTH in every rack's data).
Reads config/fym-rack-fit-nov01.json (researched Nov 1 from each brand's product page, src per row):
  R[k].len  = rack length in inches (18 / 18.5 / 19 / 20)
  T[tile].tw = tile width in inches (what decides the fit; unknown = left out = treated as large by ui112 RFIT)
Drops the old brand-based `sm` flag everywhere (ui112 E replaces smallSet()). Adds the length to the rack line of the shop list /
share text ("... (18.5 in rack)"). Locks the lengths. Idempotent. Run before ui112.py. Usage: python3 rackfit112.py <build_dir>"""
import sys, os, json
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
R, T = D['racks'], D['tiles']
F = json.load(open(REPO + 'config/fym-rack-fit-nov01.json'))
nl = nt = ns = 0
for k, x in F['racks'].items():
    if k in R and x.get('len') and R[k].get('len') != x['len']: R[k]['len'] = x['len']; nl += 1
for k, o in R.items():
    if o.pop('sm', None): ns += 1
for s in D['sets']:
    x = F['sets'].get(s['slug'])
    t = T.get(s['tile'])
    if x and t is not None and x.get('tw') and t.get('tw') != x['tw']: t['tw'] = x['tw']; nt += 1
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
a = "const nm=String(T[id]?s.name:R[id]?shortR(id):o.n)"
if '/*v112len*/' not in h:
    assert h.count(a) == 1, 'shop-list anchor moved'
    h = h.replace(a, "const nm=String(T[id]?s.name:R[id]?shortR(id)+(R[id].len?` (${R[id].len} in rack)`:'')/*v112len*/:o.n)")
open(P, 'w').write(h)
LK = json.load(open(REPO + 'builder/fym_flags/locks.json')); LK.setdefault('rack_len', {})
for k, x in F['racks'].items():
    if x.get('len'): LK['rack_len'][k] = x['len']
json.dump(LK, open(REPO + 'builder/fym_flags/locks.json', 'w'), indent=1, ensure_ascii=False)
print(f'rackfit112: len set {nl}, tile widths {nt}, sm flags dropped {ns}')
