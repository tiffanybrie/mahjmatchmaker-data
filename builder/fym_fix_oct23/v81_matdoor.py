"""FYM v81 mat door (Tiffany Oct 23 8:24pm + 8:54pm): both doors start the same way.
 - Mat door home shows the same "Take the 30-second tour" link and "1 Swipe on tiles, 2 Pick your favorite, 3 Add racks".
 - After she picks her mat she goes straight into SWIPING TILE SETS (Tiffany's matches first, then album sets by colour,
   then partner catalog sets), on top of her mat. Hearted sets fall below as tile suitors. Tap a suitor to see it,
   then "Add racks" goes straight to the racks (no frozen "Your mat" + "See other mats" step in between).
 - "See all" switches to the bird's-eye grid (the old grid); "Swipe instead" switches back.
Usage: python3 v81_matdoor.py <build_dir>"""
import sys
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
def rep(old, new, n=1):
    global h
    c = h.count(old); assert c == n, f'expected {n} x {old[:90]!r}, found {c}'; h = h.replace(old, new)

HOW = ("<button type=\"button\" class=\"solink\" data-tour style=\"display:block;margin:-4px auto 2px\">Take the 30-second tour</button>"
       "<div class=\"how\"><div><b>1</b>Swipe on tiles</div><div><b>2</b>Pick your favorite</div><div><b>3</b>Add racks</div></div>")
# 1. same intro on the mat door
rep("if(!S.dmat){const ids=doorMats();el.innerHTML=lock+doorBtns()+(S.dkeep",
    "if(!S.dmat){const ids=doorMats();el.innerHTML=lock+doorBtns()+'" + HOW.replace("'", "\\'") + "'+(S.dkeep")

# 2. tile swiper after the mat is picked (grid only on "See all")
rep(" const m=M[S.dmat];const g=setsForMat(S.dmat);const n=S.dshow||DOOR.slim;\n el.innerHTML=lock+doorBtns()+`<div class=\"picked\">",
    " const m=M[S.dmat];const g=setsForMat(S.dmat);const n=S.dshow||DOOR.slim;\n if(!S.dgrid&&S.set==null){tswipe(el,lock,m,g);return;}\n el.innerHTML=lock+doorBtns()+(S.set==null?`<div class=\"tswap\"><button type=\"button\" class=\"chip\" data-dgrid=\"0\">‹ Swipe instead</button></div>`:'')+`<div class=\"picked\">")

