#!/usr/bin/env python3
"""Build the Pinterest launch pins (1000x1500) + pins.csv.

Inputs: album #1 cards (live), holiday cards (repo), shop-the-look boards,
Christmas mat photos, Amazon boards. Output: assets/social/pinterest/pins/*.jpg
and assets/social/pinterest/pins.csv (Pinterest bulk-upload columns).
"""
import csv, json, os, sys, datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SP = sys.argv[1]  # scratchpad pins dir (holds src/ + picks.json)
OUT = os.path.join(REPO, 'assets/social/pinterest/pins')
os.makedirs(OUT, exist_ok=True)

NAVY = (5, 70, 137); PINK = (245, 108, 140); CREAM = (251, 243, 230); WHITE = (255, 255, 255)
CAPRA = os.path.join(os.path.dirname(SP), 'fonts/Caprasimo.ttf')
INTERB = '/usr/share/fonts/opentype/inter/Inter-Bold.otf'
INTERM = '/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'
LOGO = Image.open(os.path.join(REPO, 'assets/brand/mahjmatchmaker-wordmark.png')).convert('RGBA')
W, H = 1000, 1500

def font(p, s): return ImageFont.truetype(p, s)

def fit(draw, text, path, size, maxw, minsize=40):
    while size > minsize:
        f = font(path, size)
        if draw.textlength(text, font=f) <= maxw: return f
        size -= 2
    return font(path, minsize)

def wrap(draw, text, path, size, maxw, maxlines=2, minsize=52):
    """Wrap into <= maxlines lines, shrinking font until it fits."""
    while size >= minsize:
        f = font(path, size); words = text.split(); lines = []; cur = ''
        for w in words:
            t = (cur + ' ' + w).strip()
            if draw.textlength(t, font=f) <= maxw: cur = t
            else: lines.append(cur); cur = w
        lines.append(cur)
        if len(lines) <= maxlines: return f, lines
        size -= 4
    return f, lines

