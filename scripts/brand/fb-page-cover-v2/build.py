"""Facebook PAGE cover v2 (1640x856), two options + safe-area previews (Oct 19).
A = "Swipe right" dating-app card stack (Papaya Spritz profile + Press for Mahjong mat match).
B = profile-card collage of current sets (Papaya Spritz, Coquette, Luminaire, Willow) around the wordmark.
Usage: python3 scripts/brand/fb-page-cover-v2/build.py   (writes assets/brand/fb-page/cover-v2-*.jpg)
"""
import os, asyncio
from PIL import Image
from playwright.async_api import async_playwright

R = '/home/claude/mahjmatchmaker-data'
F = f'file://{R}/scripts/social/tileprofile/fonts'
OUT = f'{R}/assets/brand/fb-page'
TMP = os.path.dirname(os.path.abspath(__file__)) + '/html'
os.makedirs(TMP, exist_ok=True)
u = lambda p: f'file://{R}/{p}'

HEAD = f"""<!doctype html><html><head><meta charset=utf8><style>
@font-face{{font-family:Capra;src:url('{F}/Caprasimo.ttf')}}
@font-face{{font-family:Hand;src:url('{F}/Caveat-Bold.ttf')}}
@font-face{{font-family:PF;font-style:italic;font-weight:400;src:url('{F}/playfair-display-latin-400-italic.woff2')}}
@font-face{{font-family:PF;font-style:italic;font-weight:600;src:url('{F}/playfair-display-latin-600-italic.woff2')}}
@font-face{{font-family:Bit;font-weight:400;src:url('{F}/bitter-latin-400-normal.woff2')}}
@font-face{{font-family:Bit;font-weight:600;src:url('{F}/bitter-latin-600-normal.woff2')}}
@font-face{{font-family:Bit;font-weight:700;src:url('{F}/bitter-latin-700-normal.woff2')}}
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{--navy:#054689;--flame:#f56c8c;--rose:#c8325f;--cream:#f6e9df;--paper:#fffaf5}}
html,body{{width:1640px;height:856px;overflow:hidden;background:var(--cream);color:var(--navy);font-family:Bit,Georgia,serif}}
.abs{{position:absolute}}
.cap{{font-family:Capra;font-weight:400;line-height:.98}}
.pf{{font-family:PF;font-style:italic}}
.hand{{font-family:Hand}}
.caps{{font:700 15px Bit;letter-spacing:.22em;text-transform:uppercase}}
.ph{{background-size:cover;background-position:center}}
.pill{{display:inline-flex;align-items:center;gap:12px;background:var(--navy);color:#fff;border-radius:999px;font:700 26px Bit;padding:15px 30px;letter-spacing:.02em;white-space:nowrap}}
.pill b{{color:var(--flame);font-weight:700}}
.dot{{width:26px;height:26px;border-radius:50%;box-shadow:0 0 0 3px #fff,0 2px 6px rgba(5,40,90,.18)}}
.card{{background:#fff;border-radius:26px;box-shadow:0 22px 50px rgba(5,40,90,.20),0 3px 10px rgba(5,40,90,.10);overflow:hidden}}
</style></head><body><div style="position:relative;width:1640px;height:856px;overflow:hidden">"""
TAIL = "</div></body></html>"

def dots(cols, size=26):
    return ''.join(f'<span class="dot" style="background:{c};width:{size}px;height:{size}px"></span>' for c in cols)

