"""Find Your Mat-ch tutorial screens v2 (Tiffany 3:56pm: big screens + callout arrows). Full-page 390-wide shots at @3x
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
        pg = await b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=3)
        await pg.goto(url, wait_until='load'); await pg.wait_for_timeout(3000)
        await pg.add_style_tag(content='button.undo{display:none!important} [data-door] *{text-wrap:balance}'); await pg.wait_for_timeout(500)

        async def snap(name, sels):
            await pg.wait_for_timeout(1200)
            # full-page shots: un-stick sticky bars so they don't land mid-page
            await pg.evaluate("for(const e of document.querySelectorAll('body *')){if(getComputedStyle(e).position==='sticky')e.style.position='relative'}")
            await pg.wait_for_timeout(300)
            meta[name] = await pg.evaluate(RECT, sels)
            await pg.screenshot(path=OUT + name + '.png', full_page=True)

        await snap('doors', [['tiles', 'button', 'I have tiles'], ['mat', 'button', 'I have a mat']])
        await pg.click('text=I have tiles'); await pg.wait_for_timeout(600)
        await pg.fill('#tsq', 'Papaya Spritz'); await pg.wait_for_timeout(600)
        await pg.locator("button:has-text('Papaya Spritz')").first.click(); await pg.wait_for_timeout(2000)
        while not (await pg.evaluate(fym_shot.TOP)).strip().startswith('Heiress'):
            await pg.click('button.no'); await pg.wait_for_timeout(650)
        sw = [['picks', 'button.chip.her'], ['no', 'button.no'], ['yes', 'button.yes'], ['tiles', 'img', '', 0]]
        await snap('swipe', sw)
        await pg.click('button.yes'); await pg.wait_for_timeout(1200)   # Heiress -> shortlist
        await pg.click('button.yes'); await pg.wait_for_timeout(1200)   # Press for Mahjong -> shortlist
        await snap('shortlist', sw + [['tray', 'div.tray'], ['mock', 'div.tray button.go']])
        # back to Heiress for the mock-up
        await pg.locator('div.tray img').last.click(); await pg.wait_for_timeout(800)
        big = pg.locator('button.big')
        if await big.count():
            t = await big.first.text_content()
            if 'Heiress' not in t:
                print('mock target:', t)
        await pg.click('button.big'); await pg.wait_for_timeout(2500)
        await snap('racks', [['rackno', 'button.no', '', 1], ['rackyes', 'button.yes', '', 1], ['official', 'button.go', 'Make it official'],
                             ['rackcard', 'img[src*="r/"],img[alt*="ack"]', '', 0]])
        await pg.click('button.yes >> nth=-1'); await pg.wait_for_timeout(1200)
        await pg.click('button.go:has-text("Make it official")'); await pg.wait_for_timeout(5000)
        await snap('card', [['save', 'button', 'Save or share'], ['views', 'button', 'Mood board', -1]])
        await b.close()
    srv.shutdown()
    json.dump(meta, open(OUT + 'rects.json', 'w'), indent=1)
    print(json.dumps(meta)[:1500])

asyncio.run(main())
