"""Render the first sample of each Canva template idea (Tiffany, Oct 25: one sample each, no full library until she approves).
Flat JPGs at 1080x1920 (stories/reels). The sticker is a transparent PNG for Instagram's photo sticker."""
import os
from playwright.sync_api import sync_playwright
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__))
CARD = f'file://{D}/fym-card-cypress-eltigre-story.png'
PH = 'file:///home/claude/fymapp/caps/swipe-Cypress-El_Tigre.png'
TPL = open(D + '/tpl.html').read()

A = f'''<div class="blob" style="width:980px;height:980px;left:50px;top:520px"></div>
<div class="c" style="top:255px"><span class="pill">RATE THIS MATCH</span></div>
<div class="c cap" style="top:335px;font-size:84px;line-height:1">Would you play<br>on this?</div>
<img src="{CARD}" style="position:absolute;left:240px;top:540px;width:600px;border-radius:30px;transform:rotate(-2deg);box-shadow:0 30px 60px rgba(6,42,85,.28)">
<div class="zone" style="left:190px;right:190px;top:1610px;height:150px">YOUR SLIDER / POLL STICKER</div>
<div class="h" style="left:70px;top:1180px;font-size:80px">♥</div><div class="h" style="right:70px;top:700px;font-size:64px;color:#c8325f">♥</div>'''

B = f'''<div style="position:absolute;inset:0;background:#062a55"></div>
<div class="c" style="top:270px"><span class="pill" style="background:#d6336c">MATCH OF THE WEEK</span></div>
<div class="c cap" style="top:355px;font-size:96px;line-height:1;color:#fff">Cypress<br><span style="color:#f56c8c">×</span> El Tigre</div>
<div style="position:absolute;left:150px;top:600px;width:780px;height:1040px;border-radius:30px;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.4)">
 <img src="{CARD}" style="position:absolute;width:780px;left:0;top:-300px"></div>
<div class="c it" style="top:1700px;color:#f7b6c8;font-size:44px">tiles · mat · racks, across brands</div>'''

B_GUIDE = B + '''<div style="position:absolute;left:0;right:0;top:240px;height:1440px;border-top:6px dashed #ffd23f;border-bottom:6px dashed #ffd23f"></div>
<div class="c" style="top:190px;color:#ffd23f;font:700 30px Bit;letter-spacing:3px">GRID SHOWS ONLY BETWEEN THE LINES (3:4)</div>'''

C = f'''<div class="blob" style="width:1000px;height:1000px;left:40px;top:640px"></div>
<div class="c" style="top:255px"><span class="pill">FIND YOUR MAT-CH™</span></div>
<div class="c cap" style="top:335px;font-size:88px;line-height:1">Start with<br>your tiles.</div>
<div class="c it" style="top:525px">…we'll find the mat.</div>
<div class="phone" style="left:255px;top:630px;width:570px;transform:rotate(-2deg)"><div class="scr"><img src="{PH}"></div></div>
<div class="h" style="left:90px;top:900px;font-size:76px">♥</div><div class="h" style="right:80px;top:1400px;font-size:60px;color:#c8325f">♥</div>'''

STICKER = '''<style>body{background:transparent!important}</style>
<div style="position:absolute;left:90px;top:90px;width:900px;transform:rotate(-4deg);background:#d6336c;border-radius:60px;padding:46px 40px 40px;text-align:center;box-shadow:0 16px 40px rgba(6,42,85,.3);border:8px solid #fff">
 <div style="font-family:Cap;color:#fff;font-size:120px;line-height:1">Great match!</div>
 <div style="font:700 44px Bit;color:#fff;letter-spacing:3px;margin-top:14px">SHARE YOURS #MAHJMATCH 💗</div></div>'''

D_PREVIEW = f'''<div style="position:absolute;inset:0;background:linear-gradient(#e9d7c6,#c9a98c)"></div>
<div style="position:absolute;left:140px;top:430px;width:800px;height:1000px;background:#fff;border-radius:24px;box-shadow:0 20px 50px rgba(0,0,0,.25);overflow:hidden">
 <div style="height:90px;display:flex;align-items:center;padding:0 26px;font:700 30px Bit;color:#222">◯ &nbsp;a_follower</div>
 <div style="position:absolute;top:90px;left:0;right:0;bottom:0;overflow:hidden"><img src="{CARD}" style="width:800px;position:relative;top:-330px"></div></div>
<img src="file://{D}/sticker-great-match.png" style="position:absolute;left:300px;top:260px;width:560px">'''


def shot(pg, body, out, w=1080, h=1920, png=False):
    open(D + '/_r.html', 'w').write(TPL.replace('__BODY__', body))
    pg.set_viewport_size({'width': w, 'height': h})
    pg.goto('file://' + D + '/_r.html'); pg.wait_for_timeout(900)
    if png:
        pg.screenshot(path=out, omit_background=True)
    else:
        pg.screenshot(path=D + '/_r.png'); Image.open(D + '/_r.png').convert('RGB').save(out, quality=92)
    print(out)


with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    shot(pg, A, D + '/A-rate-this-match-story.jpg')
    shot(pg, B, D + '/B-match-of-the-week-reel-cover.jpg')
    shot(pg, B_GUIDE, D + '/B-reel-cover-grid-guide.jpg')
    shot(pg, C, D + '/C-iphone-screenshot-story.jpg')
    shot(pg, STICKER, D + '/sticker-great-match.png', 1080, 520, png=True)
    shot(pg, D_PREVIEW, D + '/D-reshare-with-sticker-preview.jpg')
    b.close()
for f in ('_r.html', '_r.png'):
    try: os.remove(D + '/' + f)
    except OSError: pass
