import sys
from playwright.sync_api import sync_playwright
st,mat,brand,out=sys.argv[1:5]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=3)
    pg.goto('http://localhost:8766/index.html?tour=off'); pg.wait_for_timeout(4000)
    try: pg.get_by_text('Skip tour').click(timeout=2000)
    except Exception: pass
    pg.locator('input').first.fill(st); pg.wait_for_timeout(700)
    pg.evaluate("(n)=>{const el=[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim().startsWith(n)); el.scrollIntoView(); el.click()}", st); pg.wait_for_timeout(2500)
    r=pg.evaluate("([m,br])=>{const id=Object.keys(M).find(k=>M[k].n===m&&M[k].bn===br); S.f.m.brand=br; S.mfront=id; renderAll(); return id}",[mat,brand]); print(r)
    pg.wait_for_timeout(2500)
    pg.evaluate("()=>{const d=document.querySelector('.deck.m');d&&d.scrollIntoView({block:'center'})}"); pg.wait_for_timeout(1500)
    pg.screenshot(path=out); b.close()
