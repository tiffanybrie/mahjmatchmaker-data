"""Replace banned B&B wood bars on existing album cards.
Style A (B&B logo panel with painted bars): the wood bar is repainted as a B&B paint bar (Almond -> Cream)
or swapped for a real-wood rack photo (dark woods -> Bam Bird Boutique Walnut), label redrawn.
Style B (RACK MATCHES panel): the wood rack image above the caption is replaced the same way and the caption rewritten."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
R = '/home/claude/mahjmatchmaker-data/'
FB = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
FSB = '/usr/share/fonts/truetype/google-fonts/Poppins-SemiBold.ttf'
NAVY = (31, 45, 92)
WALNUT = R + 'assets/racks/card/bam-bird-boutique-walnut.png'
CREAM = (0xD1, 0xCA, 0xBE)

def rows_uniform(a, x0, x1, thr=14):
    seg = a[:, x0:x1].astype(int)
    return seg.std(axis=1).mean(axis=1) < thr

def bar_box_A(a, wx, wy, ww, wh):
    cy = wy + wh // 2
    u = rows_uniform(a, 985, 1055)
    if not u[cy]:
        # label text never reaches the right side; search nearby rows
        cands = [y for y in range(cy - 12, cy + 13) if u[y]]
        if not cands: return None
        cy = min(cands, key=lambda y: abs(y - cy))
    y0 = cy
    while y0 > 0 and u[y0 - 1] and cy - y0 < 21: y0 -= 1
    y1 = cy
    while u[y1 + 1] and y1 - cy < 21: y1 += 1
    prof = a[y0:y1 + 1, 1020:1040].astype(int).mean(axis=1)
    x1 = 1040
    while x1 < 1079 and np.abs(a[y0:y1 + 1, x1 + 1].astype(int) - prof).mean() < 28: x1 += 1
    x0 = 1020
    while x0 > 600 and (x0 > wx - 4 or np.abs(a[y0:y1 + 1, x0 - 1].astype(int) - prof).mean() < 28): x0 -= 1
    return (x0, y0 - 1, x1 + 1, y1 + 2)

def paint_bar(size, rgb, template_col):
    """Rack-profile bar: shading from a clean column of an existing light bar, tinted to rgb."""
    w, h = size
    col = np.asarray(Image.fromarray(template_col).resize((1, h)).convert('L')).astype(float)[:, 0]
    sh = col / max(col.max(), 1)
    sh = 0.62 + 0.42 * (sh - sh.min()) / max(sh.max() - sh.min(), 1e-6)
    arr = np.clip(np.array(rgb)[None, None, :] * sh[:, None, None] * np.ones((1, w, 1)), 0, 255).astype(np.uint8)
    im = Image.fromarray(arr)
    d = ImageDraw.Draw(im)
    d.line([(0, h - 1), (w, h - 1)], fill=tuple(int(c * .55) for c in rgb), width=2)
    d.line([(0, 0), (0, h)], fill=tuple(int(c * .7) for c in rgb), width=2)
    d.line([(w - 2, 0), (w - 2, h)], fill=tuple(int(c * .7) for c in rgb), width=2)
    return im

def photo_bar(size, path=WALNUT):
    w, h = size
    r = Image.open(path).convert('RGBA')
    bb = r.getbbox(); r = r.crop(bb)
    r = r.resize((w, max(h, int(r.height * w / r.width))))
    # crop the vertical middle to the bar height
    t = (r.height - h) // 2
    return r.crop((0, t, w, t + h))

def fit_font(text, path, maxw, start):
    s = start
    while s > 12:
        f = ImageFont.truetype(path, s)
        if f.getlength(text) <= maxw: return f
        s -= 1
    return ImageFont.truetype(path, 12)

def draw_label(im, xy, text, size, color, maxw, shadow):
    d = ImageDraw.Draw(im)
    f = fit_font(text, FB, maxw, size)
    if shadow:
        sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
        ds.text((xy[0], xy[1] + 1), text, font=f, fill=(0, 0, 0, 120), anchor='lm')
        sh = sh.filter(ImageFilter.GaussianBlur(1.5)); im.alpha_composite(sh)
        d = ImageDraw.Draw(im)
    d.text(xy, text, font=f, fill=color, anchor='lm')

def patch_A(im, a, hit, repl, tmpl_col):
    k, wx, wy, ww, wh, st = hit
    box = bar_box_A(a, wx, wy, ww, wh)
    if not box: return None
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    if not (200 < w < 340 and 22 < h < 52): return ('badbox', box)
    if repl['kind'] == 'paint':
        bar = paint_bar((w, h), repl['rgb'], tmpl_col).convert('RGBA')
        im.alpha_composite(bar, (x0, y0))
        draw_label(im, (x0 + 17, y0 + h // 2 + 2), repl['label'], 31, NAVY, w - 30, False)
    else:
        bar = photo_bar((w, h))
        im.alpha_composite(bar, (x0, y0))
        draw_label(im, (x0 + 17, y0 + h // 2 + 1), repl['label'], 31, (255, 255, 255, 255), w - 30, True)
    return box

BITTER = '/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/qafix/Bitter-Bold.ttf'

def patch_C(im, a, hit, repl, tmpl_col):
    """Holiday-card pill bar (card2.html #bb .bar): 34px tall, label 'Bird & Bamboo X' in Bitter 18px."""
    k, wx, wy, ww, wh, st = hit
    cy = wy + wh // 2
    u = rows_uniform(a, 1040, 1072, 12)
    cands = [y for y in range(cy - 8, cy + 9) if u[y]]
    if not cands: return None
    cy = min(cands, key=lambda y: abs(y - cy))
    y0 = cy
    while u[y0 - 1] and cy - y0 < 30: y0 -= 1
    y1 = cy
    while u[y1 + 1] and y1 - cy < 30: y1 += 1
    prof = a[y0:y1 + 1, 1050:1060].astype(int).mean(axis=1)
    x0 = 1050
    while x0 > 700 and (x0 > wx - 4 or np.abs(a[y0:y1 + 1, x0 - 1].astype(int) - prof).mean() < 30): x0 -= 1
    x1 = 1079
    w, h = x1 - x0, y1 - y0 + 1
    if not (200 < w < 380 and 24 < h < 46): return ('badbox', (x0, y0, x1, y1))
    if repl['kind'] == 'paint':
        bar = paint_bar((w, h), repl['rgb'], tmpl_col).convert('RGBA'); col = NAVY + (255,) if sum(repl['rgb']) > 480 else (255, 255, 255, 255)
    else:
        bar = photo_bar((w, h)); col = (255, 255, 255, 255)
    im.alpha_composite(bar, (x0, y0))
    d = ImageDraw.Draw(im)
    f = fit_font(repl['label_full'], BITTER, w - 24, 18)
    if col[0] == 255:
        sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).text((x0 + 12, y0 + h / 2 + 1), repl['label_full'], font=f, fill=(0, 0, 0, 140), anchor='lm')
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(1.2))); d = ImageDraw.Draw(im)
    d.text((x0 + 12, y0 + h / 2), repl['label_full'], font=f, fill=col, anchor='lm')
    return (x0, y0, x1, y1)

