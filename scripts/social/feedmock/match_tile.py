"""Grid post 'It's a match!' (1080x1350; the 3:4 grid crop keeps everything inside the center 1080x1440... safe zone y 120-1230)."""
import asyncio, importlib.util
R='/home/claude/mahjmatchmaker-data'; u=lambda p:f'file://{R}/{p}'
F=f'file://{R}/scripts/social/tileprofile/fonts'; G='file:///usr/share/fonts/truetype/google-fonts'
TILE='assets/tiles/album/papaya-spritz.jpg'; MAT='assets/colorcards/papaya-spritz/mats/heiress-britt-mills.jpg'
H='<svg viewBox="0 0 48 48" width="{w}" height="{w}"><path d="M24 40 C10 30 6 23 6 17 C6 11 11 7 16 7 C20 7 22 9 24 12 C26 9 28 7 32 7 C37 7 42 11 42 17 C42 23 38 30 24 40 Z" fill="{c}"/></svg>'
html=f"""<!doctype html><html><head><meta charset=utf8><style>
@font-face{{font-family:Hand;src:url('{F}/Caveat-Bold.ttf')}}
@font-face{{font-family:Lo;src:url('{G}/Lora-Variable.ttf')}}
@font-face{{font-family:Lo;font-style:italic;src:url('{G}/Lora-Italic-Variable.ttf')}}
@font-face{{font-family:Bit;font-weight:600;src:url('{F}/bitter-latin-600-normal.woff2')}}
*{{margin:0;padding:0;box-sizing:border-box}} body{{width:1080px;height:1350px;overflow:hidden}}
</style></head><body><div style="position:relative;width:1080px;height:1350px;background:#fdece4;display:flex;flex-direction:column;align-items:center;justify-content:center;overflow:hidden">
<div style="position:absolute;right:-200px;top:-220px;width:700px;height:700px;border-radius:50%;background:#fbd9c9"></div>
<div style="position:absolute;left:-220px;bottom:-240px;width:640px;height:640px;border-radius:50%;background:#fbe3ea"></div>
<div style="position:relative;font-family:Hand;font-size:140px;color:#d6336c;line-height:1">It&rsquo;s a match!</div>
<div style="position:relative;display:flex;align-items:center;margin-top:44px">
  <div style="width:360px;height:380px;border-radius:50%;background:url({u(TILE)}) center/cover;box-shadow:0 0 0 14px #fff,0 24px 50px rgba(200,80,40,.25)"></div>
  <div style="position:relative;z-index:2;margin:0 -40px;width:130px;height:130px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 10px 26px rgba(0,0,0,.15)">{H.format(w=84,c='#f56c8c')}</div>
  <div style="width:360px;height:360px;border-radius:40px;background:url({u(MAT)}) center/cover;box-shadow:0 0 0 14px #fff,0 24px 50px rgba(200,80,40,.25)"></div>
</div>
<div style="position:relative;font-family:Lo;font-weight:700;font-size:78px;color:#062a55;margin-top:64px;line-height:1.05;text-align:center">Papaya Spritz <span style="color:#e0702a">&hearts;</span> <i>Heiress</i></div>
<div style="position:relative;font:600 30px Bit;letter-spacing:.18em;text-transform:uppercase;color:#c8325f;margin-top:18px">Oh My Mahjong &middot; Britt Mills</div>
<div style="position:relative;margin-top:44px;background:#062a55;color:#fff;border-radius:999px;padding:20px 44px;font:600 36px Bit">All 50 of her matches are live</div>
<img src="{u('assets/brand/mahjmatchmaker-wordmark-notag.png')}" style="position:relative;width:300px;margin-top:34px">
</div></body></html>"""
open(R+'/scripts/social/feedmock/match_tile.html','w').write(html)
async def go():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1080,'height':1350})
        await pg.goto('file://'+R+'/scripts/social/feedmock/match_tile.html'); await pg.wait_for_timeout(1500)
        await pg.screenshot(path=R+'/assets/social/papaya-spritz-launch/grid/papaya-grid-1-its-a-match-heiress.jpg',type='jpeg',quality=93); await b.close()
asyncio.run(go())
