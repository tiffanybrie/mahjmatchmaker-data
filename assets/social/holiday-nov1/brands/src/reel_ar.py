"""Reel 1 v2 (Tiffany's 12:22am update): Anders Ruff "Outfit change" photo-dump splices INTERWOVEN with the real
Find Your Mat-ch flow on a phone (zoomed in): Dear Santa tiles -> swipe AR mats -> racks -> the match card it makes.
Song: Ariana Grande "Santa Tell Me" (96 BPM). Beat map in README."""
import sys, math
from PIL import Image, ImageDraw
from common import *
from app import App, Flow, caption
import reel_ar_outfit as O

B = O.B; CAP = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else '/tmp/claude-0/-home-claude/f4da3022-6ec8-595a-90aa-668aea191899/scratchpad/cap/ar3'
A = App(CAP)
FL = Flow(A, B, O.BG_RED, {'tiles': 'Pick your tiles: Dear Santa', 'mats': 'Swipe her Anders Ruff matches',
                          'suitors': 'Your suitors', 'zoom': 'Zoom in on the mat  + + +', 'racks': 'Now swipe racks',
                          'card': "It's a match! Your match card", 'shop': 'Shop it all in one list',
                          'rack_names': ['Peace Love Mahjong Oak', 'Bird & Bamboo Red', 'Bird & Bamboo Evergreen']})
NSW = 4
# timeline in beats
T_LOOKS, T_APP1 = 2, 9
T_GRID = T_APP1 + FL.len1(NSW)          # 16
T_APP2 = T_GRID + 2                      # 18
T_END = T_APP2 + Flow.LEN2               # 27.5
NB = T_END + 3.5                         # 31 beats = 19.4 s
DUR = NB * B

def hook(t):
    c = O.BG_RED.copy(); d = ImageDraw.Draw(c); sparkles(d, t, n=50, seed=4, col=(255, 226, 170))
    p = back_out(t / (B * 0.8)); y = lerp(-700, 640, p)
    shadow_paste(c, O.HOOK_POL, (W // 2 - O.HOOK_POL.width // 2, y), rot=-4 + 2 * math.sin(t / B * math.pi), alpha=150)
    d = ImageDraw.Draw(c)
    draw_center(d, 270, 'Dear Santa,', O.f_cav, (255, 244, 230), shadow=(0, 6, (90, 8, 16)))
    if t >= B * 0.5: draw_center(d, 450, 'what do I wear', O.f_cap70, (255, 244, 230), shadow=(0, 5, (90, 8, 16)))
    if t >= B * 1.0: draw_center(d, 540, 'to Christmas?', O.f_cap70, (255, 214, 120), shadow=(0, 5, (90, 8, 16)))
    return c

def end(t, te):
    c = O.BG_RED.copy(); d = ImageDraw.Draw(c); snow(d, t, n=60, seed=5, col=(255, 240, 236))
    p1 = back_out(clamp(te / 0.25))
    draw_center(d, 280, 'Dear Santa has', O.f_cap70, (255, 244, 230), shadow=(0, 5, (90, 8, 16)))
    sz = int(170 * (0.7 + 0.3 * p1))
    draw_center(d, 380 + (170 - sz) // 2, '27 matches', font(FONT_CAP, sz), (255, 214, 120), shadow=(0, 7, (90, 8, 16)))
    draw_runs_center(d, 600, [('in Find ', O.f_cap70), ('Your', font(FONT_PLAY_I, 72)), (' Mat-ch™', O.f_cap70)], (255, 244, 230), shadow=(0, 5, (90, 8, 16)))
    sm = 136; gap = 8; x0 = W // 2 - (7 * sm + 6 * gap) // 2
    for j, m in enumerate(O.MATS):
        pj = back_out(clamp((te - 0.5 * B - j * 0.04) / 0.2))
        if pj <= 0: continue
        s2 = max(4, int(sm * pj)); shadow_paste(c, rounded(m.resize((s2, s2), Image.LANCZOS), 10), (x0 + j * (sm + gap) + (sm - s2) // 2, 750 + (sm - s2) // 2), alpha=120, blur=10, offset=(0, 6))
    d = ImageDraw.Draw(c)
    y = 930
    for ln in ['Anders Ruff’s 8 Christmas mats,', 'matched 93 times with 35 tile sets']:
        draw_center(d, y, ln, font(FONT_POP_B, 42), (255, 236, 224)); y += 62
    if te >= B:
        pill(d, W // 2, 1100, 'Shop now · use code MAHJMATCH', font(FONT_POP_B, 46), (255, 255, 255), PINK, padx=44, pady=22)
        draw_center(d, 1240, 'Preorders open · mats ship early November · link in bio', font(FONT_POP_M, 30), (255, 236, 224))
        draw_center(d, 1330, 'mahjmatchmaker.com', font(FONT_CAP, 54), (255, 244, 230))
    return c

def draw(t):
    b = t / B
    if b < T_LOOKS: return hook(t)
    if b < T_APP1:
        k = min(6, int(b - T_LOOKS)); return O.look(t, k, (b - T_LOOKS - k) * B)
    if b < T_GRID: return FL.f1(b - T_APP1, NSW)
    if b < T_APP2: return O.grid(t, (b - T_GRID) * B * 2.8)
    if b < T_END: return FL.f2(b - T_APP2)
    return end(t, (b - T_END) * B)

if __name__ == '__main__':
    OUT = O.OUT
    if '--only' in sys.argv:
        for tt in [float(x) for x in sys.argv[sys.argv.index('--only') + 1].split(',')]:
            draw(tt).save(f'/dev/shm/brand-reshare/ar2_{tt:05.2f}.jpg', quality=88)
        sys.exit()
    R = Renderer('ar2', DUR); R.run(draw)
    cuts = [x * B for x in [T_LOOKS, T_APP1, T_GRID, T_APP2, T_END]]
    click_track('/dev/shm/brand-reshare/ar_click.wav', DUR, O.BPM, marks=cuts)
    R.encode(f'{OUT}/ar-outfit-change-reel.mp4', '/dev/shm/brand-reshare/ar_click.wav', f'{OUT}/ar-outfit-change-reel-BEATTEST.mp4')
    O.grid(0, 4 * B).save(f'{OUT}/ar-outfit-change-cover.jpg', quality=90)
    R.cleanup()
    contact_sheet(f'{OUT}/ar-outfit-change-reel.mp4', f'{OUT}/ar-outfit-change-contact.jpg')
