"""Capture REAL Find Your Mat-ch screens (live site app HTML, Version 1.10, served locally) for a brand reel.
Flow (FYM-REEL-RULES 14-22): pick tiles (Holiday chip) -> swipe mats (♥/✕, card png + bbox cut out for the fly-off)
-> suitors -> racks step: + + zoom on the chosen mat -> swipe racks ✕/♥/♥ -> card.
Usage: python3 cap_fym.py <cfg.json> <outdir>   (the app HTML: getsrc in README; served at http://localhost:8791)"""
import sys, json, os
from playwright.sync_api import sync_playwright
CFG = json.load(open(sys.argv[1])); OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
meta = {}
def shot(pg, n): pg.screenshot(path=f'{OUT}/{n}.png'); print('shot', n)
def deck(pg, sel='.deck.m', off=330):
    pg.evaluate(f"()=>{{const d=document.querySelector('{sel}');window.scrollTo(0,d.getBoundingClientRect().top+scrollY-{off})}}"); pg.wait_for_timeout(1100)
def card(pg, sel, n):
    bb = pg.evaluate(f"()=>{{const e=document.querySelector('{sel} .scard:not(.back)');const q=e.getBoundingClientRect();return [q.left,q.top,q.width,q.height]}}")
    pg.locator(f'{sel} .scard:not(.back)').first.screenshot(path=f'{OUT}/{n}-card.png'); meta[n] = bb
def front(pg, name):
    k = pg.evaluate("(n)=>Object.keys(M).find(k=>M[k].n===n&&!M[k].hid)", name); assert k, name
    pg.evaluate("(k)=>{S.mfront=k;renderAll()}", k); pg.wait_for_timeout(1300)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=3)
    pg.goto('http://localhost:8791/index.html?tour=off', timeout=60000); pg.wait_for_timeout(6500)
    pg.add_style_tag(content='.swh{display:none!important}')
    pg.evaluate("()=>[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim().startsWith('Start with tiles')).click()"); pg.wait_for_timeout(1500)
    pg.evaluate("()=>[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim()==='Holiday').click()"); pg.wait_for_timeout(1800)
    # scroll so the chosen set's button is in view, record its centre
    idx = pg.evaluate("(s)=>D.sets.findIndex(x=>x.slug===s)", CFG['set'])
    pg.evaluate(f"()=>{{const b=document.querySelector('[data-tile=\"{idx}\"]');window.scrollTo(0,b.getBoundingClientRect().top+scrollY-420)}}"); pg.wait_for_timeout(1500)
    meta['tilebtn'] = pg.evaluate(f"()=>{{const q=document.querySelector('[data-tile=\"{idx}\"]').getBoundingClientRect();return [q.left+q.width/2,q.top+q.height/2]}}")
    shot(pg, '01-tiles')
    pg.evaluate(f"()=>document.querySelector('[data-tile=\"{idx}\"]').click()"); pg.wait_for_timeout(2600)
    meta['deckn'] = pg.evaluate("()=>matDeck().length")
    TOP = "()=>{const e=document.querySelector('.deck.m .scard:not(.back)');const n=e.querySelector('b,strong,h3,.nm');return e.innerText.split('\\n').map(x=>x.trim()).filter(x=>x)}"
    meta['swipes'] = []; did_no = False
    pg.evaluate("(ns)=>{Object.keys(M).forEach(k=>{if(ns.includes(M[k].n))S.seen[k]=1});renderAll()}", CFG.get('skip', [])); pg.wait_for_timeout(1200)
    for i in range(CFG.get('swipes', 5)):
        deck(pg); txt = pg.evaluate(TOP)
        key = pg.evaluate("()=>{const q=queue('m');return q&&q[0]}")
        mm = pg.evaluate("(k)=>M[k]?[M[k].n,M[k].bn]:null", key)
        kind = 'yes'
        if mm and mm[0] == CFG.get('no'): kind = 'no'
        shot(pg, f's{i}-b'); card(pg, '.deck.m', f's{i}'); meta['swipes'].append([key, mm, kind])
        pg.evaluate(f"()=>[...document.querySelectorAll('.deck.m button.{kind}')].filter(b=>b.offsetParent)[0].click()"); pg.wait_for_timeout(1400)
        deck(pg); shot(pg, f's{i}-a')
    print(meta['swipes'])
    deck(pg, '.deck.m', 250); pg.evaluate("window.scrollBy(0,360)"); pg.wait_for_timeout(1000); shot(pg, '30-suitors')
    pk = pg.evaluate("(n)=>Object.keys(M).find(k=>M[k].n===n&&!M[k].hid&&S.liked.includes(k))||Object.keys(M).find(k=>M[k].n===n&&!M[k].hid)", CFG['pick'])
    pg.evaluate("(k)=>{if(!S.liked.includes(k))S.liked.push(k);S.fav=k;renderAll()}", pk); pg.wait_for_timeout(2500); meta['pick'] = pk
    RY = CFG['racks_yes']; RX = CFG['rack_no']
    pg.evaluate("(r)=>{const pool=rackPool;window.rackPool=function(){const a=pool();return [...r.filter(x=>R[x]),...a.filter(x=>!r.includes(x))]};try{rackPool=window.rackPool}catch(e){};S.f.r.her=false;S.rseen=[];renderRacks();}", [RX] + RY); pg.wait_for_timeout(2500)
    pg.evaluate("()=>{const d=document.querySelector('.deck.r');window.scrollTo(0,d.getBoundingClientRect().top+scrollY-420)}"); pg.wait_for_timeout(1500)
    PL = "()=>[...document.querySelectorAll('[data-z],button')].filter(b=>b.offsetParent&&b.innerText.trim()==='+'&&b.getBoundingClientRect().top>0&&b.getBoundingClientRect().top<420)[0]"
    try: meta['rz'] = pg.evaluate(f"()=>{{const b=({PL})();const q=b.getBoundingClientRect();return [q.left+q.width/2,q.top+q.height/2]}}")
    except Exception as e: meta['rz'] = None; print('no + found', e)
    for i in range(3):
        shot(pg, f'40-rz{i}')
        if i < 2: pg.evaluate(f"()=>{{const b=({PL})();b&&b.click()}}"); pg.wait_for_timeout(900)
    for j, (rk, kind) in enumerate([(RX, 'no'), (RY[0], 'yes'), (RY[1], 'yes')]):
        shot(pg, f'r{j}-b'); card(pg, '.deck.r', f'r{j}')
        pg.evaluate(f"()=>[...document.querySelectorAll('.deck.r button.{kind}')].filter(b=>b.offsetParent)[0].click()"); pg.wait_for_timeout(1500)
        shot(pg, f'r{j}-a')
    pg.evaluate("()=>{S.rpick=S.rliked.slice(-2);S.made=true;renderAll();}"); pg.wait_for_timeout(2500)
    pg.evaluate("()=>{const d=document.getElementById('s-card');window.scrollTo(0,d.getBoundingClientRect().top+scrollY-10)}"); pg.wait_for_timeout(3500)
    shot(pg, '60-card')
    pg.evaluate("window.scrollBy(0,640)"); pg.wait_for_timeout(1500); shot(pg, '61-card2')
    json.dump(meta, open(f'{OUT}/meta.json', 'w'), indent=1); b.close()
