# ShopMy collection cover cards. v2 = Tiffany's Oct 21 1:27-1:40pm edits (approved 2:19pm):
#  - official wordmark PNG WITH the tagline ribbon (never retyped), Caprasimo headlines, kicker in Bitter 700
#    (v1 used the variable Bitter.woff2, which renders at its default Thin weight: that was the "super light" subtitle)
#  - 5 photos per collage (4 looked like one was missing bottom-right); 3-up and 6-up only where she laid them out
#  - transparent PNGs (Mahj & Vine) go on white with a white border, never black
#  - black mat/rack bags and black flipped-corner backs are cropped or patched out per image (CROP / FIX below)
# Usage: python3 scripts/shopmy/make_covers.py <img_dir> [slug ...]   (images named <pinId>.jpg|.png)
import sys, os, glob
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageChops
R = '/home/claude/mahjmatchmaker-data/'
IMG = sys.argv[1] if len(sys.argv) > 1 else '.'
OUT = R + 'assets/shopmy/covers/'
CAP = R + 'scripts/moodboard/fonts/Caprasimo.woff2'
BIT = R + 'scripts/social/tileprofile/fonts/bitter-latin-700-normal.woff2'
PFI = R + 'scripts/social/tileprofile/fonts/playfair-display-latin-600-italic.woff2'
LOGO = R + 'assets/brand/mahjmatchmaker-wordmark-notag.png'   # official wordmark image (826px, crisp); never retyped
RIBBON = (245, 108, 140)   # #f56c8c, same ribbon as assets/brand/mahjmatchmaker-wordmark.png and the approved Papaya lockup
BG = (250, 243, 234); NAVY = (5, 70, 137); INK = (43, 38, 35)
def font(p, s): return ImageFont.truetype(p, s)
def hexc(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

# per-pin crop box (fractions l, t, r, b) to cut black bags / packaging
CROP = {
    96210831: (0, 0, .845, .875),        # pink tiger moon: drop the rolled bag
    96210535: (0, 0, 1, 1),
    96212924: (0, 0, .80, .98),    # Sweet Jojo: drop the black bag
    96213709: (0, 0, .845, .96),       # green tropical plants: drop the black bag
    96213996: (0, 0, .815, .88),        # beige & white floral chinoiserie: drop the black bag
    96216016: (0, 0, 1, .955),        # yellow floral: drop the black bag
    96237389: (0, 0, .80, .93),        # gothic raven mat: drop the black mat bag
    96217176: (0, .31, .70, 1),      # tortoise racks: drop the box + paisley bag
    96217490: (0, .31, .70, 1),      # clear scalloped racks: drop the box + paisley bag
    96229865: (0, 0, 1, .66),        # cognac leather tile bag: the big bag only
    96222455: (0, 0, 1, .78),        # bird lamp: lose the books
}
# black flipped-back corners patched with the mirrored opposite corner: (corner, w frac, h frac)
FIX = {
    96210535: [('tr', .36, .36)],    # pink bows
    96213996: [('tr', .42, .34)],    # beige floral (after crop)
    96237389: [('tr', .30, .24)],    # gothic raven
    96233460: [('tr', .16, .16)],    # santa & reindeer
}

COVERS = [
 # id, slug, title, tagline, kicker, accent, layout, picks (hero first; 3-up = [hero, left, right]; 6-up = [hero, under-hero, 4 corners])
 (8393657, 'dice-dishes', 'Dice Dishes & Accessories', 'the little extras that finish a table', 'table shop', '#e0607e', 5,
  [96203680, 96196661, 96195144, 96207171, 96203770]),
 (8398138, 'mahjong-lamps', 'Mahjong Lamps', 'cordless lamps for a cozy game night', 'table shop', '#c4932b', 5,
  [96222800, 96222662, 96193399, 96228999, 96222455]),
 (8392222, 'etsy-mahjong-mats', 'Etsy Mahjong Mats', 'one-of-a-kind mats from small shops', 'mat shop', '#e0607e', 5,
  [96122627, 96131839, 96131764, 96131413, 96131171]),
 (8399101, 'racks', 'Mahjong Racks', 'racks and pushers for every set', 'rack shop', '#054689', 3,
  [96217240, 96217176, 96217490]),
 (8400954, 'mahjong-tablecloths', 'Mahjong Tablecloths', 'the layer under your mat', 'table shop', '#1f5a3a', 5,
  [96230340, 96231302, 96230869, 96230691, 96212892]),
 (8398332, 'amazon-mahjong-mats', 'Amazon Mahjong Mats', 'pretty mats that ship fast', 'mat shop', '#1f5a3a', 6,
  [96210831, 96210535, 96212924, 96213709, 96213996, 96216016]),
 (8398036, 'mahj-and-vine', 'Mahj & Vine', 'chinoiserie mats in every color', 'mat shop', '#1f5a3a', 5,
  [95959018, 96195087, 95959071, 95959047, 96195067]),
 (8387635, 'tala-mahj', 'Tala Mahj Favorites', 'my favorite fringe mats', 'mat shop', '#c46a2b', 5,
  [96067421, 96304138, 96067632, 96067718, 96067638]),
 (8398013, 'charleston-mahjong-club', 'Charleston Mahjong Club', 'club mats, bags and totes', 'brand shop', '#054689', 5,
  [95958590, 95959013, 95959041, 95958614, 95958946]),
 (8400718, 'omm-love-shack-fancy', 'Oh My Mahjong x LoveShackFancy', 'the coquette collab, all in one place', 'shop the collab', '#e0607e', 5,
  [96227058, 96226860, 96233820, 96227272, 96227121]),
 (8392650, 'the-mahjong-house', 'The Mahjong House', 'pearl, tortoise and island tile sets', 'tile shop', '#054689', 5,
  [96127861, 96127725, 96127601, 96130241, 96129673]),
 (8399799, 'mahjong-storage', 'Mahjong Storage', 'bags and totes for your set', 'storage', '#054689', 3,
  [96214131, 95958946, 96229865]),
 (8399927, 'merry-mahjong', 'Merry Mahjong', 'christmas finds for your mahj table', 'holiday shop', '#b3202a', 5,
  [96216077, 96226001, 96232169, 96232833, 96216391]),
 (8399777, 'mahjong-gifts', 'Mahjong Gifts', 'for every mahj friend on your list', 'gift guide', '#b3202a', 5,
  [96216286, 96213699, 96217133, 96213080, 96213309]),
 (8398045, 'bam-lets-mahjong', "BAM! Let's Mahjong", 'holly jolly tiles, mat and shufflers', 'holiday shop', '#b3202a', 3,
  [96194546, 95959321, 96194521]),
 (8391624, 'betty-june-jeannette', 'Betty June Jeannette', 'dreamy watercolor mahjong mats', 'mat shop', '#e0607e', 5,
  [96114928, 96126037, 96126853, 96126603, 96125859]),
 (8401508, 'halloween-mahjong-table', 'Halloween Mahjong Table', 'a gothic raven table for spooky season', 'shop the look', '#6b1d2e', 6,
  [96237389, 96238653, 96237516, 96237993, 96239262, 96237822]),
 (8401175, 'a-reindeer-holiday-table', 'A Reindeer Holiday Table', 'santa, reindeer and cherry red', 'shop the look', '#b3202a', 5,
  [96233460, 96234339, 96234075, 96234203, 96233625]),
 (8401385, 'a-classic-plaid-holiday-table', 'A Classic Plaid Holiday Table', 'tartan, walnut and candlelight', 'shop the look', '#054689', 5,
  [96237159, 96236976, 96236021, 96236809, 96235867]),
 (8401290, 'a-retro-holiday-table', 'A Retro Holiday Table', 'red plaid and a glowing ceramic tree', 'shop the look', '#4f6b3a', 5,
  [96234587, 96234736, 96235121, 96235268, 96235452]),
]


def lockup(w):
    """Official wordmark + the 'MATCHING MAHJONG TILES, MATS & RACKS' ribbon (brand guide Oct 21 14:12). The ribbon PNG
    (assets/brand/mahjmatchmaker-wordmark.png) is only 420px wide, so its ribbon text is unreadable on a cover; the ribbon is
    rebuilt at size under the official wordmark image, exactly like scripts/social/omm_forward/render.py lockup()."""
    wm = Image.open(LOGO).convert('RGBA'); wm = wm.resize((w, int(w * wm.height / wm.width)), Image.LANCZOS)
    rh = int(w * .075); gap = int(w * .025); fs = int(w * .037)
    out = Image.new('RGBA', (w, wm.height + gap + rh), (0, 0, 0, 0)); out.alpha_composite(wm, (0, 0))
    d = ImageDraw.Draw(out); d.rounded_rectangle((0, wm.height + gap, w - 1, wm.height + gap + rh), 4, fill=RIBBON + (255,))
    f = font(BIT, fs); txt = 'MATCHING MAHJONG TILES, MATS & RACKS'; sp = fs * .15
    tw = sum(d.textlength(ch, font=f) for ch in txt) + sp * (len(txt) - 1); x = (w - tw) / 2; cy = wm.height + gap + rh / 2 + 1
    for ch in txt:
        d.text((x, cy), ch, font=f, fill=(255, 255, 255), anchor='lm'); x += d.textlength(ch, font=f) + sp
    return out


def load(pid):
    fs = glob.glob(os.path.join(IMG, f'{pid}.*'))
    if not fs: raise SystemExit(f'missing image for pin {pid}')
    im = Image.open(fs[0])
    if im.mode in ('RGBA', 'LA', 'P'):   # transparent PNG -> on WHITE (Mahj & Vine came in on black)
        im = im.convert('RGBA'); bg = Image.new('RGB', im.size, (255, 255, 255)); bg.paste(im, mask=im.getchannel('A')); im = bg
    im = im.convert('RGB')
    if pid in CROP:
        l, t, r, b = CROP[pid]; im = im.crop((int(l * im.width), int(t * im.height), int(r * im.width), int(b * im.height)))
    for corner, fw, fh in FIX.get(pid, []):
        w, h = int(im.width * fw), int(im.height * fh)
        if corner == 'tr': src = im.crop((0, 0, w, h)).transpose(Image.FLIP_LEFT_RIGHT); im.paste(src, (im.width - w, 0))
        if corner == 'tl': src = im.crop((im.width - w, 0, im.width, h)).transpose(Image.FLIP_LEFT_RIGHT); im.paste(src, (0, 0))
        if corner == 'bl': src = im.crop((im.width - w, im.height - h, im.width, im.height)).transpose(Image.FLIP_LEFT_RIGHT); im.paste(src, (0, im.height - h))
        if corner == 'br': src = im.crop((0, im.height - h, w, im.height)).transpose(Image.FLIP_LEFT_RIGHT); im.paste(src, (im.width - w, im.height - h))
    return im


def card(pid, size, rot):
    im = load(pid)
    diff = ImageChops.difference(im, Image.new('RGB', im.size, (255, 255, 255))).convert('L').point(lambda v: 255 if v > 18 else 0)
    bb = diff.getbbox()
    if bb:
        mx = int(max(bb[2] - bb[0], bb[3] - bb[1]) * .05)
        im = im.crop((max(0, bb[0] - mx), max(0, bb[1] - mx), min(im.width, bb[2] + mx), min(im.height, bb[3] + mx)))
    ar = im.width / im.height
    if 0.8 < ar < 1.25: im = ImageOps.fit(im, (size - 24, size - 24), Image.LANCZOS)
    im = ImageOps.pad(im, (size - 24, size - 24), color=(255, 255, 255), method=Image.LANCZOS)
    c = Image.new('RGBA', (size, size), (255, 255, 255, 255)); c.paste(im, (12, 12))
    m = Image.new('L', (size, size), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, size - 1, size - 1), 22, fill=255)
    c.putalpha(m)
    return c.rotate(rot, expand=True, resample=Image.BICUBIC)


