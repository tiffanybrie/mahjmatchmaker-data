"""Corner view that FILLS THE SQUARE (Tiffany Nov 2 8:15am: 'a corner view must fill the whole square'; Scandi Folk Christmas
(Cream), YOLO Winter Ski Resort sat small in a beige square). For every Corner-class mat this finds a real flat corner of the
mat in its photo (straightened if the photo is tilted), puts it at the card's bottom-right and crops the largest square that
is ALL mat, so the photo covers the whole card. Output per mat: m = 2D affine (a,b,c,d,e,f) mapping the photo in 0..1 units to
the card in 0..1 units (canvas transform), f = share of the mat's side the card shows (sets the rack / wall scale), kind.
Photos with no background to find a corner in (close-ups, props, mat on a table) use the largest centred square of the photo.
Usage: python3 corner_nov02.py <build dir> <keys json> <peel template json> <out json>"""
import sys, json, numpy as np, cv2
from scipy import ndimage
sys.path.insert(0, __import__('os').path.dirname(__file__))
from matimg import load_D, mat_full
def mat_mask(a, note, solid_peel=False, peel=None):
    H, W = a.shape[:2]; b = np.concatenate([a[:4].reshape(-1, 3), a[-4:].reshape(-1, 3), a[:, :4].reshape(-1, 3), a[:, -4:].reshape(-1, 3)]).astype(float)
    if solid_peel:  # double-sided solid leatherette: the mat side we keep = colour of the bottom-left quadrant
        body = np.median(a[H // 2:, :W // 2].reshape(-1, 3), 0); m = np.sqrt(((a - body) ** 2).sum(2)) < 28
    else:
        mn = a.min(2); bgw = (mn > 228) & (a.max(2) - mn < 18)  # near-white studio backdrop
        lb, n = ndimage.label(bgw); edge_ids = set(np.unique(np.r_[lb[0], lb[-1], lb[:, 0], lb[:, -1]])) - {0}
        bg = np.isin(lb, list(edge_ids)); m = ~bg
        if bg.mean() < .02: return None  # no background: the photo is all mat (or a scene) -> centred square
    if not solid_peel:  # white mats (toile on white, gingham with white checks): close the gaps so the mat is one solid shape
        k = max(3, int(.025 * max(W, H))); m = ndimage.binary_fill_holes(ndimage.binary_closing(np.pad(m, k), iterations=k))[k:-k, k:-k]
    if peel is not None: m &= ~peel
    m = ndimage.binary_opening(m, iterations=2); lb, n = ndimage.label(m)
    if not n: return None
    sz = ndimage.sum(m, lb, range(1, n + 1)); m = ndimage.binary_fill_holes(lb == (np.argmax(sz) + 1)); return m
def inside(m, P, a, b, s, n=40):
    t = (np.arange(n) + .5) / n; X, Y = np.meshgrid(t, t); pts = P[None, None] + (X[..., None] * s) * a + (Y[..., None] * s) * b
    xs, ys = np.round(pts[..., 0]).astype(int), np.round(pts[..., 1]).astype(int); H, W = m.shape
    ok = (xs >= 0) & (xs < W) & (ys >= 0) & (ys < H); v = np.zeros_like(ok); v[ok] = m[ys[ok], xs[ok]]; return v.mean()
def best_square(m, P, a, b):
    lo, hi = 0.0, float(max(m.shape)) * 1.5
    for _ in range(30):
        mid = (lo + hi) / 2
        if inside(m, P, a, b, mid, 64) >= 1.0: lo = mid
        else: hi = mid
    return lo
def fit(a, note, solid_peel=False, peel=None):
    H, W = a.shape[:2]; m = mat_mask(a, note, solid_peel, peel)
    if m is None: return centred(W, H, 'all mat (no background): centred square')
    cs, _ = cv2.findContours(m.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE); cnt = max(cs, key=cv2.contourArea)
    ap = cv2.approxPolyDP(cnt, .01 * cv2.arcLength(cnt, True), True)[:, 0].astype(float); n = len(ap); best = None
    segs = [(ap[i], ap[(i + 1) % n]) for i in range(n)]; Lmin = .18 * max(W, H)
    longs = [i for i, (p, q) in enumerate(segs) if np.linalg.norm(q - p) >= Lmin]
    for j in range(len(longs)):
        i1, i2 = longs[j], longs[(j + 1) % len(longs)]
        if len(longs) < 2: break
        gap = (i2 - i1) % n
        if gap > 4: continue  # only a short chamfer / rounded bit between the two long edges
        p1, q1 = segs[i1]; p2, q2 = segs[i2]; d1 = (q1 - p1) / np.linalg.norm(q1 - p1); d2 = (q2 - p2) / np.linalg.norm(q2 - p2)
        ang = np.degrees(np.arccos(np.clip(-d1 @ d2, -1, 1)))
        if not 80 <= ang <= 100: continue
        Mx = np.c_[d1, -d2]
        if abs(np.linalg.det(Mx)) < 1e-6: continue
        t = np.linalg.solve(Mx, p2 - p1); P = p1 + t[0] * d1  # where the two long edges meet = the mat's real corner
        e1 = -d1; e2 = d2; e2 = e2 - (e2 @ e1) * e1; e2 /= np.linalg.norm(e2)
        P2 = P + .03 * max(W, H) * (e1 + e2)  # step past a rounded corner
        sq = best_square(m, P2, e1, e2); lu, lv = np.linalg.norm(q1 - p1), np.linalg.norm(q2 - p2)
        e1_, e2_ = (e2, e1) if np.linalg.det(np.c_[e1, e2]) < 0 else (e1, e2)
        rot = abs(np.degrees(np.arctan2(e1_[1], -e1_[0])))
        sc = sq * (1 if rot < 25 else .8)
        if best is None or sc > best[5]: best = (sq, P2, e1, e2, max(lu, lv), sc)
    if best is None or best[0] < .3 * min(W, H): return centred(W, H, 'no clean right-angle corner: centred square') if m.mean() > .9 else None
    s, P, e1, e2, L, _ = best; s *= .985
    if np.linalg.det(np.c_[e1, e2]) < 0: e1, e2 = e2, e1
    side = L if note in ('edge-rolled', 'peel', 'peel-solid', 'banner-partial') else L / .85
    return affine(P, e1, e2, s, W, H, min(.9, max(.4, s / side)), 'corner')
def bbox_corner(a, which, f=.56, inset=.03):
    H, W = a.shape[:2]; mn = a.min(2); bg = (mn > 228) & (a.max(2) - mn < 18); fg = ~bg
    rows = np.where(fg[:, W // 4:3 * W // 4].mean(1) > .5)[0]; cols = np.where(fg[H // 4:3 * H // 4].mean(0) > .5)[0]
    x0, x1, y0, y1 = cols.min(), cols.max(), rows.min(), rows.max(); side = max(x1 - x0, y1 - y0); r = inset * side
    if which == 'BR': P, e1, e2 = np.array([x1 - r, y1 - r]), np.array([-1., 0]), np.array([0., -1])
    else: P, e1, e2 = np.array([x0 + r, y1 - r]), np.array([0., -1]), np.array([1., 0])
    return affine(P, e1, e2, f * side, W, H, f, 'corner', f'flat {which} corner of the whole-mat photo')
def centred(W, H, why, cx=.5, cy=.5, k=.97):
    s = min(W, H) * k; P = np.array([cx * W + s / 2, cy * H + s / 2]); return affine(P, np.array([-1., 0]), np.array([0., -1]), s, W, H, .55, 'centred', why)
def affine(P, a, b, s, W, H, f, kind, why=''):
    A = np.c_[a * s, b * s]; Ai = np.linalg.inv(A); M = np.c_[-Ai @ np.diag([W, H]), np.ones(2) + Ai @ P]
    return {'m': [round(float(x), 6) for x in (M[0, 0], M[1, 0], M[0, 1], M[1, 1], M[0, 2], M[1, 2])], 'f': round(float(f), 3), 'kind': kind, 'why': why}
def warp(im, r, N=300):
    a, b, c, d, e, f = r['m']; M = np.array([[a, c, e], [b, d, f]]) * N; W, H = im.size
    Mi = np.array([[a * N / W, c * N / H, e * N], [b * N / W, d * N / H, f * N]])
    return cv2.warpAffine(np.asarray(im), Mi, (N, N), flags=cv2.INTER_AREA, borderValue=(255, 0, 255))
if __name__ == '__main__':
    from PIL import Image, ImageDraw
    B, KEYS, PT, OUT = sys.argv[1:5]; D = load_D(B); ks = json.load(open(KEYS)); T = json.load(open(PT)); C = json.load(open('config/tableview-photo-class-nov01.json'))
    res = {}
    for k in ks:
        im = mat_full(B, D['mats'][k]['f']); a = np.asarray(im); H, W = a.shape[:2]; note = str(C.get(k, {}).get('note', '')); peel = None
        solid = D['mats'][k]['bn'] == 'Mahjong Register' and note.startswith('peel')
        if note.startswith('peel') and not solid:
            from PIL import ImageDraw as _D
            pm = Image.new('L', (W, H), 0); b = T.get('m', {}).get(k, {}).get('b', [0, 0, 1, 1]); w_, h_ = (b[2] - b[0]) * W, (b[3] - b[1]) * H
            _D.Draw(pm).polygon([(b[0] * W + x * w_, b[1] * H + y * h_) for x, y in T['T2']], fill=255); peel = ndimage.binary_dilation(np.asarray(pm) > 0, iterations=int(.03 * W))
        if note.startswith('peel') and not solid:  # rejected fills: keep the whole top-right (peel) quarter out of the square
            q = np.zeros((H, W), bool); q[:int(H * .58), int(W * .42):] = True; peel = q if peel is None else (peel | q)
        MAN = {'Domino Oxblood': (.47, .42, .72, 'mat on a table with a rack: square on the mat only'), 'El Tigre': (.5, .45, .62, 'mat in a frame: square inside the frame'), 'Pink Rose': (.36, .56, .56, 'brand label under the mat, peel top-right: square on the mat only')}
        nm = D['mats'][k]['n']
        if nm in MAN: cx, cy, kk, why = MAN[nm]; r = centred(W, H, why, cx, cy, kk)
        elif note.startswith('peel') and not solid: r = bbox_corner(a, 'BR')
        elif note in ('edge-rolled', 'banner-partial'): r = bbox_corner(a, 'BL', inset=.07)  # step past the grey shadow beside the mat
        else: r = fit(a, note, solid, peel) or centred(W, H, 'fallback centred')
        res[k] = r
    json.dump(res, open(OUT, 'w'), indent=0)
    import collections; print(collections.Counter(r['kind'] for r in res.values()))
    S = 260; Wn = 7; o = Image.new('RGB', (Wn * S, ((len(ks) + Wn - 1) // Wn) * (S + 14)), 'white'); dr = ImageDraw.Draw(o)
    for i, k in enumerate(ks):
        im = mat_full(B, D['mats'][k]['f']); w = Image.fromarray(warp(im, res[k], S)); x, y = (i % Wn) * S, (i // Wn) * (S + 14); o.paste(w, (x, y))
        dr.text((x + 2, y + S), f"{i} {res[k]['kind'][:4]} f{res[k]['f']} {D['mats'][k]['n'][:22]}", fill='black')
    o.save(OUT.replace('.json', '.jpg'), quality=84)
