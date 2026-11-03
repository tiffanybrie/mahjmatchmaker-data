"""v114 WOOD everywhere (QA r9 Nov 3, Tiffany's top complaint): the real-grain wood racks made for Table view (round 8:
6 Bird & Bamboo stains from B&B's own WOOD STAINS photo, 4 Yellow Mountain from 2048px brand photos; config/tableview-rack-audit-
nov02.json 'fixed', method 'real grain' / Provincial grain for Red Mahogany) now also show in the rack DECK, suitor tray, selected
rack, match card and My hearts: every one of those reads rackSrc(id) = IMG[R[id].im], so at start-up these racks point R[id].im at
the Table picture (TVD.ro). Nothing else changes. Gate [154]. Idempotent."""
import sys, os, json
P = sys.argv[1]; P = P if P.endswith('.html') else os.path.join(P, 'index.html'); h = open(P).read()
if '/*v114 wood deck*/' in h: print('wood114 already'); sys.exit()
R0 = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
aud = json.load(open(os.path.join(R0, 'config/tableview-rack-audit-nov02.json')))['fixed']
keys = sorted(k for k, v in aud.items() if 'grain' in v.get('method', ''))
a = "const M=D.mats,R=D.racks,T=D.tiles,UNI=D.uni;"
assert h.count(a) == 1, h.count(a)
b = a + "/*v114 wood deck*/(" + json.dumps(keys) + ").forEach(k=>{const ro=D.tv&&D.tv.ro&&D.tv.ro[k];if(R[k]&&ro){IMG['wg:'+k]=ro;R[k].im='wg:'+k;}});"
h = h.replace(a, b); open(P, 'w').write(h); print('wood114 ok', len(keys))
