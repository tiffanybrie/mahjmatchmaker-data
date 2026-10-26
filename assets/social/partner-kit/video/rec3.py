"""Record FYM at 2x with a tap dot + an event log for the compositor."""
import sys,os,asyncio,time,base64,json
from playwright.async_api import async_playwright
CFG=json.load(open(sys.argv[1]))
B=CFG['brand']; TS=CFG['tiles']; MX=CFG['mat_skip']; MAT=CFG['mat']; RK=CFG.get('racks','yes,no,yes')
TAPJS="""(sel)=>{const el=typeof sel==='string'?document.querySelector(sel):sel;}"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); ctx=await b.new_context(viewport={'width':390,'height':844},device_scale_factor=2)
        pg=await ctx.new_page(); await pg.goto('http://localhost:8766/index.html?tour=off'); await pg.wait_for_timeout(3500)
        js=lambda c,a=None: pg.evaluate(c,a); w=pg.wait_for_timeout
        await js("""()=>{codeLine=()=>'';const st=document.createElement('style');st.textContent='#tapdot{position:fixed;width:46px;height:46px;margin:-23px 0 0 -23px;border-radius:50%;background:rgba(200,50,95,.35);border:3px solid rgba(255,255,255,.95);box-shadow:0 4px 14px rgba(6,42,85,.35);pointer-events:none;z-index:99999;opacity:0;transform:scale(.6);transition:opacity .18s,transform .25s}#tapdot.on{opacity:1;transform:scale(1)}#tapdot.press{transform:scale(.78);background:rgba(200,50,95,.6)}';document.head.appendChild(st);const d=document.createElement('div');d.id='tapdot';document.body.appendChild(d);
          window.__tap=async(el)=>{const r=el.getBoundingClientRect();const x=r.left+r.width/2,y=r.top+r.height/2;d.style.left=x+'px';d.style.top=y+'px';d.className='on';await new Promise(s=>setTimeout(s,550));d.className='on press';await new Promise(s=>setTimeout(s,160));el.click();d.className='on';await new Promise(s=>setTimeout(s,260));d.className='';return [r.left,r.top,r.width,r.height];};
          window.__rect=el=>{const r=el.getBoundingClientRect();return [r.left,r.top,r.width,r.height]}; }""")
        # pre-set: tile door filtered to the brand
        await js("(br)=>{const s=[...document.querySelectorAll('select')].find(x=>[...x.options].some(o=>o.text.startsWith(br)));const o=[...s.options].find(o=>o.text.startsWith(br));s.value=o.value;s.dispatchEvent(new Event('change',{bubbles:true}));}",B); await w(1200)
        await js("(br)=>{const s=[...document.querySelectorAll('select')].find(x=>[...x.options].some(o=>o.text.startsWith(br)));s.scrollIntoView({block:'start'});window.scrollBy(0,-70)}",B); await w(800)
        os.makedirs('frames',exist_ok=True); [os.remove('frames/'+f) for f in os.listdir('frames')]
        cdp=await ctx.new_cdp_session(pg); FR=[]; run=[True]; EV=[]
        async def cap():
            while run[0]:
                m=await cdp.send('Page.getLayoutMetrics'); v=m['cssVisualViewport']; r=await cdp.send('Page.captureScreenshot',{'format':'jpeg','quality':90,'clip':{'x':v['pageX'],'y':v['pageY'],'width':390,'height':844,'scale':2}}); FR.append(time.time()); open('frames/%05d.jpg'%len(FR),'wb').write(base64.b64decode(r['data']))
        T0=time.time(); task=asyncio.create_task(cap())
        def ev(kind,rect=None,label=None): EV.append({'t':time.time()-T0,'kind':kind,'rect':rect,'label':label})
        async def tap(jsfind,arg=None,label=None,kind='tap'):
            h=await pg.evaluate_handle(jsfind,arg); await js('(e)=>{const r=e.getBoundingClientRect();if(r.bottom>innerHeight-30||r.top<70){e.scrollIntoView({block:"center"});}}',h); await w(450); ev('pre',await js('(e)=>__rect(e)',h),label)
            r=await js('(e)=>__tap(e)',h); ev(kind,r,label); return r
        ev('step',None,'1 · Pick your tiles'); await w(1600)
        await tap("(n)=>[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim().startsWith(n))",TS,'1 · Pick your tiles'); await w(900)
        await js("([m,br])=>{const id=Object.keys(M).find(k=>M[k].n===m&&M[k].bn===br);S.f.m.brand=br;S.f.m.her=false;S.mfront=id;renderAll();const d=document.querySelector('.deck.m');d.scrollIntoView({block:'center'});window.scrollBy(0,40)}",[MX,B]); await w(300)
        ev('step',None,'2 · Swipe the mats'); ev('full',await js("()=>__rect(document.querySelector('.deck.m'))")); await w(1700)
        await tap("()=>document.querySelector('button.no:not([disabled])')",None,'2 · Swipe the mats'); await w(700)
        await js("([m,br])=>{const id=Object.keys(M).find(k=>M[k].n===m&&M[k].bn===br);S.mfront=id;renderMats();}",[MAT,B]); await w(1500)
        await tap("()=>[...document.querySelectorAll('button.yes')].find(b=>b.offsetParent)",None,'2 · Swipe the mats'); await w(900)
        await js("([m,br])=>{const b=[...document.querySelectorAll('button')].filter(e=>e.offsetParent&&e.innerText.trim()==m).pop();b.click();S.f.r.brand=br;S.f.r.her=false;renderRacks();const d=document.querySelector('.deck.r');d.scrollIntoView({block:'center'});window.scrollBy(0,40)}",[MAT,B]); await w(300)
        ev('step',None,'3 · Add two racks'); ev('full',await js("()=>__rect(document.querySelector('.deck.r'))")); await w(1400)
        for sel in RK.split(','):
            await tap("(s)=>[...document.querySelectorAll('button.'+s)].filter(b=>b.offsetParent).pop()",sel,'3 · Add two racks'); await w(800)
        await js("()=>{S.rpick=S.rliked.slice(0,2);renderRacks();const mk=[...document.querySelectorAll('button')].filter(e=>e.offsetParent&&/Make it official/.test(e.innerText)).pop();mk.scrollIntoView({block:'center'})}"); await w(900)
        await tap("()=>[...document.querySelectorAll('button')].filter(e=>e.offsetParent&&/Make it official/.test(e.innerText)).pop()",None,'3 · Add two racks'); await w(600)
        ev('step',None,'4 · Your match card'); await js("()=>{codeLine=()=>'';S.view='tri';drawCard();}"); await w(3200)
        await js("()=>{const p=document.getElementById('prev');p.scrollIntoView({block:'center'})}"); await w(300)
        ev('card',await js("()=>__rect(document.getElementById('prev'))")); await w(3800)
        ev('end')
        run[0]=False; await task; print('rpick',await js("()=>S.rpick.map(r=>R[r].n)"),await js("()=>S.fav&&M[S.fav].n")); await b.close()
    json.dump({'frames':[t-T0 for t in FR],'events':EV},open('rec.json','w'),indent=1); print('frames',len(FR))
asyncio.run(main())
