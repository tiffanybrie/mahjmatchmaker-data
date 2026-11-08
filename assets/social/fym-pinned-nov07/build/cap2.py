"""Pinned reel v2 (Nov 8): 2x screen recordings from the CURRENT live FYM (website copy v118 @7817f04d, lib2.start).
Sunday tiles x Brownstone Bloom; racks Bam Bird Walnut + PLM Oak (X Teal Wood); Make it official; card views; shop list.
Usage: python3 cap2.py [rec0|recA|recB|all] -> /dev/shm/pin2/{rec0,recA,recP,recB}"""
import sys, os, json, time, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib2 import *
O = '/dev/shm/pin2'; os.makedirs(O + '/dbg', exist_ok=True)
WHAT = sys.argv[1] if len(sys.argv) > 1 else 'all'
BB = 'shop.andersruff.com/brownstone-bloom-mahjong-mat'; SONG = 'mahjandvine.com/chinoiserie-song-bird'
OZ = 'alb2:ozark-mah-jongg-carson-vintage'; MG = 'brittmillsdesign.com/knox-neoprene-mahjong-mat'
WAL = 'www.bambirdboutique.com/wooden-mahjong-rack-pusher-set'; OAK = 'peacelovemahjong.com/mahjong-racks-racks-pushers-set-of-4'
TEAL = 'www.bambirdboutique.com/wooden-mahjong-rack-pusher-set?v=52307844235573'
DECKQ = [BB, SONG, OZ, MG]
def smooth(pg, js_target, ms=700):
    pg.evaluate(f"""()=>{{const y=({js_target});const s=scrollY,d=y-s,t0=performance.now();function f(t){{const k=Math.min(1,(t-t0)/{ms});window.scrollTo(0,s+d*(k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2));if(k<1)requestAnimationFrame(f)}}requestAnimationFrame(f)}}"""); pg.wait_for_timeout(ms + 150)
def imgs(pg): pg.evaluate("()=>Promise.all([...document.images].filter(i=>i.offsetParent&&!i.complete).map(i=>new Promise(r=>{i.onload=i.onerror=r;setTimeout(r,8000)})))")
def btn(txt): return f"[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim().startsWith({json.dumps(txt)}))"
def rect(pg, js): return pg.evaluate(f"()=>{{const b={js};if(!b)return null;const r=b.getBoundingClientRect();return [r.left,r.top,r.width,r.height]}}")
SB = "[...document.querySelectorAll('button')].find(b=>b.offsetParent&&/\\nSunday\\nSunday Mahjong/.test(b.innerText))"
MATCH = "(()=>{const h=[...document.querySelectorAll('h1,h2,h3,div')].find(e=>e.offsetParent&&e.innerText&&e.innerText.trim().startsWith('Mat-ching'));return h.getBoundingClientRect().top+scrollY-70})()"
def queue(pg):
    pg.evaluate("""(q)=>{const md=matDeck0;window.matDeck0=function(){const a=md();return q.filter(x=>!S.seen[x])};try{matDeck0=window.matDeck0}catch(e){};renderAll()}""", DECKQ); pg.wait_for_timeout(1500); imgs(pg)
def sunday(pg):
    pg.evaluate(f"()=>{btn('Start with tiles')}.click()"); pg.wait_for_timeout(1200)
    pg.locator('input[placeholder*=Search]').first.click(); pg.keyboard.type('Sunday'); pg.wait_for_timeout(1500)
    pg.evaluate(f"()=>{SB}.click()"); pg.wait_for_timeout(4000); fixlogo(pg); queue(pg)