def header(cv, title, sub, accent=NAVY):
    d = ImageDraw.Draw(cv)
    lg = LOGO.copy(); lg.thumbnail((330, 80)); cv.paste(lg, ((W - lg.width) // 2, 34), lg)
    f, lines = wrap(d, title, CAPRA, 84, W - 90)
    y = 140
    for ln in lines:
        d.text((W // 2, y), ln, font=f, fill=accent, anchor='ma'); y += int(f.size * 1.12)
    fs = fit(d, sub, INTERM, 36, W - 100, 26)
    d.text((W // 2, y + 8), sub, font=fs, fill=(60, 60, 70), anchor='ma')
    return y + 8 + fs.size + 26

def footer(cv, line1='Find your match at mahjmatchmaker.com', line2='Save with code MAHJMATCH at partner shops', bg=NAVY):
    d = ImageDraw.Draw(cv)
    d.rectangle([0, H - 150, W, H], fill=bg)
    f1 = fit(d, line1, INTERB, 46, W - 80, 30); f2 = fit(d, line2, INTERM, 32, W - 80, 22)
    d.text((W // 2, H - 122), line1, font=f1, fill=WHITE, anchor='ma')
    d.text((W // 2, H - 62), line2, font=f2, fill=(255, 205, 216), anchor='ma')

def place(cv, im, top, bottom, margin=40, radius=22):
    im = im.convert('RGB'); maxw, maxh = W - 2 * margin, bottom - top
    s = min(maxw / im.width, maxh / im.height); im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    x = (W - im.width) // 2; y = top + (maxh - im.height) // 2
    sh = Image.new('RGBA', (im.width + 40, im.height + 40), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([20, 24, im.width + 20, im.height + 24], radius, fill=(0, 0, 0, 60))
    sh = sh.filter(ImageFilter.GaussianBlur(10)); cv.paste(sh, (x - 20, y - 20), sh)
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius, fill=255)
    cv.paste(im, (x, y), m)

def card_crop(path):
    """Keep the card's title + styled match; drop the bottom logo strip and footer
    (old cards carry the retired tagline / old footers)."""
    im = Image.open(path).convert('RGB')
    return im.crop((0, 0, im.width, int(im.height * 0.815)))

pins = []

# ---------- 1. Album #1 match pins ----------
MATCH = [  # slug, set name, tile brand, board
 ('amara','Amara','Oh My Mahjong','Pink Mahjong Tiles and Mat Matches'),
 ('birdie','Birdie','Oh My Mahjong','Blue Mahjong Tiles and Mat Matches'),
 ('cypress-forest','Cypress','Oh My Mahjong','Neutral Mahjong Tiles and Mat Matches'),
 ('emerald','Emerald','Oh My Mahjong','Green Mahjong Tiles and Mat Matches'),
 ('gatsby','Gatsby','Oh My Mahjong','Blue Mahjong Tiles and Mat Matches'),
 ('glow-wild','Glow Wild','Oh My Mahjong','Pink Mahjong Tiles and Mat Matches'),
 ('heritage-2-0','Heritage 2.0','Oh My Mahjong','Neutral Mahjong Tiles and Mat Matches'),
 ('heritage','Heritage','Oh My Mahjong','Neutral Mahjong Tiles and Mat Matches'),
 ('jade','Jade','Miss Mahjong','Green Mahjong Tiles and Mat Matches'),
 ('la-fete','La Fete','Oh My Mahjong','Pink Mahjong Tiles and Mat Matches'),
 ('lagoon','Lagoon','Oh My Mahjong','Blue Mahjong Tiles and Mat Matches'),
 ('malachite','Malachite','Miss Mahjong','Green Mahjong Tiles and Mat Matches'),
 ('moonlight','Moonlight','Oh My Mahjong','Blue Mahjong Tiles and Mat Matches'),
 ('nantucket','Nantucket','Oh My Mahjong','Oh My Mahjong Tile and Mat Matches'),
 ('osler','Osler','Oh My Mahjong','Blue Mahjong Tiles and Mat Matches'),
 ('palm-royale','Palm Royale','Oh My Mahjong','Green Mahjong Tiles and Mat Matches'),
 ('pearlescent','Pearlescent','Oh My Mahjong','Neutral Mahjong Tiles and Mat Matches'),
 ('pippa','Pippa','Oh My Mahjong','Oh My Mahjong Tile and Mat Matches'),
 ('seabreeze','Seabreeze','Oh My Mahjong','Blue Mahjong Tiles and Mat Matches'),
 ('talulah','Talulah','Oh My Mahjong','Neutral Mahjong Tiles and Mat Matches'),
]
picks = {p['slug']: p for p in json.load(open(os.path.join(SP, 'picks.json')))}
# distinct mats matched per live album (counted from the live album pages, Oct 18)
COUNTS = json.load(open(os.path.join(SP, 'counts.json')))
start = datetime.datetime(2026, 10, 21, 11, 0)
for i, (slug, name, tbrand, board) in enumerate(MATCH):
    p = picks[slug]; mat = p['title'].split(' + ', 1)[1]; mbrand = p['brand'].replace('Retired', '').strip()
    cv = Image.new('RGB', (W, H), CREAM)
    n = COUNTS[slug]
    top = header(cv, f'{n} mats that match {name} tiles', f"Shown: Tiffany's #1 pick, the {mat} mat by {mbrand}")
    place(cv, card_crop(os.path.join(SP, p['file'])), top, H - 180)
    footer(cv, f"See all {n} of {name}'s matches \u2192", 'mahjmatchmaker.com  \u00b7  Save with code MAHJMATCH')
    fn = f'{i+1:02d}-{slug}-mahjong-tiles-{mat.lower().replace(" ", "-").replace("&","and")}-mat-pin.jpg'
    cv.save(os.path.join(OUT, fn), quality=88)
    pins.append(dict(file=fn, board=board,
        title=f'{n} Mats That Match {name} Mahjong Tiles',
        desc=(f"See all {n} mahjong mats that match {tbrand} {name} mahjong tiles, each styled with racks that pull the tile colors. "
              f"Shown here: my #1 pick, the {mat} mat by {mbrand}. Find your favorite {name} tile, mat and rack match at mahjmatchmaker.com, and save with code MAHJMATCH at participating partner shops. "
              f"#mahjong #mahjongmat #mahjongtiles #mahjmatchmaker"),
        link=f'https://www.mahjmatchmaker.com/{slug}-mahjong-tile-matches?utm_source=pinterest&utm_medium=social&utm_campaign=launch',
        date=(start + datetime.timedelta(days=i)).strftime('%Y-%m-%dT%H:%M:%S'), holiday=False,
        keywords=f'{name} mahjong tiles, mahjong mat, {mat} mahjong mat, mahjong tile and mat match, {tbrand}'))

# ---------- 2. Holiday shop-the-look boards (already 1000x1500) ----------
hstart = datetime.datetime(2026, 11, 1, 19, 0); hi = 0
def hdate():
    global hi
    d = (hstart + datetime.timedelta(days=hi)).strftime('%Y-%m-%dT%H:%M:%S'); hi += 1; return d
# Search-first holiday table pins (Tiffany, Oct 18): keyword first, short titles,
# framed as "build a holiday table with the tiles you own". The boards' own baked-in
# "How I'm Styling" titles are cropped off (crop = rows to drop from the top).
BOARDS = [
 ('assets/blog/holiday-tablescape/holiday-mahjong-table-polo-club-shop-the-look.jpg','polo-club', 340,
  'Holiday mahjong table with the tiles you own', 'No Christmas mat needed',
  'Holiday Mahjong Table Ideas With Tiles You Own',
  'Holiday mahjong table ideas using the tiles you already own: a plaid mat, Heritage tiles, walnut racks, a candle wreath and a ribboned lamp. No Christmas mat needed, and it stays up all season.',
  'https://www.mahjmatchmaker.com/blog/holiday-mahjong-table'),
 ('assets/blog/holiday-tablescape-rattan/holiday-mahjong-table-rattan-shop-the-look.jpg','retro-rattan', 385,
  'Mahjong Christmas table decor', 'Build a holiday table with the tiles you own',
  'Mahjong Christmas Table Decor Ideas',
  'Mahjong Christmas table decor ideas: a red tartan cloth, a ceramic tree lamp, amber glass coasters, a holly dice dish and walnut racks on a rattan mat. Build a holiday mahjong table with the tiles you own.',
  'https://www.mahjmatchmaker.com/holiday-mahjong-matches'),
 ('assets/blog/holiday-tablescape-rudolph/holiday-mahjong-table-rackin-rudolph-shop-the-look.jpg','rackin-rudolph', 315,
  'Christmas mahjong table ideas', 'A reindeer mat, red cloth and milk glass racks',
  'Christmas Mahjong Table Ideas: Reindeer Theme',
  'Christmas mahjong table ideas with a reindeer mat, a cherry red cloth, scalloped milk glass racks, a bow lamp and a reindeer dice box. Find more Christmas mahjong mats and matches.',
  'https://www.mahjmatchmaker.com/holiday-mahjong-matches'),
]
for src, slug, crop, head, sub, title, desc, link in BOARDS:
    fn = f'holiday-mahjong-table-{slug}-pin.jpg'
    im = Image.open(os.path.join(REPO, src)).convert('RGB'); im = im.crop((0, crop, im.width, im.height))
    cv = Image.new('RGB', (W, H), CREAM); top = header(cv, head, sub, accent=(150, 24, 40))
    place(cv, im, top, H - 180)
    footer(cv, 'More holiday mahjong matches \u2192', 'mahjmatchmaker.com  \u00b7  Save with code MAHJMATCH', bg=(150, 24, 40))
    cv.save(os.path.join(OUT, fn), quality=88)
    pins.append(dict(file=fn, board='Holiday Mahjong Table Ideas', title=title,
        desc=desc + ' Code MAHJMATCH saves at participating partner shops. #holidaymahjong #christmasmahjong #mahjongtable #mahjmatchmaker',
        link=link + '?utm_source=pinterest&utm_medium=social&utm_campaign=holiday', date=hdate(), holiday=True,
        keywords='holiday mahjong table, christmas mahjong table, mahjong christmas decor, holiday mahjong mats'))

# ---------- 3. Holiday tile + mat cards ----------
HOL = [
 ('dear-santa-mahjong-tiles-anders-ruff-candy-cane-lane-mat.jpg','Dear Santa','Candy Cane Lane','Anders Ruff'),
 ('rackin-rudolph-mahjong-tiles-anders-ruff-candy-cane-lane-mat.jpg',"Rackin' Rudolph",'Candy Cane Lane','Anders Ruff'),
 ('holly-jolly-red-mahjong-tiles-bespoke-mahjong-holiday-love-red-green-mat.jpg','Holly Jolly Red','Holiday Love Red & Green','Bespoke Mahjong'),
 ('tinselle-emerald-mahjong-tiles-luxe-mahjong-the-polo-club-mat.jpg','Tinselle Emerald','The Polo Club','Luxe Mahjong'),
 ('nivalee-blue-mahjong-tiles-virora-mahjong-hiverelle-mat.jpg','Nivalee Glacier Blue','Hiverelle','Virora Mahjong'),
 ('nutcracker-ballet-mahjong-tiles-mahj-squad-clara-s-dream-christmas-mat.jpg','Nutcracker Ballet',"Clara's Dream Christmas",'Mahj Squad'),
]
for f, name, mat, mbrand in HOL:
    cv = Image.new('RGB', (W, H), CREAM)
    top = header(cv, f'Christmas mats for {name} tiles', f'Shown: Tiffany\'s #1 holiday pick, {mat} by {mbrand}', accent=(150, 24, 40))
    src = os.path.join(REPO, 'assets/cards/polofix-v1', f)
    if not os.path.exists(src): src = os.path.join(REPO, 'assets/cards/holiday-v4', f)
    place(cv, card_crop(src), top, H - 180)
    footer(cv, f"See all of {name}'s holiday matches \u2192", 'mahjmatchmaker.com  \u00b7  Save with code MAHJMATCH', bg=(150, 24, 40))
    fn = 'holiday-' + f.replace('.jpg', '-pin.jpg'); cv.save(os.path.join(OUT, fn), quality=88)
    pins.append(dict(file=fn, board='Christmas Mahjong Mats', title=f'Christmas Mahjong Mats That Match {name} Tiles',
        desc=(f"See all of my Christmas mat matches for {name} mahjong tiles, each with racks to match. Shown here: my #1 holiday pick, the {mat} mat by {mbrand}. Find every holiday tile, mat and rack match at mahjmatchmaker.com. "
              "Code MAHJMATCH saves at participating partner shops. #christmasmahjong #holidaymahjong #mahjongmat #mahjmatchmaker"),
        link='https://www.mahjmatchmaker.com/holiday-mahjong-matches?utm_source=pinterest&utm_medium=social&utm_campaign=holiday',
        date=hdate(), holiday=True, keywords=f'christmas mahjong mat, {name} mahjong tiles, holiday mahjong, {mat} mahjong mat'))

# ---------- 4. Christmas mat gallery pin (collage) ----------
MATS = ['oh-my-mahjong-winterberry','britt-mills-winter-berry','anders-ruff-tartan-tidings','oh-my-mahjong-clara','mahjong-register-very-merry-wreath',
        'anders-ruff-candy-cane-lane','hip-hip-mahjong-rackin-rudolph','oh-my-mahjong-yuletide','mahj-squad-claras-dream']
cv = Image.new('RGB', (W, H), CREAM); top = header(cv, 'Christmas Mahjong Mats I Love', '40 holiday mahjong mats in one gallery', accent=(150, 24, 40))
grid_top, gap, cell = top + 10, 22, (W - 80 - 2 * 22) // 3
for i, m in enumerate(MATS):
    im = Image.open(os.path.join(REPO, 'assets/blog/christmas-mats', m + '-christmas-mahjong-mat.jpg')).convert('RGB').resize((cell, cell), Image.LANCZOS)
    x = 40 + (i % 3) * (cell + gap); y = grid_top + (i // 3) * (cell + gap)
    mk = Image.new('L', im.size, 0); ImageDraw.Draw(mk).rounded_rectangle([0, 0, cell - 1, cell - 1], 18, fill=255); cv.paste(im, (x, y), mk)
footer(cv, 'See all 40 at mahjmatchmaker.com', bg=(150, 24, 40))
fn = 'christmas-mahjong-mats-gallery-pin.jpg'; cv.save(os.path.join(OUT, fn), quality=88)
pins.append(dict(file=fn, board='Christmas Mahjong Mats', title='Christmas Mahjong Mats: 40 Holiday Mahjong Mats to Shop',
    desc='A gallery of my favorite Christmas mahjong mats from Oh My Mahjong, Britt Mills, Anders Ruff, Hip Hip Mahjong, Mahj Squad and more, plus which mats work with the tiles you already own. Code MAHJMATCH saves at participating partner shops. #christmasmahjong #mahjongmat #holidaymahjong',
    link='https://www.mahjmatchmaker.com/christmas-mahjong-mats?utm_source=pinterest&utm_medium=social&utm_campaign=holiday',
    date=hdate(), holiday=True, keywords='christmas mahjong mats, holiday mahjong mat, mahjong gift ideas'))

# ---------- 5. Amazon boards -> storefront ----------
AMZ = [('amazon-board-polo-club-holiday.jpg', 290, 'Holiday mahjong table decor', 'Plaid cloth, lamp and coasters, all on Amazon',
        'Holiday Mahjong Table Decor From Amazon', 'a cozy plaid'),
       ('amazon-board-retro-rattan-holiday.jpg', 290, 'Mahjong table decor finds', 'A plaid cloth, tree lamp and holly dice dish',
        'Mahjong Table Decor: Amazon Holiday Finds', 'a retro plaid'),
       ('amazon-board-rackin-rudolph.jpg', 290, 'Christmas mahjong decor', 'A red cloth, bow lamp and reindeer dice box',
        'Christmas Mahjong Decor: Amazon Finds', 'a red reindeer')]
for f, crop, head, sub, title, nm in AMZ:
    im = Image.open(os.path.join(REPO, 'assets/amazon-store/boards', f)).convert('RGB'); im = im.crop((0, crop, im.width, im.height))
    cv = Image.new('RGB', (W, H), CREAM); top = header(cv, head, sub)
    place(cv, im, top, H - 180)
    footer(cv, 'Shop my Amazon mahjong finds', 'Linked in my Amazon storefront')
    fn = f.replace('.jpg', '-pin.jpg'); cv.save(os.path.join(OUT, fn), quality=88)
    pins.append(dict(file=fn, board='Amazon Mahjong Finds', title=title,
        desc=f'{title}: everything for {nm} holiday mahjong table, including a 60x60 tablecloth for a standard card table, a lamp, coasters and a dice dish. Works with the tiles you already own. As an Amazon Associate I earn from qualifying purchases. #mahjong #amazonfinds #holidaymahjong',
        link='https://www.amazon.com/shop/heritagesig05', date=hdate(), holiday=True,
        keywords='holiday mahjong table decor, mahjong christmas decor, amazon mahjong finds, mahjong gift ideas'))

json.dump(pins, open(os.path.join(SP, 'pins.json'), 'w'), indent=1)
print(len(pins), 'pins')
