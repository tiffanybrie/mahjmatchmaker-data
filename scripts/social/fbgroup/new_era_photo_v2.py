"""FB group NEW ERA post photo preview v2 (Oct 21): same layout as fb-new-era-photo-preview.jpg
(1200x1005: group-cover-style badge over an album collage on top, then FB's 4-tile row with "+N"),
rebuilt with the uniform album covers (frame3, white logos, flame-heart wordmark, FIND YOUR MATCH).
Top: v7 badge (same code as scripts/brand/group_cover_stacked.py) over a rainbow collage of every uniform cover.
Bottom: first 4 of the 13 new albums in post order; the last tile carries +N (photos beyond the 5 shown).
Usage: python3 new_era_photo_v2.py <uniform_covers_dir> <out.jpg>"""
import sys, os, glob, colorsys, random, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
R = '/home/claude/mahjmatchmaker-data/'; CV = sys.argv[1].rstrip('/') + '/'; OUT = sys.argv[2]
NEW = ['pippa', 'smith', 'osler', 'talulah', 'seabreeze', 'coquette', 'cypress-forest', 'sunday-tile-set',
       'shangri-la', 'lilac-soiree', 'preppy-soiree', 'spring-love', 'papaya-spritz']
# newest file per album (Papaya's committed uniform cover is newer than the batch run)
OVR = {'papaya-spritz': R + 'assets/covers/albums/v2/00-papaya-spritz-mahjong-tiles-cover-uniform.jpg'}
def path(k): return OVR.get(k, CV + k + '.jpg')
keys = sorted(os.path.basename(f)[:-4] for f in glob.glob(CV + '*.jpg'))
NAVY = (5, 70, 137); PINK = (214, 96, 140); CREAM = (253, 248, 246)
FONTS = R + 'scripts/social/tileprofile/fonts/'

# ---- top: rainbow collage of all uniform covers, 1640x856
def hue(k):
    a = np.asarray(Image.open(path(k)).convert('RGB').resize((108, 135)))[30:105, 15:93].reshape(-1, 3) / 255.
    a = a[a.min(axis=1) < 0.85]                # drop the white logo/title/frame ink
    r, g, b = np.median(a, axis=0); h, l, s = colorsys.rgb_to_hls(r, g, b)
    if s < 0.18: return 0.80 + l / 10          # greys/browns-low-sat go to the end
    return (h + 0.08) % 1.0                    # start at pink/red
order = sorted(keys, key=hue)
W, H = 1640, 856; cov = Image.new('RGBA', (W, H), (240, 232, 236, 255))
cw, ch = 210, 262; cols, rows = 11, 4; sx = (W + 60) / cols; sy = (H + 40) / rows
random.seed(7); slots = [(c, r) for c in range(cols) for r in range(rows)]
slots = [sl for sl in slots if sl != (5, 2)][:len(order)]   # one slot fully behind the badge: no duplicate cover
for i, (c, r) in enumerate(slots):
    k = order[i % len(order)]
    im = Image.open(path(k)).convert('RGB').resize((cw, ch), Image.LANCZOS)
    card = Image.new('RGBA', (cw + 12, ch + 12), (0, 0, 0, 0)); m = Image.new('L', card.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, cw + 11, ch + 11), 12, fill=255)
    card.paste((255, 255, 255, 255), (0, 0), m); card.paste(im, (6, 6))
    card = card.rotate(random.uniform(-7, 7), Image.BICUBIC, expand=True)
    x = int(-40 + c * sx + (sx - card.width) / 2 + random.uniform(-10, 10) + (r % 2) * 18)
    y = int(-30 + r * sy + (sy - card.height) / 2 + random.uniform(-8, 8))
    sh = Image.new('RGBA', cov.size, (0, 0, 0, 0)); a = card.split()[3].point(lambda v: v * 0.45)
    sh.paste((20, 20, 40, 255), (x + 4, y + 8), a); cov.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
    cov.alpha_composite(card, (x, y))
# badge (v7 group cover code, unchanged)
bw, bh = 684, 560; x0 = (W - bw) // 2; y0 = (H - bh) // 2
sh = Image.new('RGBA', cov.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((x0 + 6, y0 + 14, x0 + bw + 6, y0 + bh + 14), 48, fill=(10, 20, 50, 110)); cov.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16)))
d = ImageDraw.Draw(cov)
d.rounded_rectangle((x0, y0, x0 + bw, y0 + bh), 48, fill=PINK)
d.rounded_rectangle((x0 + 10, y0 + 10, x0 + bw - 10, y0 + bh - 10), 40, fill=CREAM)
d.rounded_rectangle((x0 + 22, y0 + 22, x0 + bw - 22, y0 + bh - 22), 32, outline=NAVY, width=6)
av = Image.open(R + 'assets/brand/fb-page/mahj-matchmaker-page-profile-1080.jpg').convert('RGB').crop((120, 215, 975, 880))
a = np.asarray(av).astype(int); m = (a.min(axis=2) < 235).astype('uint8') * 255
lg = av.convert('RGBA'); lg.putalpha(Image.fromarray(m).filter(ImageFilter.GaussianBlur(0.8)))
lw = 430; lg = lg.resize((lw, int(lg.height * lw / lg.width)), Image.LANCZOS)
cov.alpha_composite(lg, ((W - lw) // 2 + 10, y0 + 42))
try: f1 = ImageFont.truetype('/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf', 19)
except Exception: f1 = ImageFont.load_default()
txt = 'MATCHING MAHJONG TILES, MATS & RACKS'; sp = 3
tw = sum(d.textlength(c, font=f1) + sp for c in txt) - sp; py = y0 + bh - 140
d.rounded_rectangle(((W - tw) / 2 - 26, py, (W + tw) / 2 + 26, py + 46), 23, fill=PINK)
x = (W - tw) / 2
for c in txt: d.text((x, py + 11), c, font=f1, fill=(255, 255, 255)); x += d.textlength(c, font=f1) + sp
d.text((W / 2, py + 76), '40+ tile set albums  |  mahjmatchmaker.com', font=ImageFont.truetype(FONTS + 'Caprasimo.ttf', 25), fill=NAVY, anchor='mm')
top = cov.convert('RGB')
top.save(os.path.splitext(OUT)[0] + '-photo1.jpg', quality=92)   # uploadable first photo (1640x856)

# ---- preview: 1200x1005, FB 5-photo layout
P = Image.new('RGB', (1200, 1005), (255, 255, 255)); G = 4; TH = 624
P.paste(top.resize((1200, TH), Image.LANCZOS), (0, 0))
tw_, th_ = (1200 - 3 * G) // 4, 1005 - TH - G
nphotos = 1 + len(NEW); more = nphotos - 5
for i, k in enumerate(NEW[:4]):
    im = Image.open(path(k)).convert('RGB'); s = th_ / im.height
    im = im.resize((round(im.width * s), th_), Image.LANCZOS); cx = (im.width - tw_) // 2
    im = im.crop((cx, 0, cx + tw_, th_))
    if i == 3 and more > 0:
        im = Image.blend(im, Image.new('RGB', im.size, (0, 0, 0)), 0.45); dd = ImageDraw.Draw(im)
        try: fp = ImageFont.truetype('/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf', 76)
        except Exception: fp = ImageFont.load_default()
        dd.text((tw_ / 2, th_ / 2), f'+{more}', font=fp, fill=(255, 255, 255), anchor='mm')
    P.paste(im, (i * (tw_ + G), TH + G))
P.save(OUT, quality=92); print(OUT, 'photos in post:', nphotos, '+', more)
for k in NEW: print(k, path(k))
