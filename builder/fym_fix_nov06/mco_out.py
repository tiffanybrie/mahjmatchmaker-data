"""Mahjong Co. MATS out of Find Your Mat-ch (Tiffany Nov 6 3:56pm: "hide every one"; the shop is empty, the mats are retired/404).
Hides (never deletes) every mat whose key is on mahjongco.com (brand label 'Mahjong by SI'); the Kaleidoscope tiles and any other
Mahjong Co. TILE set stay. Writes what it hid to archive/mahjong-co-mats-hidden-2026-11-06.json. Gate [161] checks the result.
Usage: python3 builder/fym_fix_nov06/mco_out.py <build dir>   (edits <build dir>/index.html in place)"""
import sys, os, json
B = sys.argv[1]; R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
DOM = 'mahjongco.com/'
p = B + '/index.html'; h = open(p).read(); i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:])
hid = []
for k, v in D['mats'].items():
    if k.startswith(DOM):
        if not v.get('hid'): hid.append(k)
        v['hid'] = True; v['parked'] = 'mahjong-co-retired-nov06'
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[i + e:]
open(p, 'w').write(h)
json.dump({'hidden_mats': hid, 'why': 'Tiffany Nov 6 3:56pm: hide every Mahjong Co. mat (retired, shop empty); Kaleidoscope tiles stay'},
          open(R + 'archive/mahjong-co-mats-hidden-2026-11-06.json', 'w'), indent=1)
print('Mahjong Co. mats OUT of FYM:', len(hid))
