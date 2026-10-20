"""Pinned Find Your Mat-ch banner: one 2160x1350 design split into two 1080x1350 grid posts (pins 2+3, next to Meet post).
Grid thumbnails are 3:4, so ~34px each side is cropped: keep content off the seam and outer edges."""
import asyncio
from PIL import Image
R='/home/claude/mahjmatchmaker-data'; u=lambda p:f'file://{R}/{p}'
F=f'file://{R}/scripts/social/tileprofile/fonts'
O=R+'/assets/social/pinned/'
card=lambda img,x,y,rot,w=470,z=1:f"""<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg);z-index:{z};background:#fff;border-radius:34px;padding:16px;box-shadow:0 22px 50px rgba(60,40,25,.22)">
<div style="width:100%;aspect-ratio:4/5;border-radius:22px;background:url({u(img)}) center/cover"></div></div>"""
html=f"""<!doctype html><html><head><meta charset=utf8><style>
@font-face{{font-family:Capra;src:url('{F}/Caprasimo.ttf')}}
@font-face{{font-family:PF;font-style:italic;src:url('{F}/playfair-display-latin-400-italic.woff2')}}
@font-face{{font-family:Bit;font-weight:600;src:url('{F}/bitter-latin-600-normal.woff2')}}
@font-face{{font-family:Bit;font-weight:400;src:url('{F}/bitter-latin-400-normal.woff2')}}
*{{margin:0;padding:0;box-sizing:border-box}} body{{width:2160px;height:1350px;overflow:hidden;background:#f6ece3}}
.btn{{position:absolute;width:150px;height:150px;border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 14px 30px rgba(60,40,25,.22);z-index:9}}
</style></head><body><div style="position:relative;width:2160px;height:1350px">
<div style="position:absolute;left:-200px;top:-260px;width:900px;height:900px;border-radius:50%;background:#f9d9c6;opacity:.8"></div>
<div style="position:absolute;right:-240px;bottom:-300px;width:1000px;height:1000px;border-radius:50%;background:#f6d3df;opacity:.8"></div>
<!-- LEFT: words -->
<div style="position:absolute;left:120px;top:250px;width:860px">
 <div style="font:600 26px Bit;letter-spacing:.3em;text-transform:uppercase;color:#c8325f">New on mahjmatchmaker.com</div>
 <div style="font:400 150px/.98 Capra;color:#054689;margin-top:26px">Find your<br>Mat-ch</div>
 <div style="font:italic 400 44px/1.3 PF;color:#3c4f73;margin-top:40px">Pick your tiles. Swipe through every mat.<br>Heart the ones you love.</div>
 <div style="display:inline-block;margin-top:56px;background:#054689;color:#fff;font:600 34px Bit;padding:22px 44px;border-radius:60px">Launching Tuesday, Oct 27</div>
 <div style="font:600 24px Bit;letter-spacing:.24em;text-transform:uppercase;color:#c8325f;margin-top:34px">Link in bio &rarr;</div>
</div>
<!-- RIGHT: swipe stack -->
{card('assets/colorcards/papaya-spritz/mats/greenly-mahj-and-vine.jpg',1290,230,-9,520,1)}
{card('assets/mats/gallery/anders-ruff--press-for-mahjong-mat.webp',1570,220,8,520,2)}
<div style="position:absolute;left:1370px;top:150px;width:600px;z-index:3;background:#fff;border-radius:34px;padding:18px 18px 30px;box-shadow:0 22px 50px rgba(60,40,25,.22)">
 <div style="position:relative;width:100%;aspect-ratio:1/1;border-radius:22px;background:url({u('assets/mats/gallery/britt-mills--heiress.webp')}) center/cover">
  <div style="position:absolute;right:-6px;bottom:-40px;width:220px;height:220px;border-radius:50%;background:url({u('assets/tiles/album/papaya-spritz.jpg')}) center/cover;box-shadow:0 0 0 10px #fff,0 12px 26px rgba(60,40,25,.25)"></div></div>
 <div style="font:600 18px Bit;letter-spacing:.24em;text-transform:uppercase;color:#c8325f;margin:34px 0 0 8px">Britt Mills</div>
 <div style="font:400 58px/1.05 Capra;color:#054689;margin:8px 0 0 8px">Heiress</div>
 <div style="font:italic 400 28px PF;color:#3c4f73;margin:8px 0 0 8px">for your Papaya Spritz tiles</div></div>
<div class="btn" style="left:1480px;top:1110px;background:#fff"><svg width="60" height="60" viewBox="0 0 24 24"><path d="M5 5L19 19M19 5L5 19" stroke="#054689" stroke-width="3.2" stroke-linecap="round"/></svg></div>
<div class="btn" style="left:1730px;top:1110px;background:#f2708f"><svg width="70" height="70" viewBox="0 0 24 24"><path d="M12 21s-7.5-4.6-9.6-9.2C.9 8.4 3.2 4.5 7 4.5c2.1 0 3.6 1.2 5 3 1.4-1.8 2.9-3 5-3 3.8 0 6.1 3.9 4.6 7.3C19.5 16.4 12 21 12 21z" fill="#fff"/></svg></div>
<img src="{u('assets/brand/mahjmatchmaker-wordmark-notag.png')}" style="position:absolute;left:120px;bottom:110px;width:330px">
</div></body></html>"""
hp=R+'/scripts/social/pinned/fym_split.html'; open(hp,'w').write(html)
async def go():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':2160,'height':1350},device_scale_factor=2)
        await pg.goto('file://'+hp); await pg.wait_for_timeout(2000); await pg.screenshot(path='/tmp/fym2x.png'); await b.close()
    im=Image.open('/tmp/fym2x.png').convert('RGB').resize((2160,1350),Image.LANCZOS)
    im.save(O+'find-your-match-banner-full.jpg',quality=92)
    im.crop((0,0,1080,1350)).save(O+'find-your-match-2-left.jpg',quality=93)
    im.crop((1080,0,2160,1350)).save(O+'find-your-match-3-right.jpg',quality=93)
asyncio.run(go())
