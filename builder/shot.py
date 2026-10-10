import asyncio
from playwright.async_api import async_playwright
P='/tmp/claude-0/-home-claude-mahjmatchmaker-data/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/match-builder-prototype.html'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for name,w in (('d',1000),('m',400)):
            pg=await b.new_page(viewport={'width':w,'height':900})
            errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
            await pg.goto('file://'+P);await pg.wait_for_timeout(800)
            await pg.screenshot(path=f'/tmp/mb/{name}_board.png')
            # find a set where table enabled
            n=await pg.evaluate('D.sets.length')
            for i in range(n):
                await pg.evaluate(f'choose({i})')
                dis=await pg.evaluate("document.getElementById('vTable').disabled")
                if not dis:
                    await pg.click('#vTable');await pg.wait_for_timeout(300)
                    await pg.screenshot(path=f'/tmp/mb/{name}_table.png',full_page=True);print(name,'table ok on set',i);break
            print(name,'errors',errs, 'scrollW',await pg.evaluate('document.documentElement.scrollWidth'))
        await b.close()
asyncio.run(main())
