"""v2 (Nov 2) captures for the holiday intro reel, from the live FYM site copy (v113): mat photos + two screen recordings
with element rects logged at each step (used for the spotlight cut-outs in v2_reel.py).
Usage: python3 v2_capture.py [mats|recA|recB|all]   -> /dev/shm/introv2/{mats,recA,recB}"""
import sys, json, time, base64, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v2_lib import *
WHAT = sys.argv[1] if len(sys.argv) > 1 else 'all'
WALNUT = 'www.bambirdboutique.com/wooden-mahjong-rack-pusher-set'
def smooth(pg, js_target, ms=700):
    pg.evaluate(f"""()=>{{const y=({js_target});const s=scrollY,d=y-s,t0=performance.now();function f(t){{const k=Math.min(1,(t-t0)/{ms});window.scrollTo(0,s+d*(k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2));if(k<1)requestAnimationFrame(f)}}requestAnimationFrame(f)}}"""); pg.wait_for_timeout(ms + 150)
def front(pg, n):
    k = pg.evaluate("(n)=>Object.keys(M).find(k=>M[k].n===n&&!M[k].hid)", n)
    pg.evaluate("(k)=>{S.mfront=k;S.mfset=S.set;renderAll()}", k); pg.wait_for_timeout(1300); fixlogo(pg)
def dear_santa(pg):
    pg.locator('input[placeholder*=Search]').first.click(); pg.keyboard.type('Dear Santa'); pg.wait_for_timeout(1300)
    pg.evaluate("()=>[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.includes('Dear Santa')).click()"); pg.wait_for_timeout(4000); fixlogo(pg)
    # deck queue (picks stay on, the app default): Polo Club, Color Me Merry, Festive Plaid Premium, Candy Cane Lane, then the app's own order
    pg.evaluate("""()=>{const q=['The Polo Club','Color Me Merry','Festive Plaid Premium','Candy Cane Lane'].map(n=>Object.keys(M).find(k=>M[k].n===n&&!M[k].hid&&(n!=='Candy Cane Lane'||M[k].bn==='Anders Ruff')));window._mq=q;const md=matDeck0;window.matDeck0=function(){const a=md();return [...q.filter(x=>!S.seen[x]),...a.filter(x=>!q.includes(x))]};try{matDeck0=window.matDeck0}catch(e){};renderAll()}"""); pg.wait_for_timeout(1500)
    pg.evaluate("()=>Promise.all([...document.images].filter(i=>!i.complete).map(i=>new Promise(r=>{i.onload=i.onerror=r;setTimeout(r,8000)})))")
class Rec:
    def __init__(s, ctx, pg, out):
        s.pg, s.out = pg, out; os.makedirs(out + '/f', exist_ok=True); s.FR = []; s.marks = []; s.cdp = ctx.new_cdp_session(pg)
        def onf(e):
            n = len(s.FR); open(f'{out}/f/{n:05d}.jpg', 'wb').write(base64.b64decode(e['data'])); s.FR.append(e['metadata']['timestamp'])
            try: s.cdp.send('Page.screencastFrameAck', {'sessionId': e['sessionId']})
            except Exception: pass
        s.cdp.on('Page.screencastFrame', onf)
    def go(s):
        s.cdp.send('Page.startScreencast', {'format': 'jpeg', 'quality': 92, 'maxWidth': 780, 'maxHeight': 1688, 'everyNthFrame': 1}); s.T0 = time.time()
    def mark(s, n, *sels):
        rects = {q: s.pg.evaluate(RECT, q) for q in sels}
        s.marks.append([n, round(time.time() - s.T0, 3), len(s.FR), rects]); print(n, s.marks[-1][1:])
    def stop(s, extra=None):
        s.cdp.send('Page.stopScreencast'); s.pg.wait_for_timeout(300)
        json.dump({'frames': s.FR, 'marks': s.marks, **(extra or {})}, open(s.out + '/marks.json', 'w'), indent=1); print(len(s.FR), 'frames')

