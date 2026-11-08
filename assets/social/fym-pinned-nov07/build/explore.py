import sys, json; sys.path.insert(0,'.')
from lib2 import *
D='/dev/shm/pin2/dbg'
BB='shop.andersruff.com/brownstone-bloom-mahjong-mat'; SONG='mahjandvine.com/chinoiserie-song-bird'; OZ='alb2:ozark-mah-jongg-carson-vintage'; MG='brittmillsdesign.com/knox-neoprene-mahjong-mat'
WAL='www.bambirdboutique.com/wooden-mahjong-rack-pusher-set'; OAK='peacelovemahjong.com/mahjong-racks-racks-pushers-set-of-4'; TEAL='www.bambirdboutique.com/wooden-mahjong-rack-pusher-set?v=52307844235573'
def ex(pg,js):
    try: return pg.evaluate(js)
    except Exception as e: return 'ERR '+str(e)[:200]
with sync_playwright() as p:
    b,ctx,pg=start(p,1)
    print('fns', ex(pg,"()=>[typeof matDeck0,typeof rackPool,typeof renderRacks,typeof renderAll,typeof S]"))
    print('keys', ex(pg, f"()=>[{json.dumps([BB,SONG,OZ,MG,WAL,OAK,TEAL])}].flat().map(k=>[k, !!(D.mats&&D.mats[k]) , !!(D.racks&&D.racks[k])])"))
    pg.evaluate("()=>[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim().startsWith('Start with tiles')).click()"); pg.wait_for_timeout(1200)
    pg.locator('input[placeholder*=Search]').first.click(); pg.keyboard.type('Sunday'); pg.wait_for_timeout(1500)
    print('results', ex(pg,"()=>[...document.querySelectorAll('button')].filter(b=>b.offsetParent&&/Sunday/.test(b.innerText)).map(b=>b.innerText.replace(/\\n/g,' | ')).slice(0,5)"))
    pg.screenshot(path=D+'/s1.png')
    ex(pg,"()=>[...document.querySelectorAll('button')].find(b=>b.offsetParent&&/\\nSunday\\nSunday Mahjong/.test(b.innerText)).click()"); pg.wait_for_timeout(4000)
    print('q', ex(pg, "(q)=>{const md=matDeck0;window.matDeck0=function(){const a=md();return q.filter(x=>!S.seen[x])};try{matDeck0=window.matDeck0}catch(e){};renderAll();return 'ok'}".replace('(q)','()').replace('q.filter',json.dumps([BB,SONG,OZ,MG])+'.filter')))
    pg.wait_for_timeout(2000)
    pg.screenshot(path=D+'/s2.png', full_page=True)
    print('yesno', ex(pg,"()=>[...document.querySelectorAll('button.yes,button.no')].filter(b=>b.offsetParent).length"))
    for k in ['yes','no','yes','yes']:
        ex(pg,f"()=>[...document.querySelectorAll('button.{k}')].filter(b=>b.offsetParent)[0].click()"); pg.wait_for_timeout(1500)
    pg.screenshot(path=D+'/s3.png', full_page=True)
    print('pick1', ex(pg,"()=>[...document.querySelectorAll('.pick1 button')].filter(b=>b.offsetParent).map(b=>b.innerText.slice(0,40))"))
    ex(pg,"()=>[...document.querySelectorAll('.pick1 button')].find(b=>b.offsetParent&&/Brownstone/.test(b.innerText)).click()"); pg.wait_for_timeout(2500)
    pg.screenshot(path=D+'/s4.png', full_page=True)
    print('rack ui', ex(pg,"()=>({deckr:!!document.querySelector('.deck.r'), zb:[...document.querySelectorAll('.zb button')].filter(b=>b.offsetParent).map(b=>b.innerText.trim()), chips:[...document.querySelectorAll('button')].filter(b=>b.offsetParent&&/Tiffany|Wood|Acrylic|picks/.test(b.innerText)).map(b=>b.innerText.trim()).slice(0,12), go:[...document.querySelectorAll('button.go')].filter(b=>b.offsetParent).map(b=>b.innerText.trim())})"))
    b.close()
