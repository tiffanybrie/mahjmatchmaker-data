import sys
from playwright.sync_api import sync_playwright
TILE,MAT,BRAND,OUT=sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]
RB=sys.argv[5] if len(sys.argv)>5 else BRAND
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':797},device_scale_factor=3)
    pg.goto('http://localhost:8766/index.html?tour=off'); pg.wait_for_timeout(4000)
    pg.locator('input[placeholder*=Search]').first.click(); pg.keyboard.type(TILE); pg.wait_for_timeout(1200)
    pg.evaluate("(t)=>[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim().startsWith(t)).click()",TILE); pg.wait_for_timeout(1200)
    pg.evaluate("([m,br])=>{const id=Object.keys(M).find(k=>M[k].n===m&&M[k].bn===br);S.f.m.her=false;S.f.m.brand=br;S.mfront=id;renderAll();}",[MAT,BRAND]); pg.wait_for_timeout(3000)
    pg.evaluate("()=>{const d=document.querySelector('.deck.m');window.scrollTo(0,d.getBoundingClientRect().top+scrollY-360)}"); pg.wait_for_timeout(3000)
    pg.screenshot(path=OUT+'_swipe.png')
    pg.evaluate("()=>[...document.querySelectorAll('button.yes')].find(b=>b.offsetParent).click()"); pg.wait_for_timeout(1500)
    pg.evaluate("(m)=>[...document.querySelectorAll('button')].filter(e=>e.offsetParent&&e.innerText.trim()==m).pop().click()",MAT); pg.wait_for_timeout(1500)
    pg.evaluate("(br)=>{S.f.r.her=false;S.f.r.brand=br;renderRacks();}",RB); pg.wait_for_timeout(2500)
    RK=sys.argv[6].split(',') if len(sys.argv)>6 else []
    OV=sys.argv[7].split(',') if len(sys.argv)>7 and sys.argv[7] else []
    if OV:
        import base64
        ov={r:'data:image/png;base64,'+base64.b64encode(open(f,'rb').read()).decode() for r,f in zip(RK,OV) if f}
        pg.evaluate("""async(ov)=>{const ix=await hdIndex();ix.r=ix.r||{};for(const k in ov){ix.r[k]='file:'+ov[k];IMG[R[k].im]=ov[k];R[k].c=true;}}""",ov)
    if RK: pg.evaluate("(r)=>{S.rpick=r;S.rliked=r.slice();renderRacks();}",RK); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{window.codeLine=()=>'';try{codeLine=()=>''}catch(e){}}")
    pg.evaluate("()=>[...document.querySelectorAll('button.go')].filter(b=>b.offsetParent&&b.innerText.includes('official')).pop().click()"); pg.wait_for_timeout(4500)
    ok=pg.evaluate("()=>{const b=[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim()=='Mood board');if(!b)return 0;b.click();return 1}")
    pg.wait_for_timeout(800)
    pg.evaluate("()=>{const b=[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim().startsWith('Post'));if(b)b.click();}"); pg.wait_for_timeout(3000)
    if ok: pg.evaluate("()=>{const b=[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim()=='Mood board');window.scrollTo(0,b.getBoundingClientRect().top+scrollY-75)}"); pg.wait_for_timeout(2500)
    print('card',ok, pg.evaluate("S.rpick"))
    pg.screenshot(path=OUT+'_card.png')
    b.close()
