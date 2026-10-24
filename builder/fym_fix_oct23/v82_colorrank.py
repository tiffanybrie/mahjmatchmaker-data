"""FYM v82: a pure colour ranking per tile set (s.cr = top 300 mat indices into D.order), measured, with no boost for
Tiffany's picks. Used when Tiffany's picks are OFF (Tiffany Oct 23: "defer to what the color theorist would pull").
Tile colours: the measured palette in config/tile-tones.json (white faces masked, doc 76); the tile photo only when a set has none; mat colours: M[id].ms swatches.
Score = 0.6 * (tile colours -> nearest mat colour) + 0.4 * (mat colours -> nearest tile colour), CIEDE2000, weighted by
share; holiday mats +25 so they sit after year-round mats unless the Holiday filter is on.
Usage: python3 v82_colorrank.py <build_dir>"""
import sys, os, json
import numpy as np
from PIL import Image
from skimage.color import rgb2lab, deltaE_ciede2000
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
def lab(hx): return rgb2lab(np.array([[[int(hx[k:k + 2], 16) / 255 for k in (1, 3, 5)]]]))[0, 0]
def swatches(im, n=6):
    sm = im.copy(); sm.thumbnail((240, 240)); a = np.asarray(sm.convert('RGB')).reshape(-1, 3)
    a = a[(a.min(1) < 235) | (a.max(1) - a.min(1) > 18)]
    if not len(a): return []
    q = Image.fromarray(a.reshape(-1, 1, 3).astype('uint8')).quantize(n, method=Image.Quantize.MEDIANCUT); pal = q.getpalette()[:n * 3]
    cnt = np.bincount(np.asarray(q).ravel(), minlength=n); tot = cnt.sum()
    return [('#%02x%02x%02x' % tuple(pal[k * 3:k * 3 + 3]), cnt[k] / tot) for k in np.argsort(-cnt) if cnt[k] / tot > .04]
order = D['order']; M = D['mats']
ML = {}
for m in order:
    ms = M[m].get('ms') or []
    if ms: ML[m] = (np.array([lab(hx) for hx, _ in ms]), np.array([w for _, w in ms], float))
keys = [m for m in order if m in ML and not M[m].get('hid')]
ALL = np.concatenate([ML[m][0] for m in keys]); W = [ML[m][1] for m in keys]
seg = np.cumsum([0] + [len(w) for w in W])
done = miss = 0; pal_photo = [0]
REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
TONES = json.load(open(os.path.join(REPO, 'config', 'tile-tones.json')))['sets']
import re
nm = lambda x: re.sub(r'[^a-z0-9]', '', (x or '').lower())
TBN = {nm(v.get('name')): v for v in TONES.values() if isinstance(v, dict)}
for s in D['sets']:
    tt = TONES.get(s['slug']) or TBN.get(nm(s['name']))
    if tt and tt.get('palette'): sw = [(hx, w) for hx, w in tt['palette'] if w >= .04]
    else:
        t = D['tiles'].get(s['tile']) or {}; f = t.get('full')
        if not f or not os.path.exists(os.path.join(B, f)): miss += 1; continue
        sw = swatches(Image.open(os.path.join(B, f))); pal_photo[0] += 1
    if not sw: miss += 1; continue
    la = np.array([lab(hx) for hx, _ in sw]); wa = np.array([w for _, w in sw], float)
    Dm = deltaE_ciede2000(np.repeat(la, len(ALL), 0), np.tile(ALL, (len(la), 1))).reshape(len(la), len(ALL))
    sc = []
    for j, m in enumerate(keys):
        d = Dm[:, seg[j]:seg[j + 1]]; wb = W[j]
        v = 0.6 * float((d.min(1) * wa).sum() / wa.sum()) + 0.4 * float((d.min(0) * wb).sum() / wb.sum())
        sc.append((v + (25 if M[m].get('hol') else 0), order.index(m)))
    sc.sort(); s['cr'] = [k for _, k in sc[:300]]; done += 1
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
h = h.replace("function colorPool(){const r=set().rank.map(i=>D.order[i])", "function colorPool(){const r=(set().cr&&set().cr.length?[...set().cr,...set().rank]:set().rank).map(i=>D.order[i])", 1)
h = h.replace("const s=new Set(r);return [...r,", "const s=new Set(r);return [...new Set(r),", 1)
open(P, 'w').write(h); print('colour rank: sets', done, 'missing photo', miss, 'from photo (no palette)', pal_photo[0])
