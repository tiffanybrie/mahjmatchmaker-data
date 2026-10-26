"""FYM v97 (Version 1.1) racks (docs/MATCH-INBOX.md, Oct 26 evening). Idempotent. Usage: v97_racks.py <build>
1. My Fair Mahjong NATURAL WOOD (Tiffany 5:40pm: feature it, we're short on wood racks). Its card photo was a tiny rotated crop
   from the vertical group shot (photo score 1, so the v96 rule kept it from ever leading). New photo: one straight rack cut
   from MFM's own 'Natural_Wooden_Racks.png' (assets/racks/v97/mfm-natural-wood-single.webp, looked at on white + navy),
   cutout (c:true), photo score 5, featured flag ft: a featured rack gets a lift (-8) in the rack pool whenever its colour fits the
   mat (within 35 dE), so warm / earthy / wood-friendly pairings see it early; MFM tile sets already put MFM racks first (tile
   brand rule). Links: all 6 MFM wood entries already point to /products/wooden-racks?variant=... (curl 200 Oct 26); only their
   internal keys carry the old 404 handle. Gate [87].
2. Peace Love Mahjong PAINTED racks (Tiffany 5:50pm: "chopped up"): 11 colours re-cut whole (both ends, lips, magnets) from PLM's
   own straight-on group photo RackswithNewColors (assets/racks/v97/plm/*.webp, flood-fill background + per-rack band split,
   neighbour slivers trimmed; looked at on white + navy). Mint and White are not in that photo and keep their current image.
   Gate [56] (rack review) + [88]."""
import sys, os, io, json, base64
import numpy as np
from PIL import Image
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
R = D['racks']; hd = json.load(open(B + '/hd/index.json')); IMG = {}; n = 0
def webp(path, w=700):
    im = Image.open(REPO + path).convert('RGBA')
    if im.width > w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'WEBP', quality=88, method=6); return 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode(), im
NW = 'myfairmahjong.com/wooden-racks?v=53371892990263'
if R[NW].get('im') != 'rk97natwood':
    IMG['rk97natwood'], im = webp('assets/racks/v97/mfm-natural-wood-single.webp')
    a = np.asarray(im).reshape(-1, 4); a = a[a[:, 3] > 200][:, :3]; med = np.median(a, 0).astype(int)
    R[NW].update(im='rk97natwood', c=True, pq=5, ft=True, hx='#%02x%02x%02x' % tuple(med)); hd['r'].pop(NW, None); n += 1
PLM = ['Chartreuse', 'Dark Green', 'Aqua', 'French Blue', 'Navy', 'Purple', 'Pink', 'Light Pink', 'Lilac', 'Red', 'Cobalt']
for c in PLM:
    k = 'plm:' + c; slug = c.lower().replace(' ', '-'); key = 'rk97plm' + slug.replace('-', '')
    if k not in R or R[k].get('im') == key: continue
    IMG[key], _ = webp(f'assets/racks/v97/plm/plm-{slug}.webp'); R[k].update(im=key, c=True); hd['r'].pop(k, None); n += 1
json.dump(hd, open(B + '/hd/index.json', 'w'), separators=(',', ':'))
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
o = "-(rkW(r)===2?18:6*rkW(r));"
if '/*v97 featured wood*/' not in h:
    assert h.count(o) == 1, h.count(o); h = h.replace(o, "-(rkW(r)===2?18:6*rkW(r))-(R[r].ft&&sc(r)<=35?8:0)/*v97 featured wood*/;"); n += 1
if IMG:
    inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMG, separators=(',', ':')) + ');</script>'
    a_ = '<script src="b24v1.js"></script>'; assert h.count(a_) == 1; h = h.replace(a_, a_ + inl, 1)
open(P, 'w').write(h)
q = json.load(open(REPO + 'config/rack-photo-quality.json'))
if q.get(NW, {}).get('score') != 5:
    q[NW].update(score=5, why='single straight rack cutout from the brand listing photo (v97)')
    json.dump(q, open(REPO + 'config/rack-photo-quality.json', 'w'), indent=1, ensure_ascii=False)
print('v97 racks', n, 'images', len(IMG))
