# ShopMy covers that work on BOTH shapes (Tiffany Oct 29 4:16pm: tall 2:3 covers looked great on phones but desktop's Square shelf
# centre-crops them to 1000x1000, cutting titles and pictures). Rule: everything that matters sits in the CENTRE SQUARE
# (y 250-1250) minus the name block ShopMy prints over the bottom ~22% of the tile (measured on her phone, Oct 29) => title + picture grid live in y 268-985.
# Phone-only extras sit outside the square: logo + kicker in the top band, tagline in the bottom band (below the square, above the tall-tile overlay).
# Built by re-composing the already-approved portrait covers (assets/shopmy/covers-portrait/<slug>.jpg): the picture grid is cut out and
# re-placed unchanged, the title/logo/tagline are redrawn from the same make_covers.COVERS row.
# Usage: python3 scripts/shopmy/make_covers_dual.py <slug> [slug ...]     (no slugs = all rows that have a portrait cover)
import sys, os
sys.argv = [sys.argv[0], '.'] + sys.argv[1:]
sys.path.insert(0, '/home/claude/tiffanybrie/mahjmatchmaker-data/scripts/shopmy')
import make_covers as M
from make_covers import *
import make_covers_portrait as P
from PIL import Image, ImageDraw, ImageChops
W, H = 1000, 1500
OUT = R + 'assets/shopmy/covers-dual/'
SQ_TOP, GRID_BOTTOM = 268, 985

def old_grid_top(title, tag, kicker):
    d = ImageDraw.Draw(Image.new('RGB', (10, 10)))
    logo = lockup(500); ky = 40 + logo.height + 34
    for ts in range(104, 60, -4):
        f = font(CAP, ts); ls = P.wrap(d, title, f, 840)
        if len(ls) <= 2 or (len(ls) == 3 and ts <= 92): break
    y = ky + 30 + ts // 2 + int(ts * .98) * len(ls) + 2
    tl = P.wrap(d, tag, font(PFI, 36), 820); y += 44 * len(tl)
    return y + 30

def make(cid, slug, title, tag, kicker, accent, n, picks):
    src = Image.open(P.OUTP + slug + '.jpg').convert('RGB')
    gt = int(old_grid_top(title, tag, kicker)) - 6
    reg = src.crop((0, gt, W, 1262)); bgc = Image.new('RGB', reg.size, BG)
    bb = ImageChops.difference(reg, bgc).convert('L').point(lambda v: 255 if v > 14 else 0).getbbox()
    grid = reg.crop(bb); gw, gh = grid.size
    c = Image.new('RGBA', (W, H), BG + (255,)); d = ImageDraw.Draw(c)
    # top band (phone only): logo + kicker
    lw = 460; logo = lockup(lw); c.alpha_composite(logo, ((W - lw) // 2, 52))
    d.text((W / 2, 52 + logo.height + 34), ' '.join(kicker.upper()), font=font(BIT, 24), fill=NAVY, anchor='mm')
    # title (inside the square), as large as fits above the grid
    avail_h = GRID_BOTTOM - gh - 24 - SQ_TOP
    for ts in range(108, 56, -4):
        f = font(CAP, ts); ls = P.wrap(d, title, f, 860)
        if len(ls) * int(ts * .98) <= avail_h and (len(ls) <= 2 or ts <= 92): break
    if len(ls) * int(ts * .98) > avail_h:                      # shrink the grid if the title still doesn't fit
        k = (GRID_BOTTOM - SQ_TOP - 24 - len(ls) * int(ts * .98)) / gh; grid = grid.resize((int(gw * k), int(gh * k)), Image.LANCZOS); gw, gh = grid.size
    gy = GRID_BOTTOM - gh; ty = SQ_TOP + (gy - 14 - SQ_TOP - len(ls) * int(ts * .98)) / 2 + int(ts * .98) / 2
    for l in ls:
        d.text((W / 2, ty), l, font=f, fill=hexc(accent), anchor='mm'); ty += int(ts * .98)
    c.paste(grid, ((W - gw) // 2, gy))
    # bottom band (phone only): tagline, well above the phone overlay
    tf = font(PFI, 38)
    for i, l in enumerate(P.wrap(d, tag, tf, 820)):
        d.text((W / 2, 1310 + i * 46), l, font=tf, fill=INK, anchor='mm')
    os.makedirs(OUT, exist_ok=True); out = OUT + slug + '.jpg'; c.convert('RGB').save(out, quality=92); return out

def preview(paths, names, outp):
    """Top row: desktop Square tile (centre 1:1 crop, name overlay at bottom). Bottom row: phone tile (2:3, overlay at bottom)."""
    s = 420; pw, ph = 280, 420; pad = 10
    sheet = Image.new('RGB', (len(paths) * (s + pad) + pad, s + ph + 3 * pad), (255, 255, 255))
    for i, (p, nm) in enumerate(zip(paths, names)):
        im = Image.open(p).convert('RGB')
        for row, (tw, th) in enumerate(((s, s), (pw, ph))):
            t = ImageOps.fit(im, (tw, th), Image.LANCZOS, centering=(.5, .5)).convert('RGBA')
            oh = int(th * .26); ov = Image.new('RGBA', (tw, oh), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
            for yy in range(oh): od.line([(0, yy), (tw, yy)], fill=(40, 40, 40, int(170 * yy / oh)))
            t.alpha_composite(ov, (0, th - oh)); ImageDraw.Draw(t).text((14, th - 26), nm, font=font(BIT, 18), fill=(255, 255, 255), anchor='lm')
            sheet.paste(t.convert('RGB'), (pad + i * (s + pad), pad if row == 0 else s + 2 * pad))
    sheet.save(outp, quality=90)

if __name__ == '__main__':
    only = sys.argv[2:]; made = []; names = []
    for row in M.COVERS:
        if (not only and os.path.exists(P.OUTP + row[1] + '.jpg') and row[1] != 'mahj-and-moon') or row[1] in only:
            made.append(make(*row)); names.append(row[2])
    print(len(made), made[:3])
    preview(made, names, OUT + 'preview-' + (only[0] if only else 'all') + '.jpg')
