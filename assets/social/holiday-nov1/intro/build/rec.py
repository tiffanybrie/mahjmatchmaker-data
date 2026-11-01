import sys,json,time,base64,os; sys.path.insert(0,'/tmp/claude-0/-home-claude/f4da3022-6ec8-595a-90aa-668aea191899/scratchpad')
from fymlib import *
OUT='/dev/shm/holiday-intro/rec'; os.makedirs(OUT+'/f',exist_ok=True)
marks=[]; T0=[0]
def mark(n): marks.append((n,round(time.time()-T0[0],3))); print(n,marks[-1][1])
def smooth(pg,js_target,ms=700):
    pg.evaluate(f"""()=>{{const y=({js_target});const s=scrollY,d=y-s,t0=performance.now();function f(t){{const k=Math.min(1,(t-t0)/{ms});window.scrollTo(0,s+d*(k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2));if(k<1)requestAnimationFrame(f)}}requestAnimationFrame(f)}}"""); pg.wait_for_timeout(ms+150)
DECK="(()=>{const d=document.querySelector('.deck.m');return d.getBoundingClientRect().top+scrollY-300})()"
FILT="(()=>{const d=document.querySelector('button.holc');return d.getBoundingClientRect().top+scrollY-520})()"
with sync_playwright() as p:
    b,ctx,pg=start(p,2)
    pg.locator('input[placeholder*=Search]').first.click(); pg.keyboard.type('Dear Santa'); pg.wait_for_timeout(1300)
    pg.evaluate("()=>[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.includes('Dear Santa')).click()"); pg.wait_for_timeout(3500); fixlogo(pg)
    pg.evaluate(f"()=>window.scrollTo(0,{DECK})"); pg.wait_for_timeout(4000)
    pg.evaluate(f"()=>window.scrollTo(0,{FILT})"); pg.wait_for_timeout(2500)
    # chip rect for later ring overlay
    chip=pg.evaluate("()=>{const r=document.querySelector('button.holc').getBoundingClientRect();return [r.left,r.top,r.width,r.height]}")
    cdp=ctx.new_cdp_session(pg); FR=[]
    def onf(e):
        n=len(FR); open(f'{OUT}/f/{n:05d}.jpg','wb').write(base64.b64decode(e['data'])); FR.append(e['metadata']['timestamp'])
        try: cdp.send('Page.screencastFrameAck',{'sessionId':e['sessionId']})
        except Exception: pass
    cdp.on('Page.screencastFrame',onf)
    cdp.send('Page.startScreencast',{'format':'jpeg','quality':92,'maxWidth':780,'maxHeight':1688,'everyNthFrame':1})
    T0[0]=time.time(); pg.wait_for_timeout(1200); mark('chips')
    pg.evaluate("()=>document.querySelector('.chip.holc').click()"); mark('tap'); pg.wait_for_timeout(1500)
    smooth(pg,DECK,700); mark('deck'); pg.wait_for_timeout(500)
    k=pg.evaluate("()=>Object.keys(M).find(k=>M[k].n==='The Polo Club'&&!M[k].hid)"); pg.evaluate("(k)=>{S.mfront=k;S.mfset=S.set;renderAll()}",k); pg.wait_for_timeout(1500); fixlogo(pg); mark('polo')
    pg.evaluate("()=>[...document.querySelectorAll('button.no')].filter(b=>b.offsetParent)[0].click()"); mark('x'); pg.wait_for_timeout(1600)
    pg.evaluate("()=>[...document.querySelectorAll('button.yes')].filter(b=>b.offsetParent)[0].click()"); mark('h1'); pg.wait_for_timeout(1600)
    k=pg.evaluate("()=>Object.keys(M).find(k=>M[k].n==='Festive Plaid Premium'&&!M[k].hid)"); pg.evaluate("(k)=>{S.mfront=k;S.mfset=S.set;renderAll()}",k); pg.wait_for_timeout(1500); fixlogo(pg); mark('fp')
    pg.evaluate("()=>[...document.querySelectorAll('button.yes')].filter(b=>b.offsetParent)[0].click()"); mark('h2'); pg.wait_for_timeout(1600)
    smooth(pg,"(()=>{const t=document.querySelector('.tray');return t?t.getBoundingClientRect().top+scrollY-520:scrollY+300})()",600); mark('tray'); pg.wait_for_timeout(1500); mark('end')
    cdp.send('Page.stopScreencast'); pg.wait_for_timeout(300)
    json.dump({'frames':FR,'marks':marks,'chip':chip},open(OUT+'/marks.json','w'),indent=1); print(len(FR),'frames',chip)
    b.close()
