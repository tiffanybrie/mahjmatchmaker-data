"""FYM v71 UI fixes (Tiffany, phone test Oct 21 6:20pm). Usage: python3 builder/fym_fix_oct21/v71_ui.py <build_dir>
A. Mat-first door:
   - after tiles: pairing summary at the top (mat thumb + "Your mat" + Change mat; tiles thumb + "Your tiles" + Change tiles),
     both always visible and working; Change mat keeps the tiles, Change tiles keeps the mat (each picker has a Keep button)
   - the mats step shows her mat as one card (no swipe copy, no filters, no picks toggle) with "See other mats for <set>"
     (opens the normal swipe deck; her mat stays in the suitors tray) and "Next: add racks"
   - step indicator for both doors (Mat > Tiles > Racks > Mock up in the mat door; Tiles > Mat > Racks > Mock up in the tiles door)
   - the mock-up CTA is the racks step's button ("Mock up this match"); the mats step's buttons say "Next: add racks"
   - Tiffany's picks toggle: hidden wherever it changes nothing; labelled "Tiffany's picks: on/off" with a one-line hint
   - no "swipe" copy on a locked single card or a deck with fewer than 2 cards
B. racks-step tray wraps instead of squeezing the text one word per line at 390px
C. shorter tile-search placeholder
Gate [22] (builder/fym_matdoor_check.js) runs the page's own code in node over these paths."""
import sys
B = sys.argv[1]; P = B + '/index.html'
h = open(P).read()
i = h.index('const D=') + 8
import json
_, end = json.JSONDecoder().raw_decode(h[i:]); end += i
head, data, tail = h[:i], h[i:end], h[end:]

def rep(s, a, b, n=1):
    c = s.count(a)
    assert c == n, (c, a[:90])
    return s.replace(a, b)

t = tail
H = head
# ---- CSS (head)
H = rep(H, '.si span.go{opacity:.6}\n</style>', '''.si span.go{opacity:.6}
/* v71 (Oct 21): mat-door pairing summary, step indicator, racks tray wrap */
.pair{display:flex;flex-direction:column;gap:8px}
.pair .picked .chip{flex:none}
.flow{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;align-items:center;gap:4px 6px;font:700 11.5px var(--body);color:var(--mute)}
.flow li{display:flex;align-items:center;gap:6px;white-space:nowrap}
.flow li+li::before{content:"\\2192";color:#d9b9c6;font-weight:400}
.flow li.done{color:var(--navy)}
.flow li.now span{background:var(--pink);color:#fff;border-radius:999px;padding:2px 8px}
.dacts{display:flex;flex-direction:column;gap:8px}
.dacts .big{padding:12px}
.dkeep{display:flex;align-items:center;justify-content:space-between;gap:8px;flex-wrap:wrap}
.tray.rk{flex-wrap:wrap}
.tray.rk .th,.tray.rk .none{flex:1 1 calc(100% - 64px);min-width:0}
.tray.rk .ownr{flex:1 1 auto;margin:0}
.tray.rk .go{flex:1 1 auto;max-width:none}
.herbar small{flex:1;min-width:0;text-align:right;line-height:1.3}
</style>''')

# ---- placeholder
t = rep(t, 'placeholder="Don\\u2019t see yours? Search tile sets by name or brand"', 'placeholder="Search tile sets by name or brand"')

