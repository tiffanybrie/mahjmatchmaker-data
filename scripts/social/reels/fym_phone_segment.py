#!/usr/bin/env python3
"""Dynamic 'Match her up at Find Your Mat-ch' phone segment for an album reel (Tiffany Nov 10 7:43pm: same direction as
her Canva pages, more dynamic). 1080x1920 @30fps, no audio (she adds the song).
- headline grows toward the viewer once, then holds with a slow breathe
- white iPhone rises in; each mat: Aerial -> Table (app-style crossfade), a view label pops each change
- mat to mat = the screen SWIPES right (dating-app 'like') with a pink heart pop; the phone frame stays put; slow push-in
Usage: fym_phone_segment.py <set key> <out.mp4>   (phones: assets/social/<key>-launch/fym-phones/juniper-fym-phone-{2-aerial,1-table}-<mat>.png)"""
import sys, os, asyncio, subprocess, math
from PIL import Image, ImageDraw, ImageFilter
from playwright.async_api import async_playwright
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) + '/'
key, out = sys.argv[1], sys.argv[2]
PH = f'{R}assets/social/{key}-launch/fym-phones/'
MATS = ['flora-belle', 'palm-royale', 'garden-glow', 'cherry-blossom-jade', 'jungle-hot-pink', 'the-kerry', 'zesty-plume', 'lotus-cove']
W, H, FPS = 1080, 1920, 30; BG = (255, 255, 255)
F = R + 'scripts/social/tileprofile/fonts/'; TMP = '/tmp/fymseg_txt'; os.makedirs(TMP, exist_ok=True)
async def texts():
    css = f"""@font-face{{font-family:Cap;src:url('file://{F}Caprasimo.ttf')}}
@font-face{{font-family:PF;font-style:italic;font-weight:600;src:url('file://{F}playfair-display-latin-600-italic.woff2')}}
*{{margin:0;padding:0}} body{{background:transparent}}"""
    items = {'head': '<div style="font:400 112px/1.02 Cap;color:#054689;text-align:center;padding:10px 20px">Match her up at<br>Find <span style="font:italic 600 118px PF">Your</span> Mat-ch<span style="font:400 40px Cap;vertical-align:52px">™</span></div>',
             'aerial': '<div style="display:inline-block;font:700 40px Poppins;color:#fff;background:#c8325f;border-radius:999px;padding:14px 34px;margin:6px">Aerial view</div>',
             'table': '<div style="display:inline-block;font:700 40px Poppins;color:#fff;background:#054689;border-radius:999px;padding:14px 34px;margin:6px">Table view · add racks</div>'}
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 400}, device_scale_factor=1)
        for k, h in items.items():
            hp = f'{TMP}/{k}.html'; open(hp, 'w').write(f'<html><head><meta charset=utf8><style>{css}</style></head><body><span id=t style="display:inline-block">{h}</span></body></html>')
            await pg.goto('file://' + hp); await pg.wait_for_load_state('networkidle')
            await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(150)
            await pg.locator('#t').screenshot(path=f'{TMP}/{k}.png', omit_background=True)
        await b.close()
