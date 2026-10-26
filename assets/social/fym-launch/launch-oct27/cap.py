import sys,os
from playwright.sync_api import sync_playwright
TILE,MAT,BRAND,OUT,RK=sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5].split(',')
MATFIX=os.environ.get('MATFIX')
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':797},device_scale_factor=3)
    pg.goto('http://localhost:8766/index.html?tour=off'); pg.wait_for_timeout(4000)
    if MATFIX:
        k_,n_=MATFIX.split('|||'); pg.evaluate("([k,n])=>{M[k].n=n;M[k].dn=n}",[k_,n_])
    pg.locator('input[placeholder*=Search]').first.click(); pg.keyboard.type(TILE); pg.wait_for_timeout(1200)
    pg.evaluate("(t)=>[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim().startsWith(t)).click()",TILE); pg.wait_for_timeout(1500)
    pg.evaluate("([m,br])=>{const id=Object.keys(M).find(k=>M[k].n===m&&M[k].bn===br);S.f.m.her=false;S.mfront=id;renderAll();}",[MAT,BRAND]); pg.wait_for_timeout(3000)
    pg.evaluate("()=>{const d=document.querySelector('.deck.m');window.scrollTo(0,d.getBoundingClientRect().top+scrollY-360)}"); pg.wait_for_timeout(3000)
    pg.screenshot(path=OUT+'_swipe.png')
    pg.evaluate("()=>[...document.querySelectorAll('button.yes')].find(b=>b.offsetParent).click()"); pg.wait_for_timeout(1500)
    pg.evaluate("(m)=>[...document.querySelectorAll('button')].filter(e=>e.offsetParent&&e.innerText.trim()==m).pop().click()",MAT); pg.wait_for_timeout(2500)
    # bring the first wanted rack to the front of the rack deck
    pg.evaluate("(r)=>{const pool=rackPool;window.rackPool=function(){const a=pool();return [...r.filter(x=>R[x]),...a.filter(x=>!r.includes(x))]};try{rackPool=window.rackPool}catch(e){};renderRacks();}",RK); pg.wait_for_timeout(2500)
    pg.evaluate("()=>{const d=document.querySelector('.deck.r')||document.querySelector('.deck');window.scrollTo(0,d.getBoundingClientRect().top+scrollY-300)}"); pg.wait_for_timeout(3000)
    pg.screenshot(path=OUT+'_racks.png')
    pg.evaluate("(r)=>{S.rpick=r;S.rliked=r.slice();renderRacks();}",RK); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{const c=set().tc||'#d6247f';const src=drawCard.toString();const i=src.indexOf('const tc=(()=>');const j=src.indexOf('})();',i)+5;window.drawCard=(0,eval)('('+src.slice(0,i)+\"const tc='\"+c+\"';\"+src.slice(j)+')');try{drawCard=window.drawCard}catch(e){}}")
    P=os.environ.get('SRCPATCH')
    if P:
        for pr in P.split(';;'):
            o_,n_=pr.split('|||'); print('patch',pg.evaluate("([o,n])=>{const src=drawCard.toString();if(!src.includes(o))return false;window.drawCard=(0,eval)('('+src.split(o).join(n)+')');try{drawCard=window.drawCard}catch(e){};return true}",[o_,n_]))
    pg.evaluate("()=>[...document.querySelectorAll('button.go')].filter(b=>b.offsetParent&&b.innerText.includes('official')).pop().click()"); pg.wait_for_timeout(4500)
    ok=pg.evaluate("()=>{const b=[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim()=='Mood board');if(!b)return 0;b.click();return 1}"); pg.wait_for_timeout(800)
    pg.evaluate("()=>{const b=[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim().startsWith('Post'));if(b)b.click();}"); pg.wait_for_timeout(3000)
    pg.evaluate("()=>{const b=[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim()=='Mood board');window.scrollTo(0,b.getBoundingClientRect().top+scrollY-75)}"); pg.wait_for_timeout(2500)
    print('card',ok,pg.evaluate("S.rpick"))
    pg.screenshot(path=OUT+'_card.png')
    b.close()
