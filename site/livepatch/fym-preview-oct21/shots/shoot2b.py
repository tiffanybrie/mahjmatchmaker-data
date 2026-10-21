import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':390,'height':724},device_scale_factor=2)
        await pg.goto('http://localhost:8791/index.html'); await pg.wait_for_timeout(3500)
        await pg.add_style_tag(content='.undo{visibility:hidden!important}')
        await pg.fill('input', 'Papaya'); await pg.wait_for_timeout(600)
        await pg.click('button[data-tile]:has-text("Papaya Spritz")'); await pg.wait_for_timeout(2500)
        for i in range(3):
            await pg.click('button.no'); await pg.wait_for_timeout(900)
        await pg.wait_for_timeout(800)
        r=await pg.evaluate("(()=>{const y=scrollY;const t=document.querySelector('.band, .deck');const no=document.querySelector('button.yes');const a=document.querySelector('.deck').getBoundingClientRect();const tb=[...document.querySelectorAll('img,div')].find(e=>e.innerText===undefined);return [document.querySelector('button.no').getBoundingClientRect().bottom+y, y]})()")
        print(r)
        await pg.screenshot(path='/dev/shm/fymp/shots/s2full.png', full_page=True)
        await b.close()
asyncio.run(main())
