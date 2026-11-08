"""FYM 1.18: Table view MATS made usable (Tiffany Nov 7 10:22pm 'get table view completely updated'; OMM Lotus Cove first).
Runs after tv118.py (build118.sh calls it when present). Reads config/tableview-mats-nov07.json and, inside D.tv:
  cls / why  class per mat (A full table, B corner, C grayed + reason); A/B drop any old 'why'
  fa         affine that crops/straightens the app's own FYM photo to the mat (full table; no new bytes)
  mo         a different VENDOR photo (product page), straightened to an all-mat square, inlined as a data URL (800px webp)
  cv         corner fit for new corner-class mats
  pf         peel-corner renders filled to a full table (square box b; the global T2 peel polygon)
A mat given fa/mo loses any old peel fill (pf) / corner fit (cv) entry, which were measured on the old photo.
JS (preview_tv.js render(), patched in place, idempotent): the Table render uses TVD.mo[mat] instead of matFull(mat) when set,
and draws TVD.fa[mat] (full table) before the plain centre-square crop. Racks are NOT touched (rack agent: tableview_racks_v118.py).
Works on a build dir or a single index.html (website copy: site-app/fym-vNN/index.html).
Usage: python3 builder/fym_fix_nov07/tableview_v118.py <build dir | index.html>"""
import sys, os, json, io, base64, pathlib
from PIL import Image
R = pathlib.Path(__file__).resolve().parents[2]
A = sys.argv[1]; P = A if A.endswith('.html') else os.path.join(A, 'index.html')
C = json.load(open(R / 'config/tableview-mats-nov07.json'))
h = open(P).read(); i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:])
M = D['mats']; TV = D['tv']
for k in ('cls', 'why', 'pf', 'cv'): TV.setdefault(k, {})
TV.setdefault('fa', {}); TV.setdefault('mo', {})
def durl(p, px=800, q=80):
    im = Image.open(R / p).convert('RGB'); im = im.resize((px, px), Image.LANCZOS) if im.size != (px, px) else im
    b = io.BytesIO(); im.save(b, 'WEBP', quality=q); return 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()
n = {'cls': 0, 'fa': 0, 'mo': 0, 'cv': 0, 'missing_key': 0}
for k, cl in C['cls'].items():
    if k not in M: n['missing_key'] += 1; continue
    TV['cls'][k] = cl; n['cls'] += 1
    if cl in ('A', 'B'): TV['why'].pop(k, None)
    elif C['why'].get(k): TV['why'][k] = C['why'][k]
    TV['fa'].pop(k, None); TV['mo'].pop(k, None)  # this config owns fa/mo for its keys (a re-run never keeps a stale photo)
    if k in C['fa'] or k in C['mo'] or k in C.get('pf', {}) or cl == 'C':
        TV['pf'].pop(k, None)
        if k not in C['cv']: TV['cv'].pop(k, None)
    if k in C['fa']: TV['fa'][k] = C['fa'][k]; n['fa'] += 1
    if k in C['mo']: TV['mo'][k] = durl(C['mo'][k]); n['mo'] += 1
    if k in C['cv']: TV['cv'][k] = C['cv'][k]; n['cv'] += 1
    if k in C.get('pf', {}): TV['pf'][k] = C['pf'][k]; n['pf'] = n.get('pf', 0) + 1
for k in list(TV['fa']):
    if TV['cls'].get(k) != 'A': TV['fa'].pop(k)
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[i + e:]
J1a = 'matFull(mat).then(load)'; J1b = '(TVD.mo&&TVD.mo[mat]?Promise.resolve(TVD.mo[mat]):matFull(mat)).then(load)'
J2a = 'else if(corner){const q0=N*.36;c.drawImage(mi,q0,q0,N-q0,N-q0)}'
J2b = ('else if(!corner&&TVD.fa&&TVD.fa[mat]){const [fa,fb,fc,fd,fe,ff]=TVD.fa[mat];c.save();c.setTransform(fa*N,fb*N,fc*N,fd*N,fe*N,ff*N);'
       'c.drawImage(mi,0,0,1,1);c.restore()}' + J2a)
js = 'already'
if J1b not in h:
    assert h.count(J1a) == 1 and h.count(J2a) == 1, ('Table view render() anchors not found', h.count(J1a), h.count(J2a))
    h = h.replace(J1a, J1b).replace(J2a, J2b); js = 'patched'
else:
    assert 'TVD.fa&&TVD.fa[mat]' in h
open(P, 'w').write(h)
vm = [k for k, m in M.items() if not m.get('hid')]
from collections import Counter
cc = Counter(TV['cls'].get(k, '-') for k in vm)
mo_kb = sum(len(v) for v in TV['mo'].values()) // 1024
print(f"tableview_v118: config {n} | JS {js} | D.tv.mo {len(TV['mo'])} photos ({mo_kb} KB inline), fa {len(TV['fa'])}")
print(f"tableview_v118: mats usable {cc['A'] + cc['B']} of {len(vm)} visible (A {cc['A']}, B {cc['B']}, C {cc['C']}, unclassified {cc['-']})")
lc = 'www.ohmymahjong.com/lotus-cove-mat-in-tube'
print('tableview_v118: Lotus Cove', TV['cls'].get(lc), 'vendor photo' if lc in TV['mo'] else '', 'hidden' if M.get(lc, {}).get('hid') else 'visible')
