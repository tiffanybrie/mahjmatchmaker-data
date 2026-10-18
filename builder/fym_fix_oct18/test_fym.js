const {chromium}=require('playwright');
const W=+process.argv[2]||390;
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:W,height:900}});
const errs=[];p.on('pageerror',e=>errs.push(String(e)));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
await p.goto('http://localhost:8791/index.html',{waitUntil:'load',timeout:90000});await p.waitForTimeout(1500);
const out={};
const pick=async slug=>{await p.evaluate(slug=>{const i=D.sets.findIndex(s=>s.slug===slug);const b=document.createElement('button');b.dataset.tile=i;document.body.appendChild(b);b.click();b.remove();},slug);await p.waitForTimeout(300);};
for(const s of ['anders-ruff-brownstone-bloom','amara','heritage','malachite','sunday-mahjong-sunday','rackin-rudolph','sunday-mahjong-december-1994','oh-my-mahjong-papaya-spritz']){
 await pick(s);
 out[s]=await p.evaluate(()=>{const top=document.querySelector('#top-m');const id=top&&top.dataset.id;return {first:id&&M[id].n+' | '+M[id].bn,label:top&&top.querySelector('.hb')?top.querySelector('.hb').textContent.trim():'',m0:set().m[0]&&M[set().m[0][0]].n,herOn:S.f.m.her,nHer:set().m.length,first5:matDeck().slice(0,5).map(i=>M[i].n)};});
}
// Sunday Regency
await pick('sunday-mahjong-sunday');
out.regency=await p.evaluate(()=>{const id='mahjsquadshop.com/regency-mahjong-mat';S.f.m.her=false;const pool=matDeck();return {herMat:herMat(id),pos:pool.indexOf(id),nHer:set().m.length,label:card(id,'m').includes('Tiffany’s match')};});
// label audit across all sets with filter off: any mat labeled hers not in m?
out.labelAudit=await p.evaluate(()=>{let bad=0;D.sets.forEach((s,i)=>{S.set=i;matPool().slice(0,60).forEach(id=>{if(card(id,'m').includes('Tiffany’s match')&&!s.m.some(x=>x[0]===id))bad++;});});return bad;});
// Rudolph + Liberty racks
await pick('rackin-rudolph');
out.rudLib=await p.evaluate(()=>{const lib=set().m.find(x=>/Liberty/.test(M[x[0]].n));S.fav=lib[0];return {mat:M[lib[0]].n,her:herRacks().map(r=>R[r].n),pool10:rackPool().slice(0,10).map(r=>R[r].n),mauveHer:herRacks().includes('bb:Mauve'),multiInPool:rackPool().includes('www.ohmymahjong.com/acrylic-rack-and-pusher-set')};});
await p.evaluate(()=>{S.fav=null;});
await p.screenshot({path:`rud_${W}.png`});
// stale case: like A, mock A, then peek B
await pick('amara');
const st=await p.evaluate(async()=>{const q=matDeck();const A=q[0],B=q[1];S.liked=[A,B];document.querySelector('[data-mock]')||0;
 const click=(sel)=>{const b=document.createElement('button');Object.entries(sel).forEach(([k,v])=>b.dataset[k]=v);document.body.appendChild(b);b.click();b.remove();};
 click({mock:A});const r1=document.querySelector('#s-racks .matv img')?.alt;
 click({peek:B});const pr=document.querySelector('#s-racks .r3p');const btn=pr&&pr.querySelector('[data-mock]');
 return {A:M[A].n,B:M[B].n,afterMock:r1,prompt:!!pr,btnFor:btn&&M[btn.dataset.mock].n,favStill:M[S.fav].n};});
out.stale=st;
await p.evaluate(()=>window.scrollTo(0,document.getElementById('s-racks').offsetTop-60));await p.waitForTimeout(400);
await p.screenshot({path:`stale_${W}.png`});
// toggle sync
out.sync=await p.evaluate(()=>{const bs=()=>[...document.querySelectorAll('#s-mats [data-her="m"]')].map(b=>b.getAttribute('aria-pressed')+':'+b.textContent.trim());const a=bs();document.querySelectorAll('#s-mats .herbar [data-her="m"]')[0].click();const b2=bs();return {before:a,after:b2};});
// badge
out.badge=await p.evaluate(()=>{S.fav=S.fav||set().m[0][0];return card('mm:Hawksbill','r').includes('Best value in tortoise');});
// door flows
const door=async(matName,tileSlug)=>{return await p.evaluate(([mn,ts])=>{const click=(sel)=>{const b=document.createElement('button');Object.entries(sel).forEach(([k,v])=>b.dataset[k]=v);document.body.appendChild(b);b.click();b.remove();};
 click({door:'mat'});const c=matCounts();const id=Object.keys(M).filter(i=>!M[i].hid&&M[i].n.toLowerCase().includes(mn.toLowerCase())).sort((a,b)=>(c[b]||0)-(c[a]||0))[0];if(!id)return {mat:mn,missing:true};click({dmat:id});const g=setsForMat(id);const her=g.her.map(r=>r.s.name);
 let res={mat:mn,id,herCount:her.length,herFirst:her.slice(0,5),txt:document.querySelector('#s-tiles').innerText.slice(0,0)};
 res.hasnt=document.querySelector('#s-tiles').innerText.includes('hasn’t matched');
 if(ts){const i=D.sets.findIndex(s=>s.slug===ts);click({dset:i});res.after={fav:S.fav&&M[S.fav].n,peek:S.peek&&M[S.peek].n,liked:S.liked.map(x=>M[x].n),note:(document.querySelector('#s-mats .dnote')||{}).innerText,topCard:(document.querySelector('#top-m')||{}).dataset?.id,racksPrompt:!!document.querySelector('#s-racks .r3p')};}
 return res;},[matName,tileSlug]);};
for(const mn of ['Larkspur','Brownstone Bloom','The Polo Club','White Lotus']) out['door_'+mn]=await door(mn);
out.door_viv=await door('Vivienne','pippa');
await p.waitForTimeout(900);
out.scrollY=await p.evaluate(()=>({y:scrollY,mats:document.getElementById('s-mats').offsetTop,racks:document.getElementById('s-racks').offsetTop}));
await p.screenshot({path:`door_viv_${W}.png`});
// door sweep: mats with cards but 'hasn't matched'
out.doorSweep=await p.evaluate(()=>{const c=matCounts();return {matsWithHer:Object.keys(c).length,visibleMats:Object.keys(M).filter(i=>!M[i].hid).length};});
// lightbox
await p.evaluate(()=>openLbx(S.fav||Object.keys(M)[0]));await p.waitForTimeout(800);await p.screenshot({path:`lbx_${W}.png`});await p.evaluate(()=>closeLbx());
out.errs=errs.slice(0,10);
console.log(JSON.stringify(out,null,1));await b.close();})();
