"""Find Your Mat-ch tutorial screens v2 (Tiffany 3:56pm: big screens + callout arrows). v72 flow (Oct 21 night): doors, buttons (heart / X / Back / picks / colors + Holiday), shortlist, Pick 2 racks, card. Full-page 390-wide shots at @3x
plus element rects (page CSS px) so render2.py can crop each step and point arrows at the real UI.
  PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python3 scripts/fym_promo/capture2.py <fym build dir> [/dev/shm/fymh/v2]
Taps hearts only inside this local headless copy (TRK_URL empty, nothing leaves the browser). Undo hidden."""
import asyncio, sys, json, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'social', 'its_a_match'))
import fym_shot
from playwright.async_api import async_playwright

OUT = (sys.argv[2] if len(sys.argv) > 2 else '/dev/shm/fymh/v2') + '/'
RECT = """(sels)=>{const o={};for(const [k,s,txt,nth] of sels){let els=[...document.querySelectorAll(s)].filter(e=>e.offsetParent&&(!txt||e.textContent.includes(txt)));
const e=els[nth||0];if(e){const r=e.getBoundingClientRect();o[k]=[r.left,r.top+scrollY,r.width,r.height]}}
const d=[...document.querySelectorAll('button.dot')].filter(e=>e.offsetParent).slice(0,7);if(d.length){const a=d[0].getBoundingClientRect(),b=d[d.length-1].getBoundingClientRect();o.dots=[a.left,a.top+scrollY,Math.min(390,b.right)-a.left,a.height]}
o.H=document.documentElement.scrollHeight;return o}"""


async def main():
    os.makedirs(OUT, exist_ok=True)
    srv = fym_shot.serve(sys.argv[1]); url = f'http://127.0.0.1:{srv.server_address[1]}/index.html'
    meta = {}
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=3)
        # v72: no first-run tour prompt and no one-time hint bounces in the screenshots
        await ctx.add_init_script("""try{localStorage.setItem('fym_tour','skipped');localStorage.setItem('fym_hints','{"back":1,"picks":1,"colors":1,"mock":1}')}catch(e){}""")
        pg = await ctx.new_page()
        await pg.goto(url, wait_until='load'); await pg.wait_for_function('window.__imgsReady===true', timeout=60000); await pg.wait_for_timeout(1500)
        await pg.add_style_tag(content='button.undo{display:none!important} [data-door] *{text-wrap:balance} .bnc,.bnc1{animation:none!important}'); await pg.wait_for_timeout(500)

        async def snap(name, sels):
            await pg.wait_for_timeout(1200)
            # full-page shots: un-stick sticky bars so they don't land mid-page
            await pg.evaluate("for(const e of document.querySelectorAll('body *')){if(getComputedStyle(e).position==='sticky')e.style.position='relative'}")
            await pg.wait_for_timeout(300)
            meta[name] = await pg.evaluate(RECT, sels)
            await pg.screenshot(path=OUT + name + '.png', full_page=True)
            await pg.evaluate("for(const e of document.querySelectorAll('body *')){if(e.style.position==='relative')e.style.position=''}")

        await snap('doors', [['tiles', '[data-door="tiles"]'], ['mat', '[data-door="mat"]']])
        await pg.click('[data-door="tiles"]'); await pg.wait_for_timeout(600)
        await pg.fill('#tsq', 'Papaya Spritz'); await pg.wait_for_timeout(600)
        i = await pg.evaluate("D.sets.findIndex(s=>s.name==='Papaya Spritz')")
        await pg.click(f'[data-tile="{i}"]'); await pg.wait_for_timeout(2000)
        # real swipes: love Heiress + Press for, X Greenly + Goldie -> Haven on screen, Back is live, 2 suitors in the shortlist
        for k in ('yes', 'yes', 'no', 'no'):
            await pg.click(f'[data-{k}="m"]'); await pg.wait_for_timeout(900)
        print('swipe card:', await pg.evaluate("D.mats[queue('m')[0]].n"), 'liked', await pg.evaluate("S.liked.map(k=>D.mats[k].n)"))
        await snap('swipe', [['picks', '.frow button.chip.her'], ['hol', '.frow button.holc'], ['dot', '.frow button.dot[data-fam]:not([data-fam=""])'],
                             ['back', '[data-back="m"]'], ['no', '[data-no="m"]'], ['yes', '[data-yes="m"]'], ['top', '#top-m'],
                             ['tray', 'div.tray'], ['trayimg', 'div.tray img'], ['go', 'div.tray button.go']])
        await pg.click('div.tray button.go'); await pg.wait_for_timeout(1200)
        await pg.locator("button[data-mock*='heiress']").first.click(); await pg.wait_for_timeout(1200)
        big = pg.locator("button.big[data-mock*='heiress']")
        if await big.count() and await big.first.is_visible():
            await big.first.click(); await pg.wait_for_timeout(1500)
        # racks: love Beechwood (her pick), X Chartreuse + Lavender, love Coral -> 2 of 2
        for k in ('yes', 'no', 'no', 'yes'):
            await pg.click(f'[data-{k}="r"]'); await pg.wait_for_timeout(1000)
        print('racks:', await pg.evaluate("document.querySelectorAll('div.tray')[1].innerText.replace(/\\n/g,' | ')"))
        await snap('racks', [['rtray', 'div.tray', '', 1], ['rslot', 'div.tray button.rx', '', 0], ['official', 'button.go', 'Make it official'],
                             ['rno', '[data-no="r"]'], ['ryes', '[data-yes="r"]'], ['rtop', '#top-r']])
        await pg.click('button.go:has-text("Make it official")'); await pg.wait_for_timeout(5000)
        await snap('card', [['views', 'button', 'Love triangle'], ['mood', 'button', 'Mood board'], ['story', 'button', 'Story 9:16'], ['post', 'button', 'Post 4:5'],
                            ['pin', 'button', 'Pin 2:3'], ['save', 'button.big', 'Save'], ['shop', 'a.go', 'Shop'], ['dc', 'a.dc', 'Discount'],
                            ['cardimg', '#s-card img,#s-card canvas'], ['home', 'h2,h3,b', 'Take them home']])
        await b.close()
    srv.shutdown()
    json.dump(meta, open(OUT + 'rects.json', 'w'), indent=1)
    print(json.dumps(meta)[:2500])

asyncio.run(main())
