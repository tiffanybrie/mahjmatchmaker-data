"""Cover (9:16), 4:5 feed carousel (7 slides) and 9:16 story frames for the holiday intro, same visual system as reel.py.
Usage: python3 stills.py  -> /dev/shm/holiday-intro/out/{cover.jpg,feed-0N.jpg,story-0N.jpg}"""
import json, os, sys
os.environ['TMPDIR'] = '/dev/shm/holiday-intro/tmp'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel import CFG, FONTS, W, Q
from playwright.sync_api import sync_playwright

CSS = """@font-face{font-family:Cap;src:url(__F__/Caprasimo.ttf)}
@font-face{font-family:Bit;src:url(__F__/bitter-latin-700-normal.woff2);font-weight:700}
@font-face{font-family:Bit;src:url(__F__/bitter-latin-600-normal.woff2);font-weight:600}
@font-face{font-family:PF;src:url(__F__/playfair-display-latin-600-italic.woff2);font-style:italic}
:root{--navy:#062a55;--red:#b3202a;--pine:#1f5a3a;--gold:#e9c77b;--pink:#f56c8c;--rose:#d6336c;--cream:#faf3ea}
*{margin:0;box-sizing:border-box}
body{width:1080px;height:__H__px;overflow:hidden;position:relative;background:var(--navy);font-family:Bit}
.bg{position:absolute;inset:0;overflow:hidden}
.quilt{position:absolute;left:0;top:50%;transform:translateY(-50%);display:grid;grid-template-columns:repeat(6,180px)}
.quilt img{width:180px;height:180px;object-fit:cover;box-shadow:0 0 0 3px #fff}
.plaid{background-color:#9e1b25;background-image:
 repeating-linear-gradient(90deg,rgba(14,64,40,.55) 0 70px,transparent 70px 150px,rgba(255,255,255,.07) 150px 158px,transparent 158px 230px),
 repeating-linear-gradient(0deg,rgba(14,64,40,.55) 0 70px,transparent 70px 150px,rgba(255,255,255,.07) 150px 158px,transparent 158px 230px)}
.safe{position:absolute;left:0;right:0;top:__T__px;bottom:__B__px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:26px}
.card{background:var(--navy);border-radius:40px;padding:46px 56px 52px;box-shadow:0 30px 80px rgba(0,0,0,.5);color:#fff;max-width:920px}
.kick{font:700 34px Bit;letter-spacing:9px;color:var(--gold);text-transform:uppercase}
.cap{font-family:Cap;line-height:1.03}
.pill{display:inline-block;font:700 34px Bit;letter-spacing:4px;padding:15px 34px;border-radius:60px;text-transform:uppercase}
.it{font:italic 600 46px/1.3 PF;color:var(--gold)}
.lab{position:absolute;font:700 30px/1.15 Bit;color:#fff;background:var(--rose);padding:10px 20px;border-radius:16px;white-space:nowrap;box-shadow:0 10px 26px rgba(0,0,0,.28);transform:rotate(-3deg)}
.lab small{display:block;font:600 22px Bit}.lab.n{background:var(--navy)}.lab.x{background:#5e5368}
.ph{position:relative;border-radius:46px;overflow:hidden;border:22px solid #14121a;box-shadow:0 30px 80px rgba(0,0,0,.5);background:#fff}
.ph img{position:absolute;display:block}
.num{font:400 230px/1 Cap;color:var(--cream)}
.stat{display:flex;align-items:baseline;gap:22px;background:rgba(6,42,85,.92);border-radius:30px;padding:16px 40px 22px;box-shadow:0 18px 40px rgba(0,0,0,.4)}
.stat b{font:400 120px/1 Cap;color:var(--gold)}.stat span{font:400 50px/1.05 Cap;color:#fff;text-align:left}
"""
FYM = """Find <span style="font:italic 600 1em/1 PF;color:var(--pink)">Your</span> Mat-ch<sup style="font-size:.36em;vertical-align:top;position:relative;top:.12em">™</sup>"""

def quilt(dim=0.0):
    ims = ''.join(f'<img src="{u}">' for u in (CFG['QU']+['file://'+f for f,n,b in Q[54:]]+CFG['QU'])[:66])
    return f'<div class="bg"><div class="quilt">{ims}</div><div style="position:absolute;inset:0;background:rgba(6,42,85,{dim})"></div></div>'

def phone(src, fw, crop_y, crop_h, w, labels=''):
    # show frame (780 px wide) cropped from crop_y, height crop_h, scaled to width w
    s = w / fw
    return (f'<div class="ph" style="width:{w + 44}px;height:{crop_h * s + 44:.0f}px"><img src="{src}" style="left:0;top:{-crop_y * s:.0f}px;width:{w}px">{labels}</div>')

