"""v105 / Version 1.9 (Oct 30): step-2 layout = the MAT-DOOR model + search at every step.
Tiffany 11:45am ("use this as a tabletop tool") + 11:53am (keep the two pictures together; controls below; she missed the mat search
because it sat above the tile photo, out of frame; the mat door had no tile search).
Usage: python3 patch105.py <src index.html> <out index.html>
- BOTH doors, step 2: chosen item's photo + label bar, then the swipe card directly underneath (touching). View (Up close/Aerial),
  the filter row (Tiffany's picks, Brand, colour) and the search box move BELOW the deck, above the bottom X/heart row.
- tiles door: the existing mat search (msq) moves below the deck: 'Search any mat by name or brand' (pick = that mat on top)
- mat door: NEW tile-set search (tdq) below the deck: pick = that set becomes the current tile card on this mat
- racks: the rack search button says it searches every rack
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
MSQ='`<div class="msearch"><input id="msq" type="search" enterkeyhint="search" placeholder="Already own a mat? Search by name or brand" autocomplete="off" aria-label="Search mats"><div id="msr" class="msr" role="listbox"></div></div>`'
MSQ2='<div class="msearch s2"><input id="msq" type="search" enterkeyhint="search" placeholder="Search any mat by name or brand" autocomplete="off" aria-label="Search mats"><div id="msr" class="msr" role="listbox"></div></div>'
rep("+"+MSQ+"+","+")
rep("(S.mode==='close'?`<div class=\"cmp\">${tileView('m')}<div class=\"tcap\"><span>${esc(s.name)} tiles</span>${backBtn()}</div>${VROW()}<div class=\"rfil mfil\">${filters('m')}</div>${deck('m')}</div>`:`<div class=\"backrow\">${backBtn()}</div>${VROW()}<div class=\"rfil mfil\">${filters('m')}</div><div class=\"cmp aer\">${deck('m')}</div>`)+acts('m')",
    "(S.mode==='close'?`<div class=\"cmp\">${tileView('m')}<div class=\"tcap\"><span>${esc(s.name)} tiles</span>${backBtn()}</div>${deck('m')}</div>`:`<div class=\"backrow\">${backBtn()}</div><div class=\"cmp aer\">${deck('m')}</div>`)+`<div class=\"s2ctl\">${VROW()}<div class=\"rfil mfil\">${filters('m')}</div>"+MSQ2+"</div>`+acts('m')")
rep("S.mfront=id;S.mfset=S.set;","S.mfront=id;S.mfset=S.set;trk('search2',{door:'tiles',set:set().slug,mat:id});")
# 2. mat door step 2: View + NEW tile-set search box BELOW the deck (photo and card touch)
rep('`<div class="shrow">${head(2,\'Swipe the tiles\',sub)}<button type="button" class="chip" data-dgrid="1">See all</button></div>`+\n  VROW()+',
    '`<div class="shrow">${head(2,\'Swipe the tiles\',sub)}<button type="button" class="chip" data-dgrid="1">See all</button></div>`+\n  ')
rep('<button type="button" class="backb" data-tback>‹ Back</button>\':\'\'}</div>${deck}</div>`)+acts+tray;',
    '<button type="button" class="backb" data-tback>‹ Back</button>\':\'\'}</div>${deck}</div>`)+`<div class="s2ctl">${VROW()}<div class="msearch s2"><input id="tdq" type="search" enterkeyhint="search" placeholder="Search any tile set by name or brand" autocomplete="off" aria-label="Search tile sets for this mat"><div id="tdr" class="msr" role="listbox"></div></div></div>`+acts+tray;')
CSS='''.s2ctl{margin:10px 0 4px;padding:8px 10px 2px;border-radius:16px;background:#fff5f8;border:1px solid #f3d3df}.s2ctl .vrow{margin:0 0 6px}.s2ctl .rfil{margin:2px 0 6px}.msearch.s2{margin:4px 0 6px}.msearch.s2 .msr{position:relative}
'''
i_=h.rindex('</style></head>'); h=h[:i_]+CSS+h[i_:]
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
# 4. X / heart on the LEFT / RIGHT of the swipe card in BOTH doors (Tiffany 11:53am: she never scrolls down to the bottom buttons;
#    the old side X/heart were only the one-time swipe cue). Bottom buttons stay for now.
rep("acts('m')+herBar('m')+tray('m');\n bindCard('m');","acts('m')+herBar('m')+tray('m');\n addSB(el,'m');bindCard('m');")
rep("+acts+tray;\n const t=$('tv-d');","+acts+tray;\n addSB(el,'t');const t=$('tv-d');")
SB="function addSB(el,k){const d=el.querySelector('.deck');if(!d||d.querySelector('.sbx'))return;const ok=k==='m'?(!S.peek&&!matLocked()&&queue('m').length):(S.tpeek==null&&tq().length);if(!ok)return;\n d.insertAdjacentHTML('beforeend',k==='m'?'<div class=\"sbx\"><button type=\"button\" class=\"sb no\" data-no=\"m\" aria-label=\"No thanks\">✕</button><button type=\"button\" class=\"sb yes\" data-yes=\"m\" aria-label=\"Love\">♥</button></div>':'<div class=\"sbx\"><button type=\"button\" class=\"sb no\" data-tno aria-label=\"No thanks\">✕</button><button type=\"button\" class=\"sb yes\" data-tyes aria-label=\"Love\">♥</button></div>');}\n"
rep('const VROW=()=>',SB+'const VROW=()=>')
CSS2=".sbx{position:absolute;left:0;right:0;top:46%;z-index:6;display:flex;justify-content:space-between;padding:0 8px;pointer-events:none}.sbx .sb{pointer-events:auto;width:50px;height:50px;border-radius:50%;border:0;font:700 22px var(--body);display:flex;align-items:center;justify-content:center;background:rgba(255,255,255,.95);box-shadow:0 4px 14px rgba(0,0,0,.22);cursor:pointer}.sbx .sb.no{color:#5e5368}.sbx .sb.yes{color:#c8325f}.deck .swh span{visibility:hidden}\n"
i_=h.rindex('</style></head>'); h=h[:i_]+CSS2+h[i_:]
open(OUT,'w').write(h); print('ok',len(h))
