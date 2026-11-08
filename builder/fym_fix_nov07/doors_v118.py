#!/usr/bin/env python3
"""FYM 1.18: the two doors MIRROR (Tiffany Nov 7 10:24pm: "I want to do basically brand lock on the Lotus mat. I just want to put the
Lotus mat in, and then I just only want to see all my Oh My Mahjong tiles... There's no drop down to just select all my Oh My Mahjong.
Like there is if you come in through the other door... make sure everything is mirrored up").

Rule: an item type (tile sets, mats, racks) gets the SAME filters wherever it is chosen: first step of its door, second step of the
other door, the racks step, and the Table view swap sheet. Matrix + gaps: docs/fym-door-parity-nov07.md. Gate [167] (doors_check.py).

What this adds (reusing the app's own chips, dots, Brand sheet, price dropdown and in-stock chip):
  TILE SETS, mat door step 2 (swipe + 'See all' grid): In stock only, Price (was there), Tiffany's picks, Brand (sheet with logos),
    'Same brand as my mat' (brand lock: Lotus Cove -> only Oh My Mahjong tiles, her picks first), Holiday + colour-group dots (the
    tiles door's colour groups). A combination that empties the deck shows everything with 'No tile sets fit all of those' + Clear.
    Filters reset when the mat changes. Tile cards in the 'See all' grid show the price line when a price is picked.
  TILE SETS, tiles door step 1 (grid): In stock only + Price (the mat door's mat grid had in-stock; neither grid had price).
    With in-stock or a price on and no colour/brand picked, the A-Z list shows (filtered) instead of the brand logos.
  MATS, mat door step 1 (grid): Price (the mat deck had it); mat buttons show the price line when a price is picked.
  MATS, tiles door step 2 deck: 'Same brand as my tiles' chip next to Brand.
  RACKS, step 3 (both doors): 'Same brand as my tiles' and 'Same brand as my mat' (when the mat's brand differs).
  TABLE VIEW swap sheet: 'Same brand as my mat / tiles' at the top of the Brand menu; Mat tab gets the Holiday chip.
All of them clear (tap again / Clear / All colors); nothing locks. X and heart untouched.

Usage: python3 builder/fym_fix_nov07/doors_v118.py <build_dir | index.html>   (idempotent; run after the data patches and
zoomswipe_v118.py, before release118.py)
"""
import os, sys

MARK = '/*v118 doors*/'

