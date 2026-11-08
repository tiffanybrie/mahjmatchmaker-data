"""FYM 1.18 price filter: items with NO listed price are no longer hidden when a price is chosen (gap audit B4: 708 of 1,521 visible
mats had no price, so 'Under $X' silently dropped 47% of mats). Priced items under the chosen price come first (deck order kept), then
every item without a price, in deck order, each card saying 'Price not listed'. The note under the dropdown says
'N without a listed price shown last.' Same rule in the app's mat / rack / tile decks (PRF, setsForMat) and in the Table view swap sheet.
'Nothing under $X here, so showing all' is unchanged (no priced item under X).
Works on any copy (build / website / artifact). Idempotent. Gate [166] (static + node test of PRF).
Usage: python3 builder/fym_fix_nov07/price118.py <dir or index.html>"""
import sys, os
P = sys.argv[1]; P = P if P.endswith('.html') else os.path.join(P, 'index.html'); h = open(P).read()
MARK = '/*v118 no-price last*/'
R = [
    # app decks: priced <= v first, then unpriced (never hidden)
    ("if(!f.filter(id=>!forced(k,id)).length&&ids.length){S.prE[k]=1;return ids}return f}",
     "if(!f.filter(id=>!forced(k,id)).length&&ids.length){S.prE[k]=1;return ids}" + MARK + "return f.concat(ids.filter(id=>!forced(k,id)&&!PRP(k,id)))}"),
    # tile deck in the mat door: inside each group, priced first then unpriced (stable sort keeps the deck order)
    ("const f=a=>(a||[]).filter(r=>keep.has(r.i));return Object.assign({},g,{her:f(g.her),alb:f(g.alb),cat:f(g.cat)})};",
     "const f=a=>(a||[]).filter(r=>keep.has(r.i)).sort((x,y)=>(PRP('t',x.i)?0:1)-(PRP('t',y.i)?0:1));return Object.assign({},g,{her:f(g.her),alb:f(g.alb),cat:f(g.cat)})};"),
    ("${S.prN[k]?`${S.prN[k]} without a listed price not shown. `:''}", "${S.prN[k]?`${S.prN[k]} without a listed price shown last. `:''}"),
    # card line while a price is chosen
    ("const x=PRP(k,id);if(!x)return '';const viaCode=", "const x=PRP(k,id);if(!x)return '<b class=\"prc1 prnl\"><em>Price not listed</em></b>';const viaCode="),
    # Table view swap sheet
    ("if(SW.price!==''){info.nop=rows.filter(r=>r.pc==null).length;rows=rows.filter(r=>r.pc!=null&&r.pc<=SW.price)}",
     "if(SW.price!==''){info.nop=rows.filter(r=>r.pc==null).length;rows=rows.filter(r=>r.pc!=null&&r.pc<=SW.price).concat(rows.filter(r=>r.pc==null))}"),
    ("if(SW.price!==''&&info.nop)h=`${info.nop} without a listed price not shown. `+h;", "if(SW.price!==''&&info.nop)h=`${info.nop} without a listed price shown last. `+h;"),
    (":(it.cd?' <em>less with code MAHJMATCH</em>':'')}</span>`:''}</button>`",
     ":(it.cd?' <em>less with code MAHJMATCH</em>':'')}</span>`:(SW.price!==''?'<span class=\"pr\"><em>Price not listed</em></span>':'')}</button>`"),
]
if MARK in h:
    print('price118: already applied', P); sys.exit()
for a, b in R:
    assert h.count(a) == 1, (h.count(a), a[:80]); h = h.replace(a, b)
open(P, 'w').write(h)
print('price118 ok', P)