def slides(H):
    R = CFG
    rec = R['REC'] + '00060.jpg'; rec2 = R['REC2'] + '00041.jpg'
    S = []
    S.append(('plaid', quilt(0.25), f'''<div class="card"><img src="{R['FH']}" style="width:110px"><div class="kick" style="margin-top:14px">Merry Mahjong</div>
      <div class="cap" style="font-size:104px;margin-top:14px">We made a<br>holiday list.</div>
      <div class="it" style="margin-top:22px">So many holiday sets, matched.<br>Swipe to see it →</div></div>'''))
    S.append(('', quilt(0.55), f'''<div class="card" style="background:rgba(6,42,85,.94)"><div class="num">152</div><div class="cap" style="font-size:84px">holiday mats</div>
      <div class="it" style="margin-top:12px">in {FYM}</div></div>'''))
    lab1 = ('<div class="lab n" style="left:24px;top:250px">Dear Santa tiles<small>Anders Ruff</small></div>'
            '<div class="lab" style="left:24px;top:760px">♥ Candy Cane Lane<small>Anders Ruff</small></div>'
            '<div class="lab" style="right:24px;top:520px;transform:rotate(3deg)">Holiday chip on</div>')
    S.append(('plaid', '', f'''<div class="cap" style="font-size:78px;color:#fff;background:var(--navy);padding:14px 34px 22px;border-radius:28px">Pick your tiles.<br>Swipe holiday mats.</div>
      {phone(rec, 780, 230, 1150 if H > 1400 else 980, 700 if H > 1400 else 660, lab1)}'''))
    lab2 = ('<div class="lab n" style="left:24px;top:300px">Festive Plaid Premium<small>Sunday Mahjong · zoomed in</small></div>'
            '<div class="lab" style="left:24px;top:620px">♥ Persimmon<small>Bird & Bamboo</small></div>')
    S.append(('plaid', '', f'''<div class="cap" style="font-size:78px;color:#fff;background:var(--navy);padding:14px 34px 22px;border-radius:28px">Zoom in.<br>Swipe racks to match.</div>
      {phone(rec2, 780, 500, 1120 if H > 1400 else 1010, 700 if H > 1400 else 640, lab2)}'''))
    S.append(('plaid', '', f'''<div class="pill" style="background:var(--pink);color:#fff">It's a match!</div>
      <img src="{R['CARD']}" style="height:{1150 if H > 1400 else 900}px;border-radius:26px;box-shadow:0 30px 80px rgba(0,0,0,.5)">
      <div class="it" style="color:#fff;font-size:40px">Dear Santa tiles · Festive Plaid Premium mat<br>Persimmon + Walnut racks</div>'''))
    tiles = ''.join(f'<img src="{u}" style="width:360px;height:360px;object-fit:cover">' for u in (R['TILES13'] * 2)[:18])
    S.append(('', f'<div class="bg"><div style="display:grid;grid-template-columns:repeat(3,360px)">{tiles}</div><div style="position:absolute;inset:0;background:rgba(6,42,85,.45)"></div></div>',
      f'''<div class="stat"><b>13</b><span>holiday<br>tile sets</span></div><div class="stat"><b>45</b><span>tile set albums with<br>holiday matches</span></div>
      <div class="stat"><b>400+</b><span>holiday matches<br>and counting</span></div>'''))
    S.append(('', '', f'''<img src="{R['FH']}" style="width:130px"><div class="kick">Merry Mahjong</div>
      <div class="cap" style="font-size:100px;color:#fff;white-space:nowrap">{FYM}</div>
      <div class="it" style="color:var(--cream);max-width:860px">The only place to see holiday tiles, mats &amp; racks together, then shop them.</div>
      <div class="pill" style="background:var(--pink);color:#fff;text-transform:none;letter-spacing:2px;font-size:42px;padding:20px 44px">Shop now · use code MAHJMATCH</div>
      <div style="font:700 44px Bit;color:#fff">mahjmatchmaker.com</div>'''))
    return S

def cover():
    return ('', quilt(0.15), f'''<div class="card" style="padding:44px 60px 50px"><img src="{CFG['FH']}" style="width:110px"><div class="kick" style="margin-top:12px">Merry Mahjong</div>
      <div class="cap" style="font-size:150px;margin-top:6px">152</div><div class="cap" style="font-size:78px">holiday mats</div>
      <div class="it" style="margin-top:14px;font-size:44px">matched with tiles &amp; racks<br>in {FYM}</div></div>''')

def html(H, T, B, sl):
    cls, bg, body = sl
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS.replace("__F__", FONTS).replace("__H__", str(H)).replace("__T__", str(T)).replace("__B__", str(B))}</style></head>'
            f'<body class="{cls}">{bg}<div class="safe">{body}</div></body></html>')

if __name__ == '__main__':
    out = f'{W}/out'; os.makedirs(out, exist_ok=True)
    jobs = [('cover', 1920, 560, 560, cover())]
    for i, s in enumerate(slides(1350)): jobs.append((f'feed-{i + 1:02d}', 1350, 120, 120, s))
    for i, s in enumerate(slides(1920)): jobs.append((f'story-{i + 1:02d}', 1920, 290, 400, s))
    with sync_playwright() as p:
        b = p.chromium.launch()
        for name, H, T, B, s in jobs:
            pg = b.new_page(viewport={'width': 1080, 'height': H})
            f = f'{W}/tmp/{name}.html'; open(f, 'w').write(html(H, T, B, s))
            pg.goto('file://' + f); pg.wait_for_timeout(900)
            pg.screenshot(path=f'{out}/{name}.jpg', type='jpeg', quality=90); pg.close()
        b.close()
    print('ok', len(jobs))
