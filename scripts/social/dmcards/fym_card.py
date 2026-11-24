"""Holiday Find Your Mat-ch DM card (Tiffany Nov 23 8:07pm): WHITE phone, real-looking snow over ONE seamless
background, flame-heart icon (holiday red/green), bullets, the real mahjmatchmaker wordmark + .com, crisp at size.
Usage: fym_card.py <phone.png> <out.jpg> [W H]"""
import sys, asyncio, random, base64
from playwright.async_api import async_playwright
from PIL import Image, ImageFilter
R = '/home/claude/mahjmatchmaker-data/'; F = R + 'scripts/social/tileprofile/fonts/'
import os; phone, out = os.path.abspath(sys.argv[1]), sys.argv[2]; W, H = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (1200, 628)
u = lambda p: 'file://' + p
random.seed(11)
flakes = ''.join(
    f'<i style="left:{random.uniform(-2,100):.2f}%;top:{random.uniform(-3,100):.2f}%;width:{s:.1f}px;height:{s:.1f}px;opacity:{random.uniform(.55,.95):.2f};filter:blur({b:.1f}px)"></i>'
    for s, b in [(lambda s: (s, max(0, (s - 6) * .18)))(random.choice([2, 2.5, 3, 3, 4, 4, 5, 6, 8, 11])) for _ in range(260)])
html = f"""<html><head><style>
@font-face{{font-family:Cap;src:url({u(F+'Caprasimo.ttf')})}}@font-face{{font-family:Bit;font-weight:700;src:url({u(F+'bitter-latin-700-normal.woff2')})}}
@font-face{{font-family:Bit;font-weight:600;src:url({u(F+'bitter-latin-600-normal.woff2')})}}
html,body{{margin:0;width:{W}px;height:{H}px;overflow:hidden}}
.bg{{position:absolute;inset:0;background:radial-gradient(130% 150% at 80% 35%,#eaf2f9 0%,#d3e2f0 45%,#bcd0e4 100%)}}
.snow{{position:absolute;inset:0}}.snow i{{position:absolute;border-radius:50%;background:radial-gradient(circle,#fff 0 45%,rgba(255,255,255,.85) 60%,rgba(255,255,255,0) 72%);box-shadow:0 0 2px rgba(60,90,130,.25)}}
.ph{{position:absolute;right:{int(W*.06)}px;top:{int(H*.06)}px;height:{int(H*.94)}px;filter:drop-shadow(0 18px 30px rgba(30,50,90,.28))}}
.l{{position:absolute;left:{int(W*.055)}px;top:{int(H*.11)}px;width:{int(W*.55)}px;color:#054689;font-family:Bit}}
.ic{{height:{int(H*.13)}px;display:block;margin-bottom:{int(H*.03)}px}}
.lk{{width:{int(W*.5)}px;display:block}}
ul{{list-style:none;padding:0;margin:{int(H*.06)}px 0 0;font-weight:700;font-size:{int(H*.046)}px;line-height:1.25}}
li{{display:flex;gap:12px;align-items:center;margin:0 0 {int(H*.022)}px}}li b{{display:inline-flex;align-items:center;justify-content:center;width:{int(H*.06)}px;height:{int(H*.06)}px;border-radius:50%;background:#b8263a;color:#fff;font-size:{int(H*.034)}px;flex:none}}
li span em{{font-style:normal;color:#1f6b45}}
.wm{{position:absolute;left:{int(W*.055)}px;bottom:{int(H*.08)}px;display:flex;align-items:flex-end;gap:2px}}
.wm img{{height:{int(H*.075)}px}}.wm span{{font-family:Cap;color:#1f6b45;font-size:{int(H*.062)}px;line-height:1;margin-bottom:{int(H*.008)}px}}
</style></head><body><div class="bg"></div><div class="snow">{flakes}</div>
<img class="ph" src="{u(phone)}">
<div class="l"><img class="ic" src="{u(R+'assets/brand/flame-heart-holiday.png')}"><img class="lk" src="{u(R+'assets/brand/fym-lockup/find-your-mat-ch-lockup.png')}">
<ul><li><b>1</b><span>Pick your <em>holiday</em> tiles</span></li><li><b>2</b><span>Swipe mats, set at your table</span></li><li><b>3</b><span>Add racks, make your match card</span></li></ul></div>
<div class="wm"><img src="{u(R+'assets/brand/mahjmatchmaker-wordmark-holiday-notag.png')}"><span>.com</span></div>
</body></html>"""
open('/tmp/fymcard.html', 'w').write(html)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox', '--allow-file-access-from-files'])
        pg = await b.new_page(viewport={'width': W, 'height': H}, device_scale_factor=2)
        await pg.goto('file:///tmp/fymcard.html'); await pg.wait_for_timeout(1500)
        await pg.screenshot(path='/tmp/fymcard2x.png'); await b.close()
asyncio.run(main())
Image.open('/tmp/fymcard2x.png').convert('RGB').resize((W, H), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.0, 50, 2)).save(out, quality=93)
print(out)
