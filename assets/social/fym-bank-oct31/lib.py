import os
os.environ['TMPDIR']='/dev/shm/w'
from playwright.sync_api import sync_playwright
O='/dev/shm/w/caps/'; os.makedirs(O,exist_ok=True)
def start(p):
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=3)
    pg.goto('http://localhost:8777/index.html?tour=off'); pg.wait_for_timeout(5000)
    pg.add_style_tag(content='.swh{display:none!important}')
    return b,pg
def shot(pg,n): pg.screenshot(path=O+n+'.png'); print('shot',n)
def search_pick(pg,q,name):
    pg.locator('input[placeholder*=Search]').first.click(); pg.keyboard.type(q); pg.wait_for_timeout(1300)
    r=pg.evaluate("(t)=>{const b=[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim().startsWith(t));if(b){b.click();return true}return [...document.querySelectorAll('button')].filter(b=>b.offsetParent).map(b=>b.innerText.trim().slice(0,40)).slice(0,40)}",name)
    pg.wait_for_timeout(2800); return r
def deck(pg,sel='.deck.m',off=330):
    pg.evaluate(f"()=>{{const d=document.querySelector('{sel}');window.scrollTo(0,d.getBoundingClientRect().top+scrollY-{off})}}"); pg.wait_for_timeout(900)
def front(pg,name):
    k=pg.evaluate("(n)=>Object.keys(M).find(k=>M[k].n===n&&!M[k].hid)",name); assert k,name
    pg.evaluate("(k)=>{S.mfront=k;S.mfset=S.set;renderAll()}",k); pg.wait_for_timeout(1300)
