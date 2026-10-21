#!/usr/bin/env python3
"""Step 3 "Get New Matches First" image for the homepage How It Works row (Oct 21).
A fan of the newest album covers on brand blush, flame-heart mark. 1200x880 (shows as
~522x382 on desktop like step 1; content is centred so the phone crop (~0.84) keeps the fan)."""
import os
from PIL import Image, ImageDraw, ImageFilter
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
C = os.path.join(R, 'assets/covers/albums/w800/')
W, H = 1200, 880
bg = Image.new('RGBA', (W, H), (251, 227, 234, 255))
# soft paper glow in the middle
glow = Image.new('L', (W, H), 0); ImageDraw.Draw(glow).ellipse((240, 120, 960, 820), fill=150)
bg.alpha_composite(Image.new('RGBA', (W, H), (255, 246, 241, 255)), (0, 0)) if False else None
bg = Image.composite(Image.new('RGBA', (W, H), (255, 244, 239, 255)), bg, glow.filter(ImageFilter.GaussianBlur(120)))
covers = ['00-osler', '00-talulah', '00-coquette', '00-seabreeze', '00-smith']  # centre (index 2) = newest, coquette
rots = [14, 7, 0, -7, -14]
order = [0, 4, 1, 3, 2]  # draw outer cards first, centre last
xs = [-250, -125, 0, 125, 250]
cw = 320
def card(path):
    im = Image.open(path).convert('RGB'); ch = int(cw * im.height / im.width)
    im = im.resize((cw, ch), Image.LANCZOS)
    pad = 10; c = Image.new('RGBA', (cw + 2 * pad, ch + 2 * pad), (255, 255, 255, 255)); c.paste(im, (pad, pad))
    m = Image.new('L', c.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, c.width - 1, c.height - 1), 14, fill=255); c.putalpha(m)
    return c
for i in [0, 4, 1, 3, 2]:
    c = card(C + covers[i] + '-mahjong-tiles-cover.jpg').rotate(rots[i], expand=True, resample=Image.BICUBIC)
    sh = Image.new('RGBA', c.size, (90, 40, 60, 0)); sh.putalpha(c.getchannel('A').point(lambda v: int(v * .30)).filter(ImageFilter.GaussianBlur(14)))
    cx = W // 2 + xs[i]; cy = H // 2 + 10 + abs(xs[i]) // 5
    bg.alpha_composite(sh, (cx - c.width // 2 + 6, cy - c.height // 2 + 14))
    bg.alpha_composite(c, (cx - c.width // 2, cy - c.height // 2))
out = os.path.join(R, 'assets/site/home/how-it-works-3-new-matches-first.jpg')
bg.convert('RGB').save(out, quality=88, optimize=True, progressive=True); print(out)
