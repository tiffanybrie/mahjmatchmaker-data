import sys,os,asyncio,time,base64
from playwright.async_api import async_playwright
B,TS,MAT=sys.argv[1:4]
RK=sys.argv[4] if len(sys.argv)>4 else 'yes,no,yes'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); ctx=await b.new_context(viewport={'width':390,'height':844},device_scale_factor=2)
        pg=await ctx.new_page(); await pg.goto('http://localhost:8766/index.html?tour=off'); await pg.wait_for_timeout(3500)
        js=lambda c,a=None: pg.evaluate(c,a); w=pg.wait_for_timeout
        await js("()=>{codeLine=()=>''}")
        os.makedirs('frames',exist_ok=True); [os.remove('frames/'+f) for f in os.listdir('frames')]
        cdp=await ctx.new_cdp_session(pg); FR=[]; run=[True]
        async def cap():
            while run[0]:
                m=await cdp.send('Page.getLayoutMetrics'); v=m['cssVisualViewport']; r=await cdp.send('Page.captureScreenshot',{'format':'jpeg','quality':90,'clip':{'x':v['pageX'],'y':v['pageY'],'width':390,'height':844,'scale':2}}); FR.append(time.time()); open('frames/%05d.jpg'%len(FR),'wb').write(base64.b64decode(r['data']))
        task=asyncio.create_task(cap()); await w(600)
        await js("(br)=>{const s=[...document.querySelectorAll('select')].find(x=>[...x.options].some(o=>o.text.startsWith(br)));if(s){const o=[...s.options].find(o=>o.text.startsWith(br));s.value=o.value;s.dispatchEvent(new Event('change',{bubbles:true}));}}",B); await w(1800)
        await js("(n)=>{const el=[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim().startsWith(n));el.scrollIntoView({behavior:'smooth',block:'center'})}",TS); await w(1200)
        await js("(n)=>{[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim().startsWith(n)).click()}",TS); await w(1800)
        await js("([m,br])=>{const id=Object.keys(M).find(k=>M[k].n===m&&M[k].bn===br);S.f.m.brand=br;S.f.m.her=false;S.mfront=id;renderAll();}",[MAT,B]); await w(600)
        await js("()=>{const d=document.querySelector('.deck.m');d&&d.scrollIntoView({behavior:'smooth',block:'center'})}"); await w(2200)
        await pg.locator('button.yes:visible').first.click(); await w(1500)
        await js("(m)=>{const b=[...document.querySelectorAll('button')].filter(e=>e.offsetParent&&e.innerText.trim()==m).pop();b&&b.scrollIntoView({behavior:'smooth',block:'center'});}",MAT); await w(900)
        await js("(m)=>{const b=[...document.querySelectorAll('button')].filter(e=>e.offsetParent&&e.innerText.trim()==m).pop();b.click()}",MAT); await w(1800)
        await js("(br)=>{S.f.r.brand=br;S.f.r.her=false;renderRacks();const d=document.querySelector('.deck.r');d&&d.scrollIntoView({behavior:'smooth',block:'center'})}",B); await w(1800)
        for sel in RK.split(','):
            await pg.locator('button.'+sel).last.click(); await w(1200)
        await js("()=>{S.rpick=S.rliked.slice(0,2);renderRacks();const mk=[...document.querySelectorAll('button')].filter(e=>e.offsetParent&&/Make it official/.test(e.innerText)).pop();mk&&mk.scrollIntoView({behavior:'smooth',block:'center'})}"); await w(1400)
        await js("()=>{const b=[...document.querySelectorAll('button')].filter(e=>e.offsetParent&&/Make it official/.test(e.innerText)).pop();b&&b.click()}"); await w(1500)
        await js("()=>{codeLine=()=>'';S.view='tri';drawCard();}"); await w(2500)
        await js("()=>{const p=document.getElementById('prev');p&&p.scrollIntoView({behavior:'smooth',block:'center'})}"); await w(4500)
        print('rpick',await js("()=>S.rpick.map(r=>R[r].n)"),await js("()=>S.fav&&M[S.fav].n"))
        run[0]=False; await task; await b.close()
    with open('frames/list.txt','w') as f:
        for i,t in enumerate(FR):
            d=(FR[i+1]-t) if i+1<len(FR) else 1.5
            f.write("file '%05d.jpg'\nduration %.3f\n"%(i+1,d))
        f.write("file '%05d.jpg'\n"%len(FR))
    print('frames',len(FR),round(FR[-1]-FR[0],1))
asyncio.run(main())
