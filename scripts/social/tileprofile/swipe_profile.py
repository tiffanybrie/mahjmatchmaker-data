"""Tile Set Profile, version D = THE STANDARD (Tiffany approved Oct 19, 11:19pm): no LIKE stamp, launch day line, 3 prompts (looking for / love language / irrational fear), no color row.
Based on version C: dating-app profile (Oct 19).
Tiffany asked for a version built from the swipe-app trademarks: photo dashes, LIKE stamp, name + verified check,
green active dot, interest pills, "Looking for", a prompt, basics row and the 5-button row.
Usage: python3 scripts/social/tileprofile/swipe_profile.py   (writes assets/colorcards/papaya-spritz/00-papaya-spritz-mahjong-tiles-profile-c-story.jpg)
Labels stay level (doc 79 label rule, max 12 deg). The LIKE stamp is the one tilted element at -12.
"""
import os, asyncio
from PIL import Image
from playwright.async_api import async_playwright

R = '/home/claude/mahjmatchmaker-data'
F = f'file://{R}/scripts/social/tileprofile/fonts'
u = lambda p: f'file://{R}/{p}'
OUT = f'{R}/assets/colorcards/papaya-spritz/00-papaya-spritz-mahjong-tiles-profile-d-story.jpg'
TMP = os.path.dirname(os.path.abspath(__file__)) + '/html'
os.makedirs(TMP, exist_ok=True)

P = dict(name='Papaya Spritz', brand='Oh My Mahjong', photo='assets/tiles/album/papaya-spritz.jpg',
         active='Launching Wed 10/21', looking='Long-term mat partner',
         pills=['Golden hour', 'Pink mats', 'Garden parties', "Spritz o'clock"],
         love='Coordinating racks',
         prompt_q='My most irrational fear', prompt_a='A beige tablecloth.',
         basics=[('#de7e30', 'Papaya backs'), ('#a8a3e1', 'Lavender layer'), ('#c8d7a5', 'Light lime layer'), ('#ef7aa0', 'Pink faces')],
         matches=50)

def svg(path, color, size, stroke=6, fill='none'):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 48 48"><path d="{path}" fill="{fill}" stroke="{color}" stroke-width="{stroke}" stroke-linecap="round" stroke-linejoin="round"/></svg>'

HEART = 'M24 40 C10 30 6 23 6 17 C6 11 11 7 16 7 C20 7 22 9 24 12 C26 9 28 7 32 7 C37 7 42 11 42 17 C42 23 38 30 24 40 Z'
X = 'M14 14 L34 34 M34 14 L14 34'
STAR = 'M24 6 L29 18 L42 19 L32 28 L35 41 L24 34 L13 41 L16 28 L6 19 L19 18 Z'
BACK = 'M18 12 L8 20 L18 28 M8 20 H30 C36 20 40 25 40 30 C40 36 36 40 30 40 H22'
BOLT = 'M27 5 L11 27 H23 L21 43 L37 20 H25 Z'

def btn(d, color, size, inner, fill='none', stroke=5, bg='#fff'):
    return (f'<div style="width:{size}px;height:{size}px;border-radius:50%;background:{bg};display:flex;align-items:center;justify-content:center;'
            f'box-shadow:0 10px 24px rgba(5,40,90,.16),0 2px 6px rgba(5,40,90,.10)">{svg(d, color, inner, stroke, fill)}</div>')

pills = ''.join(f'<span class="pill">{t}</span>' for t in P['pills'])
basics = ''.join(f'<span class="basic"><span class="dot" style="background:{c}"></span>{t}</span>' for c, t in P['basics'])

