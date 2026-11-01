"""v113 QA round 1 fixes (Nov 1):
 1. Brand cap on the MAT-DOOR tile deck: tAll() = her picks + album + catalog; BCAP now runs over album+catalog COMBINED (her picks
    first, exempt), keyed by the tile brand (TB). The per-list cap in setsForMat0 is removed.
 2. Rack search (#rsq) never returns hidden racks (pending-review racks had <img src=undefined> and could be added).
 3. Card preview never collapses while redrawing: the preview <img> carries the canvas width/height (aspect ratio reserved) and #prev
    keeps its last height until the new card is in; tour step 8 (Save or share) waits for the preview, then brings its target into view.
 6. Rack FINISH is its own row (Wood / Walnut / Tortoise / Pearl / Clear / Lucite / Metallic / White), AND-combined with the colour dots,
    each clearable, a chip only when it leaves racks (with the current colour / picks); shown with Tiffany's picks on when a pick has it.
 7. Retired works-for-holiday mats (Dapper 1 + 2) are offered in the TILES-door mat deck for holiday tile sets, after the available mats
    (cards say retired; In stock only hides them).
Idempotent. Usage: python3 ui113b.py <build_dir>"""
import sys
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
if '/*v113b*/' in h: print('ui113b already'); sys.exit()
def rep(a, b, n=1):
    global h
    assert h.count(a) == n, (h.count(a), a[:100]); h = h.replace(a, b)
# 1
rep("return {her,alb:BCAP(alb,NOK,r=>r.s.maker),cat:BCAP(cat,NOK,r=>r.s.maker)};}", "return {her,alb,cat};}")
rep("const g=setsForMat(S.dmat);let A=[...g.her,...g.alb,...g.cat];", "const g=setsForMat(S.dmat);let A=[...g.her,...BCAP([...g.alb,...g.cat],NOK,r=>TB(r.s))];/*v113b: one cap over album+catalog*/")
# 2
rep("const hits=Object.keys(R).filter(id=>{const s=NRM(", "const hits=Object.keys(R).filter(id=>{if(!R[id]||R[id].hid)return false;const s=NRM(")
# 3
rep("const p=$('prev');if(p&&job===cardJob)p.innerHTML=cardURL?`<img src=\"${cardURL}\" alt=\"Your ${esc(s.name)} match card\">`",
    "const p=$('prev');if(p&&job===cardJob)setTimeout(()=>{if(TOUR.on&&(TSTEPS[TOUR.step]||{}).k==='share'){TOUR.repos=1;tourPaint();}},40);/*v113b: tip re-placed after the card redraws*/if(p&&job===cardJob)p.innerHTML=cardURL?`<img src=\"${cardURL}\" width=\"${cv.width}\" height=\"${cv.height}\" style=\"height:auto\" alt=\"Your ${esc(s.name)} match card\">`")
rep("{k:'share',t:'Step 8 · Save or share',", "{k:'share',wait:()=>{const p=$('prev');if(!p)return true;const i=p.querySelector('img');return !!(i&&i.complete&&i.naturalHeight&&p.offsetHeight>40)||/Couldn/.test(p.textContent);},t:'Step 8 · Save or share',")
rep("let c=$('coach');if(!TOUR.on){if(c)c.remove();return;}",
    "let c=$('coach');if(!TOUR.on){if(c)c.remove();return;}const rp=TOUR.repos;TOUR.repos=0;{const s0=TSTEPS[TOUR.step];if(s0&&s0.wait){if(!s0.wait()&&(TOUR.wt=(TOUR.wt||0)+1)<50){clearTimeout(TOUR.wtT);TOUR.wtT=setTimeout(()=>{TOUR.repos=1;tourPaint();},100);}else if(TOUR.wt){TOUR.wt=0;clearTimeout(TOUR.wtT);TOUR.wtT=setTimeout(()=>{TOUR.repos=1;tourPaint();},60);}}}")
