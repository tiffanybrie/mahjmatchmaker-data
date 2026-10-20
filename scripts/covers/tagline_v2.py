"""Album cover tagline v2 (Tiffany, Oct 19 night): white letter-spaced tagline, no pink box, sitting in the open
space between the frame's bottom border lines; wordmark moved up for breathing room.
Works on finished 1080x1350 covers: inpaints the old wordmark + tagline, redraws both.
Usage: python3 tagline_v2.py <cover.jpg> <out.jpg> ["TAGLINE"]"""
import sys, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
R = '/home/claude/mahjmatchmaker-data/'
WM = R + 'scripts/covers/holiday/ourlogo.png'
FONT = '/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf'
def clean(img):
    a = np.asarray(img.convert('RGB')).copy(); hsv = cv2.cvtColor(a, cv2.COLOR_RGB2HSV)
    m = np.zeros(a.shape[:2], np.uint8)
    y0, y1 = 895, 1052
    band = a[y0:y1].astype(int); hb = hsv[y0:y1]
    white = (band.min(axis=2) > 205) & (hb[..., 1] < 60)
    pink = (np.abs(band[..., 0] - 245) < 30) & (np.abs(band[..., 1] - 108) < 40) & (np.abs(band[..., 2] - 140) < 40)
    mm = (white | pink).astype(np.uint8) * 255
    mm[:, :190] = 0; mm[:, 890:] = 0
    # keep the frame's bottom border lines (outside the opening)
    for (xa, xb) in ((0, 352), (728, 1080)):
        mm[990 - y0:1035 - y0, xa:xb] = 0
    m[y0:y1] = mm
    m = cv2.dilate(m, np.ones((7, 7), np.uint8))
    return Image.fromarray(cv2.inpaint(a, m, 9, cv2.INPAINT_TELEA))
def tagline(txt, max_w=372):
    for size in range(30, 14, -1):
        f = ImageFont.truetype(FONT, size); tr = size * 0.22
        w = sum(f.getlength(c) for c in txt) + tr * (len(txt) - 1)
        if w <= max_w: break
    W, H = int(w + 20), int(size * 2)
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); x = 10
    for c in txt: d.text((x, (H - size * 1.25) / 2), c, font=f, fill=(251, 246, 238, 255)); x += f.getlength(c) + tr
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); sh.putalpha(im.getchannel('A').point(lambda v: int(v * .35))); sh = sh.filter(ImageFilter.GaussianBlur(3))
    out = Image.new('RGBA', im.size, (0, 0, 0, 0)); out.alpha_composite(sh, (0, 2)); out.alpha_composite(im); return out
def apply(src, dst, txt='TILES · MATS · RACKS'):
    img = clean(Image.open(src).convert('RGB').resize((1080, 1350), Image.LANCZOS)).convert('RGBA')
    wm = Image.open(WM).convert('RGBA'); w = 540; wm = wm.resize((w, int(wm.height * w / wm.width)), Image.LANCZOS)
    img.alpha_composite(wm, ((1080 - w) // 2, 942 - wm.height // 2))
    t = tagline(txt); img.alpha_composite(t, ((1080 - t.width) // 2, 1012 - t.height // 2))
    img.convert('RGB').save(dst, quality=94)
if __name__ == '__main__':
    apply(sys.argv[1], sys.argv[2], *(sys.argv[3:4]))
