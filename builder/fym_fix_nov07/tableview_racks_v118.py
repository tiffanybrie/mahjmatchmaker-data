"""FYM 1.18: Table view RACKS caught up (Tiffany Nov 7: "Table view completely caught up"; gap audit B3: 169 of 293 usable).
Reads config/tableview-racks-nov07.json:
  racks      {rack key: {file, sha1, len, ...}}  a clean straight single-rack cut-out (brand photo, straightened, cut out, LOOKED AT
             on white + navy, approved in builder/fym_flags/rack_image_review.json tag 'tv'). file = null -> the app's own rack image
             is already a clean straight cut-out (only the Table flag was missing).
  not_usable {rack key: {why}}  still grayed in Table view, with the exact reason shown in the swap sheet.
For every visible rack with an entry: D.tv.ro[k] = the cut-out (embedded byte-for-byte, so the reviewed sha1 is what ships),
D.tv.rk[k] = 1, D.tv.rkw[k] dropped, D.racks[k].len = the brand's stated length. Not-usable racks get their reason in D.tv.rkw.
Run by build118.sh after tv118.py (data patches first). Idempotent. Does not touch any other build file.
Usage: python3 builder/fym_fix_nov07/tableview_racks_v118.py <build dir>"""
import sys, os, json, base64, hashlib, pathlib
R0 = pathlib.Path(__file__).resolve().parents[2]
B = sys.argv[1]; P = os.path.join(B, 'index.html')
C = json.load(open(R0 / 'config/tableview-racks-nov07.json'))
REV = json.load(open(R0 / 'builder/fym_flags/rack_image_review.json'))
h = open(P).read(); i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:])
RK = D['racks']; TV = D['tv']; TV.setdefault('ro', {}); TV.setdefault('rk', {}); TV.setdefault('rkw', {})
vis = [k for k, r in RK.items() if not r.get('hid')]
before = sum(1 for k in vis if TV['rk'].get(k))
added, lens, skipped = [], 0, []
for k, v in C['racks'].items():
    if k not in RK or RK[k].get('hid'): skipped.append(k); continue
    if v.get('file'):
        b = open(R0 / v['file'], 'rb').read(); s = hashlib.sha1(b).hexdigest()
        assert s == v['sha1'], f"{v['name']}: cut-out changed since it was looked at ({v['file']})"
        assert REV.get(s, {}).get('verdict') == 'ok', f"{v['name']}: cut-out not approved in rack_image_review.json"
        TV['ro'][k] = 'data:image/webp;base64,' + base64.b64encode(b).decode()
    if not TV['rk'].get(k): added.append(v['name'])
    TV['rk'][k] = 1; TV['rkw'].pop(k, None)
    if v.get('len') and RK[k].get('len') != v['len']: RK[k]['len'] = v['len']; lens += 1
for k, v in C.get('not_usable', {}).items():
    if k in RK and not TV['rk'].get(k): TV['rkw'][k] = v['why']
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[i + e:]; open(P, 'w').write(h)
after = sum(1 for k in vis if TV['rk'].get(k))
print(f"tableview_racks_v118: Table-usable racks {before} -> {after} of {len(vis)} visible (+{len(added)}; lengths set {lens}; "
      f"not in this build {len(skipped)}); still grayed {len(vis) - after}")
