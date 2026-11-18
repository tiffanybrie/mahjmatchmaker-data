import json
from playwright.sync_api import sync_playwright
O='/tmp/jr/omm2/'
with sync_playwright() as p:
    b=p.chromium.launch();ctx=b.new_context(viewport={'width':390,'height':844},device_scale_factor=3)
    pg=ctx.new_page();pg.goto('https://www.mahjmatchmaker.com/find-your-match',timeout=90000);pg.wait_for_timeout(9000)
    f=pg.frames[1]
    f.evaluate("()=>{const s=document.createElement('style');s.textContent='.swh{display:none!important}';document.head.appendChild(s)}")
    s=f.locator('input[placeholder*=Search]').first;s.click();s.type('Juniper',delay=40);pg.wait_for_timeout(1500)
    f.evaluate("()=>[...document.querySelectorAll('button')].find(b=>b.offsetParent&&/Juniper/.test(b.innerText)).click()");pg.wait_for_timeout(3000)
    clk=lambda t:f.evaluate("t=>{const b=[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim().startsWith(t));b&&b.click();return !!b}",t)
    sc=lambda y:(f.evaluate("y=>window.scrollTo(0,y)",y),pg.wait_for_timeout(900))
    def top():
        f.evaluate("()=>{const d=document.querySelector('.deck.m');window.scrollTo(0,d.getBoundingClientRect().top+scrollY-110)}");pg.wait_for_timeout(1200)
    clk('Aerial');pg.wait_for_timeout(1200)
    sc(330);pg.screenshot(path=O+'01-before.png')
    clk('Same brand as my tiles');pg.wait_for_timeout(2500)
    pg.screenshot(path=O+'02-samebrand.png')
    top();log=[]
    for i in range(12):
        name=f.evaluate("()=>{const c=document.querySelector('.deck.m');return c?c.innerText.split('\\n').slice(0,2).join(' / '):''}")
        pg.screenshot(path=O+f'1{i:02d}-deck.png');log.append(name)
        f.evaluate("()=>{const d=document.querySelector('.deck.m');const r=d.getBoundingClientRect();const b=[...document.querySelectorAll('button')].filter(b=>b.offsetParent&&b.innerText.trim()=='✕');const x=b.find(b=>{const q=b.getBoundingClientRect();return q.top>r.top&&q.top<r.bottom});x&&x.click()}")
        pg.wait_for_timeout(1300)
    print(log)
    # search Camellia
    m=f.locator('input[placeholder*="Search any mat"]').first
    f.evaluate("()=>{const m=document.querySelector('input[placeholder*=\"Search any mat\"]');window.scrollTo(0,m.getBoundingClientRect().top+scrollY-260)}");pg.wait_for_timeout(800)
    m.click()
    for k,t in enumerate(['C','Ca','Cam','Came','Camel','Camellia']):
        m.fill(t);pg.wait_for_timeout(700);pg.screenshot(path=O+f'2{k}-type.png')
    f.evaluate("()=>{const L=[...document.querySelectorAll('.msr button')].filter(b=>b.offsetParent);const e=L.find(b=>b.innerText.includes('Camellia'));e&&e.click()}");pg.wait_for_timeout(2500)
    top();pg.screenshot(path=O+'30-camellia.png')
    f.evaluate("()=>{const d=document.querySelector('.deck.m');const r=d.getBoundingClientRect();const b=[...document.querySelectorAll('button')].filter(b=>b.offsetParent&&b.innerText.trim()=='♥');const x=b.find(b=>{const q=b.getBoundingClientRect();return q.top>r.top&&q.top<r.bottom});x&&x.click()}")
    pg.wait_for_timeout(500);pg.screenshot(path=O+'31-heart.png');pg.wait_for_timeout(1500);pg.screenshot(path=O+'32-afterheart.png')
    # back to camellia via search, table + rack swaps
    m.fill('Camellia');pg.wait_for_timeout(1200)
    f.evaluate("()=>{const L=[...document.querySelectorAll('.msr button')].filter(b=>b.offsetParent);const e=L.find(b=>b.innerText.includes('Camellia'));e&&e.click()}");pg.wait_for_timeout(2500)
    clk('Table');pg.wait_for_timeout(1500)
    for k,r in enumerate(['Oh My Mahjong Tortoise Shell','Oh My Mahjong White Acrylic','Oh My Mahjong Agate','Oh My Mahjong Pink Quartz','Oh My Mahjong Burl','Carrara Rack']):
        clk('Adjust');pg.wait_for_timeout(1000);clk('Swap racks');pg.wait_for_timeout(1200)
        f.locator('input[placeholder*="Search racks"]').first.fill(' '.join(r.split()[-2:]));pg.wait_for_timeout(1200)
        got=f.evaluate("r=>{const L=[...document.querySelectorAll('.tvit')].filter(x=>x.offsetParent);let e=L.find(x=>x.innerText.startsWith(r));if(!e){const w=r.toLowerCase().split(' ');e=L.find(x=>w.every(k=>x.innerText.toLowerCase().includes(k)))};if(e){e.click();return e.innerText.split('\\n')[0]};return 'NONE'}",r)
        pg.wait_for_timeout(1800)
        for _ in range(3):
            f.evaluate("()=>{const b=[...document.querySelectorAll('button')].filter(b=>b.offsetParent&&b.innerText.trim()=='×'&&b.getBoundingClientRect().top>300);b.length&&b[b.length-1].click()}");pg.wait_for_timeout(600)
        top();pg.screenshot(path=O+f'4{k}-rack.png');print('rack',r,got)
    b.close()
