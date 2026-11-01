"""Reel 1: Anders Ruff "Outfit change" (Dear Santa tiles stay put; the 7 Anders Ruff Christmas mats Tiffany matched
with Dear Santa swap underneath on the beat). Primary song: Ariana Grande "Santa Tell Me" (96 BPM, beat = 0.625 s).
Usage: python3 reel_ar_outfit.py [--only t1,t2,...]  (stills for checking) """
import sys, math
from PIL import Image, ImageDraw, ImageFilter
from common import *

BPM = 96; B = 60 / BPM; DUR = 26 * B   # 16.25 s
OUT = f'{REPO}/assets/social/holiday-nov1/brands'
# (photo, name) in show order. All 7 = Dear Santa's FYM match list (her picks), all in stock Nov 1 00:06 ET.
LOOKS = [('ar-classic-0.jpg', 'Classic Very Merry Mahj'), ('ar-tidings-0.jpg', 'Tartan Tidings'),
         ('ar-mail-0.jpg', "Santa's Mahjong Mail"), ('ar-candy-0.jpg', 'Candy Cane Lane'),
         ('ar-water-0.jpg', 'Watercolor Christmas Tree'), ('ar-toile-0.jpg', 'Tartan Toile Noël'),
         ('ar-ever-0.jpg', 'Evergreen & Tartan')]
MS = 960  # mat size on screen
MAT_Y = 430

