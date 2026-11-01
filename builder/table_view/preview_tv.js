/* Table view inside the full Find Your Mat-ch app (preview only, Nov 1). Adds 'Table' to the View switch; every swipe card
   (mat deck, mat-door tile deck, rack deck) is redrawn as a top-down table. Uses the app's own globals (D, S, M, R, T, set,
   matFull, rackSrc, pile, renderRacks) + TVD (coverage classes, real tile back colors, rack finishes/prices). */
(function(){
const TV={walls:true,players:4,faces:'center',rack:null,q:'',brand:'',fcol:'',fin:'',price:'',instock:false};
const LS=(()=>{try{return JSON.parse(localStorage.getItem('fymTV')||'{}')}catch(e){return {}}})();Object.assign(TV,{walls:LS.walls!==false,players:LS.players||4,faces:LS.faces||'center'});
const save=()=>{try{localStorage.setItem('fymTV',JSON.stringify({walls:TV.walls,players:TV.players,faces:TV.faces}))}catch(e){}};
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'})[c]);
const BDN=b=>b==='Tigre de Tartan'?'Tigre de Tartán':b;
const twOf=s=>(T[s.tile]&&T[s.tile].tw)||.9;
const fits=(k,s)=>!(twOf(s)>.95&&((R[k]&&R[k].len)||20)<=18.5);
const rackOK=(k,s)=>!!(R[k]&&!R[k].hid&&TVD.rk[k]&&fits(k,s));
const rackWhy=(k,s)=>!TVD.rk[k]?(TVD.rkw[k]||'Only a group or angled photo of these racks.'):(!fits(k,s)?'Too short for these tiles.':'');
const matCls=k=>TVD.cls[k]||'C';
function pickRack(s,mat){if(TV.rack&&rackOK(TV.rack,s))return TV.rack;
  const her=(s.m.find(x=>x[0]===mat)||[])[1]||[];for(const k of her)if(rackOK(k,s))return k;
  for(const k of (D.lt&&D.lt[s.slug])||[])if(rackOK(k,s))return k;
  return Object.keys(R).find(k=>rackOK(k,s))}
/* ---------- drawing ---------- */
const IC={};function load(src){if(!src)return Promise.resolve(null);if(!IC[src])IC[src]=new Promise(r=>{const i=new Image();i.onload=()=>r(i);i.onerror=()=>r(null);i.src=src});return IC[src]}
function rr(c,x,y,w,h,r){c.beginPath();c.moveTo(x+r,y);c.arcTo(x+w,y,x+w,y+h,r);c.arcTo(x+w,y+h,x,y+h,r);c.arcTo(x,y+h,x,y,r);c.arcTo(x,y,x+w,y,r);c.closePath()}
function shade(hx,f){const n=parseInt(hx.slice(1),16);const m=v=>Math.max(0,Math.min(255,Math.round(f>1?v+(255-v)*(f-1):v*f)));return `rgb(${m(n>>16)},${m(n>>8&255)},${m(n&255)})`}
const CACHE={};
async function render(mat,s,rack,corner){const key=[mat,s.slug,rack,corner?1:0,TV.walls,TV.players,TV.faces].join('|');if(CACHE[key])return CACHE[key];
  const N=1000,PPI=N/36,C=N/2;const [mi,ri,fi]=await Promise.all([matFull(mat).then(load),load(rackSrc(rack)),load(pile(s))]);
  const bk=TVD.backs[s.slug];const [pat,spr]=await Promise.all([load(bk&&bk.p),load(bk&&bk.s)]);
  const oc=document.createElement('canvas');oc.width=oc.height=N;const c=oc.getContext('2d');c.fillStyle='#e4dcd2';c.fillRect(0,0,N,N);
  if(mi){if(corner){const q0=N*.36;c.drawImage(mi,q0,q0,N-q0,N-q0)}else{const m=Math.min(mi.width,mi.height);c.drawImage(mi,(mi.width-m)/2,(mi.height-m)/2,m,m,0,0,N,N)}}
  const seats=corner?['S','E']:{4:['S','E','N','W'],3:['S','E','W'],2:['S','N']}[TV.players];
  const RL=(R[rack]&&R[rack].len)||20;let RD=ri?RL*ri.height/ri.width:2.4;RD=Math.min(Math.max(RD,1.6),3.2);const L=RL*PPI,Dp=RD*PPI;const edge={S:1.1,N:.7,E:.9,W:.9};const inner={},place=[];
  for(const sd of seats){let x,y,w,h,a;if(sd==='S'){w=L;h=Dp;x=C-L/2;y=N-edge.S*PPI-Dp;a=0;inner.S=y}if(sd==='N'){w=L;h=Dp;x=C-L/2;y=edge.N*PPI;a=Math.PI;inner.N=y+Dp}
    if(sd==='E'){w=Dp;h=L;x=N-edge.E*PPI-Dp;y=C-L/2;a=-Math.PI/2;inner.E=x}if(sd==='W'){w=Dp;h=L;x=edge.W*PPI;y=C-L/2;a=Math.PI/2;inner.W=x+Dp}place.push({sd,x,y,w,h,a})}
  const drawRacks=()=>{for(const p of place){c.save();c.translate(p.x+p.w/2,p.y+p.h/2);c.rotate(p.a);c.drawImage(ri,-L/2,-Dp/2,L,Dp);c.restore()}};
  if(ri){c.save();c.shadowColor='rgba(20,10,10,.45)';c.shadowBlur=.35*PPI;c.shadowOffsetX=.08*PPI;c.shadowOffsetY=.14*PPI;drawRacks();c.restore()}
  if(TV.walls&&bk){const tw=twOf(s),W=tw*PPI,H=tw*1.43*PPI,gap=.07*PPI,L19=19*W*.985,a0=C-L19/2;let seed=7;const rnd=()=>{seed=(seed*16807)%2147483647;return seed/2147483647-.5};
    for(const p of place){const vert=p.sd==='E'||p.sd==='W';
      for(let i=0;i<19;i++){const a=a0+i*W*.985;let x,y,w,h;
        if(p.sd==='S'){x=a;y=inner.S-gap-H;w=W;h=H}if(p.sd==='N'){x=a;y=inner.N+gap;w=W;h=H}if(p.sd==='E'){x=inner.E-gap-H;y=a;w=H;h=W}if(p.sd==='W'){x=inner.W+gap;y=a;w=H;h=W}
        if(i===0){c.save();c.fillStyle='rgba(15,8,8,.28)';const gw=vert?H:L19,gh=vert?L19:H;rr(c,x+.08*PPI,y+.12*PPI,gw+.1*PPI,gh+.1*PPI,.12*PPI);c.fill();c.restore()}
        x+=rnd()*.02*PPI;y+=rnd()*.02*PPI;
        if(spr){c.save();c.translate(x+w/2,y+h/2);if(vert)c.rotate(Math.PI/2);c.drawImage(spr,-W/2,-H/2,W,H);c.restore();continue}
        c.save();rr(c,x,y,w,h,.11*PPI);c.clip();
        if(pat){const sw=pat.width*.6,sh=pat.height*.6;c.drawImage(pat,(rnd()+.5)*(pat.width-sw),(rnd()+.5)*(pat.height-sh),sw,sh,x,y,w,h)}
        else{const g=c.createLinearGradient(x,y,x+w,y+h);g.addColorStop(0,shade(bk.b,1.14));g.addColorStop(.55,bk.b);g.addColorStop(1,shade(bk.b,.84));c.fillStyle=g;c.fillRect(x,y,w,h)}
        c.restore();c.strokeStyle='rgba(0,0,0,.28)';c.lineWidth=1.5;rr(c,x,y,w,h,.11*PPI);c.stroke()}}}
  if(ri)drawRacks();
  if(fi&&TV.faces!=='off'){const d=N*(TV.faces==='center'?.26:.22),cx=TV.faces==='center'?C:(corner?N*.2:N*.8),cy=TV.faces==='center'?C:(corner?N*.2:N*.8);
    c.save();c.shadowColor='rgba(0,0,0,.35)';c.shadowBlur=18;c.beginPath();c.arc(cx,cy,d/2+8,0,7);c.fillStyle='#fff';c.fill();c.restore();
    c.save();c.beginPath();c.arc(cx,cy,d/2,0,7);c.clip();const m=Math.min(fi.width,fi.height);c.drawImage(fi,(fi.width-m)/2,(fi.height-m)/2,m,m,cx-d/2,cy-d/2,d,d);c.restore()}
  return CACHE[key]=oc.toDataURL('image/jpeg',.86)}
/* ---------- cards ---------- */
function ctx(card){const st=D.sets[S.set];
  if(card.classList.contains('tk'))return {mat:S.dmat,s:D.sets[+card.dataset.i],rack:null};
  if(card.classList.contains('rk'))return {mat:S.fav,s:st,rack:card.dataset.id};
  return {mat:card.dataset.id,s:st,rack:null}}
function note(card,txt){let n=card.querySelector('.tvna');if(!n){n=document.createElement('div');n.className='tvna';card.querySelector('.ph').appendChild(n)}n.textContent=txt;card.classList.add('tvoff')}
function proc(card){const x=ctx(card);if(!x.mat||!x.s||!M[x.mat])return;const img=card.querySelector('.ph img:not(.onmat)');if(!img)return;
  const cls=matCls(x.mat);const rack=x.rack||pickRack(x.s,x.mat);const key=[x.mat,x.s.slug,rack,TV.walls,TV.players,TV.faces].join('|');if(card.dataset.tvk===key)return;card.dataset.tvk=key;
  card.classList.remove('tvoff');const old=card.querySelector('.tvna');if(old)old.remove();
  if(cls==='C'){note(card,'Not available in Table view: '+(TVD.why[x.mat]||(TVD.cls[x.mat]?'no flat, top-down photo of this mat yet.':'not checked for Table view yet (new to the app this week).')));return}
  if(x.rack&&!rackOK(x.rack,x.s)){note(card,'Not available in Table view: '+rackWhy(x.rack,x.s));return}
  if(!rack){note(card,'No rack with a clean photo fits these tiles yet.');return}
  render(x.mat,x.s,rack,cls==='B').then(u=>{if(card.dataset.tvk===key){img.src=u;img.classList.add('tvimg')}});
  if(cls==='B')note(card,'Corner view: we only have a close-up photo of this mat.'),card.classList.remove('tvoff');
  if(!TVD.backs[x.s.slug]&&TV.walls&&!card.querySelector('.tvna'))note(card,'Walls off: back color not confirmed yet.'),card.classList.remove('tvoff')}
/* ---------- table bar + rack picker ---------- */
function bar(){const st=D.sets[S.set];if(!st)return '';const mat=S.fav||S.dmat;const r=pickRack(st,mat||(document.querySelector('#top-m')||{}).dataset?.id);
  return `<div class="tvbar"><div class="tvrow"><b>Table</b><span class="tvl">racks:</span><b class="tvrn">${r?esc(R[r].n):'none yet'}</b><button type="button" class="tvchg" data-tvrs>Swap racks ›</button>${TV.rack?'<button type="button" class="tvauto" data-tvauto>Use Tiffany’s pick</button>':''}</div>
   <div class="tvrow"><label><input type="checkbox" data-tvw ${TV.walls?'checked':''}> Walls</label>
   <span class="tvseg" data-tvp>${[4,3,2].map(n=>`<button type="button" data-n="${n}" class="${TV.players===n?'on':''}">${n}</button>`).join('')}</span><span class="tvl">players</span></div>
   <div class="tvrow"><span class="tvl">Tile faces</span><span class="tvseg" data-tvf>${[['center','Center'],['corner','Corner'],['off','Off']].map(([v,l])=>`<button type="button" data-v="${v}" class="${TV.faces===v?'on':''}">${l}</button>`).join('')}</span></div>
   <p class="tvhint">Table is new. Up close and Aerial work just like today. Gray cards aren’t available in Table view yet.</p></div>`}
function addBars(){for(const id of ['s-mats','s-tiles','s-racks']){const el=document.getElementById(id);if(!el)continue;const dk=el.querySelector('.deck');const ex=el.querySelector('.tvbar');
  const html=bar();if(!dk||!html){if(ex)ex.remove();continue}if(ex){if(ex.dataset.h!==html){ex.outerHTML=html;const nb=el.querySelector('.tvbar');if(nb)nb.dataset.h=html}continue}
  const host=dk.closest('.cmp')||dk;host.insertAdjacentHTML('afterend',html);const nb=el.querySelector('.tvbar');if(nb)nb.dataset.h=html}}
const FAMS=['pink','red','orange','yellow','green','blue','purple','neutral','black','wood','clear','tortoise','metallic'];
const FINS=[['wood','Wood'],['walnut','Walnut'],['tortoise','Tortoise'],['pearl','Pearl'],['clear','Clear / Acrylic'],['lucite','Lucite'],['metallic','Metallic'],['white','White'],['glitter','Glitter']];
function sheet(){const st=D.sets[S.set];let sh=document.getElementById('tvsheet');if(!sh){sh=document.createElement('div');sh.id='tvsheet';document.body.appendChild(sh)}
  const q=TV.q.trim().toLowerCase();const brands=[...new Set(Object.keys(R).filter(k=>!R[k].hid).map(k=>R[k].bn))].sort();
  let rows=Object.keys(R).filter(k=>!R[k].hid).map(k=>{const r=R[k];const pr=TVD.price[k]||[];return {k,r,ok:rackOK(k,st),why:rackWhy(k,st),fin:TVD.fin[k]||[],p:pr[0],pc:pr[1],cd:pr[2],so:TVD.so[k]}});
  const words=o=>[o.r.n,BDN(o.r.bn),...(o.r.rf||[]),...o.fin].join(' ').toLowerCase();
  rows=rows.filter(o=>(!q||q.split(/\s+/).every(w=>words(o).includes(w)))&&(!TV.brand||o.r.bn===TV.brand)&&(!TV.fcol||(o.r.rf||[]).includes(TV.fcol))&&(!TV.fin||o.fin.includes(TV.fin)));
  if(!q)rows=rows.filter(o=>fits(o.k,st));
  let nop=0;if(TV.price!==''){nop=rows.filter(o=>o.pc==null).length;rows=rows.filter(o=>o.pc!=null&&o.pc<=TV.price)}
  if(TV.instock&&rows.some(o=>!o.so))rows=rows.filter(o=>!o.so);
  const her=new Set(((st.m.find(x=>x[0]===(S.fav||S.dmat))||[])[1])||[]);rows.sort((a,b)=>(b.ok-a.ok)||(her.has(b.k)-her.has(a.k))||(b.r.pa-a.r.pa)||a.r.n.localeCompare(b.r.n));
  const act=[q&&`“${esc(TV.q)}”`,TV.brand&&esc(BDN(TV.brand)),TV.fcol,TV.fin,TV.price!==''&&`under $${TV.price}`,TV.instock&&'in stock only'].filter(Boolean);
  sh.innerHTML=`<div class="tvs-in" role="dialog" aria-label="Swap racks"><div class="tvs-h"><b>Swap racks</b><button type="button" class="tvx" data-tvclose aria-label="Close">×</button></div>
  <input id="tvq" type="search" placeholder="Search racks: name, color or finish (walnut, pearl…)" value="${esc(TV.q)}">
  <select id="tvbrand"><option value="">All brands</option>${brands.map(b=>`<option value="${esc(b)}" ${TV.brand===b?'selected':''}>${esc(BDN(b))}</option>`).join('')}</select>
  <div class="tvchips">${FAMS.map(f=>`<button type="button" data-tvfam="${f}" class="${TV.fcol===f?'on':''}">${f}</button>`).join('')}</div>
  <div class="tvchips">${FINS.map(([f,l])=>`<button type="button" data-tvfin="${f}" class="${TV.fin===f?'on':''}">${l}</button>`).join('')}</div>
  <div class="tvchips"><button type="button" data-tvpr="" class="${TV.price===''?'on':''}">Any price</button>${(TVD.pr||[]).map(v=>`<button type="button" data-tvpr="${v}" class="${TV.price===v?'on':''}">Under $${v}</button>`).join('')}<label class="tvst"><input type="checkbox" data-tvstock ${TV.instock?'checked':''}> In stock only</label></div>
  ${act.length?`<div class="tvact">Showing ${act.join(' · ')} <button type="button" data-tvclear>Clear</button></div>`:''}
  <p class="tvhint">Only racks that fit ${esc(st.name)} tiles can go on the table${q?'':' (shorter racks appear when you search)'}.${nop?` ${nop} without a listed price not shown.`:''}</p>
  <div class="tvgrid">${rows.slice(0,150).map(o=>`<button type="button" class="tvit${o.ok?'':' off'}${TV.rack===o.k?' on':''}" data-tvrack="${esc(o.k)}"><span class="ph"><img src="${rackSrc(o.k)||''}" alt="" loading="lazy">${her.has(o.k)?'<i>♥</i>':''}${o.ok?'':`<em>${esc(o.why.replace(/\.$/,''))}</em>`}</span><span class="nm">${esc(o.r.n)}${o.so?' <small>Sold out</small>':''}</span><span class="bn">${esc(BDN(o.r.bn))}</span>${o.p!=null?`<span class="pr">$${Math.round(o.p)}${o.cd?' <em>less with code MAHJMATCH</em>':''}</span>`:''}</button>`).join('')||'<p class="tvhint">Nothing matches. Tap Clear.</p>'}</div></div>`;
  sh.hidden=false;const qi=sh.querySelector('#tvq');qi.oninput=e=>{TV.q=e.target.value;clearTimeout(sheet.t);sheet.t=setTimeout(()=>{sheet();const n=document.getElementById('tvq');n.focus();n.setSelectionRange(n.value.length,n.value.length)},250)};
  sh.querySelector('#tvbrand').onchange=e=>{TV.brand=e.target.value;sheet()}}
document.addEventListener('click',e=>{const t=e.target.closest('[data-tvp] button,[data-tvf] button,[data-tvrs],[data-tvauto],[data-tvclose],[data-tvfam],[data-tvfin],[data-tvpr],[data-tvclear],[data-tvrack]');if(!t)return;e.stopPropagation();e.preventDefault();
  if(t.closest('[data-tvp]'))TV.players=+t.dataset.n;else if(t.closest('[data-tvf]'))TV.faces=t.dataset.v;else if(t.hasAttribute('data-tvauto'))TV.rack=null;
  else if(t.hasAttribute('data-tvrs')){sheet();return}else if(t.hasAttribute('data-tvclose')){document.getElementById('tvsheet').hidden=true;return}
  else if(t.dataset.tvfam!==undefined){TV.fcol=TV.fcol===t.dataset.tvfam?'':t.dataset.tvfam;sheet();return}else if(t.dataset.tvfin!==undefined){TV.fin=TV.fin===t.dataset.tvfin?'':t.dataset.tvfin;sheet();return}
  else if(t.dataset.tvpr!==undefined){TV.price=t.dataset.tvpr===''?'':+t.dataset.tvpr;sheet();return}else if(t.hasAttribute('data-tvclear')){Object.assign(TV,{q:'',brand:'',fcol:'',fin:'',price:'',instock:false});sheet();return}
  else if(t.dataset.tvrack!==undefined){const k=t.dataset.tvrack,st=D.sets[S.set];if(!rackOK(k,st)){alertNote(R[k].n+': '+rackWhy(k,st));return}TV.rack=k;document.getElementById('tvsheet').hidden=true}
  save();pass(true)},true);
document.addEventListener('change',e=>{if(e.target.matches('[data-tvw]')){TV.walls=e.target.checked;save();pass(true)}if(e.target.matches('[data-tvstock]')){TV.instock=e.target.checked;sheet()}},true);
function alertNote(t){let n=document.getElementById('tvtoast');if(!n){n=document.createElement('div');n.id='tvtoast';document.body.appendChild(n)}n.textContent=t;n.hidden=false;clearTimeout(alertNote.t);alertNote.t=setTimeout(()=>n.hidden=true,3500)}
/* ---------- watch the app ---------- */
let was=false,busy=false;
function pass(force){if(busy)return;busy=true;try{const on=S.mode==='table';document.body.classList.toggle('tvmode',on);
  if(on){if(force)document.querySelectorAll('.scard[data-tvk]').forEach(c=>delete c.dataset.tvk);document.querySelectorAll('.scard').forEach(proc);addBars()}
  else{document.querySelectorAll('.tvbar').forEach(b=>b.remove());if(was&&typeof renderRacks==='function')renderRacks()}
  was=on}finally{busy=false}}
if(typeof MutationObserver!=='undefined'&&document.body)new MutationObserver(()=>{clearTimeout(pass.t);pass.t=setTimeout(()=>pass(false),40)}).observe(document.body,{childList:true,subtree:true});
})();
