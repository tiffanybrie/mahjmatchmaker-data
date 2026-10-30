"""v105 QA fixes (Oct 30 pm, independent QA of b105):
1. US spelling: every user-facing 'colour' -> 'color' (gate [111]); the step-2 filter row wraps under the card so '+ Add color' is never cut off.
2. After a step-2 search pick, scroll so the chosen photo (not just the new top card) sits right under the sticky header.
4. Match card subtitle drops '(retired)' from mat names ('tiles on the Spring Fling mat').
5. Racks step gets the same side X / heart on the rack swipe card.
(3: side B's own mat-door order = v105so.py + setsForMat uses M[id].so.)
Usage: python3 patch105b.py <index.html>  (in place)"""
import sys
P = sys.argv[1]; h = open(P).read()
def rep(a, b, n=1):
    global h
    c = h.count(a); assert c == n, (c, a[:90]); h = h.replace(a, b)
# 1. spelling
rep("${f.multi?'\\u2713 Adding':'+ Add colour'}", "${f.multi?'\\u2713 Adding':'+ Add color'}")
rep('Want two colors together? Tap + Add a colour first.', 'Want two colors together? Tap + Add a color first.')
rep("${S.dmulti?'\\u2713 Adding colours':'+ Add a colour'}", "${S.dmulti?'\\u2713 Adding colors':'+ Add a color'}")
CSS = '.s2ctl .frow{flex-wrap:wrap;overflow:visible;margin:0;padding:2px 0;justify-content:center;row-gap:6px}\n'
i_ = h.rindex('</style></head>'); h = h[:i_] + CSS + h[i_:]
# 2. search pick: scroll to the chosen photo (the compare block), just under the sticky header
OLD_M = "requestAnimationFrame(()=>{const c=$('top-m');if(c){const y=c.getBoundingClientRect().top+window.scrollY-120;window.scrollTo({top:Math.max(0,y),behavior:'smooth'});}});"
NEW_M = "requestAnimationFrame(()=>{const c=$('top-m');if(c){const bx=c.closest('.cmp')||c,pb=bx.classList.contains('aer')&&bx.previousElementSibling||bx;const hd=document.querySelector('header.top');const y=pb.getBoundingClientRect().top+window.scrollY-((hd&&hd.getBoundingClientRect().height)||56)-6;window.scrollTo({top:Math.max(0,y),behavior:'smooth'});}});"
rep(OLD_M, NEW_M)
OLD_T = "renderTiles();requestAnimationFrame(()=>{const c=$('top-t');if(c){const y=c.getBoundingClientRect().top+window.scrollY-120;window.scrollTo({top:Math.max(0,y),behavior:'smooth'});}});});"
NEW_T = "const qi=$('tdq');if(qi)qi.value='';const r_=$('tdr');if(r_)r_.innerHTML='';renderTiles();requestAnimationFrame(()=>{const c=$('top-t');if(c){const bx=c.closest('.cmp')||c,pb=bx.classList.contains('aer')&&bx.previousElementSibling||bx;const hd=document.querySelector('header.top');const y=pb.getBoundingClientRect().top+window.scrollY-((hd&&hd.getBoundingClientRect().height)||56)-6;window.scrollTo({top:Math.max(0,y),behavior:'smooth'});}});});"
rep(OLD_T, NEW_T)
# 3. side B: own mat-door order (M[id].so = set indices best first, from v105so.py)
rep("const p=ix<0?1e9:s.rank.indexOf(ix);return {s,i,her,p:p<0?1e9:p};",
    "const SO=M[id]&&M[id].so;const p=SO?(SO.indexOf(i)<0?1e9:SO.indexOf(i)):(ix<0?1e9:s.rank.indexOf(ix));return {s,i,her,p:p<0?1e9:p};")
# 4. card subtitle without '(retired)'
rep("st=`tiles on the ${mName} mat`", "st=`tiles on the ${String(mName).replace(/\\s*\\(retired\\)/i,'')} mat`")
# 5. racks: side X / heart too
rep("const ok=k==='m'?(!S.peek&&!matLocked()&&queue('m').length):(S.tpeek==null&&tq().length);if(!ok)return;",
    "const ok=k==='m'?(!S.peek&&!matLocked()&&queue('m').length):k==='r'?queue('r').length:(S.tpeek==null&&tq().length);if(!ok)return;")
rep("d.insertAdjacentHTML('beforeend',k==='m'?'<div class=\"sbx\"><button type=\"button\" class=\"sb no\" data-no=\"m\" aria-label=\"No thanks\">✕</button><button type=\"button\" class=\"sb yes\" data-yes=\"m\" aria-label=\"Love\">♥</button></div>':",
    "d.insertAdjacentHTML('beforeend',(k==='m'||k==='r')?'<div class=\"sbx\"><button type=\"button\" class=\"sb no\" data-no=\"'+k+'\" aria-label=\"No thanks\">✕</button><button type=\"button\" class=\"sb yes\" data-yes=\"'+k+'\" aria-label=\"Love\">♥</button></div>':")
rep("bindCard('r');bindMat();updFlow();}", "addSB(el,'r');bindCard('r');bindMat();updFlow();}")
open(P, 'w').write(h); print('patch105b ok', len(h))
