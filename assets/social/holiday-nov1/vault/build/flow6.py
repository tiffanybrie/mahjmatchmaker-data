import os,shutil,json
from playwright.sync_api import sync_playwright
O='/dev/shm/vault-tour/cap/flow/seq3/'
shutil.rmtree(O,ignore_errors=True); os.makedirs(O)
n=[0]; log=[]
def shot(pg,tag):
    pg.screenshot(path=f'{O}{n[0]:03d}.jpg',type='jpeg',quality=92); log.append((n[0],tag)); n[0]+=1
def burst(pg,tag,k=10,gap=40):
    for i in range(k): shot(pg,tag); pg.wait_for_timeout(gap)
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx=b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True)
    pg=ctx.new_page(); pg.goto('https://www.mahjmatchmaker.com/find-your-match',wait_until='networkidle',timeout=90000); pg.wait_for_timeout(2500)
    fr=[f for f in pg.frames if f.url=='about:srcdoc'][0]
    fr.get_by_text('No thanks').click(); pg.wait_for_timeout(400)
    fr.locator('[data-tcol="Holiday"]').first.click(); pg.wait_for_timeout(1000)
    fr.locator('button:has-text("Dear Santa")').first.click(); pg.wait_for_timeout(3000)
    fr.locator('button.sb.yes').first.click(); pg.wait_for_timeout(2000)
    fr.locator('[data-mock="shop.andersruff.com/candy-cane-lane-mahjong-mat"]').first.click(); pg.wait_for_timeout(2500)
    y=fr.evaluate("document.getElementById('s-racks').getBoundingClientRect().top+scrollY")
    fr.evaluate(f'window.scrollTo(0,{int(y)+95})'); pg.wait_for_timeout(1500); shot(pg,'racks')
    for i in range(3):
        fr.locator('#s-racks [data-tz="1"]').first.click(); burst(pg,f'zoom{i}',5,60)
    pg.wait_for_timeout(800); fr.evaluate(f'window.scrollTo(0,{int(y)+95})'); pg.wait_for_timeout(800); shot(pg,'zoomed')
    fr.locator('#s-racks [data-no="r"]').first.click(); burst(pg,'rno',12,30); pg.wait_for_timeout(1200); shot(pg,'rack2')
    fr.locator('#s-racks [data-yes="r"]').first.click(); burst(pg,'ryes',12,30); pg.wait_for_timeout(1200); shot(pg,'rack3')
    fr.locator('#s-racks [data-yes="r"]').first.click(); burst(pg,'ryes2',12,30); pg.wait_for_timeout(1200); shot(pg,'rack4')
    b.close()
json.dump(log,open(O+'log.json','w')); print(log)
