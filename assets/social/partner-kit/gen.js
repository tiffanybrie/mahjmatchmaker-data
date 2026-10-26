async (args)=>{ const [B,N,EX]=args; const ex=new Set(EX||[]); codeLine=()=>'';
 const reset=()=>{S.f={m:{fam:[],brand:'',her:false},r:{fam:[],brand:'',her:false}};S.seen={};S.rseen={};S.peek=null;S.dmat=null;S.door='tiles';S.mfront=null;};
 const okSet=i=>{const s=D.sets[i];const t=T[s.tile];return t&&!t.soon&&!ex.has(s.name)&&!/travel|mini/i.test(s.name)&&!/Paige/i.test(s.name);};
 const okMat=id=>M[id]&&!M[id].hid&&!M[id].rt&&M[id].pa!==false&&!/Paige/i.test(M[id].n);
 const own=D.sets.map((s,i)=>i).filter(i=>D.sets[i].maker===B&&okSet(i));
 const cands=[];
 if(own.length){ for(const i of own){ S.set=i; reset(); S.f.m.brand=B; const her=D.sets[i].m.map(x=>x[0]).filter(id=>okMat(id)&&M[id].bn===B);
   const rk=matDeck().filter(okMat).filter(id=>!M[id].hol); her.forEach((id,j)=>cands.push([i,id,j])); rk.forEach((id,j)=>cands.push([i,id,50+j])); } }
 else { const mats=Object.keys(M).filter(id=>M[id].bn===B&&okMat(id)&&!M[id].hol);
   D.sets.forEach((s,i)=>{ if(!okSet(i)||!T[s.tile].pa||s.maker==='Mahjong Studios') return; S.set=i; reset(); const cp=colorPool(); const her=new Set(s.m.map(x=>x[0]));
     mats.forEach(id=>{ const r=cp.indexOf(id); if(her.has(id)) cands.push([i,id,r<0?5:r/10]); else if(r>=0) cands.push([i,id,50+r]); }); }); }
 cands.sort((a,b)=>a[2]-b[2]); const pick=[],uS=new Set(),uM=new Set(),uMk=new Set();
 for(const c of cands){ if(pick.length>=N) break; if(uS.has(c[0])||uM.has(c[1])) continue; if(!own.length&&uMk.has(D.sets[c[0]].maker)&&cands.some(d=>!uS.has(d[0])&&!uM.has(d[1])&&!uMk.has(D.sets[d[0]].maker)&&d[2]<c[2]+40)) continue; pick.push(c); uS.add(c[0]); uM.add(c[1]); uMk.add(D.sets[c[0]].maker); }
 const hasR=Object.values(R).filter(r=>r.bn===B).length; const uR=new Set(); const out=[];
 for(const [i,m,sc] of pick){ S.set=i; reset(); S.fav=m; S.f.r.brand=hasR?B:''; let rl=rackDeck().filter(r=>R[r]&&R[r].bn!=='Mahjong Studios'&&!R[r].lo&&R[r].pa!==false); const fresh=rl.filter(r=>!uR.has(r)); const rp=(fresh.length>=2?fresh:fresh.concat(rl.filter(r=>uR.has(r)))).slice(0,2); rp.forEach(r=>uR.add(r));
   S.rpick=rp; S.made=true; S.fmt='story'; S.view='tri'; cardURL=''; await drawCard(); for(let k=0;k<40&&!cardURL;k++) await new Promise(r=>setTimeout(r,250));
   out.push({set:D.sets[i].name,maker:D.sets[i].maker,mat:M[m].n,matBrand:M[m].bn,racks:rp.map(r=>R[r].n+' ('+R[r].bn+')'),score:sc,url:cardURL}); }
 return out; }