def place(canvas, im, cx, cy):
    x, y = int(cx - im.width / 2), int(cy - im.height / 2)
    sh = Image.new('RGBA', im.size, (60, 40, 30, 0)); sh.putalpha(im.getchannel('A').point(lambda v: int(v * .30)))
    pad = 34; big = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0)); big.alpha_composite(sh, (pad, pad))
    canvas.alpha_composite(big.filter(ImageFilter.GaussianBlur(12)), (x - pad + 5, y - pad + 12))
    canvas.alpha_composite(im, (x, y))


def make(cid, slug, title, tag, kicker, accent, layout, picks):
    W = H = 1080; c = Image.new('RGBA', (W, H), BG + (255,)); d = ImageDraw.Draw(c)
    lw = 500; logo = lockup(lw)
    c.alpha_composite(logo, ((W - lw) // 2, 30))
    kf = font(BIT, 25); kt = ' '.join(kicker.upper()).replace('   ', '      ')
    ky = 30 + logo.height + 30
    d.text((W / 2, ky), kt, font=kf, fill=NAVY, anchor='mm')
    ts = 90
    while d.textlength(title, font=font(CAP, ts)) > W - 110 and ts > 66: ts -= 2
    lines = [title]
    if d.textlength(title, font=font(CAP, ts)) > W - 110:
        ws = title.split(); best = None
        for i in range(1, len(ws)):
            a, b = ' '.join(ws[:i]), ' '.join(ws[i:]); m = max(d.textlength(a, font=font(CAP, 76)), d.textlength(b, font=font(CAP, 76)))
            if best is None or m < best[0]: best = (m, [a, b])
        lines = best[1]; ts = 76
        while max(d.textlength(l, font=font(CAP, ts)) for l in lines) > W - 110: ts -= 2
    y = ky + 26 + ts // 2
    for l in lines:
        d.text((W / 2, y), l, font=font(CAP, ts), fill=hexc(accent), anchor='mm'); y += int(ts * 1.02)
    d.text((W / 2, y - 4), tag, font=font(PFI, 34), fill=INK, anchor='mm')
    top = y + 22
    area_c = (top + H) / 2; avail = H - top - 20
    if layout == 3:
        hero = min(int(avail * .80), 480); side = 330
        pos = [(172, area_c + 14, side, -5), (908, area_c + 14, side, 5), (540, area_c, hero, -1)]
        order = [picks[1], picks[2], picks[0]]
    elif layout == 6:
        hero = min(int(avail * .66), 400); side = int(min(avail * .43, 265)); low = int(side * .86)
        pos = [(180, area_c - avail * .22, side, -6), (900, area_c - avail * .22, side, 5),
               (185, area_c + avail * .25, side, 4), (895, area_c + avail * .25, side, -4),
               (540, area_c + avail * .30, low, 2), (540, area_c - avail * .12, hero, -1.5)]
        order = [picks[2], picks[3], picks[4], picks[5], picks[1], picks[0]]
    else:   # 5-up: hero centre, two on each side
        hero = min(int(avail * .80), 480); side = int(min(avail * .43, 280))
        pos = [(185, area_c - avail * .23, side, -6), (895, area_c - avail * .21, side, 5),
               (190, area_c + avail * .25, side, 4), (890, area_c + avail * .25, side, -4), (540, area_c + 6, hero, -1.5)]
        order = [picks[1], picks[2], picks[3], picks[4], picks[0]]
    for p, (cx, cy, s, r) in zip(order, pos): place(c, card(p, s, r), cx, cy)
    c.convert('RGB').save(OUT + slug + '.jpg', quality=90)
    return OUT + slug + '.jpg'


if __name__ == '__main__':
    only = sys.argv[2:]
    for row in COVERS:
        if not only or row[1] in only: print(make(*row))
