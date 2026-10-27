#!/usr/bin/env python3
"""Table-view mock (Oct 27): mat + 4 double-stacked walls skinned from a tile set's
back + layer colours, racks at the edges, tile photo circle bottom-right.

usage: walls_mock.py config.json out.jpg
config: {mat, rack, tiles_photo, back:[r,g,b], layers:[[r,g,b],...] (top->bottom, incl. back),
         layer_frac:[...], tile_in:[w,h,t], mat_in:32}
"""
import json, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

cfg = json.load(open(sys.argv[1])); out = sys.argv[2]
SS = 2                      # supersample
PPI = 46 * SS               # px per inch
MAT_IN = cfg.get('mat_in', 32)
W = int(MAT_IN * PPI)
TW, TH, TT = cfg.get('tile_in', [0.97, 1.33, 0.66])   # width, length, thickness (in)
K = 0  # how much of the front side shows (0 = straight down)

mat = Image.open(cfg['mat']).convert('RGB').resize((W, W), Image.LANCZOS)
canvas = mat.copy()

def shade(rgb, f):
    return tuple(int(max(0, min(255, c * f))) for c in rgb)

def mix(a, b, t):
    return tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3))

back = tuple(cfg['back'])
layers = [tuple(c) for c in cfg['layers']]
frac = cfg['layer_frac']

# ---- one tile sprite: AERIAL view of the back only (Tiffany 5:53pm: no sides) ----
P = cfg.get('profile', {})
RAD = P.get('corner', 0.16)      # corner radius as share of tile width
BEV = P.get('bevel', 0.14)       # how far the rounded edge rolls off (share of half-size); small = squared off
GLOSS = P.get('gloss', 0.25)     # broad sheen
SPEC = P.get('spec', 0.0)        # crisp window-light reflection (glossy acrylic)
def tile_sprite(wpx, hpx, rot):
    yy, xx = np.mgrid[0:hpx, 0:wpx].astype(float)
    # distance to edge in px, normalised by the short half-size
    half = min(wpx, hpx) / 2
    de = np.minimum.reduce([xx, wpx - 1 - xx, yy, hpx - 1 - yy]) / half
    roll = np.clip(1 - de / BEV, 0, 1) ** 1.6            # 1 at the very edge, 0 on the flat top
    nx = xx / (wpx - 1) * 2 - 1; ny = yy / (hpx - 1) * 2 - 1
    # which way the edge faces: lit from top-left
    facing = np.where(np.abs(nx) * hpx > np.abs(ny) * wpx, np.sign(nx), np.sign(ny))
    light = 1.0 - 0.05 * (nx + ny) / 2
    light = light - roll * (0.30 + 0.22 * facing) + roll * 0.06 * (facing < 0)
    rgb = np.array(back, float)[None, None, :] * light[..., None]
    # broad sheen toward top-left
    g = np.exp(-(((nx + 0.45) / 0.9) ** 2 + ((ny + 0.55) / 0.8) ** 2))
    rgb = rgb + (255 - rgb) * (GLOSS * g)[..., None]
    if SPEC:
        # soft-edged window reflection band (same direction on every tile, like one light over the table)
        u = (xx + yy * 0.35) / (wpx + hpx * 0.35)        # diagonal coordinate
        band = np.clip(1 - np.abs(u - 0.30) / 0.10, 0, 1) ** 2 * (de > BEV * 0.6)
        rgb = rgb + (255 - rgb) * (SPEC * band)[..., None]
        # thin bright lip on the lit edges
        lip = np.clip(1 - np.abs(de - BEV * 0.55) / (BEV * 0.25 + 1e-6), 0, 1) * (facing < 0)
        rgb = rgb + (255 - rgb) * (0.35 * SPEC * lip)[..., None]
    rgb = np.clip(rgb, 0, 255).astype(np.uint8)
    im = Image.fromarray(np.dstack([rgb, np.full((hpx, wpx), 255, np.uint8)]), 'RGBA')
    m = Image.new('L', (wpx, hpx), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, wpx - 1, hpx - 1], int(min(wpx, hpx) * RAD), fill=255)
    im.putalpha(m)
    ImageDraw.Draw(im).rounded_rectangle([0, 0, wpx - 1, hpx - 1], int(min(wpx, hpx) * RAD), outline=shade(back, P.get('edge_dark', 0.65)) + (200,), width=max(1, SS))
    return im

# ---- wall geometry (pinwheel square, each wall 19 stacks) ----
L = 19 * TW; D = TH
S = L + D                      # outer square side (in)
cx = cy = W / 2
tiles = []                     # (x_in, y_in, w_in, h_in) top-face rects, centred coords
# south wall: tiles side by side along x, long side along y
for i in range(19):
    x = -S / 2 + i * TW; y = S / 2 - D
    tiles.append((x, y, TW, TH, 0))
def rot(t, k):
    x, y, w, h, _ = t
    pts = [(x, y), (x + w, y + h)]
    for _ in range(k):
        pts = [(-py, px) for px, py in pts]
    xs = sorted(p[0] for p in pts); ys = sorted(p[1] for p in pts)
    return (xs[0], ys[0], xs[1] - xs[0], ys[1] - ys[0], k)
allt = []
for k in range(4):
    allt += [rot(t, k) for t in tiles]
lift = 2 * TT * PPI * K        # top faces drawn raised by the stack height

