"""Reel 2: Virora Mahjong Tinselle (Emerald Green) "Trim the tree": Tinselle is the star on top, and the holiday mats
Tiffany matched with it (FYM v1.10 match list, partners with a verified IG handle, in stock Nov 1 00:10 ET) drop onto the
tree as ornaments, one per beat. Then two ornaments open into full match views (mat full, tiles inset).
Primary song: Brenda Lee "Rockin' Around the Christmas Tree" (~142 BPM, beat = 0.4225 s)."""
import sys, math
from PIL import Image, ImageDraw, ImageFilter
from common import *

BPM = 142; B = 60 / BPM; NB = 38; DUR = NB * B   # ~16.06 s
OUT = f'{REPO}/assets/social/holiday-nov1/brands'
ORN = [  # (photo, mat name, brand)  order = drop order (top of tree first)
 ('ar-ever-0.jpg', 'Evergreen & Tartan', 'Anders Ruff'), ('omm-yuletide-0.jpg', 'Yuletide', 'Oh My Mahjong'),
 ('ar-tidings-0.jpg', 'Tartan Tidings', 'Anders Ruff'), ('plm-hol-5.jpg', 'Merry Mix', 'Peace Love Mahjong'),
 ('bam-hjmat-0.jpg', 'Holly Jolly Christmas', "Bam! Let's Mahjong"), ('ar-candy-0.jpg', 'Candy Cane Lane', 'Anders Ruff'),
 ('plm-hol-9.jpg', 'Spirit of Christmas', 'Peace Love Mahjong'), ('bbb-holiday-0.jpg', 'Holiday Neoprene', 'Bam Bird Boutique'),
 ('ar-mail-0.jpg', "Santa's Mahjong Mail", 'Anders Ruff'), ('plm-hol-8.jpg', 'Poinsettia & Peace', 'Peace Love Mahjong'),
 ('plm-hol-4.jpg', 'Nutcracker Noel - Red & Green', 'Peace Love Mahjong'), ('ar-classic-0.jpg', 'Classic Very Merry Mahj', 'Anders Ruff'),
 ('plm-hol-2.jpg', 'Candy Cane Lane', 'Peace Love Mahjong'), ('plm-hol-7.jpg', 'Vintage Noel', 'Peace Love Mahjong'),
 ('plm-hol-3.jpg', 'Perfectly Wrapped', 'Peace Love Mahjong'), ('plm-hol-10.jpg', 'Merry & Striped', 'Peace Love Mahjong'),
]
ROWS = [2, 3, 3, 4, 4]; ROW_Y = [640, 800, 960, 1125, 1290]; ROW_W = [250, 470, 560, 760, 860]
R0 = 74  # ornament radius
POS = []
for r, (n, y, w) in enumerate(zip(ROWS, ROW_Y, ROW_W)):
    for i in range(n): POS.append((W // 2 - w // 2 + (w * i // (n - 1)), y + (18 if i % 2 else 0)))

def mat_square(fn, thr=240):
    im = trim_white(photo(fn), thr=thr); s = min(im.size)
    return im.crop(((im.width - s) // 2, (im.height - s) // 2, (im.width + s) // 2, (im.height + s) // 2))
SQ = [mat_square(f) for f, _, _ in ORN]

def bauble(sq, r):
    d2 = r * 2; m = sq.resize((int(d2 * 1.08), int(d2 * 1.08)), Image.LANCZOS)
    m = m.crop(((m.width - d2) // 2, (m.height - d2) // 2, (m.width - d2) // 2 + d2, (m.height - d2) // 2 + d2)).convert('RGBA')
    mask = Image.new('L', (d2, d2), 0); ImageDraw.Draw(mask).ellipse((0, 0, d2 - 1, d2 - 1), fill=255); m.putalpha(mask)
    # glossy shine + gold rim + cap
    o = Image.new('RGBA', (d2 + 8, d2 + 40), (0, 0, 0, 0)); o.paste(m, (4, 36), m); od = ImageDraw.Draw(o)
    od.ellipse((4, 36, d2 + 3, d2 + 35), outline=GOLD, width=5)
    sh = Image.new('RGBA', (d2, d2), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    sd.ellipse((int(d2 * .18), int(d2 * .12), int(d2 * .45), int(d2 * .34)), fill=(255, 255, 255, 120))
    sh = sh.filter(ImageFilter.GaussianBlur(4)); o.alpha_composite(sh, (4, 36))
    cw = int(r * 0.6); od.rounded_rectangle((d2 // 2 + 4 - cw // 2, 18, d2 // 2 + 4 + cw // 2, 44), 6, fill=GOLD, outline=GOLD_D, width=2)
    od.ellipse((d2 // 2 + 4 - 10, 2, d2 // 2 + 4 + 10, 22), outline=GOLD, width=4)
    return o
BAUBLES = [bauble(s, R0) for s in SQ]

TILE = photo('fym-tinselle-emerald-grid3.jpg')
BG = radial((W, H), (22, 104, 70), (4, 30, 22), cy=0.5, rad=0.95)
f_cap = lambda s: font(FONT_CAP, s); f_pb = lambda s: font(FONT_POP_B, s); f_cav = font(FONT_CAVEAT, 110)
CREAMY = (255, 246, 228)

def topper(c, t, size=300, y=300, glow=True):
    """Tinselle star: the canonical tile photo in a gold-rimmed circle with rays."""
    d = ImageDraw.Draw(c); cx = W // 2; cy = y + size // 2
    if glow:
        for k in range(12):
            a = k * math.pi / 6 + t * 0.6; L = size * (0.72 + 0.06 * math.sin(t * 6 + k))
            d.line((cx, cy, cx + L * math.cos(a), cy + L * math.sin(a)), fill=(240, 210, 130), width=4)
    ph = cover(TILE, (size, size), cx=0.5); m = Image.new('L', (size, size), 0); ImageDraw.Draw(m).ellipse((0, 0, size - 1, size - 1), fill=255)
    ph = ph.convert('RGBA'); ph.putalpha(m)
    shadow_paste(c, ph, (cx - size // 2, y), alpha=150, blur=16, offset=(0, 8))
    d = ImageDraw.Draw(c); d.ellipse((cx - size // 2 - 3, y - 3, cx + size // 2 + 2, y + size + 2), outline=GOLD, width=8)

def garland(d, t, n_lit):
    """gold bead garlands draped across the tree rows."""
    for r in range(len(ROW_Y)):
        y = ROW_Y[r] - 70; w = ROW_W[r] + 170
        for k in range(46):
            u = k / 45; x = W // 2 - w // 2 + w * u; yy = y + 60 * math.sin(math.pi * u) + 12 * r
            on = (k + int(t * 8)) % 3 == 0
            rr = 5 if on else 3.5
            d.ellipse((x - rr, yy - rr, x + rr, yy + rr), fill=(255, 226, 140) if on else GOLD_D)

def tree_scene(t, tb):
    """tb = beats since tree scene started."""
    c = BG.copy(); d = ImageDraw.Draw(c); sparkles(d, t, n=50, seed=11, col=(255, 232, 170))
    # tree silhouette
    d.polygon([(W // 2, 480), (W // 2 - 520, 1420), (W // 2 + 520, 1420)], fill=(12, 70, 46))
    garland(d, t, 0)
    topper(c, t, size=200, y=262 + 10)
    d = ImageDraw.Draw(c)
    n = int(clamp(tb, 0, 16))
    for i in range(min(16, int(tb) + 1)):
        ti = (tb - i) * B  # seconds since this ornament's drop
        if ti < 0: continue
        x, y = POS[i]
        drop = ease_out(ti / 0.22); yy = lerp(y - 380, y, drop)
        sw = 9 * math.exp(-ti * 2.2) * math.sin(ti * 11)  # swing (degrees)
        b = BAUBLES[i]
        if tb >= 18:
            pulse = 1 + 0.06 * math.sin((tb - 18) * math.pi)  # on-beat twinkle
            b = b.resize((int(b.width * pulse), int(b.height * pulse)), Image.BILINEAR)
        bb = b.rotate(sw, resample=Image.BICUBIC, expand=True, center=(b.width // 2, 0))
        d.line((x, yy - R0 - 60, x, yy - R0 - 30), fill=GOLD, width=2)
        c.paste(bb, (int(x - bb.width / 2), int(yy - R0 - 36 - (bb.height - b.height) / 2)), bb)
    d = ImageDraw.Draw(c)
    if tb < 16.5:
        k = min(15, int(tb)); nm, br = ORN[k][1], ORN[k][2]
        fs = 50 if text_w(nm, f_cap(50)) < 960 else 42
        draw_center(d, 1408, nm, f_cap(fs), CREAMY, shadow=(0, 4, (2, 20, 12)))
        draw_center(d, 1474, br.upper(), f_pb(28), (240, 210, 130))
        pill(d, W // 2, 520 - 40, f'ORNAMENT {k + 1} OF 16', f_pb(24), (12, 70, 46), (255, 236, 190))
    else:
        p = back_out(clamp((tb - 16.5) * B / 0.25))
        draw_center(d, 1404, '16 holiday mats she matched', f_cap(50), CREAMY, shadow=(0, 4, (2, 20, 12)))
        draw_center(d, 1466, 'IN STOCK TONIGHT · 5 BRANDS', f_pb(30), (240, 210, 130))
    return c

def hook(t):
    c = BG.copy(); d = ImageDraw.Draw(c); sparkles(d, t, n=60, seed=12, col=(255, 232, 170))
    p = back_out(clamp(t / 0.35)); sz = int(560 * (0.5 + 0.5 * p))
    topper(c, t, size=sz, y=760 - sz // 2 + 40)
    d = ImageDraw.Draw(c)
    draw_center(d, 270, 'Tinselle', f_cap(130), (255, 214, 120), shadow=(0, 6, (2, 20, 12)))
    draw_center(d, 430, '(Emerald Green)', f_cap(60), CREAMY, shadow=(0, 4, (2, 20, 12)))
    if t >= 2 * B:
        draw_center(d, 1150, 'is back in stock.', f_cav, CREAMY, shadow=(0, 5, (2, 20, 12)))
    if t >= 3 * B:
        draw_center(d, 1300, 'Let’s trim the tree.', f_cap(62), (255, 214, 120), shadow=(0, 4, (2, 20, 12)))
        pill(d, W // 2, 1420, 'VIRORA MAHJONG', f_pb(30), (12, 70, 46), (255, 236, 190))
    return c

def reveal(t, k, tr, dur):
    """ornament k opens into a full match view: mat square, Tinselle inset bottom-right."""
    c = BG.copy(); d = ImageDraw.Draw(c); sparkles(d, t, n=40, seed=13, col=(255, 232, 170))
    p = ease_out(tr / 0.3); S = int(lerp(150, 900, p)); x, y = POS[k]
    cx = lerp(x, W // 2, p); cy = lerp(y, 860, p)
    sq = SQ[k].resize((S, S), Image.LANCZOS).convert('RGBA')
    rad = int(lerp(S / 2, 30, p)); m = Image.new('L', (S, S), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, S - 1, S - 1), rad, fill=255); sq.putalpha(m)
    shadow_paste(c, sq, (cx - S / 2, cy - S / 2), alpha=160)
    d = ImageDraw.Draw(c)
    if tr > 0.25:
        q = back_out(clamp((tr - 0.25) / 0.25))
        ins = polaroid(TILE, (360, 360), border=14, bottom=14, r=12, label='Tinselle tiles', lf=font(FONT_CAVEAT, 44), lcol=PINE)
        s2 = max(0.05, q); ins = ins.resize((max(4, int(ins.width * s2)), max(4, int(ins.height * s2))), Image.LANCZOS)
        shadow_paste(c, ins, (650 + (1 - s2) * 180, 1030 + (1 - s2) * 200), rot=-4, alpha=150)
        d = ImageDraw.Draw(c)
    nm, br = ORN[k][1], ORN[k][2]
    pill(d, W // 2, 262, "IT'S A MATCH", f_pb(28), (255, 255, 255), PINK)
    draw_center(d, 336, f'Tinselle x {nm}', f_cap(56 if text_w(f'Tinselle x {nm}', f_cap(56)) < 1000 else 46), CREAMY, shadow=(0, 4, (2, 20, 12)))
    d.text((90, 1330), br.upper(), font=f_pb(30), fill=(240, 210, 130))
    return c

def end(t, te):
    c = BG.copy(); d = ImageDraw.Draw(c); snow(d, t, n=60, seed=14)
    topper(c, t, size=300, y=270)
    d = ImageDraw.Draw(c)
    draw_center(d, 640, 'Tinselle (Emerald Green) has', f_cap(54), CREAMY, shadow=(0, 4, (2, 20, 12)))
    p = back_out(clamp(te / 0.25)); fs = int(160 * (0.7 + 0.3 * p))
    draw_center(d, 720 + (160 - fs) // 2, '23 matches', f_cap(fs), (255, 214, 120), shadow=(0, 6, (2, 20, 12)))
    if te >= B:
        draw_runs_center(d, 930, [('in Find ', f_cap(68)), ('Your', font(FONT_PLAY_I, 70)), (' Mat-ch™', f_cap(68))], CREAMY, shadow=(0, 4, (2, 20, 12)))
    if te >= 2 * B:
        # ornament row
        for j in range(8):
            b = BAUBLES[j].resize((96, 120), Image.LANCZOS); c.paste(b, (W // 2 - 4 * 112 + j * 112 + 8, 1050), b)
        d = ImageDraw.Draw(c)
    if te >= 3 * B:
        pill(d, W // 2, 1215, 'Back in stock at Virora Mahjong', f_pb(36), (12, 70, 46), (255, 236, 190))
        pill(d, W // 2, 1320, 'Code MAHJMATCH  ·  link in bio', f_pb(42), (255, 255, 255), PINK)
        draw_center(d, 1440, 'mahjmatchmaker.com', f_cap(60), CREAMY)
    return c

# timeline in beats
T_TREE, T_REV1, T_REV2, T_END = 4, 24, 28, 31
def draw(t):
    b = t / B
    if b < T_TREE: return hook(t)
    if b < T_REV1: return tree_scene(t, b - T_TREE)
    if b < T_REV2: return reveal(t, 0, t - T_REV1 * B, 4 * B)
    if b < T_END: return reveal(t, 1, t - T_REV2 * B, 3 * B)
    return end(t, t - T_END * B)

if __name__ == '__main__':
    if '--only' in sys.argv:
        for tt in [float(x) for x in sys.argv[sys.argv.index('--only') + 1].split(',')]:
            draw(tt).save(f'/dev/shm/brand-reshare/vi_{tt:05.2f}.jpg', quality=88)
        sys.exit()
    R = Renderer('vi', DUR); R.run(draw)
    cuts = [T_TREE * B + i * B for i in range(16)] + [T_REV1 * B, T_REV2 * B, T_END * B]
    click_track('/dev/shm/brand-reshare/vi_click.wav', DUR, BPM, marks=cuts)
    R.encode(f'{OUT}/virora-tinselle-tree-reel.mp4', '/dev/shm/brand-reshare/vi_click.wav', f'{OUT}/virora-tinselle-tree-reel-BEATTEST.mp4')
    tree_scene(19.5 * B, 19.5 - 4 + 0.0).save(f'{OUT}/virora-tinselle-tree-cover.jpg', quality=90)
    R.cleanup()