# --- edits inside the app's own functions (each anchor must occur exactly once) ---
REPL = [
    # mats / racks deck chip row: same-brand chip(s) right after Brand
    ("data-brands=\"${k}\">${f.brand?esc(f.brand)+' \\u2715':'Brand \\u25be'}</button>",
     "data-brands=\"${k}\">${f.brand?esc(f.brand)+' \\u2715':'Brand \\u25be'}</button>${typeof SAMEB==='function'?SAMEB(k):''}"),
    # mat door step 2 (tile swipe): full tile filter row in place of the lone price row
    ("${typeof PRB==='function'?PRB('t'):''}",
     "<div class=\"rfil mfil tfil\">${typeof TFIL==='function'?TFIL():(typeof PRB==='function'?PRB('t'):'')}</div>"),
    # mat door step 2 'See all' grid: the same filter row above the lists
    ("(g.her.length?`<p class=\"dsub\">Tiffany matched this mat with",
     "(typeof TFIL==='function'?`<div class=\"s2ctl dgctl\"><div class=\"rfil mfil tfil\">${TFIL()}</div></div>`:'')+(g.her.length?`<p class=\"dsub\">Tiffany matched this mat with"),
    # tiles door step 1: in-stock inside the colour box (as in the mat door), price after the brand menu
    ("${tileChips()}</div>${brandMenu()}<div class=\"msearch\">",
     "${tileChips()}${typeof TINS==='function'?TINS():''}</div>${brandMenu()}${typeof GPRB==='function'?GPRB('t'):''}<div class=\"msearch\">"),
    # mat door step 1: price after the brand menu
    ("'<div class=\"tfind\">'+doorChips()+matBrandMenu()+",
     "'<div class=\"tfind\">'+doorChips()+matBrandMenu()+(typeof GPRB==='function'?GPRB('m'):'')+"),
    # tile grid (tiles door step 1): in-stock + price filter the list; with either on, no colour/brand = the A-Z list
    ("const all=D.sets.map((s,i)=>[s,i]).filter(x=>VIS(x[0]));if(S.tbrand)",
     "let all=D.sets.map((s,i)=>[s,i]).filter(x=>VIS(x[0]));if(typeof TGF==='function')all=TGF(all);if(S.tbrand)"),
    ("if(S.tcol==='')return blogoView();",
     "if(S.tcol===''&&!(typeof TGON==='function'&&TGON()))return blogoView();"),
    ("if(S.tcol==='az')return all", "if(S.tcol==='az'||S.tcol==='')return all"),
    # price line on grid buttons (only shows while a price is picked; PRC returns '' otherwise)
    ("<small>${esc(BDN(s.maker))}${(T[s.tile]||{}).so?' · sold out':''}</small></button>",
     "<small>${esc(BDN(s.maker))}${(T[s.tile]||{}).so?' · sold out':''}</small>${typeof PRC==='function'?PRC('t',i):''}</button>"),
    ("${M[id].rt?'<b class=\"rtd\">Retired</b>':''}</button>",
     "${M[id].rt?'<b class=\"rtd\">Retired</b>':''}${typeof PRC==='function'?PRC('m',id):''}</button>"),
    ("${r.her?'<b class=\"her\">♥ Tiffany’s match</b>':''}</button>",
     "${r.her?'<b class=\"her\">♥ Tiffany’s match</b>':''}${typeof PRC==='function'?PRC('t',r.i):''}</button>"),
    # Table view swap sheet: same-brand at the top of the Brand menu; Holiday chip on the Mat tab
    ("p.innerHTML=`<button type=\"button\" data-tvb=\"\">All brands</button>`+bs.map(",
     "p.innerHTML=`<button type=\"button\" data-tvb=\"\">All brands</button>`+(()=>{const s=curSet(),m=curMat(),o=[];"
     "const add=(w,L)=>{const b=L.find(x=>x&&cnt[x]);if(b&&!o.some(y=>y[1]===b))o.push([w,b]);};"
     "if(SW.tab!=='mat'&&m&&M[m])add('mat',[M[m].bn]);if(SW.tab!=='tiles'&&s)add('tiles',[(T[s.tile]||{}).bn,s.maker,...String(s.maker||'').split(/\\s+x\\s+/i)]);"
     "return o.map(([w,b])=>`<button type=\"button\" class=\"tvsame\" data-tvb=\"${esc(b)}\">\\u2605 Same brand as my ${w} \\u00b7 ${esc(BD(b))}</button>`).join('');})()+bs.map("),
    ("if(SW.tab==='mat')return ['pink'", "if(SW.tab==='mat')return ['holiday','pink'"),
    ("cols:[...(o.mf||[]),...(o.ha||[])]", "cols:[...(o.mf||[]),...(o.ha||[]),...(isHolM(k)?['holiday']:[])]"),
    ("const COL={pink:'#ef8fb4'", "const COL={holiday:'linear-gradient(135deg,#c8202f 50%,#1f6b3a 50%)',pink:'#ef8fb4'"),
]

# tile grid sorts: tile sets with no listed price go last while a price is picked (same rule as the decks, gate [166])
SOON = "!!T[a[0].tile].soon-!!T[b[0].tile].soon"