# ---------------- Option A ----------------
PAPAYA = ['#df772f', '#a99bd0', '#c4dc8c', '#ef7aa0', '#3fb8b0']
A = HEAD + f"""
<!-- soft backdrop shapes -->
<div class="abs" style="right:-140px;top:-160px;width:760px;height:760px;border-radius:50%;background:#f9dccf"></div>
<div class="abs" style="left:-120px;bottom:-260px;width:520px;height:520px;border-radius:50%;background:#efdccd"></div>

<!-- left copy column: everything ends above y~556 so the mobile profile photo (bottom-left) never covers it -->
<div class="abs" style="left:112px;top:138px;width:640px">
  <img src="{u('assets/brand/mahjmatchmaker-wordmark-notag.png')}" style="width:380px;display:block">
  <div class="cap" style="font-size:70px;margin-top:22px;white-space:nowrap">Swipe right on<br>your <span style="color:var(--rose)">perfect mat.</span></div>
  <div class="pf" style="font-size:29px;line-height:1.3;margin-top:12px;color:#2e4f7d">Tiles, mats &amp; racks, matched by color.</div>
  <div style="display:flex;align-items:center;gap:22px;margin-top:22px"><span class="pill">Find your match <b>&middot;</b> 10.27</span><span class="caps" style="font-size:16px;color:var(--rose)">mahjmatchmaker.com</span></div>
</div>
<!-- card stack -->
<div class="abs card" style="left:790px;top:176px;width:340px;height:520px;transform:rotate(-9deg);background:#e9dcf3"></div>
<div class="abs card" style="left:800px;top:166px;width:340px;height:520px;transform:rotate(5deg);background:#d9ecc4"></div>
<div class="abs card" style="left:796px;top:132px;width:350px;height:560px">
  <div class="ph" style="height:318px;background-image:url({u('assets/tiles/album/papaya-spritz.jpg')})"></div>
  <div class="abs" style="left:16px;top:16px;background:rgba(255,255,255,.92);border-radius:999px;padding:7px 14px;font:700 13px Bit;letter-spacing:.16em;color:var(--rose)">NEW GIRL</div>
  <div style="padding:18px 24px 0">
    <div class="cap" style="font-size:44px;color:#e0702a;white-space:nowrap">Papaya Spritz</div>
    <div class="caps" style="font-size:13px;color:#5a6b85;margin-top:6px">Oh My Mahjong</div>
    <div class="pf" style="font-size:21px;line-height:1.3;margin-top:10px">Seeking: pink, peach or periwinkle.</div>
    <div style="display:flex;gap:10px;margin-top:14px">{dots(PAPAYA, 24)}</div>
  </div>
</div>
<!-- swipe buttons -->
<div class="abs" style="left:858px;top:654px;width:76px;height:76px;border-radius:50%;background:#fff;box-shadow:0 10px 24px rgba(5,40,90,.20);display:flex;align-items:center;justify-content:center;font:700 38px Bit;color:#9aa6b8">&#x2715;</div>
<div class="abs" style="left:1010px;top:646px;width:92px;height:92px;border-radius:50%;background:var(--flame);box-shadow:0 12px 28px rgba(200,50,95,.35);display:flex;align-items:center;justify-content:center">
  <svg width="46" height="42" viewBox="0 0 24 22"><path d="M12 21s-9-5.6-9-12.2C3 5.6 5.4 3 8.4 3c1.6 0 2.9.8 3.6 2 .7-1.2 2-2 3.6-2C18.6 3 21 5.6 21 8.8 21 15.4 12 21 12 21z" fill="#fff"/></svg></div>

<!-- match -->
<div class="abs hand" style="left:1210px;top:140px;font-size:58px;color:var(--rose);transform:rotate(-4deg);white-space:nowrap">It's a match!</div>
<img class="abs" src="{u('assets/brand/flame-heart.png')}" style="left:1150px;top:386px;width:64px;z-index:3;filter:drop-shadow(0 6px 10px rgba(200,50,95,.3))">
<div class="abs card" style="left:1200px;top:228px;width:320px;padding:14px 14px 0;transform:rotate(4deg);border-radius:20px">
  <div class="ph" style="width:292px;height:292px;border-radius:10px;background-image:url({u('assets/colorcards/papaya-spritz/mats/press-for-mahjong-anders-ruff.jpg')})"></div>
  <div style="padding:14px 4px 16px;text-align:center">
    <div class="cap" style="font-size:28px">Press for Mahjong</div>
    <div class="caps" style="font-size:12px;color:#5a6b85;margin-top:6px">mat &middot; Anders Ruff</div>
  </div>
</div>
""" + TAIL

