"""Peel-corner mats (Tiffany Nov 2 8:15am, via coordinator): ~90 product renders show the whole mat except a curled top-right
corner (black underside / the other side of a double-sided mat). Table view fills that corner at draw time by mirroring the
mat left<->right inside a small polygon around the peel, so these mats become FULL table class. No new image bytes: per mat we
store the mat square in the photo (b = x0,y0,x1,y1, 0..1) and the peel polygon (p, 0..1 of the square).
Usage: python3 peel_nov02.py <build dir> <out json> [sheet.jpg]"""
import sys, json, numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
from scipy.spatial import ConvexHull
sys.path.insert(0, __import__('os').path.dirname(__file__))
from matimg import load_D, mat_full
def analyse(im):
    a = np.asarray(im).astype(int); H, W = a.shape[:2]; mn = a.min(2); mx = a.max(2); L = a.mean(2)
    bg = (mn > 238) & (mx - mn < 12)
    fg = ~bg; rows = np.where(fg[:, :W // 2].mean(1) > .3)[0]; cols = np.where(fg[H // 2:].mean(0) > .3)[0]
    if not len(rows) or not len(cols): return None
    y0, y1, x0, x1 = rows.min(), rows.max(), cols.min(), cols.max()
    S = a[y0:y1 + 1, x0:x1 + 1]; h, w = S.shape[:2]
    if abs(h - w) > .08 * max(h, w): return {'why': f'not square ({w}x{h})'}
    sbg = bg[y0:y1 + 1, x0:x1 + 1]; sL = L[y0:y1 + 1, x0:x1 + 1]; ssp = (mx - mn)[y0:y1 + 1, x0:x1 + 1]
    q = np.zeros((h, w), bool); q[:int(h * .62), int(w * .38):] = True
    lb, nb = ndimage.label(sbg & q); ids = set(np.unique(lb[0, :])) | set(np.unique(lb[:, -1])); ids.discard(0)
    sbg = np.isin(lb, list(ids))  # background = only the white connected to the top / right edge (not white in the design)
    dark = (sL < 100) & (ssp < 45) & q
    lab, n = ndimage.label(dark); best, bs = None, 0
    near = ndimage.binary_dilation(sbg & q, iterations=4)
    for i in range(1, n + 1):
        cc = lab == i; s = cc.sum()
        if s > bs and (cc & near).any(): best, bs = cc, s
    if best is None or bs < .004 * h * w: return {'why': 'no peel found'}
    P = best | (sbg & q & (np.arange(w)[None, :] > w * .5))
    P = ndimage.binary_dilation(P, iterations=max(4, int(w * .012)))
    ys, xs = np.where(P); pts = np.c_[xs, ys]; hull = ConvexHull(pts); poly = pts[hull.vertices]
    if (xs < w * .5).any() or (ys > h * .5).any(): return {'why': 'peel area crosses the middle'}
    return {'b': [round(x0 / W, 4), round(y0 / H, 4), round((x1 + 1) / W, 4), round((y1 + 1) / H, 4)], 'p': [[round(x / w, 4), round(y / h, 4)] for x, y in poly], 'area': round(float(P.mean()), 3)}
def fill(im, r):
    W, H = im.size; b = r['b']; sq = im.crop((int(b[0] * W), int(b[1] * H), int(b[2] * W), int(b[3] * H))); w, h = sq.size
    mir = sq.transpose(Image.FLIP_LEFT_RIGHT); m = Image.new('L', sq.size, 0); ImageDraw.Draw(m).polygon([(x * w, y * h) for x, y in r['p']], fill=255)
    out = sq.copy(); out.paste(mir, (0, 0), m); return out
if __name__ == '__main__':
    B, OUT = sys.argv[1], sys.argv[2]; D = load_D(B); C = json.load(open('config/tableview-photo-class-nov01.json'))
    ks = [k for k, v in C.items() if not k.startswith('_') and v['class'] == 'B' and str(v.get('note', '')).startswith('peel') and k in D['mats']]
    res = {}
    for k in ks:
        im = mat_full(B, D['mats'][k]['f']); r = analyse(im) if im else {'why': 'no photo'}; res[k] = r
    json.dump(res, open(OUT, 'w'), indent=0); ok = [k for k in ks if 'p' in res[k]]
    print('peel mats', len(ks), 'polygon found', len(ok), 'not:', {D['mats'][k]['n']: res[k]['why'] for k in ks if 'p' not in res[k]})
    if len(sys.argv) > 3:
        S = 220; Wn = 8; rows = (len(ks) + Wn - 1) // Wn; o = Image.new('RGB', (Wn * S * 2, rows * (S + 16)), 'white'); d = ImageDraw.Draw(o)
        for i, k in enumerate(ks):
            im = mat_full(B, D['mats'][k]['f']); x, y = (i % Wn) * S * 2, (i // Wn) * (S + 16)
            t = im.copy(); t.thumbnail((S, S)); o.paste(t, (x, y))
            if 'p' in res[k]: f = fill(im, res[k]); f.thumbnail((S, S)); o.paste(f, (x + S, y))
            d.text((x + 2, y + S + 2), f"{i} {D['mats'][k]['n'][:30]} {res[k].get('why', '')}", fill='black')
        o.save(sys.argv[3], quality=82)
def square_box(im):
    a = np.asarray(im).astype(int); H, W = a.shape[:2]; mn = a.min(2); mx = a.max(2); bg = (mn > 238) & (mx - mn < 12)
    rows = np.where((~bg)[:, :W // 2].mean(1) > .3)[0]; cols = np.where((~bg)[H // 2:].mean(0) > .3)[0]
    y0, y1, x0, x1 = rows.min(), rows.max(), cols.min(), cols.max()
    if abs((y1 - y0) - (x1 - x0)) > .08 * max(y1 - y0, x1 - x0): return None
    return [round(x0 / W, 4), round(y0 / H, 4), round((x1 + 1) / W, 4), round((y1 + 1) / H, 4)]
def template(B, D, ks, refs):
    pts = []
    for k in ks:
        if D['mats'][k]['n'] in refs:
            r = analyse(mat_full(B, D['mats'][k]['f'])); pts += r['p']
    pts = np.array(pts); h = ConvexHull(pts); return [[round(float(x), 4), round(float(y), 4)] for x, y in pts[h.vertices]]
