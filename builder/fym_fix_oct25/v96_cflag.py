"""FYM v96 (QA Oct 26): racks whose photo is a transparent cutout must carry c:true, or the tri card draws a white box behind
them. Sets c:true for every visible rack whose image is a transparent cutout (all 4 corners alpha 0) in the named list.
Idempotent. Usage: python3 v96_cflag.py <build>"""
import sys, json
NAMES = ['My Fair Mahjong Bright White', 'My Fair Mahjong Pearl White', 'Virora White Magnetic', 'Ivory Oyster Pearl',
         'White Wooden Racks with Scalloped', 'Baby Blue Wooden Racks with Scalloped', 'Double Wooden Mahjong Racks', 'Bam Bird Boutique White Acrylic', 'White Lace']
P = sys.argv[1] + '/index.html'; h = open(P).read(); i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:]); e += i
n = []
for k, r in D['racks'].items():
    if r.get('hid'): continue
    full = r.get('n', '') + ' ' + r.get('bn', '')
    if any(x.lower() in full.lower() for x in NAMES) and not r.get('c'):
        r['c'] = True; n.append(r['n'])
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[e:]
open(P, 'w').write(h); print('cflag', len(n), n)
