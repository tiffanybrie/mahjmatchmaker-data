const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('http://localhost:8116/index.html',{waitUntil:'load',timeout:120000});await p.waitForTimeout(2500);
const r=await p.evaluate(()=>{const out={n:0,partner:0,mahj:0,other:{},linkonly:0,none:0,bad:[]};
 D.sets.forEach((s,i)=>{if(!VIS(s))return;S.set=i;S.f.m={fam:[],brand:'',her:false};S.seen={};let d=[];try{d=matDeck()}catch(e){}
  d.slice(0,6).forEach(mid=>{S.fav=mid;S.f.r={fam:[],brand:'',her:false};S.rseen={};let rd=[];try{rd=rackDeck()}catch(e){}
   for(const rp of [[],rd.slice(0,1)]){S.rpick=rp;out.n++;const cl=codeLine();
    const ps=[T[s.tile],M[mid],...rp.map(x=>R[x])].filter(o=>o&&o.pa&&!o.nc);const nl=ps.filter(o=>!LINKONLY[o.bn]);
    if(nl.length){out.partner++;if(/MAHJMATCH/.test(cl))out.mahj++;else{out.other[cl]=(out.other[cl]||0)+1;if(!/Use code \S+ to save/.test(cl))out.bad.push(s.name+' + '+M[mid].n+' => "'+cl+'"')}}
    else if(ps.length){out.linkonly++;if(cl!=='Save through our links')out.bad.push('linkonly '+s.name+'+'+M[mid].n+' => '+cl)}
    else {out.none++;if(cl)out.bad.push('nonpartner '+s.name+'+'+M[mid].n+' => '+cl)}}});});
 const k=D.sets.findIndex(s=>s.slug==='mahjong-co-kaleidoscope');S.set=k;S.fav=matDeck()[0];S.rpick=[];out.kal=codeLine()+' | '+M[S.fav].n+' ('+M[S.fav].bn+')';
 out.bad=out.bad.slice(0,15);return out;});
console.log(JSON.stringify(r,null,1));await b.close()})();
