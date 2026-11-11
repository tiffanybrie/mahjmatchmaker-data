#!/usr/bin/env python3
"""FYM phone shots for an album's reel kit (Tiffany Nov 10-11: white iPhone, tiles visible with the mat, the album's
TOP 8 mats in Table / Aerial / Up close, Table view on each mat's own album racks = manifest mat_racks[0], never oak).
Goes to each mat with the app's own "Search any mat" box (works for any set, no reliance on deck order).
Usage: fym_capture.py <tile search text> <tile button regex> <plan.json> <outdir>
plan.json = [{"key":"reba","mat":"Reba","brand":"Britt Mills","rack":"Bird & Bamboo Evergreen"}, ...]
Writes <outdir>/raw/<i>-<view>-<key>.png (1170x2532) then frame with iphone_white.py."""
import sys, os, json
from playwright.sync_api import sync_playwright
q, rx, plan, out = sys.argv[1], sys.argv[2], json.load(open(sys.argv[3])), sys.argv[4]
os.makedirs(out + '/raw', exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=3)
    pg = ctx.new_page(); pg.goto('https://www.mahjmatchmaker.com/find-your-match', timeout=90000); pg.wait_for_timeout(9000)
    f = pg.frames[1]
    f.evaluate("()=>{const s=document.createElement('style');s.textContent='.swh{display:none!important}';document.head.appendChild(s)}")
    s = f.locator('input[placeholder*=Search]').first; s.click(); s.type(q, delay=40); pg.wait_for_timeout(1500)
    f.evaluate("rx=>[...document.querySelectorAll('button')].find(b=>b.offsetParent&&new RegExp(rx).test(b.innerText)).click()", rx); pg.wait_for_timeout(3000)
    clk = lambda t: f.evaluate("t=>{const b=[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim().startsWith(t));b&&b.click();return !!b}", t)
    def top():
        f.evaluate("()=>{const d=document.querySelector('.deck.m');window.scrollTo(0,d.getBoundingClientRect().top+scrollY-110)}"); pg.wait_for_timeout(1500)
    log = []
    for i, it in enumerate(plan):
        # jump to the mat
        m = f.locator('input[placeholder*="Search any mat"]').first
        m.fill(''); m.type(it['mat'], delay=30); pg.wait_for_timeout(1500)
        hit = f.evaluate("([m,br])=>{const L=[...document.querySelectorAll('.msr button, button')].filter(b=>b.offsetParent&&b.closest('.msr'));let e=L.find(b=>b.innerText.split('\\n')[0].trim()==m&&b.innerText.includes(br))||L.find(b=>b.innerText.includes(m));if(e){e.click();return e.innerText.replace(/\\n/g,' | ')};return 'NONE'}", [it['mat'], it['brand']])
        pg.wait_for_timeout(2500)
        clk('Table'); pg.wait_for_timeout(1500)
        got = 'n/a'
        if it.get('rack'):
            clk('Adjust'); pg.wait_for_timeout(1200); clk('Swap racks'); pg.wait_for_timeout(1500)
            w = it['rack'].split(); rq = ' '.join(w[-2:]) if len(w) > 2 else it['rack']
            f.locator('input[placeholder*="Search racks"]').first.fill(rq); pg.wait_for_timeout(1500)
            got = f.evaluate("r=>{const L=[...document.querySelectorAll('.tvit')].filter(x=>x.offsetParent);let e=L.find(x=>x.innerText.startsWith(r));if(!e){const w=r.toLowerCase().split(' ');e=L.find(x=>w.every(k=>x.innerText.toLowerCase().includes(k)))};if(e){e.click();return e.innerText.split('\\n')[0]};return 'NONE'}", it['rack'])
            pg.wait_for_timeout(2000)
            for _ in range(3):
                f.evaluate("()=>{const b=[...document.querySelectorAll('button')].filter(b=>b.offsetParent&&b.innerText.trim()=='×'&&b.getBoundingClientRect().top>300);b.length&&b[b.length-1].click()}"); pg.wait_for_timeout(700)
        top(); shown = f.evaluate("()=>{const c=document.querySelector('.deck.m');return c?c.innerText.split('\\n').slice(0,2).join(' / '):''}")
        pg.screenshot(path=f"{out}/raw/{i+1}-1-table-{it['key']}.png")
        clk('Aerial'); pg.wait_for_timeout(1800); top(); pg.screenshot(path=f"{out}/raw/{i+1}-2-aerial-{it['key']}.png")
        clk('Up close'); pg.wait_for_timeout(1800); top(); f.evaluate("()=>window.scrollBy(0,-260)"); pg.wait_for_timeout(800); pg.screenshot(path=f"{out}/raw/{i+1}-3-upclose-{it['key']}.png")
        log.append(dict(it, search=hit, rack_got=got, shown=shown)); print(i + 1, it['mat'], '| search:', hit[:40], '| rack:', got, '| deck:', shown[:50], flush=True)
    json.dump(log, open(out + '/capture-log.json', 'w'), indent=1)
    b.close()
