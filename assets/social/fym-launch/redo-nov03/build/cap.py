"""Launch reel redo (Nov 3): screen recordings from the live FYM site copy v113 (same harness as the holiday intro v5:
v2_lib.start = 2x capture + mc/ routing fix). Sunday tiles x Brownstone Bloom.
Usage: python3 cap.py [rec0|recA|recB|all]  -> /dev/shm/lr/{rec0,recA,recP,recB} (+ recB/storycard.png)"""
import sys, os, json, time, base64
sys.path.insert(0, '/home/claude/mahjmatchmaker-data/assets/social/holiday-nov1/intro/build')
from v2_lib import *
O = '/dev/shm/lr'; os.makedirs(O + '/dbg', exist_ok=True)
WHAT = sys.argv[1] if len(sys.argv) > 1 else 'all'
BB = 'shop.andersruff.com/brownstone-bloom-mahjong-mat'; SONG = 'mahjandvine.com/chinoiserie-song-bird'
OZ = 'alb2:ozark-mah-jongg-carson-vintage'; MG = 'brittmillsdesign.com/knox-neoprene-mahjong-mat'  # Nov 6: was Mahjong Row Midnight Garden (MR out); Knox = her real Sunday pick
WAL = 'www.bambirdboutique.com/wooden-mahjong-rack-pusher-set'; OAK = 'peacelovemahjong.com/mahjong-racks-racks-pushers-set-of-4'
TEAL = 'www.bambirdboutique.com/wooden-mahjong-rack-pusher-set?v=52307844235573'
DECKQ = [BB, SONG, OZ, MG]
def smooth(pg, js_target, ms=700):
    pg.evaluate(f"""()=>{{const y=({js_target});const s=scrollY,d=y-s,t0=performance.now();function f(t){{const k=Math.min(1,(t-t0)/{ms});window.scrollTo(0,s+d*(k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2));if(k<1)requestAnimationFrame(f)}}requestAnimationFrame(f)}}"""); pg.wait_for_timeout(ms + 150)
def imgs(pg): pg.evaluate("()=>Promise.all([...document.images].filter(i=>i.offsetParent&&!i.complete).map(i=>new Promise(r=>{i.onload=i.onerror=r;setTimeout(r,8000)})))")
def btn(txt): return f"[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim().startsWith({json.dumps(txt)}))"
def rect(pg, js): return pg.evaluate(f"()=>{{const b={js};if(!b)return null;const r=b.getBoundingClientRect();return [r.left,r.top,r.width,r.height]}}")
def sunday(pg):
    pg.locator('input[placeholder*=Search]').first.click(); pg.keyboard.type('Sunday'); pg.wait_for_timeout(1300)
    pg.evaluate("()=>[...document.querySelectorAll('button')].find(b=>b.offsetParent&&/\\nSunday\\nSunday Mahjong/.test(b.innerText)).click()"); pg.wait_for_timeout(4000); fixlogo(pg)
    queue(pg)
def queue(pg):
    pg.evaluate("""(q)=>{const md=matDeck0;window.matDeck0=function(){const a=md();return q.filter(x=>!S.seen[x])};try{matDeck0=window.matDeck0}catch(e){};renderAll()}""", DECKQ); pg.wait_for_timeout(1500); imgs(pg)
class Rec:
    def __init__(s, ctx, pg, out):
        s.pg, s.out = pg, out; os.makedirs(out + '/f', exist_ok=True); s.FR = []; s.marks = []; s.cdp = ctx.new_cdp_session(pg)
        def onf(e):
            n = len(s.FR); open(f'{out}/f/{n:05d}.jpg', 'wb').write(base64.b64decode(e['data'])); s.FR.append(e['metadata']['timestamp'])
            try: s.cdp.send('Page.screencastFrameAck', {'sessionId': e['sessionId']})
            except Exception: pass
        s.cdp.on('Page.screencastFrame', onf)
    def go(s): s.cdp.send('Page.startScreencast', {'format': 'jpeg', 'quality': 82, 'maxWidth': 780, 'maxHeight': 1688, 'everyNthFrame': 1}); s.T0 = time.time()
    def mark(s, n, extra=None):
        s.marks.append([n, round(time.time() - s.T0, 3), len(s.FR), extra or {}]); print(n, s.marks[-1][1:3], extra or '')
    def stop(s, extra=None):
        s.cdp.send('Page.stopScreencast'); s.pg.wait_for_timeout(300)
        json.dump({'frames': s.FR, 'marks': s.marks, **(extra or {})}, open(s.out + '/marks.json', 'w'), indent=1); print(len(s.FR), 'frames')
