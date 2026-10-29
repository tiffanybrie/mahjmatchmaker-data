"""Launch reel REDO (Oct 29) capture: real FYM screens, 390px phone, for the storyboard + later render.
Sunday (Sunday Mahjong) tiles x Brownstone Bloom (Anders Ruff); racks Bam Bird Walnut + PLM Oak.
Serve the live artifact build on :8766 first. Output dir = argv[1]. Every swipe: <id>-b (before), <id>-card (top card cut out + bbox in meta), <id>-a (after, next card underneath)."""
import sys, os, json
from playwright.sync_api import sync_playwright
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True); DSF = int(os.environ.get('DSF', '2'))
K = dict(oz='alb2:ozark-mah-jongg-carson-vintage', mv='mahjandvine.com/chinoiserie-song-bird', og='mahjongrowandco.com/osmanthus-grove-mat',
         bb='shop.andersruff.com/brownstone-bloom-mahjong-mat', sp='sundaymahjong.com/sunday-premium-mahjong-mat')
RT = 'www.bambirdboutique.com/wooden-mahjong-rack-pusher-set?v=52307844235573'  # Bam Bird Teal Wood (✕: no teal in the mat)
RW = 'www.bambirdboutique.com/wooden-mahjong-rack-pusher-set'                  # Bam Bird Walnut (♥)
RO = 'peacelovemahjong.com/mahjong-racks-racks-pushers-set-of-4'               # PLM Oak (♥)
meta = {}
def shot(pg, n): pg.screenshot(path=f'{OUT}/{n}.png'); print('shot', n)
def view(pg, off=70): pg.evaluate(f"()=>{{const d=document.querySelector('.tilev.m');window.scrollTo(0,d.getBoundingClientRect().top+scrollY-{off})}}"); pg.wait_for_timeout(900)
def rview(pg, off=60): pg.evaluate(f"()=>{{const d=document.querySelector('.tilev.r')||document.querySelector('.deck.r');window.scrollTo(0,d.getBoundingClientRect().top+scrollY-{off})}}"); pg.wait_for_timeout(1100)
def bbox(pg, sel): return pg.evaluate(f"()=>{{const e=document.querySelector(`{sel}`);if(!e)return null;const q=e.getBoundingClientRect();return [q.left,q.top,q.width,q.height]}}")
def card(pg, sel, n):
    meta[n] = bbox(pg, f'{sel} .scard:not(.back)'); pg.locator(f'{sel} .scard:not(.back)').first.screenshot(path=f'{OUT}/{n}-card.png')
def front(pg, k): pg.evaluate("(k)=>{S.mfront=k;S.mfset=S.set;delete S.seen[k];renderAll()}", k); pg.wait_for_timeout(1400)
def press(pg, kind, last=False): pg.evaluate(f"()=>{{const a=[...document.querySelectorAll('button.{kind}')].filter(b=>b.offsetParent);(a.length?{ 'a[a.length-1]' if last else 'a[0]'}:null).click()}}"); pg.wait_for_timeout(1400)
def tray(pg, n):
    ok = pg.evaluate("()=>{const els=[...document.querySelectorAll('div,section')].filter(e=>e.offsetParent&&/SUITOR/i.test(e.innerText||'')&&e.getBoundingClientRect().height<140&&e.getBoundingClientRect().height>40);els.sort((a,b)=>a.getBoundingClientRect().height*a.getBoundingClientRect().width-b.getBoundingClientRect().height*b.getBoundingClientRect().width);const e=els[els.length-1];if(!e)return 0;document.querySelectorAll('[data-tray]').forEach(x=>x.removeAttribute('data-tray'));e.setAttribute('data-tray','1');return 1}")
    if ok: pg.locator('[data-tray]').first.screenshot(path=f'{OUT}/{n}.png'); print('tray', n)
