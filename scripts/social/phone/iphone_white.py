#!/usr/bin/env python3
"""White iPhone (Tiffany Nov 10 3:56pm: "It's supposed to be a white iPhone... make it look like a real phone").
Real-phone geometry: every corner is CONCENTRIC (screen radius + bezel = bezel radius, + frame = body radius), black glass
bezel around the screen (all iPhones have it), white/silver titanium frame band, Dynamic Island, side buttons.
Input: a 390x844 @3x screenshot (1170x2532). Output: transparent PNG, phone only (add shadows in Canva).
Usage: iphone_white.py <screenshot.png> <out.png> [more pairs...]"""
import sys
from PIL import Image, ImageDraw, ImageFilter
SS = 2                                   # supersample for smooth edges
SW, SH, SR = 1170, 2532, 165             # screen + iPhone 15/16 display corner radius (55pt @3x)
BZ, FR, BT = 46, 24, 9                   # black bezel, white frame band, button protrusion
from PIL import ImageFont
SB = 162                                 # status bar (54pt @3x): the page starts BELOW the Dynamic Island, like a real phone
def statusbar(sc):
    c = Image.new('RGBA', (SW, SH), (255, 255, 255, 255)); c.paste(sc.crop((0, 0, SW, SH - SB)), (0, SB))
    d = ImageDraw.Draw(c); k = (17, 17, 17, 255)
    try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 50)
    except OSError: f = ImageFont.load_default()
    d.text((150, 92), '9:41', font=f, fill=k, anchor='mm')
    x = 905                                                   # signal bars, wifi, battery
    for i, h in enumerate((14, 22, 30, 38)): d.rounded_rectangle([x + i * 15, 108 - h, x + i * 15 + 10, 108], radius=3, fill=k)
    cx, cy = 1012, 108
    for r, w in ((40, 8), (26, 8)): d.arc([cx - r, cy - r, cx + r, cy + r], 225, 315, fill=k, width=w)
    d.ellipse([cx - 7, cy - 14, cx + 7, cy], fill=k)
    d.rounded_rectangle([1048, 70, 1118, 106], radius=11, outline=(17, 17, 17, 110), width=4)
    d.rounded_rectangle([1054, 76, 1112, 100], radius=7, fill=k); d.rounded_rectangle([1121, 81, 1127, 95], radius=2, fill=(17, 17, 17, 110))
    return c
def phone(shot, out):
    W, H = SW + 2 * (BZ + FR + BT), SH + 2 * (BZ + FR)
    s = lambda v: int(round(v * SS))
    im = Image.new('RGBA', (s(W), s(H)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    ox = BT
    # side buttons (behind the frame): left action + volume up/down, right side button
    btn = (226, 227, 229, 255); bdk = (190, 192, 196, 255)
    for (x0, y0, h) in ((0, 430, 110), (0, 620, 200), (0, 860, 200)):
        d.rounded_rectangle([s(x0), s(y0), s(x0 + BT + 14), s(y0 + h)], radius=s(7), fill=bdk)
        d.rounded_rectangle([s(x0 + 2), s(y0 + 3), s(x0 + BT + 14), s(y0 + h - 3)], radius=s(6), fill=btn)
    d.rounded_rectangle([s(W - BT - 14), s(700), s(W), s(1020)], radius=s(7), fill=bdk)
    d.rounded_rectangle([s(W - BT - 14), s(703), s(W - 2), s(1017)], radius=s(6), fill=btn)
    # body: frame band (white titanium) with a soft edge highlight
    R_out = SR + BZ + FR
    d.rounded_rectangle([s(ox), 0, s(ox + SW + 2 * (BZ + FR)), s(H)], radius=s(R_out), fill=(204, 206, 210, 255))
    d.rounded_rectangle([s(ox + 3), s(3), s(ox + SW + 2 * (BZ + FR) - 3), s(H - 3)], radius=s(R_out - 3), fill=(246, 246, 247, 255))
    d.rounded_rectangle([s(ox + FR - 4), s(FR - 4), s(ox + SW + 2 * BZ + FR + 4), s(H - FR + 4)], radius=s(SR + BZ + 4), fill=(214, 216, 220, 255))
    # black glass bezel
    # WHITE front (Tiffany Nov 10 4:12pm: "the phone's supposed to be white"), with a fine grey line where glass meets screen
    d.rounded_rectangle([s(ox + FR), s(FR), s(ox + FR + SW + 2 * BZ), s(H - FR)], radius=s(SR + BZ), fill=(250, 250, 251, 255))
    d.rounded_rectangle([s(ox + FR + BZ - 4), s(FR + BZ - 4), s(ox + FR + BZ + SW + 4), s(FR + BZ + SH + 4)], radius=s(SR + 4), fill=(206, 208, 212, 255))
    im = im.resize((W, H), Image.LANCZOS)
    # screen, clipped to the display radius
    sc = statusbar(Image.open(shot).convert('RGBA').resize((SW, SH), Image.LANCZOS))
    m = Image.new('L', (SW * SS, SH * SS), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, SW * SS - 1, SH * SS - 1], radius=SR * SS, fill=255)
    m = m.resize((SW, SH), Image.LANCZOS)
    im.paste(sc, (ox + FR + BZ, FR + BZ), m)
    # Dynamic Island (126x37pt, 11pt from the top)
    di = Image.new('RGBA', (378 * SS, 111 * SS), (0, 0, 0, 0)); ImageDraw.Draw(di).rounded_rectangle([0, 0, 378 * SS - 1, 111 * SS - 1], radius=56 * SS, fill=(0, 0, 0, 255))
    di = di.resize((378, 111), Image.LANCZOS); im.alpha_composite(di, (ox + FR + BZ + (SW - 378) // 2, FR + BZ + 33))
    im.save(out); return im.size
if __name__ == '__main__':
    a = sys.argv[1:]
    for i in range(0, len(a), 2): print(a[i + 1], phone(a[i], a[i + 1]))
