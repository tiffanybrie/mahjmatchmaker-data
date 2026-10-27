"""Tinder-style capture: BEFORE/AFTER screens + the top card cut out, for every swipe (mats, holiday, racks)."""
import sys,json,os
from playwright.sync_api import sync_playwright
SET='Miss Classic Malachite'; OUT='/tmp/sun/how/malt'; os.makedirs(OUT,exist_ok=True)
EVERY=[('Darjeeling','yes'),('Cognac','no'),('YOTD Black','yes')]
HOL=[('Classic Very Merry Mahj','yes'),('Sleigh All Day Mat','no'),('Evergreen & Tartan','yes')]
PICK='Evergreen & Tartan'; RX='peacelovemahjong.com/mahjong-racks-racks-pushers-set-of-4'; RY=['bb:Wine','bb:Dark Teal']
meta={}
def shot(pg,n): pg.screenshot(path=f'{OUT}/{n}.png'); print('shot',n)
def deck(pg,sel='.deck.m',off=330): pg.evaluate(f"()=>{{const d=document.querySelector('{sel}');window.scrollTo(0,d.getBoundingClientRect().top+scrollY-{off})}}"); pg.wait_for_timeout(900)
def card(pg,sel,n):
    el=pg.locator(f'{sel} .scard:not(.back)').first
    bb=pg.evaluate(f"()=>{{const e=document.querySelector('{sel} .scard:not(.back)');const q=e.getBoundingClientRect();return [q.left,q.top,q.width,q.height]}}")
    el.screenshot(path=f'{OUT}/{n}-card.png'); meta[n]=bb
def front(pg,name):
    k=pg.evaluate("(n)=>Object.keys(M).find(k=>M[k].n===n&&!M[k].hid)",name); assert k,name
    pg.evaluate("(k)=>{S.mfront=k;renderAll()}",k); pg.wait_for_timeout(1300)
