/* Table view inside the full Find Your Mat-ch app (preview, Nov 1 rebuild after Tiffany 7:43pm + 7:45pm).
   Matches the Table View Sample UX: the table fills the swipe card (X / heart as usual), one compact Adjust button by the
   View switch opens the bottom sheet (Swap tiles / Swap mat / Swap racks on top, then Walls, Tile faces Center/Corner/Off);
   each Swap opens the half-height swap sheet (tabs Tiles · Mat · Racks, own search per tab with Clear, brand, color,
   finish for racks, In stock only, Tiffany's picks, price chips) with the table visible above. A swapped mat / tile set /
   rack becomes the CURRENT card of the app's own deck, so heart → Racks → Card works exactly like the normal app.
   Always 4 players. Zoom: the app's own zoomer (pinch, double-tap, + / −), persisted across swaps (S.zs.tvz); ⤢ opens the
   whole table full screen. Sizes from config/tableview-sizecheck-nov01.json (20in rack, 19-tile wall = 19 x tile width,
   centered, tight against the rack, wall depth 1.55 x tile width). Uses the app's globals (D, S, M, R, T, ...). */
(function(){
const SZ=TVD.sz||{mat:33,edge:1.0,wallDepth:1.55,gap:0};
const TV={walls:true,faces:'center',rack:null};
try{const o=JSON.parse(localStorage.getItem('fymTV')||'{}');TV.walls=o.walls!==false;if(['center','corner','off'].includes(o.faces))TV.faces=o.faces}catch(e){}
const save=()=>{try{localStorage.setItem('fymTV',JSON.stringify({walls:TV.walls,faces:TV.faces}))}catch(e){}};
const SW={tab:'mat',qs:{tiles:'',mat:'',racks:''},brand:'',color:'',fin:'',price:'',instock:false,picks:false};
let CTX='s-mats';
const $i=id=>document.getElementById(id);
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'})[c]);
const BD=b=>b==='Tigre de Tartan'?'Tigre de Tartán':(b||'');
const twOf=s=>(T[s.tile]&&T[s.tile].tw)||.9;
const fits=(k,s)=>!(s&&twOf(s)>.95&&((R[k]&&R[k].len)||20)<=18.5);
const rackOK=(k,s)=>!!(R[k]&&!R[k].hid&&TVD.rk[k]&&fits(k,s));
const rackWhy=(k,s)=>!TVD.rk[k]?(TVD.rkw[k]||'Only a group or angled photo of these racks.'):(!fits(k,s)?'Too short for these tiles.':'');
const matCls=k=>TVD.cls[k]||'C';
const matWhy=k=>TVD.why[k]||(TVD.cls[k]?'no flat, top-down photo of this mat yet.':'not checked for Table view yet (new to the app this week).');
const toast=t=>{let n=$i('tvtoast');if(!n){n=document.createElement('div');n.id='tvtoast';document.body.appendChild(n)}n.textContent=t;n.hidden=false;clearTimeout(toast.t);toast.t=setTimeout(()=>n.hidden=true,3800)};
function herFor(s,mat){return ((s&&s.m.find(x=>x[0]===mat))||[])[1]||[]}
function pickRack(s,mat){if(TV.rack&&rackOK(TV.rack,s))return TV.rack;
  const cand=[...herFor(s,mat),...((D.lt&&D.lt[s.slug])||[]),...Object.keys(R)];
  return cand.find(k=>rackOK(k,s)&&!OOS('r',k))||cand.find(k=>rackOK(k,s))}/* QA Nov 1: an in-stock rack first */
window.TVPICK=(slug,mat)=>{const s=D.sets.find(x=>x.slug===slug);return s?pickRack(s,mat):null};/* test hook */
/* ---------- drawing ---------- */
const IC={};function load(src){if(!src)return Promise.resolve(null);if(!IC[src])IC[src]=new Promise(r=>{const web=!/^(data|blob):/i.test(src);
  const go=(u,again)=>{const i=new Image();if(web)i.crossOrigin='anonymous';i.onload=()=>r(i);i.onerror=()=>{if(web&&!again)go(u+(u.includes('?')?'&':'?')+'cors=1',true);else r(null)};i.src=u};go(src,false)});return IC[src]}
/* website copy: photos come from the jsDelivr CDN (another origin); without crossOrigin the canvas is tainted and toDataURL throws (same as the app's match-card loader lk) */
function rr(c,x,y,w,h,r){c.beginPath();c.moveTo(x+r,y);c.arcTo(x+w,y,x+w,y+h,r);c.arcTo(x+w,y+h,x,y+h,r);c.arcTo(x,y+h,x,y,r);c.arcTo(x,y,x+w,y,r);c.closePath()}
function shade(hx,f){const n=parseInt(hx.slice(1),16);const m=v=>Math.max(0,Math.min(255,Math.round(f>1?v+(255-v)*(f-1):v*f)));return `rgb(${m(n>>16)},${m(n>>8&255)},${m(n&255)})`}
const CACHE=new Map();const cget=k=>{const v=CACHE.get(k);if(v){CACHE.delete(k);CACHE.set(k,v)}return v};const cput=(k,v,max)=>{CACHE.set(k,v);while(CACHE.size>max)CACHE.delete(CACHE.keys().next().value)};
async function render(mat,s,rack,corner,N){
  const PPI=N/SZ.mat,C=N/2;
  const [mi,ri,fi]=await Promise.all([matFull(mat).then(load),load(rackSrc(rack)),load(tileFull(s)||pile(s))]);
  const bk=TVD.backs[s.slug];const [pat,spr]=await Promise.all([load(bk&&bk.p),load(bk&&bk.s)]);
  const oc=document.createElement('canvas');oc.width=oc.height=N;const c=oc.getContext('2d');c.imageSmoothingQuality='high';c.fillStyle='#e4dcd2';c.fillRect(0,0,N,N);
  if(mi){if(corner){const q0=N*.36;c.drawImage(mi,q0,q0,N-q0,N-q0)}else{const m=Math.min(mi.width,mi.height);c.drawImage(mi,(mi.width-m)/2,(mi.height-m)/2,m,m,0,0,N,N)}}
  const seats=corner?['S','E']:['S','E','N','W'];/* always 4 players (Tiffany Nov 1 7:43pm) */
  const RL=(R[rack]&&R[rack].len)||20;let RD=ri?RL*ri.height/ri.width:2.4;RD=Math.min(Math.max(RD,1.6),3.2);
  const L=RL*PPI,Dp=RD*PPI,E=SZ.edge*PPI;const inner={},place=[];
  for(const sd of seats){let x,y,w,h,a;if(sd==='S'){w=L;h=Dp;x=C-L/2;y=N-E-Dp;a=0;inner.S=y}if(sd==='N'){w=L;h=Dp;x=C-L/2;y=E;a=Math.PI;inner.N=y+Dp}
    if(sd==='E'){w=Dp;h=L;x=N-E-Dp;y=C-L/2;a=-Math.PI/2;inner.E=x}if(sd==='W'){w=Dp;h=L;x=E;y=C-L/2;a=Math.PI/2;inner.W=x+Dp}place.push({sd,x,y,w,h,a})}
  const drawRacks=()=>{for(const p of place){c.save();c.translate(p.x+p.w/2,p.y+p.h/2);c.rotate(p.a);c.drawImage(ri,-L/2,-Dp/2,L,Dp);c.restore()}};
  if(ri){c.save();c.shadowColor='rgba(20,10,10,.45)';c.shadowBlur=.35*PPI;c.shadowOffsetX=.08*PPI;c.shadowOffsetY=.14*PPI;drawRacks();c.restore()}
  if(TV.walls&&bk){const tw=twOf(s),W=tw*PPI,H=tw*SZ.wallDepth*PPI,gap=SZ.gap*PPI,L19=19*W,a0=C-L19/2;let seed=7;const rnd=()=>{seed=(seed*16807)%2147483647;return seed/2147483647-.5};
    for(const p of place){const vert=p.sd==='E'||p.sd==='W';
      for(let i=0;i<19;i++){const a=a0+i*W;let x,y,w,h;
        if(p.sd==='S'){x=a;y=inner.S-gap-H;w=W;h=H}if(p.sd==='N'){x=a;y=inner.N+gap;w=W;h=H}if(p.sd==='E'){x=inner.E-gap-H;y=a;w=H;h=W}if(p.sd==='W'){x=inner.W+gap;y=a;w=H;h=W}
        if(i===0){c.save();c.fillStyle='rgba(15,8,8,.28)';const gw=vert?H:L19,gh=vert?L19:H;rr(c,x+.08*PPI,y+.12*PPI,gw+.1*PPI,gh+.1*PPI,.12*PPI);c.fill();c.restore()}
        x+=rnd()*.015*PPI;y+=rnd()*.015*PPI;
        if(spr){c.save();c.translate(x+w/2,y+h/2);if(vert)c.rotate(Math.PI/2);c.drawImage(spr,-W/2,-H/2,W,H);c.restore();continue}
        c.save();rr(c,x,y,w,h,.1*PPI);c.clip();
        if(pat){const sw=pat.width*.6,sh=pat.height*.6;c.drawImage(pat,(rnd()+.5)*(pat.width-sw),(rnd()+.5)*(pat.height-sh),sw,sh,x,y,w,h)}
        else{const g=c.createLinearGradient(x,y,x+w,y+h);g.addColorStop(0,shade(bk.b,1.14));g.addColorStop(.55,bk.b);g.addColorStop(1,shade(bk.b,.84));c.fillStyle=g;c.fillRect(x,y,w,h)}
        c.restore();c.strokeStyle='rgba(0,0,0,.28)';c.lineWidth=Math.max(1,.02*PPI);rr(c,x,y,w,h,.1*PPI);c.stroke()}}}
  if(ri)drawRacks();
  if(fi&&TV.faces!=='off'){const d=N*(TV.faces==='center'?.26:.22),cx=TV.faces==='center'?C:(corner?N*.2:N*.8),cy=TV.faces==='center'?C:(corner?N*.2:N*.8);
    c.save();c.shadowColor='rgba(0,0,0,.35)';c.shadowBlur=N*.018;c.beginPath();c.arc(cx,cy,d/2+N*.008,0,7);c.fillStyle='#fff';c.fill();c.restore();
    c.save();c.beginPath();c.arc(cx,cy,d/2,0,7);c.clip();const m=Math.min(fi.width,fi.height);c.drawImage(fi,(fi.width-m)/2,(fi.height-m)/2,m,m,cx-d/2,cy-d/2,d,d);c.restore()}
  try{return oc.toDataURL('image/jpeg',.88)}catch(e){return null}}
function tableURL(x,N){const key=[x.mat,x.s.slug,x.rack,x.corner?1:0,TV.walls,TV.faces,N].join('|');const v=cget(key);if(v)return v;
  const p=render(x.mat,x.s,x.rack,x.corner,N);cput(key,p,N>2000?3:36);return p}
/* ---------- cards ---------- */
function ctx(card){let mat,s,rack=null;
  if(card.classList.contains('tk')){mat=S.dmat;s=D.sets[+card.dataset.i]}
  else if(card.classList.contains('rk')){mat=S.fav;s=D.sets[S.set];rack=card.dataset.id}
  else{mat=card.dataset.id;s=D.sets[S.set]}
  if(!mat||!s||!M[mat])return null;const cls=matCls(mat);
  return {mat,s,cls,fixed:!!rack,rack:rack||pickRack(s,mat),corner:cls==='B'}}
const cardN=c=>Math.round(Math.min(1800,Math.max(1000,((c&&c.clientWidth)||360)*Math.min(window.devicePixelRatio||1,3))));
function note(card,txt,gray){let n=card.querySelector('.tvna');if(!n){n=document.createElement('div');n.className='tvna';const ph=card.querySelector('.ph');if(!ph)return;ph.appendChild(n)}n.textContent=txt;card.classList.toggle('tvoff',!!gray)}
function proc(card){const x=ctx(card);if(!x)return;const img=card.querySelector('.ph img:not(.onmat)');if(!img)return;
  const N=cardN(card);const key=[x.mat,x.s.slug,x.rack,TV.walls,TV.faces].join('|');if(card.dataset.tvk===key)return;card.dataset.tvk=key;delete card.dataset.tvhi;
  card.classList.remove('tvoff');const old=card.querySelector('.tvna');if(old)old.remove();
  if(x.cls==='C'){note(card,'Not available in Table view: '+matWhy(x.mat),true);return}
  if(x.fixed&&!rackOK(x.rack,x.s)){note(card,'Not available in Table view: '+rackWhy(x.rack,x.s),true);return}
  if(!x.rack){note(card,'No rack with a clean photo fits these tiles yet.',true);return}
  tableURL(x,N).then(u=>{if(card.dataset.tvk!==key||card.dataset.tvhi)return;if(!u){note(card,'Table view couldn’t load a photo for this one. Try Up close or Aerial.',true);return}img.src=u;img.classList.add('tvimg')});
  if(x.corner)note(card,'Corner view: we only have a close-up photo of this mat.');
  else if(!TVD.backs[x.s.slug]&&TV.walls)note(card,'Walls off: back color not confirmed yet.')}
/* sharper picture once zoomed in */
setInterval(()=>{if(S.mode!=='table'||!S.zs||!S.zs.tvz||S.zs.tvz.s<1.2)return;
  for(const c of document.querySelectorAll('.scard[id^="top-"][data-tvk]')){if(c.dataset.tvhi===c.dataset.tvk||c.classList.contains('tvoff'))continue;const x=ctx(c);if(!x||x.cls==='C')continue;
    const key=c.dataset.tvk;c.dataset.tvhi=key;tableURL(x,2600).then(u=>{if(u&&c.dataset.tvk===key){const im=c.querySelector('.ph img:not(.onmat)');if(im){im.src=u;im.classList.add('tvimg')}}})}},350);
/* ⤢ = the whole table full screen (app's openLbx calls this first in Table view) */
window.TVLBX=function(id){const c=[...document.querySelectorAll('.scard[id^="top-"]')].find(e=>id==='tv'?e.id==='top-t':e.dataset.id===id)||$i('top-t');if(!c)return false;
  const x=ctx(c);if(!x||x.cls==='C'||!x.rack)return false;
  const ttl=`${x.s.name} tiles · ${M[x.mat].n} · ${R[x.rack].n}`;const d=document.createElement('div');d.className='lbx';d.id='lbx';
  d.innerHTML=`<div class="lbh"><b>${esc(ttl)}</b><button type="button" data-lbxclose>Close ✕</button></div><div class="lbb" id="lbb"><img alt="${esc(ttl)}" draggable="false"><div class="zb"><button type="button" data-z="-1" aria-label="Zoom out">−</button><button type="button" data-z="1" aria-label="Zoom in">+</button></div></div>`;
  document.body.appendChild(d);document.body.style.overflow='hidden';const bx=$i('lbb'),im=bx.querySelector('img');let bound=false;
  const go=()=>{if(bound)return;bound=true;const r=bx.getBoundingClientRect(),k=Math.min(r.width,r.height);Object.assign(im.style,{width:k+'px',height:k+'px',maxWidth:'none',maxHeight:'none',left:(r.width-k)/2+'px',top:(r.height-k)/2+'px'});zoomer(bx,im,bx,{})};
  im.addEventListener('load',go,{once:true});const cur=c.querySelector('.ph img.tvimg');if(cur)im.src=cur.src;
  bx.addEventListener('wheel',e=>{e.preventDefault();const b=bx.querySelector(e.deltaY<0?'[data-z="1"]':'[data-z="-1"]');if(b)b.click()},{passive:false});
  tableURL(x,3000).then(u=>{if(u&&im.isConnected)im.src=u});return true};
/* the lightbox locks body scrolling; put the page back where it was when it closes */
{let LBY=null;const ol=window.openLbx,cl=window.closeLbx;if(typeof ol==='function'&&typeof cl==='function'){
  window.openLbx=function(id){if(!document.getElementById('lbx'))LBY=window.scrollY;return ol(id)};
  window.closeLbx=function(){const had=!!document.getElementById('lbx');cl();if(had&&LBY!=null){const y=LBY;LBY=null;window.scrollTo({top:y,behavior:'instant'})}}}}
/* ---------- landing: the table, not the controls ---------- */
const panelOpen=()=>{const p=$i('tvpanel');return !!(p&&p.classList.contains('open'))};
function land(id){const el=$i(id);if(!el)return;const c=el.querySelector('.scard[id^="top-"]')||el.querySelector('.deck');if(!c)return;
  const hd=document.querySelector('header.top');const H=(hd?hd.getBoundingClientRect().height:56)+6;const Y=window.scrollY;
  const ct=c.getBoundingClientRect().top+Y;const ac=el.querySelector('.acts');const bot=Math.max(c.getBoundingClientRect().bottom,ac&&ac.offsetParent?ac.getBoundingClientRect().bottom:0)+Y;
  const vr=el.querySelector('.vrow');const vt=vr&&vr.offsetParent?vr.getBoundingClientRect().top+Y:ct;const avail=innerHeight-(panelOpen()&&innerWidth<1280&&!$i('tvpanel').classList.contains('side')?$i('tvpanel').offsetHeight:0);
  let y=ct-H;if(!panelOpen()&&vt<ct&&ct-vt<90&&bot-vt+H<=avail)y=vt-H;
  window.scrollTo({top:Math.max(0,y),behavior:'smooth'})}
window.TVLAND=id=>{if(!['s-mats','s-tiles','s-racks'].includes(id))return false;requestAnimationFrame(()=>setTimeout(()=>land(id),30));return true};/* the Card step keeps the app's own jump */
const secOf=e=>{const s=e&&e.closest&&e.closest('#s-mats,#s-tiles,#s-racks');return s?s.id:null};
function activeSec(){/* the section whose swipe card is nearest the middle of the screen */let best=null,bd=1e9;for(const id of ['s-tiles','s-mats','s-racks']){const c=document.querySelector('#'+id+' .scard[id^="top-"]');if(!c||!c.offsetParent)continue;const r=c.getBoundingClientRect();const d=Math.abs((r.top+r.bottom)/2-innerHeight/2);if(d<bd){bd=d;best=id}}return best||CTX}
document.addEventListener('click',e=>{const t=e.target.closest&&e.target.closest('[data-mfront],[data-tfront],[data-mode],[data-dmat]');if(!t)return;
  const isTable=t.dataset.mode==='table'||(t.dataset.mode===undefined&&S.mode==='table');if(!isTable)return;
  const sec=t.hasAttribute('data-mfront')?'s-mats':(t.hasAttribute('data-tfront')||t.hasAttribute('data-dmat'))?'s-tiles':(secOf(t)||activeSec());
  setTimeout(()=>land(sec),140)},false);
/* ---------- Adjust button + bottom sheet (adjust / swap) ---------- */
function curSet(){if(CTX==='s-tiles'){const c=$i('top-t');if(c)return D.sets[+c.dataset.i]}return D.sets[S.set]}
function curMat(){if(CTX==='s-racks')return S.fav;if(CTX==='s-tiles')return S.dmat;const c=$i('top-m');return (c&&c.dataset.id)||S.fav||S.dmat}
function curRack(){if(CTX==='s-racks'){const c=$i('top-r');if(c)return c.dataset.id}const s=curSet(),m=curMat();return s&&m?pickRack(s,m):null}
function addAdjust(){const on=S.mode==='table';
  for(const id of ['s-mats','s-tiles','s-racks']){const el=$i(id);if(!el)continue;const has=!!el.querySelector('.deck .scard[id^="top-"]');
    el.querySelectorAll('.tvadj').forEach(b=>{if(!on||!has)b.remove()});el.querySelectorAll('.tvctl').forEach(b=>{if(!on||!has)b.remove()});
    if(!on||!has||el.querySelector('.tvadj'))continue;
    const vr=el.querySelector('.vrow');const btn='<button type="button" class="tvadj" data-tvadj aria-label="Adjust the table">Adjust</button>';
    if(vr)vr.insertAdjacentHTML('beforeend',btn);else{const dk=el.querySelector('.deck');const host=dk.closest('.cmp')||dk;host.insertAdjacentHTML('afterend','<div class="vrow tvctl">'+btn+'</div>')}}}
function panel(){let p=$i('tvpanel');if(p)return p;p=document.createElement('aside');p.id='tvpanel';p.className='tvp';p.setAttribute('aria-label','Table tools');p.dataset.tvmode='adjust';
  p.innerHTML=`<div class="tvgrab"><span></span><button type="button" class="tvback" data-tvopen="adjust">‹ Adjust</button><button type="button" class="tvx" data-tvclose aria-label="Close">×</button></div>
  <section class="tvadjsec"><h3>Adjust the table</h3>
   <div class="tvswaps"><button type="button" data-tvopen="tiles">Swap tiles</button><button type="button" data-tvopen="mat">Swap mat</button><button type="button" data-tvopen="racks">Swap racks</button></div>
   <div class="tvc"><span>Walls</span><button type="button" class="tvsw" id="tvwalls" role="switch" aria-label="Walls"></button></div><p class="tvhint" id="tvwn" hidden></p>
   <div class="tvc"><span>Tile faces</span><span class="tvseg" id="tvfaces">${[['center','Center'],['corner','Corner'],['off','Off']].map(([v,l])=>`<button type="button" data-v="${v}">${l}</button>`).join('')}</span></div>
   <p class="tvhint" id="tvrn"></p></section>
  <section class="tvswapsec"><div class="tvtabs" role="tablist">${[['tiles','Tiles'],['mat','Mat'],['racks','Racks']].map(([t,l])=>`<button type="button" role="tab" data-tvtab="${t}">${l}</button>`).join('')}</div>
   <label class="tvsearch"><span aria-hidden="true">⌕</span><input id="tvq" type="search" autocomplete="off" enterkeyhint="search"><button type="button" id="tvqx" aria-label="Clear search" hidden>Clear</button></label>
   <div class="tvbw"><button type="button" class="tvbtn" id="tvbrand">All brands ▾</button><div class="tvpop" id="tvpop" hidden></div></div>
   <div class="tvchips" id="tvdots"></div><div class="tvchips" id="tvfins"></div><div class="tvchips" id="tvprices"></div>
   <div class="tvtg"><label><button type="button" class="tvsw" id="tvins" role="switch" aria-label="In stock only"></button>In stock only</label><label><button type="button" class="tvsw" id="tvpk" role="switch" aria-label="Tiffany's picks"></button>Tiffany’s picks</label></div>
   <div class="tvact" id="tvact" hidden></div><p class="tvhint" id="tvsh"></p><div class="tvgrid" id="tvgrid"></div></section>`;
  document.body.appendChild(p);
  /* QA Nov 1: the app's click handler must never see clicks/drags in the sheet */
  for(const ev of ['click','pointerdown','pointerup','mousedown','mouseup','touchstart','touchend'])p.addEventListener(ev,e=>e.stopPropagation());
  /* drag the grab bar down to close */
  const g=p.querySelector('.tvgrab');let y0=null,dy=0;
  g.addEventListener('pointerdown',e=>{if(e.target.closest('button'))return;y0=e.clientY;dy=0;p.classList.add('drag');try{g.setPointerCapture(e.pointerId)}catch(_){}});
  g.addEventListener('pointermove',e=>{if(y0===null)return;dy=Math.max(0,e.clientY-y0);p.style.transform=`translateY(${dy}px)`});
  const end=()=>{if(y0===null)return;p.classList.remove('drag');if(dy>70)closeP();else p.style.transform='';y0=null};g.addEventListener('pointerup',end);g.addEventListener('pointercancel',end);
  p.querySelector('#tvq').addEventListener('input',e=>{SW.qs[SW.tab]=e.target.value;$i('tvqx').hidden=!e.target.value;grid()});
  if(typeof ResizeObserver!=='undefined')new ResizeObserver(pad).observe(p);return p}
function pad(){const p=$i('tvpanel');document.body.style.paddingBottom=p&&p.classList.contains('open')&&innerWidth<1280&&!p.classList.contains('side')?p.offsetHeight+'px':''}
function fitP(){const p=$i('tvpanel');if(!p||innerWidth>=1280)return;const el=$i(CTX);const c=el&&el.querySelector('.scard[id^="top-"]');const hd=document.querySelector('header.top');
  const H=(hd?hd.getBoundingClientRect().height:56)+6;const ch=c?c.getBoundingClientRect().height:0;const room=Math.round(innerHeight-H-ch-8);const cr=c?c.getBoundingClientRect().right:innerWidth;const sw=Math.floor(innerWidth-cr-16);
  const side=innerWidth>=700&&room<130&&sw>=220;p.classList.toggle('side',side);if(side){p.style.width=sw+'px';p.style.maxHeight='';return}p.style.width='';
  p.style.maxHeight=Math.max(innerWidth>=700?130:200,room)+'px'}/* short wide screens: dock in the margin beside the card *//* QA Nov 1: the whole card, name row included, stays above the sheet (tablet/small desktop: no 200px floor) */
addEventListener('resize',()=>{if(panelOpen()){fitP();pad()}});
function openP(mode,tab){const p=panel();fitP();p.dataset.tvmode=mode;if(tab&&tab!==SW.tab){SW.tab=tab;resetFilters()}p.classList.add('open');p.style.transform='';p.scrollTop=0;syncAdj();if(mode==='swap')tabSync();requestAnimationFrame(()=>{pad();land(CTX)})}
function closeP(){const p=$i('tvpanel');if(!p)return;p.classList.remove('open');p.style.transform='';pad()}
function resetFilters(){SW.brand='';SW.color='';SW.fin='';SW.price=''}
function setSw(el,on){if(el)el.setAttribute('aria-checked',on?'true':'false')}
function syncAdj(){const p=$i('tvpanel');if(!p)return;const s=curSet();setSw($i('tvwalls'),TV.walls);p.querySelectorAll('#tvfaces button').forEach(b=>b.classList.toggle('on',b.dataset.v===TV.faces));
  const wn=$i('tvwn');const nob=s&&!TVD.backs[s.slug];wn.hidden=!nob;if(nob)wn.textContent=`No walls for ${s.name} yet: we only draw walls from its real back color, and it isn’t confirmed.`;
  const r=curRack();$i('tvrn').innerHTML=r?`Racks on the table: <b>${esc(R[r].n)}</b>${TV.rack?' <button type="button" class="tvlink" data-tvauto>Use Tiffany’s pick</button>':''}`:''}
function tabSync(){const p=panel();p.querySelectorAll('[data-tvtab]').forEach(b=>{const on=b.dataset.tvtab===SW.tab;b.classList.toggle('on',on);b.setAttribute('aria-selected',on)});
  const q=$i('tvq');q.value=SW.qs[SW.tab];q.placeholder={tiles:'Search tile sets by name or brand',mat:'Search mats by name or brand',racks:'Search racks: name, color or finish (walnut, pearl…)'}[SW.tab];$i('tvqx').hidden=!q.value;
  $i('tvbrand').textContent=(SW.brand?BD(SW.brand):'All brands')+' ▾';$i('tvpop').hidden=true;setSw($i('tvins'),SW.instock);setSw($i('tvpk'),SW.picks);dots();fins();prices();grid()}
const COL={pink:'#ef8fb4',red:'#d23b3b',orange:'#f08a2c',yellow:'#f3cf3d',green:'#4f9e5a',teal:'#2fa3a0',blue:'#4c84c9',purple:'#9a6cc0',neutral:'#e9e0d0',dark:'#3a3340',black:'#222',brown:'#8a5a3a',white:'#fff',wood:'#b07a4a',tortoise:'#7b4a26',clear:'#dfeff4',metallic:'#c9b26b',pearl:'#efe9f2'};
function colorKeys(){if(SW.tab==='mat')return ['pink','red','orange','yellow','green','blue','purple','neutral','dark'];if(SW.tab==='racks')return ['pink','red','orange','yellow','green','blue','purple','neutral','black','brown','dark'];return Object.keys(typeof BACKG==='object'?BACKG:{})}
function dots(){const box=$i('tvdots');const ks=colorKeys();
  box.innerHTML=`<button type="button" class="tvdot all${SW.color?'':' on'}" data-tvc="">All colors</button>`+ks.map(c=>SW.tab==='tiles'?`<button type="button" class="tvchip${SW.color===c?' on':''}" data-tvc="${esc(c)}">${esc(c)}</button>`:`<button type="button" class="tvdot${SW.color===c?' on':''}" data-tvc="${c}" style="background:${COL[c]||'#ccc'}" aria-label="${c}" title="${c}"></button>`).join('')}
const FINS=[['wood','Wood'],['walnut','Walnut'],['tortoise','Tortoise'],['pearl','Pearl'],['clear','Clear / Acrylic'],['lucite','Lucite'],['metallic','Metallic'],['white','White'],['glitter','Glitter']];
function fins(){const box=$i('tvfins');box.hidden=SW.tab!=='racks';if(box.hidden){box.innerHTML='';return}const have=new Set(Object.values(TVD.fin).flat());
  box.innerHTML=FINS.filter(([f])=>have.has(f)).map(([f,l])=>`<button type="button" class="tvchip${SW.fin===f?' on':''}" data-tvfin="${f}">${l}</button>`).join('')}
function prices(){const r=(TVD.pr||{})[SW.tab]||[];const box=$i('tvprices');box.hidden=!r.length;
  box.innerHTML=`<button type="button" class="tvchip${SW.price===''?' on':''}" data-tvpr="">Any price</button>`+r.map(v=>`<button type="button" class="tvchip${SW.price===v?' on':''}" data-tvpr="${v}">Under $${v}</button>`).join('')}
function pool(){const s=curSet(),m=curMat();
  if(SW.tab==='mat'){const her=new Set(s?s.m.map(x=>x[0]):[]);const ord=s?[...her,...s.rank.map(i=>D.order[i])]:[];const seen=new Set();const ids=[];for(const k of [...ord,...Object.keys(M)])if(M[k]&&!M[k].hid&&!seen.has(k)){seen.add(k);ids.push(k)}
    return ids.map(k=>{const o=M[k],cl=matCls(k),pr=TVD.pm[k]||[];return {k,n:o.n,bn:o.bn,th:matTh(k),pa:o.pa,so:OOS('m',k),pk:her.has(k),off:cl==='C',why:'Not available in Table view: '+matWhy(k),tag:cl==='C'?'Not in Table view':(cl==='B'?'Corner only':''),cols:[...(o.mf||[]),...(o.ha||[])],p:pr[0],pc:pr[1],cd:pr[2],on:k===m,w:''}})}
  if(SW.tab==='tiles'){return D.sets.map((x,i)=>[x,i]).filter(([x])=>typeof VIS!=='function'||VIS(x)).map(([x,i])=>{const t=T[x.tile]||{},pr=TVD.pt[x.tile]||[];const pk=!!(m&&x.m.some(y=>y[0]===m));
    return {k:i,n:x.name,bn:t.bn||x.maker,th:pile(x),pa:t.pa,so:OOS('t',x.tile),pk,off:false,tag:TVD.backs[x.slug]?'':'No walls yet',cols:Object.keys(typeof BACKG==='object'?BACKG:{}).filter(g=>(BACKG[g]||[]).includes(x.name)),p:pr[0],pc:pr[1],cd:pr[2],on:s&&x.slug===s.slug,w:''}}).sort((a,b)=>(b.pk-a.pk)||((b.pa?1:0)-(a.pa?1:0))||a.n.localeCompare(b.n))}
  const her=new Set(s&&m?herFor(s,m):[]);const r0=curRack();
  return Object.keys(R).filter(k=>!R[k].hid).map(k=>{const o=R[k],pr=TVD.price[k]||[];const ok=rackOK(k,s);return {k,n:o.n,bn:o.bn,th:rackSrc(k),pa:o.pa,so:OOS('r',k),pk:her.has(k),off:!ok,why:rackWhy(k,s),tag:ok?'':rackWhy(k,s).replace(/\.$/,''),short:!fits(k,s),cols:o.rf||[],fin:TVD.fin[k]||[],p:pr[0],pc:pr[1],cd:pr[2],on:k===r0,w:(TVD.fin[k]||[]).join(' ')}}).sort((a,b)=>(a.off-b.off)||(b.pk-a.pk)||((b.pa?1:0)-(a.pa?1:0))||a.n.localeCompare(b.n))}
function list(){const q=SW.qs[SW.tab].trim().toLowerCase();let rows=pool();const info={};
  const words=it=>[it.n,BD(it.bn),...it.cols,it.w].join(' ').toLowerCase();
  if(q)rows=rows.filter(it=>q.split(/\s+/).every(w=>words(it).includes(w)));
  if(SW.brand)rows=rows.filter(it=>it.bn===SW.brand);if(SW.color)rows=rows.filter(it=>it.cols.includes(SW.color));if(SW.fin)rows=rows.filter(it=>(it.fin||[]).includes(SW.fin));
  if(SW.picks)rows=rows.filter(it=>it.pk);
  if(SW.tab==='racks'&&!q&&!SW.brand){info.cut=rows.filter(r=>r.short).length;rows=rows.filter(r=>!r.short)}
  if(SW.price!==''){info.nop=rows.filter(r=>r.pc==null).length;rows=rows.filter(r=>r.pc!=null&&r.pc<=SW.price)}
  if(SW.instock){const a=rows.filter(r=>!r.so);info.allso=!a.length&&rows.length>0;if(!info.allso)rows=a}
  rows.sort((a,b)=>(a.off?1:0)-(b.off?1:0));return [rows,info,q]}
const money=v=>'$'+(Math.round(v)===v?v:v.toFixed(2));
let VIS_ROWS=[];
function grid(){const [rows,info,q]=list();const s=curSet(),m=curMat();
  const parts=[];if(q)parts.push(`results for <b>“${esc(q)}”</b>`);if(SW.brand)parts.push(`<b>${esc(BD(SW.brand))}</b>`);if(SW.color)parts.push(`<b>${esc(SW.color)}</b>`);if(SW.fin)parts.push(`<b>${FINS.find(f=>f[0]===SW.fin)[1]}</b>`);if(SW.price!=='')parts.push(`<b>under $${SW.price}</b>`);if(SW.instock)parts.push('<b>in stock only</b>');if(SW.picks)parts.push('<b>Tiffany’s picks</b>');
  const a=$i('tvact');a.hidden=!parts.length;a.innerHTML=parts.length?`<span>Showing ${parts.join(' · ')}</span><button type="button" data-tvclear>Clear</button>`:'';
  let h='';if(SW.tab==='mat')h=s?`♥ = Tiffany’s match for ${esc(s.name)}. Gray = not available in Table view (tap to see why).`:'';
  if(SW.tab==='tiles')h=m&&M[m]?`♥ = Tiffany matched this set with ${esc(M[m].n)}.`:'';
  if(SW.tab==='racks')h=`Only racks that fit ${s?esc(s.name):'these'} tiles can go on the table${info.cut?` (${info.cut} shorter racks show when you search)`:''}. ♥ = Tiffany’s rack picks for this mat.`;
  if(info.allso)h='No in-stock matches here, so showing all. '+h;if(SW.price!==''&&info.nop)h=`${info.nop} without a listed price not shown. `+h;if(SW.price!=='')h+=' Prices: store price, or less with code MAHJMATCH where it applies.';
  $i('tvsh').innerHTML=h;const g=$i('tvgrid');
  if(!rows.length){g.innerHTML='<div class="tvempty">Nothing matches. Tap Clear above to see everything again.</div>';VIS_ROWS=[];return}
  VIS_ROWS=rows.slice(0,150);g.className='tvgrid'+(SW.tab==='racks'?' rk':'');
  g.innerHTML=VIS_ROWS.map((it,i)=>`<button type="button" class="tvit${it.off?' off':''}${it.on?' on':''}" data-tvi="${i}"><span class="ph">${it.th?`<img src="${esc(it.th)}" alt="" loading="lazy">`:''}${it.pk?'<span class="tvpk">♥</span>':''}${it.tag?`<span class="tvtag">${esc(it.tag)}</span>`:''}</span><span class="nm">${esc(it.n)}${it.so?' <small>Sold out</small>':''}</span><span class="bn">${esc(BD(it.bn))}</span>${it.p!=null?`<span class="pr">${money(it.p)}${it.cd?' <em>less with code MAHJMATCH</em>':''}</span>`:''}</button>`).join('')+(rows.length>VIS_ROWS.length?`<div class="tvempty">${rows.length-VIS_ROWS.length} more. Search to narrow it down.</div>`:'')}
function brandPop(){const p=$i('tvpop');if(!p.hidden){p.hidden=true;return}const cnt={};for(const it of pool()){cnt[it.bn]=cnt[it.bn]||{n:0,pa:!!it.pa};cnt[it.bn].n++}
  const bs=Object.entries(cnt).sort((a,b)=>(b[1].pa-a[1].pa)||a[0].localeCompare(b[0]));
  p.innerHTML=`<button type="button" data-tvb="">All brands</button>`+bs.map(([b,v])=>`<button type="button" data-tvb="${esc(b)}">${v.pa?'<span class="tvh">♥</span> ':''}${esc(BD(b))} (${v.n})</button>`).join('')+'<p class="tvhint">♥ Code MAHJMATCH works at these brands.</p>';p.hidden=false}
/* ---------- a swap = the app's own current pick ---------- */
function synth(a,v){const x=document.createElement('button');x.type='button';x.setAttribute(a,String(v));x.style.display='none';document.body.appendChild(x);x.click();x.remove()}
function swapMat(k){
  if(S.door==='mat'){if(S.set==null||S.tilesOpen){const tc=$i('top-t'),ti=tc?+tc.dataset.i:null;S.dmat=k;tReset();S.dshow=0;if(ti!=null&&D.sets[ti]){S.tfront=ti;S.tfmat=k}renderTiles();steps();CTX='s-tiles'}else{synth('data-mock',k);CTX='s-racks'}}
  else if(S.fav&&CTX==='s-racks'){synth('data-mock',k)}
  else{S.mfront=k;S.mfset=S.set;S.tvforce=k;delete S.seen[k];S.peek=null;renderMats();steps();CTX='s-mats'}}
function swapTiles(i){const m=curMat();
  if(S.door==='mat'){if(S.set==null||S.tilesOpen){S.tfront=i;S.tfmat=S.dmat;delete S.tseen[i];S.tpeek=null;S.thist=S.thist.filter(x=>x!==i);renderTiles();CTX='s-tiles'}else{pairUp(i);CTX='s-mats'}}
  else{const wasRacks=CTX==='s-racks'&&S.fav;synth('data-tile',i);if(m&&M[m]){if(wasRacks){synth('data-mock',m);CTX='s-racks'}else{S.mfront=m;S.mfset=S.set;S.tvforce=m;delete S.seen[m];renderMats();steps();CTX='s-mats'}}}}
function swapRack(k){const s=curSet();if(!rackOK(k,s)){toast(R[k].n+': '+rackWhy(k,s));return false}TV.rack=k;
  if(CTX==='s-racks'){S.tvrf=k;delete S.rseen[k];renderRacks()}return true}
function pickRow(it){if(it.off){toast(`${it.n}: ${it.why||it.tag}${SW.tab==='mat'?' You can still pick it in Up close or Aerial.':''}`);return}
  if(SW.tab==='mat')swapMat(it.k);else if(SW.tab==='tiles')swapTiles(it.k);else if(!swapRack(it.k))return;
  save();pass(true);syncAdj();grid();setTimeout(()=>{fitP();pad();land(CTX)},140)}
document.addEventListener('click',e=>{const t=e.target.closest&&e.target.closest('[data-tvadj],[data-tvopen],[data-tvclose],[data-tvtab],[data-tvc],[data-tvfin],[data-tvpr],[data-tvclear],[data-tvi],[data-tvb],#tvbrand,#tvqx,#tvwalls,#tvins,#tvpk,#tvfaces button,[data-tvauto]');
  if(!t){const p=$i('tvpop');if(p&&!p.hidden&&!e.target.closest('.tvbw'))p.hidden=true;return}e.preventDefault();e.stopPropagation();
  if(t.hasAttribute('data-tvadj')){CTX=secOf(t)||activeSec();openP('adjust');return}
  if(t.dataset.tvopen){if(t.dataset.tvopen==='adjust')openP('adjust');else openP('swap',t.dataset.tvopen);return}
  if(t.hasAttribute('data-tvclose')){closeP();return}
  if(t.dataset.tvtab){SW.tab=t.dataset.tvtab;resetFilters();tabSync();return}
  if(t.id==='tvqx'){SW.qs[SW.tab]='';$i('tvq').value='';t.hidden=true;grid();return}
  if(t.id==='tvbrand'){brandPop();return}
  if(t.dataset.tvb!==undefined){SW.brand=t.dataset.tvb;$i('tvbrand').textContent=(SW.brand?BD(SW.brand):'All brands')+' ▾';$i('tvpop').hidden=true;grid();return}
  if(t.dataset.tvc!==undefined){SW.color=SW.color===t.dataset.tvc?'':t.dataset.tvc;dots();grid();return}
  if(t.dataset.tvfin!==undefined){SW.fin=SW.fin===t.dataset.tvfin?'':t.dataset.tvfin;fins();grid();return}
  if(t.dataset.tvpr!==undefined){SW.price=t.dataset.tvpr===''?'':+t.dataset.tvpr;prices();grid();return}
  if(t.id==='tvins'){SW.instock=!SW.instock;setSw(t,SW.instock);grid();return}
  if(t.id==='tvpk'){SW.picks=!SW.picks;setSw(t,SW.picks);grid();return}
  if(t.hasAttribute('data-tvclear')){SW.qs[SW.tab]='';SW.instock=false;SW.picks=false;resetFilters();tabSync();return}
  if(t.dataset.tvi!==undefined){const it=VIS_ROWS[+t.dataset.tvi];if(it)pickRow(it);return}
  if(t.id==='tvwalls'){TV.walls=!TV.walls;save();syncAdj();pass(true);return}
  if(t.closest('#tvfaces')){TV.faces=t.dataset.v;save();syncAdj();pass(true);return}
  if(t.hasAttribute('data-tvauto')){TV.rack=null;S.tvrf=null;save();syncAdj();pass(true);return}},true);
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeP()});
/* ---------- watch the app ---------- */
let busy=false;
function pass(force){if(busy)return;busy=true;try{const on=S.mode==='table';document.body.classList.toggle('tvmode',on);
  if(on){if(force)document.querySelectorAll('.scard[data-tvk]').forEach(c=>delete c.dataset.tvk);
    document.querySelectorAll('.scard[id^="top-"]').forEach(proc);document.querySelectorAll('.scard:not([id^="top-"])').forEach(proc);addAdjust();
    if(panelOpen())syncAdj()}
  else{addAdjust();closeP()}}finally{busy=false}}
if(typeof MutationObserver!=='undefined'&&document.body)new MutationObserver(()=>{clearTimeout(pass.t);pass.t=setTimeout(()=>pass(false),30)}).observe(document.body,{childList:true,subtree:true});
})();
