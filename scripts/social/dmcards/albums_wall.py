"""Rainbow album wall (Tiffany Nov 23 8:07pm): every LIVE album cover once, no repeats, no unreleased sets, no
Cypress/Mahjong Row, real 4:5 proportions (never squashed), sorted into a rainbow; center badge in brand colours.
Usage: albums_wall.py <out.jpg> [W H]   (renders at 2x then downsamples so it is crisp at its real size)"""
import os, re, sys, random, colorsys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
R = '/home/claude/mahjmatchmaker-data/'; F = R + 'scripts/social/tileprofile/fonts/'
out = sys.argv[1]; OW, OH = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (1200, 628)
S = 2; W, H = OW * S, OH * S
live = set(re.findall(r'com/(.+?)-mahjong-tile-matches', open(R + 'config/album-urls.txt').read()))
live |= {'papaya-spritz', 'spring-love', 'petalee', 'preppy-soiree', 'brownstone-bloom', 'juniper', 'deco-lagoon', 'lilac-soiree'}
live -= {'cypress-forest'}
D = R + 'assets/covers/albums/w800/'; covers = []
for f in sorted(os.listdir(D)):
    m = re.match(r'\d+-(.+?)-mahjong-tiles', f)
    if m and m.group(1) in live: covers.append(D + f)
def hue(p):
    im = Image.open(p).convert('RGB').resize((40, 50)); px = list(im.getdata()); hs = []
    for r, g, b in px:
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        if s > .25 and v > .25: hs.append(h)
    if not hs: return 0.995
    hs.sort(); h = hs[len(hs) // 2]
    return (h + 0.08) % 1.0   # start the rainbow at pink/red
covers.sort(key=hue)
random.seed(7)
rows = 4 if OW / OH > 1.5 else 6
cols = -(-len(covers) // rows)
cw, ch = W / cols, H / rows
ch_cov = int(ch * 1.28); cw_cov = int(ch_cov * 0.8)
bg = Image.new('RGB', (W, H), (240, 232, 226)); canvas = bg.convert('RGBA')
cells = [(c, r) for c in range(cols) for r in range(rows)]
for i, p in enumerate(covers):
    c, r = cells[i]
    im = Image.open(p).convert('RGB'); im = im.resize((cw_cov, int(cw_cov * im.height / im.width)), Image.LANCZOS)
    b = 10 * S // 2; card = Image.new('RGBA', (im.width + 2 * b, im.height + 2 * b), (255, 255, 255, 255)); card.paste(im, (b, b))
    m = Image.new('L', card.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, card.width - 1, card.height - 1), 14 * S // 2, fill=255); card.putalpha(m)
    card = card.rotate(random.uniform(-7, 7), Image.BICUBIC, expand=True)
    x = int(c * cw + cw / 2 - card.width / 2 + random.uniform(-.12, .12) * cw); y = int(r * ch + ch / 2 - card.height / 2 + random.uniform(-.1, .1) * ch)
    sh = Image.new('RGBA', canvas.size, (0, 0, 0, 0)); sh.paste((20, 10, 30, 80), (x + 4 * S, y + 8 * S), card.split()[3])
    canvas.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7 * S))); canvas.alpha_composite(card, (x, y))
# center badge
NAVY = (5, 70, 137); PINK = (200, 50, 95); CREAM = (253, 248, 246)
bw, bh = int(W * .44), int(H * .44); x0, y0 = (W - bw) // 2, (H - bh) // 2
sh = Image.new('RGBA', canvas.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((x0, y0 + 12 * S, x0 + bw, y0 + bh + 12 * S), 26 * S, fill=(10, 20, 50, 120))
canvas.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14 * S)))
d = ImageDraw.Draw(canvas)
d.rounded_rectangle((x0, y0, x0 + bw, y0 + bh), 26 * S, fill=CREAM)
d.rounded_rectangle((x0 + 9 * S, y0 + 9 * S, x0 + bw - 9 * S, y0 + bh - 9 * S), 20 * S, outline=NAVY, width=4 * S)
wm = Image.open(R + 'assets/brand/mahjmatchmaker-wordmark-notag.png').convert('RGBA'); ww = int(bw * .8); wm = wm.resize((ww, int(wm.height * ww / wm.width)), Image.LANCZOS)
canvas.alpha_composite(wm, ((W - ww) // 2, y0 + int(bh * .13)))
bit = lambda n, w=700: ImageFont.truetype(F + ('bitter-latin-700-normal.woff2' if w == 700 else 'bitter-latin-600-normal.woff2'), n)
cap = lambda n: ImageFont.truetype(F + 'Caprasimo.ttf', n)
t = 'MATCHING MAHJONG TILES, MATS & RACKS'; f = bit(int(bh * .062)); sp = 2 * S
tw = sum(d.textlength(ch_, font=f) + sp for ch_ in t) - sp; py = y0 + int(bh * .47); hh = int(bh * .13)
d.rounded_rectangle(((W - tw) / 2 - 18 * S, py, (W + tw) / 2 + 18 * S, py + hh), hh // 2, fill=PINK)
x = (W - tw) / 2
for ch_ in t: d.text((x, py + hh / 2), ch_, font=f, fill=(255, 255, 255), anchor='lm'); x += d.textlength(ch_, font=f) + sp
d.text((W / 2, y0 + int(bh * .76)), f'{len(covers)}+ tile set albums and counting'.replace(f'{len(covers)}+', '40+'), font=cap(int(bh * .095)), fill=PINK, anchor='mm')
d.text((W / 2, y0 + int(bh * .89)), 'mahjmatchmaker.com', font=bit(int(bh * .075), 600), fill=NAVY, anchor='mm')
img = canvas.convert('RGB').resize((OW, OH), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.0, 60, 2))
img.save(out, quality=93); print(out, len(covers), 'covers')
