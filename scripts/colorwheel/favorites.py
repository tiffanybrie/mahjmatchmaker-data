"""'Her best features' favorite-tiles graphic (1080x1350)."""
import asyncio
R='/home/claude/mahjmatchmaker-data'; u=lambda p:f'file://{R}/{p}'
F=f'file://{R}/scripts/social/tileprofile/fonts'; G='file:///usr/share/fonts/truetype/google-fonts'
T='assets/tiles/faces/papaya-spritz/'
favs=[('dragon-green','Dancing dragons','my favorite dragons'),('crane','The crane','her 1 Bam'),('lola-ginger','Ginger Lola','the redheaded joker'),('dot-3','Parasol dots','little umbrellas')]
cards=''.join(f'''<div style="display:flex;flex-direction:column;align-items:center;width:440px">
<div style="background:#fff;border-radius:26px;padding:22px;box-shadow:0 16px 36px rgba(200,80,40,.18);transform:rotate({r}deg)"><img src="{u(T+k+'.png')}" style="width:230px;height:316px;object-fit:cover;border-radius:14px;image-rendering:auto"></div>
<div style="font-family:Hand;font-size:58px;color:#062a55;margin-top:22px;line-height:1">{n}</div>
<div style="font:600 24px Bit;letter-spacing:.14em;text-transform:uppercase;color:#c8325f;margin-top:6px">{s}</div></div>''' for (k,n,s),r in zip(favs,[-3,2,-2,3]))
html=f"""<!doctype html><html><head><meta charset=utf8><style>
@font-face{{font-family:Hand;src:url('{F}/Caveat-Bold.ttf')}} @font-face{{font-family:Capra;src:url('{F}/Caprasimo.ttf')}}
@font-face{{font-family:Bit;font-weight:600;src:url('{F}/bitter-latin-600-normal.woff2')}}
*{{margin:0;padding:0;box-sizing:border-box}} body{{width:1080px;height:1350px;overflow:hidden}}</style></head><body>
<div style="position:relative;width:1080px;height:1350px;background:#fdece4;overflow:hidden;display:flex;flex-direction:column;align-items:center;padding-top:56px">
<div style="position:absolute;right:-200px;top:-220px;width:700px;height:700px;border-radius:50%;background:#fbd9c9"></div>
<div style="position:absolute;left:-220px;bottom:-240px;width:640px;height:640px;border-radius:50%;background:#fbe3ea"></div>
<div style="position:relative;font:600 28px Bit;letter-spacing:.2em;text-transform:uppercase;color:#c8325f">Papaya Spritz</div>
<div style="position:relative;font-family:Capra;font-size:96px;color:#062a55;margin-top:6px">Her best features</div>
<div style="position:relative;display:flex;flex-wrap:wrap;justify-content:center;gap:14px 20px;margin-top:30px">{cards}</div>
<img src="{u('assets/brand/mahjmatchmaker-wordmark-notag.png')}" style="position:absolute;bottom:34px;width:240px">
</div></body></html>"""
open(R+'/scripts/colorwheel/favorites.html','w').write(html)
async def go():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1080,'height':1350})
        await pg.goto('file://'+R+'/scripts/colorwheel/favorites.html'); await pg.wait_for_timeout(1500)
        await pg.screenshot(path=R+'/assets/social/papaya-spritz-launch/papaya-favorite-tiles.jpg',type='jpeg',quality=93); await b.close()
asyncio.run(go())
