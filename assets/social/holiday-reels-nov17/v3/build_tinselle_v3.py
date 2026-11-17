"""Tinselle Emerald reel v3 (Nov 17, Tiffany: open on the cover card with a zoom and a holiday hook; never reuse the
pile shot, show the mats a different way). Segments:
 1 opener: full-screen tall cover (build_tinselle_cover.py) zooming out, hook plate on top
 2 tiles: the v2 tiles segment (fix_tin 66-117)
 3 mats, NEW format: the same Tinselle tiles under a mat that swaps every third of a second (15 mats, no Polo Club)
 4 phone: search Tinselle (fix_tin 264-296), then swipes from the full capture with the header fixed (ph_fix 1-86)
 5 end card: build_endcards.py wall + plate, blended from the last phone frame."""
import json, os, sys, shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter
R = '/home/claude/tiffanybrie/mahjmatchmaker-data/'; S = '/tmp/claude-0/-home-user/480229dd-9afd-5a5d-8d97-f8a0f68e2764/scratchpad/'
sys.path.insert(0, R + 'assets/social/holiday-endcards-nov17')
W, H = 1080, 1920; CREAM = (246, 234, 224); GREEN = (15, 72, 42); RED = (179, 32, 42)
CAP = R + 'scripts/social/tileprofile/fonts/Caprasimo.ttf'; BIT = R + 'scripts/albumcard/woodfix/Bitter-Bold.ttf'
OUT = S + 'tin3/'; os.makedirs(OUT, exist_ok=True); [os.remove(OUT + f) for f in os.listdir(OUT)]
n = [0]
def put(im):
    n[0] += 1; im.convert('RGB').save(OUT + f'f{n[0]:04d}.png')
def last(): return Image.open(OUT + f'f{n[0]:04d}.png').convert('RGB')
def blend_in(frames, k=6):
    prev = last()
    for i, fr in enumerate(frames):
        fr = fr.convert('RGB'); put(Image.blend(prev, fr, (i + 1) / k) if i < k else fr)
