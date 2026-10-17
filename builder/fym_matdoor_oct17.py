"""Oct 17: Find Your Match second door, "I have a mat" (launch plan item 1-3, doc 54).
Start screen gets two doors. The mat door: pick your mat (search, color chips, most-matched first) ->
tile sets ranked for that mat (Tiffany's matches first, then album sets by the same palette ranking the
tile-first flow uses, then partner catalog sets) -> tap a set and you land on the racks step with that mat.
Usage: python3 fym_matdoor_oct17.py <in index.html> <out index.html>"""
import sys
src, out = sys.argv[1:3]
t = open(src).read()
assert 'data-door' not in t, 'already patched'

CSS = """
.door{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:8px 0 6px}
.door button{border:2px solid var(--line);background:#fff;border-radius:16px;padding:10px 8px;font:700 14px/1.2 var(--body);color:var(--navy);cursor:pointer}
.door button small{display:block;font:500 11px var(--body);color:var(--mute);margin-top:2px}
.door button[aria-pressed="true"]{border-color:var(--pink);background:#fff5f8;box-shadow:0 0 0 3px rgba(217,70,127,.18)}
.mgrid img{border-radius:12px!important}
.dsets .her{display:block;font:700 10px var(--body);color:var(--pink);letter-spacing:.06em}
.dmore{display:block;margin:4px auto 14px;border:1.5px solid var(--line);background:#fff;border-radius:999px;padding:8px 16px;font:700 13px var(--body);color:var(--navy);cursor:pointer}
.dsub{text-align:center;font:600 13px var(--body);color:var(--mute);margin:10px 0 6px}
"""
t = t.replace('</style>', CSS + '</style>', 1)

