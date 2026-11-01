import sys,json,time,base64,os; sys.path.insert(0,'/tmp/claude-0/-home-claude/f4da3022-6ec8-595a-90aa-668aea191899/scratchpad')
from fymlib import *
OUT='/dev/shm/holiday-intro/rec2'; os.makedirs(OUT+'/f',exist_ok=True)
marks=[]; T0=[0]
def mark(n): marks.append((n,round(time.time()-T0[0],3))); print(n,marks[-1][1])
def smooth(pg,js_target,ms=700):
    pg.evaluate(f"""()=>{{const y=({js_target});const s=scrollY,d=y-s,t0=performance.now();function f(t){{const k=Math.min(1,(t-t0)/{ms});window.scrollTo(0,s+d*(k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2));if(k<1)requestAnimationFrame(f)}}requestAnimationFrame(f)}}"""); pg.wait_for_timeout(ms+150)
def front(pg,n):
    k=pg.evaluate("(n)=>Object.keys(M).find(k=>M[k].n===n&&!M[k].hid)",n); pg.evaluate("(k)=>{S.mfront=k;S.mfset=S.set;renderAll()}",k); pg.wait_for_timeout(1200)
with sync_playwright() as p:
    b,ctx,pg=start(p,2)
    pg.locator('input[placeholder*=Search]').first.click(); pg.keyboard.type('Dear Santa'); pg.wait_for_timeout(1300)
    pg.evaluate("()=>[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.includes('Dear Santa')).click()"); pg.wait_for_timeout(3500)
    pg.evaluate("()=>document.querySelector('.chip.holc').click()"); pg.wait_for_timeout(1200)
    front(pg,'Festive Plaid Premium'); pg.evaluate("()=>[...document.querySelectorAll('button.yes')].filter(b=>b.offsetParent)[0].click()"); pg.wait_for_timeout(1500)
    pg.evaluate("()=>[...document.querySelectorAll('button.yes')].filter(b=>b.offsetParent)[0].click()"); pg.wait_for_timeout(1500)
    print(pg.evaluate("()=>[...document.querySelectorAll('.pick1 button, .r3p button, .tray .th button')].filter(b=>b.offsetParent).map(b=>b.className+'|'+(b.innerText||b.querySelector('img')?.alt||'').trim().slice(0,40))"))
    # pick Festive Plaid suitor
    r=pg.evaluate("()=>{const bs=[...document.querySelectorAll('.pick1 button, .r3p button')].filter(b=>b.offsetParent);const f=bs.find(b=>/Festive/.test(b.innerText));(f||bs[0]).click();return !!f}"); print('picked festive',r); pg.wait_for_timeout(3000); fixlogo(pg)
    pg.evaluate("()=>{window._rq=['bb:Persimmon'];const pool=rackPool;window.rackPool=function(){const a=pool();return [...window._rq,...a.filter(x=>!window._rq.includes(x))]};try{rackPool=window.rackPool}catch(e){};renderRacks()}"); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{const d=document.querySelector('.deck.r');window.scrollTo(0,d.getBoundingClientRect().top+scrollY-520)}"); pg.wait_for_timeout(3000); fixlogo(pg)
    pg.screenshot(path='/dev/shm/holiday-intro/r0.png')
    print(pg.evaluate("()=>[...document.querySelectorAll('.tilev.mband .zb button, .tilev .zb button')].filter(b=>b.offsetParent).map(b=>b.innerText+'|'+JSON.stringify(b.getBoundingClientRect()))"))
    cdp=ctx.new_cdp_session(pg); FR=[]
    def onf(e):
        n=len(FR); open(f'{OUT}/f/{n:05d}.jpg','wb').write(base64.b64decode(e['data'])); FR.append(e['metadata']['timestamp'])
        try: cdp.send('Page.screencastFrameAck',{'sessionId':e['sessionId']})
        except Exception: pass
    cdp.on('Page.screencastFrame',onf)
    cdp.send('Page.startScreencast',{'format':'jpeg','quality':92,'maxWidth':780,'maxHeight':1688,'everyNthFrame':1})
    T0[0]=time.time(); pg.wait_for_timeout(1000); mark('racks')
    for i in range(3):
        pg.evaluate("()=>{const bs=[...document.querySelectorAll('.tilev.mband .zb button')].filter(b=>b.offsetParent);const plus=bs.find(b=>b.innerText.trim()==='+');plus&&plus.click()}"); mark(f'plus{i}'); pg.wait_for_timeout(700)
    pg.wait_for_timeout(600)
    for r,k in [('bb:Persimmon','yes'),('bb:Lilac','no'),('bb:Basil','yes')]:
        pg.evaluate("(r)=>{window._rq=[r];renderRacks()}",r); pg.wait_for_timeout(900); mark('show '+r)
        pg.evaluate(f"()=>[...document.querySelectorAll('button.{k}')].filter(b=>b.offsetParent).pop().click()"); mark(k+' '+r); pg.wait_for_timeout(1400)
    pg.evaluate("()=>{S.rpick=[S.rliked[0],S.rliked[1]];renderRacks()}"); pg.wait_for_timeout(900); mark('official')
    pg.evaluate("()=>[...document.querySelectorAll('button.go')].filter(b=>b.offsetParent).pop().click()"); pg.wait_for_timeout(2500)
    smooth(pg,"(()=>{const h=[...document.querySelectorAll('h2,h1,div')].find(e=>e.innerText&&e.innerText.trim().startsWith('Your match card')&&e.offsetParent);return h.getBoundingClientRect().top+scrollY-90})()",900)
    mark('card'); pg.wait_for_timeout(2500); mark('end')
    cdp.send('Page.stopScreencast'); pg.wait_for_timeout(300)
    pg.evaluate("()=>[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim()==='Story 9:16').click()"); pg.wait_for_timeout(5000)
    src=pg.evaluate("()=>{const i=[...document.querySelectorAll('img')].filter(e=>e.offsetParent&&e.naturalHeight>=3000)[0];return i?i.src:''}")
    if src.startswith('data:'): open(OUT+'/storycard.png','wb').write(base64.b64decode(src.split(',',1)[1])); print('storycard ok')
    else: print('no storycard',src[:60])
    json.dump({'frames':FR,'marks':marks},open(OUT+'/marks.json','w'),indent=1); print(len(FR),'frames')
    b.close()