HTML = f"""<!doctype html><html><head><meta charset=utf8><style>
@font-face{{font-family:Capra;src:url('{F}/Caprasimo.ttf')}}
@font-face{{font-family:Hand;src:url('{F}/Caveat-Bold.ttf')}}
@font-face{{font-family:PF;font-style:italic;font-weight:400;src:url('{F}/playfair-display-latin-400-italic.woff2')}}
@font-face{{font-family:Bit;font-weight:400;src:url('{F}/bitter-latin-400-normal.woff2')}}
@font-face{{font-family:Bit;font-weight:600;src:url('{F}/bitter-latin-600-normal.woff2')}}
@font-face{{font-family:Bit;font-weight:700;src:url('{F}/bitter-latin-700-normal.woff2')}}
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--navy:#054689;--flame:#f56c8c;--rose:#c8325f;--cream:#f6e9df}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:var(--cream);color:var(--navy);font-family:Bit,Georgia,serif}}
.abs{{position:absolute}}
.card{{position:absolute;left:60px;top:170px;width:960px;height:1500px;background:#fff;border-radius:44px;overflow:hidden;
  box-shadow:0 30px 70px rgba(5,40,90,.20),0 4px 12px rgba(5,40,90,.10)}}
.photo{{position:absolute;left:0;top:0;width:960px;height:930px;background:url('{u(P['photo'])}') center/cover}}
.bars{{position:absolute;left:24px;right:24px;top:22px;display:flex;gap:10px}}
.bars i{{flex:1;height:8px;border-radius:4px;background:rgba(255,255,255,.5)}}
.bars i:first-child{{background:#fff}}
.shade{{position:absolute;left:0;right:0;bottom:0;height:420px;background:linear-gradient(to bottom,rgba(40,14,4,0),rgba(40,14,4,.82))}}
.name{{position:absolute;left:44px;bottom:150px;font-family:Capra;font-size:96px;color:#fff;line-height:1;display:flex;align-items:center;gap:20px}}
.check{{width:62px;height:62px;border-radius:50%;background:#3d8fe0;display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 5px #fff}}
.meta{{position:absolute;left:46px;bottom:92px;font:600 34px Bit;color:#fff;display:flex;align-items:center;gap:14px}}
.meta .g{{width:20px;height:20px;border-radius:50%;background:#5fd36b;box-shadow:0 0 0 4px rgba(95,211,107,.35)}}
.meta .b{{font-weight:400;opacity:.9}}
.info{{position:absolute;right:40px;bottom:96px;width:66px;height:66px;border-radius:50%;border:4px solid #fff;display:flex;align-items:center;justify-content:center}}
.pillrow{{position:absolute;left:44px;right:44px;bottom:26px;display:flex;gap:12px;flex-wrap:nowrap}}
.pill{{font:600 25px Bit;color:#fff;border:2.5px solid rgba(255,255,255,.85);border-radius:999px;padding:8px 20px;white-space:nowrap;background:rgba(255,255,255,.12)}}
.stamp{{position:absolute;left:64px;top:110px;transform:rotate(-12deg);border:9px solid #3fae5a;color:#3fae5a;font:700 104px Bit;letter-spacing:.06em;
  padding:0 26px;border-radius:18px;background:rgba(255,255,255,.80)}}
.body{{position:absolute;left:44px;right:44px;top:966px}}
.box{{background:#fdf4ee;border-radius:26px;padding:22px 30px;margin-bottom:20px}}
.q{{font:700 22px Bit;letter-spacing:.2em;text-transform:uppercase;color:var(--rose);margin-bottom:8px;display:flex;align-items:center;gap:12px}}
.a{{font-family:Capra;font-size:54px;line-height:1.05;color:var(--navy)}}
.pa{{font-family:PF;font-style:italic;font-size:56px;line-height:1.1;color:var(--navy)}}
.basics{{display:flex;flex-wrap:nowrap;gap:9px}}
.basic{{display:inline-flex;align-items:center;gap:10px;font:600 23px Bit;color:var(--navy);background:#fff;border:2.5px solid #ecdcd0;border-radius:999px;padding:8px 16px 8px 10px}}
.dot{{width:26px;height:26px;border-radius:50%;box-shadow:0 0 0 3px #fff,0 1px 4px rgba(5,40,90,.2)}}
.btns{{position:absolute;left:0;right:0;top:1618px;display:flex;justify-content:center;align-items:center;gap:30px}}
.foot{{position:absolute;left:0;right:0;top:1810px;text-align:center;font:700 26px Bit;letter-spacing:.12em;text-transform:uppercase;color:var(--navy)}}
.foot b{{color:var(--rose)}}
</style></head><body><div style="position:relative;width:1080px;height:1920px;overflow:hidden">
<div class="abs" style="right:-220px;top:-200px;width:760px;height:760px;border-radius:50%;background:#f9dccf"></div>
<div class="abs" style="left:-200px;bottom:-240px;width:620px;height:620px;border-radius:50%;background:#efdccd"></div>
<img class="abs" src="{u('assets/brand/mahjmatchmaker-wordmark-notag.png')}" style="left:50%;transform:translateX(-50%);top:58px;width:430px">
<div class="card">
 <div class="photo">
 <div class="bars"><i></i><i></i><i></i><i></i></div>
 <div class="shade"></div>
 <div class="name">{P['name']}<span class="check">{svg('M13 25 L21 33 L36 16', '#fff', 40, 6)}</span></div>
 <div class="meta"><span class="g"></span>{P['active']} <span class="b">· {P['brand']}</span></div>
 <div class="info">{svg('M24 34 V14 M15 22 L24 13 L33 22', '#fff', 40, 5)}</div>
 <div class="pillrow">{pills}</div>
 </div>
 <div class="body">
  <div class="box"><div class="q">{svg(HEART, '#c8325f', 30, 4, '#f56c8c')} Looking for</div><div class="a">{P['looking']}</div></div>
  <div class="box"><div class="q">Love language</div><div class="a">{P['love']}</div></div>
  <div class="box"><div class="q">{P['prompt_q']}</div><div class="pa">{P['prompt_a']}</div></div>
 </div>
</div>
<div class="btns">
 {btn(BACK, '#e8a23a', 92, 44)}
 {btn(X, '#054689', 124, 56, stroke=6)}
 {btn(STAR, '#7d8fe0', 92, 46, fill='#7d8fe0', stroke=3)}
 {btn(HEART, '#fff', 124, 60, fill='#fff', stroke=2, bg='#f56c8c')}
 {btn(BOLT, '#a07ad8', 92, 46, fill='#a07ad8', stroke=3)}
</div>
<div class="foot">See all <b>{P['matches']}</b> of her matches · mahjmatchmaker.com</div>
</div></body></html>"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 1080, 'height': 1920}, device_scale_factor=2)
        hp = f'{TMP}/profile-d.html'; open(hp, 'w').write(HTML)
        await pg.goto('file://' + hp); await pg.wait_for_load_state('networkidle'); await pg.evaluate('document.fonts.ready')
        png = f'{TMP}/profile-d@2x.png'; await pg.screenshot(path=png); await b.close()
    im = Image.open(png).convert('RGB').resize((1080, 1920), Image.LANCZOS); im.save(OUT, quality=93, optimize=True)
    im.save(OUT.replace('profile-d-story', 'profile-c-story'), quality=93, optimize=True)  # same file under the old name other scripts use

if __name__ == '__main__':
    asyncio.run(main()); print(OUT)