def patch_B(im, a, hit, repl, tmpl_col):
    """RACK MATCHES panel: rack image sits above its caption; caption 'Bird & Bamboo X' left-aligned."""
    k, wx, wy, ww, wh, st = hit
    bg = a[wy + wh // 2, 1066].astype(int)
    diff = lambda y, xa, xb: (np.abs(a[y, xa:xb].astype(int) - bg).sum(axis=1) > 60)
    # caption extent
    band = range(wy - 2, wy + wh + 3)
    cols = np.zeros(1080, bool)
    for y in band: cols[600:1079] |= diff(y, 600, 1079)
    cl = wx
    gap = 0
    while cl > 640:
        if cols[cl - 1]: gap = 0
        else:
            gap += 1
            if gap > 22: break
        cl -= 1
    cl += gap
    # rack image above: rows with many differing pixels
    y = wy - 4
    while y > wy - 20 and diff(y, cl, 1050).sum() < 40: y -= 1
    ry1 = y
    while ry1 - y < 70 and diff(y, cl - 10, 1060).sum() >= 40: y -= 1
    ry0 = y + 1
    if not (14 < ry1 - ry0 < 70): return ('badrack', (ry0, ry1))
    xs = np.where(np.mean([diff(yy, cl - 20, 1066) for yy in range(ry0, ry1 + 1)], axis=0) > 0.5)[0] + cl - 20
    rx0, rx1 = int(xs.min()), int(xs.max())
    d = ImageDraw.Draw(im)
    bgc = tuple(int(c) for c in bg) + (255,)
    d.rectangle([rx0 - 8, ry0 - 4, min(rx1 + 10, 1074), ry1 + 10], fill=bgc)
    d.rectangle([cl - 3, wy - 4, min(wx + ww + 12, 1074), wy + wh + 6], fill=bgc)
    rw, rh = rx1 - rx0, ry1 - ry0
    if repl['kind'] == 'paint':
        bar = paint_bar((rw, max(rh - 6, 18)), repl['rgb'], tmpl_col).convert('RGBA')
        shd = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(shd).rectangle([rx0 + 2, ry0 + 6, rx1, ry0 + 6 + bar.height], fill=(0, 0, 0, 90))
        im.alpha_composite(shd.filter(ImageFilter.GaussianBlur(4)))
        im.alpha_composite(bar, (rx0, ry0 + 2))
    else:
        r = Image.open(WALNUT).convert('RGBA'); r = r.crop(r.getbbox()); r = r.resize((rw, int(r.height * rw / r.width)))
        im.alpha_composite(r, (rx0, ry0 + (rh - r.height) // 2))
    d = ImageDraw.Draw(im)
    f = fit_font(repl['label_full'], FB, 1066 - cl, 22)
    d.text((cl, wy + wh / 2 + 1), repl['label_full'], font=f, fill=NAVY, anchor='lm')
    return (rx0, ry0, rx1, ry1)

def paint_pill(size, rgb):
    w, h = size
    t = np.linspace(0, 1, h)[:, None]
    hi = np.clip(1 - t / 0.4, 0, 1) * 0.28
    lo = np.clip((t - 0.4) / 0.6, 0, 1) * 0.18
    base = np.array(rgb, float)[None, :]
    col = base * (1 - hi) + 255 * hi
    col = col * (1 - lo)
    arr = np.repeat(col[:, None, :], w, axis=1).astype(np.uint8)
    im = Image.fromarray(arr).convert('RGBA')
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w + 6, h - 1], radius=3, fill=255)
    im.putalpha(m); return im

def patch_C(im, a, hit, repl, tmpl_col):
    k, wx, wy, ww, wh, st = hit
    cy = wy + wh // 2
    seg = a[:, 1056:1068].astype(int)
    u = seg.std(axis=1).mean(axis=1) < 6
    cands = [y for y in range(cy - 10, cy + 11) if u[y]]
    if not cands: return None
    cy = min(cands, key=lambda y: abs(y - cy))
    ref = a[:, 1062].astype(int)
    y0 = cy
    while y0 > cy - 22 and u[y0 - 1] and np.abs(ref[y0 - 1] - ref[y0]).sum() < 30: y0 -= 1
    y1 = cy
    while y1 < cy + 22 and u[y1 + 1] and np.abs(ref[y1 + 1] - ref[y1]).sum() < 30: y1 += 1
    # left edge: walk left along a row just below the text band where the pill is plain
    yy = y1 - 2
    c = a[yy, 1062].astype(int)
    x0 = 1062
    while x0 > 700 and (x0 > wx - 4 or np.abs(a[yy, x0 - 1].astype(int) - c).sum() < 45): x0 -= 1
    x1 = 1071
    if 1071 - x0 < 250: x0 = 821
    w, h = x1 - x0, y1 - y0 + 1
    if not (200 < w < 380 and 26 < h < 44): return ('badbox', (x0, y0, x1, y1))
    if repl['kind'] == 'paint':
        bar = paint_pill((w, h), repl['rgb']); dark = sum(repl['rgb']) < 480
    else:
        bar = photo_bar((w, h)); dark = True
    # wipe the old pill (incl. its drop shadow) with the pixels just right of it? keep simple: paint over exact box
    im.alpha_composite(bar, (x0, y0))
    d = ImageDraw.Draw(im)
    f = fit_font(repl['label_full'], BITTER, w - 26, 18)
    tx, ty = x0 + 12, y0 + h / 2
    if dark:
        sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).text((tx, ty + 1), repl['label_full'], font=f, fill=(0, 0, 0, 150), anchor='lm')
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(1.2))); d = ImageDraw.Draw(im)
        d.text((tx, ty), repl['label_full'], font=f, fill=(255, 255, 255, 255), anchor='lm')
    else:
        d.text((tx, ty), repl['label_full'], font=f, fill=(43, 43, 43, 255), anchor='lm')
    return (x0, y0, x1, y1)
