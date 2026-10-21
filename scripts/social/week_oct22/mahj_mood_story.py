"""Mahj Mood clear racks + pushers restock: 4-frame stories with REAL product photos (Tiffany, Oct 21 1:13pm: the
first version named the pushers but never showed them). Photos: mahjmood.com/products/<handle>.json, picked by eye,
saved in assets/social/week-oct22/mahj-mood/photos/. Same pink-paper look as the countdown stories.
Two versions: tease (Thu 10/22, "back tomorrow") and drop (Fri 10/23 10am CT, "back").
  1  "Nice racks are back (tomorrow)" + the clear scalloped racks photo; empty band for a VISIBLE @mahj_mood mention
  2  the Malachite scalloped pusher, big: "Malachite owners 👀"
  3  grid of the other new pushers, photo + name
  4  code + link-sticker band
Stories 1080x1920, key content inside y 269-1536.
Run: python3 scripts/social/week_oct22/mahj_mood_story.py -> assets/social/week-oct22/mahj-mood/{tease,drop}/story-N.jpg"""
import os
from playwright.sync_api import sync_playwright
from PIL import Image

R = '/home/claude/mahjmatchmaker-data'
PH = 'assets/social/week-oct22/mahj-mood/photos/'
u = lambda p: f'file://{R}/{p}'
FA = f'file://{R}/assets/fonts'
HEART = ('<svg viewBox="0 0 230 210" style="width:{w}px;vertical-align:middle"><path d="M115 200S12 140 12 72C12 36 38 12 70 12c22 0 37 12 45 '
         '28 8-16 23-28 45-28 32 0 58 24 58 60 0 68-103 128-103 128z" fill="{c}"/></svg>')
CSS = f"""
@font-face{{font-family:Shrikhand;src:url({FA}/shrikhand-latin-400-normal.woff2)}}
@font-face{{font-family:Bitter;font-weight:700;src:url({FA}/bitter-latin-700-normal.woff2)}}
@font-face{{font-family:Playfair;font-style:italic;src:url({FA}/playfair-display-latin-400-italic.woff2)}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1080px;height:1920px;background:linear-gradient(170deg,#fff7f4,#fde3ec);font-family:Bitter,Georgia,serif;color:#064587;position:relative;overflow:hidden}}
.bgdots{{position:absolute;inset:0;background-image:radial-gradient(#f6c9d6 2.2px,transparent 2.6px);background-size:46px 46px;opacity:.55}}
.abs{{position:absolute;left:0;right:0;text-align:center}}
.pill{{display:inline-block;background:#064587;color:#fff;font:700 38px Bitter;letter-spacing:.14em;padding:12px 40px;border-radius:99px}}
.big{{font:118px/1.02 Shrikhand;color:#d6608c;text-shadow:0 8px 0 #fff}}
.mid{{font:80px/1.05 Shrikhand;color:#064587;text-shadow:0 5px 0 #fff}}
.line{{font:italic 54px/1.2 Playfair;color:#064587}}
.ph{{border:12px solid #fff;border-radius:36px;box-shadow:0 18px 50px rgba(6,40,90,.20);background-size:cover;background-position:center}}
.code{{display:inline-flex;align-items:center;gap:18px;background:#d6608c;color:#fff;font:700 50px Bitter;padding:26px 56px;border-radius:99px;box-shadow:0 10px 30px rgba(214,96,140,.35)}}
.nm{{font:700 30px Bitter;color:#064587;margin-top:12px;line-height:1.15}}
.wm{{position:absolute;left:50%;transform:translateX(-50%);width:420px}}
"""
WM = f"<img class=wm src='{u('assets/brand/mahjmatchmaker-wordmark-notag.png')}' style='top:{{t}}px'>"


def page(inner):
    return f"<!doctype html><html><head><meta charset=utf-8><style>{CSS}</style></head><body><div class=bgdots></div>{inner}</body></html>"


def frames(kind):
    tease = kind == 'tease'
    f1 = f"""<div class=abs style='top:285px'><span class=pill>{'RESTOCK · FRI 10/23 · 10AM CT' if tease else 'RESTOCKED TODAY'}</span></div>
<div class='abs big' style='top:385px'>Nice racks</div>
<div class='abs mid' style='top:515px'>{'are back tomorrow.' if tease else 'are back.'}</div>
<div class=ph style='position:absolute;left:90px;top:660px;width:900px;height:675px;background-image:url({u(PH + "racks.jpg")})'></div>
<div class='abs line' style='top:1365px;font-size:46px'>Mahj Mood 20&rdquo; clear scalloped racks</div>"""
    f2 = f"""<div class=abs style='top:285px'><span class=pill>NEW PUSHER</span></div>
<div class='abs mid' style='top:380px;font-size:92px'>Malachite owners 👀</div>
<div class=ph style='position:absolute;left:170px;top:520px;width:740px;height:880px;background-image:url({u(PH + "malachite.jpg")})'></div>
<div class='abs line' style='top:1420px;font-size:48px'>Scalloped Malachite pusher</div>"""
    grid = [('pink.jpg', 'Pink Scalloped'), ('tortoise.jpg', 'Tortoise Scalloped'), ('white.jpg', 'White Scalloped'),
            ('bluepearl.jpg', 'Blue Pearl'), ('greenpearl-crop.jpg', 'Green Pearl'), ('whitepearl.jpg', 'White Pearl')]
    cells = ''.join(f"<div style='text-align:center'><div class=ph style='width:290px;height:290px;border-width:9px;border-radius:28px;background-image:url({u(PH + f)})'></div><div class=nm>{n}</div></div>" for f, n in grid)
    f3 = f"""<div class=abs style='top:285px'><span class=pill>MORE NEW PUSHERS</span></div>
<div class='abs mid' style='top:380px;font-size:84px'>Pick your pusher.</div>
<div style='position:absolute;left:60px;right:60px;top:530px;display:grid;grid-template-columns:repeat(3,1fr);row-gap:34px;justify-items:center'>{cells}</div>"""
    f4 = f"""<div class=abs style='top:420px'>{HEART.format(w=150, c='#d6608c')}</div>
<div class='abs mid' style='top:620px;font-size:92px'>{'Fri 10/23 · 10am CT' if tease else 'Live now'}</div>
<div class='abs line' style='top:750px'>at Mahj Mood</div>
<div class=abs style='top:900px'><span class=code>Use code <b style='letter-spacing:.06em'>MAHJMATCH</b> to save {HEART.format(w=50, c='#fff')}</span></div>"""
    return [f1,  # no wordmark: y 1440-1536 is the band for the visible @mahj_mood mention
             f2 + WM.format(t=1500), f3 + WM.format(t=1460), f4 + WM.format(t=1460)]


with sync_playwright() as p:
    b = p.chromium.launch()
    for kind in ('tease', 'drop'):
        od = f'{R}/assets/social/week-oct22/mahj-mood/{kind}'; os.makedirs(od, exist_ok=True)
        for i, inner in enumerate(frames(kind), 1):
            pg = b.new_page(viewport={'width': 1080, 'height': 1920})
            hp = f'/dev/shm/mm_{kind}_{i}.html'; open(hp, 'w').write(page(inner))
            pg.goto('file://' + hp); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(700)
            pg.screenshot(path=f'/dev/shm/mm_{kind}_{i}.png'); pg.close()
            Image.open(f'/dev/shm/mm_{kind}_{i}.png').convert('RGB').save(f'{od}/story-{i}.jpg', quality=92)
        print('ok', od)
    b.close()