# ---- helpers after matDeck
t = rep(t, "function rackPool(){", """/* v71: mat-door lock + picks-toggle usefulness + step indicator */
const matLocked=()=>S.door==='mat'&&!!S.dmat&&S.set!=null&&!S.ddeck&&!!M[S.dmat];
function herUseful(k){if(k==='m'&&matLocked())return false;const n=k==='m'?set().m.filter(x=>M[x[0]]&&!M[x[0]].hid).length:herRacks().length;if(!n)return false;const f=S.f[k],o=f.her,dk=()=>(k==='m'?matDeck():rackDeck()).filter(id=>!(k==='m'?S.seen:S.rseen)[id]).join('|');f.her=true;const a=dk();f.her=false;const b=dk();f.her=o;return a!==b;}
function flowHTML(){const md=S.door==='mat'&&!!S.dmat;const st=md?[['Mat',true],['Tiles',S.set!=null]]:[['Tiles',S.set!=null],['Mat',!!S.fav]];st.push(['Racks',S.rpick.length>0],['Mock up',!!S.made]);const cur=st.findIndex(x=>!x[1]);return st.map(([l,d],i)=>`<li class="${d?'done':(i===cur?'now':'')}"><span>${l}${d?' \\u2713':''}</span></li>`).join('');}
function updFlow(){const f=$('flow');if(f)f.innerHTML=flowHTML();}
function rackPool(){""")

# ---- picks toggle label + hint, hidden when useless
t = rep(t, "function herBtn(k){const on=S.f[k].her;return `<button type=\"button\" class=\"chip her\" data-her=\"${k}\" aria-pressed=\"${on}\" title=\"Tap to switch\">${icon()} ${on?'Showing: Tiffany\\u2019s picks only':'Showing: all '+(k==='m'?'mats':'racks')}</button>`;}",
        "function herBtn(k){if(!herUseful(k))return '';const on=S.f[k].her;return `<button type=\"button\" class=\"chip her\" data-her=\"${k}\" aria-pressed=\"${on}\" title=\"Tap to switch\">${icon()} Tiffany\\u2019s picks: ${on?'on':'off'}</button>`;}")
t = rep(t, "function herBar(k){const n=k==='m'?set().m.length:herRacks().length;return `<div class=\"herbar\">${herBtn(k)}<small>${S.f[k].her?'Tap to see everything':(n?'Her picks still come first':'')}</small></div>`;}",
        "function herBar(k){if(!herUseful(k))return '';const w=k==='m'?'mats':'racks';return `<div class=\"herbar\">${herBtn(k)}<small>${S.f[k].her?`Only the ${w} Tiffany matched with ${esc(set().name)}. Tap to see all.`:`Showing every ${w.slice(0,-1)}. Her picks still come first.`}</small></div>`;}")

t = rep(t, "with <b>Tiffany’s matches on</b>. To see all the possibilities, turn Tiffany’s matches off.<button type=\"button\" class=\"big gh\" style=\"width:auto;padding:10px 16px\" data-her=\"${k}\">Turn Tiffany’s matches off</button>",
        "with <b>Tiffany’s picks on</b>. To see all the possibilities, turn Tiffany’s picks off.<button type=\"button\" class=\"big gh\" style=\"width:auto;padding:10px 16px\" data-her=\"${k}\">Turn Tiffany’s picks off</button>")
# ---- deck: locked mat-door card
t = rep(t, "function deck(k){const q=queue(k);\n", "function deck(k){const q=queue(k);\n if(k==='m'&&matLocked())return `<div class=\"deck m\"><div class=\"peekbar\"><span>Your mat</span></div>${card(S.dmat,k)}</div>`;\n")
t = rep(t, "<button type=\"button\" class=\"pill\" data-unpeek>‹ Keep swiping</button><button type=\"button\" class=\"pill pk\" data-mock=\"${esc(S.peek)}\">Mock this match ♥</button>",
        "<button type=\"button\" class=\"pill\" data-unpeek>‹ Back to the deck</button><button type=\"button\" class=\"pill pk\" data-mock=\"${esc(S.peek)}\">Next: add racks ›</button>")
t = rep(t, "<button type=\"button\" class=\"go\" data-mock=\"${esc(S.peek||L[L.length-1])}\">Mock your match ›</button>`:'<div class=\"none\">Swipe right on mats you like. They’ll wait here so you can compare.</div>'}</div>`;}",
        "<button type=\"button\" class=\"go\" data-mock=\"${esc(S.peek||L[L.length-1])}\">Next: add racks ›</button>`:`<div class=\"none\">${queue('m').length>1&&!S.peek?'Swipe right':'Tap ♥'} on mats you like. They’ll wait here so you can compare.</div>`}</div>`;}")