JS = r'''
/* v81: mat door = swipe tile sets on top of your mat (Tiffany Oct 23 8:54pm) */
S.tseen={};S.tliked=[];S.thist=[];S.tpeek=null;S.dgrid=false;
const TB=s=>((T[s.tile]||{}).bn||s.maker);
const tAll=()=>{if(!S.dmat||!M[S.dmat])return [];const g=setsForMat(S.dmat);return [...g.her,...g.alb,...g.cat];};
const tq=()=>tAll().filter(r=>!S.tseen[r.i]);
function tcard(r,peek){const s=r.s;return `<div class="scard tk" ${peek?'':'id="top-t"'} data-i="${r.i}"><div class="ph"><img src="${tileFull(s)||pile(s)}" alt="${esc(s.name)} tiles" class="photo" draggable="false">${peek?'':'<span class="stamp yes" aria-hidden="true">♥</span><span class="stamp no" aria-hidden="true">✕</span>'}</div>${r.her?`<span class="hb">${icon()} Tiffany’s match</span>`:''}<div class="meta">${LG(TB(s))?`<img class="lg" src="${LG(TB(s))}" alt="">`:''}<div class="tx"><b>${esc(s.name)}</b><span>${esc(s.maker)}</span></div></div></div>`;}
function tswipe(el,lock,m,g){const all=tAll(),q=tq(),pk=S.tpeek!=null?all.find(r=>r.i===S.tpeek):null,L=S.tliked.filter(i=>all.some(r=>r.i===i));
 const sub=g.her.length?`Tiffany matched ${esc(MN(S.dmat))} with ${g.her.length} tile set${g.her.length>1?'s':''}; they come first. Tap ♥ if you love it, ✕ if it’s not the one.`:`Tiffany hasn’t matched this mat yet, so the closest color matches come first. Tap ♥ if you love it, ✕ if it’s not the one.`;
 const deck=pk?`<div class="deck t"><div class="peekbar"><span>Your suitor</span></div>${tcard(pk,true)}</div>`:(q.length?`<div class="deck t">${q[1]?tcard(q[1],true).replace('class="scard tk"','class="scard tk back"'):''}${tcard(q[0])}</div>`:`<div class="deck t"><div class="empty">That’s every tile set for this mat. Tap ♥ suitors below, or See all.</div></div>`);
 const acts=pk?`<div class="acts pk"><button type="button" class="pill" data-tunpeek>‹ Back to the deck to keep swiping</button><button type="button" class="pill gh" data-tunlike="${pk.i}">✕ Remove from suitors</button></div>`:`<div class="acts"><button type="button" class="no" data-tno aria-label="No thanks" ${q.length?'':'disabled'}>✕</button><button type="button" class="yes" data-tyes aria-label="Love" ${q.length?'':'disabled'}>♥</button></div>`;
 const tray=`<div class="tray ttr" id="ttray"><div class="tl"><b>${L.length}</b>${L.length===1?'suitor':'suitors'}${L.length>3?'<span class="more">swipe for more ›</span>':''}</div>${L.length?`<div class="th">${L.slice().reverse().map(i=>`<button type="button" data-tpk="${i}" aria-pressed="${S.tpeek===i}" aria-label="${esc(D.sets[i].name)}"><img src="${pile(D.sets[i])}" alt=""></button>`).join('')}</div>${pk?`<button type="button" class="go" data-tadd="${pk.i}">Add racks ›</button>`:`<button type="button" class="go" disabled>Tap a suitor to pick your tiles</button>`}`:`<div class="none">${q.length>1?'Swipe right':'Tap ♥'} on tile sets you like. They’ll wait here so you can compare.</div>`}</div>`;
 el.innerHTML=lock+doorBtns()+`<div class="picked"><span class="num">1</span><img src="${matTh(S.dmat)}" alt=""><div class="tx"><i>Your mat</i><b>${esc(m.n)}</b><small>${esc(m.bn||'')}</small></div><button type="button" class="chip" data-dchange>Change mat</button></div>`+
  `<div class="shrow">${head(2,'Swipe the tiles',sub)}<button type="button" class="chip" data-dgrid="1">See all</button></div>`+
  `<div class="cmp"><div class="tilev" id="tv-d"><img src="${matSrc(S.dmat)}" alt="${esc(m.n)}" draggable="false"><div class="zb"><button type="button" data-tz="-1" aria-label="Zoom out">−</button><button type="button" data-tz="1" aria-label="Zoom in">+</button></div></div><div class="tcap"><span>${esc(MN(S.dmat))} mat</span>${S.thist.length?'<button type="button" class="backb" data-tback>‹ Back</button>':''}</div>${deck}</div>`+acts+tray;
 const t=$('tv-d');if(t)zoomer(t,t.querySelector('img'),t,{key:'tz_d_'+S.dmat,fp:[.5,.5],fz:1});
 const c=$('top-t');if(c){const img=c.querySelector('.ph img');zoomer(c,img,c.querySelector('.ph'),{zoom:false,swipe:{yes:c.querySelector('.stamp.yes'),no:c.querySelector('.stamp.no'),ok:()=>S.tpeek==null,fly:y=>tfly(y)}});}}
function tdecide(yes){const q=tq();if(!q.length)return;const i=q[0].i;S.tseen[i]=1;S.thist.push(i);if(yes&&!S.tliked.includes(i))S.tliked.push(i);trk(yes?'right':'left',{mat:S.dmat,set:D.sets[i].slug});renderTiles();}
function tfly(yes){const c=$('top-t');if(!c||!tq().length||S.tpeek!=null)return;const r=c.getBoundingClientRect(),g=c.cloneNode(true);g.removeAttribute('id');Object.assign(g.style,{position:'fixed',left:r.left+'px',top:r.top+'px',width:r.width+'px',height:r.height+'px',margin:'0',zIndex:'55',pointerEvents:'none',transition:'none',transform:c.style.transform||''});document.body.appendChild(g);const s=g.querySelector('.stamp.'+(yes?'yes':'no'));if(s)s.style.opacity=1;tdecide(yes);requestAnimationFrame(()=>{g.style.transition='transform .22s ease-in, opacity .22s';g.style.transform=`translateX(${yes?150:-150}%) rotate(${yes?18:-18}deg)`;g.style.opacity='.5';});setTimeout(()=>g.remove(),280);}
const tReset=()=>{S.tseen={};S.tliked=[];S.thist=[];S.tpeek=null;S.dgrid=false;};
document.addEventListener('click',e=>{const q=s=>e.target.closest&&e.target.closest(s);let b;
 if(q('[data-tyes]')){tfly(true);return;}
 if(q('[data-tno]')){tfly(false);return;}
 if(b=q('[data-tpk]')){S.tpeek=+b.dataset.tpk;renderTiles();return;}
 if(q('[data-tunpeek]')){S.tpeek=null;renderTiles();return;}
 if(b=q('[data-tunlike]')){const i=+b.dataset.tunlike;S.tliked=S.tliked.filter(x=>x!==i);S.tpeek=null;renderTiles();toast('Removed from your suitors');return;}
 if(q('[data-tback]')){const i=S.thist.pop();if(i!=null){delete S.tseen[i];S.tliked=S.tliked.filter(x=>x!==i);}renderTiles();return;}
 if(b=q('[data-dgrid]')){S.dgrid=b.dataset.dgrid==='1';S.tpeek=null;renderTiles();return;}
 if(b=q('[data-tadd]')){const i=+b.dataset.tadd;S.tpeek=null;pairUp(i);jump('s-racks');return;}
 if(q('[data-dmat]')||q('[data-dchange]')||q('[data-door]')){const pickd=!!q('[data-dmat]');tReset();if(S.door==='mat'&&(S.set==null||S.tilesOpen))renderTiles();if(pickd&&!TOUR.on)requestAnimationFrame(()=>{const h=document.querySelector('#s-tiles .shrow');if(h){let y=h.getBoundingClientRect().top+window.scrollY-64;const ac=document.querySelector('#s-tiles .acts');if(ac){const ab=ac.getBoundingClientRect().bottom+window.scrollY+16-innerHeight;if(ab>y)y=Math.min(ab,h.getBoundingClientRect().top+window.scrollY-8);}window.scrollTo({top:Math.max(0,y),behavior:'smooth'});}});return;}
});
'''
rep("function pairUp(i){", JS + "function pairUp(i){")

css = """.deck.t{height:min(80vw,360px)}
.scard.tk .ph img.photo{object-fit:cover;width:100%;height:100%}
.tswap{display:flex;justify-content:flex-start;margin:2px 0 4px}
.coach button.sk"""
rep(".coach button.sk", css)
open(P, 'w').write(h); print('v81 mat door applied')
