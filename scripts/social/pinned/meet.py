"""Pinned 'Meet your matchmaker' post, slide 1 (1080x1350), v2 (Tiffany Oct 20 1:30am): photoreal + editorial, her
chambray designer headshot, real product photos only, brand type (Caprasimo / Playfair italic / Bitter). No handwriting
font, no clip-art, no color chips."""
import asyncio
R='/home/claude/mahjmatchmaker-data'; u=lambda p:f'file://{R}/{p}'
F=f'file://{R}/scripts/social/tileprofile/fonts'
OUT=R+'/assets/social/pinned/meet-your-matchmaker-1.jpg'
html=f"""<!doctype html><html><head><meta charset=utf8><style>
@font-face{{font-family:Capra;src:url('{F}/Caprasimo.ttf')}}
@font-face{{font-family:PF;font-style:italic;src:url('{F}/playfair-display-latin-400-italic.woff2')}}
@font-face{{font-family:Bit;font-weight:600;src:url('{F}/bitter-latin-600-normal.woff2')}}
@font-face{{font-family:Bit;font-weight:400;src:url('{F}/bitter-latin-400-normal.woff2')}}
*{{margin:0;padding:0;box-sizing:border-box}} body{{width:1080px;height:1350px;overflow:hidden;background:#f6ece3}}
.print{{position:absolute;background:#fff;padding:14px;box-shadow:0 18px 40px rgba(60,40,25,.20),0 3px 8px rgba(60,40,25,.10)}}
</style></head><body><div style="position:relative;width:1080px;height:1350px">
<!-- soft mood-board backdrop: real mat photo, faded -->
<div style="position:absolute;right:-120px;top:-60px;width:760px;height:760px;background:url({u('assets/launches/omm-vivienne-mat/01.jpg')}) center/cover;opacity:.14;transform:rotate(8deg);border-radius:30px"></div>
<!-- portrait print -->
<div class="print" style="left:70px;top:150px;width:560px;height:700px;transform:rotate(-2.5deg)">
 <div style="width:100%;height:100%;background:url({u('assets/brand/headshot/tiffany-chambray-headshot-full.jpg')}) center 20%/cover"></div></div>
<!-- real tile pile, round -->
<div style="position:absolute;left:30px;top:720px;width:250px;height:250px;border-radius:50%;background:url({u('assets/tiles/album/papaya-spritz.jpg')}) center/cover;box-shadow:0 0 0 10px #fff,0 16px 34px rgba(60,40,25,.22)"></div>
<!-- text -->
<div style="position:absolute;left:665px;top:210px;right:50px">
 <div style="font:600 20px Bit;letter-spacing:.28em;text-transform:uppercase;color:#c8325f">Meet your matchmaker</div>
 <div style="font:400 84px/1.02 Capra;color:#054689;margin-top:18px">Hi, I&rsquo;m<br>Tiffany.</div>
 <div style="font:italic 400 32px/1.3 PF;color:#3c4f73;margin-top:26px">Designer, color lover and the eye behind every match.</div>
</div>
<div style="position:absolute;left:90px;right:90px;top:1000px;text-align:center">
 <div style="font:400 30px/1.5 Bit;color:#2c3e63">I pair mahjong tiles with the mats and racks<br>that make them look their best.</div>
</div>
<div style="position:absolute;left:0;right:0;bottom:90px;display:flex;justify-content:center;align-items:center;gap:26px">
 <img src="{u('assets/brand/mahjmatchmaker-wordmark-notag.png')}" style="width:300px">
 <span style="font:600 20px Bit;letter-spacing:.24em;text-transform:uppercase;color:#c8325f">swipe &rarr;</span>
</div>
</div></body></html>"""
hp=R+'/scripts/social/pinned/meet.html'; open(hp,'w').write(html)
async def go():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1080,'height':1350},device_scale_factor=2)
        await pg.goto('file://'+hp); await pg.wait_for_timeout(1500); await pg.screenshot(path='/tmp/meet2x.png'); await b.close()
    from PIL import Image
    Image.open('/tmp/meet2x.png').convert('RGB').resize((1080,1350),Image.LANCZOS).save(OUT,quality=93)
asyncio.run(go()); print(OUT)
