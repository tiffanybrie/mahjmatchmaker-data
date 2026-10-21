"""Capture the real Find Your Mat-ch app screens for the tutorial (launch email + FYM page), Oct 21.
Serves a local FYM build (v69 = scratchpad fym-oct21e), 390x844 @3x, undo hidden (X and heart only).
Flow: doors -> I have tiles -> Papaya Spritz -> swipe to Heiress (her #1 pick) -> picks on/off -> Pink colour dot ->
heart Heiress -> racks (her Beechwood pick on top) -> heart -> Make it official -> match card.
  PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python3 scripts/fym_promo/capture.py <build_dir> [/dev/shm/fymh]
Nothing leaves the browser (the build's TRK_URL is empty)."""
import asyncio, sys
sys.path.insert(0,'/home/claude/mahjmatchmaker-data/scripts/social/its_a_match')
import fym_shot
from playwright.async_api import async_playwright
O=(sys.argv[2] if len(sys.argv)>2 else '/dev/shm/fymh')+'/'
HIDE='button.undo{display:none!important}'
async def main():
    srv=fym_shot.serve(sys.argv[1]); url=f'http://127.0.0.1:{srv.server_address[1]}/index.html'
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=3)
        await pg.goto(url,wait_until='load'); await pg.wait_for_timeout(3000)
        await pg.add_style_tag(content=HIDE+' [data-door] *{text-wrap:balance}'); await pg.wait_for_timeout(600)
        await pg.screenshot(path=O+'doors.jpg',type='jpeg',quality=93)
        await pg.click('text=I have tiles'); await pg.wait_for_timeout(600)
        await pg.fill('#tsq','Papaya Spritz'); await pg.wait_for_timeout(600)
        await pg.locator("button:has-text('Papaya Spritz')").first.click(); await pg.wait_for_timeout(2000)
        for _ in range(10):
            t=(await pg.evaluate(fym_shot.TOP)).strip()
            if t.startswith('Heiress'): break
            await pg.click('button.no'); await pg.wait_for_timeout(650)
        await pg.wait_for_timeout(1200)
        await pg.screenshot(path=O+'picks-on.jpg',type='jpeg',quality=93)
        await pg.locator('button.chip.her').first.click(); await pg.wait_for_timeout(1800)
        await pg.screenshot(path=O+'picks-off.jpg',type='jpeg',quality=93)
        print('off chips:',await pg.evaluate("[...document.querySelectorAll('button.chip')].filter(e=>e.offsetParent).map(e=>e.className+'|'+e.textContent.trim())"), 'top', await pg.evaluate(fym_shot.TOP))
        # back on
        await pg.locator('button.chip.her').first.click(); await pg.wait_for_timeout(1500)
        print('back chips:',await pg.evaluate("[...document.querySelectorAll('button.chip')].filter(e=>e.offsetParent).map(e=>e.className+'|'+e.textContent.trim())"))
        # colour: first dot
        dots=await pg.evaluate("[...document.querySelectorAll('button.dot')].filter(e=>e.offsetParent).map(e=>(e.title||e.getAttribute('aria-label')||'')+'|'+e.className)")
        print('dots',dots)
        await pg.locator('button.dot').nth(1).click(); await pg.wait_for_timeout(1800)
        await pg.evaluate("(()=>{const d=[...document.querySelectorAll('button.dot')].filter(e=>e.offsetParent)[3];let p=d.parentElement;while(p&&p.scrollWidth<=p.clientWidth)p=p.parentElement;if(p)p.scrollLeft=p.scrollWidth})()"); await pg.wait_for_timeout(600)
        await pg.screenshot(path=O+'color.jpg',type='jpeg',quality=93)
        print('color top',await pg.evaluate(fym_shot.TOP))
        await pg.locator('button.dot').nth(1).click(); await pg.wait_for_timeout(1500)
        for _ in range(30):
            t=(await pg.evaluate(fym_shot.TOP)).strip()
            if t.startswith('Heiress'): break
            await pg.click('button.no'); await pg.wait_for_timeout(650)
        print('top before yes',t)
        await pg.click('button.yes'); await pg.wait_for_timeout(1500)
        await pg.screenshot(path=O+'after-yes.jpg',type='jpeg',quality=93)
        print(await pg.evaluate("[...document.querySelectorAll('button')].filter(e=>e.offsetParent).map(e=>e.className+'|'+e.textContent.trim().slice(0,30))"))
        await pg.click('button.big'); await pg.wait_for_timeout(2500)
        await pg.evaluate("""(()=>{const e=[...document.querySelectorAll('h1,h2,h3,p,div')].filter(x=>x.children.length<3&&/wingman/i.test(x.textContent)&&x.offsetParent).pop();let h=e;for(let i=0;i<3&&h.parentElement;i++){if(/Rack/.test(h.parentElement.textContent.slice(0,200)))h=h.parentElement}const y=h.getBoundingClientRect().top+scrollY-90;scrollTo(0,y)})()"""); await pg.wait_for_timeout(800)
        await pg.screenshot(path=O+'racks.jpg',type='jpeg',quality=93)
        print(await pg.evaluate("[...document.querySelectorAll('button')].filter(e=>e.offsetParent).map(e=>e.className+'|'+e.textContent.trim().slice(0,30))"))
        await pg.click('button.yes >> nth=-1'); await pg.wait_for_timeout(1500)
        await pg.screenshot(path=O+'racks2.jpg',type='jpeg',quality=93)
        await pg.click('button.go:has-text("Make it official")'); await pg.wait_for_timeout(5000)
        await pg.screenshot(path=O+'card.jpg',type='jpeg',quality=93)
        await b.close()
    srv.shutdown()
asyncio.run(main())
