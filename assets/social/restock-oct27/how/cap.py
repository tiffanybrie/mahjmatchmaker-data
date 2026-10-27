import sys,json
from playwright.sync_api import sync_playwright
SET,TAG,MATS,PICK,RACKS=sys.argv[1],sys.argv[2],json.loads(sys.argv[3]),sys.argv[4],json.loads(sys.argv[5])
OUT=f'/tmp/sun/how/{TAG}'; import os; os.makedirs(OUT,exist_ok=True)
def shot(pg,n): pg.screenshot(path=f'{OUT}/{n}.png'); print('shot',n)
def deck(pg,off=330): pg.evaluate(f"()=>{{const d=document.querySelector('.deck.m');window.scrollTo(0,d.getBoundingClientRect().top+scrollY-{off})}}"); pg.wait_for_timeout(1100)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=3)
    pg.goto('http://localhost:8766/index.html?tour=off'); pg.wait_for_timeout(4500); pg.add_style_tag(content='.swh{display:none!important}')
    pg.locator('input[placeholder*=Search]').first.click(); pg.keyboard.type(SET.split()[-1]); pg.wait_for_timeout(1200); shot(pg,'01-search')
    pg.evaluate("(t)=>[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim().startsWith(t)).click()",SET); pg.wait_for_timeout(2500)
    ids=pg.evaluate("(names)=>names.map(n=>Object.keys(M).find(k=>M[k].n===n&&!M[k].hid))",MATS); print(ids)
    for i,k in enumerate(ids):
        pg.evaluate("(k)=>{S.mfront=k;renderAll()}",k); pg.wait_for_timeout(1500); deck(pg); shot(pg,f'02-swipe{i}')
        pg.evaluate("()=>[...document.querySelectorAll('button.yes')].find(b=>b.offsetParent).click()"); pg.wait_for_timeout(1300)
    deck(pg,250); pg.evaluate("window.scrollBy(0,360)"); pg.wait_for_timeout(900); shot(pg,'03-suitors')
    pg.evaluate("(m)=>{const b=[...document.querySelectorAll('.r3p .pick1 button, button')].filter(e=>e.offsetParent&&e.innerText.includes(m)).pop();b&&b.click()}",PICK); pg.wait_for_timeout(2500)
    pg.evaluate("(r)=>{const pool=rackPool;window.rackPool=function(){const a=pool();return [...r.filter(x=>R[x]),...a.filter(x=>!r.includes(x))]};try{rackPool=window.rackPool}catch(e){};S.f.r.her=false;S.rseen=[];renderRacks();}",RACKS); pg.wait_for_timeout(2500)
    pg.evaluate("()=>{const d=document.querySelector('.deck.r');window.scrollTo(0,d.getBoundingClientRect().top+scrollY-420)}"); pg.wait_for_timeout(1500); shot(pg,'04-racks')
    # zoom the mat (top card) with its + button
    z=pg.evaluate("()=>{const btn=[...document.querySelectorAll('button')].filter(b=>b.offsetParent&&b.innerText.trim()==='+');const r=btn.map(b=>b.getBoundingClientRect().top);return btn.length}"); print('plus buttons',z)
    pg.evaluate("()=>{const btn=[...document.querySelectorAll('button')].filter(b=>b.offsetParent&&b.innerText.trim()==='+'&&b.getBoundingClientRect().top>0&&b.getBoundingClientRect().top<400);btn[0]&&btn[0].click();}"); pg.wait_for_timeout(900)
    pg.evaluate("()=>{const btn=[...document.querySelectorAll('button')].filter(b=>b.offsetParent&&b.innerText.trim()==='+'&&b.getBoundingClientRect().top>0&&b.getBoundingClientRect().top<400);btn[0]&&btn[0].click();}"); pg.wait_for_timeout(1200); shot(pg,'05-racks-zoom')
    for _ in RACKS:
        pg.evaluate("()=>[...document.querySelectorAll('button.yes')].filter(b=>b.offsetParent).pop().click()"); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{S.rpick=S.rliked.slice(0,2);renderRacks()}"); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{const d=document.querySelector('.deck.r');window.scrollTo(0,d.getBoundingClientRect().top+scrollY-60)}"); pg.wait_for_timeout(1000); shot(pg,'06-slots')
    b.close()
