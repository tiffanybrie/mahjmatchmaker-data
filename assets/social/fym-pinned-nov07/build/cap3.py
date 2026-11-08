"""Pinned reel v3 (Nov 8, FEEDBACK-nov08-v3.md): 2x screen recordings from the CURRENT live FYM (website copy v118 @7817f04d, lib3.start).
rec0 = home -> type Sunday SLOWLY (280ms/char) -> tap -> Mat-ching.  Per version V in A|B:
 S<V> = view switcher (Up close -> Aerial -> Table [-> Up close for A]) then swipes: heart Brownstone Bloom, X Songbird, heart Carson Vintage, heart Knox
        (B swipes in Table view). P<V> = pick Brownstone. K<V> = racks (YES only: Bam Bird Walnut, PLM Oak) with the rack filters
        (Wood tone + brown colour dot), Make it official, card Story close up -> Story mood board, shop list.
Usage: python3 cap3.py rec0|A|B|all  -> /dev/shm/pin3/{rec0,SA,PA,KA,SB,PB,KB}"""
import sys, os, json, time, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib3 import *
O = '/dev/shm/pin3'; os.makedirs(O + '/dbg', exist_ok=True)
WHAT = sys.argv[1] if len(sys.argv) > 1 else 'all'
BB = 'shop.andersruff.com/brownstone-bloom-mahjong-mat'; SONG = 'mahjandvine.com/chinoiserie-song-bird'
OZ = 'alb2:ozark-mah-jongg-carson-vintage'; MG = 'brittmillsdesign.com/knox-neoprene-mahjong-mat'
WAL = 'www.bambirdboutique.com/wooden-mahjong-rack-pusher-set'; OAK = 'peacelovemahjong.com/mahjong-racks-racks-pushers-set-of-4'
DECKQ = [BB, SONG, OZ, MG]
def smooth(pg, js_target, ms=700):
    pg.evaluate(f"""()=>{{const y=({js_target});const s=scrollY,d=y-s,t0=performance.now();function f(t){{const k=Math.min(1,(t-t0)/{ms});window.scrollTo(0,s+d*(k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2));if(k<1)requestAnimationFrame(f)}}requestAnimationFrame(f)}}"""); pg.wait_for_timeout(ms + 150)
def imgs(pg): pg.evaluate("()=>Promise.all([...document.images].filter(i=>i.offsetParent&&!i.complete).map(i=>new Promise(r=>{i.onload=i.onerror=r;setTimeout(r,8000)})))")
def btn(txt): return f"[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim().startsWith({json.dumps(txt)}))"
def rect(pg, js): return pg.evaluate(f"()=>{{const b={js};if(!b)return null;const r=b.getBoundingClientRect();return [r.left,r.top,r.width,r.height]}}")
def mode(m): return f"[...document.querySelectorAll('[data-mode={m}]')].find(b=>b.offsetParent)"
SB = "[...document.querySelectorAll('button')].find(b=>b.offsetParent&&/\\nSunday\\nSunday Mahjong/.test(b.innerText))"
MATCH = "(()=>{const h=[...document.querySelectorAll('h1,h2,h3,div')].find(e=>e.offsetParent&&e.innerText&&e.innerText.trim().startsWith('Mat-ching'));return h.getBoundingClientRect().top+scrollY-70})()"
CARDR = "[...document.querySelectorAll('.card,.deck .c,.deck>div')].filter(e=>e.offsetParent).sort((a,b)=>b.getBoundingClientRect().width*b.getBoundingClientRect().height-a.getBoundingClientRect().width*a.getBoundingClientRect().height)[0]"
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
    def go(s): s.cdp.send('Page.startScreencast', {'format': 'jpeg', 'quality': 84, 'maxWidth': 780, 'maxHeight': 1688, 'everyNthFrame': 1}); s.T0 = time.time(); s.W0 = None
    def mark(s, n, extra=None):
        s.pg.wait_for_timeout(30); s.marks.append([n, round(time.time() - s.T0, 3), len(s.FR), extra or {}]); print(n, s.marks[-1][1:3], extra or '')
    def stop(s, extra=None):
        s.cdp.send('Page.stopScreencast'); s.pg.wait_for_timeout(300)
        json.dump({'frames': s.FR, 'marks': s.marks, **(extra or {})}, open(s.out + '/marks.json', 'w'), indent=1); print(s.out, len(s.FR), 'frames')
