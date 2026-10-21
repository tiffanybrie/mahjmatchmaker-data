"""Render the launch-day hero preview: live homepage with the hero copy/link swapped and the announcement bar hidden.
Usage: PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python3 preview.py <out_dir> [before|after]"""
import sys,asyncio,pathlib
from playwright.async_api import async_playwright
HERE=pathlib.Path(__file__).parent
AFTER=(HERE/'after-text-block.html').read_text().strip()
JS='''(html)=>{const t=document.querySelector('#block-b79726a6f150a9dd219f .sqs-html-content');t.innerHTML=html;
const a=document.querySelector('#block-yui_3_17_2_1_1773260945246_2648 a');a.textContent='Start swiping';a.setAttribute('href','/find-your-match');
const bar=document.querySelector('.sqs-announcement-bar-dropzone');if(bar)bar.style.display='none';
const h1=t.querySelector('h1');return {h1lines:Math.round(h1.getBoundingClientRect().height/parseFloat(getComputedStyle(h1).lineHeight)),sw:document.documentElement.scrollWidth}}'''
async def main():
    out=pathlib.Path(sys.argv[1]); mode=sys.argv[2] if len(sys.argv)>2 else 'after'
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for w,h in [(390,844),(1280,800)]:
            pg=await b.new_page(viewport={'width':w,'height':h})
            await pg.goto('https://www.mahjmatchmaker.com/?preview=launch',wait_until='networkidle',timeout=60000)
            await pg.wait_for_timeout(1500)
            if mode=='after': print(w,await pg.evaluate(JS,AFTER))
            await pg.screenshot(path=str(out/f'hero-{mode}-{w}.png'))
            await pg.close()
        await b.close()
asyncio.run(main())
