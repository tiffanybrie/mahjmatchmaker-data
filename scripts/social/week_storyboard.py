"""Next-week social storyboards (Fridays prep): STILLS ONLY for Tiffany's OK, built from existing content.
Usage: python3 scripts/social/week_storyboard.py  -> assets/social/week-2026-11-02/*.jpg
Each day = one sheet: header (day, time, where) + numbered panels (feed slides / story frames) + panel notes.
Text panels are rough type; final pieces use the saved templates (its_a_match/render.py, holiday-tables reels) after her yes.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(R, 'assets/social/week-2026-11-02')
CARDS = os.path.join(R, 'assets/cards/holiday-v4')
CAPS = os.path.join(R, 'assets/social/fym-launch/app-caps')
TAB = os.path.join(R, 'assets/social/holiday-tables')
CAP = os.path.join(R, 'assets/fonts/Caprasimo.ttf')
BIT = os.path.join(R, 'scripts/albumcard/woodfix/Bitter-Bold.ttf')
DJ = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
NAVY, PINK, CREAM, RED = (27, 42, 89), (196, 52, 98), (250, 243, 234), (160, 26, 44)


def f(p, s):
    try:
        return ImageFont.truetype(p, s)
    except OSError:
        return ImageFont.truetype(DJ, s)


def card(name):
    return Image.open(os.path.join(CARDS, name + '.jpg')).convert('RGB')


def text_slide(lines, size=(1080, 1350), bg=CREAM, note=None):
    im = Image.new('RGB', size, bg)
    d = ImageDraw.Draw(im)
    y = size[1] * 0.22
    for txt, fs, col, font in lines:
        fo = f(font, fs)
        w = d.textlength(txt, font=fo)
        d.text(((size[0] - w) / 2, y), txt, font=fo, fill=col)
        y += fs * 1.35
    if note:
        fo = f(DJ, 30)
        w = d.textlength(note, font=fo)
        d.text(((size[0] - w) / 2, size[1] - 120), note, font=fo, fill=(120, 120, 120))
    return im


def phone(cap, size=(1080, 1350), title=None, bg=CREAM):
    im = Image.new('RGB', size, bg)
    d = ImageDraw.Draw(im)
    top = 150 if title else 60
    if title:
        fo = f(CAP, 64)
        w = d.textlength(title, font=fo)
        d.text(((size[0] - w) / 2, 50), title, font=fo, fill=NAVY)
    s = Image.open(cap).convert('RGB')
    h = size[1] - top - 50
    s = s.resize((int(s.width * h / s.height), h))
    fr = Image.new('RGB', (s.width + 36, s.height + 36), NAVY)
    fr.paste(s, (18, 18))
    im.paste(fr, ((size[0] - fr.width) // 2, top - 18))
    return im


def placeholder(label, size=(1080, 1350)):
    im = Image.new('RGB', size, (236, 236, 240))
    d = ImageDraw.Draw(im)
    d.rectangle([20, 20, size[0] - 20, size[1] - 20], outline=NAVY, width=6)
    fo = f(DJ, 44)
    y = size[1] / 2 - 80
    for ln in label.split('\n'):
        w = d.textlength(ln, font=fo)
        d.text(((size[0] - w) / 2, y), ln, font=fo, fill=NAVY)
        y += 60
    return im


def its_a_match_s1(card_img, tile, mat, brands):
    """Rough slide 1 of the saved It's a mat-ch! template: tile crop + mat crop + names."""
    im = Image.new('RGB', (1080, 1350), CREAM)
    d = ImageDraw.Draw(im)
    fo = f(CAP, 110)
    t = "It's a mat-ch!"
    d.text(((1080 - d.textlength(t, font=fo)) / 2, 110), t, font=fo, fill=PINK)
    c = card_img
    tile_crop = ImageOps.fit(c.crop((660, 590, 1080, 1105)), (380, 380))
    mat_crop = ImageOps.fit(c.crop((0, 135, 640, 700)), (440, 440))
    mask = Image.new('L', (380, 380), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, 380, 380], fill=255)
    im.paste(tile_crop, (90, 380), mask)
    im.paste(mat_crop, (560, 350))
    fo2 = f(CAP, 90)
    d.text((488, 500), '♥', font=f(DJ, 90), fill=PINK)
    y = 870
    for txt, fs, col, font in [(f'{tile} + {mat}', 54, NAVY, BIT), (brands, 36, PINK, BIT),
                               ('Mock up your own in Find Your Mat-ch', 40, NAVY, BIT),
                               ('mahjmatchmaker.com', 40, NAVY, BIT)]:
        fo = f(font, fs)
        d.text(((1080 - d.textlength(txt, font=fo)) / 2, y), txt, font=fo, fill=col)
        y += fs * 1.6
    return im