def swipe(pg, R, nm, k):
    R.mark('show ' + nm, {'btn': rect(pg, f"[...document.querySelectorAll('button.{k}')].filter(b=>b.offsetParent)[0]")}); pg.wait_for_timeout(420)
    pg.evaluate(f"()=>[...document.querySelectorAll('button.{k}')].filter(b=>b.offsetParent)[0].click()"); R.mark(k + ' ' + nm); pg.wait_for_timeout(1250); imgs(pg)
def version(p, V):
    b, ctx, pg = start(p, 2); sunday(pg)
    pg.evaluate(f"()=>window.scrollTo(0,{MATCH}+60)"); pg.wait_for_timeout(2500); fixlogo(pg); imgs(pg)
    pg.screenshot(path=f'{O}/dbg/S{V}0.png')
    R = Rec(ctx, pg, f'{O}/S{V}'); R.go(); pg.wait_for_timeout(900)
    R.mark('show', {'sw': rect(pg, mode('aerial')), 'close': rect(pg, mode('close')), 'table': rect(pg, mode('table'))}); pg.wait_for_timeout(700)
    pg.evaluate(f"()=>{mode('aerial')}.click()"); R.mark('aerial'); pg.wait_for_timeout(500); imgs(pg); pg.wait_for_timeout(900)
    R.mark('aerial2', {'table': rect(pg, mode('table'))})
    pg.evaluate(f"()=>{mode('table')}.click()"); R.mark('table'); pg.wait_for_timeout(500); imgs(pg); pg.wait_for_timeout(1100)
    R.mark('table2', {'close': rect(pg, mode('close')), 'yes': rect(pg, "[...document.querySelectorAll('button.yes')].filter(b=>b.offsetParent)[0]")})
    if V == 'A':
        pg.evaluate(f"()=>{mode('close')}.click()"); R.mark('close'); pg.wait_for_timeout(400); pg.evaluate(f"()=>window.scrollTo(0,{MATCH}+60)"); imgs(pg); pg.wait_for_timeout(900); R.mark('closed')
    for nm, k in [('bb', 'yes'), ('song', 'no'), ('oz', 'yes'), ('mg', 'yes')]: swipe(pg, R, nm, k)
    R.mark('end'); R.stop(); pg.screenshot(path=f'{O}/dbg/S{V}1.png')
    pk = "[...document.querySelectorAll('.pick1 button')].find(b=>b.offsetParent&&/Brownstone/.test(b.innerText))"
    smooth(pg, f"(()=>{{const b={pk};return b.getBoundingClientRect().top+scrollY-560}})()", 300); imgs(pg); pg.wait_for_timeout(900)
    R0 = Rec(ctx, pg, f'{O}/P{V}'); R0.go(); pg.wait_for_timeout(900)
    R0.mark('pick0', {'tray': rect(pg, "document.querySelector('.pick1')"), 'bb': rect(pg, pk)}); pg.wait_for_timeout(700)
    pg.evaluate(f"()=>{pk}.click()"); R0.mark('picktap'); pg.wait_for_timeout(2200); fixlogo(pg); R0.mark('after'); R0.stop()
    pg.evaluate("(q)=>{window._rq=q;const pool=rackPool;window.rackPool=function(){const a=pool();return window._rq.concat(a.filter(x=>!window._rq.includes(x)))};try{rackPool=window.rackPool}catch(e){};renderRacks()}", [WAL, OAK]); pg.wait_for_timeout(1500)
    DECK = "(()=>{const d=document.querySelector('.deck.r');return d.getBoundingClientRect().top+scrollY-%d})()"
    off = 470 if V == 'A' else 120
    pg.evaluate(f"()=>window.scrollTo(0,{DECK % off})"); pg.wait_for_timeout(2500); fixlogo(pg); imgs(pg); pg.wait_for_timeout(1500)
    pg.screenshot(path=f'{O}/dbg/K{V}0.png')
    R = Rec(ctx, pg, f'{O}/K{V}'); R.go(); pg.wait_for_timeout(900)
    R.mark('racks', {'deck': rect(pg, "document.querySelector('.deck.r')"), 'yes': rect(pg, "[...document.querySelectorAll('button.yes')].filter(b=>b.offsetParent).pop()")}); pg.wait_for_timeout(1400)
    WOOD = "[...document.querySelectorAll('button.chip.finc')].find(b=>b.offsetParent&&/Wood tone/.test(b.innerText))"
    smooth(pg, f"(()=>{{const b={WOOD};return b.getBoundingClientRect().top+scrollY-300}})()", 700)
    R.mark('filters', {'wood': rect(pg, WOOD), 'dots': pg.evaluate("()=>[...document.querySelectorAll('button.dot')].filter(b=>b.offsetParent).map(b=>{const r=b.getBoundingClientRect();return [b.title||b.getAttribute('aria-label')||b.style.background,r.left,r.top,r.width,r.height]})")}); pg.wait_for_timeout(500)
    BROWN = "[...document.querySelectorAll('button.dot')].filter(b=>b.offsetParent&&b.getBoundingClientRect().top>0).find(b=>/^Brown/i.test(b.title||b.getAttribute('aria-label')||''))"
    R.mark('brown0', {'brown': rect(pg, BROWN)}); pg.evaluate(f"()=>{{const b={BROWN};if(b)b.click()}}"); R.mark('brown'); pg.wait_for_timeout(1100)
    R.mark('wood0', {'wood': rect(pg, WOOD)}); pg.evaluate(f"()=>{WOOD}.click()"); R.mark('wood'); pg.wait_for_timeout(1100)
    R.mark('woodd', {'deck': pg.evaluate("()=>(document.querySelector('.deck.r')||{}).innerText||''")[:80]})
    pg.evaluate("()=>{window._rq=window._rq;renderRacks()}"); pg.wait_for_timeout(300); imgs(pg)
    smooth(pg, DECK % off, 700); imgs(pg); R.mark('back', {'yes': rect(pg, "[...document.querySelectorAll('button.yes')].filter(b=>b.offsetParent).pop()")}); pg.wait_for_timeout(700)
    for i, r in enumerate([WAL, OAK]):
        pg.evaluate("(q)=>{window._rq=q;renderRacks()}", [WAL, OAK][i:]); pg.wait_for_timeout(500); imgs(pg); R.mark('show ' + r)
        pg.wait_for_timeout(300); pg.evaluate("()=>[...document.querySelectorAll('button.yes')].filter(b=>b.offsetParent).pop().click()"); R.mark('yes ' + r); pg.wait_for_timeout(1300)
    pg.evaluate("()=>{if(!(S.rpick&&S.rpick.length)){S.rpick=S.rliked.slice(0,2);renderRacks()}}"); pg.wait_for_timeout(500)
    GO = "[...document.querySelectorAll('button.go')].filter(b=>b.offsetParent&&/official/i.test(b.innerText)).pop()"
    smooth(pg, f"(()=>{{const b={GO};return b.getBoundingClientRect().top+scrollY-600}})()", 700); R.mark('tray', {'go': rect(pg, GO)}); pg.wait_for_timeout(700)
    pg.evaluate(f"()=>{GO}.click()"); R.mark('official'); pg.wait_for_timeout(2400); imgs(pg)
    CARD = "(()=>{const h=[...document.querySelectorAll('h1,h2,h3,div')].find(e=>e.offsetParent&&e.innerText&&/^4\\s*Your match card/.test(e.innerText.trim())||e.offsetParent&&e.innerText&&e.innerText.trim().startsWith('Your match card'));return h?h.getBoundingClientRect().top+scrollY-40:scrollY+600})()"
    smooth(pg, CARD, 900)
    pg.wait_for_function("()=>!/Dressing up your match/.test(document.body.innerText)", timeout=20000); pg.wait_for_timeout(500)
    pg.evaluate(f"()=>{{const b={btn('Story 9:16')};if(b)b.click()}}"); pg.wait_for_timeout(600)
    pg.evaluate(f"()=>{{const b={btn('Close up')};if(b)b.click()}}"); pg.wait_for_timeout(600)
    pg.wait_for_function("()=>!/Dressing up your match/.test(document.body.innerText)", timeout=20000); imgs(pg); pg.wait_for_timeout(1200)
    pg.screenshot(path=f'{O}/dbg/C{V}close.png')
    R.mark('card', {'save': rect(pg, btn('Save image')), 'img': rect(pg, "[...document.querySelectorAll('img,canvas')].filter(i=>i.offsetParent&&i.getBoundingClientRect().top>-50&&i.getBoundingClientRect().top<844).sort((a,b)=>b.getBoundingClientRect().width*b.getBoundingClientRect().height-a.getBoundingClientRect().width*a.getBoundingClientRect().height)[0]")}); pg.wait_for_timeout(1500)
    R.mark('v0 Mood board', {'b': rect(pg, btn('Mood board'))}); pg.evaluate(f"()=>{btn('Mood board')}.click()"); pg.wait_for_timeout(250); R.mark('v Mood board'); pg.wait_for_timeout(600); pg.wait_for_function("()=>!/Dressing up your match/.test(document.body.innerText)", timeout=20000); imgs(pg); pg.wait_for_timeout(1500); pg.screenshot(path=f'{O}/dbg/C{V}mood.png')
    R.mark('mood2')
    SH = "(()=>{const h=[...document.querySelectorAll('h2,h3,div,p')].find(e=>e.offsetParent&&e.innerText&&/^Shop your match/.test(e.innerText.trim()));return h?h.getBoundingClientRect().top+scrollY-120:scrollY+900})()"
    smooth(pg, SH, 1000); imgs(pg)
    R.mark('shop', {'rows': pg.evaluate("()=>[...document.querySelectorAll('a,button')].filter(b=>b.offsetParent&&/^(Shop|Sold out|Discount code)/.test(b.innerText.trim())).map(b=>{const r=b.getBoundingClientRect();return [b.innerText.trim(),r.left,r.top,r.width,r.height]})")})
    pg.wait_for_timeout(2500); R.mark('end'); R.stop({'rliked': pg.evaluate('()=>S.rliked'), 'rpick': pg.evaluate('()=>S.rpick')})
    b.close()
