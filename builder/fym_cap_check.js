// v113 QA (Nov 1): runs the page's OWN decks in Chromium and checks the per-brand cap + search hygiene.
//  [140] brand cap on the decks people actually swipe: mat-door tile deck tAll() for every visible mat, tiles-door mat deck matDeck()
//        for every visible set, rack deck rackDeck() for every set (picks on + off): in the first 30 non-exempt cards no brand > 6
//        (when >= 5 brands are available) and no avoidable back-to-back same brand. Exempt: her picks.
//  [142] search: #rsq / #msq never return hidden racks / mats, and no result image has src 'undefined'.
// Usage: node fym_cap_check.js <build dir>  -> prints JSON {fail:[...]} ; exit 1 on failures
const {chromium}=require('playwright');const http=require('http');const fs=require('fs');const path=require('path');
const B=process.argv[2];const MIME={'.html':'text/html','.js':'text/javascript','.json':'application/json','.webp':'image/webp','.jpg':'image/jpeg','.png':'image/png'};
const srv=http.createServer((q,r)=>{const p=path.join(B,decodeURIComponent(q.url.split('?')[0]));fs.readFile(p,(e,d)=>{if(e){r.writeHead(404);r.end();return;}r.writeHead(200,{'Content-Type':MIME[path.extname(p)]||'application/octet-stream'});r.end(d);});});
srv.listen(0,async()=>{const port=srv.address().port;const b=await chromium.launch();const fail=[];let out={};
try{const p=await b.newPage({viewport:{width:390,height:844}});await p.route(/supabase\.co|jsdelivr|googleapis|gstatic/,r=>r.abort());
 await p.goto(`http://localhost:${port}/index.html`,{waitUntil:'load',timeout:120000});await p.waitForFunction(()=>window.__imgsReady,null,{timeout:120000});
 out=await p.evaluate(()=>{const F=[];
  const st=(A,bo,keep)=>{const f=A.slice(0,30);const cnt={};let adj=0,prev=null;const brands=new Set(A.filter(x=>!keep(x)).map(bo));
   f.forEach((x,i)=>{if(keep(x)){prev=null;return;}const b=bo(x);cnt[b]=(cnt[b]||0)+1;if(prev===b&&A.slice(i).some(y=>!keep(y)&&bo(y)!==b))adj++;prev=b;});
   const mx=Object.entries(cnt).sort((a,b)=>b[1]-a[1])[0]||['',0];return {bad:(mx[1]>6&&brands.size>=5)||adj>0,mx,adj};};
  S.ins=false;S.door='mat';let n1=0;
  for(const id of Object.keys(M).filter(i=>!M[i].hid&&!M[i].rt)){S.dmat=id;S.tfront=null;S.tseen={};const A=tAll();n1++;const s=st(A,r=>TB(r.s),r=>r.her);if(s.bad&&F.length<40)F.push(`[140] mat-door tile deck for ${M[id].n}: ${s.mx[0]} ${s.mx[1]} of 30, back-to-back ${s.adj}`);}
  S.door='tiles';const VS=D.sets.map((s,i)=>[s,i]).filter(([s])=>VIS(s));let n2=0;
  for(const [s,i] of VS){S.set=i;S.f.m={fam:[],brand:'',her:false,multi:false};S.mfront=null;S.seen={};const A=matDeck();n2++;const x=st(A,id=>M[id].bn,()=>false);if(x.bad&&F.length<60)F.push(`[140] mat deck for ${s.name}: ${x.mx[0]} ${x.mx[1]} of 30, back-to-back ${x.adj}`);
   S.fav=(s.m[0]||[])[0]||A[0];if(!S.fav||!M[S.fav])continue;for(const her of [false,true]){S.f.r={fam:[],brand:'',her,fin:''};S.rseen={};const hr=herRacks();const q=rackDeck();const y=st(q,r=>R[r].bn,r=>hr.includes(r));if(y.bad&&F.length<80)F.push(`[140] rack deck (picks ${her?'on':'off'}) for ${s.name}: ${y.mx[0]} ${y.mx[1]} of 30, back-to-back ${y.adj}`);}}
  // search hygiene
  const QS=['wood','solid wood','tortoise','pearl','clear','white','pink','register','mahjong','acrylic','walnut','lucite','christmas','floral','besties','queen'];
  const fire=(id,v)=>{const el=document.getElementById(id);if(!el)return null;el.value=v;el.dispatchEvent(new Event('input',{bubbles:true}));return el;};
  for(const v of QS){if(fire('rsq',v)){document.querySelectorAll('#rsr [data-rown]').forEach(e=>{const r=R[e.dataset.rown];if(!r||r.hid)F.push(`[142] rack search '${v}' returns hidden rack ${e.dataset.rown}`);});document.querySelectorAll('#rsr img').forEach(i=>{if(/undefined/.test(i.getAttribute('src')||''))F.push(`[142] rack search '${v}': img src undefined`);});}
   if(fire('msq',v)){document.querySelectorAll('#msr [data-mfront],#msr [data-mid],#msr [data-id]').forEach(e=>{const id=e.dataset.mfront||e.dataset.mid||e.dataset.id;const m=M[id];if(m&&m.hid)F.push(`[142] mat search '${v}' returns hidden mat ${id}`);});document.querySelectorAll('#msr img').forEach(i=>{if(/undefined/.test(i.getAttribute('src')||''))F.push(`[142] mat search '${v}': img src undefined`);});}}
  fire('rsq','');fire('msq','');
  return {F:[...new Set(F)],n1,n2,nsets:VS.length};});
 fail.push(...out.F);
}catch(e){fail.push('[140] cap check did not run: '+String(e).slice(0,200));}
console.log(JSON.stringify({fail,matDoorMats:out.n1,sets:out.n2}));await b.close();srv.close();process.exit(fail.length?1:0);});
