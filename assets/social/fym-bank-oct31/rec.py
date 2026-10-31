"""Real screen recording of FYM v107 (Version 1.9.2): Tinselle (Emerald Green) -> holiday + green chips -> X Polo Club, heart Evergreen & Tartan -> racks (heart Brick Red, X Dark Navy, heart Evergreen) -> match card.
Viewport 390x844 @2x, captured with the CDP screencast (780x1688 JPEG frames + timestamps) into /dev/shm/w/rec/f/, marks.json."""
import os,json,time
os.environ['TMPDIR']='/dev/shm/w'
from playwright.sync_api import sync_playwright
OUT='/dev/shm/w/rec'; os.makedirs(OUT,exist_ok=True)
marks=[]; T0=[0]
def mark(n): marks.append((n,round(time.time()-T0[0],2))); print(n,marks[-1][1])
def smooth(pg,js_target,ms=700):
    pg.evaluate(f"""()=>{{const y=({js_target});const s=scrollY,d=y-s,t0=performance.now();function f(t){{const k=Math.min(1,(t-t0)/{ms});window.scrollTo(0,s+d*(k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2));if(k<1)requestAnimationFrame(f)}}requestAnimationFrame(f)}}"""); pg.wait_for_timeout(ms+150)
DECK="(()=>{const d=document.querySelector('.deck.m');return d.getBoundingClientRect().top+scrollY-330})()"
FILT="(()=>{const d=document.querySelector('button.holc');return d.getBoundingClientRect().top+scrollY-300})()"
RDECK="(()=>{const d=document.querySelector('.deck.r');return d.getBoundingClientRect().top+scrollY-420})()"
def tap(pg,js,wait=1100): pg.evaluate(js); pg.wait_for_timeout(wait)
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx=b.new_context(viewport={'width':390,'height':844},device_scale_factor=2)
    pg=ctx.new_page()
    pg.goto('http://localhost:8777/index.html?tour=off'); pg.wait_for_timeout(5000)
    pg.add_style_tag(content='.swh{display:none!important}'); pg.wait_for_timeout(500)
    import base64; os.makedirs(OUT+'/f',exist_ok=True); FR=[]
    cdp=ctx.new_cdp_session(pg)
    def onf(e):
        n=len(FR); open(f'{OUT}/f/{n:05d}.jpg','wb').write(base64.b64decode(e['data'])); FR.append(e['metadata']['timestamp'])
        try: cdp.send('Page.screencastFrameAck',{'sessionId':e['sessionId']})
        except Exception: pass
    cdp.on('Page.screencastFrame',onf)
    cdp.send('Page.startScreencast',{'format':'jpeg','quality':90,'maxWidth':780,'maxHeight':1688,'everyNthFrame':1})
    T0[0]=time.time(); pg.wait_for_timeout(300)
    mark('home')
    pg.wait_for_timeout(1200)
    pg.locator('input[placeholder*=Search]').first.click(); mark('type'); pg.keyboard.type('Tinselle',delay=110); pg.wait_for_timeout(900)
    tap(pg,"()=>[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim().startsWith('Tinselle (Emerald')).click()",2600)
    smooth(pg,DECK); mark('deck'); pg.wait_for_timeout(1200)
    smooth(pg,FILT); mark('chips'); pg.wait_for_timeout(500)
    tap(pg,"()=>document.querySelector('.chip.holc').click()",900)
    tap(pg,"()=>[...document.querySelectorAll('button.dot')].find(b=>b.title==='Green'&&b.offsetParent).click()",1000)
    smooth(pg,DECK); mark('swipe'); pg.wait_for_timeout(700)
    tap(pg,"()=>[...document.querySelectorAll('button.no')].filter(b=>b.offsetParent)[0].click()",1500); mark('heart')
    tap(pg,"()=>[...document.querySelectorAll('button.yes')].filter(b=>b.offsetParent)[0].click()",1500)
    mark('suitors')
    tap(pg,"()=>{const b=[...document.querySelectorAll('.pick1 button, .r3p button')].filter(b=>b.offsetParent)[0];b&&b.click()}",2200)
    pg.evaluate("()=>{window._rq=['bb:Brick Red'];const pool=rackPool;window.rackPool=function(){const a=pool();return [...window._rq,...a.filter(x=>!window._rq.includes(x))]};try{rackPool=window.rackPool}catch(e){};renderRacks()}"); pg.wait_for_timeout(1200)
    smooth(pg,RDECK); mark('racks'); pg.wait_for_timeout(600)
    for r,k in [('bb:Brick Red','yes'),('bb:Dark Navy','no'),('bb:Evergreen','yes')]:
        pg.evaluate("(r)=>{window._rq=[r];renderRacks()}",r); pg.wait_for_timeout(700)
        tap(pg,f"()=>[...document.querySelectorAll('button.{k}')].filter(b=>b.offsetParent).pop().click()",1300)
    pg.evaluate("()=>{S.rpick=[S.rliked[0],S.rliked[1]];renderRacks()}"); pg.wait_for_timeout(900)
    mark('official')
    tap(pg,"()=>[...document.querySelectorAll('button.go')].filter(b=>b.offsetParent).pop().click()",2500)
    smooth(pg,"(()=>{const h=[...document.querySelectorAll('h2,h1,div')].find(e=>e.innerText&&e.innerText.trim().startsWith('Your match card')&&e.offsetParent);return h.getBoundingClientRect().top+scrollY-90})()",900)
    mark('card'); pg.wait_for_timeout(1500)
    smooth(pg,"scrollY+260",800); pg.wait_for_timeout(2200); mark('end')
    cdp.send('Page.stopScreencast'); pg.wait_for_timeout(300); ctx.close(); b.close()
json.dump({'frames':FR,'marks':marks},open(OUT+'/marks.json','w'),indent=1); print(len(FR),'frames')
