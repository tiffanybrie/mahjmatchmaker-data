#!/usr/bin/env python3
"""Table view mock v6 (Oct 28, Tiffany 2:35pm: no white halo round the tiles on a dark mat; 20-inch racks; real-photo mats only).
Based on v5 (Oct 27, after Tiffany's 5:58/5:59pm notes).

- Mat = a PHOTO (or, when no overhead photo exists, the art file + photo treatment, labelled so).
- 4 racks on the mat; each wall of 19 sits right against ITS rack, centred on it
  (no closed square, corners don't touch).
- Tile backs = a REAL photo of one tile back (cut out once), repeated with tiny
  jitter, contact + double-stack shadow. Optional luminance-preserving recolour.

usage: walls_v5.py cfg.json out_prefix      -> out_prefix-walls.jpg, -nowalls.jpg, -closeup.jpg
"""
import json, sys, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

cfg = json.load(open(sys.argv[1])); outp = sys.argv[2]
rnd = random.Random(7)

mat = Image.open(cfg['mat']).convert('RGB')
N = cfg.get('mat_px', 2000)
mat = mat.resize((N, N), Image.LANCZOS)
PPI = N / cfg['mat_in']

def photo_treat(im):
    """art file -> looks shot: fine neoprene grain, soft light falloff, faint sheen."""
    a = np.asarray(im, float)
    h, w = a.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w] / max(h, w)
    fall = 1.04 - 0.16 * ((xx - 0.38) ** 2 + (yy - 0.32) ** 2) ** 0.8 * 2.2   # light from upper-left
    sheen = 0.06 * np.exp(-(((xx - 0.30) / 0.30) ** 2 + ((yy - 0.25) / 0.22) ** 2))
    rng = np.random.default_rng(3)
    g = rng.normal(0, 1, (h, w)); g = np.asarray(Image.fromarray(((g * 18) + 128).clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8)), float) - 128
    a = a * fall[..., None] + (255 - a) * sheen[..., None] + g[..., None] * 0.55
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

if cfg.get('treat_art'):
    mat = photo_treat(mat)

# ---- tile back sprite from a real photo ----
back = Image.open(cfg['back_photo']).convert('RGBA')
back = back.crop(back.split()[3].point(lambda v: 255 if v > 128 else 0).getbbox())   # tight to the tile edge

# v6 DEFRINGE (Tiffany Oct 28 2:35pm: 'fake highlight' halo round every tile on the dark mat).
# The cut-out's outer rim carries the photo's pale studio rim + white-background spill. In an edge band we
# rebuild the colour from the tile's own interior colour (keeping only a mild shading), then pull the alpha
# edge in a little and feather it, so no pale/white ring is left to show on a dark mat.
import scipy.ndimage as ndi
_a = np.asarray(back, float); _rgb = _a[..., :3].copy(); _al = _a[..., 3]
_solid = _al > 128
_dist = ndi.distance_transform_edt(np.pad(_solid, 2))[2:-2, 2:-2]   # px from the cut edge (padded: the image border IS the tile edge)
BAND = cfg.get('defringe_px', 0.03) * max(back.size)           # ~ edge roll-off width
_core = _dist > BAND * 2.0
_Lp = _rgb @ [0.299, 0.587, 0.114]
_Lc = np.median(_Lp[_core]); _cc = np.median(_rgb[_core], axis=0)
_w = np.clip((1.6 * BAND - _dist) / (0.6 * BAND), 0, 1)[..., None]   # fully rebuilt out to BAND, then fades over 0.6 BAND
_shade = np.clip(_Lp / _Lc, 0.70, cfg.get('rim_max', 1.0))[..., None] * (1 - 0.18 * _w)   # rim slightly darker, never brighter
_rgb = _rgb * (1 - _w) + (_cc[None, None, :] * _shade) * _w
_er = ndi.binary_erosion(np.pad(_solid, 4), iterations=cfg.get('erode_px', 3))[4:-4, 4:-4]
_al2 = np.asarray(Image.fromarray((_er * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.0)), float)
back = Image.fromarray(np.dstack([np.clip(_rgb, 0, 255), np.minimum(_al, _al2)]).astype(np.uint8), 'RGBA')
_EDGE_W = np.clip((3.2 * BAND - _dist) / (1.0 * BAND), 0, 1)   # no recolour highlights near the rim either
if cfg.get('recolour'):
    tgt = np.array(cfg['recolour'], float)
    a = np.asarray(back, float); rgb = a[..., :3]; al = a[..., 3]
    L = rgb @ [0.299, 0.587, 0.114]
    Lm = np.median(L[al > 200])
    rel = L / Lm
    base = tgt[None, None, :] * np.clip(rel, 0, 3)[..., None] ** cfg.get('recolour_gamma', 1.6)
    hi = np.clip((rel - 1.06) / 0.25, 0, 1) ** 1.2 * (1 - _EDGE_W)
    rel = np.where(_EDGE_W > 0, np.minimum(rel, 1.0 + 0.06 * (1 - _EDGE_W)), rel)   # rim never lighter than the body
    base = tgt[None, None, :] * np.clip(rel, 0, 3)[..., None] ** cfg.get('recolour_gamma', 1.6)     # keep the photo's own highlights, but never on the rim (v6)
    out = base + (255 - base) * (hi * cfg.get('recolour_hi', 0.85))[..., None]
    back = Image.fromarray(np.dstack([np.clip(out, 0, 255), al]).astype(np.uint8), 'RGBA')

