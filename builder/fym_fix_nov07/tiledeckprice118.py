"""FYM 1.18 QA fix F2 (Nov 8, independent QA qa-v118-2026-11-08.md): mat door -> tile deck with a price chosen put unpriced sets
in the middle of the deck (Lotus Cove + 'Under $175': Taylor 6th 'Price not listed', 31 priced sets after the first unpriced one).
Cause: the price118 setsForMat wrapper sorts priced-first inside her/album/catalog, then tAll() re-sorts album + catalog by the tile
rank (TSOM, D.tso) and the brand cap (BCAP) and undoes it.
Fix: with a tile price chosen (and something priced under it), the deck is
   her priced picks, album + catalog priced (tile-rank order, brand cap), her unpriced picks, album + catalog unpriced (same order)
so the tile-rank order holds inside the priced group and inside the unpriced group, and no priced set ever follows an unpriced one.
No price chosen (or nothing priced under it): unchanged. The 'See all' grid already keeps priced-first inside each section (the
wrapper's stable sort over setsForMat0's tile-rank order); gate [166b] checks both the deck and the grid by running the page's own code.
Price test = the same as price118's PRP('t') (TVD.pt[tile]; PRP itself lives inside price118's IIFE).
Run AFTER price118.py and tilerank_v118.py (build118.sh, site118.py, artifact118.py). Works on any copy. Idempotent.
Usage: python3 builder/fym_fix_nov07/tiledeckprice118.py <dir or index.html>"""
import sys, os
MARK = '/*v118b tile-deck price groups*/'
OLD = 'let A=[...g.her,...BCAP(TSOM([...g.alb,...g.cat]),NOK,r=>TB(r.s))];'
NEW = ("let A=(S.pr.t===''||S.prE.t)?[...g.her,...BCAP(TSOM([...g.alb,...g.cat]),NOK,r=>TB(r.s))]:TPG(g);" + MARK)
DEF_A = 'const tAll=()=>{'
DEF = (MARK + "const TPG=g=>{const pr=r=>!!((typeof TVD==='object'&&TVD.pt)||{})[r.s.tile],R=TSOM([...g.alb,...g.cat]),cap=a=>BCAP(a,NOK,r=>TB(r.s));"
       "return [...g.her.filter(pr),...cap(R.filter(pr)),...g.her.filter(r=>!pr(r)),...cap(R.filter(r=>!pr(r)))];}; ")


# QA2 (Nov 8): the 'See all' grid kept priced-first only INSIDE each section, so Lotus Cove + 'Under $175' opened on 9 unpriced
# 'Best color matches' with the 24 priced partner sets behind a button. With a tile price chosen (and something priced under it) the
# grid is now: her priced picks | priced album + catalog sets as ONE tile-rank list ('More tile sets that suit it' / 'Best color
# matches', 'Show more' as before; the partner button is not needed) | a last 'Price not listed' section (her unpriced picks first,
# then the rest), shown once every priced set is on screen. The her header still counts all her picks.
MARK2 = '/*v118c grid price groups*/'
G_OLD = 'const m=M[S.dmat];const g=setsForMat(S.dmat);const n=S.dshow||DOOR.slim;\n if(!S.dgrid&&S.set==null){tswipe(el,lock,m,g);return;}'
G_NEW = ('const m=M[S.dmat];let g=setsForMat(S.dmat);const n=S.dshow||DOOR.slim;\n if(!S.dgrid&&S.set==null){tswipe(el,lock,m,g);return;}'
         + MARK2 + 'g=TGG(g);')  # keeps the 'tswipe(el,lock,m,g)' text (gate [42])
G_DEF = (MARK2 + "const TGG=g=>{const herN=(g.her||[]).length;if(S.pr.t===''||S.prE.t)return Object.assign({},g,{herN,np:[]});"
         "const pr=r=>!!((typeof TVD==='object'&&TVD.pt)||{})[r.s.tile],R=TSOM([...g.alb,...g.cat]);"
         "return Object.assign({},g,{herN,her:g.her.filter(pr),alb:R.filter(pr),cat:[],np:[...g.her.filter(r=>!pr(r)),...R.filter(r=>!pr(r))]});}; ")
H_OLD = ("(g.her.length?`<p class=\"dsub\">Tiffany matched this mat with ${g.her.length} tile set${g.her.length>1?'s':''}</p>"
         "<div class=\"tgrid dsets\">${g.her.map(dsetBtn).join('')}</div>`:")
H_NEW = ("(g.herN?`<p class=\"dsub\">Tiffany matched this mat with ${g.herN} tile set${g.herN>1?'s':''}</p>"
         "${g.her.length?`<div class=\"tgrid dsets\">${g.her.map(dsetBtn).join('')}</div>`:'<p class=\"hint\">Her picks have no listed price, so they are under Price not listed below.</p>'}`:")
M_OLD = "`<p class=\"dsub\">${g.her.length?'More tile sets that suit it':'Best color matches'}</p>"
M_NEW = "`<p class=\"dsub\">${g.herN?'More tile sets that suit it':'Best color matches'}</p>"
E_OLD = "(g.cat.length?`<button type=\"button\" class=\"dmore\" data-dmore=\"c\">Show partner brands’ tile sets</button>`:''));}"
E_NEW = ("(g.cat.length?`<button type=\"button\" class=\"dmore\" data-dmore=\"c\">Show partner brands’ tile sets</button>`:''))"
         "+(g.np.length&&g.alb.length<=n?`<p class=\"dsub\">Price not listed</p><div class=\"tgrid dsets\">${g.np.map(dsetBtn).join('')}</div>`:'');}")


def patch_grid(h):
    if MARK2 in h: return h, False
    for a in (G_OLD, H_OLD, M_OLD, E_OLD, DEF_A):
        assert h.count(a) == 1, ('grid anchor not found once', h.count(a), a[:70])
    h = h.replace(G_OLD, G_NEW).replace(H_OLD, H_NEW).replace(M_OLD, M_NEW).replace(E_OLD, E_NEW).replace(DEF_A, G_DEF + DEF_A)
    return h, True


def patch(h):
    h, d2 = patch_grid(h)
    if MARK in h: return h, d2
    for a in (OLD, DEF_A, '/*v118 no-price last*/', 'function TSOM(', "function PRP(k,id){if(typeof TVD!=='object')return null;"):
        assert h.count(a) == 1, ('anchor not found once (run price118 + tilerank_v118 first)', h.count(a), a[:60])
    h = h.replace(OLD, NEW).replace(DEF_A, DEF + DEF_A)
    return h, True


if __name__ == '__main__':
    P = sys.argv[1]; P = P if P.endswith('.html') else os.path.join(P, 'index.html')
    h, did = patch(open(P).read())
    if did: open(P, 'w').write(h)
    print('tiledeckprice118:', 'applied' if did else 'already applied', P)
