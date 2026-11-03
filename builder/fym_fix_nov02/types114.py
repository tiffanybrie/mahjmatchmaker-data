"""v114 (Tiffany Nov 3 2:48pm, ANSWERS):
 - RACK TYPES: one type per rack, by eye (config/rack-types-nov03.json, via D.tv.rt): Wood tone, Painted, Acrylic, Marble, Clear,
   Tortoise, Pearl, Metallic. The 'Finish' row becomes 'Type'; Walnut folds into Wood tone. White stays as a colour dot (D.tv.rw).
   Filters stay single-select (ui114): a type clears the colour, a colour clears the type. Gate [151].
 - TIFFANY'S PICKS DEFAULT OFF (mats and racks): the toggle stays; her real picks still lead the mat deck with the 'Tiffany's match'
   label; racks show the full colour-theory deck. Gate [152].
Idempotent. Usage: python3 types114.py <build dir or index.html>"""
import sys, os
P = sys.argv[1]; P = P if P.endswith('.html') else os.path.join(P, 'index.html'); h = open(P).read()
if '/*v114 types*/' in h: print('types114 already'); sys.exit()
def rep(a, b, n=1):
    global h
    assert h.count(a) == n, (h.count(a), a[:90]); h = h.replace(a, b)
rep("RFINN={wood:'Wood',walnut:'Walnut',tortoise:'Tortoise',pearl:'Pearl',clear:'Clear',lucite:'Lucite',metallic:'Metallic',white:'White'};/*v113b*/const FINS=['wood','walnut','tortoise','pearl','clear','lucite','metallic','white'];",
    "RFINN=(D.tv&&D.tv.rtl)||{};/*v114 types*/const FINS=(D.tv&&D.tv.rto)||[];")
i = h.index("function RFIN(r){"); j = h.index("return a;}", i) + len("return a;}")
h = h[:i] + "function RFIN(r){const t=((D.tv&&D.tv.rt)||{})[r];return t?[t]:[];}/*v114: exactly one type per rack*/" + h[j:]
rep('aria-label="Rack finish"><span class="fl">Finish</span>', 'aria-label="Rack type"><span class="fl">Type</span>')
rep("if(nw)S.f.m.her=set().m.length>0;", "if(nw)S.f.m.her=false;/*v114 picks off by default*/")
rep("S.f.m.her=set().m.length>0;S.tilesOpen=false;renderAll();jump('s-mats');}", "S.f.m.her=false;S.tilesOpen=false;renderAll();jump('s-mats');}")
rep("S.f.m.her=true;if(!queue('m').length)S.f.m.her=false;", "S.f.m.her=false;")
rep("S.f.r.her=herRacks().length>0;", "S.f.r.her=false;")
# her real picks still LEAD the mat deck with picks off (with or without a colour), and are never cut by the per-brand cap
rep("function matDeck0(){const f=S.f.m;let ids=MSL(f.her?matPool():colorPool());",
    "function matDeck0(){const f=S.f.m;let ids=MSL(f.her?matPool():colorPool());if(!f.her){const hp=MSL(matPool()).filter(herMat),hs=new Set(hp);ids=[...hp,...ids.filter(x=>!hs.has(x))];}/*v114: picks off by default, her picks still lead*/")
rep("ids=f.her?[...ids.filter(herMat),...CSORT(ids.filter(id=>!herMat(id)),C)]:CSORT(ids,C);", "ids=[...ids.filter(herMat),...CSORT(ids.filter(id=>!herMat(id)),C)];")
rep("if(!f.brand)ids=BCAP(ids,f.her?herMat:NOK,id=>M[id].bn);", "if(!f.brand)ids=BCAP(ids,herMat,id=>M[id].bn);")
js = """<script>/*v114 white dot*/(function(){try{if(!RFAMS.includes('white'))RFAMS.push('white');FAMN.white='White';FAMC.white='#fbfaf6';((D.tv&&D.tv.rw)||[]).forEach(k=>{if(R[k]){const rf=R[k].rf||[];if(!rf.includes('white'))R[k].rf=[...rf,'white'];}});}catch(e){}})();</script>"""
j = h.rindex('</body>') if '</body>' in h else len(h); h = h[:j] + js + h[j:]
h = h.replace('</style>', '.dot[data-fam="white"] i{box-shadow:inset 0 0 0 1px #cfc6c0}</style>', 1)
open(P, 'w').write(h); print('types114 ok')