with sync_playwright() as p:
    if WHAT in ('mats', 'all'):
        b, ctx, pg = start(p, 1)
        st = json.load(open(f'{W}/stock.json'))
        ids = [k for k, v in st.items() if v['avail']] + ['soireeallday.co/color-me-merry-mahjong-mat']
        out = {}
        for k in ids:
            r = pg.evaluate("""async(id)=>{try{const f=M[id].f;await loadMC(f);const u=MC[f]||IMG[M[id].th];const bl=await (await fetch(u)).blob();const ab=new Uint8Array(await bl.arrayBuffer());let s='';for(let i=0;i<ab.length;i+=32768)s+=String.fromCharCode.apply(null,ab.subarray(i,i+32768));return [bl.type,btoa(s),M[id].n,M[id].bn]}catch(e){return ['err',String(e)]}}""", k)
            if r[0] == 'err': print('ERR', k, r[1]); continue
            ext = {'image/webp': 'webp', 'image/jpeg': 'jpg', 'image/png': 'png'}.get(r[0], 'bin')
            fn = f"{W}/mats/{k.replace('/', '__')}.{ext}"; open(fn, 'wb').write(base64.b64decode(r[1])); out[k] = [fn, r[2], r[3]]
        json.dump(out, open(f'{W}/mats/map.json', 'w'), indent=1); print('mats', len(out)); b.close()
    if WHAT in ('recA', 'all'):
        b, ctx, pg = start(p, 2); dear_santa(pg)
        DECK = "(()=>{const d=document.querySelector('.deck.m');return d.getBoundingClientRect().top+scrollY-300})()"
        pg.evaluate(f"()=>window.scrollTo(0,{DECK})"); pg.wait_for_timeout(3500)
        pg.evaluate("()=>{const d=document.querySelector('button.holc');window.scrollTo(0,d.getBoundingClientRect().top+scrollY-520)}"); pg.wait_for_timeout(2500)
        R = Rec(ctx, pg, f'{W}/recA'); R.go(); pg.wait_for_timeout(1200); R.mark('chips', 'button.holc')
        pg.evaluate("()=>document.querySelector('.chip.holc').click()"); R.mark('tap', 'button.holc'); pg.wait_for_timeout(1400)
        smooth(pg, DECK, 800); R.mark('deck', '.deck.m', '.mband')
        pg.evaluate("()=>Promise.all([...document.images].filter(i=>i.offsetParent&&!i.complete).map(i=>new Promise(r=>{i.onload=i.onerror=r;setTimeout(r,6000)})))"); pg.wait_for_timeout(1200); R.mark('deckready', '.deck.m')
        R.mark('polo', '.deck.m')
        pg.evaluate("()=>[...document.querySelectorAll('button.no')].filter(b=>b.offsetParent)[0].click()"); R.mark('x'); pg.wait_for_timeout(1500)
        R.mark('cmm', '.deck.m')
        pg.evaluate("()=>[...document.querySelectorAll('button.yes')].filter(b=>b.offsetParent)[0].click()"); R.mark('h1'); pg.wait_for_timeout(1500)
        R.mark('fp', '.deck.m')
        pg.evaluate("()=>[...document.querySelectorAll('button.yes')].filter(b=>b.offsetParent)[0].click()"); R.mark('h2'); pg.wait_for_timeout(1500)
        smooth(pg, "(()=>{const t=document.querySelector('.tray');return t?t.getBoundingClientRect().top+scrollY-520:scrollY+300})()", 700)
        R.mark('tray', '.tray'); pg.wait_for_timeout(1800); R.mark('end', '.tray'); R.stop(); b.close()
    if WHAT in ('recB', 'all'):
        b, ctx, pg = start(p, 2); dear_santa(pg)
        pg.evaluate("()=>document.querySelector('.chip.holc').click()"); pg.wait_for_timeout(1200)
        pg.evaluate("()=>[...document.querySelectorAll('button.no')].filter(b=>b.offsetParent)[0].click()"); pg.wait_for_timeout(1500)
        pg.evaluate("()=>[...document.querySelectorAll('button.yes')].filter(b=>b.offsetParent)[0].click()"); pg.wait_for_timeout(1500)
        pg.evaluate("()=>[...document.querySelectorAll('button.yes')].filter(b=>b.offsetParent)[0].click()"); pg.wait_for_timeout(1500)
        r = pg.evaluate("()=>{const bs=[...document.querySelectorAll('.pick1 button, .r3p button')].filter(b=>b.offsetParent);const f=bs.find(b=>/Festive/.test(b.innerText));(f||bs[0]).click();return bs.map(b=>b.innerText.slice(0,30))}"); print('suitor buttons', r); pg.wait_for_timeout(3000); fixlogo(pg)
        pg.evaluate("()=>{window._rq=['bb:Persimmon'];const pool=rackPool;window.rackPool=function(){const a=pool();return [...window._rq,...a.filter(x=>!window._rq.includes(x))]};try{rackPool=window.rackPool}catch(e){};renderRacks()}"); pg.wait_for_timeout(1500)
        pg.evaluate("()=>{const d=document.querySelector('.deck.r');window.scrollTo(0,d.getBoundingClientRect().top+scrollY-520)}"); pg.wait_for_timeout(3000); fixlogo(pg)
        pg.screenshot(path=f'{W}/dbg/racks0.png')
        R = Rec(ctx, pg, f'{W}/recB'); R.go(); pg.wait_for_timeout(1000); R.mark('racks', '.tilev.mband', '.deck.r')
        for i in range(3):
            pg.evaluate("()=>{const bs=[...document.querySelectorAll('.tilev.mband .zb button')].filter(b=>b.offsetParent);const plus=bs.find(b=>b.innerText.trim()==='+');plus&&plus.click()}"); R.mark(f'plus{i}', '.tilev.mband .zb'); pg.wait_for_timeout(750)
        pg.wait_for_timeout(500)
        for r, k in [('bb:Persimmon', 'yes'), ('bb:Basil', 'no'), (WALNUT, 'yes')]:
            pg.evaluate("(r)=>{window._rq=[r];renderRacks()}", r); pg.wait_for_timeout(1000); R.mark('show ' + r, '.deck.r', '.tilev.mband')
            pg.evaluate(f"()=>[...document.querySelectorAll('button.{k}')].filter(b=>b.offsetParent).pop().click()"); R.mark(k + ' ' + r); pg.wait_for_timeout(1400)
        pg.evaluate("()=>{S.rpick=S.rliked.slice(0,2);renderRacks()}"); pg.wait_for_timeout(900); R.mark('official')
        pg.evaluate("()=>[...document.querySelectorAll('button.go')].filter(b=>b.offsetParent).pop().click()"); pg.wait_for_timeout(2500)
        smooth(pg, "(()=>{const h=[...document.querySelectorAll('h2,h1,div')].find(e=>e.innerText&&e.innerText.trim().startsWith('Your match card')&&e.offsetParent);return h.getBoundingClientRect().top+scrollY-90})()", 900)
        R.mark('card'); pg.wait_for_timeout(2500); R.mark('end'); R.stop({'rliked': pg.evaluate('()=>S.rliked'), 'rpick': pg.evaluate('()=>S.rpick')})
        pg.evaluate("()=>{const b=[...document.querySelectorAll('button')].find(b=>b.offsetParent&&/Story/.test(b.innerText));if(b)b.click();else{S.fmt='story';renderAll()}}"); pg.wait_for_timeout(6000)
        src = pg.evaluate("()=>{const i=[...document.querySelectorAll('img')].filter(e=>e.offsetParent&&e.naturalHeight>=3000)[0];return i?i.src:(typeof cardURL!=='undefined'?cardURL:'')}")
        if src.startswith('data:'): open(f'{W}/recB/storycard.png', 'wb').write(base64.b64decode(src.split(',', 1)[1])); print('storycard ok')
        elif src.startswith('blob:'):
            d = pg.evaluate("async(u)=>{const ab=new Uint8Array(await (await fetch(u)).arrayBuffer());let s='';for(let i=0;i<ab.length;i+=32768)s+=String.fromCharCode.apply(null,ab.subarray(i,i+32768));return btoa(s)}", src)
            open(f'{W}/recB/storycard.png', 'wb').write(base64.b64decode(d)); print('storycard ok (blob)')
        else: print('no storycard', src[:60])
        b.close()