TW, TH = cfg['tile_in'][:2]
def sprite(vertical_wall):
    w, h = round(TW * PPI), round(TH * PPI)
    s = back.resize((w, h), Image.LANCZOS)
    if vertical_wall:                       # wall runs up/down: long side horizontal; transpose keeps light top-left
        s = s.transpose(Image.TRANSPOSE)
    return s

# ---- racks ----
rack = Image.open(cfg['rack']).convert('RGBA')
RL = cfg.get('rack_in', 22.5)
RD = min(max(RL * rack.height / rack.width, 2.2), 2.9)
rk = rack.resize((round(RL * PPI), round(RD * PPI)), Image.LANCZOS)
E_ = cfg.get('rack_edge_in', 1.4); EDG = E_ if isinstance(E_, dict) else {k: E_ for k in 'NSEW'}
OFF = cfg.get('rack_shift_in', {})
c = N / 2
racks = []   # (image, x, y, side)
for side, ang in (('S', 0), ('N', 180), ('E', 90), ('W', 270)):
    r = rk.rotate(ang, expand=True)
    edge = EDG[side] * PPI; sh_ = OFF.get(side, 0) * PPI
    if side == 'S': x, y = c - r.width / 2 + sh_, N - edge - r.height
    if side == 'N': x, y = c - r.width / 2 + sh_, edge
    if side == 'E': x, y = N - edge - r.width, c - r.height / 2 + sh_
    if side == 'W': x, y = edge, c - r.height / 2 + sh_
    racks.append((r, int(x), int(y), side))

def inner(side):
    for r, x, y, s in racks:
        if s == side:
            return {'S': y, 'N': y + r.height, 'E': x, 'W': x + r.width}[side]

# ---- walls: 19 stacks right against each rack, centred on it ----
gap = cfg.get('wall_gap_in', 0.06) * PPI
L19 = 19 * TW * PPI
tiles = []   # (x, y, vertical)
for side in 'NSEW':
    vert = side in 'EW'
    for i in range(19):
        rc = [(x_ + r_.width / 2, y_ + r_.height / 2) for r_, x_, y_, s_ in racks if s_ == side][0]
        along = (rc[1] if vert else rc[0]) - L19 / 2 + i * TW * PPI * cfg.get('pitch', 1.0)
        if side == 'S': x, y = along, inner('S') - gap - TH * PPI
        if side == 'N': x, y = along, inner('N') + gap
        if side == 'E': x, y = inner('E') - gap - TH * PPI, along
        if side == 'W': x, y = inner('W') + gap, along
        tiles.append((x, y, vert))

