"""FYM v110 capture for the Nutcracker Ballet holiday reel (Nov 1). Raw 1170x2532 PNGs -> /dev/shm/fym-holiday/caps."""
import sys; sys.path.insert(0,'/dev/shm/fym-holiday'); from lib import *
meta={}
def card(pg,sel,n):
    meta[n]=bbox(pg,f"document.querySelector('{sel} .scard:not(.back)')")
    pg.locator(f'{sel} .scard:not(.back)').first.screenshot(path=f'{O}{n}-card.png')
def press(pg,kind,last=False):
    ev(pg,f"()=>{{const a=[...document.querySelectorAll('.deck button.{kind}, button.sb.{kind}')].filter(b=>b.offsetParent);(({str(last).lower()})?a[a.length-1]:a[0]).click()}}"); pg.wait_for_timeout(1500)
DECK=330
def filt(pg): to(pg,'button.holc',300)
SUJS="()=>{const e=[...document.querySelectorAll('div')].filter(e=>e.offsetParent&&/^\\d+\\s*SUITORS?$/i.test((e.innerText||'').trim())).pop();return e}"
def suit(pg,off=360):
    ev(pg,f"()=>{{const e=({SUJS})();window.scrollTo(0,e.getBoundingClientRect().top+scrollY-{off})}}"); pg.wait_for_timeout(900)
def suitbox(pg):
    return ev(pg,f"()=>{{const e=({SUJS})().parentElement;const q=e.getBoundingClientRect();const th=[...e.querySelectorAll('img')].map(i=>{{const r=i.getBoundingClientRect();return [r.left,r.top,r.width,r.height]}});return {{box:[q.left,q.top,q.width,q.height],th}}}}")
with sync_playwright() as p:
    b,pg=start(p,3)
    pg.locator('input[placeholder*=Search]').first.click(); pg.keyboard.type('Nutcracker',delay=60); pg.wait_for_timeout(1500)
    meta['search_btn']=bbox(pg,"[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.includes('Nutcracker Ballet'))")
    shot(pg,'01-search')
    ev(pg,"(t)=>[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.includes(t)).click()",'Nutcracker Ballet'); pg.wait_for_timeout(3500)
    meta['n_all']=ev(pg,"()=>matDeck().length")
    to(pg,'.deck.m',DECK); shot(pg,'02-deck')
    # Holiday chip
    filt(pg); meta['holc']=bbox(pg,"document.querySelector('button.holc')"); shot(pg,'10-hol-before')
    meta['hid_sugarplum']=ev(pg,"()=>{const k='www.ohmymahjong.com/sugarplum-mat';M[k].hid=true;renderAll();return true}"); pg.wait_for_timeout(800)
    ev(pg,"()=>document.querySelector('button.holc').click()"); pg.wait_for_timeout(1500)
    meta['n_hol']=ev(pg,"()=>matDeck().length"); filt(pg); shot(pg,'11-hol-after')
    seq=[("Clara's Dream Christmas",'yes',"Yuletide"),("Yuletide",'no',"Tied With A Bow"),
         ('BLUE',None,None),("Pretty Little Christmas",'yes',"Clara"),("Clara",'yes',None)]
    i=0
    for name,kind,nxt in seq:
        if name=='BLUE':
            to(pg,'.deck.m',DECK)
            filt(pg); meta['blue']=bbox(pg,"[...document.querySelectorAll('button.dot')].find(b=>b.title==='Blue & teal')"); shot(pg,'20-blue-before')
            ev(pg,"()=>[...document.querySelectorAll('button.dot')].find(b=>b.title==='Blue & teal').click()"); pg.wait_for_timeout(1500)
            meta['n_holblue']=ev(pg,"()=>matDeck().length"); meta['holblue']=ev(pg,"()=>matDeck().map(k=>M[k].n+' | '+M[k].bn)")
            filt(pg); shot(pg,'21-blue-after'); front(pg,'Pretty Little Christmas'); filt(pg); shot(pg,'21b-blue-after'); continue
        front(pg,name); to(pg,'.deck.m',DECK); shot(pg,f's{i}-b'); card(pg,'.deck.m',f's{i}')
        meta[f's{i}-btn']=bbox(pg,f"[...document.querySelectorAll('.deck.m button.{kind}')].filter(b=>b.offsetParent)[0]")
        press(pg,kind)
        if nxt: front(pg,nxt)
        to(pg,'.deck.m',DECK); shot(pg,f's{i}-a')
        meta[f's{i}-next']=ev(pg,"()=>{const e=document.querySelector('.deck.m .scard:not(.back)');return e?e.dataset.id:''}")
        if kind=='yes':
            # suitors row
            suit(pg); meta[f'su{i}']=suitbox(pg); shot(pg,f'su{i}')
        i+=1
    json.dump(meta,open(O+'meta.json','w'),indent=1)
    exec(open('/dev/shm/fym-holiday/cap_tail.py').read())
    json.dump(meta,open(O+'meta.json','w'),indent=1)
    b.close()
