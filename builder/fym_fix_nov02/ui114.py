"""v114 UI (Tiffany Nov 1 11:33pm, ANSWERS):
 2. RACK FILTER = SINGLES: Finish chips and colour dots are ONE single-select group. Tapping Tortoise = every tortoise rack (any colour);
    tapping a colour = that colour (any finish); a new chip replaces the old one; the rainbow = All (clears both). Both rows ALWAYS show
    every option the rack pool has (never shrink to what is left after another pick: she picked White, went back to the rainbow and saw
    'no colors'). White chip kept. Replaces the v113 'finish combines with colour' behaviour (v112q RDOTN / v113 FINN row trimming).
 3. TOUR: a step on the View switch after the mat swipe step: 'Try Table view' (Table shows the whole setup). Next or tapping Table moves on.
Idempotent. Usage: python3 ui114.py <build dir or index.html>"""
import sys, os
P = sys.argv[1]; P = P if P.endswith('.html') else os.path.join(P, 'index.html'); h = open(P).read()
if '/*v114 singles*/' in h: print('ui114 already'); sys.exit()
def rep(a, b):
    global h
    assert h.count(a) == 1, (h.count(a), a[:100]); h = h.replace(a, b)
# finish chip: single select, clears the colour
rep("if(b=q('[data-fin]')){const f=S.f.r;f.fin=f.fin===b.dataset.fin?'':b.dataset.fin;rerender('r');return;}",
    "if(b=q('[data-fin]')){const f=S.f.r;f.fin=f.fin===b.dataset.fin?'':b.dataset.fin;if(f.fin)f.fam=[];rerender('r');return;}/*v114 singles*/")
# colour dot / rainbow on the rack row: single select, clears the finish (rainbow clears both)
rep("const f=S.f[b.dataset.k];f.fam=PICK(b.dataset.k,f,b.dataset.fam);rerender(b.dataset.k);tourEv('fam');return;}",
    "const f=S.f[b.dataset.k];f.fam=PICK(b.dataset.k,f,b.dataset.fam);if(b.dataset.k==='r'){f.fam=f.fam.slice(-1);f.fin='';}rerender(b.dataset.k);tourEv('fam');return;}")
# rows always show every option in the pool
rep("const L=FINS.filter(x=>pool.some(id=>RFIN(id).includes(x))&&(f.fin===x||FINN(x)>0));", "const L=FINS.filter(x=>pool.some(id=>RFIN(id).includes(x)));/*v114: never shrinks*/")
rep(".filter(x=>pool.some(id=>fk(id).includes(x))).filter(x=>k!=='r'||f.fam.includes(x)||RDOTN(x)>0);", ".filter(x=>pool.some(id=>fk(id).includes(x)));/*v114: rack colours never shrink (no dot-count trimming)*/")
rep('data-fam="" data-k="${k}" aria-pressed="${!f.fam.length}"', 'data-fam="" data-k="${k}" aria-pressed="${!f.fam.length&&!(k===\'r\'&&f.fin)}"')
# tour step on the View switch
a = " {k:'pick',t:'Step 3 · Pick your mat',"
rep(a, " {k:'table',t:'New · Try Table view',p:'Tap Table to see your whole setup from above: the mat, four racks, tile walls and your tiles. Up close and Aerial work like before.',b:'#s-mats .vrow [data-mode=\"table\"],#s-tiles .vrow [data-mode=\"table\"]',next:'Next',done:()=>S.mode==='table',skip:()=>matLocked()},\n" + a)
open(P, 'w').write(h); print('ui114 ok')
