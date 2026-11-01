# --- suitors: before picking
suit(pg,300); meta['su_final']=suitbox(pg); shot(pg,'30-suitors')
meta['suitor_html']=ev(pg,f"()=>({SUJS})().parentElement.outerHTML.slice(0,1500)")
# pick Clara: click the suitor thumbnail for Clara
meta['pickbtn']=bbox(pg,"[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim()==='Clara')")
ok=ev(pg,"()=>{const b=[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim()==='Clara');b.click();return !!b}")
print('pick',ok); pg.wait_for_timeout(2500)
shot(pg,'31-picked')
meta['picked']=ev(pg,"()=>JSON.stringify({dmat:S.dmat,step:S.step})")
# racks
RX='peacelovemahjong.com/mahjong-racks-racks-pushers-set-of-4'; RY=['bb:Magenta','bb:Light Blue']
meta['rdeck0']=ev(pg,"()=>rackDeck().slice(0,12)")
to(pg,'.deck.r',420)
PL="()=>[...document.querySelectorAll('button')].filter(b=>b.offsetParent&&b.innerText.trim()==='+'&&b.getBoundingClientRect().top>0&&b.getBoundingClientRect().top<420)[0]"
meta['rz']=bbox(pg,f"({PL})()")
for j in range(4):
    shot(pg,f'40-rz{j}')
    if j<3: ev(pg,f"()=>{{const b=({PL})();b&&b.click()}}"); pg.wait_for_timeout(1000)
pr=ev(pg,"()=>{const e=[...document.querySelectorAll('img')].filter(i=>i.offsetParent&&i.getBoundingClientRect().top<330&&i.getBoundingClientRect().width>150)[0].getBoundingClientRect();return [e.left+e.width/2,Math.max(e.top,120)+80]}")
meta['pan']=pr
pg.mouse.move(pr[0],pr[1]); pg.mouse.down(); pg.mouse.move(pr[0]+90,pr[1]+70,steps=12); pg.mouse.up(); pg.wait_for_timeout(1000); shot(pg,'40-rz4')
WC="()=>[...document.querySelectorAll('button.chip')].find(b=>b.offsetParent&&b.innerText.trim()==='Wood')"
meta['woodchip']=bbox(pg,f"({WC})()"); meta['rchips']=ev(pg,"()=>[...document.querySelectorAll('button.chip')].filter(b=>b.offsetParent&&b.getBoundingClientRect().top>0&&b.getBoundingClientRect().top<520).map(b=>{const q=b.getBoundingClientRect();return [b.innerText.trim(),q.left,q.top,q.width,q.height]})")
shot(pg,'45-chips')
ev(pg,f"()=>({WC})().click()"); pg.wait_for_timeout(1400)
meta['wood_deck']=ev(pg,"()=>rackDeck().slice(0,8).map(r=>R[r].n)")
to(pg,'.deck.r',420); shot(pg,'46-wood')
def force(r):
    ev(pg,"(r)=>{if(!window._rp0)window._rp0=rackPool;window.rackPool=function(){const a=window._rp0();return [r,...a.filter(x=>x!==r)]};try{rackPool=window.rackPool}catch(e){};renderRacks()}",r); pg.wait_for_timeout(1400)
for j,(rk,kind) in enumerate([(RX,'no'),(RY[0],'yes'),(RY[1],'yes')]):
    if j==1: ev(pg,f"()=>({WC})().click()"); pg.wait_for_timeout(1300)
    force(rk); to(pg,'.deck.r',420)
    shot(pg,f'r{j}-b'); card(pg,'.deck.r',f'r{j}')
    meta[f'r{j}-name']=ev(pg,"()=>{const e=document.querySelector('.deck.r .scard:not(.back)');return e?e.dataset.id:''}")
    ev(pg,f"()=>{{const a=[...document.querySelectorAll('.deck.r button.{kind}')].filter(b=>b.offsetParent);a[0].click()}}"); pg.wait_for_timeout(1500)
    if j<2: force([RY[0],RY[1],RY[1]][j])
    to(pg,'.deck.r',420); shot(pg,f'r{j}-a')
    meta[f'r{j}-next']=ev(pg,"()=>{const e=document.querySelector('.deck.r .scard:not(.back)');return e?e.dataset.id:''}")
meta['rliked']=ev(pg,"()=>S.rliked")
ev(pg,"()=>{S.rpick=S.rliked.filter(x=>x.startsWith('bb:')).slice(0,2);renderRacks()}"); pg.wait_for_timeout(1500)
ev(pg,"()=>window.scrollBy(0,400)"); pg.wait_for_timeout(800); shot(pg,'50-slots')
meta['go']=ev(pg,"()=>[...document.querySelectorAll('button.go')].filter(b=>b.offsetParent).map(b=>b.innerText.trim()+'|'+b.disabled)")
ev(pg,"()=>{const a=[...document.querySelectorAll('button.go')].filter(b=>b.offsetParent&&!b.disabled);a[a.length-1].click()}"); pg.wait_for_timeout(4000)
ev(pg,"()=>{const h=[...document.querySelectorAll('h2,h1,div')].find(e=>e.innerText&&e.innerText.trim().startsWith('Your match card')&&e.offsetParent);if(h)window.scrollTo(0,h.getBoundingClientRect().top+scrollY-90)}"); pg.wait_for_timeout(1500)
shot(pg,'60-card')
ev(pg,"()=>[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim()==='Story 9:16').click()"); pg.wait_for_timeout(4500)
src=ev(pg,"()=>{const i=[...document.querySelectorAll('img')].filter(e=>e.naturalHeight>=3000)[0];return i?i.src:''}")
import base64
if src.startswith('data:'): open(O+'storycard.'+('png' if 'png' in src[:30] else 'jpg'),'wb').write(base64.b64decode(src.split(',',1)[1])); print('storycard ok')
else: print('no storycard',src[:80])
shot(pg,'61-story')
# shop list
ev(pg,"()=>{const h=[...document.querySelectorAll('h2,h3,div,p')].filter(e=>e.offsetParent&&e.innerText&&/^(Shop|Shop your match|Shop the match)/i.test(e.innerText.trim())).pop();if(h)window.scrollTo(0,h.getBoundingClientRect().top+scrollY-120)}"); pg.wait_for_timeout(1200)
shot(pg,'70-shop')
meta['shop_text']=ev(pg,"()=>document.body.innerText.split('\\n').filter(t=>/MAHJMATCH|code|Shop/i.test(t)).slice(0,40)")