# ---------------- Option B ----------------
SETS = [
    # name, brand, tile, accent, swatches, line
    ('Papaya Spritz', 'Oh My Mahjong', 'assets/tiles/album/papaya-spritz.jpg', '#e0702a', ['#df772f', '#a99bd0', '#c4dc8c'], 'Papaya, lavender &amp; lime'),
    ('Coquette', 'LoveShackFancy x OMM', 'assets/tiles/album/coquette.jpg', '#d6608c', ['#e8a9bf', '#c9dbef', '#cfc3e6'], 'Pink, powder blue &amp; lilac'),
    ('Luminaire', 'Oh My Mahjong', 'assets/tiles/album/luminaire.jpg', '#9a7fc0', ['#f2c1c1', '#c7cce6', '#a59bb5'], 'Blush, periwinkle &amp; lilac'),
    ('Willow', 'Oh My Mahjong', 'assets/tiles/album/willow.jpg', '#6f8550', ['#97a77a', '#1c4a67', '#c4a363'], 'Sage, navy &amp; gold'),
]
def pcard(s, x, y, rot, w=236):
    name, brand, tile, acc, sw, line = s
    return f"""<div class="abs card" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg);border-radius:22px">
  <div class="ph" style="height:{int(w*0.86)}px;background-image:url({u(tile)})"></div>
  <div style="padding:14px 18px 18px">
    <div class="cap" style="font-size:29px;color:{acc};white-space:nowrap">{name}</div>
    <div class="caps" style="font-size:11px;color:#5a6b85;margin-top:5px;letter-spacing:.16em">{brand}</div>
    <div style="display:flex;gap:8px;margin-top:11px;align-items:center">{dots(sw, 20)}</div>
    <div class="pf" style="font-size:16px;margin-top:9px;color:#2e4f7d;white-space:nowrap">{line}</div>
  </div></div>"""

B = HEAD + f"""
<div class="abs" style="left:50%;top:50%;width:900px;height:900px;margin:-450px 0 0 -450px;border-radius:50%;background:radial-gradient(circle,#fff6ef 0,#fbe6dc 55%,rgba(246,233,223,0) 72%)"></div>
{pcard(SETS[1], 112, 156, -8)}
{pcard(SETS[0], 350, 222, 5)}
{pcard(SETS[2], 1054, 222, -5)}
{pcard(SETS[3], 1292, 156, 8)}
<div class="abs" style="left:640px;top:196px;width:360px;text-align:center">
  <img src="{u('assets/brand/flame-heart.png')}" style="width:58px;display:block;margin:0 auto 18px">
  <img src="{u('assets/brand/mahjmatchmaker-wordmark-notag.png')}" style="width:360px;display:block">
  <div class="cap" style="font-size:40px;margin-top:26px;line-height:1.08">Hooking up tiles,<br><span style="color:var(--rose)">mats &amp; racks</span></div>
  <div class="hand" style="font-size:31px;color:var(--flame);margin-top:12px;white-space:nowrap">swipe right on your perfect mat</div>
  <div style="margin-top:22px"><span class="pill" style="font-size:24px;padding:14px 28px">Find your match <b>&middot;</b> 10.27</span></div>
  <div class="caps" style="font-size:15px;color:var(--rose);margin-top:16px">mahjmatchmaker.com</div>
</div>
""" + TAIL