rep("if(fresh&&b&&!s.still){/* every new step brings its own area into view */", "if((fresh||rp)&&b&&!s.still){/* every new step brings its own area into view (v113b: again once a waited-for preview is ready) */")
rep("if(fresh){const br=b.getBoundingClientRect();if(br.top<64||br.bottom>innerHeight-10)", "if(fresh||rp){const br=b.getBoundingClientRect();if(br.top<64||br.bottom>innerHeight-10)")
# 6
rep("RFINN={wood:'Wood',tortoise:'Tortoise',metallic:'Metallic',clear:'Clear',pearl:'Pearl'};",
    "RFINN={wood:'Wood',walnut:'Walnut',tortoise:'Tortoise',pearl:'Pearl',clear:'Clear',lucite:'Lucite',metallic:'Metallic',white:'White'};/*v113b*/const FINS=['wood','walnut','tortoise','pearl','clear','lucite','metallic','white'];function RFIN(r){const o=R[r]||{},rf=o.rf||[],n=(o.n||'').toLowerCase(),a=[];if(rf.includes('wood')||/\\bwood/.test(n))a.push('wood');if(/walnut/.test(n))a.push('walnut');if(rf.includes('tortoise'))a.push('tortoise');if(rf.includes('pearl'))a.push('pearl');if(rf.includes('clear'))a.push('clear');if(/lucite/.test(n))a.push('lucite');if(rf.includes('metallic'))a.push('metallic');if(/\\bwhite\\b/.test(n))a.push('white');return a;}function FINN(x){const f=S.f.r,s=f.fin,e0=S.insE;f.fin=x;let n=0;try{n=rackDeck().length;}catch(z){n=1;}finally{f.fin=s;S.insE=e0;}return n;}")
rep("${k==='r'?['wood','tortoise','metallic','clear','pearl'].filter(x=>pool.some(id=>fk(id).includes(x))&&(f.fam.includes(x)||RDOTN(x)>0)).map(x=>`<button type=\"button\" class=\"chip finc\" data-fam=\"${x}\" data-k=\"r\" aria-pressed=\"${f.fam.includes(x)}\">${RFINN[x]}</button>`).join(''):''}", "")
rep("return INSB(k)+`<div class=\"frow\" role=\"group\" aria-label=\"Filters\">", "return INSB(k)+(k==='r'?FINROW(f,pool):'')+`<div class=\"frow\" role=\"group\" aria-label=\"Filters\">")
rep("function filters(k){", "function FINROW(f,pool){/*v113b: rack finish row (above the colour row so the picks toggle stays right above the deck)*/const L=FINS.filter(x=>pool.some(id=>RFIN(id).includes(x))&&(f.fin===x||FINN(x)>0));if(!L.length)return '';return `<div class=\"frow finrow\" role=\"group\" aria-label=\"Rack finish\"><span class=\"fl\">Finish</span>${L.map(x=>`<button type=\"button\" class=\"chip finc\" data-fin=\"${x}\" aria-pressed=\"${f.fin===x}\">${RFINN[x]}</button>`).join('')}${f.fin?'<button type=\"button\" class=\"lnk\" data-finclear>Clear</button>':''}</div>`;}function filters(k){")
rep("if(!f.brand)ids=BCAP(ids,r=>hr.includes(r),r=>R[r].bn);", "if(f.fin)ids=ids.filter(r=>RFIN(r).includes(f.fin));")
rep("ids.splice(ia,1);ids.splice(HB,0,A);}}return ids;}\nfunction queue(k){", "ids.splice(ia,1);ids.splice(HB,0,A);}}/*v113b: cap last, after the photo/tortoise reorders*/if(!f.brand)ids=BCAP(ids,r=>hr.includes(r),r=>R[r].bn);return ids;}\nfunction queue(k){")
rep("if((b=q('.frow [data-fam]'))||(b=q('[data-fam=\"holiday\"]'))){", "if(b=q('[data-fin]')){const f=S.f.r;f.fin=f.fin===b.dataset.fin?'':b.dataset.fin;rerender('r');return;}if(q('[data-finclear]')){S.f.r.fin='';rerender('r');return;}if((b=q('.frow [data-fam]'))||(b=q('[data-fam=\"holiday\"]'))){")
i = h.index('</style>'); h = h[:i] + '.frow.finrow{margin:0 -12px 6px;padding:2px 12px;flex-wrap:nowrap;overflow-x:auto;justify-content:flex-start;scrollbar-width:none}.finrow .fl{font:700 11px var(--body);letter-spacing:.06em;text-transform:uppercase;color:var(--mute);margin-right:4px}' + h[i:]
# 7
rep("return [...new Set(r),...set().m.map(x=>x[0]).filter(id=>M[id]&&!M[id].hid&&!s.has(id))];}",
    "const out=[...new Set(r),...set().m.map(x=>x[0]).filter(id=>M[id]&&!M[id].hid&&!s.has(id))];/*v113b: retired works-for-holiday mats (Dapper 1 + 2) close the deck for holiday tile sets*/if(new Set(BACKG.Holiday||[]).has(set().name)){const o=new Set(out);out.push(...Object.keys(M).filter(id=>M[id].rt&&M[id].wfh&&!M[id].hid&&!o.has(id)));}return out;}")
open(P, 'w').write(h); print('ui113b ok')
