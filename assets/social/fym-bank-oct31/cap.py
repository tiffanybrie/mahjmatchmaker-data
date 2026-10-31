"""Capture FYM v107 (Version 1.9.2) phone screens for the Oct 31 content bank. Local copy of site-app/fym-v107 (commit c7ab351a) served on :8777.
Raw 1170x2532 PNGs go to /dev/shm/w/caps (not committed). Usage: python3 cap.py"""
import sys,json; sys.path.insert(0,'/home/claude/mahjmatchmaker-data/assets/social/fym-bank-oct31')
from lib import *
meta={}
def ev(pg,js,*a): return pg.evaluate(js,*a)
def filt(pg): ev(pg,"()=>{const d=document.querySelector('button.holc');window.scrollTo(0,d.getBoundingClientRect().top+scrollY-330)}"); pg.wait_for_timeout(900)
def press(pg,kind,last=False): ev(pg,f"()=>{{const a=[...document.querySelectorAll('button.{kind}')].filter(b=>b.offsetParent);(a.length>1&&{str(last).lower()}?a[a.length-1]:a[0]).click()}}"); pg.wait_for_timeout(1500)
def dot(pg,t): ev(pg,"(t)=>[...document.querySelectorAll('button.dot')].find(b=>b.title===t&&b.offsetParent).click()",t); pg.wait_for_timeout(1300)
def card_flow(pg,racks,tag):
    ev(pg,"()=>{const b=[...document.querySelectorAll('.pick1 button, .r3p button')].filter(b=>b.offsetParent)[0];b&&b.click()}"); pg.wait_for_timeout(2500)
    meta[tag+'-rdeck']=ev(pg,"()=>rackDeck().slice(0,8)")
    if not racks: deck(pg,'.deck.r',420); shot(pg,f'{tag}-rack0'); press(pg,'yes',True)
    for i,(rk,kind) in enumerate(racks):
        ev(pg,"(r)=>{const pool=rackPool;window.rackPool=function(){const a=pool();return [r,...a.filter(x=>x!==r)]};try{rackPool=window.rackPool}catch(e){};renderRacks()}",rk); pg.wait_for_timeout(1500)
        deck(pg,'.deck.r',420); shot(pg,f'{tag}-rack{i}'); press(pg,kind,True)
    ev(pg,"()=>{S.rpick=S.rliked.slice(0,2);renderRacks()}"); pg.wait_for_timeout(1500)
    press(pg,'go',True); pg.wait_for_timeout(3500)
    ev(pg,"()=>{const h=[...document.querySelectorAll('h2,h1,div')].find(e=>e.innerText&&e.innerText.trim().startsWith('Your match card')&&e.offsetParent);if(h)window.scrollTo(0,h.getBoundingClientRect().top+scrollY-90)}"); pg.wait_for_timeout(1500)
    shot(pg,f'{tag}-card')
    ev(pg,"()=>[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim()==='Story 9:16').click()"); pg.wait_for_timeout(4000)
    src=ev(pg,"()=>{const i=[...document.querySelectorAll('img')].filter(e=>e.offsetParent&&e.naturalHeight>=3000)[0];return i?i.src:''}")
    if src.startswith('data:'):
        import base64; open(O+f'{tag}-storycard.'+('png' if 'png' in src[:30] else 'jpg'),'wb').write(base64.b64decode(src.split(',',1)[1])); print('storycard',tag)
    else: print('no storycard', src[:80])
with sync_playwright() as p:
  if 1:
    A=sys.argv[1:] or ['h','p','m']
    # 1 Holiday: Tinselle (Emerald Green) x Evergreen & Tartan
  if 'h' in A:
    b,pg=start(p)
    search_pick(pg,'Tinselle','Tinselle (Emerald')
    meta['tin_all']=ev(pg,"()=>matDeck().length")
    deck(pg); shot(pg,'h-deck')
    filt(pg); shot(pg,'h-filt0')
    ev(pg,"()=>document.querySelector('.chip.holc').click()"); pg.wait_for_timeout(1300); meta['tin_hol']=ev(pg,"()=>matDeck().length")
    dot(pg,'Green'); meta['tin_holgreen']=ev(pg,"()=>matDeck().length"); meta['tin_hg_names']=ev(pg,"()=>matDeck().map(k=>M[k].n)")
    filt(pg); shot(pg,'h-filt1')
    front(pg,'Evergreen & Tartan'); deck(pg); shot(pg,'h-heart')
    press(pg,'yes'); deck(pg); shot(pg,'h-after')
    card_flow(pg,[('bb:Brick Red','yes'),('bb:Dark Navy','no'),('bb:Evergreen','yes')],'h')
    b.close()
  if 'p' in A:
    b,pg=start(p)
    pg.locator('input[placeholder*=Search]').first.click(); pg.keyboard.type('Papaya'); pg.wait_for_timeout(1300); shot(pg,'p-search')
    ev(pg,"()=>[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim().startsWith('Papaya Spritz')).click()"); pg.wait_for_timeout(2800)
    meta['pap_all']=ev(pg,"()=>matDeck().length"); meta['heiress']=ev(pg,"()=>Object.keys(M).filter(k=>/Heiress/.test(M[k].n)).map(k=>M[k].n+'|'+M[k].bn+'|'+!!M[k].hid)")
    deck(pg); shot(pg,'p-deck')
    filt(pg); shot(pg,'p-filt0')
    dot(pg,'Pink'); meta['pap_pink']=ev(pg,"()=>matDeck().length"); meta['pap_pink_names']=ev(pg,"()=>matDeck().slice(0,10).map(k=>M[k].n+'/'+M[k].bn)")
    filt(pg); shot(pg,'p-filt1'); deck(pg); shot(pg,'p-pinkdeck')
    dot(pg,'All colors')
    hn=[x.split('|')[0] for x in meta['heiress'] if x.endswith('false')]
    if hn:
        front(pg,hn[0]); deck(pg); shot(pg,'p-heart'); press(pg,'yes')
        card_flow(pg,[],'p')
    b.close()
  if 'm' in A:
    b,pg=start(p)
    ev(pg,"()=>[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim().startsWith('Start with a mat')).click()"); pg.wait_for_timeout(2500)
    shot(pg,'m-door')
    inp=pg.locator('input[placeholder*=Search]:visible').first; inp.click(); pg.keyboard.type('Heiress'); pg.wait_for_timeout(1500); shot(pg,'m-search')
    meta['mdoor_btns']=ev(pg,"()=>[...document.querySelectorAll('button')].filter(b=>b.offsetParent&&/Heiress/.test(b.innerText)).map(b=>b.className+'|'+b.innerText.trim().slice(0,40))")
    ev(pg,"()=>{const b=[...document.querySelectorAll('button')].find(b=>b.offsetParent&&/Heiress/.test(b.innerText));b&&b.click()}"); pg.wait_for_timeout(3000)
    meta['mdoor_state']=ev(pg,"()=>JSON.stringify({mode:S.mode,dset:S.dset,step:S.step})")
    ev(pg,"()=>{const d=document.querySelector('.deck.t,.deck');d&&window.scrollTo(0,d.getBoundingClientRect().top+scrollY-330)}"); pg.wait_for_timeout(1200); shot(pg,'m-tiles')
    b.close()
json.dump(meta,open(O+'meta.json','w'),indent=1); print(json.dumps(meta,indent=0)[:3000])