with sync_playwright() as p:
    if WHAT in ('rec0', 'all'):  # home -> Start with tiles -> type Sunday -> tap Sunday -> mats screen
        b, ctx, pg = start(p, 2); queue(pg)  # queue first so the first mat card under Sunday is Brownstone Bloom (no unacknowledged card)
        R = Rec(ctx, pg, f'{O}/rec0'); R.go(); pg.wait_for_timeout(1000)
        R.mark('top', {'swt': rect(pg, btn('Start with tiles'))})
        pg.evaluate(f"()=>{btn('Start with tiles')}.click()"); R.mark('swttap'); pg.wait_for_timeout(1000)
        inp = pg.locator('input[placeholder*=Search]').first
        R.mark('search', {'inp': pg.evaluate("()=>{const i=[...document.querySelectorAll('input')].find(i=>i.offsetParent&&/Search/.test(i.placeholder));const r=i.getBoundingClientRect();return [r.left,r.top,r.width,r.height]}")})
        inp.click(); 
        for ch in 'Sunday': pg.keyboard.type(ch); pg.wait_for_timeout(110)
        pg.wait_for_timeout(900); imgs(pg)
        sb = "[...document.querySelectorAll('button')].find(b=>b.offsetParent&&/\\nSunday\\nSunday Mahjong/.test(b.innerText))"
        R.mark('result', {'sun': rect(pg, sb)}); pg.wait_for_timeout(600)
        pg.evaluate(f"()=>{sb}.click()"); R.mark('suntap'); pg.wait_for_timeout(2600); fixlogo(pg)
        CTX = "(()=>{const h=[...document.querySelectorAll('h1,h2,h3,div')].find(e=>e.offsetParent&&e.innerText&&e.innerText.trim().startsWith('Mat-ching'));return h.getBoundingClientRect().top+scrollY-70})()"
        smooth(pg, CTX, 800); imgs(pg); pg.wait_for_timeout(500); R.mark('mats'); pg.wait_for_timeout(900); R.mark('end'); R.stop(); b.close()
    if WHAT in ('recA', 'all'):  # swipes: ♥ Brownstone, ✕ Songbird, ♥ Carson Vintage, ♥ Midnight Garden
        b, ctx, pg = start(p, 2); sunday(pg)
        CTX = "(()=>{const h=[...document.querySelectorAll('h1,h2,h3,div')].find(e=>e.offsetParent&&e.innerText&&e.innerText.trim().startsWith('Mat-ching'));return h.getBoundingClientRect().top+scrollY-70})()"
        pg.evaluate(f"()=>window.scrollTo(0,{CTX})"); pg.wait_for_timeout(2500); fixlogo(pg); imgs(pg)
        pg.screenshot(path=f'{O}/dbg/deck0.png')
        R = Rec(ctx, pg, f'{O}/recA'); R.go(); pg.wait_for_timeout(1200)
        for nm, k in [('bb', 'yes'), ('song', 'no'), ('oz', 'yes'), ('mg', 'yes')]:
            R.mark('show ' + nm); pg.wait_for_timeout(500)
            pg.evaluate(f"()=>[...document.querySelectorAll('button.{k}')].filter(b=>b.offsetParent)[0].click()"); R.mark(k + ' ' + nm); pg.wait_for_timeout(1500); imgs(pg)
        smooth(pg, "(()=>{const t=document.querySelector('.tray');return t?t.getBoundingClientRect().top+scrollY-520:scrollY+300})()", 700)
        R.mark('tray'); pg.wait_for_timeout(1500); R.mark('end'); R.stop(); b.close()
    if WHAT in ('recB', 'all'):
        b, ctx, pg = start(p, 2); sunday(pg)
        for k in ['yes', 'no', 'yes', 'yes']: pg.evaluate(f"()=>[...document.querySelectorAll('button.{k}')].filter(b=>b.offsetParent)[0].click()"); pg.wait_for_timeout(1500)
        pk = "[...document.querySelectorAll('.pick1 button')].find(b=>b.offsetParent&&/Brownstone/.test(b.innerText))"
        smooth(pg, f"(()=>{{const b={pk};return b.getBoundingClientRect().top+scrollY-430}})()", 300); imgs(pg); pg.wait_for_timeout(800)
        R0 = Rec(ctx, pg, f'{O}/recP'); R0.go(); pg.wait_for_timeout(900)
        R0.mark('pick0', {'bb': rect(pg, pk)}); pg.wait_for_timeout(700)
        pg.evaluate(f"()=>{pk}.click()"); R0.mark('picktap'); pg.wait_for_timeout(1800); fixlogo(pg); R0.mark('after'); R0.stop()
        pg.evaluate("(q)=>{window._rq=q;const pool=rackPool;window.rackPool=function(){const a=pool();return window._rq.slice()};try{rackPool=window.rackPool}catch(e){};renderRacks()}", [TEAL, WAL, OAK]); pg.wait_for_timeout(1200)
        # turn Tiffany's rack picks OFF with the real chip so the deck opens on Teal Wood (nothing on screen goes unacknowledged)
        pg.evaluate("()=>{const d=document.querySelector('.deck.r');const top=d?d.getBoundingClientRect().top:0;const c=[...document.querySelectorAll('button')].filter(b=>b.offsetParent&&/^Tiffany.s picks: on/.test(b.innerText.trim())).find(b=>b.getBoundingClientRect().top>top-400);c&&c.click()}"); pg.wait_for_timeout(600)
        pg.evaluate("(q)=>{window._rq=q;renderRacks()}", [TEAL, WAL, OAK]); pg.wait_for_timeout(1500)
        pg.evaluate("()=>{const d=document.querySelector('.deck.r');window.scrollTo(0,d.getBoundingClientRect().top+scrollY-520)}"); pg.wait_for_timeout(2500); fixlogo(pg); imgs(pg)
        pg.screenshot(path=f'{O}/dbg/racks0.png')
        R = Rec(ctx, pg, f'{O}/recB'); R.go(); pg.wait_for_timeout(900); R.mark('racks')
        for i in range(2):
            pg.evaluate("()=>{const bs=[...document.querySelectorAll('.tilev.mband .zb button')].filter(b=>b.offsetParent);const plus=bs.find(b=>b.innerText.trim()==='+');plus&&plus.click()}"); R.mark(f'plus{i}'); pg.wait_for_timeout(700)
        wood = "[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim()==='Wood')"
        R.mark('wood0', {'wood': rect(pg, wood)}); pg.wait_for_timeout(300)
        pg.evaluate(f"()=>{{const b={wood};b&&b.click()}}"); pg.wait_for_timeout(200)
        pg.evaluate("(q)=>{window._rq=q;renderRacks()}", [TEAL, WAL, OAK]); R.mark('woodtap'); pg.wait_for_timeout(1100); imgs(pg)
        SEQ = [(TEAL, 'no'), (WAL, 'yes'), (OAK, 'yes')]
        for i, (r, k) in enumerate(SEQ):
            pg.evaluate("(q)=>{window._rq=q;renderRacks()}", [x for x, _ in SEQ[i:]]); pg.wait_for_timeout(900); R.mark('show ' + r)
            pg.evaluate(f"()=>[...document.querySelectorAll('button.{k}')].filter(b=>b.offsetParent).pop().click()"); R.mark(k + ' ' + r); pg.wait_for_timeout(1400)
        pg.evaluate("()=>{S.rpick=S.rliked.slice(0,2);renderRacks()}"); pg.wait_for_timeout(900); R.mark('official')
        pg.evaluate("()=>[...document.querySelectorAll('button.go')].filter(b=>b.offsetParent).pop().click()"); pg.wait_for_timeout(2500)
        smooth(pg, "(()=>{const h=[...document.querySelectorAll('h2,h1,div')].find(e=>e.innerText&&e.innerText.trim().startsWith('Your match card')&&e.offsetParent);return h.getBoundingClientRect().top+scrollY-90})()", 900)
        R.mark('card'); pg.wait_for_timeout(2000)
        sh = "(()=>{const h=[...document.querySelectorAll('h2,h3,div,p')].find(e=>e.offsetParent&&e.innerText&&/^Shop your match/.test(e.innerText.trim()));return h?h.getBoundingClientRect().top+scrollY-90:scrollY+900})()"
        smooth(pg, sh, 1000); imgs(pg); R.mark('shop'); pg.wait_for_timeout(2000); R.mark('end')
        R.stop({'rliked': pg.evaluate('()=>S.rliked'), 'rpick': pg.evaluate('()=>S.rpick')})
        pg.evaluate("()=>{const b=[...document.querySelectorAll('button')].find(b=>b.offsetParent&&/Story/.test(b.innerText));if(b)b.click();else{S.fmt='story';renderAll()}}"); pg.wait_for_timeout(6000)
        src = pg.evaluate("()=>{const i=[...document.querySelectorAll('img')].filter(e=>e.offsetParent&&e.naturalHeight>=3000)[0];return i?i.src:''}")
        if src.startswith('data:'): open(f'{O}/recB/storycard.png', 'wb').write(base64.b64decode(src.split(',', 1)[1])); print('storycard ok')
        elif src.startswith('blob:'):
            d = pg.evaluate("async(u)=>{const ab=new Uint8Array(await (await fetch(u)).arrayBuffer());let s='';for(let i=0;i<ab.length;i+=32768)s+=String.fromCharCode.apply(null,ab.subarray(i,i+32768));return btoa(s)}", src)
            open(f'{O}/recB/storycard.png', 'wb').write(base64.b64decode(d)); print('storycard ok (blob)')
        else: print('no storycard')
        b.close()
