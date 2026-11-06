# Spotlight capture (house style, FYM-REEL-RULES #39; pattern from holiday-nov1/intro/build/v2_capture.py) on the LIVE FYM page
import json, time, base64, os
from playwright.sync_api import sync_playwright
OUT=os.path.dirname(os.path.abspath(__file__))+'/rec'; os.makedirs(OUT+'/f',exist_ok=True)
RECT="""(sel)=>{const e=[...document.querySelectorAll(sel)].find(x=>x.offsetParent);if(!e)return null;const r=e.getBoundingClientRect();return [r.left,r.top,r.width,r.height]}"""
with sync_playwright() as p:
    b=p.chromium.launch(args=['--force-device-scale-factor=2']); ctx=b.new_context(viewport={'width':390,'height':844},device_scale_factor=2); pg=ctx.new_page()
    pg.goto('https://www.mahjmatchmaker.com/find-your-match',wait_until='networkidle',timeout=90000); pg.wait_for_timeout(4000)
    f=[x for x in pg.frames if x.url=='about:srcdoc'][0]
    def rect(sel):
        r=f.evaluate(RECT,sel); 
        if not r: return None
        o=pg.evaluate("()=>{const i=document.querySelector('iframe');const r=i.getBoundingClientRect();return [r.left,r.top]}")
        return [round(2*(r[0]+o[0]),1),round(2*(r[1]+o[1]),1),round(2*r[2],1),round(2*r[3],1)]
    try: f.get_by_text('No thanks').click(timeout=3000)
    except Exception: pass
    f.get_by_text('Start with tiles').click(); f.select_option('#tbr','Royal Mahjong Society'); pg.wait_for_timeout(1500)
    f.evaluate("()=>{const e=[...document.querySelectorAll('*')].find(x=>x.offsetParent&&x.children.length<4&&x.innerText&&x.innerText.trim().startsWith('Heirloom Collection Crown Jewels'));let c=e;while(c&&c.tagName!=='BUTTON')c=c.parentElement;(c||e).id='cjcard';(c||e).scrollIntoView({block:'center'})}")
    f.evaluate("()=>Promise.all([...document.images].filter(i=>i.offsetParent&&!i.complete).map(i=>new Promise(r=>{i.onload=i.onerror=r;setTimeout(r,6000)})))"); pg.wait_for_timeout(1500)
    FR=[]; marks=[]; cdp=ctx.new_cdp_session(pg)
    def onf(e):
        n=len(FR); open(f'{OUT}/f/{n:05d}.jpg','wb').write(base64.b64decode(e['data'])); FR.append(e['metadata']['timestamp'])
        try: cdp.send('Page.screencastFrameAck',{'sessionId':e['sessionId']})
        except Exception: pass
    cdp.on('Page.screencastFrame',onf)
    cdp.send('Page.startScreencast',{'format':'jpeg','quality':85,'maxWidth':780,'maxHeight':1688,'everyNthFrame':1}); T0=time.time()
    def mark(n,**sels):
        marks.append([n,round(time.time()-T0,3),len(FR),{k:rect(v) for k,v in sels.items()}]); print(marks[-1][:3], marks[-1][3])
    pg.wait_for_timeout(1200); mark('list',card='#cjcard')
    f.evaluate("()=>document.getElementById('cjcard').click()"); mark('tap',card='#cjcard'); pg.wait_for_timeout(2600)
    f.evaluate("()=>Promise.all([...document.images].filter(i=>i.offsetParent&&!i.complete).map(i=>new Promise(r=>{i.onload=i.onerror=r;setTimeout(r,6000)})))"); pg.wait_for_timeout(800)
    mark('deck',deck='.deck.m',tiles='.mband')
    seq=['yes','no','no','yes','no','yes']
    for i,k in enumerate(seq):
        f.evaluate(f"()=>[...document.querySelectorAll('button.sb.{k}')].filter(b=>b.offsetParent)[0].click()"); mark(f'{k}{i}',deck='.deck.m'); pg.wait_for_timeout(1500)
    f.evaluate("()=>{const t=document.querySelector('#th');t.scrollIntoView({behavior:'smooth',block:'center'})}"); pg.wait_for_timeout(1300)
    mark('tray',tray='#th'); pg.wait_for_timeout(2000); mark('end',tray='#th')
    cdp.send('Page.stopScreencast'); pg.wait_for_timeout(300)
    names=f.evaluate("()=>[...document.querySelectorAll('#th button')].map(b=>b.getAttribute('aria-label'))")
    json.dump({'frames':FR,'marks':marks,'suitors':names},open(OUT+'/marks.json','w'),indent=1); print(len(FR),'frames',names)
    b.close()
