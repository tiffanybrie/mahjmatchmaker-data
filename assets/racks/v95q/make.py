"""Build the v95 single-rack cutouts (Tiffany Oct 26 11:35/11:39). Sources = the rack photos already in the v95 build
(real brand photos; HD where present) or the brand's own earlier cutout (Iridescent Opal). Method: key the background
(alpha already present / dark slate luminance key / colour distance from slate), label the racks, keep the LONGEST one,
rotate it level (PCA of its mask), crop. Usage: python3 make.py <dir with racks/<i>.webp dump> """
import sys, os, numpy as np
from PIL import Image
from scipy import ndimage
H = os.path.dirname(os.path.abspath(__file__)) + '/'; REPO = H + '../../../'

def longest(al, a, thr=.35, area=False):
    m = ndimage.binary_opening(al > thr, iterations=2); m = ndimage.binary_closing(m, iterations=3)
    lab, n = ndimage.label(m); best = None
    for j in range(1, n + 1):
        ys, xs = np.nonzero(lab == j)
        if len(xs) < 500: continue
        c = np.cov(np.vstack([xs, ys])); w, v = np.linalg.eigh(c); L = len(xs) if area else np.sqrt(w[-1])
        if best is None or L > best[0]: best = (L, j, v[:, -1])
    _, j, v = best
    keep = ndimage.binary_dilation(lab == j, iterations=3)
    al2 = np.where(keep, al, 0)
    ang = np.degrees(np.arctan2(v[1], v[0]))
    if ang > 90: ang -= 180
    if ang < -90: ang += 180
    o = Image.fromarray(np.dstack([(a * 255).astype(np.uint8), (al2 * 255).astype(np.uint8)]), 'RGBA')
    o = o.rotate(ang, resample=Image.BICUBIC, expand=True)
    return o.crop(o.getbbox())

def load(p):
    im = Image.open(p).convert('RGBA'); x = np.asarray(im).astype(float) / 255; return x[..., :3], x[..., 3]

def key_slate(a, lo=.50, hi=.72):
    lum = a @ [.299, .587, .114]; return np.clip((lum - lo) / (hi - lo), 0, 1)

def key_colour(a, border=40, t0=.10, t1=.22):
    edge = np.concatenate([a[:border].reshape(-1, 3), a[-border:].reshape(-1, 3), a[:, :border].reshape(-1, 3), a[:, -border:].reshape(-1, 3)])
    bg = np.median(edge, 0); d = np.linalg.norm(a - bg, axis=2); return np.clip((d - t0) / (t1 - t0), 0, 1)

def key_white(a, t=.035):
    d = 1 - a.min(2); m = d > t
    m = ndimage.binary_closing(m, iterations=4); m = ndimage.binary_fill_holes(m); m = ndimage.binary_erosion(m, iterations=3)
    return ndimage.gaussian_filter(m.astype(float), 1.0)

def key_sat(a, t0=.12, t1=.25):
    s = a.max(2) - a.min(2); m = np.clip((s - t0) / (t1 - t0), 0, 1)
    mm = ndimage.binary_fill_holes(ndimage.binary_closing(m > .5, iterations=3))
    mm = ndimage.binary_erosion(mm, iterations=2)
    return ndimage.gaussian_filter(mm.astype(float), 1.0)

def unbg(a, al, bg):  # un-premultiply against a flat bg colour so edges don't keep the slate
    return np.clip((a - (1 - al[..., None]) * bg) / np.maximum(al[..., None], .05), 0, 1)

if __name__ == '__main__':
    D = sys.argv[1] + '/racks/'
    jobs = {
        'bambird-white-acrylic': ('50', 'white'),
        'ymi-modern-clear': ('83', 'white'),
        'plm-wavy-white': ('35', 'alpha'),
        'plm-wavy-pink': ('43', 'alpha'),
        'mahjmood-white-wood-scallop': ('22', 'slate'),
        'mahjmood-scalloped-white-clear': ('226', 'alpha'),
        'cmc-clear-acrylic': ('225', 'alpha_fill'),
        'andersruff-rose-pink-pearl': ('205', 'alpha'),
        'middlemain-la-vie-en-rose': ('68', 'alpha'),
        'mahjmood-baby-blue-wood': ('21', 'sat'),
        'mahjmood-double-wood-pink': ('23', 'sat'),
    }
    for name, (i, how) in jobs.items():
        a, al = load(D + i + '.webp')
        if how == 'slate':
            k = key_slate(a); bg = np.median(a[k < .05], 0); a = unbg(a, k, bg); al = k
        elif how == 'colour':
            edge = np.concatenate([a[:40].reshape(-1, 3), a[-40:].reshape(-1, 3)]); bg = np.median(edge, 0)
            k = key_colour(a); a = unbg(a, k, bg); al = k
        elif how == 'alpha_fill':  # glare punched a hole in the brand cutout: fill interior holes only
            m0 = al > .35; holes = ndimage.binary_fill_holes(m0) & ~m0; lab, n = ndimage.label(holes)
            sz = ndimage.sum(holes, lab, range(1, n + 1)); small = np.isin(lab, [j + 1 for j, s in enumerate(sz) if s < 1500])
            al = np.where(small, 1.0, al); a = np.where(small[..., None], ndimage.median_filter(a, size=(25, 25, 1)), a)
        elif how == 'white':
            al = key_white(a)
        elif how == 'sat':
            al = key_sat(a)
        o = longest(al, a, area=(how == 'sat')); o.save(H + name + '.webp', quality=90, method=6); print(name, o.size)

    # Iridescent Opal: Miss Mahjong's own single-rack cutout (assets/racks/cutouts/...-1.png, used on the album cards)
    o = Image.open(REPO + 'assets/racks/card/miss-mahjong-scalloped-iridescent-opal.png').convert('RGBA')
    o = o.crop(o.getbbox()); o.thumbnail((1200, 400)); o.save(H + 'missmahjong-iridescent-opal.webp', quality=92, method=6); print('opal', o.size)
    # Bespoke Bright White reads grey: lift the whites (levels), keep its alpha
    a, al = load(D + '60.webp'); a = np.clip(a / .86, 0, 1) ** .8
    Image.fromarray(np.dstack([(a * 255).astype(np.uint8), (al * 255).astype(np.uint8)]), 'RGBA').save(H + 'bespoke-bright-white.webp', quality=90, method=6)
