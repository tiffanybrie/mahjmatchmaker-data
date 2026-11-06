const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:390,height:844}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://localhost:8116/index.html',{waitUntil:'load',timeout:120000});await p.waitForTimeout(2500);
const r=await p.evaluate(()=>{
 const out={fails:[],info:{}};
 const PM=id=>/^mahjongrowandco\.com\//.test(id)||/^mahjongco\.com\//.test(id);
 const PR=id=>/^mahjongrowandco\.com\//.test(id)||/Mahjong Row/.test((R[id]||{}).bn||'');
 const PS=s=>/Mahjong Row/.test(s.maker)||/mahjongrow/.test(s.tile)||/cypress/i.test(s.slug);
 const vis=D.sets.map((s,i)=>[s,i]).filter(([s])=>VIS(s));
 out.info.visibleSets=vis.length;
 vis.forEach(([s])=>{if(PS(s))out.fails.push('visible set '+s.name)});
 const kal=vis.find(([s])=>/Kaleidoscope/.test(s.name));out.info.kaleidoscope=!!kal;if(!kal)out.fails.push('Kaleidoscope missing');
 // visible mats overall
 const vm=Object.keys(M).filter(id=>!M[id].hid);out.info.visibleMats=vm.length;
 vm.forEach(id=>{if(PM(id)||/Mahjong Row|Mahjong Co|Mahjong by SI/.test(M[id].bn||''))out.fails.push('visible mat '+id)});
 const vr=Object.keys(R).filter(id=>!R[id].hid);vr.forEach(id=>{if(PR(id))out.fails.push('visible rack '+id)});
 const vt=Object.keys(T).filter(id=>!T[id].hid);vt.forEach(id=>{if(/mahjongrow/.test(id)||/Mahjong Row/.test(T[id].bn||''))out.fails.push('visible tile '+id)});
 const fams=[[],...FAMS.map(c=>[c]),['holiday']];
 let deckChecks=0,rackChecks=0,empty=[];const errs=[];
 const save=JSON.stringify(S);
 vis.forEach(([s,i])=>{
  S.set=i;
  for(const her of [false,true])for(const fam of fams){S.f.m={fam:fam.slice(),brand:'',her};S.seen={};
   let d;try{d=matDeck();}catch(e){errs.push(s.name+' '+fam+' '+e.message);continue}
   deckChecks++;d.forEach(id=>{if(PM(id)||!M[id]||M[id].hid)out.fails.push('deck '+s.name+'/'+fam+' -> '+id)});
   if(!her&&!fam.length){ if(!d.length)empty.push(s.name);
     d.slice(0,4).forEach(mid=>{S.fav=mid;S.f.r={fam:[],brand:'',her:false};S.rseen={};
       try{const rd=rackDeck();rackChecks++;rd.forEach(r=>{if(PR(r)||!R[r]||R[r].hid)out.fails.push('rack '+s.name+'/'+mid+' -> '+r)});
       const hr=herRacks().filter(r=>R[r]&&!R[r].hid);hr.forEach(r=>{if(PR(r))out.fails.push('herRack '+r)});}catch(e){errs.push('rack '+s.name+' '+e.message)}});
   }}
 });
 out.info.deckChecks=deckChecks;out.info.rackChecks=rackChecks;out.info.emptyDecks=empty;
 // her picks for named sets
 const want=['Gatsby','Heritage 2.0','Smith','Osler','Sunday'];
 out.info.picks={};
 vis.forEach(([s,i])=>{if(want.some(w=>s.name.includes(w))){S.set=i;S.f.m={fam:[],brand:'',her:true};S.seen={};let d=[];try{d=matDeck()}catch(e){};const vm=s.m.filter(x=>M[x[0]]&&!M[x[0]].hid).length;out.info.picks[s.name+' ('+s.maker+')']={herVisible:vm,herDeck:d.length,mTotal:s.m.length};}});
 // mat door
 let doorN=0,setCh=0;
 for(const fam of fams){S.dfams=fam.slice();S.mbr='';let dm;try{dm=doorMats()}catch(e){errs.push('door '+e.message);continue}
  if(!fam.length)out.info.doorMats=dm.length;
  dm.forEach(id=>{doorN++;if(PM(id)||M[id].hid)out.fails.push('door mat '+id)});}
 S.dfams=[];const dm=doorMats();
 dm.forEach(id=>{let g;try{g=setsForMat(id)}catch(e){errs.push('sfm '+id+' '+e.message);return}setCh++;
   [...(g.her||[]),...(g.alb||[]),...(g.cat||[])].forEach(r=>{if(PS(r.s)||!VIS(r.s))out.fails.push('setsForMat '+id+' -> '+r.s.name)})});
 out.info.doorChecks=doorN;out.info.setsForMatChecks=setCh;
 // brand lists
 out.info.logosInDoorBrands=[...new Set(Object.keys(M).filter(id=>!M[id].hid).map(id=>M[id].bn))].filter(b=>/Mahjong Row|Mahjong Co|by SI/.test(b));
 out.errs=errs.slice(0,20);out.nErrs=errs.length;
 return out;});
r.fails=[...new Set(r.fails)];
console.log(JSON.stringify(r,null,1).slice(0,6000));console.log('PAGEERR',errs);await b.close()})();