def ease(t): return t * t * (3 - 2 * t)
# 1 opener
cov = Image.open(R + 'assets/social/holiday-reels-nov17/v3/tinselle-reel-cover.jpg').convert('RGB')
hook = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(hook); F = ImageFont.truetype(CAP, 62)
t = 'Deck the table in emerald'; tw = d.textlength(t, font=F); assert tw < 900, tw
bx = ((W - tw) / 2 - 44, 170, (W + tw) / 2 + 44, 290)
sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((bx[0], bx[1] + 10, bx[2], bx[3] + 10), 60, fill=(0, 0, 0, 90))
hook.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14))); d = ImageDraw.Draw(hook)
d.rounded_rectangle(bx, 60, fill=CREAM + (255,)); b = F.getbbox(t); d.text((W / 2 - (b[0] + b[2]) / 2, (bx[1] + bx[3]) / 2 - (b[1] + b[3]) / 2), t, font=F, fill=GREEN)
N1 = 72
for i in range(N1):
    s = 1.0 + 0.07 * ease(i / (N1 - 1)); cw, ch = round(W / s), round(H / s)
    fr = cov.crop(((W - cw) // 2, (H - ch) // 2, (W - cw) // 2 + cw, (H - ch) // 2 + ch)).resize((W, H), Image.LANCZOS).convert('RGBA')
    a = min(1, max(0, (i - 8) / 8)); h = hook.copy(); h.putalpha(h.getchannel('A').point(lambda v: int(v * a))); fr.alpha_composite(h)
    if i < 5: fr = Image.blend(Image.new('RGBA', (W, H), (0, 0, 0, 255)), fr, (i + 1) / 5)
    put(fr)
# 2 tiles
blend_in([Image.open(S + f'fix_tin/f{i:04d}.png') for i in range(66, 118)])
# 3 mats swap
from PIL import ImageChops
def trim(im):  # same as build_endcards.trim (importing that file runs its renders)
    rgb=im.convert('RGB'); bg=Image.new('RGB',rgb.size,(255,255,255))
    bb=ImageChops.difference(rgb,bg).convert('L').point(lambda v:255 if v>40 else 0).getbbox(); im=rgb.crop(bb) if bb else rgb
    w,h=im.size; k=int(min(w,h)*0.02); im=im.crop((k,k,w-k,h-k)); w,h=im.size; m=min(w,h)
    return im.crop(((w-m)//2,(h-m)//2,(w-m)//2+m,(h-m)//2+m))
MATS = json.load(open(R + 'assets/social/holiday-endcards-nov17/tinselle-wall-mats.json'))
NAMES = ['Candy Cane Lane · Anders Ruff', 'Classic Very Merry Mahj · Anders Ruff', 'Evergreen & Tartan · Anders Ruff',
 "Holly Jolly Christmas · Bam! Let's Mahjong", 'Holiday Love · Bespoke x Corey Paige', "Rackin' Rudolph · Hip Hip Mahjong", None,
 'Letters to Santa · Mahjong Register', 'Plaid Tidings · My Fair Mahjong', 'Candy Cane Lane · Peace Love Mahjong',
 'Merry & Striped · Peace Love Mahjong', 'Merry Mix · Peace Love Mahjong', 'Nutcracker Noel · Peace Love Mahjong',
 'Perfectly Wrapped · Peace Love Mahjong', 'Poinsettia & Peace · Peace Love Mahjong', 'Festive Plaid · Sunday Mahjong']
ORDER = [2, 9, 5, 14, 4, 8, 13, 0, 12, 15, 7, 10, 1, 3, 11]
MS = 840; MX = (W - MS) // 2; MY = 300
def rr(im, r):
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), r, fill=255); return m
base = Image.new('RGBA', (W, H), GREEN + (255,)); d = ImageDraw.Draw(base); FH = ImageFont.truetype(CAP, 64)
for line, y in (('Holiday mats that', 128), ('match Tinselle', 204)):
    b = FH.getbbox(line); assert b[2] - b[0] < 940; d.text((W / 2 - (b[0] + b[2]) / 2, y - b[1]), line, font=FH, fill=CREAM)
tsrc = Image.open(R + 'assets/tiles/holiday/tinselle-emerald-3x3.jpg').convert('RGB').crop((240, 655, 1160, 1005))
TW = MS; th = round(tsrc.height * TW / tsrc.width); tiles = tsrc.resize((TW, th), Image.LANCZOS); TY = MY + MS + 92
sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
sd.rounded_rectangle((MX, MY + 14, MX + MS, MY + MS + 14), 30, fill=(0, 0, 0, 110)); sd.rounded_rectangle((MX, TY + 12, MX + TW, TY + th + 12), 26, fill=(0, 0, 0, 110))
base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18))); base.paste(tiles, (MX, TY), rr(tiles, 26))
FL = ImageFont.truetype(BIT, 36)
mats = [trim(Image.open(R + MATS[k])).resize((MS, MS), Image.LANCZOS) for k in ORDER]
HOLD, SL = 9, 4
frames = []
for j, k in enumerate(ORDER):
    for f in range(HOLD):
        fr = base.copy(); dd = ImageDraw.Draw(fr)
        if j > 0 and f < SL:
            p = ease((f + 1) / SL); off = round((1 - p) * (W - MX))
            fr.paste(mats[j - 1], (MX - round(p * 0) , MY), rr(mats[j - 1], 30))
            fr.paste(mats[j], (MX + off, MY), rr(mats[j], 30))
            fr.paste(GREEN, (0, MY, MX, MY + MS)); fr.paste(GREEN, (MX + MS, MY, W, MY + MS))
        else:
            fr.paste(mats[j], (MX, MY), rr(mats[j], 30))
        lab = NAMES[ORDER[j - 1]] if (j > 0 and f < SL and ease((f + 1) / SL) < .5) else NAMES[k]; b = FL.getbbox(lab); assert b[2] - b[0] < 960, lab
        dd.text((W / 2 - (b[0] + b[2]) / 2, MY + MS + 22 - b[1]), lab, font=FL, fill=CREAM)
        frames.append(fr)
frames += [frames[-1]] * 6
blend_in(frames)
# 4 phone
blend_in([Image.open(S + f'fix_tin/f{i:04d}.png') for i in range(264, 297)])
for i in range(1, 87): put(Image.open(S + f'rb/ph_fix/f{i:04d}.png'))
print('frames', n[0])
