"""Remove white halos / white background left inside rack cutouts (Oct 25 21:42 rack audit on a navy background).
defringe(im, whiteish_rack) -> RGBA. Background remnants are near-white pixels connected to the transparent area
(or big flat white holes enclosed by the racks, e.g. the square between crossed racks). White/clear racks use a stricter
threshold so the rack body (shaded, < ~245) survives."""
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
def defringe(im, whiteish_rack=False, holes=None):
    a = np.asarray(im.convert('RGBA')).astype(float); rgb = a[..., :3]; al = a[..., 3]
    mn = rgb.min(2); sp = rgb.max(2) - mn
    thr = 247 if whiteish_rack else 205
    wh = (mn >= thr) & (sp <= (18 if whiteish_rack else 40)) & (al > 0)
    tr = al < 10
    lab, n = ndimage.label(wh | tr, structure=np.ones((3, 3)))
    touch = np.unique(lab[tr]); kill = np.isin(lab, touch[touch > 0]) & wh
    if holes is None: holes = not whiteish_rack
    if holes:  # big enclosed flat white holes
        hl, hn = ndimage.label(wh & ~kill)
        if hn:
            sz = ndimage.sum(np.ones_like(al), hl, range(1, hn + 1)); op = (al > 128).sum()
            for j, s in enumerate(sz, 1):
                if s > 0.002 * op and mn[hl == j].mean() > (246 if whiteish_rack else 228) and sp[hl == j].mean() < 12: kill |= hl == j
    if holes and whiteish_rack:  # white/clear sets: a flat white gap fully enclosed by racks (never touching the outside)
        near = ndimage.binary_dilation(tr | kill, iterations=3)
        cl, cn = ndimage.label((mn >= 228) & (sp <= 16) & (al > 0))
        op = (al > 128).sum()
        for j in range(1, cn + 1):
            c = cl == j
            if c.sum() > 0.001 * op and not (c & near).any(): kill |= c
    al = np.where(kill, 0, al)
    m = ndimage.binary_opening(al > 128, iterations=1); m = ndimage.binary_erosion(m, iterations=1)
    keep = ndimage.binary_dilation(m, iterations=1)
    al = np.where(keep, al, 0)
    o = Image.fromarray(np.dstack([rgb, al]).astype(np.uint8), 'RGBA')
    A = o.getchannel('A').filter(ImageFilter.GaussianBlur(0.6)); o.putalpha(A)
    return o
