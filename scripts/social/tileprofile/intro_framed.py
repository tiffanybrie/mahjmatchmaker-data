"""Oct 20 (Tiffany): every intro slide sits inside the SAME dating-profile card, so the carousel reads like swiping
through her profile. Rendered as one HTML frame per slide (no pasting over photos, so no edge artifacts):
cream background with the soft circles, the white profile card, 7 progress bars (slide n active), slide content
inside the card, a Mahj Matchmaker sign-off at the bottom of every card, and the 5 Tinder-style buttons.
Slide 1 = the real profile card (swipe_profile.py writes ...-profile-d-card@2x.png). Slides 2-7 = intro.py output.
Usage: python3 intro_framed.py papaya-spritz -> assets/social/<key>-launch/intro-framed/1..7.jpg"""
import sys, os, asyncio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.async_api import async_playwright
from PIL import Image
import swipe_profile as SP
R = '/home/claude/mahjmatchmaker-data'
key = sys.argv[1]; SRC = f'{R}/assets/social/{key}-launch/intro'; OUT = f'{R}/assets/social/{key}-launch/intro-framed'
CARD = f'{R}/assets/colorcards/{key}/00-{key}-mahjong-tiles-profile-d-card@2x.png'
os.makedirs(OUT, exist_ok=True); TMP = os.path.dirname(os.path.abspath(__file__)) + '/html'
F = SP.F; u = lambda p: 'file://' + p
CX, CY, CW, CH = 130, 22, 820, 1281          # card (960x1500 scaled .854)
def page(n):
    bars = ''.join(f'<i style="background:{"#054689" if j == n else "#d6deea"}"></i>' for j in range(1, 8))
    if n == 1:
        inner = f'<img src="{u(CARD)}" style="position:absolute;inset:0;width:100%;height:100%"><div style="position:absolute;left:0;right:0;bottom:0;height:60px;background:#fff"></div>'
    else:
        src = Image.open(f'{SRC}/{n}.jpg'); cream = '#%02x%02x%02x' % src.convert('RGB').getpixel((8, 700))
        inner = (f'<div class="bars">{bars}</div>'
                 f'<div class="panel" style="background:{cream}"><div class="crop" style="background-image:url({u(SRC + f"/{n}.jpg")})"></div><div style="position:absolute;left:0;right:0;top:0;height:48px;background:{cream}"></div></div>')
    return f"""<!doctype html><html><head><meta charset=utf8><style>
@font-face{{font-family:Bit;font-weight:700;src:url('{F}/bitter-latin-700-normal.woff2')}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1080px;height:1350px;overflow:hidden;background:#f6e9df}}
.card{{position:absolute;left:{CX}px;top:{CY}px;width:{CW}px;height:{CH}px;background:#fff;border-radius:38px;overflow:hidden;
  box-shadow:0 26px 60px rgba(5,40,90,.18),0 4px 12px rgba(5,40,90,.09)}}
.bars{{position:absolute;left:22px;right:22px;top:20px;display:flex;gap:9px}}
.bars i{{flex:1;height:7px;border-radius:4px}}
.panel{{position:absolute;left:18px;right:18px;top:44px;bottom:142px;border-radius:24px;overflow:hidden}}
.crop{{position:absolute;inset:0;background-size:contain;background-repeat:no-repeat;background-position:center top 6px}}
.sign{{position:absolute;left:0;right:0;bottom:70px;display:flex;flex-direction:column;align-items:center;gap:4px}}
.sign img{{width:230px}}
.sign span{{font:700 15px Bit;letter-spacing:.22em;text-transform:uppercase;color:#c8325f}}
.btns{{position:absolute;left:0;right:0;top:{CY + CH - 52}px;display:flex;justify-content:center;align-items:center;gap:120px}}
</style></head><body>
<div style="position:absolute;right:-190px;top:-170px;width:650px;height:650px;border-radius:50%;background:#f9dccf"></div>
<div style="position:absolute;left:-170px;bottom:-200px;width:530px;height:530px;border-radius:50%;background:#efdccd"></div>
<div class="card">{inner}
 <div class="sign"><img src="{u(R + '/assets/brand/mahjmatchmaker-wordmark-notag.png')}"><span>Dating profiles for tile sets</span></div>
</div>
<div class="btns">{SP.btn(SP.X, '#054689', 112, 50, stroke=6)}{SP.btn(SP.HEART, '#fff', 112, 54, fill='#fff', stroke=2, bg='#f56c8c')}</div>
</body></html>"""
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1350}, device_scale_factor=2)
        for n in range(1, 8):
            hp = f'{TMP}/framed-{n}.html'; open(hp, 'w').write(page(n))
            await pg.goto('file://' + hp); await pg.wait_for_load_state('networkidle'); await pg.evaluate('document.fonts.ready')
            png = f'{TMP}/framed-{n}@2x.png'; await pg.screenshot(path=png)
            Image.open(png).convert('RGB').resize((1080, 1350), Image.LANCZOS).save(f'{OUT}/{n}.jpg', quality=93)
        await b.close()
asyncio.run(main()); print(OUT)
