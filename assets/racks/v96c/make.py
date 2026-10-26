"""v96 rack cutouts (QA v95 item 2c). Real brand photos only. Background keyed by flood fill from the border (near-white
studio backgrounds) or by saturation (TdT racks on blue damask). Keep the LONGEST rack (or the whole stack where racks are
stacked flat and touch), level it, crop. Clear acrylic keeps a soft translucent body (alpha floor) so it reads as clear on
cream. Usage: python3 make.py <src_dir> <out_dir>"""
import sys, os, numpy as np
from PIL import Image
from scipy import ndimage

def load(p, maxw=1400):
    im = Image.open(p).convert('RGB')
    if im.width > maxw: im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    return np.asarray(im).astype(float) / 255

def flood_bg(a, tol=.045, b=6):
    edge = np.concatenate([a[:b].reshape(-1, 3), a[-b:].reshape(-1, 3), a[:, :b].reshape(-1, 3), a[:, -b:].reshape(-1, 3)])
    bg = np.median(edge, 0)
    # local background varies (vignette): compare to a heavily blurred bg estimate too
    d = np.linalg.norm(a - bg, axis=2)
    near = d < tol
    lab, n = ndimage.label(near)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bgm = np.isin(lab, list(border))
    return bgm, d, bg

def sat_bg(a, t=.10):
    s = a.max(2) - a.min(2); return s > t, s

def pick(fg, mode):
    it = 2 if min(fg.shape) > 300 else 1
    fg = ndimage.binary_opening(fg, iterations=it); fg = ndimage.binary_closing(fg, iterations=2 * it)
    fg = ndimage.binary_fill_holes(fg)
    lab, n = ndimage.label(fg); best = None
    for j in range(1, n + 1):
        ys, xs = np.nonzero(lab == j)
        if len(xs) < max(200, fg.size * .002): continue
        c = np.cov(np.vstack([xs, ys])); w, v = np.linalg.eigh(c)
        L = len(xs) if mode == 'area' else np.sqrt(w[-1])
        if best is None or L > best[0]: best = (L, j, v[:, -1])
    if best is None:
        ys, xs = np.nonzero(fg); c = np.cov(np.vstack([xs, ys])); w, v = np.linalg.eigh(c); return fg, v[:, -1]
    _, j, v = best
    return lab == j, v

def finish(a, m, v, clear=False, d=None, level=True, floor=.42):
    al = ndimage.gaussian_filter(m.astype(float), 1.2)
    if clear and d is not None:
        body = np.clip(floor + d * 6, floor, 1.0)       # translucent body, edges/details stay strong
        al = al * body
    o = Image.fromarray(np.dstack([(a * 255).astype(np.uint8), (np.clip(al, 0, 1) * 255).astype(np.uint8)]), 'RGBA')
    if level:
        ang = np.degrees(np.arctan2(v[1], v[0]))
        if ang > 90: ang -= 180
        if ang < -90: ang += 180
        if abs(ang) > .4: o = o.rotate(ang, resample=Image.BICUBIC, expand=True)
    return o.crop(o.getbbox())

JOBS = {  # name: (source, method, options)
    'omm-clear-acrylic':        ('omm_full.jpg', 'flood', dict(clear=True, mode='len')),
    'missmahjong-clear-scallop':('miss_full.png', 'flood', dict(clear=True, mode='len')),
    'tdt-dove-white':           ('tdt_full.jpg', 'sat', dict(mode='len')),
    'mfm-clear':                ('cur/07.png', 'flood', dict(clear=True, mode='area', level=False)),
    'mfm-bright-white':         ('cur/08.png', 'flood', dict(mode='area', level=False, tol=.02)),
    'mfm-pearl-white':          ('cur/09.png', 'flood', dict(mode='area', level=False, tol=.03)),
    'virora-white-magnetic':    ('cur/10.png', 'flood', dict(mode='area', level=False, tol=.02)),
    'mahjongrow-white':         ('cur/11.png', 'flood', dict(mode='area', level=False, tol=.02)),
    'register-ivory-oyster':    ('cur/12.png', 'flood', dict(mode='area', level=False, tol=.03)),
    'bespoke-crystal-clear':    ('cur/13.png', 'flood', dict(clear=True, mode='area', level=False)),
    'bam-white-acrylic':        ('cur/14.png', 'flood', dict(mode='area', level=False, tol=.03)),
    'bam-clear-scallop':        ('cur/15.png', 'flood', dict(clear=True, mode='area', level=False, tol=.03)),
}
if __name__ == '__main__':
    S, O = sys.argv[1], sys.argv[2]; os.makedirs(O, exist_ok=True)
    only = sys.argv[3:]
    for name, (src, how, opt) in JOBS.items():
        if only and name not in only: continue
        a = load(os.path.join(S, src))
        if how == 'flood':
            bgm, d, bg = flood_bg(a, tol=opt.get('tol', .045)); fg = ~bgm
        else:
            fg, d = sat_bg(a); fg = ~fg; d = None
        m, v = pick(fg, opt.get('mode', 'len'))
        o = finish(a, m, v, clear=opt.get('clear', False), d=d if how == 'flood' else None, level=opt.get('level', True))
        if o.width > 1000: o = o.resize((1000, round(o.height * 1000 / o.width)), Image.LANCZOS)
        o.save(os.path.join(O, name + '.webp'), quality=90, method=6); print(name, o.size)