def sheet(fname, header, sub, panels, cols=4):
    pw = 300
    rows = (len(panels) + cols - 1) // cols
    ph_max = 0
    thumbs = []
    for im, note in panels:
        th = im.resize((pw, int(im.height * pw / im.width)))
        ph_max = max(ph_max, th.height)
        thumbs.append((th, note))
    W = 40 + cols * (pw + 30)
    H = 170 + rows * (ph_max + 130) + 20
    S = Image.new('RGB', (W, H), (255, 253, 208))  # light yellow, matches the HQ needs card
    d = ImageDraw.Draw(S)
    d.text((40, 30), header, font=f(BIT, 44), fill=NAVY)
    d.text((40, 95), sub, font=f(DJ, 24), fill=(70, 70, 70))
    for i, (th, note) in enumerate(thumbs):
        x = 40 + (i % cols) * (pw + 30)
        y = 170 + (i // cols) * (ph_max + 130)
        S.paste(th, (x, y))
        d.rectangle([x, y, x + 34, y + 30], fill=NAVY)
        d.text((x + 8, y + 2), str(i + 1), font=f(DJ, 22), fill='white')
        fo = f(DJ, 18)
        words, line, ly = note.split(), '', y + th.height + 8
        for w_ in words:
            if d.textlength(line + ' ' + w_, font=fo) > pw:
                d.text((x, ly), line.strip(), font=fo, fill=(40, 40, 40)); ly += 22; line = ''
            line += ' ' + w_
        d.text((x, ly), line.strip(), font=fo, fill=(40, 40, 40))
    S.save(os.path.join(OUT, fname), quality=88)
    print('wrote', fname, S.size)


def frames(folder, prefix):
    return [Image.open(os.path.join(TAB, folder, f'{prefix}-story-0{i}.jpg')).convert('RGB') for i in range(1, 8)]


def reel_still(folder, mp4):
    import subprocess
    p = os.path.join(OUT, f'_{folder}_reel_t2.jpg')
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', '2', '-i', os.path.join(TAB, folder, mp4),
                    '-frames:v', '1', p], check=False)
    return Image.open(p).convert('RGB') if os.path.exists(p) else placeholder('reel still')


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    ds = os.path.join(CAPS, 'set-Dear_Santa.png')

    # MON Nov 2: Merry Mahjong kickoff (carousel; same stills = reel storyboard; story = every slide)
    mon = [
        (text_slide([("'Tis the season", 96, NAVY, CAP), ('for holiday mat matching', 64, NAVY, CAP), ('', 40, NAVY, BIT),
                     ('11 Christmas albums', 58, PINK, BIT), ('100+ holiday mats', 58, PINK, BIT),
                     ('12 holiday tile sets', 58, PINK, BIT)], note='rough type; reel = counters ticking up'),
         'Hook + counts (numbers from the Oct 28 stock check; recount the morning of)'),
        (phone(ds, title='Pick your tiles, tap Holiday'), 'REAL APP: Dear Santa in Find Your Mat-ch, Holiday on, ✕/♥ (recapture from 1.8 at render)'),
        (card('dear-santa-mahjong-tiles-anders-ruff-candy-cane-lane-mat'), 'Dear Santa x Candy Cane Lane (her #1 Dear Santa card) · Anders Ruff'),
        (card('nutcracker-ballet-mahjong-tiles-mahj-squad-clara-s-dream-christmas-mat'), "Nutcracker Ballet x Clara's Dream (her #1) · Mahj Squad"),
        (card('holly-jolly-pink-mahjong-tiles-peace-love-mahjong-peace-love-holiday-mat'), 'Holly Jolly Sugarplum Pink x Peace Love Holiday (her #1) · Bam! + PLM'),
        (card('tinselle-ruby-mahjong-tiles-sunday-mahjong-festive-plaid-mat'), 'Tinselle Ruby x Festive Plaid (her #1) · Virora + Sunday'),
        (text_slide([('Find', 70, NAVY, CAP), ('Your Mat-ch™', 90, NAVY, CAP), ('', 30, NAVY, BIT),
                     ('Code MAHJMATCH', 60, PINK, BIT), ('mahjmatchmaker.com', 48, NAVY, BIT)], note='"Your" in Playfair italic at render'),
         'CTA: tool + code + site'),
    ]
    sheet('mon-nov02-merry-mahjong.jpg', 'MON Nov 2 · 10am ET · Merry Mahjong kickoff',
          'IG carousel (7) + FB Page · story = all 7 frames · reel version = same stills, counters + swipes, her song', mon)

    # TUE Nov 3: It's a mat-ch! Rackin' Rudolph x Candy Cane Lane (AR series #1, cross-brand)
    rr = card('rackin-rudolph-mahjong-tiles-anders-ruff-candy-cane-lane-mat')
    tue = [
        (its_a_match_s1(rr, "Rackin' Rudolph", 'Candy Cane Lane', 'HIP HIP MAHJONG · ANDERS RUFF'), "Slide 1 = saved It's a mat-ch! template (rough here)"),
        (rr, "Slide 2: her #1 Rackin' Rudolph card (racks as on the card)"),
        (placeholder("REAL APP\nRackin' Rudolph\non Candy Cane Lane\n(capture from 1.8\nat render)"), 'Slide 3: Find Your Mat-ch phone, swipe view'),
        (its_a_match_s1(rr, "Rackin' Rudolph", 'Candy Cane Lane', 'HIP HIP MAHJONG · ANDERS RUFF').resize((1080, 1350)), 'Story frame 1 = slide 1 (@andersruffdesignco mention); frames 2-3 = slides 2-3'),
    ]
    sheet('tue-nov03-rudolph-x-candy-cane-lane.jpg', "TUE Nov 3 · 10am ET · It's a mat-ch! Rudolph x Candy Cane",
          'IG carousel (3) + FB Page · story = all 3 · Anders Ruff Christmas #1 (cross-brand: in-stock tiles on their mat)', tue)

    # WED Nov 4: Polo Club holiday table reel + 7 story frames (BUILT Oct, Planoly drafts 01a16476-febc + 01a16477-0078)
    pf = frames('polo', 'polo')
    wed = [(reel_still('polo', 'polo-holiday-table-reel.mp4'), 'Reel (built), her song from the 4 in the reminder')] + \
          [(im, n) for im, n in zip(pf, ['Frame 1 @ohmymahjong', '2', '3', '4', 'Frame 5 poll sticker', '6', 'Frame 7 link sticker → blog'])]
    sheet('wed-nov04-polo-holiday-table.jpg', 'WED Nov 4 · 11am CT · Polo Club table reel + story',
          'Already built + in Planoly as dated drafts. New lint-clean caption. Reminder post (song + stickers)', wed)

    # THU Nov 5: Dear Santa on 7 Anders Ruff Christmas mats (her album order) + real app
    order = ['candy-cane-lane', 'classic-very-merry-mahj', 'evergreen-tartan', 'santa-s-mahjong-mail',
             'tartan-tidings', 'tartan-toile-no-l', 'watercolor-christmas-tree']
    thu = [(text_slide([('Dear Santa,', 100, RED, CAP), ('all I want is...', 70, NAVY, CAP), ('all of them', 70, NAVY, CAP),
                        ('', 30, NAVY, BIT), ('Anders Ruff tiles on 7', 50, PINK, BIT), ('Anders Ruff Christmas mats', 50, PINK, BIT),
                        ('Preorder: mats ship Nov 17', 40, NAVY, BIT)]), 'Hook slide')]
    for i, m in enumerate(order, 1):
        thu.append((card(f'dear-santa-mahjong-tiles-anders-ruff-{m}-mat'), f'Her Dear Santa order #{i}' if i > 1 else 'Her #1 (Candy Cane Lane)'))
    thu.append((phone(ds, title='Swipe them all yourself'), 'REAL APP close: Dear Santa, Holiday, ✕/♥, Bird & Bamboo Cherry Red racks step'))
    sheet('thu-nov05-dear-santa-anders-ruff.jpg', 'THU Nov 5 · 10am ET · Dear Santa on 7 Anders Ruff mats',
          'IG carousel (9) + FB Page · story = all 9 · @andersruffdesignco collab invite · Bird & Bamboo tie-in', thu, cols=5)

    # FRI Nov 6: Rackin' Rudolph holiday table reel + story (BUILT, Planoly drafts 01a16477-0208 + 01a16477-03c8)
    rf = frames('rudolph', 'rudolph')
    fri = [(reel_still('rudolph', 'rudolph-holiday-table-reel.mp4'), 'Reel (built), her song from the 4 in the reminder')] + \
          [(im, n) for im, n in zip(rf, ['Frame 1', '2', '3', '4', '5', '6', 'Frame 7 link sticker'])]
    sheet('fri-nov06-rudolph-holiday-table.jpg', "FRI Nov 6 · 11am CT · Rackin' Rudolph table reel + story",
          'Already built + in Planoly as dated drafts. New lint-clean caption. Reminder post (song + link sticker)', fri)

    # SAT Nov 7: It's a mat-ch! Holly Jolly Rudolph Red x Bespoke Holiday Love (her #1)
    hj = card('holly-jolly-red-mahjong-tiles-bespoke-mahjong-holiday-love-red-green-mat')
    sat = [
        (its_a_match_s1(hj, 'Holly Jolly', 'Holiday Love', "BAM! LET'S MAHJONG · BESPOKE MAHJONG"), "Slide 1 = saved It's a mat-ch! template (rough here)"),
        (hj, 'Slide 2: her #1 Holly Jolly Rudolph Red card'),
        (placeholder('REAL APP\nHolly Jolly Red\non Holiday Love,\ncolour chip taps\n(capture at render)'), 'Slide 3: Find Your Mat-ch phone'),
    ]
    sheet('sat-nov07-holly-jolly-x-holiday-love.jpg', "SAT Nov 7 · 10am ET · It's a mat-ch! Holly Jolly x Holiday Love",
          'IG carousel (3) + FB Page · story = all 3 · tiles in stock in all 3 colours', sat)

    # SUN Nov 8: no new feed post. Story-only recap from Mon frames (plain frames auto-post)
    sun = [(mon[0][0], 'Story 1 (Mon frame 1)'), (mon[1][0], 'Story 2 (real app)'), (mon[6][0], 'Story 3 CTA (add link sticker = reminder)')]
    sheet('sun-nov08-story-recap.jpg', 'SUN Nov 8 · 10am ET · Story-only: Merry Mahjong recap',
          'No feed post (2-hours-a-week system). Reuses Monday frames; nothing new to build', sun)
