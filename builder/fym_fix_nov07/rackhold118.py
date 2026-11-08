"""FYM 1.18: Table view rack cut-outs held back for a light halo (gate [146] (b); coordinator Nov 7: "Don't ship a halo"). Looked at on
white + navy Nov 7 11:40pm (scratchpad peony_rack.jpg): Mahjong Register Peony Blush Pearl Scalloped shows a white rim on the scallops and
the bottom edge on navy; builder/fym_defringe.py (white/clear threshold) removes almost nothing (pearl body is near-white at the rim), so the
cut is held: the rack stays in every deck, only its Table view flag is off with a reason (rkw) until the racks agent re-cuts it.
Runs after tableview_racks_v118.py. Idempotent. Usage: python3 builder/fym_fix_nov07/rackhold118.py <build dir>"""
import sys, os, json
HOLD = {'mahjongregister.com/signature-collection-acrylic-mahjong-racks-set-of-4-20-luxury-tile-holders-copy?v=53016959287608':
        'Table view cut-out being redone (light edge on dark mats).'}
P = os.path.join(sys.argv[1], 'index.html'); h = open(P).read(); i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:]); e += i
TV = D['tv']; n = 0
for k, why in HOLD.items():
    if k in D['racks'] and (TV.get('rk', {}).get(k) or k in TV.get('ro', {})):
        TV['rk'].pop(k, None); TV.get('ro', {}).pop(k, None); TV.setdefault('rkw', {})[k] = why; n += 1
open(P, 'w').write(h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[e:])
print('rackhold118: held', n)
