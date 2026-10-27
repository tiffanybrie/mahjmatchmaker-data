import os
from playwright.sync_api import sync_playwright
OUT='/tmp/sun/caps'; os.makedirs(OUT,exist_ok=True)
def shot(pg,n): pg.screenshot(path=f'{OUT}/{n}.png'); print('shot',n)
def deck(pg,off=380): pg.evaluate(f"()=>{{const d=document.querySelector('.deck.m');window.scrollTo(0,d.getBoundingClientRect().top+scrollY-{off})}}"); pg.wait_for_timeout(1200)
def front(pg,k): pg.evaluate("(k)=>{S.mfront=k;renderAll()}",k); pg.wait_for_timeout(1800)
def yes(pg): pg.evaluate("()=>[...document.querySelectorAll('button.yes')].find(b=>b.offsetParent).click()"); pg.wait_for_timeout(1500)
def no(pg): pg.evaluate("()=>[...document.querySelectorAll('button.no')].find(b=>b.offsetParent).click()"); pg.wait_for_timeout(1500)
SB='mahjandvine.com/chinoiserie-song-bird';BB='shop.andersruff.com/brownstone-bloom-mahjong-mat'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=3)
    pg.goto('http://localhost:8766/index.html?tour=off'); pg.wait_for_timeout(4500); pg.add_style_tag(content='.swh{display:none!important}')
    pg.locator('input[placeholder*=Search]').first.click(); pg.keyboard.type('Sunday'); pg.wait_for_timeout(1000)
    pg.evaluate("()=>[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim().startsWith('Sunday')&&!b.innerText.includes('Blues')).click()"); pg.wait_for_timeout(2500)
    shot(pg,'02-search')
    front(pg,SB); deck(pg); shot(pg,'04-swipe-songbird')
    no(pg); front(pg,BB); deck(pg); shot(pg,'05-swipe-brownstone')
    yes(pg); pg.wait_for_timeout(800); deck(pg,250); shot(pg,'06-after-hearts')
    # scroll to suitors / pick step
    pg.evaluate("window.scrollBy(0,350)"); pg.wait_for_timeout(700); shot(pg,'07-suitors')
    pg.evaluate("()=>[...document.querySelectorAll('.r3p .pick1 button')].find(b=>b.innerText.includes('Brownstone')).click()"); pg.wait_for_timeout(2500)
    RK=['www.bambirdboutique.com/wooden-mahjong-rack-pusher-set','peacelovemahjong.com/mahjong-racks-racks-pushers-set-of-4']
    pg.evaluate("()=>{S.f.r.her=false;renderRacks()}"); pg.wait_for_timeout(800)
    pg.evaluate("(r)=>{const pool=rackPool;window.rackPool=function(){const a=pool();return [...r.filter(x=>R[x]),...a.filter(x=>!r.includes(x))]};try{rackPool=window.rackPool}catch(e){};S.f.r.her=false;S.rseen=[];renderRacks();}",RK); pg.wait_for_timeout(2500)
    pg.evaluate("()=>{const d=document.querySelector('.deck.r');window.scrollTo(0,d.getBoundingClientRect().top+scrollY-420)}"); pg.wait_for_timeout(1500); shot(pg,'08-racks')
    pg.evaluate("()=>[...document.querySelectorAll('button.yes')].filter(b=>b.offsetParent).pop().click()"); pg.wait_for_timeout(1800)
    pg.evaluate("()=>{const d=document.querySelector('.deck.r');window.scrollTo(0,d.getBoundingClientRect().top+scrollY-420)}"); pg.wait_for_timeout(1200); shot(pg,'09-racks2')
    pg.evaluate("()=>[...document.querySelectorAll('button.yes')].filter(b=>b.offsetParent).pop().click()"); pg.wait_for_timeout(1800)
    pg.evaluate("()=>{S.rpick=S.rliked.slice(0,2);renderRacks()}"); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{const d=document.querySelector('.deck.r');window.scrollTo(0,d.getBoundingClientRect().top+scrollY-60)}"); pg.wait_for_timeout(1000); shot(pg,'10-rack-slots')
    pg.evaluate("()=>[...document.querySelectorAll('button.go')].filter(b=>b.offsetParent&&b.innerText.includes('official')).pop().click()"); pg.wait_for_timeout(5000)
    pg.evaluate("()=>{const b=[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim()=='Mood board');b&&window.scrollTo(0,b.getBoundingClientRect().top+scrollY-75)}"); pg.wait_for_timeout(2500); shot(pg,'11-card')
    pg.evaluate("()=>{const h=[...document.querySelectorAll('h3')].find(h=>h.innerText.includes('Shop'));h&&window.scrollTo(0,h.getBoundingClientRect().top+scrollY-140)}"); pg.wait_for_timeout(1500); shot(pg,'12-shop')
    b.close()
