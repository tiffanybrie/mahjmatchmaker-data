"""Live Find Your Mat-ch recording for a tile set (generalised rec_fym_live.py, Nov 17).
Usage: rec.py <search text> <button text> <outdir>  -> <outdir>/f/*.jpg + meta.json"""
import os, json, time, base64, sys
from playwright.sync_api import sync_playwright
Q, BT, OUT = sys.argv[1], sys.argv[2], sys.argv[3]; os.makedirs(OUT + '/f', exist_ok=True)
FR = []; marks = []
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
    pg = ctx.new_page(); pg.goto('https://www.mahjmatchmaker.com/find-your-match', timeout=90000); pg.wait_for_timeout(10000)
    f = pg.frames[1]
    f.evaluate("()=>{const s=document.createElement('style');s.textContent='.swh{display:none!important}';document.head.appendChild(s)}")
    f.evaluate("()=>{const a=[...document.querySelectorAll('a,button')].find(x=>x.offsetParent&&/^No thanks$/.test(x.innerText.trim()));if(a)a.click()}")
    pg.wait_for_timeout(800)
    # in-stock only, so a sold-out mat never leads the reel (Nov 17)
    f.evaluate("()=>{const l=[...document.querySelectorAll('label,button,span')].find(x=>x.offsetParent&&x.innerText.trim()==='In stock only');if(l)l.click()}")
    pg.wait_for_timeout(800)
    f.evaluate("()=>window.scrollTo(0,0)"); pg.wait_for_timeout(500)
    cdp = ctx.new_cdp_session(pg)
    def onf(e):
        n = len(FR); open(f'{OUT}/f/{n:05d}.jpg', 'wb').write(base64.b64decode(e['data'])); FR.append(e['metadata']['timestamp'])
        try: cdp.send('Page.screencastFrameAck', {'sessionId': e['sessionId']})
        except Exception: pass
    cdp.on('Page.screencastFrame', onf)
    cdp.send('Page.startScreencast', {'format': 'jpeg', 'quality': 90, 'maxWidth': 780, 'maxHeight': 1688, 'everyNthFrame': 1})
    t0 = time.time(); M = lambda n: marks.append((n, round(time.time() - t0, 2)))
    pg.wait_for_timeout(900); M('home')
    inp = f.locator('input[placeholder*=Search]').first; inp.click(); inp.type(Q, delay=110); pg.wait_for_timeout(1100)
    btns = f.evaluate(f"()=>[...document.querySelectorAll('button')].filter(b=>b.offsetParent&&b.innerText.includes({json.dumps(BT)})).map(b=>b.innerText.slice(0,50))")
    print('btns', btns)
    if not btns: raise SystemExit('no tile button for ' + BT)
    f.evaluate(f"()=>[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.includes({json.dumps(BT)})).click()"); M('picked'); pg.wait_for_timeout(2500)
    f.evaluate("()=>{const d=document.querySelector('.deck.m');const y=d.getBoundingClientRect().top+scrollY-330;const s=scrollY,dd=y-s,t0=performance.now();function g(t){const k=Math.min(1,(t-t0)/800);window.scrollTo(0,s+dd*(k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2));if(k<1)requestAnimationFrame(g)}requestAnimationFrame(g)}")
    pg.wait_for_timeout(1500); M('deck')
    for k in ['yes', 'no', 'yes', 'yes']:
        f.evaluate(f"()=>[...document.querySelectorAll('button.{k}')].filter(b=>b.offsetParent)[0].click()"); pg.wait_for_timeout(1400)
    M('swiped'); pg.wait_for_timeout(1500)
    cdp.send('Page.stopScreencast'); M('end')
    json.dump({'ts': FR, 'marks': marks}, open(f'{OUT}/meta.json', 'w'))
    b.close()
print(len(FR), marks)