def load_mat(fn):
    im = trim_white(photo(fn), thr=238)
    s = min(im.size); im = im.crop(((im.width - s) // 2, (im.height - s) // 2, (im.width + s) // 2, (im.height + s) // 2))
    return im.resize((MS, MS), Image.LANCZOS)
MATS = [load_mat(f) for f, _ in LOOKS]
BGS = []
for m in MATS:
    bg = cover(m, (W // 6, H // 6)).filter(ImageFilter.GaussianBlur(6)).resize((W, H), Image.BICUBIC)
    bg = Image.blend(bg, Image.new('RGB', (W, H), (20, 12, 14)), 0.55); BGS.append(bg)
TILES = trim_white(photo('ar-dearsanta-3.jpg'), thr=246)
INSET = polaroid(TILES, (380, 380), border=16, bottom=16, r=12, label='Dear Santa tiles', lf=font(FONT_CAVEAT, 46), lcol=RED)
HOOK_POL = polaroid(TILES, (640, 640), border=22, bottom=22, r=14, label='Dear Santa tiles', lf=font(FONT_CAVEAT, 60), lcol=RED)
BG_RED = radial((W, H), (196, 38, 48), (110, 14, 22), cy=0.42, rad=0.9)
BG_GREEN = radial((W, H), (34, 104, 68), (10, 46, 30), cy=0.45, rad=0.9)
f_cav = font(FONT_CAVEAT, 150); f_cap90 = font(FONT_CAP, 92); f_cap70 = font(FONT_CAP, 66); f_cap56 = font(FONT_CAP, 54)
f_pop28 = font(FONT_POP_B, 28); f_pop34 = font(FONT_POP_B, 34); f_pop24 = font(FONT_POP_M, 26)
f_cap130 = font(FONT_CAP, 150); f_play = font(FONT_PLAY_I, 64); f_cap64 = font(FONT_CAP, 64)

def place_inset(c, t_since, scale=1.0, base=(642, 1078)):
    ins = INSET if scale == 1.0 else INSET.resize((int(INSET.width * scale), int(INSET.height * scale)), Image.LANCZOS)
    shadow_paste(c, ins, base, rot=-4, alpha=150)

def hook(t):
    c = BG_RED.copy(); d = ImageDraw.Draw(c)
    sparkles(d, t, n=50, seed=4, box=(0, 0, W, H), col=(255, 226, 170))
    # polaroid drops in (beat 0) then wiggles on beats
    p = back_out(t / (B * 0.9)); y = lerp(-700, 630, p)
    rot = -4 + 2.0 * math.sin(t / B * math.pi)
    shadow_paste(c, HOOK_POL, (W // 2 - HOOK_POL.width // 2, y), rot=rot, alpha=150)
    d = ImageDraw.Draw(c)
    if t >= 0: draw_center(d, 270, 'Dear Santa,', f_cav, (255, 244, 230), shadow=(0, 6, (90, 8, 16)))
    if t >= B * 1:
        s = back_out((t - B) / 0.25)
        draw_center(d, 450 - int(20 * (1 - s)), 'what do I wear', f_cap70, (255, 244, 230), shadow=(0, 5, (90, 8, 16)))
    if t >= B * 2:
        draw_center(d, 540, 'to Christmas?', f_cap70, (255, 214, 120), shadow=(0, 5, (90, 8, 16)))
    if t >= B * 3:
        pill(d, W // 2, 1462, '7 ANDERS RUFF LOOKS  ·  1 TILE SET', f_pop28, (110, 14, 22), (255, 244, 230))
    return c

def look(t, k, tk):
    """k = look index, tk = seconds since this look started (2 beats long)."""
    c = BGS[k].copy()
    # mat slam: scale 1.10 -> 1.0, from slight drop
    s = 1.0 + 0.10 * (1 - back_out(tk / 0.22, 2.2))
    m = MATS[k]
    if s != 1.0:
        sz = int(MS * s); m = m.resize((sz, sz), Image.BILINEAR)
    m = rounded(m, 34)
    x = W // 2 - m.width // 2; y = MAT_Y + MS // 2 - m.height // 2
    # previous mat underneath for the first frames (outfit swap wipe)
    if k > 0 and tk < 0.12:
        shadow_paste(c, rounded(MATS[k - 1], 34), (W // 2 - MS // 2, MAT_Y), alpha=140)
    shadow_paste(c, m, (x, y), alpha=170)
    d = ImageDraw.Draw(c)
    # flash
    if tk < 0.13:
        a = int(150 * (1 - tk / 0.13)); fl = Image.new('RGB', (W, H), (255, 250, 240)); c = Image.blend(c, fl, a / 255); d = ImageDraw.Draw(c)
    place_inset(c, tk)
    d = ImageDraw.Draw(c)
    # top labels
    pill(d, W // 2, 262, f'LOOK {k + 1} OF 7', f_pop28, (255, 255, 255), RED if k % 2 == 0 else PINE)
    sc = back_out(clamp(tk / 0.2))
    name = LOOKS[k][1]
    fnt = f_cap70 if text_w(name, f_cap70) < 1000 else f_cap56
    draw_center(d, 330 + int(18 * (1 - sc)), name, fnt, (255, 248, 236), shadow=(0, 5, (20, 10, 10)))
    # beat-2 heart pulse on the mat's top-left corner
    if tk >= B:
        hp = back_out(clamp((tk - B) / 0.18)); r = int(46 * hp)
        cx, cy = 120, MAT_Y + 40
        heart(d, cx, cy, r, PINK)
    # brand line under the mat, left of the inset
    d.text((70, MAT_Y + MS + 22), 'ANDERS RUFF', font=f_pop28, fill=(255, 236, 220))
    return c

def heart(d, cx, cy, r, col):
    if r <= 2: return
    d.ellipse((cx - r, cy - r * 0.9, cx, cy + r * 0.1), fill=col)
    d.ellipse((cx, cy - r * 0.9, cx + r, cy + r * 0.1), fill=col)
    d.polygon([(cx - r * 0.98, cy - r * 0.25), (cx + r * 0.98, cy - r * 0.25), (cx, cy + r * 1.05)], fill=col)

GRID_CELLS = None
def grid(t, tg):
    c = BG_GREEN.copy(); d = ImageDraw.Draw(c); sparkles(d, t, n=40, seed=9, col=(255, 230, 170))
    draw_center(d, 262, '7 Christmas looks.', f_cap70, (255, 248, 236), shadow=(0, 5, (5, 30, 18)))
    draw_center(d, 350, 'One tile set.', f_cap70, (255, 214, 120), shadow=(0, 5, (5, 30, 18)))
    cs, gap = 316, 14; x0 = W // 2 - (3 * cs + 2 * gap) // 2; y0 = 470
    order = [0, 1, 2, 5, 8, 7, 6, 3]  # clockwise around the centre
    for j, cell in enumerate(order):
        appear = j * B / 2
        if tg < appear: continue
        p = back_out(clamp((tg - appear) / 0.2)); sz = int(cs * (0.6 + 0.4 * p))
        im = rounded(MATS[j].resize((sz, sz), Image.LANCZOS), 18) if j < 7 else None
        cx = x0 + (cell % 3) * (cs + gap) + cs // 2; cy = y0 + (cell // 3) * (cs + gap) + cs // 2
        if im is not None:
            shadow_paste(c, im, (cx - sz // 2, cy - sz // 2), alpha=120, blur=14, offset=(0, 8))
        else:
            card = Image.new('RGB', (sz, sz), (255, 244, 230)); cd = ImageDraw.Draw(card)
            fs = font(FONT_CAP, max(10, int(92 * sz / cs))); fl = font(FONT_POP_B, max(8, int(25 * sz / cs)))
            draw_center(cd, int(sz * 0.20), '+20', fs, PINK, cx=sz // 2)
            draw_center(cd, int(sz * 0.56), 'MORE DEAR SANTA', fl, NAVY, cx=sz // 2)
            draw_center(cd, int(sz * 0.68), 'MATCHES IN', fl, NAVY, cx=sz // 2)
            draw_center(cd, int(sz * 0.80), 'FIND YOUR MAT-CH', fl, NAVY, cx=sz // 2)
            shadow_paste(c, rounded(card, 18), (cx - sz // 2, cy - sz // 2), alpha=120, blur=14, offset=(0, 8))
    # centre: the tiles
    cx = x0 + cs + gap + cs // 2; cy = y0 + cs + gap + cs // 2
    tp = rounded(cover(TILES, (cs, cs)), 18); shadow_paste(c, tp, (cx - cs // 2, cy - cs // 2), alpha=140, blur=14, offset=(0, 8))
    d = ImageDraw.Draw(c)
    pill(d, W // 2, y0 + 3 * cs + 2 * gap + 34, 'DEAR SANTA x ANDERS RUFF', f_pop28, (255, 255, 255), RED)
    return c

def end(t, te):
    c = BG_RED.copy(); d = ImageDraw.Draw(c); snow(d, t, n=60, seed=5, col=(255, 240, 236))
    p1 = back_out(clamp(te / 0.25))
    draw_center(d, 290, 'Dear Santa has', f_cap70, (255, 244, 230), shadow=(0, 5, (90, 8, 16)))
    sz = int(170 * (0.7 + 0.3 * p1)); fb = font(FONT_CAP, sz)
    draw_center(d, 390 + (170 - sz) // 2, '27 matches', fb, (255, 214, 120), shadow=(0, 7, (90, 8, 16)))
    if te >= B:
        draw_runs_center(d, 610, [('in Find ', f_cap70), ('Your', font(FONT_PLAY_I, 72)), (' Mat-ch™', f_cap70)], (255, 244, 230), shadow=(0, 5, (90, 8, 16)))
    if te >= B * 2:
        sm = 136; gap = 8; x0 = W // 2 - (7 * sm + 6 * gap) // 2
        for j, m in enumerate(MATS):
            pj = back_out(clamp((te - B * 2 - j * 0.05) / 0.2))
            if pj <= 0: continue
            s2 = max(4, int(sm * pj)); shadow_paste(c, rounded(m.resize((s2, s2), Image.LANCZOS), 10), (x0 + j * (sm + gap) + (sm - s2) // 2, 760 + (sm - s2) // 2), alpha=120, blur=10, offset=(0, 6))
        d = ImageDraw.Draw(c)
        y = 940
        for ln in ['Anders Ruff’s 8 Christmas mats,', 'matched 93 times with 35 tile sets']:
            draw_center(d, y, ln, font(FONT_POP_B, 42), (255, 236, 224)); y += 62
    if te >= B * 3:
        pill(d, W // 2, 1110, 'Preorder now · mats ship early November', f_pop34, RED, (255, 244, 230))
        pill(d, W // 2, 1222, 'Code MAHJMATCH  ·  link in bio', font(FONT_POP_B, 42), (255, 255, 255), PINK)
        draw_center(d, 1360, 'mahjmatchmaker.com', f_cap64, (255, 244, 230))
    return c

def draw(t):
    if t < 4 * B: return hook(t)
    if t < 18 * B:
        k = int((t - 4 * B) // (2 * B)); return look(t, k, t - 4 * B - k * 2 * B)
    if t < 22 * B: return grid(t, t - 18 * B)
    return end(t, t - 22 * B)

if __name__ == '__main__':
    if '--only' in sys.argv:
        ts = [float(x) for x in sys.argv[sys.argv.index('--only') + 1].split(',')]
        for tt in ts: draw(tt).save(f'/dev/shm/brand-reshare/ar_{tt:05.2f}.jpg', quality=88)
        sys.exit()
    R = Renderer('ar', DUR); R.run(draw)
    cuts = [4 * B + 2 * B * k for k in range(7)] + [18 * B, 22 * B]
    click_track('/dev/shm/brand-reshare/ar_click.wav', DUR, BPM, marks=cuts)
    R.encode(f'{OUT}/ar-outfit-change-reel.mp4', '/dev/shm/brand-reshare/ar_click.wav', f'{OUT}/ar-outfit-change-reel-BEATTEST.mp4')
    grid(21.9 * B, 3.9 * B).save(f'{OUT}/ar-outfit-change-cover.jpg', quality=90)
    R.cleanup()
