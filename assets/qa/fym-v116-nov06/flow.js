const {chromium}=require('playwright');
const VP=process.argv[2]||'390';const mob=VP==='390';
const OUT='qa/'+VP+'/';require('fs').mkdirSync(OUT,{recursive:true});
const BAD=/Mahjong Row|Cypress|Ivy Reverie|Mocha Bloom|Osmanthus|Marigold|Autumn Saffron|Spring Awakening|Midnight Garden|Honey Weave|Ash Burl|Terracotta Marble|The Lodge|Hunt Club|Tracing the Tides|Highland Heritage|Vintage Oxblood|Mahjong by SI/;
(async()=>{const b=await chromium.launch();
const ctx=await b.newContext(mob?{viewport:{width:390,height:844},deviceScaleFactor:2,isMobile:true,hasTouch:true}:{viewport:{width:1440,height:900}});
const p=await ctx.newPage();const R={vp:VP,checks:[],fails:[]};const ok=(c,m)=>{R.checks.push((c?'PASS ':'FAIL ')+m);if(!c)R.fails.push(m)};
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://localhost:8116/index.html',{waitUntil:'load',timeout:120000});await p.waitForTimeout(2500);
const txt=()=>p.evaluate(()=>document.getElementById('app').innerText);
const badIn=async(where)=>{const t=await txt();const m=t.match(new RegExp(BAD.source,'g'));ok(!m,'no parked names visible on '+where+(m?' :: '+[...new Set(m)].join(','):''));};
const sk=p.locator('button.sk');if(await sk.count()&&await sk.first().isVisible())await sk.first().click();
ok((await p.title()).includes('Version 1.16'),'title Version 1.16 ('+await p.title()+')');
await p.screenshot({path:OUT+'01-home.png'});await badIn('home');
const logos=await p.$$eval('[data-blogo]',e=>e.map(x=>x.dataset.blogo));
ok(!logos.some(l=>/Mahjong Row/.test(l)),'no Mahjong Row logo in brand grid');ok(logos.includes('Mahjong Co.'),'Mahjong Co. logo present (Kaleidoscope)');
// ===== TILES DOOR
await p.click('[data-door=tiles]');await p.waitForTimeout(600);
for(const q of ['Cypress','Mahjong Row','Oakley','Lyla','Mabel','Laken','Honey Weave','Ash Burl','Terracotta']){await p.fill('#tsq',q);await p.waitForTimeout(350);
 const r=await p.$$eval('[data-tile]',e=>e.filter(x=>x.offsetParent).map(x=>x.innerText.replace(/\s+/g,' ')));ok(!r.some(x=>/Mahjong Row/.test(x)),'tile search "'+q+'" -> '+(r.length?r.join(' / '):'none'));}
await p.fill('#tsq','Kaleidoscope');await p.waitForTimeout(350);
const kr=await p.$$eval('[data-tile]',e=>e.filter(x=>x.offsetParent).map(x=>x.innerText.replace(/\s+/g,' ')));ok(kr.some(x=>/Kaleidoscope/.test(x)),'Kaleidoscope tile search -> '+kr.join(' / '));
await p.screenshot({path:OUT+'02-kaleidoscope-search.png'});
await p.fill('#tsq','');await p.click('[data-tcol=az]');await p.waitForTimeout(800);
const all=await p.$$eval('[data-tile]',e=>e.map(x=>x.innerText.replace(/\s+/g,' ')));
ok(all.length>200&&!all.some(x=>/Mahjong Row|Cypress/.test(x)),'All A–Z tile list: '+all.length+' sets, none Mahjong Row/Cypress');
await p.screenshot({path:OUT+'03-tiles-az.png',fullPage:false});
await p.click('[data-tcol=az]');await p.waitForTimeout(300);
// tile colour chips switch + clear
for(const g of ['Blue','Green']){await p.click(`[data-tcol="${g}"]`);await p.waitForTimeout(400);}
const tcolG=await p.evaluate(()=>S.tcol);await p.click('[data-tcol="Green"]');await p.waitForTimeout(400);const tcolC=await p.evaluate(()=>S.tcol);
ok(tcolG==='Green'&&tcolC==='','tile colour chip switch Blue->Green then tap again clears ('+tcolG+' -> "'+tcolC+'")');
// pick Gatsby
await p.fill('#tsq','Gatsby');await p.waitForTimeout(400);await p.click('[data-tile="2"]');await p.waitForTimeout(1500);
await p.screenshot({path:OUT+'04-mats-gatsby.png'});await badIn('mats step (Gatsby)');
const d0=await p.evaluate(()=>queue('m').length);
// colour filter: switch + clear
const pick=async f=>{await p.locator(`[data-fam="${f}"][data-k=m]`).first().click();await p.waitForTimeout(600);return p.evaluate(()=>({fam:S.f.m.fam.slice(),n:queue('m').length,top:(document.querySelector('[data-lbx]')||{}).dataset?.lbx}));};
const a=await pick('blue');await p.screenshot({path:OUT+'05-filter-blue.png'});
const bq=await pick('green');await p.screenshot({path:OUT+'06-filter-green.png'});
const topFams=await p.evaluate(id=>id&&M[id]?[...(M[id].mf||[])]:null,bq.top);
const c=await pick('');
ok(a.fam.join()==='blue'&&a.n>0,'colour blue -> '+a.n+' mats');
ok(bq.fam.join()==='green'&&bq.n>0,'colour switch to green (replaces blue) -> '+bq.n+' mats; top card '+bq.top+' fams '+JSON.stringify(topFams));
ok(c.fam.length===0&&c.n===d0,'All colors clears filter -> '+c.n+' mats (start '+d0+')');
// tap same chip twice clears?
await pick('pink');const tw=await pick('pink');ok(tw.fam.length===0||tw.n>0,'tapping pink twice: fam='+JSON.stringify(tw.fam)+' n='+tw.n+' (not locked)');
if(tw.fam.length)await pick('');
// filter chip states not disabled
const dis=await p.$$eval('[data-fam][data-k=m]',e=>e.filter(x=>x.disabled).length);ok(dis===0,'no colour chip disabled ('+dis+')');
// mat search for parked mats
for(const q of ['Ivy Reverie','Mocha Bloom','The Lodge','Hunt Club','Gatsby','Tracing the Tides','Mahjong Row','Mahjong Co']){const inp=p.locator('#msq');if(!(await inp.count()))break;await inp.fill(q);await p.waitForTimeout(500);
 const t=await p.evaluate(()=>{const s=document.getElementById('msq');let r=s.closest('section,div');for(let k=0;k<3&&r.parentElement;k++)r=r.parentElement;return r.innerText.slice(0,600).replace(/\s+/g,' ');});
 const hits=await p.evaluate(()=>[...document.querySelectorAll('[data-msr],[data-mres],.msr button,[data-mpick]')].filter(e=>e.offsetParent).map(e=>e.innerText.replace(/\s+/g,' ')));
 ok(!hits.some(h=>/Mahjong Row|Mahjong by SI|Mahjong Co\.$/.test(h)||/Ivy Reverie|Mocha Bloom|Tracing the Tides|Vintage Oxblood|Highland Heritage|Osmanthus/.test(h)),'mat search "'+q+'" results: '+(hits.length?hits.slice(0,6).join(' / '):'(none listed)'));}
await p.screenshot({path:OUT+'07-mat-search.png'});await p.locator('#msq').fill('');await p.waitForTimeout(400);
// zoom persists across swipes
await p.locator('[data-z="1"]').first().click();await p.locator('[data-z="1"]').first().click();await p.waitForTimeout(300);
const z1=await p.evaluate(()=>S.zs.mz.s);const top1=await p.evaluate(()=>document.querySelector('[data-lbx]').dataset.lbx);
await p.locator('.sb.no').first().click();await p.waitForTimeout(700);await p.locator('.sb.no').first().click();await p.waitForTimeout(700);
const z2=await p.evaluate(()=>S.zs.mz.s);const top2=await p.evaluate(()=>document.querySelector('[data-lbx]').dataset.lbx);
const tr=await p.evaluate(()=>{const c=document.querySelector('#top-m img');return c?getComputedStyle(c).transform:'?'});
ok(z1>1&&z2===z1&&top1!==top2&&tr!=='none','zoom persists across 2 swipes (scale '+z1+' -> '+z2+', card '+top1+' -> '+top2+', transform '+tr+')');
await p.screenshot({path:OUT+'08-zoom-after-swipes.png'});
await p.locator('[data-z="-1"]').first().click();await p.locator('[data-z="-1"]').first().click();
// swipe gesture (drag) on mobile
if(mob){const bx=await p.locator('#top-m').boundingBox();if(bx){const before=await p.evaluate(()=>document.querySelector('[data-lbx]').dataset.lbx);
 await p.mouse.move(bx.x+bx.width/2,bx.y+bx.height/2);await p.mouse.down();await p.mouse.move(bx.x+bx.width/2-250,bx.y+bx.height/2,{steps:10});await p.mouse.up();await p.waitForTimeout(800);
 const after=await p.evaluate(()=>document.querySelector('[data-lbx]').dataset.lbx);ok(before!==after,'drag-swipe left advances card ('+before+' -> '+after+')');}}
// Tiffany picks on
await p.locator('[data-her=m].chip').first().click();await p.waitForTimeout(600);const hp=await p.evaluate(()=>({her:S.f.m.her,n:queue('m').length}));ok(hp.her&&hp.n>0,'Tiffany picks on for Gatsby -> '+hp.n+' mats');
await p.screenshot({path:OUT+'09-her-picks.png'});await badIn('her picks');
await p.locator('[data-her=m].chip').first().click();await p.waitForTimeout(400);
// heart -> pick -> racks
await p.locator('.sb.yes[data-yes=m]').first().click();await p.waitForTimeout(900);
await p.locator('[data-mock]').first().click();await p.waitForTimeout(1400);
const fav=await p.evaluate(()=>S.fav);ok(!!fav,'picked mat '+fav);
await p.locator('#s-racks').scrollIntoViewIfNeeded().catch(()=>{});await p.screenshot({path:OUT+'10-racks.png'});await badIn('racks');
const rq=await p.evaluate(()=>queue('r'));ok(!rq.some(r=>/mahjongrow/.test(r)),'rack deck has no Mahjong Row ('+rq.length+' racks)');
// rack brand menu
await p.locator('[data-brands=r]').first().click();await p.waitForTimeout(500);const bm=await p.evaluate(()=>document.body.innerText);ok(!/Mahjong Row/.test(bm),'rack Brand menu has no Mahjong Row');
await p.screenshot({path:OUT+'11-rack-brand-menu.png'});
const xb=await p.evaluate(()=>{const c=[...document.querySelectorAll('button')].filter(b=>b.offsetParent&&/^[\u2715\u00d7]$/.test(b.textContent.trim())&&!b.dataset.no);const b=c[c.length-1];if(b){b.click();return Object.keys(b.dataset).join(',')+'|'+b.className}return null});R.closeBtn=xb;await p.waitForTimeout(600);
await p.locator('button.yes[data-yes=r]').last().click();await p.waitForTimeout(800);
R.rdbg=await p.evaluate(()=>({rl:S.rliked,rp:S.rpick,nrp:document.querySelectorAll('[data-rp]').length,nrx:document.querySelectorAll('[data-rx]').length,closeB:0}));console.log(JSON.stringify(R.rdbg),R.closeBtn);await p.screenshot({path:OUT+'11b.png'});await p.locator('[data-rp]').first().click({force:true,timeout:5000});await p.waitForTimeout(800);
await p.locator('[data-make]').first().click({force:true});await p.waitForTimeout(3500);
await p.locator('#s-card').scrollIntoViewIfNeeded().catch(()=>{});await p.waitForTimeout(800);
const ct=await p.evaluate(()=>{const c=document.getElementById('s-card');return c?c.innerText:''});
await p.screenshot({path:OUT+'12-card.png'});
R.cardHasCodeText=/MAHJMATCH/.test(ct);
const shareBtns=await p.$$eval('#s-card button, #s-card a',e=>e.filter(x=>x.offsetParent).map(x=>(x.innerText||x.getAttribute('aria-label')||'').trim().slice(0,30)+'|'+Object.keys(x.dataset).join(',')));
R.cardText=ct.slice(0,900);R.cardButtons=shareBtns;
// card image render
const cv=await p.evaluate(()=>{const c=document.querySelector('#s-card canvas');if(!c)return null;try{return {w:c.width,h:c.height,u:c.toDataURL('image/jpeg',.85)}}catch(e){return {w:c.width,h:c.height,err:e.message}}});
if(cv&&cv.u){require('fs').writeFileSync(OUT+'13-card-canvas.jpg',Buffer.from(cv.u.split(',')[1],'base64'));}
R.canvas=cv?cv.w+'x'+cv.h:'none';const pv=await p.evaluate(()=>[...document.querySelectorAll('#s-card img')].filter(i=>i.offsetParent).map(i=>i.naturalWidth+'x'+i.naturalHeight+' '+i.src.slice(0,40)));R.cardImgs=pv;ok(pv.some(x=>/^\d{3,}x/.test(x))||(cv&&cv.w>0),'card preview rendered: '+pv.slice(0,3).join(' ; ')+' canvas '+R.canvas);
// share
const sh=p.locator('#s-card [data-share], #s-card [data-sl], #s-card button:has-text("Share")');
if(await sh.count()){await p.evaluate(()=>{navigator.share=async(d)=>{window.__shared=d||{};const f=(d.files||[])[0];if(f){window.__sharedURL=await new Promise(r=>{const fr=new FileReader();fr.onload=()=>r(fr.result);fr.readAsDataURL(f);});}};navigator.canShare=()=>true;});
 await sh.first().click({force:true});await p.waitForTimeout(2000);const shared=await p.evaluate(()=>window.__shared?{text:window.__shared.text,url:window.__shared.url,title:window.__shared.title,files:(window.__shared.files||[]).map(f=>f.name+' '+f.size)}:null);
 const vis=await p.evaluate(()=>document.body.innerText.slice(-600));R.share={shared,tailText:vis};ok(!!shared||/copied|Copied|link/i.test(vis),'share action fired '+JSON.stringify(shared).slice(0,300));
 await p.waitForTimeout(1500);const su=await p.evaluate(()=>window.__sharedURL||null);if(su)require('fs').writeFileSync(OUT+'13-shared-card.png',Buffer.from(su.split(',')[1],'base64'));
await p.screenshot({path:OUT+'14-share.png'});
// discount code reveal
const dch=await p.$$eval('#s-card a.dc',e=>e.map(x=>x.href));ok(dch.length>0&&dch.every(h=>/mahjmatchmaker\.com\/.*discount-code/.test(h)),'Discount code links -> '+dch.join(' , '));const dc={count:async()=>0};if(await dc.count()){await dc.click();await p.waitForTimeout(700);const t2=await p.evaluate(()=>document.body.innerText);R.dcReveal=(t2.match(/.{0,80}MAHJMATCH.{0,80}/s)||[''])[0];ok(/MAHJMATCH/.test(t2),'Discount code button reveals MAHJMATCH: '+R.dcReveal.replace(/\s+/g,' '));await p.screenshot({path:OUT+'15-discount-code.png'});}}else ok(false,'no share button found in card ('+shareBtns.join(' ; ')+')');
// ===== MAT DOOR
await p.goto('http://localhost:8116/index.html',{waitUntil:'load'});await p.waitForTimeout(2200);
if(await sk.count()&&await sk.first().isVisible())await sk.first().click();
await p.click('[data-door=mat]');await p.waitForTimeout(1500);await p.screenshot({path:OUT+'20-matdoor.png'});
await badIn('mat door');
const dn=await p.evaluate(()=>doorMats().length);
const dbrands=await p.evaluate(()=>[...new Set(doorMats().map(id=>M[id].bn))]);ok(!dbrands.some(x=>/Mahjong Row|Mahjong Co|by SI/.test(x)),'mat door brands ('+dbrands.length+') exclude Mahjong Row / Mahjong Co. mats');
const chips=await p.$$eval('[data-dfam],[data-dcol],[data-fam]',e=>e.filter(x=>x.offsetParent).map(x=>Object.entries(x.dataset).map(([k,v])=>k+'='+v).join(',')));R.doorChips=chips.slice(0,30);
const dsel=chips.find(c=>/dfam=blue|dcol=blue|dfam=Blue/.test(c));
const attr=dsel?dsel.split(',')[0].split('='):null;
if(attr){const sel=`[data-${attr[0].replace(/[A-Z]/g,m=>'-'+m.toLowerCase())}="${attr[1]}"]`;await p.locator(sel).first().click();await p.waitForTimeout(600);const n1=await p.evaluate(()=>({f:S.dfams,n:doorMats().length}));
 const gsel=sel.replace(/"blue"|"Blue"/,m=>m.replace(/blue/i,'green'));await p.locator(gsel).first().click();await p.waitForTimeout(600);const n2=await p.evaluate(()=>({f:S.dfams,n:doorMats().length}));await p.screenshot({path:OUT+'21-matdoor-green.png'});
 await p.locator(gsel).first().click();await p.waitForTimeout(600);const n3=await p.evaluate(()=>({f:S.dfams,n:doorMats().length}));
 if(n3.f&&n3.f.length){const clr=p.locator('[data-dfam=""],[data-dclear]');if(await clr.count()){await clr.first().click();await p.waitForTimeout(500);}}
 const n4=await p.evaluate(()=>({f:S.dfams,n:doorMats().length}));
 ok(n1.n>0&&n2.n>0&&(n4.f||[]).length===0&&n4.n===dn,'mat door colour: blue '+JSON.stringify(n1)+' -> green '+JSON.stringify(n2)+' -> tap again '+JSON.stringify(n3)+' -> cleared '+JSON.stringify(n4)+' (all '+dn+')');}
else ok(false,'mat door colour chips not found: '+chips.slice(0,10).join(' ; '));
// mat door search
const ds=await p.$$eval('#app input',e=>e.filter(x=>x.offsetParent).map(x=>x.id||x.getAttribute('aria-label')));R.doorInputs=ds;
const dinp=p.locator('#app input:visible').first();
for(const q of ['Ivy Reverie','Lodge','Hunt Club','Gatsby','Mocha','Mahjong Row']){if(!(await dinp.count()))break;await dinp.fill(q);await p.waitForTimeout(500);
 const hits=await p.$$eval('[data-dmat],[data-dm]',e=>e.filter(x=>x.offsetParent).map(x=>x.innerText.replace(/\s+/g,' ').slice(0,60)));ok(!hits.some(h=>/Mahjong Row|Mahjong by SI|Mahjong Co\.$/.test(h)||/Ivy Reverie|Mocha Bloom|Tracing the Tides|Vintage Oxblood|Highland Heritage|Osmanthus/.test(h)),'mat door search "'+q+'" -> '+(hits.slice(0,6).join(' / ')||'none'));}
await p.screenshot({path:OUT+'22-matdoor-search.png'});await dinp.fill('').catch(()=>{});await p.waitForTimeout(500);
// pick Sunday Rattan or first mat
const mbtn=p.locator('[data-dmat]:visible, [data-dm]:visible').first();const mid=await mbtn.evaluate(e=>e.dataset.dmat||e.dataset.dm).catch(()=>null);
if(mid){await mbtn.click();await p.waitForTimeout(1500);}
await p.screenshot({path:OUT+'23-matdoor-tiles.png'});await badIn('tile swipe (mat first)');
const tdeck=await p.evaluate(()=>({mat:S.dmat,n:tq().length,names:tAll().map(r=>r.s.name+'·'+r.s.maker)}));R.tdeck=tdeck.names.slice(0,15);
ok(tdeck.n>0&&!tdeck.names.some(x=>/Mahjong Row|Cypress/.test(x)),'mat-first tile deck for '+tdeck.mat+': '+tdeck.n+' sets, no Mahjong Row');
// heart a tile set
const ty=p.locator('[data-tyes], .sb.yes:visible').first();if(await ty.count()){await ty.click({force:true});await p.waitForTimeout(1200);}
await p.screenshot({path:OUT+'24-matdoor-after-heart.png'});
for(const q of ['Cypress','Oakley','Mahjong Row','Ash Burl']){const ti=p.locator('#tdq');if(!(await ti.count()))break;await ti.fill(q);await p.waitForTimeout(500);const h=await p.$$eval('[data-tfront]',e=>e.filter(x=>x.offsetParent).map(x=>x.innerText.replace(/\s+/g,' ')));ok(!h.some(x=>/Mahjong Row|Cypress/.test(x)),'mat-door tile search "'+q+'" -> '+(h.join(' / ')||'none'));}
await p.locator('#tdq').fill('Kaleidoscope').catch(()=>{});await p.waitForTimeout(500);R.kalTdq=await p.$$eval('[data-tfront]',e=>e.filter(x=>x.offsetParent).map(x=>x.innerText.replace(/\s+/g,' ')));ok(R.kalTdq.some(x=>/Kaleidoscope/.test(x)),'mat-door tile search Kaleidoscope -> '+R.kalTdq.join(' / '));
await p.locator('#tdq').fill('').catch(()=>{});await p.waitForTimeout(400);
R.afterHeart=await p.evaluate(()=>({step:S.step,set:S.set,tl:S.tliked,fav:S.fav}));
const tpk=p.locator('[data-tpk]').first();if(await tpk.count()){await tpk.click({force:true});await p.waitForTimeout(1000);await p.locator('[data-tadd]').first().click({force:true,timeout:5000}).catch(e=>console.log('tadd',e.message.slice(0,80)));await p.waitForTimeout(1500);}
R.afterTpk=await p.evaluate(()=>({step:S.step,set:S.set,setName:S.set!=null?D.sets[S.set].name:null,fav:S.fav}));
await p.screenshot({path:OUT+'25-matdoor-racks.png'});
const ry=p.locator('button.yes[data-yes=r]');if(await ry.count()){await ry.last().click();await p.waitForTimeout(800);await p.locator('[data-rp]').first().click({force:true,timeout:5000}).catch(()=>{});await p.waitForTimeout(600);await p.locator('[data-make]').first().click({force:true,timeout:5000}).catch(()=>{});await p.waitForTimeout(3000);}
await p.evaluate(()=>{navigator.share=async(d)=>{window.__shared=d||{};const f=(d.files||[])[0];if(f){window.__sharedURL=await new Promise(r=>{const fr=new FileReader();fr.onload=()=>r(fr.result);fr.readAsDataURL(f);});}};navigator.canShare=()=>true;window.__sharedURL=null;});
await p.locator('#s-card').scrollIntoViewIfNeeded().catch(()=>{});await p.screenshot({path:OUT+'26-matdoor-card.png'});
const sh2=p.locator('#s-card [data-share]');if(await sh2.count()){await sh2.first().click({force:true});await p.waitForTimeout(3500);const su2=await p.evaluate(()=>window.__sharedURL);if(su2){require('fs').writeFileSync(OUT+'27-matdoor-shared-card.png',Buffer.from(su2.split(',')[1],'base64'));}ok(!!su2,'mat-door card shared ('+JSON.stringify(R.afterTpk)+')');}else ok(false,'mat-door: no card share button '+JSON.stringify(R.afterTpk));
R.errs=errs;ok(errs.length===0,'no page errors ('+errs.length+')');
require('fs').writeFileSync(OUT+'result.json',JSON.stringify(R,null,1));
console.log(R.checks.join('\n'));console.log('FAILS',R.fails.length);await b.close()})();
