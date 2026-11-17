"""Dear Santa REEL cover (Nov 17, Tiffany: "the cover for the Dear Santa album that fits our covers and will look right
in my grid"). Same design as the holiday album cover (assets/covers/holiday/dear-santa.jpg from gen3.py: candy-stripe
border, gold corners, ar tag, Caprasimo title, mahjmatchmaker wordmark) as a true 9:16, the TALL=1 way: tile photo
full-bleed top to bottom (no blur bands, no mirrored tiles), the card 285px lower so the profile grid's 3:4 middle
shows the same card as the album cover. Drawn with PIL (this container's headless Chrome is gone); the stripe ring
is copied pixel for pixel from the album cover, everything else is rebuilt from the same files and sizes."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
R = '/home/claude/tiffanybrie/mahjmatchmaker-data/'; HD = R + 'scripts/covers/holiday/'
W, H, DY = 1080, 1920, 285; CREAM = (251, 246, 238); PANEL = (23, 87, 58)
import sys; FOC = float(sys.argv[2]) if len(sys.argv) > 2 else .5
src = Image.open(R + 'assets/covers/holiday/bg/dear-santa.jpg').convert('RGB')
s = H / src.height; bg = src.resize((round(src.width * s), H), Image.LANCZOS)
x0 = round((bg.width - W) * FOC); im = bg.crop((x0, 0, x0 + W, H)).convert('RGBA')
alb = Image.open(R + 'assets/covers/holiday/dear-santa.jpg').convert('RGBA')
ring = alb.crop((73, 267, 1007, 1083)); m = Image.new('L', ring.size, 255); ImageDraw.Draw(m).rectangle((14, 14, 919, 801), fill=0)
im.paste(ring, (73, 267 + DY), m)
pn = Image.new('RGBA', (906, 788), PANEL + (round(.88 * 255),)); im.alpha_composite(pn, (87, 281 + DY))
im.alpha_composite(Image.open(HD + 'frame2_gold.png').convert('RGBA'), (87, 281 + DY))
def shadow(box, r, off, blur, a):
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((box[0], box[1] + off, box[2], box[3] + off), r, fill=(0, 0, 0, a))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur / 2)))
lg = Image.open(R + 'assets/brand/partner-logos/ar.png').convert('RGBA'); lw = round(lg.width * 130 / lg.height); lg = lg.resize((lw, 130), Image.LANCZOS)
tw, th = lw + 44, 130 + 24; tx = (W - tw) // 2; ty = 405 + DY - 1
shadow((tx, ty, tx + tw, ty + th), 14, 4, 14, 64)
ImageDraw.Draw(im).rounded_rectangle((tx, ty, tx + tw - 1, ty + th - 1), 14, fill=CREAM); im.alpha_composite(lg, (tx + 22, ty + 12))
F = ImageFont.truetype(R + 'scripts/social/tileprofile/fonts/Caprasimo.ttf', 118)
tl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(tl)
for t, top in (('Dear Santa', 595), ('Tiles', 710)):
    b = F.getbbox(t); d.text((W / 2 - (b[0] + b[2]) / 2, top + DY - b[1]), t, font=F, fill=CREAM)
sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sh.putalpha(tl.getchannel('A').point(lambda v: v * 46 // 255))
im.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, 0)).transform((W, H), Image.AFFINE, (1, 0, 0, 0, 1, -2)) if False else sh.filter(ImageFilter.GaussianBlur(4)).transform((W, H), Image.AFFINE, (1, 0, 0, 0, 1, -2)))
im.alpha_composite(tl)
ol = Image.open(HD + 'ourlogo.png').convert('RGBA'); ol = ol.resize((500, round(ol.height * 500 / ol.width)), Image.LANCZOS)
im.alpha_composite(ol, ((W - 500) // 2, 950 + DY))
out = sys.argv[1]; im.convert('RGB').save(out, quality=93); print(out)
