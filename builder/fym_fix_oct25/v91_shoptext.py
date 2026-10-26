"""FYM v91 (Tiffany Oct 25 20:07: liked 'Text or email me this list' but it read as one long run of links): each piece gets its own
block with a blank line between: 'TILES · Jasmine by Oh My Mahjong' / link, 'MAT · Elysium by Oh My Mahjong' / link,
'RACKS · Avocado by Bird & Bamboo' / link (rack names without the repeated brand).
Usage: python3 v91_shoptext.py <build_dir>"""
import sys
P = sys.argv[1] + '/index.html'; h = open(P).read()
a = ("const L=pieces().map(id=>{const o=M[id]||R[id]||T[id];if(!o||!o.u)return '';const nm=T[id]?s.name+' tiles':R[id]?o.n:o.n+' mat';"
     "return `${nm} (${o.bn}): ${o.u}`;}).filter(Boolean);")
b = ("const L=pieces().map(id=>{const o=M[id]||R[id]||T[id];if(!o||!o.u)return '';const kind=T[id]?'TILES':R[id]?'RACKS':'MAT';"
     "const nm=T[id]?s.name:R[id]?shortR(id):o.n;return `${kind} \\u00b7 ${nm} by ${o.bn}\\n${o.u}`;}).filter(Boolean);")
assert h.count(a) == 1; h = h.replace(a, b)
a2 = "return `My mahjong match: ${s.name} + ${M[S.fav].n}\\n\\n${L.join('\\n')}"
assert h.count(a2) == 1, h.count(a2); h = h.replace(a2, "return `My mahjong match: ${s.name} + ${M[S.fav].n}\\n\\n${L.join('\\n\\n')}")
open(P, 'w').write(h); print('ok')
