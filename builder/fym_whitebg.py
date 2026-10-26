"""Put a product shot taken on BLACK onto clean WHITE (Mahjong Studios piles, Oct 26). Background = near-black region
connected to the border + enclosed near-black gaps between tiles; soft 1-2px edge with the black un-premultiplied out
(no dark halo). Real photo pixels only; nothing is painted in.  to_white(im) -> RGB image."""
import numpy as np
from PIL import Image
from scipy import ndimage

def to_white(im, t_bg=42, t_hole=20, hole_min=400, island_min=0.002):
    a = np.asarray(im.convert('RGB')).astype(float); mx = a.max(2)
    dark = mx < t_bg; lab, n = ndimage.label(dark)
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(edge))
    lab2, n2 = ndimage.label((mx < t_hole) & ~bg)               # enclosed black gaps between tiles
    if n2:
        sz = ndimage.sum(np.ones_like(mx), lab2, range(1, n2 + 1))
        sd = ndimage.standard_deviation(mx, lab2, range(1, n2 + 1))  # flat black gap, not ink or a dark tile side
        bg |= np.isin(lab2, [i + 1 for i in range(n2) if sz[i] >= hole_min and sd[i] < 4])
    bg = ndimage.binary_opening(bg, iterations=1)
    fg = ~bg; lf, nf = ndimage.label(fg)                               # drop small floating specks
    if nf > 1:
        fs = ndimage.sum(fg, lf, range(1, nf + 1))
        fg &= np.isin(lf, [i + 1 for i, s in enumerate(fs) if s >= island_min * fg.size])
        bg = ~fg
    band = ndimage.binary_dilation(bg, iterations=2) & fg            # soft edge only at the boundary
    al = np.ones_like(mx); al[bg] = 0
    al[band] = np.clip((mx[band] - 12) / 70, 0, 1)
    col = a / 255
    col[band] = np.clip(col[band] / np.maximum(al[band][:, None], 1e-3), 0, 1)
    out = col * al[..., None] + (1 - al[..., None])
    return Image.fromarray((out * 255).astype(np.uint8))
