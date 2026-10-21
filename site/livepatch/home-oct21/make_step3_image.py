#!/usr/bin/env python3
"""Step 3 "Get New Matches First" image for the homepage How It Works row.

v2 (Tiffany, Oct 21 2:05pm): "bigger, no pink background" -> TRANSPARENT PNG, cropped tight to
the fan of the newest album covers (only a small margin for the soft shadows), so the fan "just
hangs there" on the section's own background (#FDF0E6 at 390/1280/1440). The fan's bounding box
is tuned to ~522x382 (step 1's image column on desktop) so object-fit:contain fills the column;
on phones it shows at full width with its natural height, so no cover is clipped.
v1 (Oct 21 12:22) was a 1200x880 JPG on blush with a lot of empty pink.
"""
import os
from PIL import Image, ImageDraw, ImageFilter

R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
C = os.path.join(R, 'assets/covers/albums/w800/')
OUT = os.path.join(R, 'assets/site/home/how-it-works-3-new-matches-first.png')
TARGET_AR = 522 / 382          # step 1's image column at 1280
OUT_W = 1200                   # 2.3x the 522px desktop column, sharp on retina
W, H = 2600, 2000              # work canvas, cropped afterwards
covers = ['00-osler', '00-talulah', '00-coquette', '00-seabreeze', '00-smith']  # centre = newest (Coquette)
rots = [15, 7.5, 0, -7.5, -15]
cw = 640                       # cover width on the work canvas
SH_BLUR, SH_DX, SH_DY, SH_A = 22, 8, 22, 0.30
SH_RGB = (96, 52, 40)          # warm brown shadow, reads soft on the peach section background


def card(path):
    im = Image.open(path).convert('RGB'); ch = int(cw * im.height / im.width)
    im = im.resize((cw, ch), Image.LANCZOS)
    pad = 18
    c = Image.new('RGBA', (cw + 2 * pad, ch + 2 * pad), (255, 255, 255, 255)); c.paste(im, (pad, pad))
    m = Image.new('L', c.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, c.width - 1, c.height - 1), 26, fill=255)
    c.putalpha(m)
    return c


def render(spread):
    xs = [-2 * spread, -spread, 0, spread, 2 * spread]
    canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for i in [0, 4, 1, 3, 2]:  # outer cards first, centre last
        c = card(C + covers[i] + '-mahjong-tiles-cover.jpg').rotate(rots[i], expand=True, resample=Image.BICUBIC)
        a = c.getchannel('A')
        sh = Image.new('RGBA', c.size, SH_RGB + (0,))
        sh.putalpha(a.point(lambda v: int(v * SH_A)))
        # blur on a padded layer so the shadow is not clipped at the card's own box
        p = SH_BLUR * 3
        shp = Image.new('RGBA', (c.width + 2 * p, c.height + 2 * p), SH_RGB + (0,))
        shp.alpha_composite(sh, (p, p))
        shp = shp.filter(ImageFilter.GaussianBlur(SH_BLUR))
        cx = W // 2 + xs[i]; cy = H // 2 + abs(xs[i]) // 5
        canvas.alpha_composite(shp, (cx - c.width // 2 - p + SH_DX, cy - c.height // 2 - p + SH_DY))
        canvas.alpha_composite(c, (cx - c.width // 2, cy - c.height // 2))
    # tight crop: alpha > ~2% keeps the visible shadow, drops the invisible tail
    bbox = canvas.getchannel('A').point(lambda v: 255 if v > 5 else 0).getbbox()
    return canvas.crop(bbox)


# pick the card spread whose fan box is closest to the desktop column's shape
fans = {s: render(s) for s in range(200, 420, 10)}
best = min(fans, key=lambda s: abs(fans[s].width / fans[s].height - TARGET_AR))
fan = fans[best]
out = fan.resize((OUT_W, round(OUT_W * fan.height / fan.width)), Image.LANCZOS)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
out.save(OUT, optimize=True)
print(OUT, out.size, 'spread', best, 'ar %.3f' % (out.width / out.height), os.path.getsize(OUT) // 1024, 'KB')
