"""Mahjong Black Acrylic Racks and Scallop Pushers (Bamlet's) Table cut, QA Nov 2 re-check: no toothy top, no dark patch,
no blue end. Source: the brand's top-down photo of 4 black racks on white (racks-src/qa-nov02/bamlets_black_acrylic_brand.jpg);
rack #2 is the cleanest (no reflection patch). Dark-pixel mask -> top/bottom edges smoothed per column -> squared ends ->
glare/blue reflections painted from the nearest black (the left magnet dot is kept). Out: racks-src/qa-nov02/black.png"""
import pathlib, numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
D = pathlib.Path(__file__).resolve().parents[2] / 'assets/table-view/racks-src/qa-nov02'
im = Image.open(D / 'bamlets_black_acrylic_brand.jpg').convert('RGB').crop((304, 140, 462, 1015)).rotate(-90, expand=True)
a = np.asarray(im).astype(float); L = a.mean(2)
m = ndimage.binary_closing(L < 120, iterations=2); lab, n = ndimage.label(m); sz = ndimage.sum(m, lab, range(1, n + 1))
m = ndimage.binary_fill_holes(lab == (np.argmax(sz) + 1)); H, W = m.shape
top = np.array([np.where(m[:, x])[0].min() if m[:, x].any() else H for x in range(W)], float)
bot = np.array([np.where(m[:, x])[0].max() if m[:, x].any() else -1 for x in range(W)], float)
c = m.sum(0); cs = np.where(c >= .85 * c.max())[0]; x0, x1 = cs.min() + 2, cs.max() - 2
ts = ndimage.gaussian_filter1d(ndimage.median_filter(top, 11), 2); bs = ndimage.gaussian_filter1d(ndimage.median_filter(bot, 11), 2)
yy = np.arange(H)[:, None]; m = (yy >= ts[None, :] + 1) & (yy <= bs[None, :]); m[:, :x0] = False; m[:, x1 + 1:] = False
keep = np.zeros_like(m); lb, nb = ndimage.label((L > 45) & m)
for i, sl in enumerate(ndimage.find_objects(lb)):
    h, w = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
    if 6 <= h <= 16 and 6 <= w <= 16 and abs(h - w) <= 3 and sl[1].start < W * .15: keep[sl] |= lb[sl] == i + 1
bad = ndimage.binary_dilation(m & ((L > 45) | ((a[..., 2] - np.maximum(a[..., 0], a[..., 1]) > 5) & (L > 6))) & ~ndimage.binary_dilation(keep, iterations=1), iterations=1) & m
good = m & ~bad  # every other pixel (glare, blue, and the soft edge just outside the rack) takes the colour of the nearest clean black pixel
_, idx = ndimage.distance_transform_edt(~good, return_indices=True); rgb = a[..., :3][idx[0], idx[1]]
rgb[(rgb[..., 2] - np.maximum(rgb[..., 0], rgb[..., 1]) > 5)] = np.median(a[good & (L < 30)], 0)  # last blue specks on the scalloped edge -> rack black
al = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(.6)))
o = Image.fromarray(np.dstack([rgb, al]).astype(np.uint8), 'RGBA'); ys, xs = np.where(al > 20)
o = o.crop((xs.min() - 2, ys.min() - 2, xs.max() + 3, ys.max() + 3)); o.thumbnail((1000, 1000)); o.save(D / 'black.png'); print('black acrylic', o.size, 'painted', int(bad.sum()))
