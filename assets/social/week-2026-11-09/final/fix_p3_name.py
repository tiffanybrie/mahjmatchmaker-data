"""p3 tap-a-color slide 3: the mat name was cut to 'Press for'; the Anders Ruff mat is 'Press for Mahjong'.
Repaints only the italic sub line (same font/size/colour as fym-bank-oct31/build.py) into copies under final/sat-color/."""
import asyncio, shutil, os
from PIL import Image
R='/home/claude/mahjmatchmaker-data'; SRC=R+'/assets/social/fym-bank-oct31/p3-color-filter'; OUT=R+'/assets/social/week-2026-11-09/final/sat-color'
F='file://'+R+'/scripts/social/tileprofile/fonts/'
os.makedirs(OUT,exist_ok=True)
for f in os.listdir(SRC): shutil.copy(f'{SRC}/{f}',OUT)
JOBS={'feed-03':(251,287,38),'story-03':(374,415,44)}
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for n,(y0,y1,s) in JOBS.items():
            im=Image.open(f'{OUT}/{n}.jpg').convert('RGB'); bg='#%02x%02x%02x'%im.getpixel((40,(y0+y1)//2))
            h=y1-y0+30; top=y0-12
            pg=await b.new_page(viewport={'width':1080,'height':h})
            await pg.set_content(f"""<style>@font-face{{font-family:PF;font-style:italic;src:url({F}playfair-display-latin-600-italic.woff2)}}*{{margin:0}}
body{{background:{bg};width:1080px;height:{h}px}}</style><div style="position:absolute;left:0;right:0;top:0;height:{h}px;display:flex;align-items:center;justify-content:center;font:600 {s}px/1.25 PF;font-style:italic;color:#e0547f">Press for Mahjong by Anders Ruff</div>""")
            await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
            await pg.screenshot(path='/tmp/strip.png'); await pg.close()
            st=Image.open('/tmp/strip.png').convert('RGB'); im.paste(st,(0,top)); im.save(f'{OUT}/{n}.jpg',quality=92)
        await b.close()
asyncio.run(main())
