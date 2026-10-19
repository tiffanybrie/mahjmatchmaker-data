"""Exact measured colors (Tiffany, Oct 19, 3:17-3:21am; docs 76 + 77): "never all the greens", not even all the "olives".
A yellower olive and a deeper olive share a name but are different colors, so layer picks and the color finder work from the
MEASURED color (CIELAB, compared with CIEDE2000), never from a color word.

mat_palette(path)  -> up to 5 [hex, weight] from the PATTERN area (a plain/dotted center panel barely counts, like families.py)
tile_palette(path) -> clusters of the tile photo with white faces/background dropped: back = biggest colored cluster.
dE(hexA, hexB)     -> CIEDE2000 distance (about 2 = same to the eye, 10 = clearly different, 25+ = different color).
"""
import numpy as np
from PIL import Image
from skimage.color import rgb2lab, deltaE_ciede2000
from sklearn.cluster import KMeans


def hex2rgb(h):
    h = h.lstrip('#'); return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], float) / 255


def rgb2hex(c):
    c = np.clip(np.round(np.asarray(c) * 255), 0, 255).astype(int); return '#%02x%02x%02x' % tuple(c)


def lab(h):
    return rgb2lab(hex2rgb(h).reshape(1, 1, 3)).reshape(3)


def dE(a, b):
    return float(deltaE_ciede2000(lab(a).reshape(1, 3), lab(b).reshape(1, 3))[0])


def _km(px, w, k):
    k = max(1, min(k, len(px)))
    km = KMeans(n_clusters=k, n_init=3, random_state=0).fit(rgb2lab(px.reshape(-1, 1, 3)).reshape(-1, 3), sample_weight=w)
    out = []
    for i in range(k):
        m = km.labels_ == i
        if not m.any(): continue
        c = np.average(px[m], axis=0, weights=w[m]); out.append([rgb2hex(c), float(w[m].sum())])
    t = sum(x[1] for x in out) or 1
    return sorted([[h, round(v / t, 3)] for h, v in out], key=lambda x: -x[1])


def mat_palette(path, N=72, k=6, keep=5):
    a = np.asarray(Image.open(path).convert('RGB').resize((N, N))).astype(float) / 255
    w = np.ones((N, N)); c0, c1 = int(N * .25), int(N * .75)
    cen = a[c0:c1, c0:c1]
    w[c0:c1, c0:c1] = 0.1 if cen.reshape(-1, 3).std(0).mean() < 0.07 else 0.45
    pal = _km(a.reshape(-1, 3), w.ravel(), k)
    return [p for p in pal if p[1] >= 0.04][:keep]


def tile_palette(path, N=96, k=8):
    """Drop white/ivory faces, white backgrounds and grey shadows/table (low chroma); the biggest remaining cluster is
    usually the back. Small clusters (3%+) are kept so thin layers (Dandy's olive) survive."""
    a = np.asarray(Image.open(path).convert('RGB').resize((N, N))).astype(float) / 255
    px = a.reshape(-1, 3); L = rgb2lab(px.reshape(-1, 1, 3)).reshape(-1, 3)
    chroma = np.hypot(L[:, 1], L[:, 2])
    keep = ~((L[:, 0] > 86) & (chroma < 14)) & ~(chroma < 9)  # white/ivory faces, backgrounds, grey shadows
    if keep.sum() < 60: keep = ~((L[:, 0] > 86) & (chroma < 14))  # a truly neutral set (ivory/black tiles)
    if keep.sum() < 40: keep = np.ones(len(px), bool)
    return [p for p in _km(px[keep], np.ones(keep.sum()), k) if p[1] >= 0.03]


def nearest(target_hex, palette):
    """Smallest CIEDE2000 distance from target to any palette color whose weight is >= 6% (a real amount)."""
    ds = [dE(target_hex, h) for h, w in palette if w >= 0.06]
    return min(ds) if ds else 99.0
