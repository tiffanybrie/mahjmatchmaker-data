#!/usr/bin/env python3
"""Holiday table reels v2 (Tiffany Nov 6 2026 1:24am: v1 used the full phone frame and stacked items unevenly).
Every element sits inside Instagram's reel SAFE ZONE and on an even grid. The build REFUSES (SystemExit) if any
element leaves the safe zone. Also writes <out>/<k>-safe-check.jpg (last frame with the safe zone drawn) to LOOK at.

Safe zone (1080x1920 reel): y 250..1480 (IG header above, caption/buttons below); right column x <= 900 for y >= 950
(like/comment/share buttons); x >= 60 on the left.
Usage: python3 scripts/social/holiday_tables_reel.py [rudolph|polo|rattan ...] -> assets/social/holiday-tables/<k>/<k>-holiday-table-reel.mp4
"""
import sys, os, subprocess, shutil, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = R + '/assets/blog/holiday-boards-oct21/src/'
OUT = R + '/assets/social/holiday-tables/'
W, H, FPS = 1080, 1920, 30
BG = (249, 245, 239)
INK = (34, 26, 30)
SAFE = dict(top=250, bottom=1480, left=60, right=1020, right_low=900, low_y=950)
F_LAB = SRC + 'HomemadeApple.ttf'
F_HEAD = R + '/assets/fonts/Caprasimo.ttf'

def font(p, s): return ImageFont.truetype(p, s)
def load(p): return Image.open(p).convert('RGBA')
def fit(im, w=None, h=None):
    if w and h:
        r = min(w / im.width, h / im.height)
    elif w: r = w / im.width
    else: r = h / im.height
    return im.resize((max(1, int(im.width * r)), max(1, int(im.height * r))), Image.LANCZOS)
def rounded(im, rad):
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), rad, fill=255)
    out = im.copy(); out.putalpha(m); return out
def card(p, w, h):
    im = load(p).convert('RGB'); r = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1), Image.LANCZOS)
    l, t = (im.width - w) // 2, (im.height - h) // 2; im = im.crop((l, t, l + w, t + h)).convert('RGBA')
    b = Image.new('RGBA', (w + 16, h + 16), (255, 255, 255, 255)); b.alpha_composite(im, (8, 8))
    return rounded(b, 18)
