from playwright.sync_api import sync_playwright
V={'width':390,'height':797}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport=V,device_scale_factor=3)
    pg.goto('http://localhost:8766/index.html?tour=off'); pg.wait_for_timeout(4000)
    pg.screenshot(path='s_home.png')
    pg.locator('input[placeholder*=Search]').first.click(); pg.keyboard.type('Malachite'); pg.wait_for_timeout(1200)
    pg.evaluate("()=>[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim().startsWith('Miss Classic Malachite')).click()"); pg.wait_for_timeout(1200)
    pg.evaluate("()=>{const id=Object.keys(M).find(k=>M[k].n==='Petalwood');S.mfront=id;renderAll();}"); pg.wait_for_timeout(2500)
    pg.evaluate("()=>{const d=document.querySelector('.deck.m');window.scrollTo(0,d.getBoundingClientRect().top+scrollY-360)}"); pg.wait_for_timeout(2500)
    pg.screenshot(path='s_swipe.png')
    pg.evaluate("()=>[...document.querySelectorAll('button.yes')].find(b=>b.offsetParent).click()"); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{const b=[...document.querySelectorAll('button')].filter(e=>e.offsetParent&&e.innerText.trim()=='Petalwood').pop(); if(b)b.click();}"); pg.wait_for_timeout(1500)
    for i in range(2):
        pg.evaluate("()=>[...document.querySelectorAll('button.yes')].filter(b=>b.offsetParent).pop().click()"); pg.wait_for_timeout(1300)
    pg.evaluate("()=>[...document.querySelectorAll('button.go')].filter(b=>b.offsetParent&&b.innerText.includes('official')).pop().click()"); pg.wait_for_timeout(3500)
    print(pg.evaluate("document.body.innerText.slice(0,300)"))
    pg.screenshot(path='s_card.png')
    print(pg.evaluate("[...document.querySelectorAll('button')].filter(b=>b.offsetParent).map(b=>(b.className+'|'+b.innerText.trim()).slice(0,40)).slice(0,80)"))
    pg.screenshot(path='s_after.png')
    b.close()
