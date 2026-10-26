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
    lw = 500; logo = lockup(lw); c.alpha_composite(logo, ((W - lw) // 2, 40))
    ky = 40 + logo.height + 34
    d.text((W / 2, ky), ' '.join(kicker.upper()), font=font(BIT, 24), fill=NAVY, anchor='mm')
    for ts in range(104, 60, -4):
        f = font(CAP, ts); ls = wrap(d, title, f, 840)
        if len(ls) <= 2 or (len(ls) == 3 and ts <= 92): break
    y = ky + 30 + ts // 2
    for l in ls:
        d.text((W / 2, y), l, font=f, fill=hexc(accent), anchor='mm'); y += int(ts * .98)
    tf = font(PFI, 36); tl = wrap(d, tag, tf, 820); y += 2
    for l in tl:
        d.text((W / 2, y), l, font=tf, fill=INK, anchor='mm'); y += 44
    top = y + 30; bot = SAFE_BOTTOM; zh = bot - top; n = len(picks)
    # cards fill the whole zone: rows x cols grid, cards overlap slightly, slight tilts
    if n >= 6: rows, cols = [3, 3], 2; grid = [3, 3]
    if n >= 6:
        grid = [3, 3]
    elif n == 5: grid = [2, 3]
    else: grid = [n]
    nr = len(grid); maxc = max(grid)
    s = min(int(zh / nr * 1.04), int(900 / maxc * 1.02), 360)
    rowh = min((zh - s) / max(nr - 1, 1), s * 1.04) if nr > 1 else 0
    top += max(0, (zh - (s + rowh * max(nr - 1, 0)))) / 2
    tilts = [-3, 2.5, -2, 3, -2.5, 2, -3, 2]; k = 0
    for ri, cnt in enumerate(grid):
        sz = s if cnt == maxc else int(s * 1.18)
        cy = top + sz / 2 + ri * rowh if nr > 1 else top + zh / 2
        if cnt != maxc: cy = top + s / 2 + ri * rowh - (sz - s) / 2 * (1 if ri == 0 else -1) * 0
        span = 900; step = (span - sz) / max(cnt - 1, 1) if cnt > 1 else 0
        for ci in range(cnt):
            cx = 500 + (0 if cnt == 1 else -span / 2 + sz / 2 + ci * step)
            place(c, card(picks[k % n], int(sz), tilts[k % len(tilts)]), cx, cy); k += 1
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