class Rec:
    def __init__(s, ctx, pg, out):
        s.pg, s.out = pg, out; os.makedirs(out + '/f', exist_ok=True); s.FR = []; s.marks = []; s.cdp = ctx.new_cdp_session(pg)
        def onf(e):
            n = len(s.FR); open(f'{out}/f/{n:05d}.jpg', 'wb').write(base64.b64decode(e['data'])); s.FR.append(e['metadata']['timestamp'])
            try: s.cdp.send('Page.screencastFrameAck', {'sessionId': e['sessionId']})
            except Exception: pass
        s.cdp.on('Page.screencastFrame', onf)
    def go(s): s.cdp.send('Page.startScreencast', {'format': 'jpeg', 'quality': 84, 'maxWidth': 780, 'maxHeight': 1688, 'everyNthFrame': 1}); s.T0 = time.time()
    def mark(s, n, extra=None):
        s.pg.wait_for_timeout(30); s.marks.append([n, round(time.time() - s.T0, 3), len(s.FR), extra or {}]); print(n, s.marks[-1][1:3], extra or '')
    def stop(s, extra=None):
        s.cdp.send('Page.stopScreencast'); s.pg.wait_for_timeout(300)
        json.dump({'frames': s.FR, 'marks': s.marks, **(extra or {})}, open(s.out + '/marks.json', 'w'), indent=1); print(len(s.FR), 'frames')