def name(pg, sel): return pg.evaluate(f"()=>{{const e=document.querySelector('{sel} .scard:not(.back)');return e?e.innerText.replace(/\\s+/g,' ').slice(0,80):null}}")
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=DSF)
    pg.goto('http://localhost:8766/index.html?tour=off'); pg.wait_for_timeout(5000); pg.add_style_tag(content='.swh{display:none!important}')
    shot(pg, '01-home')
    pg.locator('input[placeholder*=Search]').first.click(); pg.keyboard.type('Sunday'); pg.wait_for_timeout(1200); shot(pg, '02-search')
    pg.evaluate("()=>[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim().startsWith('Sunday')&&!b.innerText.includes('Blues')).click()"); pg.wait_for_timeout(3000)
    pg.evaluate("()=>window.scrollTo(0,0)"); pg.wait_for_timeout(700); shot(pg, '03-tiles-chosen')
    # --- mats: swipe with the tile strip + mat in one view
    seq = [('s0', K['oz'], 'yes', K['mv']), ('s1', K['mv'], 'no', K['sp'])]
    for sid, k, kind, nxt in seq:
        front(pg, k); view(pg); shot(pg, f'{sid}-b'); card(pg, '.deck.m', sid); meta[sid + '-name'] = name(pg, '.deck.m')
        meta[sid + '-btn'] = bbox(pg, f".deck.m ~ * button.{kind}") or pg.evaluate(f"()=>{{const q=[...document.querySelectorAll('button.{kind}')].find(b=>b.offsetParent).getBoundingClientRect();return [q.left,q.top,q.width,q.height]}}")
        press(pg, kind)
        tray(pg, f'tray-{sid}')
        if nxt: front(pg, nxt)
        view(pg); shot(pg, f'{sid}-a')
    # brand menu (menu change)
    pg.evaluate("()=>{const b=[...document.querySelectorAll('button')].find(b=>b.offsetParent&&/^Brand/.test(b.innerText.trim()));b&&b.click()}"); pg.wait_for_timeout(1000); shot(pg, '20-brand-menu')
    pg.evaluate("()=>{const b=[...document.querySelectorAll('.sheet button.x')].find(b=>b.offsetParent);b&&b.click()}"); pg.wait_for_timeout(800)
    pg.evaluate("()=>{S.f.m.brand='';renderAll()}"); pg.wait_for_timeout(900)
    # colour filter: tap Green, deck changes
    view(pg); pg.evaluate("()=>{const b=[...document.querySelectorAll('button.dot')].find(b=>b.title==='All colors');b.click()}"); pg.wait_for_timeout(900); view(pg)
    meta['n_all'] = pg.evaluate("()=>matDeck().length")
    pg.evaluate("()=>{const e=document.querySelector('button.dot[title=\"All colors\"]');e&&e.click()}"); pg.wait_for_timeout(900); view(pg)
    shot(pg, '21-colour-open'); meta['colour-open-dots'] = pg.evaluate("()=>[...document.querySelectorAll('button.dot')].filter(b=>b.offsetParent).map(b=>{const q=b.getBoundingClientRect();return [b.title,q.left+q.width/2,q.top+q.height/2]})")
    pg.evaluate("()=>{const b=[...document.querySelectorAll('button.dot')].find(b=>b.title==='Green');b.scrollIntoView({block:'nearest',inline:'center'})}"); view(pg)
    meta['green'] = pg.evaluate("()=>{const q=[...document.querySelectorAll('button.dot')].find(b=>b.title==='Green').getBoundingClientRect();return [q.left+q.width/2,q.top+q.height/2]}")
    shot(pg, '22-colour-before'); pg.evaluate("()=>[...document.querySelectorAll('button.dot')].find(b=>b.title==='Green').click()"); pg.wait_for_timeout(1300)
    meta['n_green'] = pg.evaluate("()=>matDeck().length"); front(pg, K['og']); view(pg); shot(pg, '23-colour-green')
    for sid, k, kind, nxt in [('s2', K['og'], 'no', K['bb'])]:
        front(pg, k); view(pg); shot(pg, f'{sid}-b'); card(pg, '.deck.m', sid); meta[sid + '-name'] = name(pg, '.deck.m')
        press(pg, kind); front(pg, nxt); view(pg); shot(pg, f'{sid}-a')
    # Brownstone: zoom in on the deck card (+ +), drag-pan, zoom out (−), then ♥
    front(pg, K['bb']); view(pg); shot(pg, 'mz0')
    ZB = lambda d: f"()=>{{const b=[...document.querySelectorAll('.deck.m .scard:not(.back) button, .deck.m button')].filter(b=>b.offsetParent&&b.innerText.trim()==='{d}')[0];if(b){{const q=b.getBoundingClientRect();b.click();return [q.left+q.width/2,q.top+q.height/2]}}return null}}"
    meta['mz-plus'] = pg.evaluate(ZB('+')); pg.wait_for_timeout(800); shot(pg, 'mz1'); pg.evaluate(ZB('+')); pg.wait_for_timeout(800); shot(pg, 'mz2')
    cb = bbox(pg, '.deck.m .scard:not(.back)'); cx, cy = cb[0] + cb[2] / 2, cb[1] + cb[3] * .4
    pg.evaluate('()=>getSelection().removeAllRanges()'); pg.mouse.move(cx, cy); pg.mouse.down(); pg.mouse.move(cx + 90, cy + 70, steps=10); pg.mouse.up(); pg.wait_for_timeout(800); shot(pg, 'mz3')
    meta['mz-minus'] = pg.evaluate(ZB('−')); pg.wait_for_timeout(800); pg.evaluate(ZB('−')); pg.wait_for_timeout(900); shot(pg, 'mz4')
    sid = 's3'; view(pg); shot(pg, f'{sid}-b'); card(pg, '.deck.m', sid); meta[sid + '-name'] = name(pg, '.deck.m'); press(pg, 'yes'); tray(pg, 'tray-s3'); view(pg); shot(pg, f'{sid}-a')
    # suitors row
    pg.evaluate("()=>{const e=[...document.querySelectorAll('*')].find(e=>e.offsetParent&&/^SUITORS$|^Suitors$/i.test((e.innerText||'').trim()));if(e)window.scrollTo(0,e.getBoundingClientRect().top+scrollY-520)}"); pg.wait_for_timeout(1000); shot(pg, '30-suitors')
    meta['liked'] = pg.evaluate("()=>S.liked.map(k=>M[k]?M[k].n:k)")
    pg.evaluate("()=>{const e=document.querySelector('.r3p');if(e)window.scrollTo(0,e.getBoundingClientRect().top+scrollY-200)}"); pg.wait_for_timeout(900); shot(pg, '31-pick')
    pg.evaluate("()=>{const b=[...document.querySelectorAll('.r3p .pick1 button, button')].filter(e=>e.offsetParent&&e.innerText.includes('Brownstone')).pop();b&&b.click()}"); pg.wait_for_timeout(2500)
    # racks: force the pool order, + + + zoom ON the mat, drag-pan
    pg.evaluate("(r)=>{const pool=rackPool;window.rackPool=function(){const a=pool();return [...r.filter(x=>R[x]),...a.filter(x=>!r.includes(x))]};try{rackPool=window.rackPool}catch(e){};S.f.r.her=false;S.rseen=[];renderRacks();}", [RT, RW, RO]); pg.wait_for_timeout(2500)
    pg.evaluate("()=>{const d=document.querySelector('.deck.r');window.scrollTo(0,d.getBoundingClientRect().top+scrollY-420)}"); pg.wait_for_timeout(1500)
    PL = lambda d: f"()=>[...document.querySelectorAll('button')].filter(b=>b.offsetParent&&b.innerText.trim()==='{d}'&&b.getBoundingClientRect().top>40&&b.getBoundingClientRect().top<420)[0]"
    meta['rz'] = pg.evaluate(f"()=>{{const b=({PL('+')})();if(!b)return null;const q=b.getBoundingClientRect();return [q.left+q.width/2,q.top+q.height/2]}}")
    meta['rzm'] = pg.evaluate(f"()=>{{const b=({PL('−')})();if(!b)return null;const q=b.getBoundingClientRect();return [q.left+q.width/2,q.top+q.height/2]}}")
    for i in range(4):
        shot(pg, f'40-rz{i}')
        if i < 3: pg.evaluate(f"()=>{{const b=({PL('+')})();b&&b.click()}}"); pg.wait_for_timeout(900)
    pr = pg.evaluate("()=>{const e=[...document.querySelectorAll('img')].filter(i=>i.offsetParent&&i.getBoundingClientRect().top<330&&i.getBoundingClientRect().bottom>80&&i.getBoundingClientRect().width>200)[0];if(!e)return null;const q=e.getBoundingClientRect();return [q.left+q.width/2,Math.max(q.top,120)+80]}")
    meta['pan'] = pr
    if pr: pg.mouse.move(pr[0], pr[1]); pg.mouse.down(); pg.mouse.move(pr[0] - 120, pr[1] + 50, steps=10); pg.mouse.up(); pg.wait_for_timeout(900)
    shot(pg, '40-rz4')
    # rack type chips: tap Wood
    WC = "()=>[...document.querySelectorAll('button.chip')].find(b=>b.offsetParent&&b.innerText.trim()==='Wood')"
    pg.evaluate(f"()=>{{const b=({WC})();b&&b.scrollIntoView({{block:'nearest',inline:'center'}})}}"); pg.evaluate("()=>{const d=document.querySelector('.deck.r');window.scrollTo(0,d.getBoundingClientRect().top+scrollY-420)}"); pg.wait_for_timeout(900)
    meta['rchips'] = pg.evaluate("()=>[...document.querySelectorAll('button.chip')].filter(b=>b.offsetParent&&b.getBoundingClientRect().top>0&&b.getBoundingClientRect().top<600).map(b=>{const q=b.getBoundingClientRect();return [b.innerText.trim(),Math.round(q.left+q.width/2),Math.round(q.top+q.height/2)]})")
    meta['woodchip'] = pg.evaluate(f"()=>{{const b=({WC})();if(!b)return null;const q=b.getBoundingClientRect();return [q.left+q.width/2,q.top+q.height/2]}}")
    shot(pg, '45-chips'); pg.evaluate(f"()=>{{const b=({WC})();b&&b.click()}}"); pg.wait_for_timeout(1400)
    pg.evaluate("(r)=>{const od=rackDeck;const nd=function(){const a=od();const seen=S.rseen||{};const m=r.filter(x=>R[x]&&!seen[x]&&!(S.rliked||[]).includes(x));return [...m,...a.filter(x=>!r.includes(x))]};window.rackDeck=nd;try{rackDeck=nd}catch(e){};renderRacks()}", [RT, RW, RO]); pg.wait_for_timeout(1400)
    pg.evaluate("()=>{const d=document.querySelector('.deck.r');window.scrollTo(0,d.getBoundingClientRect().top+scrollY-420)}"); pg.wait_for_timeout(900); shot(pg, '46-wood-on')
    meta['rdeck_wood'] = pg.evaluate("()=>typeof rackDeck==='function'?rackDeck().slice(0,5).map(k=>R[k].n):null")
    for j, (rk, kind) in enumerate([(RT, 'no'), (RW, 'yes'), (RO, 'yes')]):
        meta[f'r{j}-name'] = name(pg, '.deck.r'); shot(pg, f'r{j}-b'); card(pg, '.deck.r', f'r{j}')
        press(pg, kind, last=True); pg.wait_for_timeout(300); shot(pg, f'r{j}-a')
    meta['rliked'] = pg.evaluate("()=>S.rliked.map(k=>R[k]?R[k].n:k)")
    # zoom back OUT on the mat (− −) for context
    for i in range(3): pg.evaluate(f"()=>{{const b=({PL('−')})();b&&b.click()}}"); pg.wait_for_timeout(700)
    shot(pg, '47-zoom-out')
    pg.evaluate("()=>{S.rpick=S.rliked.slice(0,2);renderRacks()}"); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{const d=document.querySelector('.deck.r');window.scrollTo(0,d.getBoundingClientRect().top+scrollY-60)}"); pg.wait_for_timeout(1000); shot(pg, '50-slots')
    pg.evaluate("()=>{const b=[...document.querySelectorAll('button.go')].filter(b=>b.offsetParent&&b.innerText.includes('official')).pop();if(b)window.scrollTo(0,b.getBoundingClientRect().top+scrollY-500)}"); pg.wait_for_timeout(800); shot(pg, '51-official')
    pg.evaluate("()=>[...document.querySelectorAll('button.go')].filter(b=>b.offsetParent&&b.innerText.includes('official')).pop().click()"); pg.wait_for_timeout(5000)
    pg.evaluate("()=>{const b=[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim().startsWith('Story'));b&&b.click()}"); pg.wait_for_timeout(3000)
    pg.evaluate("()=>{const b=[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim()=='Mood board');b&&window.scrollTo(0,b.getBoundingClientRect().top+scrollY-75)}"); pg.wait_for_timeout(2500); shot(pg, '60-card-screen')
    import base64
    du = pg.evaluate("async()=>{const im=[...document.querySelectorAll('img')].filter(i=>i.offsetParent).sort((a,b)=>b.naturalWidth*b.naturalHeight-a.naturalWidth*a.naturalHeight)[0];if(!im)return null;const r=await fetch(im.src);const bl=await r.blob();return await new Promise(res=>{const f=new FileReader();f.onload=()=>res(f.result);f.readAsDataURL(bl)})}")
    if du: open(f'{OUT}/61-card-story-full.png', 'wb').write(base64.b64decode(du.split(',')[1])); print('full card saved')
    pg.evaluate("()=>{const h=[...document.querySelectorAll('h3')].find(h=>h.innerText.includes('Shop'));h&&window.scrollTo(0,h.getBoundingClientRect().top+scrollY-140)}"); pg.wait_for_timeout(1500); shot(pg, '70-shop')
    meta['shop_text'] = pg.evaluate("()=>{const h=[...document.querySelectorAll('h3')].find(h=>h.innerText.includes('Shop'));return h?h.parentElement.innerText.slice(0,900):null}")
    json.dump(meta, open(f'{OUT}/meta.json', 'w'), indent=1); b.close()
