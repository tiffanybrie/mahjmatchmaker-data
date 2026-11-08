import sys, json; sys.path.insert(0,'.')
from lib2 import *
D='/dev/shm/pin2/dbg'
BB='shop.andersruff.com/brownstone-bloom-mahjong-mat'; SONG='mahjandvine.com/chinoiserie-song-bird'; OZ='alb2:ozark-mah-jongg-carson-vintage'; MG='brittmillsdesign.com/knox-neoprene-mahjong-mat'
WAL='www.bambirdboutique.com/wooden-mahjong-rack-pusher-set'; OAK='peacelovemahjong.com/mahjong-racks-racks-pushers-set-of-4'; TEAL='www.bambirdboutique.com/wooden-mahjong-rack-pusher-set?v=52307844235573'
def ex(pg,js,a=None):
    try: return pg.evaluate(js,a) if a is not None else pg.evaluate(js)
    except Exception as e: return 'ERR '+str(e)[:300]
with sync_playwright() as p:
    b,ctx,pg=start(p,1)
    ex(pg,"()=>[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim().startsWith('Start with tiles')).click()"); pg.wait_for_timeout(1200)
    pg.locator('input[placeholder*=Search]').first.click(); pg.keyboard.type('Sunday'); pg.wait_for_timeout(1500)
    ex(pg,"()=>[...document.querySelectorAll('button')].find(b=>b.offsetParent&&/\\nSunday\\nSunday Mahjong/.test(b.innerText)).click()"); pg.wait_for_timeout(4000)
    ex(pg,"(q)=>{const md=matDeck0;window.matDeck0=function(){const a=md();return q.filter(x=>!S.seen[x])};try{matDeck0=window.matDeck0}catch(e){};renderAll()}",[BB,SONG,OZ,MG]); pg.wait_for_timeout(2000)
    for k in ['yes','no','yes','yes']:
        ex(pg,f"()=>[...document.querySelectorAll('button.{k}')].filter(b=>b.offsetParent)[0].click()"); pg.wait_for_timeout(1300)
    ex(pg,"()=>[...document.querySelectorAll('.pick1 button')].find(b=>b.offsetParent&&/Brownstone/.test(b.innerText)).click()"); pg.wait_for_timeout(2500)
    print(ex(pg,"(q)=>{window._rq=q;const pool=rackPool;window.rackPool=function(){const a=pool();return window._rq.slice()};try{rackPool=window.rackPool}catch(e){};renderRacks();return 'ok'}",[TEAL,WAL,OAK])); pg.wait_for_timeout(1500)
    pg.screenshot(path=D+'/r0.png')
    print('vis rack', ex(pg,"()=>{const d=document.querySelector('.deck.r');const r=d.getBoundingClientRect();return [r.top,r.height, d.innerText.slice(0,120)]}"))
    seq=[(TEAL,'no'),(WAL,'yes'),(OAK,'yes')]
    for i,(r,k) in enumerate(seq):
        ex(pg,"(q)=>{window._rq=q;renderRacks()}",[x for x,_ in seq[i:]]); pg.wait_for_timeout(800)
        ex(pg,f"()=>{{const d=document.querySelector('.deck.r');[...d.parentElement.parentElement.querySelectorAll('button.{k}')].filter(b=>b.offsetParent).pop().click()}}"); pg.wait_for_timeout(1300)
    print('rliked', ex(pg,"()=>[S.rliked,S.rpick]"))
    pg.screenshot(path=D+'/r1.png', full_page=True)
    print('go', ex(pg,"()=>[...document.querySelectorAll('button.go')].filter(b=>b.offsetParent).map(b=>[b.innerText.trim(),b.disabled])"))
    ex(pg,"()=>{S.rpick=S.rliked.slice(0,2);renderRacks()}"); pg.wait_for_timeout(800)
    print('go2', ex(pg,"()=>[...document.querySelectorAll('button.go')].filter(b=>b.offsetParent).map(b=>[b.innerText.trim(),b.disabled])"))
    ex(pg,"()=>[...document.querySelectorAll('button.go')].filter(b=>b.offsetParent&&/official/i.test(b.innerText)).pop().click()"); pg.wait_for_timeout(3500)
    pg.screenshot(path=D+'/c0.png', full_page=True)
    print('card btns', ex(pg,"()=>[...document.querySelectorAll('button,a')].filter(b=>b.offsetParent).map(b=>b.innerText.trim().replace(/\\n/g,' ')).filter(x=>x).slice(0,60)"))
    print('scrollH', ex(pg,"()=>document.documentElement.scrollHeight"))
    b.close()