with sync_playwright() as p:
    if WHAT in ('rec0', 'all'):
        b, ctx, pg = start(p, 2); queue(pg)
        R = Rec(ctx, pg, f'{O}/rec0'); R.go(); pg.wait_for_timeout(900)
        R.mark('top', {'swt': rect(pg, btn('Start with tiles'))})
        pg.evaluate(f"()=>{btn('Start with tiles')}.click()"); R.mark('swttap'); pg.wait_for_timeout(1000)
        inp = pg.locator('input[placeholder*=Search]').first
        R.mark('search', {'inp': pg.evaluate("()=>{const i=[...document.querySelectorAll('input')].find(i=>i.offsetParent&&/Search/.test(i.placeholder));const r=i.getBoundingClientRect();return [r.left,r.top,r.width,r.height]}")})
        inp.click(); pg.wait_for_timeout(400); R.mark('type0')
        for ch in 'Sunday': pg.keyboard.type(ch); pg.wait_for_timeout(280)
        R.mark('typed'); pg.wait_for_timeout(900); imgs(pg)
        R.mark('result', {'sun': rect(pg, SB)}); pg.wait_for_timeout(600)
        pg.evaluate(f"()=>{SB}.click()"); R.mark('suntap'); pg.wait_for_timeout(2600); fixlogo(pg)
        smooth(pg, "(" + MATCH + "+60)", 800); imgs(pg); pg.wait_for_timeout(400); R.mark('mats'); pg.wait_for_timeout(700); R.mark('end'); R.stop(); b.close()
    for V in 'AB':
        if WHAT in (V, 'all'): version(p, V)