t = rep(t, ":'<div class=\"none\">Swipe right on racks, then tap up to 2 here.</div>'}<button type=\"button\" class=\"ownr\" data-rsheet>+ Own racks? Search yours</button><button type=\"button\" class=\"go\" data-make ${S.rpick.length?'':'disabled'}>Make it official ♥</button></div>`;}",
        ":`<div class=\"none\">${queue('r').length>1?'Swipe right':'Tap ♥'} on racks, then tap up to 2 here.</div>`}<button type=\"button\" class=\"ownr\" data-rsheet>+ Own racks? Search yours</button><button type=\"button\" class=\"go\" data-make ${S.rpick.length?'':'disabled'}>Mock up this match ♥</button></div>`;}")
t = rep(t, "ok:()=>!(k==='m'&&S.peek),", "ok:()=>!(k==='m'&&(S.peek||matLocked())),")
t = rep(t, "if(!c||!queue(k).length||(k==='m'&&S.peek))return;", "if(!c||!queue(k).length||(k==='m'&&(S.peek||matLocked())))return;")

# ---- tiles step: pairing summary (mat door) + flow (both doors)
t = rep(t, "if(S.set!=null&&!S.tilesOpen){const s=set();el.innerHTML=`<div class=\"picked\"><span class=\"num\">1</span>",
        "if(S.set!=null&&!S.tilesOpen&&S.door==='mat'&&S.dmat&&M[S.dmat]){const s=set(),m=M[S.dmat];el.innerHTML=`<div class=\"pair\"><ol class=\"flow\" id=\"flow\" aria-label=\"Your steps\">${flowHTML()}</ol><div class=\"picked\"><img src=\"${matTh(S.dmat)}\" alt=\"\"><div class=\"tx\"><i>Your mat</i><b>${esc(MN(S.dmat))}</b><small>${esc(m.bn||'')}</small></div><button type=\"button\" class=\"chip\" data-dswap>Change mat</button></div><div class=\"picked\"><img src=\"${pile(s)}\" alt=\"\"><div class=\"tx\"><i>Your tiles</i><b>${esc(s.name)}</b><small>${esc(s.maker)}</small></div><button type=\"button\" class=\"chip\" data-opentiles>Change tiles</button></div></div>`;return;}\n if(S.set!=null&&!S.tilesOpen){const s=set();el.innerHTML=`<ol class=\"flow\" id=\"flow\" aria-label=\"Your steps\">${flowHTML()}</ol><div class=\"picked\"><span class=\"num\">1</span>")
t = rep(t, "<button type=\"button\" class=\"chip\" data-opentiles>Change</button></div>`;return;}", "<button type=\"button\" class=\"chip\" data-opentiles>Change tiles</button></div>`;return;}")

# ---- mats step
t = rep(t, "function renderMats(){const el=$('s-mats');if(S.set==null){el.innerHTML='';return;}if(!window.__imgsReady){el.innerHTML=BOOT('Loading the mats\\u2026');return;}const s=set();\n",
        "function renderMats(){const el=$('s-mats');if(S.set==null){el.innerHTML='';return;}if(!window.__imgsReady){el.innerHTML=BOOT('Loading the mats\\u2026');return;}const s=set();\n if(matLocked()){const m=M[S.dmat];el.innerHTML=`<div class=\"shrow\">${head(2,'Your mat-ch',esc(MN(S.dmat))+' + '+esc(s.name)+' tiles')}<div class=\"seg mode\" role=\"group\" aria-label=\"View\"><button type=\"button\" data-mode=\"close\" aria-pressed=\"${S.mode==='close'}\">Up close</button><button type=\"button\" data-mode=\"aerial\" aria-pressed=\"${S.mode==='aerial'}\">Aerial</button></div></div>`+(S.mode==='close'?`<div class=\"cmp\">${tileView('m')}<div class=\"tcap\"><span>${esc(s.name)} tiles</span><span>Pinch either photo to zoom</span></div>${deck('m')}</div>`:`<div class=\"cmp aer\">${deck('m')}</div>`)+`<div class=\"dacts\"><button type=\"button\" class=\"big\" data-mock=\"${esc(S.dmat)}\">Next: add racks ›</button><button type=\"button\" class=\"big gh\" data-ddeck>See other mats for ${esc(s.name)}</button></div>`;bindCard('m');if(S.mode==='close')bindTile('tv-m');return;}\n")