def compose(with_walls):
    can = mat.copy().convert('RGBA')
    # rack shadows
    sh = Image.new('L', (N, N), 0); sd = ImageDraw.Draw(sh)
    for r, x, y, s in racks:
        a = r.split()[3]
        sh.paste(a.point(lambda v: 150 if v > 40 else 0), (x + int(0.10 * PPI), y + int(0.16 * PPI)), a)
    if with_walls:
        for x, y, v in tiles:
            w, h = (TH, TW) if v else (TW, TH)
            # double stack: soft cast shadow toward lower-right + tight contact shadow
            sd.rounded_rectangle([x + 0.06 * PPI, y + 0.10 * PPI, x + (w + 0.30) * PPI, y + (h + 0.32) * PPI], int(0.14 * PPI), fill=120)
    sh = sh.filter(ImageFilter.GaussianBlur(0.20 * PPI))
    can = Image.composite(Image.new('RGBA', (N, N), (12, 10, 10, 255)), can, sh.point(lambda v: int(v * 0.55)))
    if with_walls:
        ao = Image.new('L', (N, N), 0); ad = ImageDraw.Draw(ao)
        for k0 in range(0, len(tiles), 19):          # one continuous seam shadow per wall
            xs_ = [t[0] for t in tiles[k0:k0 + 19]]; ys_ = [t[1] for t in tiles[k0:k0 + 19]]; v = tiles[k0][2]
            w, h = (TH, TW) if v else (TW, TH)
            ad.rounded_rectangle([min(xs_) + 0.03 * PPI, min(ys_) + 0.03 * PPI, max(xs_) + (w - 0.03) * PPI, max(ys_) + (h - 0.03) * PPI], int(0.10 * PPI), fill=230)
        ao = ao.filter(ImageFilter.GaussianBlur(0.05 * PPI))
        can = Image.composite(Image.new('RGBA', (N, N), (8, 6, 6, 255)), can, ao.point(lambda v: int(v * 0.62)))
    for r, x, y, s in racks:
        can.alpha_composite(r, (x, y))
    if with_walls:
        cache = {}
        for x, y, v in tiles:
            if v not in cache: cache[v] = sprite(v)
            spr = cache[v]
            jit = spr.rotate(rnd.uniform(-0.35, 0.35), resample=Image.BICUBIC, expand=True)
            if cfg.get('vary', 0.03):
                f = 1 + rnd.uniform(-1, 1) * cfg.get('vary', 0.03)
                r_, g_, b_, a_ = jit.split()
                jit = Image.merge('RGBA', [ch.point(lambda p, f=f: min(255, int(p * f))) for ch in (r_, g_, b_)] + [a_])
            ox = x + rnd.uniform(-0.012, 0.012) * PPI - (jit.width - spr.width) / 2
            oy = y + rnd.uniform(-0.012, 0.012) * PPI - (jit.height - spr.height) / 2
            can.alpha_composite(jit, (int(round(ox)), int(round(oy))))
    return can.convert('RGB')

def frame(img):
    F = cfg.get('out_px', 1400)
    im = img.resize((F, F), Image.LANCZOS)
    pad = int(F * 0.035)
    fr = Image.new('RGB', (F + 2 * pad, F + 2 * pad + int(F * 0.11)), (250, 246, 240))
    fr.paste(im, (pad, pad))
    tp = Image.open(cfg['tiles_photo']).convert('RGB')
    cd = int(F * 0.25); s = min(tp.size)
    tp = tp.crop(((tp.width - s) // 2, (tp.height - s) // 2, (tp.width + s) // 2, (tp.height + s) // 2)).resize((cd, cd), Image.LANCZOS)
    cm = Image.new('L', (cd, cd), 0); ImageDraw.Draw(cm).ellipse([0, 0, cd - 1, cd - 1], fill=255)
    ox = fr.width - cd - int(pad * 0.8); oy = pad + F - int(cd * 0.82)
    shd = Image.new('L', fr.size, 0); ImageDraw.Draw(shd).ellipse([ox + 6, oy + 12, ox + cd + 6, oy + cd + 12], fill=110)
    fr = Image.composite(Image.new('RGB', fr.size, (40, 30, 30)), fr, shd.filter(ImageFilter.GaussianBlur(14)))
    ring = int(cd * 0.035)
    ImageDraw.Draw(fr).ellipse([ox - ring, oy - ring, ox + cd + ring, oy + cd + ring], fill=(255, 255, 255))
    fr.paste(tp, (ox, oy), cm)
    try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf', int(F * 0.022))
    except Exception: f = ImageFont.load_default()
    for n, line in enumerate(cfg.get('label', '').split('\n')):
        ImageDraw.Draw(fr).text((pad, F + pad + int(F * 0.018) + n * int(F * 0.032)), line, fill=(70, 50, 50), font=f)
    return fr

on = compose(True); off = compose(False)
frame(on).save(outp + '-walls.jpg', quality=92)
frame(off).save(outp + '-nowalls.jpg', quality=92)
# close-up: bottom wall corner + rack, at native resolution
cx0 = int(c - L19 / 2 - 1.0 * PPI); cy0 = int(inner('S') - 4.0 * PPI)
cl = on.crop((cx0, cy0, cx0 + int(9 * PPI), cy0 + int(7.5 * PPI)))
cl.resize((cl.width * 1400 // max(cl.size), cl.height * 1400 // max(cl.size)), Image.LANCZOS).save(outp + '-closeup.jpg', quality=92)
print('ok', outp)
