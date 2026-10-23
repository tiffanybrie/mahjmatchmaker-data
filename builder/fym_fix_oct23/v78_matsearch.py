"""FYM v78 fix (Tiffany Oct 23 3:21pm, CRITICAL): picking a mat from "Already own a mat? Search by name or brand" on the mat
screen jumped her down to the RACKS with that mat already set up (the result buttons used data-mock = pick + Add racks).
Correct: the searched mat comes up as the next card in the MAT swiper, right there on the mat screen. She hearts it (it falls
into her suitors) or ✕'s it like any other mat; picking a suitor and Add racks stay her choice. Filters never hide it.
Gate [40] checks: mat-search results never carry data-mock, and choosing one puts that mat on top of the mat deck.
Usage: python3 v78_matsearch.py <build_dir>"""
import sys
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
def rep(old, new, n=1):
    global h
    c = h.count(old); assert c == n, f'expected {n} x {old[:90]!r}, found {c}'; h = h.replace(old, new)
rep("""if(f.brand)ids=ids.filter(id=>M[id].bn===f.brand);return ids;}""",
    """if(f.brand)ids=ids.filter(id=>M[id].bn===f.brand);if(S.mfront&&M[S.mfront]&&!S.seen[S.mfront])ids=[S.mfront,...ids.filter(x=>x!==S.mfront)];return ids;}""")
rep("""box.innerHTML=hits.length?hits.map(id=>`<button type="button" data-mock="${id}"><img src="${matTh(id)}" alt="">""",
    """box.innerHTML=hits.length?hits.map(id=>`<button type="button" data-mfront="${id}"><img src="${matTh(id)}" alt="">""")
rep("""if(b=q('[data-mock]')){""", """if(b=q('[data-mfront]')){const id=b.dataset.mfront;if(M[id]){S.mfront=id;delete S.seen[id];S.peek=null;const qi=$('msq');if(qi)qi.value='';const r=$('msr');if(r)r.innerHTML='';renderMats();steps();requestAnimationFrame(()=>{const c=$('top-m');if(c){const y=c.getBoundingClientRect().top+window.scrollY-120;window.scrollTo({top:Math.max(0,y),behavior:'smooth'});}});}return;}
 if(b=q('[data-mock]')){""")
open(P, 'w').write(h); print('mat search fixed')
