import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
        await pg.goto('http://localhost:8791/index.html'); await pg.wait_for_timeout(3500); await pg.add_style_tag(content='[data-door] *{text-wrap:balance}')
        await pg.click('button[data-tcol]:has-text("Pink")'); await pg.wait_for_timeout(1500)
        r=await pg.evaluate("(()=>{const d=document.querySelector('[data-door]').parentElement.getBoundingClientRect();const t=[...document.querySelectorAll('button[data-tile]')].filter(e=>e.offsetParent);const tr=t[5].getBoundingClientRect();return [d.top,tr.bottom,t.slice(0,6).map(e=>e.textContent.trim())]})()")
        print(r)
        await pg.screenshot(path='/dev/shm/fymp/shots/s1-doors.png', clip={'x':0,'y':r[0]-14,'width':430,'height':r[1]-r[0]+28}, full_page=True)
        await b.close()
asyncio.run(main())
