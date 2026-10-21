# Holiday "How I'm Styling" boards, Oct 21 rebuild.
# Blog boards (branded mats) and Amazon storefront boards (Amazon products only, generic names) are separate.
# Every cutout is drawn at true relative scale: K = pixels per inch for that board.
# Framed photos (mat-in-room photos, tablecloth photos, tile shots) are photos, not cutouts, so they are exempt.
# Usage: python3 scripts/moodboard/holiday_boards_oct21.py [--debug]
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

REPO = '/home/claude/mahjmatchmaker-data/'
SRC = REPO + 'assets/blog/holiday-boards-oct21/src/'
OUT = REPO + 'assets/blog/holiday-boards-oct21/'
BRAND = REPO + 'assets/brand/mahjmatchmaker-wordmark.png'
BG = (250, 247, 242, 255)
INK = (34, 26, 30)
DEBUG = '--debug' in sys.argv

def font(name, size): return ImageFont.truetype(SRC + name, size)

def load(p):
    im = Image.open(SRC + p if not p.startswith('/') else p)
    return im.convert('RGBA')

def clean_cut(im):
    """Trim to alpha, pull in the edge 1px and feather it so no white halo shows on cream."""
    a = im.getchannel('A')
    a2 = a.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.7))
    im = im.copy(); im.putalpha(Image.fromarray(__import__('numpy').minimum(__import__('numpy').array(a), __import__('numpy').array(a2))))
    bb = im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
    return im.crop(bb) if bb else im

def rounded(im, w, h, r, border=0, crop=None):
    if crop: im = im.crop(crop)
    im = ImageOps.fit(im, (w, h), Image.LANCZOS)
    if border:
        base = Image.new('RGBA', (w + 2 * border, h + 2 * border), (255, 255, 255, 255))
        base.alpha_composite(im, (border, border)); im = base; w, h = im.size
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), r, fill=255)
    im.putalpha(m); return im

def shadow_place(c, im, x, y, rot=0, shad=True):
    if rot: im = im.rotate(rot, expand=True, resample=Image.BICUBIC)
    if shad:
        a = im.getchannel('A')
        sh = Image.new('RGBA', im.size, (60, 40, 30, 0)); sh.putalpha(a.point(lambda v: int(v * 0.28)))
        pad = 30
        big = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0)); big.alpha_composite(sh, (pad, pad))
        big = big.filter(ImageFilter.GaussianBlur(10))
        c.alpha_composite(big, (int(x - pad + 4), int(y - pad + 9)))
    c.alpha_composite(im, (int(x), int(y)))
    return (int(x), int(y), int(x + im.width), int(y + im.height))

