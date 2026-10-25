"""FYM v85 colour fix, step 2: rebuild every tile set's colour ranking (s.cr, used whenever Tiffany's picks are off, and the ONLY
ranking for the 221 sets she hasn't matched).
Changes vs v82_colorrank (Tiffany Oct 25: Ash Burl showed Let's Be Besties Green Bright Floral first):
 1. Unblended colours: mats and tiles use config/fym-colour-oct25.json (k-means in Lab, builder/fym_fix_oct25/v85_measure.py),
    not the old 5-colour median-cut that averaged hot pink flowers into dusty rose / tan.
 2. Vividness rule (her clean-vs-earthy colour theory, doc 76): vivid share = weight of colours with Lab chroma >= 38.
    A mat much more vivid than the tiles (bright floral on natural burl) or much duller than them (muddy mat on bright tiles)
    is pushed down: +140 per unit of the gap beyond a small tolerance.
 4. Holiday tile sets (BACKG Holiday) get holiday mats first; room-photo mats (config/fym-colour-room-photos.json) stay out of colour-only ranking.
 3. Brand's own mats first (Tiffany Oct 25) for sets she hasn't matched (m == []): the tile brand's own visible mats that pass the
    colour check (score within the set's best 60) go to the front, in score order. Holiday mats stay after year-round ones.
Usage: python3 v85_colorrank.py <build_dir>  (in place)"""
import sys, os, json
import numpy as np
from skimage.color import rgb2lab, deltaE_ciede2000
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
C = json.load(open(REPO + '/config/fym-colour-oct25.json'))
def lab(hx): return rgb2lab(np.array([[[int(hx[k:k + 2], 16) / 255 for k in (1, 3, 5)]]]))[0, 0]
def prep(sw):
    if not sw: return None
    L = np.array([lab(hx) for hx, _ in sw]); w = np.array([x for _, x in sw], float); w = w / w.sum()
    chroma = np.hypot(L[:, 1], L[:, 2]); return L, w, float(w[chroma >= 38].sum())
import re as _re
_m = _re.search(r'BACKG=(\{.*?\});', h)
HOLSETS = set(json.loads(_m.group(1)).get('Holiday', [])) if _m else set()
# mats whose only photo is a room / lifestyle shot: their measured colours are mostly the room, so they stay out of the
# colour-only ranking (they still show for Tiffany's picks, filters, brand and search). Listed by eye from the audit sheets.
ROOM = set(json.load(open(REPO + '/config/fym-colour-room-photos.json'))['mats']) if os.path.exists(REPO + '/config/fym-colour-room-photos.json') else set()
M = D['mats']; order = D['order']; OI = {m: j for j, m in enumerate(order)}
keys = [m for m in order if not M[m].get('hid') and m in C['mats'] and C['mats'][m]['sw'] and m not in ROOM]
MP = {m: prep(C['mats'][m]['sw']) for m in keys}
ALL = np.concatenate([MP[m][0] for m in keys]); seg = np.cumsum([0] + [len(MP[m][1]) for m in keys])
VIV_TOL, VIV_K = 0.08, 140.0
done = brand_front = 0; report = {}
for s in D['sets']:
    cs = C['sets'].get(s['slug']) or {}
    tp = prep(cs.get('sw'))
    if not tp: continue
    la, wa, vt = tp
    hol_set = s['name'] in HOLSETS
    Dm = deltaE_ciede2000(np.repeat(la, len(ALL), 0), np.tile(ALL, (len(la), 1))).reshape(len(la), len(ALL))
    sc = {}
    for j, m in enumerate(keys):
        d = Dm[:, seg[j]:seg[j + 1]]; _, wb, vm = MP[m]
        v = 0.6 * float((d.min(1) * wa).sum()) + 0.4 * float((d.min(0) * wb).sum())
        v += VIV_K * max(0.0, abs(vm - vt) - VIV_TOL)
        if M[m].get('hol'): v += (-25 if hol_set else 25)  # holiday tile sets: holiday mats first; year-round sets: after
        sc[m] = v
    ranked = sorted(sc, key=lambda m: sc[m])
    front = []
    if not s['m']:
        best60 = set(ranked[:60]); tb = (D['tiles'].get(s['tile']) or {}).get('bn') or s['maker']
        front = [m for m in ranked if m in best60 and M[m].get('bn') == tb and (bool(M[m].get('hol')) == hol_set or M[m].get('wfh'))]
        if front: brand_front += 1
    out = front + [m for m in ranked if m not in front]
    s['cr'] = [OI[m] for m in out[:300]]; done += 1
    report[s['slug']] = {'name': s['name'], 'maker': s['maker'], 'vivid': round(vt, 2), 'brand_front': len(front),
                         'top': [[M[m]['n'], M[m]['bn'], round(sc[m], 1), round(MP[m][2], 2)] for m in out[:8]]}
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
open(P, 'w').write(h)
json.dump(report, open(B + '/v85_colorrank_report.json', 'w'), indent=1, ensure_ascii=False)
print('colour rank v85: sets', done, 'of', len(D['sets']), '| brand mats first on', brand_front, 'unmatched sets')
