# ShopMy cover cards, PORTRAIT 2:3 (Tiffany Oct 25 9pm: on phones ShopMy's Square tiles are ~2:3 portrait, so 1:1 covers got cropped
# at the sides and ShopMy prints its own name + product count over the bottom). Rules:
#  - canvas 1000x1500 (2:3); nothing important in the outer ~6% left/right (small crop on some phones)
#  - the bottom ~17% (y > 1245) is kept clear: ShopMy overlays the collection name + "N products" there
#  - title stacked on 2-3 lines, as large as fits
# Usage: python3 scripts/shopmy/make_covers_portrait.py <img_dir> <slug> [slug ...]    (rows come from make_covers.COVERS)
import sys
sys.path.insert(0, '/home/claude/tiffanybrie/mahjmatchmaker-data/scripts/shopmy')
import make_covers as M
from make_covers import *
W, H = 1000, 1500; SAFE_BOTTOM = 1245; OUTP = R + 'assets/shopmy/covers-portrait/'

def wrap(d, text, fnt, maxw):
    ws = text.split(); lines = []; cur = ''
    for w in ws:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=fnt) <= maxw: cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    lines.append(cur); return lines

def makeP(cid, slug, title, tag, kicker, accent, layout, picks):
    c = Image.new('RGBA', (W, H), BG + (255,)); d = ImageDraw.Draw(c)
    lw = 560; logo = lockup(lw); c.alpha_composite(logo, ((W - lw) // 2, 46))
    ky = 46 + logo.height + 44
    d.text((W / 2, ky), ' '.join(kicker.upper()).replace('   ', '      '), font=font(BIT, 28), fill=NAVY, anchor='mm')
    # title: biggest size whose balanced wrap fits 860px in <= 3 lines
    for ts in range(132, 70, -4):
        f = font(CAP, ts); ls = wrap(d, title, f, 860)
        if len(ls) <= (2 if len(title) < 22 else 3): break
    y = ky + 40 + ts // 2
    for l in ls:
        d.text((W / 2, y), l, font=f, fill=hexc(accent), anchor='mm'); y += int(ts * 1.0)
    tf = font(PFI, 40); tl = wrap(d, tag, tf, 800); y += 4
    for l in tl:
        d.text((W / 2, y), l, font=tf, fill=INK, anchor='mm'); y += 50
    top = y + 14; avail = SAFE_BOTTOM - top
    n = len(picks)
    if n == 5:
        hero = min(int(avail * .60), 470); s = min(int(avail * .37), 300)
        cy = top + avail / 2
        pos = [(205, top + s * .55, s, -4), (795, top + s * .6, s, 4), (205, SAFE_BOTTOM - s * .55, s, 3), (795, SAFE_BOTTOM - s * .55, s, -3), (500, cy, hero, -1.5)]
        order = [picks[1], picks[2], picks[3], picks[4], picks[0]]
    else:   # 6: hero (picks[0]) bigger top-centre-left, 2 columns x 3 rows
        s = min(int((avail - 20) / 3 * 1.12), 330)
        rows = [top + s * .52, top + avail / 2, SAFE_BOTTOM - s * .52]
        pos = [(250, rows[0], s, -4), (750, rows[0], s, 4), (250, rows[1], s, 3), (750, rows[1], s, -3), (250, rows[2], s, -3), (750, rows[2], s, 3)]
        order = list(picks)
        if layout == 'tc': order = [picks[1], picks[2], picks[3], picks[4], picks[5], picks[0]]   # hero chair last = on top, but keep grid
    for p, (cx, cy, sz, r) in zip(order, pos): place(c, card(p, int(sz), r), cx, cy)
    os.makedirs(OUTP, exist_ok=True)
    out = OUTP + slug + '.jpg'; c.convert('RGB').save(out, quality=92); return out

def phone_preview(paths, outp, names):
    """Mimic ShopMy mobile tiles: ~452x650 tile, image centre-cropped to fill, name + count overlay at the bottom."""
    tw, th = 452, 650; pad = 10
    sheet = Image.new('RGB', (len(paths) * (tw + pad) + pad, th + 2 * pad), (255, 255, 255))
    for i, (p, nm) in enumerate(zip(paths, names)):
        im = Image.open(p).convert('RGB'); im = ImageOps.fit(im, (tw, th), Image.LANCZOS, centering=(.5, .5))
        ov = Image.new('RGBA', (tw, 120), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        for yy in range(120): od.line([(0, yy), (tw, yy)], fill=(40, 40, 40, int(150 * yy / 120)))
        im = im.convert('RGBA'); im.alpha_composite(ov, (0, th - 120)); dd = ImageDraw.Draw(im)
        dd.text((26, th - 52), nm, font=font(BIT, 26), fill=(255, 255, 255), anchor='lm'); dd.text((26, th - 24), '26 products', font=font(BIT, 18), fill=(235, 235, 235), anchor='lm')
        sheet.paste(im.convert('RGB'), (pad + i * (tw + pad), pad))
    sheet.save(outp, quality=92)

if __name__ == '__main__':
    only = sys.argv[2:]; made = []; names = []
    for row in M.COVERS:
        if row[1] in only: made.append(makeP(*row)); names.append(row[2])
    print(made)
    phone_preview(made, OUTP + 'phone-preview-' + '-'.join(only)[:40] + '.jpg', names)
