"""Preview the live homepage with the hero background swapped (Papaya Spritz on Vivienne, Oct 21).
Routes the current Squarespace hero image to the local file, sets the focal point, screenshots the hero section.
Usage: PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python3 preview.py <image> <out_dir> [fx,fy]"""
import sys, asyncio, pathlib
from playwright.async_api import async_playwright
IMG = pathlib.Path(sys.argv[1]).read_bytes()
OUT = pathlib.Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
FP = sys.argv[3] if len(sys.argv) > 3 else '0.5,0.5'
SEC = 'section[data-section-id="69b1d01489d0f8016ee3d59f"]'
JS = '''([sec, fp]) => {const s=document.querySelector(sec); const img=s.querySelector('.section-background img');
 const [x,y]=fp.split(',').map(Number); if(img){img.setAttribute('data-image-focal-point',fp); img.style.objectPosition=(x*100)+'% '+(y*100)+'%';}
 const r=s.getBoundingClientRect(); const out={sec:[Math.round(r.width),Math.round(r.height)], sw:document.documentElement.scrollWidth, src:img&&img.currentSrc.slice(-60), lines:[]};
 s.querySelectorAll('h1,h2,h3,h4,p,a').forEach(e=>{const t=e.innerText.trim(); if(!t) return; const lh=parseFloat(getComputedStyle(e).lineHeight)||1;
   out.lines.push([e.tagName, t.slice(0,60), Math.round(e.getBoundingClientRect().height/lh)]);}); return out;}'''
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w, h in [(390, 844), (1280, 800), (1440, 900), (1920, 1080)]:
            pg = await b.new_page(viewport={'width': w, 'height': h})
            async def handle(route):
                await route.fulfill(body=IMG, content_type='image/jpeg')
            await pg.route('**/*loveshackfancy-coquette-mahjong-tiles-fleur-mat*', handle)
            await pg.goto('https://www.mahjmatchmaker.com/?preview=papaya', wait_until='networkidle', timeout=90000)
            await pg.wait_for_timeout(2500)
            print(w, await pg.evaluate(JS, [SEC, FP]))
            await pg.wait_for_timeout(800)
            await pg.screenshot(path=str(OUT / f'hero-papaya-{w}.png'))
            await pg.close()
        await b.close()
asyncio.run(main())
