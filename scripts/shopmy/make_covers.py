# ShopMy collection cover cards (Oct 21). 1080x1080, doc 79 palette: paper bg, navy wordmark,
# Caprasimo title, Playfair italic tagline, Bitter caps kicker, product photos as white framed cards.
# Usage: python3 scripts/shopmy/make_covers.py <pin_img_dir>   (images named <collectionId>_<idx>.jpg)
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
R = '/home/claude/mahjmatchmaker-data/'
IMG = sys.argv[1] if len(sys.argv) > 1 else '.'
OUT = R + 'assets/shopmy/covers/'
F = R + 'scripts/moodboard/fonts/'
BG = (250, 243, 234); NAVY = (5, 70, 137); INK = (43, 38, 35)
def font(n, s): return ImageFont.truetype(F + n, s)
def hexc(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

COVERS = [
 # id, slug, title, tagline, kicker, accent, picks (hero first)
 (8401508, 'halloween-mahjong-table', 'Halloween Mahjong Table', 'a gothic raven table for spooky season', 'shop the look', '#6b1d2e', [0, 1, 4, 12]),
 (8399927, 'merry-mahjong', 'Merry Mahjong', 'christmas finds for your mahj table', 'holiday shop', '#b3202a', [5, 0, 9, 1]),
 (8391624, 'betty-june-jeannette', 'Betty June Jeannette', 'dreamy watercolor mahjong mats', 'mat shop', '#e0607e', [8, 1, 11, 9]),
 (8399777, 'mahjong-gifts', 'Mahjong Gifts', 'for every mahj friend on your list', 'gift guide', '#b3202a', [1, 0, 2]),
 (8400718, 'omm-love-shack-fancy', 'Oh My Mahjong x LoveShackFancy', 'the coquette collab, all in one place', 'shop the collab', '#e0607e', [2, 0, 1, 4]),
 (8398332, 'amazon-mahjong-mats', 'Amazon Mahjong Mats', 'pretty mats that ship fast', 'mat shop', '#1f5a3a', [6, 0, 4, 12]),
 (8392222, 'etsy-mahjong-mats', 'Etsy Mahjong Mats', 'one-of-a-kind mats from small shops', 'mat shop', '#e0607e', [0, 6, 9, 10]),
 (8398036, 'mahj-and-vine', 'Mahj & Vine', 'chinoiserie mats in every color', 'mat shop', '#1f5a3a', [4, 6, 7, 13]),
 (8398013, 'charleston-mahjong-club', 'Charleston Mahjong Club', 'club mats, bags and tablecloths', 'brand shop', '#054689', [3, 5, 6, 12]),
 (8387635, 'tala-mahj', 'Tala Mahj Favorites', 'my favorite fringe mats', 'mat shop', '#c46a2b', [1, 9, 3, 8]),
 (8392650, 'the-mahjong-house', 'The Mahjong House', 'jewel-tone and island tile sets', 'tile shop', '#054689', [8, 2, 13, 12]),
 (8398045, 'bam-lets-mahjong', "BAM! Let's Mahjong", 'tiles, mats and shufflers that match', 'brand shop', '#b3202a', [4, 8, 5]),
 (8398138, 'mahjong-lamps', 'Mahjong Lamps', 'cordless lamps for a cozy game night', 'table shop', '#c4932b', [4, 1, 10, 3]),
 (8400954, 'mahjong-tablecloths', 'Mahjong Tablecloths', 'the layer under your mat', 'table shop', '#1f5a3a', [0, 3, 1]),
 (8393657, 'dice-dishes', 'Dice Dishes & Accessories', 'the little extras that finish a table', 'table shop', '#e0607e', [11, 7, 0, 1]),
 (8399799, 'mahjong-storage', 'Mahjong Storage', 'bags and totes for your set', 'storage', '#054689', [1, 0, 2]),
 (8399101, 'racks', 'Mahjong Racks', 'racks and pushers for every set', 'rack shop', '#054689', [1, 0, 5]),
 (8401175, 'a-reindeer-holiday-table', 'A Reindeer Holiday Table', 'santa, reindeer and cherry red', 'shop the look', '#b3202a', [0, 4, 1, 5]),
 (8401385, 'a-classic-plaid-holiday-table', 'A Classic Plaid Holiday Table', 'tartan, walnut and candlelight', 'shop the look', '#054689', [9, 8, 2, 7]),
 (8401290, 'a-retro-holiday-table', 'A Retro Holiday Table', 'red plaid and a glowing ceramic tree', 'shop the look', '#4f6b3a', [0, 1, 3, 5]),
]

def card(path, size, rot):
    im = Image.open(path).convert('RGB')
    from PIL import ImageChops
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

def make(cid, slug, title, tag, kicker, accent, picks):
    W = H = 1080; c = Image.new('RGBA', (W, H), BG + (255,)); d = ImageDraw.Draw(c)
    logo = Image.open(R + 'assets/brand/mahjmatchmaker-wordmark-notag.png').convert('RGBA')
    lw = 330; logo = logo.resize((lw, int(lw * logo.height / logo.width)), Image.LANCZOS)
    c.alpha_composite(logo, ((W - lw) // 2, 46))
    kf = font('Bitter.woff2', 22); kt = '  '.join(kicker.upper())
    d.text((W / 2, 128), kt, font=kf, fill=NAVY, anchor='mm')
    ts = 96
    while d.textlength(title, font=font('Caprasimo.woff2', ts)) > W - 110 and ts > 64: ts -= 2
    lines = [title]
    if d.textlength(title, font=font('Caprasimo.woff2', ts)) > W - 110:
        ws = title.split(); best = None
        for i in range(1, len(ws)):
            a, b = ' '.join(ws[:i]), ' '.join(ws[i:]); m = max(d.textlength(a, font=font('Caprasimo.woff2', 80)), d.textlength(b, font=font('Caprasimo.woff2', 80)))
            if best is None or m < best[0]: best = (m, [a, b])
        lines = best[1]; ts = 80
        while max(d.textlength(l, font=font('Caprasimo.woff2', ts)) for l in lines) > W - 110: ts -= 2
    y = 200
    for l in lines:
        d.text((W / 2, y), l, font=font('Caprasimo.woff2', ts), fill=hexc(accent), anchor='mm'); y += int(ts * 1.02)
    pf = font('PlayfairDisplay.woff2', 36)
    try: pf.set_variation_by_name('Italic')
    except Exception: pass
    d.text((W / 2, y + 2), tag, font=pf, fill=INK, anchor='mm')
    top = y + 40
    imgs = [os.path.join(IMG, f'{cid}_{k:02d}.jpg') for k in picks]
    imgs = [p for p in imgs if os.path.exists(p)]
    area_c = (top + H) / 2 + 5; avail = H - top - 30
    hero = min(int(avail * .80), 500); side = int(min(hero * .62, 300))
    if len(imgs) >= 4:
        pos = [(185, area_c - avail * .20, side, -6), (895, area_c - avail * .16, side, 5), (190, area_c + avail * .24, int(side * .92), 4), (890, area_c + avail * .27, int(side * .85), -4), (540, area_c + 8, hero, -1.5)]
        order = [imgs[1], imgs[2], imgs[3], imgs[4] if len(imgs) > 4 else None, imgs[0]]
        pos = [p for p, o in zip(pos, order) if o]; order = [o for o in order if o]
    elif len(imgs) == 3:
        pos = [(195, area_c, side, -6), (885, area_c, side, 6), (540, area_c, hero, -1)]
        order = [imgs[1], imgs[2], imgs[0]]
    else:
        pos = [(540, area_c, hero, -1)]; order = imgs[:1]
    for p, (cx, cy, s, r) in zip(order, pos): place(c, card(p, s, r), cx, cy)
    c.convert('RGB').save(OUT + slug + '.jpg', quality=90)
    return OUT + slug + '.jpg'

if __name__ == '__main__':
    only = sys.argv[2:] 
    for row in COVERS:
        if not only or row[1] in only: print(make(*row))