t = rep(t, "+(S.dmat&&S.dset===S.set&&S.peek&&S.peek===S.dmat&&M[S.dmat]?`<div class=\"dnote\">Your mat: <b>${esc(M[S.dmat].n)}</b>. Want to see other mats for ${esc(s.name)}? Swipe below.</div>`:'')+",
        "+(S.door==='mat'&&S.dmat&&S.ddeck&&M[S.dmat]?`<div class=\"dnote dkeep\"><span>Your mat <b>${esc(MN(S.dmat))}</b> stays in your suitors below.</span><button type=\"button\" class=\"chip mini\" data-dundeck>Back to ${esc(MN(S.dmat))}</button></div>`:'')+")

# ---- racks step copy
t = rep(t, "<p>Pick your favorite suitor and tap <b>Mock your match</b> to swipe racks.</p><button type=\"button\" class=\"big\" style=\"width:auto;padding:10px 18px\" data-mock=\"${esc(sel)}\">Mock your match with ${esc(M[sel].n)} ›</button>",
        "<p>Pick your favorite suitor and tap <b>Next: add racks</b>.</p><button type=\"button\" class=\"big\" style=\"width:auto;padding:10px 18px\" data-mock=\"${esc(sel)}\">Add racks with ${esc(M[sel].n)} ›</button>")
t = rep(t, "el.innerHTML=head(3,'Love triangle','All couples need a wingman. Swipe on racks.')+filters('r')+",
        "el.innerHTML=head(3,'Love triangle','All couples need a wingman. '+(queue('r').length>1?'Swipe on racks.':'Tap \\u2665 on the racks you like.'))+filters('r')+")
t = rep(t, " bindCard('r');bindTile('tv-r');}", " bindCard('r');bindTile('tv-r');updFlow();}")
t = rep(t, "$('stp').innerHTML=st.map(([id,l,on],i)=>`<button type=\"button\" data-jump=\"${id}\" ${on?'':'disabled'}><b>${i+1}</b>${l}</button>`).join('');}",
        "$('stp').innerHTML=st.map(([id,l,on],i)=>`<button type=\"button\" data-jump=\"${id}\" ${on?'':'disabled'}><b>${i+1}</b>${l}</button>`).join('');updFlow();}")

# ---- mat door: Change mat keeps tiles, Change tiles keeps mat
t = rep(t, " if(!S.dmat){const ids=doorMats();el.innerHTML=lock+doorBtns()+doorChips()+",
        " if(!S.dmat){const ids=doorMats();el.innerHTML=lock+doorBtns()+(S.dkeep&&S.set!=null&&M[S.dkeep]?`<div class=\"dnote dkeep\"><span>Pick a different mat for your <b>${esc(set().name)}</b> tiles.</span><button type=\"button\" class=\"chip mini\" data-dkeep>Keep ${esc(MN(S.dkeep))}</button></div>`:'')+doorChips()+")
t = rep(t, "<small>${esc(m.bn||'')}</small></div><button type=\"button\" class=\"chip\" data-dchange>Change</button></div>`+",
        "<small>${esc(m.bn||'')}</small></div><button type=\"button\" class=\"chip\" data-dchange>Change mat</button></div>`+(S.set!=null?`<div class=\"dnote dkeep\"><span>Pick different tiles for <b>${esc(MN(S.dmat))}</b>.</span><button type=\"button\" class=\"chip mini\" data-dkeept>Keep ${esc(set().name)}</button></div>`:'')+")
