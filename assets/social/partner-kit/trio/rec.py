import sys,os,glob,shutil
from playwright.sync_api import sync_playwright
B,TS,MAT=sys.argv[1:4]; OUT=sys.argv[4]
def js(pg,c,a=None): return pg.evaluate(c,a)
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx=b.new_context(viewport={'width':390,'height':844},device_scale_factor=2)
    pg=ctx.new_page(); import time; T0=time.time(); pg.goto('http://localhost:8766/index.html?tour=off'); pg.wait_for_timeout(3500)
    try: pg.get_by_text('Skip tour').click(timeout=1500)
    except Exception: pass
    js(pg,"()=>{codeLine=()=>''}")
    import base64; FR=[]; os.makedirs('frames',exist_ok=True); [os.remove('frames/'+f) for f in os.listdir('frames')]
    cdp=ctx.new_cdp_session(pg)
    def onf(e):
        FR.append(e['metadata']['timestamp']); open('frames/%05d.jpg'%len(FR),'wb').write(base64.b64decode(e['data'])); cdp.send('Page.screencastFrameAck',{'sessionId':e['sessionId']})
    cdp.on('Page.screencastFrame',onf); cdp.send('Page.startScreencast',{'format':'jpeg','quality':92,'maxWidth':780,'maxHeight':1688,'everyNthFrame':1})
    print('START',time.time()-T0)
    # brand filter on tile door
    js(pg,"(br)=>{const s=[...document.querySelectorAll('select')].find(x=>[...x.options].some(o=>o.text.startsWith(br)));if(s){const o=[...s.options].find(o=>o.text.startsWith(br));s.value=o.value;s.dispatchEvent(new Event('change',{bubbles:true}));}}",B)
    pg.wait_for_timeout(1800)
    js(pg,"(n)=>{const el=[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim().startsWith(n));el.scrollIntoView({behavior:'smooth',block:'center'})}",TS); pg.wait_for_timeout(1200)
    js(pg,"(n)=>{[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim().startsWith(n)).click()}",TS); pg.wait_for_timeout(1800)
    js(pg,"([m,br])=>{const id=Object.keys(M).find(k=>M[k].n===m&&M[k].bn===br);S.f.m.brand=br;S.f.m.her=false;S.mfront=id;renderAll();}",[MAT,B]); pg.wait_for_timeout(600)
    js(pg,"()=>{const d=document.querySelector('.deck.m');d&&d.scrollIntoView({behavior:'smooth',block:'center'})}"); pg.wait_for_timeout(2200)
    pg.locator('button.yes:visible').first.click(); pg.wait_for_timeout(1500)
    js(pg,"(m)=>{const b=[...document.querySelectorAll('button')].filter(e=>e.offsetParent&&e.innerText.trim()==m).pop();b&&b.scrollIntoView({behavior:'smooth',block:'center'});}",MAT); pg.wait_for_timeout(900)
    js(pg,"(m)=>{const b=[...document.querySelectorAll('button')].filter(e=>e.offsetParent&&e.innerText.trim()==m).pop();b.click()}",MAT); pg.wait_for_timeout(1800)
    js(pg,"(br)=>{S.f.r.brand=br;S.f.r.her=false;renderRacks();const d=document.querySelector('.deck.r');d&&d.scrollIntoView({behavior:'smooth',block:'center'})}",B); pg.wait_for_timeout(1800)
    for sel in ('yes','no','yes'):
        pg.locator('button.'+sel).last.click(); pg.wait_for_timeout(1200)
    js(pg,"()=>{S.rpick=S.rliked.slice(0,2);renderRacks();const mk=[...document.querySelectorAll('button')].filter(e=>e.offsetParent&&/Make it official/.test(e.innerText)).pop();mk&&mk.scrollIntoView({behavior:'smooth',block:'center'})}"); pg.wait_for_timeout(1400)
    js(pg,"()=>{const b=[...document.querySelectorAll('button')].filter(e=>e.offsetParent&&/Make it official/.test(e.innerText)).pop();b&&b.click()}"); pg.wait_for_timeout(1500)
    js(pg,"()=>{codeLine=()=>'';S.fmt='story';S.view='tri';drawCard();}"); pg.wait_for_timeout(2500)
    js(pg,"()=>{const p=document.getElementById('prev');p&&p.scrollIntoView({behavior:'smooth',block:'start'})}"); pg.wait_for_timeout(4500)
    print('rpick',js(pg,"()=>S.rpick.map(r=>R[r].n)"), js(pg,"()=>S.fav&&M[S.fav].n"))
    pg.wait_for_timeout(300); cdp.send('Page.stopScreencast')
    with open('frames/list.txt','w') as f:
        for i,t in enumerate(FR):
            d=(FR[i+1]-t) if i+1<len(FR) else 1.5
            f.write("file '%05d.jpg'\nduration %.3f\n"%(i+1,max(d,0.001)))
        f.write("file '%05d.jpg'\n"%len(FR))
    ctx.close(); b.close(); print('frames',len(FR))
