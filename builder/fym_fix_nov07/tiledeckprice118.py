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


def patch(h):
    if MARK in h: return h, False
    for a in (OLD, DEF_A, '/*v118 no-price last*/', 'function TSOM(', "function PRP(k,id){if(typeof TVD!=='object')return null;"):
        assert h.count(a) == 1, ('anchor not found once (run price118 + tilerank_v118 first)', h.count(a), a[:60])
    h = h.replace(OLD, NEW).replace(DEF_A, DEF + DEF_A)
    return h, True


if __name__ == '__main__':
    P = sys.argv[1]; P = P if P.endswith('.html') else os.path.join(P, 'index.html')
    h, did = patch(open(P).read())
    if did: open(P, 'w').write(h)
    print('tiledeckprice118:', 'applied' if did else 'already applied', P)
