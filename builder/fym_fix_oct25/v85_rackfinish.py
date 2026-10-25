"""FYM v85 (Tiffany Oct 25 14:38-14:40): rack filter gets two finish chips, WOOD and TORTOISE, at the front of the rack colour row
(start with just these two; everything else stays colour dots). Tags from config/rack-finishes.json (tagged by photo).
A finish chip combines with colours like any chip (Wood + Brown = brown wood racks).
Usage: python3 v85_rackfinish.py <build_dir>  (in place)"""
import sys, os, json
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
P = sys.argv[1] + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
F = json.load(open(REPO + '/config/rack-finishes.json')); n = 0
for fin in ('wood', 'tortoise'):
    for k in F[fin]:
        r = D['racks'].get(k)
        if r is not None and fin not in r['rf']: r['rf'] = r['rf'] + [fin]; n += 1
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
a = "data-fam=\"holiday\" data-k=\"m\" aria-pressed=\"${f.fam.includes('holiday')}\">Holiday</button>`:''}"
assert h.count(a) == 1
h = h.replace(a, a + "${k==='r'?['wood','tortoise'].filter(x=>pool.some(id=>fk(id).includes(x))).map(x=>`<button type=\"button\" class=\"chip finc\" "
              "data-fam=\"${x}\" data-k=\"r\" aria-pressed=\"${f.fam.includes(x)}\">${x==='wood'?'Wood':'Tortoise'}</button>`).join(''):''}")
css = '.rfil{padding:8px 0 10px}'
assert h.count(css) == 1
h = h.replace(css, css + ' .chip.finc{border:2px solid #8a5a3b;color:#6b4226;background:#fff;flex:none} .chip.finc[aria-pressed="true"]{background:#6b4226;border-color:#6b4226;color:#fff}')
open(P, 'w').write(h); print('rack finish tags added', n)
