"""v105 / Version 1.9: search at EVERY step (Tiffany Oct 30 11:45am: "use this as a tabletop tool").
Usage: python3 patch105.py <src index.html> <out index.html>
- tiles door step 2: the existing mat search (msq) is relabelled 'Search any mat by name or brand' (pick = that mat on top of the deck)
- mat door step 2: NEW tile-set search (tdq): pick = that set becomes the current tile card on this mat
- racks: the rack search button is relabelled 'Search any rack by name or brand'
- trk('search2') on every pick
"""
import sys
SRC,OUT=sys.argv[1],sys.argv[2]
h=open(SRC).read()
def rep(a,b,n=1):
    global h
    c=h.count(a); assert c==n,(c,a[:90]); h=h.replace(a,b)
rep('<title>Find Your Mat-ch (Version 1.8)</title>','<title>Find Your Mat-ch (Version 1.9)</title>')
rep('color:var(--mute)">Version 1.8</small>','color:var(--mute)">Version 1.9</small>')
# 1. tiles door step 2: the mat search says what it does
rep('placeholder="Already own a mat? Search by name or brand"','placeholder="Search any mat by name or brand"')
rep("S.mfront=id;S.mfset=S.set;","S.mfront=id;S.mfset=S.set;trk('search2',{door:'tiles',set:set().slug,mat:id});")
# 2. mat door step 2: tile-set search box above the View row
rep('`<div class="shrow">${head(2,\'Swipe the tiles\',sub)}<button type="button" class="chip" data-dgrid="1">See all</button></div>`+\n  VROW()+',
    '`<div class="shrow">${head(2,\'Swipe the tiles\',sub)}<button type="button" class="chip" data-dgrid="1">See all</button></div>`+`<div class="msearch"><input id="tdq" type="search" enterkeyhint="search" placeholder="Search any tile set by name or brand" autocomplete="off" aria-label="Search tile sets for this mat"><div id="tdr" class="msr" role="listbox"></div></div>`+\n  VROW()+')
rep("const tAll=()=>{if(!S.dmat||!M[S.dmat])return [];const g=setsForMat(S.dmat);return [...g.her,...g.alb,...g.cat];};",
    "const tAll=()=>{if(!S.dmat||!M[S.dmat])return [];const g=setsForMat(S.dmat);let A=[...g.her,...g.alb,...g.cat];/*v105 searched set goes on top*/const f=S.tfront;if(f!=null&&S.tfmat===S.dmat&&D.sets[f]&&!S.tseen[f]){const r=A.find(x=>x.i===f)||{s:D.sets[f],i:f,her:false,p:1e9};A=[r,...A.filter(x=>x.i!==f)];}return A;};")
rep("const tReset=()=>{S.mfront=null;S.mfset=null;","const tReset=()=>{S.tfront=null;S.tfmat=null;S.mfront=null;S.mfset=null;")
HANDLERS=r"""
/* v105: search any tile set at the mat door's swipe step (Tiffany Oct 30 11:45am) */
document.addEventListener('input',e=>{if(e.target.id!=='tdq')return;const v=NRM(e.target.value.trim()),box=$('tdr');if(!box)return;if(v.length<2){box.innerHTML='';return;}
 const toks=v.split(/\s+/);const hits=D.sets.map((s,i)=>[s,i]).filter(([s])=>VIS(s)&&toks.every(t=>NRM(s.name+' '+(s.maker||'')).includes(t)))
  .sort((a,b)=>(NRM(a[0].name).startsWith(toks[0])?0:1)-(NRM(b[0].name).startsWith(toks[0])?0:1)||(!!(T[a[0].tile]||{}).soon-!!(T[b[0].tile]||{}).soon)||a[0].name.localeCompare(b[0].name)).slice(0,12);
 box.innerHTML=hits.length?hits.map(([s,i])=>`<button type="button" data-tfront="${i}"><img src="${pile(s)}" alt=""><span><b>${esc(s.name)}</b><small>${esc(s.maker||'')}${(T[s.tile]||{}).so?' · sold out':''}</small></span></button>`).join(''):'<div class="none">No tile set by that name yet. Try the brand name.</div>';});
document.addEventListener('click',e=>{const b=e.target.closest&&e.target.closest('[data-tfront]');if(!b)return;const i=+b.dataset.tfront;if(!D.sets[i]||!S.dmat)return;
 S.tfront=i;S.tfmat=S.dmat;delete S.tseen[i];S.tpeek=null;S.thist=S.thist.filter(x=>x!==i);trk('search2',{door:'mat',mat:S.dmat,set:D.sets[i].slug});
 renderTiles();requestAnimationFrame(()=>{const c=$('top-t');if(c){const y=c.getBoundingClientRect().top+window.scrollY-120;window.scrollTo({top:Math.max(0,y),behavior:'smooth'});}});});
"""
anchor="document.addEventListener('click',e=>{const q=s=>e.target.closest&&e.target.closest(s);let b;\n /*v97 tap chosen tiles = Add racks*/"
rep(anchor,HANDLERS+anchor)
rep("if(!/^(tsq|msq|rsq|mdq)$/.test(e.target.id))return;","if(!/^(tsq|msq|rsq|mdq|tdq)$/.test(e.target.id))return;")
# 3. racks: say it searches every rack
rep('<button type="button" class="ownr" data-rsheet>+ Own racks? Search yours</button>','<button type="button" class="ownr" data-rsheet>+ Search any rack by name or brand</button>')
open(OUT,'w').write(h); print('ok',len(h))
