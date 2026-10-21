import asyncio
from playwright.async_api import async_playwright
OUT='/dev/shm/fymp/shots/'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=2)
        await pg.goto('http://localhost:8791/index.html'); await pg.wait_for_timeout(3500)
        await pg.add_style_tag(content='.undo{visibility:hidden!important}')
        await pg.screenshot(path=OUT+'s1-start.png', clip={'x':0,'y':0,'width':390,'height':440})
        await pg.fill('input', 'Papaya'); await pg.wait_for_timeout(600)
        await pg.click('button[data-tile]:has-text("Papaya Spritz")'); await pg.wait_for_timeout(2500)
        for i in range(3):
            await pg.click('button.no'); await pg.wait_for_timeout(900)
        await pg.wait_for_timeout(800)
        await pg.screenshot(path=OUT+'s2-swipe.png')
        await pg.click('button.yes'); await pg.wait_for_timeout(1500)
        await pg.click('button.big'); await pg.wait_for_timeout(2500)
        await pg.click('button.yes >> nth=-1'); await pg.wait_for_timeout(1200)
        await pg.click('button.go:has-text("Make it official")'); await pg.wait_for_timeout(5000)
        img=pg.locator('#s-card img[alt*="match card"]').first
        print(await img.count())
        src=await img.get_attribute('src')
        import base64
        if src and src.startswith('data:'):
            open(OUT+'s3-card.'+('png' if 'png' in src[:30] else 'jpg'),'wb').write(base64.b64decode(src.split(',',1)[1]))
        await img.screenshot(path=OUT+'s3-card-el.png')
        await b.close()
asyncio.run(main())
