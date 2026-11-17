"""Tinselle Emerald tall reel cover (Nov 17), same method as dear-santa-push/cover/build_reel_cover.py: the album
cover design (gen3.py) as a true 9:16, tile photo full-bleed, card 285px lower. Stripe ring and the cream tag are
copied from the album cover; the EMERALD GREEN line is lifted from it as a mask (no Montserrat file here)."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np, sys
R = '/home/claude/tiffanybrie/mahjmatchmaker-data/'; HD = R + 'scripts/covers/holiday/'
W, H, DY = 1080, 1920, 285; CREAM = (251, 246, 238); PANEL = (14, 98, 60)
src = Image.open(R + 'assets/covers/holiday/bg/tinselle-emerald.jpg').convert('RGB')
s = max(W / src.width, H / src.height); bg = src.resize((round(src.width * s), round(src.height * s)), Image.LANCZOS)
x0 = (bg.width - W) // 2; y0 = (bg.height - H) // 2; im = bg.crop((x0, y0, x0 + W, y0 + H)).convert('RGBA')
alb = Image.open(R + 'assets/covers/holiday/tinselle-emerald.jpg').convert('RGBA')
ring = alb.crop((73, 267, 1007, 1083)); m = Image.new('L', ring.size, 255); ImageDraw.Draw(m).rectangle((14, 14, 919, 801), fill=0)
im.paste(ring, (73, 267 + DY), m)
im.alpha_composite(Image.new('RGBA', (906, 788), PANEL + (round(.88 * 255),)), (87, 281 + DY))
im.alpha_composite(Image.open(HD + 'frame2_gold.png').convert('RGBA'), (87, 281 + DY))
# tag: copy the cream box (with its logo) straight from the album cover, plus a soft shadow
tb = (382, 409, 698, 502)
sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((tb[0], tb[1] + DY + 4, tb[2], tb[3] + DY + 4), 14, fill=(0, 0, 0, 64)); im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7)))
tag = alb.crop(tb); tm = Image.new('L', tag.size, 0); ImageDraw.Draw(tm).rounded_rectangle((0, 0, tag.width - 1, tag.height - 1), 14, fill=255)
im.paste(tag, (tb[0], tb[1] + DY), tm)
F = ImageFont.truetype(R + 'scripts/social/tileprofile/fonts/Caprasimo.ttf', 118)
tl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(tl)
for t, top in (('Tinselle', 533), ('Tiles', 654)):
    b = F.getbbox(t); d.text((W / 2 - (b[0] + b[2]) / 2, top + DY - b[1]), t, font=F, fill=CREAM)
sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.putalpha(tl.getchannel('A').point(lambda v: v * 46 // 255))
im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4)).transform((W, H), Image.AFFINE, (1, 0, 0, 0, 1, -2)))
im.alpha_composite(tl)
# colourway line: alpha from the album pixels' brightness over the panel
cw = np.asarray(alb.convert('RGB').crop((330, 770, 750, 810))).astype(float)
a = np.clip((cw.min(2) - 95) / (240 - 95), 0, 1)
lay = Image.new('RGBA', (420, 40), CREAM + (0,)); lay.putalpha(Image.fromarray((a * 255).astype(np.uint8)))
im.alpha_composite(lay, (330, 770 + DY))
ol = Image.open(HD + 'ourlogo.png').convert('RGBA'); ol = ol.resize((500, round(ol.height * 500 / ol.width)), Image.LANCZOS)
im.alpha_composite(ol, ((W - 500) // 2, 950 + DY))
im.convert('RGB').save(sys.argv[1], quality=93); print(sys.argv[1])