def shadowed(im, blur=14, off=(0, 10), alpha=70):
    pad = blur * 3; c = Image.new('RGBA', (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0))
    a = im.split()[-1].point(lambda v: v * alpha // 255)
    sh = Image.new('RGBA', im.size, (0, 0, 0, 255)); sh.putalpha(a)
    c.alpha_composite(sh, (pad + off[0], pad + off[1])); c = c.filter(ImageFilter.GaussianBlur(blur))
    c.alpha_composite(im, (pad, pad)); return c, pad

LOGO = fit(load(R + '/assets/brand/mahjmatchmaker-wordmark.png'), w=360)

# item: (key, kind, src, max_w, max_h, label)   kind: mat | card | cut
LOOKS = {
 'rudolph': dict(title="The Rackin' Rudolph Mat", sub=None, pill=(206, 32, 52), pillt=(255, 255, 255), titlec=(206, 32, 52),
    mat=('mat', 'mat_rr.jpg', 470, 470, "rackin' rudolph mat"),
    rows=[[('card', 'cloth_cherry.jpg', 230, 230, 'cherry red cloth'), ('cut', 'tiles_fan2.png', 250, 200, "rackin' rudolph tiles"), ('cut', 'rack_milkglass.png', 250, 200, 'milk glass racks')],
          [('cut', 'lamp_bow.png', 200, 250, 'the bow lamp'), ('cut', 'deer_box.png', 200, 250, 'reindeer dice box'), ('cut', 'coaster_marble.png', 170, 170, 'marble coaster')]],
    mid=None),
 'polo': dict(title='The Polo Club Mat', sub='holiday edition', pill=(6, 69, 135), pillt=(255, 255, 255), titlec=(214, 96, 140),
    mat=('mat', 'mat_clean.jpg', 340, 340, 'polo club mat'),
    rows=[[('card', R + '/assets/tiles/album/heritage.jpg', 170, 170, 'heritage tiles'), ('card', 'cloth60.jpg', 170, 170, 'hunter green cloth'), ('cut', 'rack_walnut.png', 240, 120, 'walnut racks')],
          [('cut', 'coaster1.png', 130, 130, 'cognac coaster'), ('cut', 'ringdish.png', 150, 150, 'tree ring dish')],
          [('cut', 'tree.png', 170, 180, 'a little tree'), ('cut', 'wreath.png', 190, 150, 'a candle wreath'), ('cut', 'lamp_green.png', 170, 190, 'a ribboned lamp')]],
    mid='pick one for the center'),
 'rattan': dict(title='The Rattan Mat', sub='retro holiday edition', pill=(0x5e, 0x65, 0x43), pillt=(0xfb, 0xf3, 0xe6), titlec=(0x5e, 0x65, 0x43),
    mat=('cut', 'rattan_clean.png', 470, 470, 'rattan mat'),
    rows=[[('card', R + '/assets/tiles/album/heritage.jpg', 220, 220, 'heritage tiles'), ('cut', 'clothE.png', 250, 200, 'red tartan cloth'), ('cut', 'rack_walnut.png', 250, 130, 'walnut racks')],
          [('cut', 'lamp_tree.png', 200, 250, 'ceramic tree lamp'), ('cut', 'dice_holly.png', 200, 200, 'holly dice dish'), ('cut', 'coaster_amber.png', 170, 170, 'amber coaster')]],
    mid=None),
}

def make(kind, src, mw, mh):
    p = src if src.startswith('/') else SRC + src
    if kind == 'card': return card(p, mw, mh)
    im = load(p); im = fit(im, w=mw, h=mh)
    if kind == 'mat': im = rounded(im.convert('RGBA'), int(im.width * 0.045))
    return im

def layout(k):
    L = LOOKS[k]; items = []
    y = SAFE['top']
    logo_xy = ((W - LOGO.width) // 2, y); y += LOGO.height + 18
    kind, src, mw, mh, lab = L['mat']; mat = make(kind, src, mw, mh)
    labf = font(F_LAB, 26)
    items.append(dict(img=mat, x=(W - mat.width) // 2, y=y + 44, label=lab, cx=W // 2, ly=y + 4, big=True))
    y = y + 44 + mat.height + 26
    rows = L['rows']; avail = SAFE['bottom'] - 92 - y   # leave room for the CTA pill
    midh = 44 if L['mid'] else 0
    rowh = (avail - midh) // len(rows)
    mid_y = None
    for ri, row in enumerate(rows):
        if L['mid'] and ri == len(rows) - 1:
            mid_y = y; y += midh
        right = SAFE['right_low']   # rows below the mat sit in the button band: keep x <= 900
        colw = (right - SAFE['left']) / len(row)
        for ci, (kind, src, mw, mh, lab) in enumerate(row):
            im = make(kind, src, mw, min(mh, rowh - 56))
            cx = int(SAFE['left'] + colw * (ci + 0.5))
            iy = y + (rowh - 56 - im.height) // 2
            items.append(dict(img=im, x=cx - im.width // 2, y=iy, label=lab, cx=cx, ly=y + rowh - 46, big=False))
        y += rowh
    pill_y = SAFE['bottom'] - 80
    return logo_xy, items, mid_y, pill_y

def draw_frame(k, t_items, logo_xy, items, mid_y, pill_y, show_mid, show_pill):
    L = LOOKS[k]; c = Image.new('RGBA', (W, H), BG + (255,)); d = ImageDraw.Draw(c)
    c.alpha_composite(LOGO, logo_xy)
    labf = font(F_LAB, 26)
    for it, a in zip(items, t_items):
        if a <= 0: continue
        s = 0.85 + 0.15 * min(1, a); im = it['img']
        if s != 1: im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)
        sp, pad = shadowed(im)
        if a < 1: sp.putalpha(sp.split()[-1].point(lambda v: int(v * a)))
        cx = it['x'] + it['img'].width // 2; cy = it['y'] + it['img'].height // 2
        c.alpha_composite(sp, (cx - im.width // 2 - pad, cy - im.height // 2 - pad))
        if a >= 1: d.text((it['cx'], it['ly']), it['label'], font=labf, fill=INK, anchor='ma')
    if show_mid and mid_y: d.text((480, mid_y + 4), LOOKS[k]['mid'], font=font(F_HEAD, 34), fill=LOOKS[k]['pill'], anchor='ma')
    if show_pill:
        f = font(F_HEAD, 34); a_, b_ = 'shop the whole table', 'LINK IN BIO'; gap = 44
        wa, wb = d.textlength(a_, font=f), d.textlength(b_, font=f); tw = wa + gap + wb
        cx = (SAFE['left'] + SAFE['right_low']) // 2; h = 74; x0 = cx - tw / 2
        d.rounded_rectangle((x0 - 40, pill_y, x0 + tw + 40, pill_y + h), h // 2, fill=L['pill'])
        d.text((x0, pill_y + h // 2), a_, font=f, fill=L['pillt'], anchor='lm')
        d.ellipse((x0 + wa + gap / 2 - 5, pill_y + h / 2 - 5, x0 + wa + gap / 2 + 5, pill_y + h / 2 + 5), fill=L['pillt'])
        d.text((x0 + wa + gap, pill_y + h // 2), b_, font=f, fill=L['pillt'], anchor='lm')
    return c.convert('RGB')

def cover(k, logo_xy):
    L = LOOKS[k]; c = Image.new('RGBA', (W, H), BG + (255,)); d = ImageDraw.Draw(c)
    c.alpha_composite(LOGO, logo_xy)
    # title block first (upper safe band, full width allowed), then the mat (centred, narrow enough for the button column)
    y = logo_xy[1] + LOGO.height + 40
    f = font(F_HEAD, 52); txt = "How I'm Styling"; tw = d.textlength(txt, font=f)
    d.rounded_rectangle((W / 2 - tw / 2 - 50, y, W / 2 + tw / 2 + 50, y + 100), 50, fill=L['pill'])
    d.text((W / 2, y + 50), txt, font=f, fill=L['pillt'], anchor='mm')
    tf = font(F_HEAD, 62); ttw = d.textlength(L['title'], font=tf)
    d.text((W / 2, y + 125), L['title'], font=tf, fill=L['titlec'], anchor='ma')
    bottom = y + 205
    if L['sub']: d.text((W / 2, y + 205), L['sub'], font=font(F_LAB, 36), fill=INK, anchor='ma'); bottom = y + 285
    y0 = bottom + 40; side = min(560, SAFE['bottom'] - 20 - y0)
    kind, src, *_ = L['mat']; mat = make(kind, src, side, side)
    sp, pad = shadowed(mat); mx = (W - mat.width) // 2
    c.alpha_composite(sp, (mx - pad, y0 - pad))
    return c.convert('RGB'), [(mx, y0, mx + mat.width, y0 + mat.height), (W / 2 - max(ttw, tw + 100) / 2, y, W / 2 + max(ttw, tw + 100) / 2, bottom)]

def check_safe(k, boxes):
    bad = []
    for name, (x0, y0, x1, y1) in boxes:
        if y0 < SAFE['top'] or y1 > SAFE['bottom'] or x0 < SAFE['left'] or x1 > SAFE['right']: bad.append((name, (x0, y0, x1, y1)))
        elif y1 > SAFE['low_y'] and x1 > SAFE['right_low']: bad.append((name + ' (in the button column)', (x0, y0, x1, y1)))
    if bad:
        raise SystemExit(f'{k}: SAFE ZONE FAIL: ' + '; '.join(f'{n} {b}' for n, b in bad))

def build(k):
    logo_xy, items, mid_y, pill_y = layout(k)
    labf = font(F_LAB, 26); dd = ImageDraw.Draw(Image.new('RGB', (10, 10)))
    boxes = [('logo', (logo_xy[0], logo_xy[1], logo_xy[0] + LOGO.width, logo_xy[1] + LOGO.height))]
    for it in items:
        boxes.append((it['label'], (it['x'], it['y'], it['x'] + it['img'].width, it['y'] + it['img'].height)))
        tw = dd.textlength(it['label'], font=labf); boxes.append((it['label'] + ' label', (it['cx'] - tw / 2, it['ly'], it['cx'] + tw / 2, it['ly'] + 44)))
    f = font(F_HEAD, 34); tw = dd.textlength('shop the whole table', font=f) + 44 + dd.textlength('LINK IN BIO', font=f); cx = (SAFE['left'] + SAFE['right_low']) // 2
    boxes.append(('CTA pill', (cx - tw / 2 - 40, pill_y, cx + tw / 2 + 40, pill_y + 74)))
    cov, cboxes = cover(k, logo_xy); boxes += [('cover mat', cboxes[0]), ('cover title', cboxes[1])]
    check_safe(k, boxes)
    fd = f'/tmp/hreel_{k}/'; shutil.rmtree(fd, ignore_errors=True); os.makedirs(fd)
    n = 0
    def save(im, reps):
        nonlocal n
        for _ in range(reps): im.save(f'{fd}{n:05d}.jpg', quality=92); n += 1
    save(cov, int(1.8 * FPS))
    step = 0.55; per = int(step * FPS); N = len(items)
    for i in range(N):
        for f_ in range(per):
            a = [1.0 if j < i else (f_ + 1) / per if j == i else 0 for j in range(N)]
            save(draw_frame(k, a, logo_xy, items, mid_y, pill_y, show_mid=(i >= N - 3), show_pill=False), 1)
    final = draw_frame(k, [1] * N, logo_xy, items, mid_y, pill_y, True, True)
    save(final, int(2.6 * FPS))
    out = f'{OUT}{k}/{k}-holiday-table-reel.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', fd + '%05d.jpg', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-movflags', '+faststart', out], check=True)
    # safe-zone overlay check image (to LOOK at)
    ov = final.copy().convert('RGBA'); o = Image.new('RGBA', ov.size, (0, 0, 0, 0)); od = ImageDraw.Draw(o)
    od.rectangle((0, 0, W, SAFE['top']), fill=(255, 0, 0, 70)); od.rectangle((0, SAFE['bottom'], W, H), fill=(255, 0, 0, 70))
    od.rectangle((SAFE['right_low'], SAFE['low_y'], W, SAFE['bottom']), fill=(255, 0, 0, 70))
    ov.alpha_composite(o); ov.convert('RGB').resize((540, 960)).save(f'{OUT}{k}/{k}-safe-check.jpg', quality=85)
    final.save(f'{OUT}{k}/{k}-reel-final-frame.jpg', quality=90)
    print(k, 'OK', out, f'{n / FPS:.1f}s', 'safe zone PASS')

if __name__ == '__main__':
    for k in (sys.argv[1:] or ['rudolph', 'polo', 'rattan']): build(k)