class Board:
    def __init__(s, W, H, K, accent, pill_txt, title, footer, sub=None):
        s.W, s.H, s.K = W, H, K
        s.c = Image.new('RGBA', (W, H), BG); s.boxes = []; s.labels = []
        d = ImageDraw.Draw(s.c)
        lw = int(W * 0.30)
        logo = load(BRAND); logo = logo.resize((lw, int(lw * logo.height / logo.width)), Image.LANCZOS)
        s.c.alpha_composite(logo, ((W - lw) // 2, 28))
        y = 28 + logo.height + 22
        pf = font('Caprasimo.ttf', 38); pw = d.textlength(pill_txt, font=pf) + 90
        d.rounded_rectangle((W / 2 - pw / 2, y, W / 2 + pw / 2, y + 66), 33, fill=accent)
        d.text((W / 2, y + 33), pill_txt, font=pf, fill=(255, 255, 255), anchor='mm')
        ts = 54
        while d.textlength(title, font=font('Caprasimo.ttf', ts)) > W - 90: ts -= 2
        d.text((W / 2, y + 66 + 58), title, font=font('Caprasimo.ttf', ts), fill=accent, anchor='mm')
        s.top = y + 66 + 58 + 40
        if sub:
            d.text((W / 2, s.top + 8), sub, font=font('HomemadeApple.ttf', 28), fill=INK, anchor='mm'); s.top += 50
        d.rounded_rectangle((100, H - 80, W - 100, H - 24), 28, fill=accent)
        d.text((W / 2, H - 52), footer, font=font('DMSerif.ttf', 29), fill=(255, 255, 255), anchor='mm')
        s.accent = accent

    def cut(s, src, inches, dim='h', x=None, y=None, cx=None, bottom=None, rot=0, name=''):
        """Cutout at true scale: `inches` real size along `dim` (h = height, w = width)."""
        im = clean_cut(load(src)); px = inches * s.K
        if dim == 'h': im = im.resize((max(1, int(im.width * px / im.height)), int(px)), Image.LANCZOS)
        else: im = im.resize((int(px), max(1, int(im.height * px / im.width))), Image.LANCZOS)
        if cx is not None: x = cx - im.width // 2
        if bottom is not None: y = bottom - im.height
        b = shadow_place(s.c, im, x, y, rot); s.boxes.append((name or src, b)); return b

    def flat(s, src, inches, x, y, r=0.04, rot=0, name=''):
        """A flat mat (top-down) at true scale, softly rounded corners."""
        im = load(src); px = int(inches * s.K)
        im = rounded(im, px, int(px * im.height / im.width), int(px * r))
        b = shadow_place(s.c, im, x, y, rot); s.boxes.append((name or src, b)); return b

    def card(s, src, w, h, x, y, crop=None, rot=0, name=''):
        """A framed photo (white border, rounded): photos are not scaled to inches."""
        im = rounded(load(src), w, h, 18, border=8, crop=crop)
        b = shadow_place(s.c, im, x, y, rot); s.boxes.append((name or src, b)); return b

    def label(s, txt, x, y, anchor='mm', size=21):
        d = ImageDraw.Draw(s.c); f = font('HomemadeApple.ttf', size)
        lines = txt.split('\n'); lh = int(size * 1.45)
        for i, t in enumerate(lines):
            yy = y + (i - (len(lines) - 1) / 2) * lh
            d.text((x, yy), t, font=f, fill=INK, anchor=anchor)
            bb = d.textbbox((x, yy), t, font=f, anchor=anchor); s.labels.append((t, bb))

    def note(s, txt, x, y, size=24):
        d = ImageDraw.Draw(s.c)
        d.text((x, y), txt, font=font('DMSerif.ttf', size), fill=s.accent, anchor='mm')

    def check(s, name):
        """Labels must keep 12px from every item and stay inside the canvas; items must not overlap other items unless allowed."""
        bad = []
        for t, (a, b, c2, d2) in s.labels:
            if a < 8 or c2 > s.W - 8: bad.append(f'label off-canvas: {t}')
            for n, (x0, y0, x1, y1) in s.boxes:
                if a < x1 + 12 and c2 > x0 - 12 and b < y1 + 12 and d2 > y0 - 12:
                    # boxes include shadow-free bbox; only flag real overlap of opaque pixels
                    reg = s._alpha_hit(n, (a - 12, b - 12, c2 + 12, d2 + 12))
                    if reg: bad.append(f'label "{t}" touches {os.path.basename(n)}')
        if DEBUG:
            d = ImageDraw.Draw(s.c)
            for n, bx in s.boxes: d.rectangle(bx, outline=(255, 0, 0))
            for t, bx in s.labels: d.rectangle(bx, outline=(0, 0, 255))
        print(name, 'OK' if not bad else bad)

    def _alpha_hit(s, n, box):
        return True  # conservative: bbox overlap counts

    def save(s, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        s.c.convert('RGB').save(path, quality=92); print('saved', path)

NAVY = (6, 69, 135); OLIVE = (94, 101, 67); CHERRY = (222, 34, 54); PINK = (214, 96, 140)
AMZ_FOOT = 'shop the look on my Amazon storefront'
BLOG_FOOT = 'shop the look  ·  mahjmatchmaker.com'
PILL = "How I'm Styling"

# ---------------------------------------------------------------- real sizes (inches)
# Amazon listings (read Oct 21): KDG lamp 15.7" tall; CryzhalinX bow lamp 13.4" tall; Joiedomi ceramic tree 9.5" with star;
# KHOYIME candle wreath 11.8" outer / 3.94" inner; Melt pillar 3x4"; Rocky Mountain burlap tree 12"; Clover89 ring dish 4";
# LAMOTI leather coaster 4"; OGANAZI amber coaster 4"; Koville marble coaster 4"; walnut rack (B0H5HYVQ5Z) 20";
# velvet ribbon 1" x 10 yd spool (~3.5" across); JUDFNCDE mat 31.5"; HunnmingRe all-in-one 55x55 (room photo).
# Not printed on the listing (estimates): RICHINNA holly dish ~6.5" across; zltSunshine enamel deer box ~6.5" tall with antlers.
# Partner mats (blog): Luxe Polo Club, Sunday Rattan, Hip Hip Rackin' Rudolph treated as standard ~32" mats.
# Partner racks: Bam Bird walnut ~18", Middle & Main scalloped milk glass ~18.5".

def amazon_plaid():
    b = Board(1080, 1350, 21, NAVY, PILL, 'A Classic Plaid Holiday Table', AMZ_FOOT)
    T = b.top + 25
    b.card('B0H9L87BHX.jpg', 470, 400, 40, T + 40, crop=(0, 150, 1000, 1000), rot=-2, name='mat')
    b.label('tartan all-in-one mat', 270, T + 8)
    b.card('ivory_tiles.jpg', 250, 215, 572, T + 50, rot=2, name='tiles')
    b.label('classic ivory tiles', 700, T + 16)
    # small pieces, true size (4" each)
    b.cut('ringdish.png', 4, 'w', cx=950, bottom=T + 140, name='ringdish')
    b.label('tree ring dish', 950, T + 168, size=19)
    b.cut('coaster1.png', 4, 'w', cx=950, bottom=T + 285, name='coaster')
    b.label('cognac coaster', 950, T + 313, size=19)
    # one walnut rack, 20"
    b.cut('walnut_rack_angled.png', 20, 'w', x=600, y=T + 365, name='rack')
    b.label('walnut rack', 800, T + 515)
    # pick-one centerpiece row (never two tall pieces on the table together)
    base = 1165
    b.note('pick one centerpiece', 545, T + 600)
    b.cut('lamp_green.png', 15.7, 'h', cx=190, bottom=base, name='lamp')
    b.cut('ribbon.png', 3.5, 'w', cx=335, bottom=base, name='ribbon')
    b.cut('tree.png', 12, 'h', cx=545, bottom=base, name='tree')
    wb = b.cut('wreath.png', 11.8, 'w', cx=865, bottom=base, name='wreath')
    b.cut('pillar34.png', 4, 'h', cx=865, bottom=(wb[1] + wb[3]) // 2 + 18, name='pillar')
    b.label('green pleated lamp', 190, base + 32)
    b.label('tie on\nvelvet ribbon', 345, base - 105, size=18)
    b.label('little burlap tree', 545, base + 32)
    b.label('candle wreath + 3x4 pillar', 865, base + 32, size=19)
    b.check('amazon plaid'); b.save(OUT + 'amazon/a-classic-plaid-holiday-table.jpg')

def amazon_retro():
    b = Board(1080, 1350, 30, OLIVE, PILL, 'A Retro Holiday Table', AMZ_FOOT)
    T = b.top + 25
    b.card('B0H9KZY2L4.jpg', 480, 415, 40, T + 40, crop=(80, 160, 1000, 940), rot=-2, name='mat')
    b.label('red plaid all-in-one mat', 280, T + 8)
    b.card('ivory_tiles.jpg', 245, 211, 590, T + 52, rot=2, name='tiles')
    b.label('classic ivory tiles', 720, T + 18)
    b.cut('dice_holly.png', 6.5, 'w', cx=695, bottom=T + 520, name='holly')
    b.label('holly dice dish', 695, T + 552)
    b.cut('coaster_amber.png', 4, 'w', cx=935, bottom=T + 505, name='coaster')
    b.label('amber glass coaster', 935, T + 540)
    b.cut('walnut_rack_angled.png', 20, 'w', x=50, y=T + 610, name='rack')
    b.label('walnut rack', 350, T + 835)
    b.cut('lamp_tree.png', 9.5, 'h', cx=880, bottom=T + 880, name='tree lamp')
    b.label('ceramic tree lamp', 880, T + 912)
    b.check('amazon retro'); b.save(OUT + 'amazon/a-retro-holiday-table.jpg')

def blog_polo():
    b = Board(1000, 1500, 17, NAVY, PILL, 'A Polo Club Holiday Table', BLOG_FOOT)
    T = b.top + 25
    m = b.flat('mat_clean.jpg', 32, 420, T + 45, name='mat')
    b.label('polo club mat by luxe mahjong', 692, T + 10)
    b.card(REPO + 'assets/tiles/album/heritage.jpg', 300, 265, 45, T + 50, rot=-2, name='tiles')
    b.label('heritage tiles', 200, T + 10)
    b.cut('rack_walnut.png', 18, 'w', x=45, y=T + 375, name='rack')
    b.label('bam bird walnut rack', 198, T + 448, size=20)
    b.card('cloth60.jpg', 240, 225, 75, T + 505, rot=2, name='cloth')
    b.label('hunter green 60x60 cloth', 200, T + 785, size=20)
    b.cut('coaster1.png', 4, 'w', cx=600, bottom=m[3] + 95, name='coaster')
    b.label('cognac coaster', 600, m[3] + 122, size=19)
    b.cut('ringdish.png', 4, 'w', cx=800, bottom=m[3] + 95, name='ringdish')
    b.label('tree ring dish', 800, m[3] + 122, size=19)
    base = 1345
    b.note('pick one centerpiece', 500, 1110)
    b.cut('tree.png', 12, 'h', cx=165, bottom=base, name='tree')
    b.cut('wreath.png', 11.8, 'w', cx=470, bottom=base, name='wreath')
    b.cut('lamp_green.png', 15.7, 'h', cx=790, bottom=base, name='lamp')
    b.cut('ribbon.png', 3.5, 'w', cx=925, bottom=base, name='ribbon')
    b.label('a little tree', 165, base + 32)
    b.label('a candle wreath', 470, base + 32)
    b.label('a lamp tied with velvet ribbon', 790, base + 32, size=19)
    b.check('blog polo'); b.save(OUT + 'blog/polo-club-holiday-table.jpg')

def blog_rattan():
    b = Board(1000, 1500, 20, OLIVE, PILL, 'A Retro Rattan Holiday Table', BLOG_FOOT)
    T = b.top + 25
    m = b.flat('rattan_clean.png', 32, 330, T + 45, r=0.0, name='mat')
    b.label('sunday rattan mat', 650, T + 10)
    cl = b.cut('clothE.png', 275 / b.K, 'w', x=30, y=T + 75, name='cloth')
    b.label('red tartan\n60x60 cloth', 165, T + 22, size=20)
    b.card(REPO + 'assets/tiles/album/heritage.jpg', 250, 225, 35, cl[3] + 85, rot=-3, name='tiles')
    b.label('heritage tiles', 165, cl[3] + 45)
    b.cut('rack_walnut.png', 18, 'w', x=470, y=m[3] + 35, name='rack')
    b.label('walnut rack', 650, m[3] + 110)
    base = 1340
    b.cut('lamp_tree.png', 9.5, 'h', cx=190, bottom=base, name='tree lamp')
    b.label('ceramic tree lamp', 190, base + 32)
    b.cut('dice_holly.png', 6.5, 'w', cx=500, bottom=base - 10, name='holly')
    b.label('holly dice dish', 500, base + 32)
    b.cut('coaster_amber.png', 4, 'w', cx=800, bottom=base - 15, name='coaster')
    b.label('amber glass coaster', 800, base + 32)
    b.check('blog rattan'); b.save(OUT + 'blog/sunday-rattan-holiday-table.jpg')

def blog_rudolph():
    b = Board(1000, 1500, 20, CHERRY, PILL, 'A Rackin’ Rudolph Holiday Table', BLOG_FOOT)
    T = b.top + 25
    m = b.flat('mat_rr.jpg', 32, 330, T + 45, r=0.04, name='mat')
    b.label("rackin' rudolph mat by hip hip mahjong", 650, T + 10, size=19)
    b.cut('rack_milkglass.png', 18.5, 'w', x=m[0] + 200, y=m[3] - 85, name='rack')
    b.label('middle + main scalloped milk glass rack', 640, m[3] + 92, size=19)
    b.card('cloth_cherry.jpg', 250, 235, 30, T + 75, rot=-2, name='cloth')
    b.label('cherry red\n60x60 cloth', 160, T + 22, size=20)
    b.cut('tiles_fan2.png', 290 / b.K, 'w', x=20, y=T + 445, name='tiles')
    b.label("rackin' rudolph\ntiles", 160, T + 395, size=20)
    base = 1335
    b.cut('lamp_bow.png', 13.4, 'h', cx=170, bottom=base, name='lamp')
    b.label('the bow lamp', 170, base + 32)
    b.label('its bow echoes\nthe bows on the mat', 340, base - 150, size=17)
    b.cut('deer_box.png', 6.5, 'h', cx=575, bottom=base, name='deer')
    b.label('reindeer dice box', 575, base + 32)
    b.cut('coaster_marble.png', 4, 'w', cx=830, bottom=base - 10, name='coaster')
    b.label('white marble coaster', 830, base + 32)
    b.check('blog rudolph'); b.save(OUT + 'blog/rackin-rudolph-holiday-table.jpg')

def amazon_reindeer():
    """Her approved Oct 18 board (posted on Amazon): keep every item and size, only fix the title to Title Case."""
    c = load('reindeer_board_approved.jpg'); d = ImageDraw.Draw(c)
    d.rectangle((150, 208, 930, 282), fill=BG)
    d.text((540, 242), 'A Reindeer Holiday Table', font=font('Caprasimo.ttf', 50), fill=(222, 34, 54), anchor='mm')
    c.convert('RGB').save(OUT + 'amazon/a-reindeer-holiday-table.jpg', quality=92); print('saved reindeer')

if __name__ == '__main__':
    amazon_reindeer(); amazon_plaid(); amazon_retro(); blog_polo(); blog_rattan(); blog_rudolph()
