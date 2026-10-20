"""Oct 20 (Tiffany, asked 3x): every intro slide sits inside the SAME dating-profile card as slide 1, so the whole
carousel reads like swiping through her profile. Takes intro/1.jpg (the profile card on its peach background) as the
frame, blanks the card, draws the 7 progress bars (slide n active), drops slide n's content (its own top bars cropped
off) into a cream panel inside the card, and keeps slide 1's action buttons. Run after intro.py.
Usage: python3 intro_framed.py papaya-spritz  -> assets/social/<key>-launch/intro-framed/1..7.jpg"""
import sys, os
from PIL import Image, ImageDraw, ImageFilter
R = '/home/claude/mahjmatchmaker-data/'
key = sys.argv[1]; SRC = R + f'assets/social/{key}-launch/intro'; OUT = R + f'assets/social/{key}-launch/intro-framed'
os.makedirs(OUT, exist_ok=True)
base = Image.open(f'{SRC}/1.jpg').convert('RGB'); base.save(f'{OUT}/1.jpg', quality=93)
CX0, CY0, CX1, CY1, RAD = 140, 27, 938, 1273, 30          # the profile card on slide 1
strip = base.crop((0, 1188, 1080, 1350))                   # card bottom + action buttons
NAVY = (5, 70, 137)
for n in range(2, 8):
    c = Image.open(f'{SRC}/{n}.jpg').convert('RGB')
    cream = c.getpixel((8, 700))
    im = base.copy(); d = ImageDraw.Draw(im)
    d.rounded_rectangle((CX0, CY0, CX1, CY1), RAD, fill=(255, 255, 255))
    # progress bars, like the photo bars on slide 1
    bx0, bx1, by, gap, N = CX0 + 26, CX1 - 26, CY0 + 18, 8, 7
    bw = (bx1 - bx0 - gap * (N - 1)) / N
    for j in range(N):
        x = bx0 + j * (bw + gap)
        d.rounded_rectangle((x, by, x + bw, by + 6), 3, fill=NAVY if j + 1 == n else (214, 222, 233))
    # cream inner panel with the slide content
    px0, py0, px1, py1 = CX0 + 18, CY0 + 44, CX1 - 18, 1200
    panel = Image.new('RGB', (px1 - px0, py1 - py0), cream)
    content = c.crop((0, 62, 1080, 1350))
    sc = min((px1 - px0) / content.width, (py1 - py0) / content.height)
    content = content.resize((round(content.width * sc), round(content.height * sc)), Image.LANCZOS)
    panel.paste(content, ((panel.width - content.width) // 2, (panel.height - content.height) // 2))
    m = Image.new('L', panel.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, panel.width - 1, panel.height - 1), 22, fill=255)
    im.paste(panel, (px0, py0), m)
    im.paste(strip, (0, 1188))
    im.save(f'{OUT}/{n}.jpg', quality=93)
print(OUT)
