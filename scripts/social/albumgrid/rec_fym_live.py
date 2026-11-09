import os,json,time,base64
from playwright.sync_api import sync_playwright
OUT='rec'; FR=[]; marks=[]
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':390,'height':844},device_scale_factor=2)
    pg=ctx.new_page(); pg.goto('https://www.mahjmatchmaker.com/find-your-match',timeout=60000); pg.wait_for_timeout(9000)
    f=pg.frames[1]
    f.evaluate("()=>{const s=document.createElement('style');s.textContent='.swh{display:none!important}';document.head.appendChild(s)}")
    cdp=ctx.new_cdp_session(pg)
    def onf(e):
        n=len(FR); open(f'{OUT}/f/{n:05d}.jpg','wb').write(base64.b64decode(e['data'])); FR.append(e['metadata']['timestamp'])
        try: cdp.send('Page.screencastFrameAck',{'sessionId':e['sessionId']})
        except Exception: pass
    cdp.on('Page.screencastFrame',onf)
    cdp.send('Page.startScreencast',{'format':'jpeg','quality':90,'maxWidth':780,'maxHeight':1688,'everyNthFrame':1})
    t0=time.time(); M=lambda n: marks.append((n,round(time.time()-t0,2)))
    pg.wait_for_timeout(900); M('home')
    f.locator('input[placeholder*=Search]').first.click(); f.locator('input[placeholder*=Search]').first.type('Dear Santa',delay=110); pg.wait_for_timeout(900)
    btns=f.evaluate("()=>[...document.querySelectorAll('button')].filter(b=>b.offsetParent&&b.innerText.includes('Dear Santa')).map(b=>b.innerText.slice(0,40))"); print('btns',btns)
    f.evaluate("()=>[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.includes('Dear Santa')).click()"); M('picked'); pg.wait_for_timeout(2500)
    f.evaluate("()=>{const d=document.querySelector('.deck.m');const y=d.getBoundingClientRect().top+scrollY-330;const s=scrollY,dd=y-s,t0=performance.now();function g(t){const k=Math.min(1,(t-t0)/800);window.scrollTo(0,s+dd*(k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2));if(k<1)requestAnimationFrame(g)}requestAnimationFrame(g)}"); pg.wait_for_timeout(1500); M('deck')
    for k in ['yes','no','yes','yes']:
        f.evaluate(f"()=>[...document.querySelectorAll('button.{k}')].filter(b=>b.offsetParent)[0].click()"); pg.wait_for_timeout(1400)
    M('swiped'); pg.wait_for_timeout(1500)
    cdp.send('Page.stopScreencast'); M('end')
    json.dump({'ts':FR,'marks':marks},open(f'{OUT}/meta.json','w'))
    b.close()
print(len(FR),marks)