# ---------------- previews ----------------
def preview(img, label):
    # Desktop: page width ~ 1640 shown at 820, crop middle 624 rows. Phone: 16:9-ish, sides trimmed, profile photo bottom-left.
    return f"""<!doctype html><html><head><meta charset=utf8><style>
*{{box-sizing:border-box;margin:0;padding:0}}body{{width:1700px;background:#e9ebee;font-family:Helvetica,Arial,sans-serif;color:#1c1e21;padding:30px}}
h2{{font-size:22px;margin:0 0 12px}} .lbl{{font-size:15px;color:#606770;margin:6px 0 18px}}
.desk{{width:1640px;background:#fff;border-radius:10px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.2)}}
.desk .cov{{width:1640px;height:624px;background:url({img}) center/1640px 856px no-repeat;position:relative}}
.desk .bar{{height:150px;position:relative}}
.desk .pp{{position:absolute;left:60px;top:-70px;width:200px;height:200px;border-radius:50%;border:6px solid #fff;background:url({u('assets/brand/fb-page/mahj-matchmaker-page-profile-1080.jpg')}) center/cover}}
.desk .nm{{position:absolute;left:290px;top:24px;font-size:36px;font-weight:700}} .desk .sub{{position:absolute;left:292px;top:76px;font-size:18px;color:#606770}}
.row{{display:flex;gap:40px;align-items:flex-start;margin-top:30px}}
.phone{{width:430px;background:#fff;border-radius:36px;border:10px solid #111;overflow:hidden;height:560px;position:relative}}
.phone .cov{{width:410px;height:{round(410*856/1520)}px;background:url({img}) center/{round(410*1640/1520)}px auto no-repeat;position:relative}}
.phone .pp{{position:absolute;left:14px;top:{round(410*856/1520)-90}px;width:150px;height:150px;border-radius:50%;border:5px solid #fff;background:url({u('assets/brand/fb-page/mahj-matchmaker-page-profile-1080.jpg')}) center/cover}}
.phone .nm{{position:absolute;left:18px;top:{round(410*856/1520)+70}px;font-size:24px;font-weight:700}}
.full{{width:820px;position:relative}} .full img{{width:820px;display:block}}
.full .z{{position:absolute;left:0;right:0;background:rgba(220,30,60,.28);border:0 dashed #c00}}
.full .pz{{position:absolute;left:0;bottom:0;width:150px;height:150px;border:3px dashed #c00;border-radius:0 50% 0 0;background:rgba(220,30,60,.18)}}
</style></head><body>
<h2>{label} &mdash; desktop Page (Facebook shows the middle 1640x624)</h2>
<div class="desk"><div class="cov"></div><div class="bar"><div class="pp"></div><div class="nm">Mahj Matchmaker</div><div class="sub">Mahjong tiles, mats &amp; racks, matched</div></div></div>
<div class="row">
 <div><h2>Phone</h2><div class="lbl">sides trimmed, profile photo over the lower-left</div>
  <div class="phone"><div class="cov"></div><div class="pp"></div><div class="nm">Mahj Matchmaker</div></div></div>
 <div><h2>Full file with crop-risk zones</h2><div class="lbl">red bands = cut on desktop (top/bottom 116px); dashed corner = phone profile photo</div>
  <div class="full"><img src="{img}"><div class="z" style="top:0;height:{116/2}px"></div><div class="z" style="bottom:0;height:{116/2}px"></div><div class="pz"></div>
  <div style="position:absolute;top:0;bottom:0;left:0;width:{60/2}px;background:rgba(30,60,220,.18)"></div><div style="position:absolute;top:0;bottom:0;right:0;width:{60/2}px;background:rgba(30,60,220,.18)"></div></div>
  <div class="lbl">blue strips = trimmed on phones</div></div>
</div></body></html>"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 1640, 'height': 856}, device_scale_factor=2)
        for key, html in (('A', A), ('B', B)):
            hp = f'{TMP}/cover-{key}.html'
            open(hp, 'w').write(html)
            await pg.goto('file://' + hp); await pg.wait_for_load_state('networkidle'); await pg.evaluate('document.fonts.ready')
            png = f'{TMP}/cover-{key}@2x.png'
            await pg.screenshot(path=png)
            Image.open(png).convert('RGB').resize((1640, 856), Image.LANCZOS).save(f'{OUT}/cover-v2-{key}.jpg', quality=93, optimize=True)
        pv = await b.new_page(viewport={'width': 1700, 'height': 800}, device_scale_factor=1)
        for key in 'AB':
            hp = f'{TMP}/preview-{key}.html'
            open(hp, 'w').write(preview(u(f'assets/brand/fb-page/cover-v2-{key}.jpg'), f'Option {key}'))
            await pv.goto('file://' + hp); await pv.wait_for_load_state('networkidle')
            await pv.screenshot(path=f'{OUT}/cover-v2-{key}-preview.jpg', full_page=True, type='jpeg', quality=88)
        await b.close()

if __name__ == '__main__':
    asyncio.run(main())
    print('done')