asyncio.run(texts())
HEAD, LAB = Image.open(f'{TMP}/head.png').convert('RGBA'), {k: Image.open(f'{TMP}/{k}.png').convert('RGBA') for k in ('aerial', 'table')}
# phone geometry (scripts/social/phone/iphone_white.py): screen at (79,70), 1170x2532, radius 165
SX, SY, SW, SH, SR = 79, 70, 1170, 2532, 165
base = Image.open(PH + 'juniper-fym-phone-1-table-' + MATS[0] + '.png').convert('RGBA')
mask = Image.new('L', (SW, SH), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, SW - 1, SH - 1], radius=SR, fill=255)
frame = base.copy(); frame.paste(Image.new('RGBA', (SW, SH), (255, 255, 255, 255)), (SX, SY), mask)
screens = [(m, v, Image.open(f'{PH}juniper-fym-phone-{"2-aerial" if v == "aerial" else "1-table"}-{m}.png').convert('RGBA').crop((SX, SY, SX + SW, SY + SH))) for m in MATS for v in ('aerial', 'table')]
heart = Image.new('RGBA', (300, 270), (0, 0, 0, 0)); hd = ImageDraw.Draw(heart)
hd.ellipse([0, 0, 160, 160], fill=(232, 74, 120, 255)); hd.ellipse([140, 0, 300, 160], fill=(232, 74, 120, 255)); hd.polygon([(12, 115), (288, 115), (150, 268)], fill=(232, 74, 120, 255))
heart = heart.filter(ImageFilter.GaussianBlur(0.6))
PSC = 1270 / frame.height                        # phone height on canvas
PW_, PH_ = int(frame.width * PSC), int(frame.height * PSC)
INTRO, HOLD, XF, SWIPE = 1.1, 0.8, 0.22, 0.5   # seconds
T = []; t = INTRO
for i in range(len(screens)): T.append(t); t += HOLD + (SWIPE if i % 2 == 1 else XF)
DUR = t + 0.4
eo = lambda x: 1 - (1 - min(max(x, 0), 1)) ** 3
def eb(x):
    x = min(max(x, 0), 1); c1 = 1.70158; c3 = c1 + 1; return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
def paste_scaled(cv, im, cx, cy, s, a=1.0):
    if s <= 0.01 or a <= 0: return
    w, h = max(1, int(im.width * s)), max(1, int(im.height * s)); r = im.resize((w, h), Image.LANCZOS)
    if a < 1: r.putalpha(r.getchannel('A').point(lambda v: int(v * a)))
    cv.alpha_composite(r, (int(cx - w / 2), int(cy - h / 2)))
def screen_at(tt):
    """screen content at time tt + (swipe offset, heart alpha)"""
    idx = max(i for i in range(len(T)) if tt >= T[i] - 1e-9) if tt >= T[0] else 0
    cur = screens[idx][2]; img = cur.copy(); dx = 0; hz = 0
    end = T[idx] + HOLD
    if idx + 1 < len(screens) and tt > end:
        nxt = screens[idx + 1][2]; k = (tt - end) / (T[idx + 1] - end)
        if idx % 2 == 0:  # aerial -> table: crossfade like the app's view switch
            img = Image.blend(cur, nxt, eo(k))
        else:             # mat -> mat: swipe right (like), next card comes from under
            img = nxt.copy(); dx = int(k ** 1.6 * SW * 1.1); hz = k
            mv = cur.rotate(-10 * k, resample=Image.BICUBIC, expand=False)
            img.alpha_composite(mv, (dx, int(80 * k))) if dx < SW else None
    return idx, img, hz
pipe = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                         '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
for n in range(int(DUR * FPS)):
    tt = n / FPS; cv = Image.new('RGBA', (W, H), BG + (255,))
    # headline: grows toward the viewer, then breathes
    hs = 0.55 + 0.45 * eb(tt / 0.7) if tt < 0.7 else 1 + 0.015 * math.sin((tt - 0.7) * 2 * math.pi / 2.4)
    paste_scaled(cv, HEAD, W / 2, 360, hs, min(1, tt / 0.25))
    # phone rises in, then a slow push-in toward the viewer
    rise = eo((tt - 0.25) / 0.7); push = 1 + 0.06 * min(max((tt - INTRO) / (DUR - INTRO), 0), 1)
    idx, scr, hz = screen_at(tt)
    ph = frame.copy(); ph.paste(scr, (SX, SY), mask)
    paste_scaled(cv, ph, W / 2, 625 + PH_ / 2 + (1 - rise) * 900, PSC * push)
    # view label pops at each new screen
    if tt >= T[0]:
        lab = LAB[screens[idx][1]]; k = (tt - T[idx]) / 0.35
        paste_scaled(cv, lab, W / 2, 590, 0.9 * eb(k) if k < 1 else 0.9)
    if hz:  # pink heart pop on the swipe
        a = math.sin(math.pi * min(hz, 1)); paste_scaled(cv, heart, W / 2 + 260, 1150, 0.5 + 0.6 * hz, a)
    pipe.stdin.write(cv.convert('RGB').tobytes())
pipe.stdin.close(); pipe.wait(); print(out, round(DUR, 2), 's')
