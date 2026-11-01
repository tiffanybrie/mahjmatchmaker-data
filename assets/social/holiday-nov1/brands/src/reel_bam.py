"""Reel 3: Bam! Let's Mahjong Holly Jolly "advent calendar": 8 doors open on the beat, each revealing a holiday mat
Tiffany matched with one of the three Holly Jolly colourways (her FYM picks, in stock Nov 1), the tiles in the centre
window switch colourway with each door. Then the real Find Your Mat-ch flow on a phone (Holly Jolly Rudolph Red).
Song: Burl Ives "A Holly Jolly Christmas" (~140 BPM)."""
import sys, math, os
from PIL import Image, ImageDraw
from common import *
from app import App, Flow

BPM = 140; B = 60 / BPM
OUT = f'{REPO}/assets/social/holiday-nov1/brands'
RED_ = (200, 32, 47); GRN = (31, 107, 58); PNK = (214, 74, 140)
CW = {'Rudolph Red': RED_, 'Grinch Green': GRN, 'Sugarplum Pink': PNK}
TILE = {'Rudolph Red': photo('fym-holly-jolly-red.jpg'), 'Grinch Green': photo('fym-holly-jolly-green.jpg'), 'Sugarplum Pink': photo('fym-holly-jolly-pink.jpg')}
DOORS = [  # (photo, mat, brand, colourway)   cell order around the centre
 ('bam-hjmat-0.jpg', 'Holly Jolly Christmas', "Bam! Let's Mahjong", 'Rudolph Red'),
 ('ar-pink-0.jpg', 'Very Merry Mahj', 'Anders Ruff', 'Sugarplum Pink'),
 ('bbb-holiday-0.jpg', 'Holiday Neoprene', 'Bam Bird Boutique', 'Rudolph Red'),
 ('plm-hol-2.jpg', 'Candy Cane Lane', 'Peace Love Mahjong', 'Grinch Green'),
 ('omm-yuletide-0.jpg', 'Yuletide', 'Oh My Mahjong', 'Rudolph Red'),
 ('omm-clara-0.jpg', 'Clara', 'Oh My Mahjong', 'Sugarplum Pink'),
 ('ar-mail-0.jpg', "Santa's Mahjong Mail", 'Anders Ruff', 'Rudolph Red'),
 ('plm-hol-6.jpg', 'Pretty Little Christmas', 'Peace Love Mahjong', 'Sugarplum Pink'),
]
CELLS = [0, 1, 2, 5, 8, 7, 6, 3]
CS, GAP = 300, 18; X0 = W // 2 - (3 * CS + 2 * GAP) // 2; Y0 = 470
def cell_xy(c): return X0 + (c % 3) * (CS + GAP), Y0 + (c // 3) * (CS + GAP)
def sq(fn):
    im = trim_white(photo(fn), thr=240); s = min(im.size)
    return im.crop(((im.width - s) // 2, (im.height - s) // 2, (im.width + s) // 2, (im.height + s) // 2)).resize((CS, CS), Image.LANCZOS)
MATS = [sq(d[0]) for d in DOORS]
BG = plaid((W, H), (253, 236, 242), [(0, 60, (244, 170, 196), 0.55), (90, 14, (200, 32, 47), 0.35)], scale=1.2)
_l = BG.crop((0, 0, W // 2, H)); BG.paste(_l.transpose(Image.FLIP_LEFT_RIGHT), (W // 2, 0))  # mirror: symmetric about the centre
f_cap = lambda s: font(FONT_CAP, s); f_pb = lambda s: font(FONT_POP_B, s)

def door_panel(i, col):
    p = Image.new('RGB', (CS, CS), col); d = ImageDraw.Draw(p)
    d.rounded_rectangle((14, 14, CS - 15, CS - 15), 18, outline=(255, 255, 255), width=5)
    # ribbon + bow
    d.rectangle((CS // 2 - 14, 0, CS // 2 + 14, CS), fill=(255, 255, 255)); d.rectangle((0, CS // 2 - 14, CS, CS // 2 + 14), fill=(255, 255, 255))
    d.ellipse((CS // 2 - 70, CS // 2 - 46, CS // 2 - 6, CS // 2 + 10), outline=(255, 255, 255), width=12)
    d.ellipse((CS // 2 + 6, CS // 2 - 46, CS // 2 + 70, CS // 2 + 10), outline=(255, 255, 255), width=12)
    nb = Image.new('RGBA', (110, 110), (0, 0, 0, 0)); nd = ImageDraw.Draw(nb); nd.ellipse((0, 0, 109, 109), fill=(255, 255, 255))
    nd.text((55, 58), str(i + 1), font=f_cap(70), fill=col, anchor='mm'); p.paste(nb, (CS - 130, CS - 130), nb)
    return p
PANELS = [door_panel(i, CW[d[3]]) for i, d in enumerate(DOORS)]

def doors(t, tb):
    c = BG.copy(); d = ImageDraw.Draw(c); sparkles(d, t, n=30, seed=21, col=(255, 255, 255))
    draw_center(d, 262, 'Holly Jolly', f_cap(104), RED_, shadow=(0, 5, (255, 255, 255)))
    n_open = clamp(tb - 1, 0, 8)
    cur = DOORS[min(7, int(n_open))][3] if tb >= 1 else 'Rudolph Red'
    draw_center(d, 382, 'advent calendar of matches', font(FONT_CAVEAT, 64), GRN)
    # centre window: the tiles in the current colourway
    cx, cy = cell_xy(4); tp = rounded(cover(TILE[cur], (CS, CS)), 22)
    shadow_paste(c, tp, (cx, cy), alpha=120, blur=12, offset=(0, 8))
    d = ImageDraw.Draw(c)
    for i, cell in enumerate(CELLS):
        x, y = cell_xy(cell); u = clamp((tb - 1 - i) / 0.6)  # door opens over 0.6 beat
        if u > 0:
            shadow_paste(c, rounded(MATS[i], 22), (x, y), alpha=110, blur=12, offset=(0, 8))
        if u < 1:
            e = ease_in_out(u); w = max(2, int(CS * (1 - e)))
            pnl = PANELS[i].resize((w, CS)); shade = int(70 * e)
            if shade: pnl = Image.blend(pnl, Image.new('RGB', pnl.size, (0, 0, 0)), shade / 255)
            c.paste(rounded(pnl, 22) if w > 50 else pnl, (x, y), rounded(pnl, 22) if w > 50 else None)
    d = ImageDraw.Draw(c)
    if 1 <= tb < 9:
        i = min(7, int(tb - 1)); dd = DOORS[i]
        pill(d, W // 2, Y0 + 3 * CS + 2 * GAP + 30, f'{dd[1]} · {dd[2]}', f_pb(32), (255, 255, 255), CW[dd[3]])
        draw_center(d, Y0 + 3 * CS + 2 * GAP + 112, f'matched with Holly Jolly {dd[3]}', f_pb(30), NAVY)
    elif tb >= 9:
        pill(d, W // 2, Y0 + 3 * CS + 2 * GAP + 30, '3 COLORWAYS · 44 MATCHES', f_pb(34), (255, 255, 255), RED_)
    else:
        pill(d, W // 2, Y0 + 3 * CS + 2 * GAP + 30, "BAM! LET'S MAHJONG", f_pb(32), (255, 255, 255), GRN)
    return c

A = App(os.environ.get('BAM_CAP', '/tmp/claude-0/-home-claude/f4da3022-6ec8-595a-90aa-668aea191899/scratchpad/cap/bam3'))
FL = Flow(A, B, BG, {'tiles': 'Pick your tiles: Holly Jolly', 'mats': 'Swipe her Rudolph Red matches', 'suitors': 'Your suitors',
                     'zoom': 'Zoom in on the mat  + + +', 'racks': 'Now swipe racks', 'card': "It's a match! Your match card",
                     'shop': 'Shop it all in one list', 'rack_names': ['Peace Love Mahjong Oak', 'Bird & Bamboo Red', 'Bird & Bamboo Kelly Green']}, sc=1.35)
NSW = 5
T_APP1 = 10; T_APP2 = T_APP1 + FL.len1(NSW); T_END = T_APP2 + FL.len2(); NB = T_END + 4; DUR = NB * B

def end(t, te):
    c = BG.copy(); d = ImageDraw.Draw(c); snow(d, t, n=50, seed=22, col=(255, 255, 255))
    draw_center(d, 280, 'Holly Jolly’s 3 colorways:', f_cap(66), RED_, shadow=(0, 4, (255, 255, 255)))
    p = back_out(clamp(te / 0.25)); fs = int(170 * (0.7 + 0.3 * p))
    draw_center(d, 380 + (170 - fs) // 2, '44 matches', f_cap(fs), GRN, shadow=(0, 5, (255, 255, 255)))
    draw_runs_center(d, 600, [('in Find ', f_cap(68)), ('Your', font(FONT_PLAY_I, 70)), (' Mat-ch™', f_cap(68))], NAVY)
    # three colourway tiles
    for j, k in enumerate(['Rudolph Red', 'Grinch Green', 'Sugarplum Pink']):
        pj = back_out(clamp((te - 0.3 * B - j * 0.08) / 0.2)); s = max(4, int(250 * pj))
        x = W // 2 - 425 + j * 300 + (250 - s) // 2
        shadow_paste(c, rounded(cover(TILE[k], (s, s)), 18), (x, 740 + (250 - s) // 2), alpha=110, blur=10, offset=(0, 6))
        d = ImageDraw.Draw(c); draw_center(d, 1010, k, f_pb(30), CW[k], cx=W // 2 - 425 + j * 300 + 125)
    d = ImageDraw.Draw(c)
    if te >= B:
        pill(d, W // 2, 1110, 'Shop now · use code MAHJMATCH', f_pb(46), (255, 255, 255), PINK, padx=44, pady=22)
        draw_center(d, 1240, "Bam! Let's Mahjong · link in bio", font(FONT_POP_M, 32), NAVY)
        # Nov 1 polish: no URL in reels (brand guide); 'link in bio' stays
    return c

def draw(t):
    b = t / B
    if b < T_APP1: return doors(t, b)
    if b < T_APP2: return FL.f1(b - T_APP1, NSW)
    if b < T_END: return FL.f2(b - T_APP2)
    return end(t, t - T_END * B)

if __name__ == '__main__':
    if '--only' in sys.argv:
        for tt in [float(x) for x in sys.argv[sys.argv.index('--only') + 1].split(',')]:
            draw(tt).save(f'/dev/shm/brand-reshare/bam_{tt:05.2f}.jpg', quality=88)
        sys.exit()
    R = Renderer('bam', DUR); R.run(draw)
    click_track('/dev/shm/brand-reshare/bam_click.wav', DUR, BPM, marks=[x * B for x in [1, T_APP1, T_APP2, T_END]])
    import shutil, os
    R.encode('/dev/shm/brand-reshare/bam-holly-jolly-advent-reel.tmp.mp4', '/dev/shm/brand-reshare/bam_click.wav', '/dev/shm/brand-reshare/bam-holly-jolly-advent-reel-beat.tmp.mp4')
    for src, dst in [('bam-holly-jolly-advent-reel.tmp.mp4', 'bam-holly-jolly-advent-reel.mp4'), ('bam-holly-jolly-advent-reel-beat.tmp.mp4', 'bam-holly-jolly-advent-reel-BEATTEST.mp4')]:  # temp name, then mv into place
        shutil.copyfile(f'/dev/shm/brand-reshare/{src}', f'{OUT}/{dst}.part'); os.replace(f'{OUT}/{dst}.part', f'{OUT}/{dst}')
    doors(0, 9.5).save(f'{OUT}/bam-holly-jolly-advent-cover.jpg', quality=90)
    R.cleanup()
    contact_sheet(f'{OUT}/bam-holly-jolly-advent-reel.mp4', f'{OUT}/bam-holly-jolly-advent-contact.jpg')