with sync_playwright() as p:
    if WHAT in ('rec0', 'all'):
        b, ctx, pg = start(p, 2); queue(pg)
        R = Rec(ctx, pg, f'{O}/rec0'); R.go(); pg.wait_for_timeout(900)
        R.mark('top', {'swt': rect(pg, btn('Start with tiles'))})
        pg.evaluate(f"()=>{btn('Start with tiles')}.click()"); R.mark('swttap'); pg.wait_for_timeout(1000)
        inp = pg.locator('input[placeholder*=Search]').first
        R.mark('search', {'inp': pg.evaluate("()=>{const i=[...document.querySelectorAll('input')].find(i=>i.offsetParent&&/Search/.test(i.placeholder));const r=i.getBoundingClientRect();return [r.left,r.top,r.width,r.height]}")})
        inp.click()
        for ch in 'Sunday': pg.keyboard.type(ch); pg.wait_for_timeout(110)
        pg.wait_for_timeout(900); imgs(pg)
        R.mark('result', {'sun': rect(pg, SB)}); pg.wait_for_timeout(500)
        pg.evaluate(f"()=>{SB}.click()"); R.mark('suntap'); pg.wait_for_timeout(2600); fixlogo(pg)
        smooth(pg, MATCH, 800); imgs(pg); pg.wait_for_timeout(400); R.mark('mats'); pg.wait_for_timeout(700); R.mark('end'); R.stop(); b.close()
    if WHAT in ('recA', 'all'):
        b, ctx, pg = start(p, 2); sunday(pg)
        pg.evaluate(f"()=>window.scrollTo(0,{MATCH})"); pg.wait_for_timeout(2500); fixlogo(pg); imgs(pg)
        R = Rec(ctx, pg, f'{O}/recA'); R.go(); pg.wait_for_timeout(1000)
        for nm, k in [('bb', 'yes'), ('song', 'no'), ('oz', 'yes'), ('mg', 'yes')]:
            R.mark('show ' + nm, {'btn': rect(pg, f"[...document.querySelectorAll('button.{k}')].filter(b=>b.offsetParent)[0]")}); pg.wait_for_timeout(450)
            pg.evaluate(f"()=>[...document.querySelectorAll('button.{k}')].filter(b=>b.offsetParent)[0].click()"); R.mark(k + ' ' + nm); pg.wait_for_timeout(1300); imgs(pg)
        R.mark('end'); R.stop(); b.close()
    if WHAT in ('recB', 'all'):
        b, ctx, pg = start(p, 2); sunday(pg)
        for k in ['yes', 'no', 'yes', 'yes']: pg.evaluate(f"()=>[...document.querySelectorAll('button.{k}')].filter(b=>b.offsetParent)[0].click()"); pg.wait_for_timeout(1400)
        pk = "[...document.querySelectorAll('.pick1 button')].find(b=>b.offsetParent&&/Brownstone/.test(b.innerText))"
        smooth(pg, f"(()=>{{const b={pk};return b.getBoundingClientRect().top+scrollY-560}})()", 300); imgs(pg); pg.wait_for_timeout(900)
        R0 = Rec(ctx, pg, f'{O}/recP'); R0.go(); pg.wait_for_timeout(900)
        R0.mark('pick0', {'tray': rect(pg, "document.querySelector('.pick1')"), 'bb': rect(pg, pk)}); pg.wait_for_timeout(700)
        pg.evaluate(f"()=>{pk}.click()"); R0.mark('picktap'); pg.wait_for_timeout(2200); fixlogo(pg); R0.mark('after'); R0.stop()
        pg.evaluate("(q)=>{window._rq=q;const pool=rackPool;window.rackPool=function(){const a=pool();return window._rq.slice()};try{rackPool=window.rackPool}catch(e){};renderRacks()}", [TEAL, WAL, OAK]); pg.wait_for_timeout(1500)
        pg.evaluate("()=>{const d=document.querySelector('.deck.r');window.scrollTo(0,d.getBoundingClientRect().top+scrollY-470)}"); pg.wait_for_timeout(2500); fixlogo(pg); imgs(pg)
        pg.screenshot(path=f'{O}/dbg/racks0.png')
        R = Rec(ctx, pg, f'{O}/recB'); R.go(); pg.wait_for_timeout(900)
        R.mark('racks', {'deck': rect(pg, "document.querySelector('.deck.r')"), 'mat': rect(pg, "[...document.querySelectorAll('img')].filter(i=>i.offsetParent&&i.getBoundingClientRect().top>0&&i.getBoundingClientRect().top<400).sort((a,b)=>b.width-a.width)[0]")})
        SEQ = [(TEAL, 'no'), (WAL, 'yes'), (OAK, 'yes')]
        for i, (r, k) in enumerate(SEQ):
            pg.evaluate("(q)=>{window._rq=q;renderRacks()}", [x for x, _ in SEQ[i:]]); pg.wait_for_timeout(700); imgs(pg); R.mark('show ' + r)
            pg.evaluate(f"()=>[...document.querySelectorAll('button.{k}')].filter(b=>b.offsetParent).pop().click()"); R.mark(k + ' ' + r); pg.wait_for_timeout(1300)
        pg.evaluate("()=>{if(!(S.rpick&&S.rpick.length)){S.rpick=S.rliked.slice(0,2);renderRacks()}}"); pg.wait_for_timeout(500)
        GO = "[...document.querySelectorAll('button.go')].filter(b=>b.offsetParent&&/official/i.test(b.innerText)).pop()"
        smooth(pg, f"(()=>{{const b={GO};return b.getBoundingClientRect().top+scrollY-600}})()", 700); R.mark('tray', {'go': rect(pg, GO)}); pg.wait_for_timeout(700)
        pg.evaluate(f"()=>{GO}.click()"); R.mark('official'); pg.wait_for_timeout(2400); imgs(pg)
        CARD = "(()=>{const h=[...document.querySelectorAll('h1,h2,h3,div')].find(e=>e.offsetParent&&e.innerText&&/^4\\s*Your match card/.test(e.innerText.trim())||e.offsetParent&&e.innerText&&e.innerText.trim().startsWith('Your match card'));return h?h.getBoundingClientRect().top+scrollY-40:scrollY+600})()"
        smooth(pg, CARD, 900); imgs(pg); R.mark('card', {'save': rect(pg, btn('Save image'))}); pg.wait_for_timeout(1500)
        for v in ['Close up', 'Story 9:16', 'Mood board', 'Post 4:5']:
            R.mark('v0 ' + v, {'b': rect(pg, btn(v))}); pg.evaluate(f"()=>{btn(v)}.click()"); pg.wait_for_timeout(250); R.mark('v ' + v); pg.wait_for_timeout(1700); imgs(pg)
        SH = "(()=>{const h=[...document.querySelectorAll('h2,h3,div,p')].find(e=>e.offsetParent&&e.innerText&&/^Shop your match/.test(e.innerText.trim()));return h?h.getBoundingClientRect().top+scrollY-120:scrollY+900})()"
        smooth(pg, SH, 1000); imgs(pg)
        R.mark('shop', {'rows': pg.evaluate("()=>[...document.querySelectorAll('a,button')].filter(b=>b.offsetParent&&/^(Shop|Sold out|Discount code)/.test(b.innerText.trim())).map(b=>{const r=b.getBoundingClientRect();return [b.innerText.trim(),r.left,r.top,r.width,r.height]})")})
        pg.wait_for_timeout(2500); R.mark('end'); R.stop({'rliked': pg.evaluate('()=>S.rliked'), 'rpick': pg.evaluate('()=>S.rpick')})
        b.close()