def press(pg,kind,sel): pg.evaluate(f"()=>[...document.querySelectorAll('{sel} ~ * button.{kind}, button.{kind}')].filter(b=>b.offsetParent)[0].click()"); pg.wait_for_timeout(1300)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=3)
    pg.goto('http://localhost:8766/index.html?tour=off'); pg.wait_for_timeout(4500); pg.add_style_tag(content='.swh{display:none!important}')
    pg.locator('input[placeholder*=Search]').first.click(); pg.keyboard.type('Malachite'); pg.wait_for_timeout(1200); shot(pg,'01-search')
    pg.evaluate("(t)=>[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim().startsWith(t)).click()",SET); pg.wait_for_timeout(2500)
    seq=[('m',x) for x in EVERY]+[('h',x) for x in HOL]
    for i,(grp,(name,kind)) in enumerate(seq):
        if i==0:
            deck(pg)
            meta['colchip']=pg.evaluate("()=>{const b=[...document.querySelectorAll('button.dot')].find(b=>b.title==='Blue & teal');b.scrollIntoView({block:'nearest',inline:'center'});return 1}"); deck(pg)
            meta['colchip']=pg.evaluate("()=>{const q=[...document.querySelectorAll('button.dot')].find(b=>b.title==='Blue & teal').getBoundingClientRect();return [q.left+q.width/2,q.top+q.height/2]}")
            shot(pg,'10-col-before'); pg.evaluate("()=>[...document.querySelectorAll('button.dot')].find(b=>b.title==='Blue & teal').click()"); pg.wait_for_timeout(1300)
            meta['coln']=pg.evaluate("()=>matDeck().length")
        if grp=='h' and seq[i-1][0]=='m':
            pg.evaluate("()=>[...document.querySelectorAll('button.dot')].find(b=>b.title==='All colors').click()"); pg.wait_for_timeout(900)
            front(pg,seq[i-1][1][0]) if False else None
            pg.evaluate("()=>document.querySelector('.chip.holc').scrollIntoView({block:'nearest',inline:'center'})"); deck(pg); shot(pg,'20-hol-before')
            meta['holchip']=pg.evaluate("()=>{const q=document.querySelector('.chip.holc').getBoundingClientRect();return [q.left+q.width/2,q.top+q.height/2]}")
            pg.evaluate("()=>document.querySelector('.chip.holc').click()"); pg.wait_for_timeout(1500)
            meta['holn']=pg.evaluate("()=>matDeck().length")
        front(pg,name); deck(pg); shot(pg,f's{i}-b'); card(pg,'.deck.m',f's{i}')
        pg.evaluate(f"()=>[...document.querySelectorAll('button.{kind}')].filter(b=>b.offsetParent)[0].click()"); pg.wait_for_timeout(1300)
        nxt = seq[i+1][1][0] if i+1<len(seq) and seq[i+1][0]==grp else None
        if nxt: front(pg,nxt); deck(pg)
        else: deck(pg)
        shot(pg,f's{i}-a')
    meta['everyn']=57
    deck(pg,'.deck.m',250); pg.evaluate("window.scrollBy(0,360)"); pg.wait_for_timeout(900); shot(pg,'30-suitors')
    pg.evaluate("(m)=>{const b=[...document.querySelectorAll('.r3p .pick1 button, button')].filter(e=>e.offsetParent&&e.innerText.includes(m)).pop();b&&b.click()}",PICK); pg.wait_for_timeout(2500)
    pg.evaluate("(r)=>{const pool=rackPool;window.rackPool=function(){const a=pool();return [...r.filter(x=>R[x]),...a.filter(x=>!r.includes(x))]};try{rackPool=window.rackPool}catch(e){};S.f.r.her=false;S.rseen=[];renderRacks();}",RY); pg.wait_for_timeout(2500)
    pg.evaluate("()=>{const d=document.querySelector('.deck.r');window.scrollTo(0,d.getBoundingClientRect().top+scrollY-420)}"); pg.wait_for_timeout(1500)
    PL="()=>[...document.querySelectorAll('[data-z],button')].filter(b=>b.offsetParent&&b.innerText.trim()==='+'&&b.getBoundingClientRect().top>0&&b.getBoundingClientRect().top<420)[0]"
    meta['rz']=pg.evaluate(f"()=>{{const b=({PL})();const q=b.getBoundingClientRect();return [q.left+q.width/2,q.top+q.height/2]}}")
    for i in range(4):
        shot(pg,f'40-rz{i}')
        if i<3: pg.evaluate(f"()=>{{const b=({PL})();b&&b.click()}}"); pg.wait_for_timeout(900)
    # pan to the tartan border
    pr=pg.evaluate("()=>{const e=[...document.querySelectorAll('img')].filter(i=>i.offsetParent&&i.getBoundingClientRect().top<300&&i.getBoundingClientRect().width>200)[0].getBoundingClientRect();return [e.left+e.width/2,Math.max(e.top,150)+60]}")
    pg.mouse.move(pr[0],pr[1]); pg.mouse.down(); pg.mouse.move(pr[0]-140,pr[1]+60,steps=10); pg.mouse.up(); pg.wait_for_timeout(900); shot(pg,'40-rz4')
    pg.evaluate("()=>{const b=[...document.querySelectorAll('button.chip')].find(b=>b.offsetParent&&b.innerText.trim()==='Tortoise');b.scrollIntoView({block:'nearest',inline:'center'})}"); pg.evaluate("()=>{const d=document.querySelector('.deck.r');window.scrollTo(0,d.getBoundingClientRect().top+scrollY-420)}"); pg.wait_for_timeout(900)
    meta['rchips']=pg.evaluate("()=>[...document.querySelectorAll('button.chip')].filter(b=>b.offsetParent&&b.getBoundingClientRect().top>0&&b.getBoundingClientRect().top<500).map(b=>{const q=b.getBoundingClientRect();return [b.innerText.trim(),q.left+q.width/2,q.top+q.height/2]})")
    print(meta['rchips'])
    WC="()=>[...document.querySelectorAll('button.chip')].find(b=>b.offsetParent&&b.innerText.trim()==='Wood')"
    meta['woodchip']=pg.evaluate(f"()=>{{const q=({WC})().getBoundingClientRect();return [q.left+q.width/2,q.top+q.height/2]}}")
    shot(pg,'45-chips')
    for j,(rk,kind) in enumerate([(RX,'no'),(RY[0],'yes'),(RY[1],'yes')]):
        if j==0: pg.evaluate(f"()=>({WC})().click()"); pg.wait_for_timeout(1300)
        if j==1: pg.evaluate(f"()=>({WC})().click()"); pg.wait_for_timeout(1300)
        shot(pg,f'r{j}-b'); card(pg,'.deck.r',f'r{j}')
        pg.evaluate(f"()=>[...document.querySelectorAll('button.{kind}')].filter(b=>b.offsetParent).pop().click()"); pg.wait_for_timeout(1500)
        shot(pg,f'r{j}-a')
    pg.evaluate("()=>{S.rpick=S.rliked.slice(0,2);renderRacks()}"); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{const d=document.querySelector('.deck.r');window.scrollTo(0,d.getBoundingClientRect().top+scrollY-60)}"); pg.wait_for_timeout(1000); shot(pg,'50-slots')
    json.dump(meta,open(f'{OUT}/meta.json','w'),indent=1); b.close()
