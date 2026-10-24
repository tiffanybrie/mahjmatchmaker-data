"""FYM v82 Tiffany's picks ON vs OFF (Tiffany Oct 23 3:55pm Amara, 8:27pm Heritage + Holiday, 8:35pm racks).
 - Mats, picks OFF: the deck is the colour-ranked list for the set (her picks mixed in where the colour ranking puts them,
   her retired picks at the end), never "her picks first". With a colour or Holiday filter on, the filter decides and the
   colour sort orders it. Picks ON is unchanged (only her picks).
 - Racks mirror the mats: when a mat goes to the racks, Tiffany's picks start ON if she has racks for that pairing
   (her racks + goes-with-everything), otherwise OFF (colour ranking, partners first).
Usage: python3 v82_picks.py <build_dir>"""
import sys
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
def rep(old, new, n=1):
    global h
    c = h.count(old); assert c == n, f'expected {n} x {old[:90]!r}, found {c}'; h = h.replace(old, new)
rep("function matDeck(){const f=S.f.m;let ids=MSL(matPool());",
    "function colorPool(){const r=set().rank.map(i=>D.order[i]).filter(id=>M[id]&&!M[id].hid&&!M[id].rt);const s=new Set(r);return [...r,...set().m.map(x=>x[0]).filter(id=>M[id]&&!M[id].hid&&!s.has(id))];}/* v82: picks off = colour ranking only */\n"
    "function matDeck(){const f=S.f.m;let ids=MSL(f.her?matPool():colorPool());")
rep("ids=[...ids.filter(herMat),...CSORT(ids.filter(id=>!herMat(id)),C)];}}",
    "ids=f.her?[...ids.filter(herMat),...CSORT(ids.filter(id=>!herMat(id)),C)]:CSORT(ids,C);}}")
rep("function renderRacks(){const el=$('s-racks');if(S.set==null){el.innerHTML='';return;}",
    "function renderRacks(){const el=$('s-racks');if(S.set==null){el.innerHTML='';return;}if(S.fav&&S._rdef!==S.fav+'|'+S.set){S._rdef=S.fav+'|'+S.set;S.f.r.her=herRacks().length>0;}")
rep("rpick:[]});S.f.r={fam:[],brand:'',her:false};}S.made=false;}", "rpick:[]});S.f.r={fam:[],brand:'',her:false};S._rdef=null;}S.made=false;}")
rep("That’s all the ${k==='m'?'mats':'racks'} that fit your current filters with <b>Tiffany’s picks on</b>. To see all the possibilities, turn Tiffany’s picks off.",
    "<span>That’s all the ${k==='m'?'mats':'racks'} that fit your current filters with <b>Tiffany’s picks on</b>. To see all the possibilities, turn Tiffany’s picks off.</span>")
open(P, 'w').write(h); print('v82 picks applied')
