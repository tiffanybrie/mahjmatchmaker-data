"""FYM v95: racks follow the TILE brand first, then the mat brand (Tiffany Oct 26 11:35: Mahj Mood 90s tiles + Anders Ruff mat
showed Anders Ruff clear racks first; Mahj Mood's own clear scallops must lead). Gate [75]. Idempotent.
Usage: python3 v95_rackbrand.py <build_dir>"""
import sys
P = sys.argv[1] + '/index.html'; h = open(P).read()
if '/*v95 tile brand first*/' in h: print('rackbrand: already'); sys.exit()
rep = [
 ("const ownB=()=>[set().maker,(D.tiles[set().tile]||{}).bn,(M[S.fav]||{}).bn];",
  "const ownB=()=>[set().maker,(D.tiles[set().tile]||{}).bn,(M[S.fav]||{}).bn];/*v95 tile brand first*/const tileB=()=>[set().maker,(D.tiles[set().tile]||{}).bn];const ownW=r=>tileB().includes(R[r].bn)?2:ownB().includes(R[r].bn)?1:0;"),
 # ownLift: tile-brand racks before mat-brand racks, then photo quality
 ("const own=[...ow.filter(wc),...ow.filter(r=>!wc(r))].slice(0,2);",
  "ow.sort((a,b)=>(ownW(b)-ownW(a))||((R[b].pq||3)-(R[a].pq||3)));const own=[...ow.filter(wc),...ow.filter(r=>!wc(r))].sort((a,b)=>ownW(b)-ownW(a)).slice(0,2);"),
 # colour chip: tile brand bonus 5 (white/clear) / .3, mat brand only 2 / .15
 ("(ownB().includes(R[r].bn)?((c==='neutral'&&R[r].wh)||(c==='clear'&&R[r].cl)?5:.3):0)",
  "(ownW(r)?((c==='neutral'&&R[r].wh)||(c==='clear'&&R[r].cl)?(ownW(r)===2?5:2):(ownW(r)===2?.3:.15)):0)"),
]
for a, b in rep:
    assert h.count(a) == 1, a[:60]; h = h.replace(a, b)
open(P, 'w').write(h); print('rackbrand: tile brand first')