JS = r"""<script>""" + MARK + r"""(function(){
/* FYM 1.18 door parity (Tiffany Nov 7 10:24pm). Filters for TILE SETS at the mat door's step 2 live in S.f.t (reset when the mat changes). */
S.f.t=S.f.t||{fam:'',brand:'',her:false,mat:null};S.tfE=0;S.tinsE=0;S.tgNP=null;
const TBM=(s,B)=>!!B&&(s.maker===B||TB(s)===B||String(s.maker||'').split(/\s+x\s+/i).includes(B));window.TBM=TBM;
const TGR=s=>Object.keys(BACKG).filter(g=>(BACKG[g]||[]).includes(s.name));window.TGR=TGR;
function tf(){const f=S.f.t;if(f.mat!==S.dmat){f.fam='';f.brand='';f.her=false;f.mat=S.dmat;}return f;}
const tOn=f=>!!(f.fam||f.brand||f.her);
const _sfm=setsForMat;
setsForMat=function(id){const g=_sfm(id);if(id!==S.dmat)return g;S.tfE=0;const f=tf();if(!tOn(f))return g;
 const ok=r=>(!f.brand||TBM(r.s,f.brand))&&(!f.fam||TGR(r.s).includes(f.fam));const all=f.her&&!f.brand;/* picks + a brand = all that brand, her picks first (as mats, v106) */
 const n={her:(g.her||[]).filter(ok),alb:all?[]:(g.alb||[]).filter(ok),cat:all?[]:(g.cat||[]).filter(ok)};
 if(!(n.her.length+n.alb.length+n.cat.length)){S.tfE=1;return g;}/* never empties: show all + a note with Clear */
 return Object.assign({},g,n);};
const chipIns=e=>`<div class="insw"><button type="button" class="chip insb" data-ins aria-pressed="${!!S.ins}">${S.ins?'\u2713 ':''}In stock only</button><small>Stock checked ${esc(D.stk||'')}</small>${S.ins&&e?'<small class="inse">No in-stock matches here, so showing all.</small>':''}</div>`;
const sameChip=(k,w,B,on)=>`<button type="button" class="chip sameb${on?' on':''}" data-sameb="${k}" data-b="${esc(B)}" aria-pressed="${on}" title="Only ${esc(BDN(B))}">${on?'\u2713 ':'\u2605 '}Same brand as my ${w}</button>`;
/* TILE SETS at the mat door's step 2: in stock, price, picks, brand, same brand as my mat, holiday + colour groups */
window.TFIL=function(){if(!S.dmat||!M[S.dmat])return '';const f=tf();S.insE=0;let g0;try{g0=_sfm(S.dmat);}catch(x){g0={her:[],alb:[],cat:[]};}const ie=S.insE;
 let pr='';try{pr=typeof PRB==='function'?PRB('t'):'';}catch(x){}try{setsForMat(S.dmat);}catch(x){}
 const all=[...(g0.her||[]),...(g0.alb||[]),...(g0.cat||[])];const gs=tileOrder().filter(G=>all.some(r=>TGR(r.s).includes(G)));
 const B=M[S.dmat].bn,hasB=!!B&&all.some(r=>TBM(r.s,B));const herU=(g0.her||[]).length>0&&((g0.alb||[]).length+(g0.cat||[]).length)>0;
 return chipIns(ie)+pr+`<div class="frow" role="group" aria-label="Tile set filters">${herU?`<button type="button" class="chip her" data-ther aria-pressed="${f.her}" title="Tap to switch">${icon()} Tiffany\u2019s picks: ${f.her?'on':'off'}</button>`:''}<button type="button" class="chip${f.brand?' on':''}" data-tbrands>${f.brand?esc(BDN(f.brand))+' \u2715':'Brand \u25be'}</button>${hasB?sameChip('t','mat',B,f.brand===B):''}<span class="sep"></span><button type="button" class="dot" data-tfam="" aria-pressed="${!f.fam}" title="All colors" aria-label="All colors"><i style="background:${RAINBOW}"></i></button>${gs.includes('Holiday')?`<button type="button" class="chip holc" data-tfam="Holiday" aria-pressed="${f.fam==='Holiday'}">Holiday</button>`:''}${gs.filter(G=>G!=='Holiday').map(G=>`<button type="button" class="dot" data-tfam="${esc(G)}" aria-pressed="${f.fam===G}" title="${esc(G)}" aria-label="${esc(G)}"><i style="background:${GCHIP[G]||GDOT[G]||'#999'}"></i></button>`).join('')}</div>`+
 (S.tfE?`<p class="fcombo">No tile sets fit all of those, so showing all. <button type="button" class="lnk" data-tclear>Clear</button></p>`:(tOn(f)?`<p class="fcombo">${f.her&&!f.brand?'Tiffany\u2019s picks':'Tile sets'}${f.brand?' by '+esc(BDN(f.brand)):''}${f.fam?' \u00b7 '+esc(f.fam):''} \u00b7 <button type="button" class="lnk" data-tclear>Clear</button></p>`:''));};
/* same-brand chips for the mat deck (tiles) and the rack deck (tiles + mat) */
window.SAMEB=function(k){try{if(S.set==null)return '';const f=S.f[k],o=k==='m'?M:R;const pool=k==='m'?matPool():rackPool();const have=new Set(pool.map(id=>o[id]&&o[id].bn).filter(Boolean));
 const s=set(),out=[];const tb=[(T[s.tile]||{}).bn,s.maker,...String(s.maker||'').split(/\s+x\s+/i)].find(b=>b&&have.has(b));if(tb)out.push(['tiles',tb]);
 if(k==='r'&&S.fav&&M[S.fav]){const mb=M[S.fav].bn;if(mb&&have.has(mb)&&mb!==tb)out.push(['mat',mb]);}
 return out.map(([w,b])=>sameChip(k,w,b,f.brand===b)).join('');}catch(x){return '';}};
/* tiles door step 1 grid: in stock + price */
window.TGON=()=>!!(S.ins||(S.pr&&S.pr.t!==''));
window.TGNP=x=>S.tgNP&&S.tgNP.has(x[1])?1:0;
window.TGF=function(all){S.tinsE=0;S.tgNP=null;let a=all;if(S.ins){const f=a.filter(x=>!OOS('t',x[0].tile));if(f.length||!a.length)a=f;else S.tinsE=1;}
 if(S.pr&&S.pr.t!==''&&window.PRF){const ids=PRF('t',a.map(x=>x[1]));a=ids.map(i=>[D.sets[i],i]);S.tgNP=new Set(ids.filter(i=>!((typeof TVD==='object'&&TVD.pt)||{})[D.sets[i].tile]));}return a;};
window.TINS=function(){try{TGF(D.sets.map((s,i)=>[s,i]).filter(x=>VIS(x[0])));}catch(x){}return chipIns(S.tinsE);};
/* price dropdown for the first-step grids, same markup as the decks' (PRB) with the grid's own notes */
window.GPRB=function(k){const r=((typeof TVD==='object'&&TVD.pr)||{})[k==='m'?'mat':'tiles']||[];if(!r.length)return '';const v=S.pr[k];
 try{if(k==='m')doorMats();else TGF(D.sets.map((s,i)=>[s,i]).filter(x=>VIS(x[0])));}catch(x){}
 return `<div class="prw gprw"><label class="prsel"><span>Price</span><select data-prsel="${k}" aria-label="Price">${['',...r].map(x=>`<option value="${x}"${v===x?' selected':''}>${x===''?'Any price':'Under $'+x}</option>`).join('')}</select></label>${v!==''?`<small class="prn">${S.prE[k]?`Nothing under $${v} here, so showing all. `:''}${S.prN[k]?`${S.prN[k]} without a listed price shown last. `:''}Store price, or less with code MAHJMATCH where it applies.</small>`:''}</div>`;};
const _dm=doorMats;doorMats=function(){const L=_dm();return window.PRF?PRF('m',L):L;};
const rT=()=>{S.tpeek=null;renderTiles();};
function tBrandSheet(){const f=tf();if(f.brand){f.brand='';rT();return;}let g;try{g=_sfm(S.dmat);}catch(x){return;}
 const bs=[...new Set([...(g.her||[]),...(g.alb||[]),...(g.cat||[])].map(r=>r.s.maker))].sort((a,b)=>a.localeCompare(b));
 const el=document.createElement('div');el.className='sheet';el.innerHTML=`<div class="box"><button type="button" class="x" aria-label="Close">\u2715</button><h3>Shop by brand</h3><div class="bl">${bs.map(b=>`<button type="button" data-b="${esc(b)}">${LG(b)?`<img src="${LG(b)}" alt="">`:''}<span>${esc(BDN(b))}</span></button>`).join('')}</div></div>`;
 el.addEventListener('click',e=>{if(e.target===el||e.target.closest('.x')){el.remove();return;}const b=e.target.closest('[data-b]');if(b){f.brand=b.dataset.b;el.remove();rT();}});openSheet(el);}
document.addEventListener('click',e=>{const q=s=>e.target.closest&&e.target.closest(s);let b;
 if(b=q('[data-sameb]')){e.stopImmediatePropagation();e.preventDefault();const k=b.dataset.sameb,B=b.dataset.b;
  if(k==='t'){const f=tf();f.brand=f.brand===B?'':B;rT();}else{const f=S.f[k];f.brand=f.brand===B?'':B;if(k==='m')S.peek=null;rerender(k);}
  try{trk('sameb',{mat:k==='t'?S.dmat:(S.fav||''),x:k+':'+B+(b.getAttribute('aria-pressed')==='true'?':off':':on')});}catch(x){}return;}
 if(q('[data-tbrands]')){e.stopImmediatePropagation();tBrandSheet();return;}
 if(b=q('[data-tfam]')){e.stopImmediatePropagation();const f=tf(),v=b.dataset.tfam;f.fam=(!v||f.fam===v)?'':v;rT();return;}
 if(q('[data-ther]')){e.stopImmediatePropagation();const f=tf();f.her=!f.her;rT();return;}
 if(q('[data-tclear]')){e.stopImmediatePropagation();const f=tf();f.fam='';f.brand='';f.her=false;rT();return;}
},true);
/* a price picked on the mat door's mat grid re-draws that grid too (the deck handler only re-draws the mat deck) */
document.addEventListener('change',e=>{const b=e.target.closest&&e.target.closest('[data-prsel]');if(!b)return;if(b.dataset.prsel==='m'&&S.door==='mat'&&(S.set==null||S.tilesOpen))renderTiles();},true);
const st=document.createElement('style');st.textContent='.chip.sameb{white-space:nowrap}.chip.sameb.on{background:#c8325f;color:#fff;border-color:#c8325f}.tfil .frow{flex-wrap:wrap}.dgctl{margin:6px 0 4px}.gprw{margin:6px 0 2px}.tvpop .tvsame{font-weight:600;color:#c8325f}';document.head.appendChild(st);
try{if(S.door==='mat'||S.set==null)renderTiles();}catch(x){}
})();</script>"""


def patch(b):
    p = b if b.endswith('.html') else os.path.join(b, 'index.html')
    h = open(p).read()
    if MARK in h:
        print('doors_v118: already applied'); return 0
    for old, new in REPL:
        n = h.count(old)
        if n != 1:
            print(f'doors_v118: anchor found {n}x (need 1): {old[:80]}'); return 1
        h = h.replace(old, new)
    a = h.find('function tileGrid('); z = h.find('\nconst GCHIP=', a)
    if a < 0 or z < 0 or h[a:z].count(SOON) != 3:
        print(f'doors_v118: tileGrid sort anchors not found (need 3 in tileGrid)'); return 1
    h = h[:a] + h[a:z].replace(SOON, 'TGNP(a)-TGNP(b)||' + SOON) + h[z:]
    i = h.rfind('</body>')
    if i < 0:
        print('doors_v118: no </body>'); return 1
    h = h[:i] + JS + h[i:]
    open(p, 'w').write(h)
    print(f'doors_v118: applied ({len(REPL)} edits + tile-grid price order + door parity script) -> {p}')
    return 0


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(__doc__); sys.exit(2)
    sys.exit(patch(sys.argv[1]))