# shadow layer
sh = Image.new('L', (W, W), 0); sd = ImageDraw.Draw(sh)
for x, y, w, h, _ in allt:
    px = cx + x * PPI; py = cy + y * PPI - lift
    sd.rounded_rectangle([px + 0.06 * PPI, py + 0.10 * PPI, px + w * PPI + 0.30 * PPI, py + h * PPI + 0.38 * PPI], int(0.15 * PPI), fill=170)
sh = sh.filter(ImageFilter.GaussianBlur(0.22 * PPI))
canvas = Image.composite(Image.new('RGB', (W, W), (10, 8, 8)), canvas, sh.point(lambda v: int(v * 0.42)))
canvas = canvas.convert('RGBA')

# racks (outside each wall)
rack = Image.open(cfg['rack']).convert('RGBA')
RL = cfg.get('rack_in', 22.0)
RD = min(max(RL * rack.height / rack.width, 2.0), 2.8)      # rack depth on the table (in)
rk = rack.resize((int(RL * PPI), int(RD * PPI)), Image.LANCZOS)
EDGE = cfg.get('rack_edge_in', 1.0) * PPI                    # racks sit near the mat edge
gap = (W / 2 - EDGE - RD * PPI) - S / 2 * PPI
for k, (ang) in enumerate([0, 90, 180, 270]):
    r = rk.rotate(ang, expand=True)
    if ang == 0:   pos = (cx - r.width / 2, cy + S / 2 * PPI + gap)
    if ang == 180: pos = (cx - r.width / 2, cy - S / 2 * PPI - gap - r.height - lift)
    if ang == 90:  pos = (cx + S / 2 * PPI + gap, cy - r.height / 2 - lift / 2)
    if ang == 270: pos = (cx - S / 2 * PPI - gap - r.width, cy - r.height / 2 - lift / 2)
    if ang in (90, 270):  # B&B rack lip faces the player
        pass
    canvas.alpha_composite(r, (int(pos[0]), int(pos[1])))

# tiles back-to-front (north first)
cache = {}
for x, y, w, h, k in sorted(allt, key=lambda t: t[1]):
    key = (round(w * PPI), round(h * PPI))
    if key not in cache: cache[key] = tile_sprite(*key, k)
    g = cfg.get('gap_in', 0.025) * PPI
    spr = cache[key].resize((max(1, key[0] - int(g)), max(1, key[1] - int(g))), Image.LANCZOS)
    canvas.alpha_composite(spr, (int(round(cx + x * PPI + g / 2)), int(round(cy + y * PPI + g / 2))))

# one light over the table: a soft reflection that runs continuously across the glossy tile backs
SPECG = P.get('table_spec', 0.0)
if SPECG:
    fm = Image.new('L', (W, W), 0); fd = ImageDraw.Draw(fm)
    for x, y, w, h, k in allt:
        px = cx + x * PPI; py = cy + y * PPI; ins = min(w, h) * PPI * BEV * 0.45
        fd.rounded_rectangle([px + ins, py + ins, px + w * PPI - ins, py + h * PPI - ins], int(min(w, h) * PPI * 0.08), fill=255)
    fm = np.array(fm.filter(ImageFilter.GaussianBlur(0.03 * PPI)), float) / 255
    yy, xx = np.mgrid[0:W, 0:W].astype(float) / W
    u = (xx - yy) * 0.7071                                            # diagonal window
    BW = P.get('band_w', 0.035)
    band = np.exp(-((u + 0.10) / BW) ** 2) + 0.45 * np.exp(-((u - 0.22) / (BW * 0.6)) ** 2)
    a = np.array(canvas.convert('RGB'), float)
    a = a + (255 - a) * (SPECG * band * fm)[..., None]
    canvas = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert('RGBA')

# final frame: mat + tile photo circle bottom-right
canvas = canvas.convert('RGB').resize((W // SS, W // SS), Image.LANCZOS)
F = W // SS; pad = int(F * 0.04)
frame = Image.new('RGB', (F + 2 * pad, F + 2 * pad + int(F * 0.13)), (250, 246, 240))
frame.paste(canvas, (pad, pad))
tp = Image.open(cfg['tiles_photo']).convert('RGB')
cd = int(F * 0.27); s = min(tp.size); tp = tp.crop(((tp.width - s) // 2, (tp.height - s) // 2, (tp.width + s) // 2, (tp.height + s) // 2)).resize((cd, cd), Image.LANCZOS)
cm = Image.new('L', (cd, cd), 0); ImageDraw.Draw(cm).ellipse([0, 0, cd - 1, cd - 1], fill=255)
ox = frame.width - cd - int(pad * 0.7); oy = pad + F - int(cd * 0.80)
shd = Image.new('L', frame.size, 0); ImageDraw.Draw(shd).ellipse([ox + 6, oy + 12, ox + cd + 6, oy + cd + 12], fill=120)
frame = Image.composite(Image.new('RGB', frame.size, (60, 40, 40)), frame, shd.filter(ImageFilter.GaussianBlur(14)))
ring = int(cd * 0.035)
ImageDraw.Draw(frame).ellipse([ox - ring, oy - ring, ox + cd + ring, oy + cd + ring], fill=(255, 255, 255))
frame.paste(tp, (ox, oy), cm)
if cfg.get('label'):
    from PIL import ImageFont
    try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf', int(F * 0.024))
    except Exception: f = ImageFont.load_default()
    for n, line in enumerate(cfg['label'].split('\n')):
        ImageDraw.Draw(frame).text((pad, F + pad + int(F * 0.02) + n * int(F * 0.036)), line, fill=(70, 50, 50), font=f)
frame.save(out, quality=92)
print(out, frame.size)
