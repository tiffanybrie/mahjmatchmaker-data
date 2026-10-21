from playwright.sync_api import sync_playwright
import base64,sys
H='/tmp/claude-0/-home-claude-mahjmatchmaker-data/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/match-builder-prototype.html'
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':400,'height':900});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('file://'+H);pg.wait_for_timeout(2500)
    pg.screenshot(path='m_full.png',full_page=True)
    for i in (0,3):
        pg.evaluate(f"(()=>{{try{{st.s={i};render()}}catch(e){{}}}})()")
        pg.evaluate("saveLook()");pg.wait_for_selector('.sheet img',timeout=15000)
        src=pg.eval_on_selector('.sheet img','e=>e.src');open(f'save{i}.jpg','wb').write(base64.b64decode(src.split(',')[1]))
        pg.evaluate("document.querySelector('.sheet').remove()")
    print(errs);b.close()
