import os,shutil,json
from playwright.sync_api import sync_playwright
O='/dev/shm/vault-tour/cap/flow/seq/'
shutil.rmtree(O,ignore_errors=True); os.makedirs(O)
n=[0]; log=[]
def shot(pg,tag):
    f=f'{O}{n[0]:03d}.jpg'; pg.screenshot(path=f,type='jpeg',quality=92); log.append((n[0],tag)); n[0]+=1
def burst(pg,tag,k=10,gap=60):
    for i in range(k): shot(pg,tag); pg.wait_for_timeout(gap)
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx=b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True)
    pg=ctx.new_page(); pg.goto('https://www.mahjmatchmaker.com/find-your-match',wait_until='networkidle',timeout=90000); pg.wait_for_timeout(2500)
    fr=[f for f in pg.frames if f.url=='about:srcdoc'][0]
    fr.get_by_text('No thanks').click(); pg.wait_for_timeout(400)
    fr.locator('[data-tcol="Holiday"]').first.click(); pg.wait_for_timeout(1000)
    fr.locator('button:has-text("Dear Santa")').first.click(); pg.wait_for_timeout(3000)
    fr.evaluate('window.scrollTo(0,200)'); pg.wait_for_timeout(1500)
    # hide the swipe hint bubble if any
    shot(pg,'deck')
    fr.locator('button.sb.yes').first.click(); burst(pg,'yes',14,40)
    pg.wait_for_timeout(1500); shot(pg,'deck2')
    y=fr.evaluate("(()=>{const e=[...document.querySelectorAll('[data-mock]')][0];return e.getBoundingClientRect().top+scrollY})()")
    fr.evaluate(f'window.scrollTo(0,{int(y)-520})'); pg.wait_for_timeout(1200); shot(pg,'suitors')
    fr.locator('[data-mock="shop.andersruff.com/candy-cane-lane-mahjong-mat"]').first.click(); pg.wait_for_timeout(2500)
    y=fr.evaluate("document.getElementById('s-racks').getBoundingClientRect().top+scrollY")
    fr.evaluate(f'window.scrollTo(0,{int(y)+100})'); pg.wait_for_timeout(1500); shot(pg,'racks')
    # zoom + on the mat preview in racks section
    plus=fr.locator('#s-racks button:has-text("+")')
    print('plus count',plus.count(), [plus.nth(i).evaluate('e=>JSON.stringify(e.dataset)+e.className') for i in range(plus.count())])
    for i in range(3):
        try: plus.first.click(); burst(pg,f'zoom{i}',4,80)
        except Exception as e: print('zoom err',e)
    pg.wait_for_timeout(800); shot(pg,'zoomed')
    fr.locator('[data-no="r"]').first.click(); burst(pg,'rno',12,40); pg.wait_for_timeout(1200); shot(pg,'rack2')
    fr.locator('[data-yes="r"]').first.click(); burst(pg,'ryes',12,40); pg.wait_for_timeout(1200); shot(pg,'rack3')
    fr.locator('[data-yes="r"]').first.click(); burst(pg,'ryes2',12,40); pg.wait_for_timeout(1200); shot(pg,'rack4')
    print(fr.evaluate("document.querySelector('#s-racks').innerText.slice(0,600)"))
    print(fr.evaluate("[...document.querySelectorAll('#s-racks button, #s-racks [data-rpick], #s-racks .suitor')].filter(b=>b.offsetParent).map(b=>b.tagName+(b.innerText||'').trim().replace(/\\n/g,' ').slice(0,25)+'|'+JSON.stringify(b.dataset)+'|'+b.className)"))
    for rp in ['bb:Matcha','bb:Flamingo']:
        fr.locator(f'[data-rp="{rp}"]').first.click(); pg.wait_for_timeout(1500); shot(pg,'pick '+rp)
    fr.locator('[data-make]').first.click(); pg.wait_for_timeout(3500)
    y=fr.evaluate("(()=>{const e=document.getElementById('s-card');return e.getBoundingClientRect().top+scrollY})()")
    fr.evaluate(f'window.scrollTo(0,{int(y)})'); pg.wait_for_timeout(2500); shot(pg,'card')
    H=fr.evaluate('document.documentElement.scrollHeight')
    for k in range(int(y)+700,min(H,int(y)+3000),700):
        fr.evaluate(f'window.scrollTo(0,{k})'); pg.wait_for_timeout(1500); shot(pg,'card+')
    print(fr.evaluate("document.querySelector('#s-card').innerText.slice(0,900)"))
    b.close()
json.dump(log,open(O+'log.json','w')); print(log[-12:])
