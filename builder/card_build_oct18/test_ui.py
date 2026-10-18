import asyncio,subprocess,time
from playwright.async_api import async_playwright
SERVE='/home/claude/mahjmatchmaker-data/builder/card_redesign_oct18/serve';OUT='/home/claude/mahjmatchmaker-data/builder/card_build_oct18/out'
async def main():
    srv=subprocess.Popen(['python3','-m','http.server','8769'],cwd=SERVE,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1);errs=[]
    try:
        async with async_playwright() as p:
            b=await p.chromium.launch()
            for w,h in [(390,844),(1280,900)]:
                pg=await b.new_page(viewport={'width':w,'height':h},device_scale_factor=2 if w==390 else 1)
                pg.on('pageerror',lambda e:errs.append(str(e)))
                await pg.goto('http://localhost:8769/index.html',wait_until='domcontentloaded',timeout=90000)
                await pg.wait_for_function('typeof D!=="undefined"&&typeof renderAll==="function"',timeout=90000)
                await pg.add_style_tag(content='@font-face{font-family:Caprasimo;src:url(Caprasimo.ttf)}')
                await pg.evaluate('''async()=>{const si=D.sets.findIndex(x=>x.name==='Papaya Spritz');S.set=si;S.fav='brittmillsdesign.com/regency-scalloped-neoprene-mahjong-mat';const hr=herRacks();S.rpick=(hr.length?hr:rackPool()).slice(0,2);S.made=true;S.view='stack';renderAll();jump('s-card');}''')
                await pg.wait_for_timeout(6000)
                el=await pg.query_selector('#s-card');await el.scroll_into_view_if_needed()
                await pg.screenshot(path=f'{OUT}/ui_{w}.png',full_page=False)
                sw=await pg.evaluate('document.documentElement.scrollWidth>document.documentElement.clientWidth');print(w,'sideways',sw,await pg.evaluate("[...document.querySelectorAll('[data-view]')].map(b=>b.textContent).join('|')"))
                await pg.close()
            await b.close()
    finally:srv.kill()
    print('errors',errs[:5])
asyncio.run(main())