JS = r"""
const DOOR={cnt:null,lim:36,slim:18};
function matCounts(){if(DOOR.cnt)return DOOR.cnt;const c={};D.sets.forEach(s=>s.m.forEach(x=>{c[x[0]]=(c[x[0]]||0)+1;}));return DOOR.cnt=c;}
function doorBtns(){const d=S.door||'tiles';return `<div class="door" role="group" aria-label="Start with"><button type="button" data-door="tiles" aria-pressed="${d==='tiles'}">I have tiles<small>Find the mat they’re meant for</small></button><button type="button" data-door="mat" aria-pressed="${d==='mat'}">I have a mat<small>Find tiles that match it</small></button></div>`;}
function doorMats(){const c=matCounts();let ids=Object.keys(M).filter(id=>!M[id].rt||c[id]);if(S.dfam)ids=ids.filter(id=>(M[id].mf||[]).includes(S.dfam));
 return ids.sort((a,b)=>(c[b]||0)-(c[a]||0)||M[a].n.localeCompare(M[b].n));}
function matBtn(id){return `<button type="button" data-dmat="${esc(id)}"><img src="${matTh(id)}" alt="" loading="lazy"><span>${esc(M[id].n)}</span><small>${esc(M[id].bn||'')}</small></button>`;}
function doorChips(){return `<div class="tchips" role="group" aria-label="Mats by color"><p>Mats by color</p><button type="button" data-dfam="" aria-pressed="${!S.dfam}" style="--c:#1f3a6b">Most matched</button>`+FAMS.map(f=>`<button type="button" data-dfam="${f}" aria-pressed="${S.dfam===f}" style="--c:${FAMC[f]}">${FAMN[f]}</button>`).join('')+`</div>`;}
function setsForMat(id){const ix=D.order.indexOf(id);const rows=D.sets.map((s,i)=>{const her=s.m.some(x=>x[0]===id);const p=ix<0?1e9:s.rank.indexOf(ix);return {s,i,her,p:p<0?1e9:p};});
 const HOL=new Set(BACKG.Holiday||[]);const ok=r=>M[id].hol||!HOL.has(r.s.name);const her=rows.filter(r=>r.her),alb=rows.filter(r=>!r.her&&!r.s.cat&&ok(r)).sort((a,b)=>a.p-b.p),cat=rows.filter(r=>!r.her&&r.s.cat&&ok(r)).sort((a,b)=>a.p-b.p);return {her,alb,cat};}
function dsetBtn(r){return `<button type="button" data-dset="${r.i}"><img src="${pile(r.s)}" alt="" loading="lazy"><span>${esc(r.s.name)}</span><small>${esc(r.s.maker)}</small>${r.her?'<b class="her">♥ Tiffany’s match</b>':''}</button>`;}
function renderMatDoor(el){const lock=`<div class="lock"><div class="eb">mahjmatchmaker.com</div><h1 class="ttl">Find Your Match</h1><div class="by">Already have your mat? Let’s find the tiles it’s been waiting for.</div></div>`;
 if(!S.dmat){const ids=doorMats();el.innerHTML=lock+doorBtns()+doorChips()+`<div class="msearch"><input id="mdq" type="search" enterkeyhint="search" placeholder="Search your mat by name or brand" autocomplete="off" aria-label="Search mats"></div><div class="tgrid mgrid" id="mdgrid">${ids.slice(0,DOOR.lim).map(matBtn).join('')}</div>`+(ids.length>DOOR.lim?`<button type="button" class="dmore" data-dmore="m">Show more mats</button>`:'');return;}
 const m=M[S.dmat];const g=setsForMat(S.dmat);const n=S.dshow||DOOR.slim;
 el.innerHTML=lock+doorBtns()+`<div class="picked"><span class="num">1</span><img src="${matTh(S.dmat)}" alt=""><div class="tx"><i>Your mat</i><b>${esc(m.n)}</b><small>${esc(m.bn||'')}</small></div><button type="button" class="chip" data-dchange>Change</button></div>`+
 (g.her.length?`<p class="dsub">Tiffany matched this mat with ${g.her.length} tile set${g.her.length>1?'s':''}</p><div class="tgrid dsets">${g.her.map(dsetBtn).join('')}</div>`:`<p class="dsub">Tiffany hasn’t matched this mat yet. These tile sets are the closest color matches.</p>`)+
 `<p class="dsub">${g.her.length?'More tile sets that suit it':'Best color matches'}</p><div class="tgrid dsets">${g.alb.slice(0,n).map(dsetBtn).join('')}</div>`+
 (g.alb.length>n?`<button type="button" class="dmore" data-dmore="s">Show more tile sets</button>`:'')+
 (S.dcat?`<p class="dsub">From our partner brands</p><div class="tgrid dsets">${g.cat.slice(0,24).map(dsetBtn).join('')}</div>`:(g.cat.length?`<button type="button" class="dmore" data-dmore="c">Show partner brands’ tile sets</button>`:''));}
document.addEventListener('click',e=>{const q=s=>e.target.closest&&e.target.closest(s);let b;
 if(b=q('[data-door]')){S.door=b.dataset.door;S.tilesOpen=true;renderTiles();return;}
 if(b=q('[data-dfam]')){S.dfam=b.dataset.dfam;DOOR.lim=36;renderTiles();return;}
 if(b=q('[data-dmat]')){S.dmat=b.dataset.dmat;S.dshow=0;S.dcat=false;renderTiles();window.scrollTo({top:0,behavior:'smooth'});return;}
 if(q('[data-dchange]')){S.dmat=null;renderTiles();return;}
 if(b=q('[data-dmore]')){const k=b.dataset.dmore;if(k==='m')DOOR.lim+=36;else if(k==='s')S.dshow=(S.dshow||DOOR.slim)+18;else S.dcat=true;renderTiles();return;}
 if(b=q('[data-dset]')){const i=+b.dataset.dset;resetFrom(1);S.set=i;S.f.m.her=set().m.length>0;resetFrom(2);S.fav=S.dmat;S.tilesOpen=false;renderAll();jump('s-racks');return;}
});
document.addEventListener('input',e=>{if(e.target.id!=='mdq')return;const v=e.target.value.trim().toLowerCase(),g=$('mdgrid');if(!g)return;if(v.length<2){g.innerHTML=doorMats().slice(0,DOOR.lim).map(matBtn).join('');return;}
 const toks=v.split(/\s+/);const hits=Object.keys(M).filter(id=>{const s=(M[id].n+' '+(M[id].bn||'')).toLowerCase();return toks.every(k=>s.includes(k));}).slice(0,60);g.innerHTML=hits.length?hits.map(matBtn).join(''):'<p class="hint" style="grid-column:1/-1">No mats match that yet.</p>';});
"""

# 1) door buttons on the tile start screen + route to the mat door
old = "function renderTiles(){const el=$('s-tiles');"
assert old in t
t = t.replace(old, old + "\n if((S.set==null||S.tilesOpen)&&S.door==='mat'){renderMatDoor(el);return;}", 1)
old2 = '<div class="how"><div><b>1</b>Swipe on mats</div>'
assert old2 in t
t = t.replace(old2, '${doorBtns()}' + old2, 1)
# 2) functions + handlers before the first document click listener
anchor = "document.addEventListener('click',e=>{const q=s=>e.target.closest(s);let b;"
assert anchor in t
t = t.replace(anchor, JS + anchor, 1)
open(out, 'w').write(t)
print('patched', len(t))