t = rep(t, "function dsetBtn(r){return `<button type=\"button\" data-dset=\"${r.i}\">", "function dsetBtn(r){return `<button type=\"button\" data-dset=\"${r.i}\" aria-pressed=\"${S.set===r.i}\">")
t = rep(t, " if(q('[data-dchange]')){S.dmat=null;renderTiles();return;}",
        " if(q('[data-dchange]')||q('[data-dswap]')){if(S.set!=null&&S.dmat)S.dkeep=S.dmat;S.dmat=null;S.tilesOpen=true;S.dfams=[];DOOR.lim=36;renderTiles();window.scrollTo({top:0,behavior:'smooth'});return;}\n if(q('[data-dkeep]')){S.dmat=S.dkeep;S.dkeep=null;S.tilesOpen=false;renderAll();return;}\n if(q('[data-dkeept]')){S.tilesOpen=false;renderTiles();steps();return;}\n if(q('[data-ddeck]')){S.ddeck=true;S.peek=null;if(!S.liked.includes(S.dmat))S.liked.push(S.dmat);S.seen[S.dmat]=1;S.f.m.her=true;if(!queue('m').length)S.f.m.her=false;renderMats();steps();jump('s-mats');return;}\n if(q('[data-dundeck]')){S.ddeck=false;S.peek=null;if(S.fav!==S.dmat){resetFrom(2);S.fav=S.dmat;}renderAll();jump('s-mats');return;}")
t = rep(t, " if(b=q('[data-dmat]')){S.dmat=b.dataset.dmat;",
        " if(b=q('[data-dmat]')){if(S.dkeep&&S.set!=null){S.dmat=b.dataset.dmat;pairUp(S.set);return;}S.dmat=b.dataset.dmat;")
t = rep(t, " if(b=q('[data-dset]')){const i=+b.dataset.dset;resetFrom(1);S.set=i;S.f.m.her=set().m.length>0;resetFrom(2);const dm=S.dmat;S.dset=i;S.liked=[dm];S.seen[dm]=1;S.peek=dm;S.fav=dm;S.tilesOpen=false;renderAll();jump('s-mats');return;}\n});",
        " if(b=q('[data-dset]')){pairUp(+b.dataset.dset);return;}\n});\nfunction pairUp(i){const dm=S.dmat;trk('matdoor',{set:D.sets[i].slug,mat:dm});resetFrom(1);S.set=i;resetFrom(2);S.dset=i;S.liked=[dm];S.seen[dm]=1;S.peek=null;S.fav=dm;S.ddeck=false;S.dkeep=null;S.f.m.her=set().m.length>0;S.tilesOpen=false;renderAll();jump('s-mats');}")
# picking another mat while browsing the deck in the mat door makes it "your mat" in the summary
t = rep(t, " if(b=q('[data-mock]')){const id=b.dataset.mock;if(!S.liked.includes(id))S.liked.push(id);",
        " if(b=q('[data-mock]')){const id=b.dataset.mock;if(S.door==='mat'&&S.dmat&&S.set!=null&&id!==S.dmat&&M[id]){S.dmat=id;S.ddeck=true;}if(!S.liked.includes(id))S.liked.push(id);")
# switching doors resets the mat-door pairing
t = rep(t, " if(b=q('[data-door]')){S.door=b.dataset.door;S.tilesOpen=true;renderTiles();return;}",
        " if(b=q('[data-door]')){if(S.door!==b.dataset.door){S.ddeck=false;S.dkeep=null;}S.door=b.dataset.door;S.tilesOpen=true;renderTiles();return;}")

open(P, 'w').write(H + data + t)
print('v71 ui patched')
