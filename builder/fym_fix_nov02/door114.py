"""v114 NOTHING PRESELECTED (Tiffany via coordinator Nov 3): on first open neither door looks selected (both neutral, same style)
until a door is tapped (or a tile set / mat is already chosen, e.g. after a restore). The tiles door content still shows below.
Gate [35] (tour walk) + [146] static check. Idempotent."""
import sys, os
P = sys.argv[1]; P = P if P.endswith('.html') else os.path.join(P, 'index.html'); h = open(P).read()
if '/*v114 door neutral*/' in h: print('door114 already'); sys.exit()
a = "function doorBtns(){const d=S.door||'tiles';"
b = "function doorBtns(){/*v114 door neutral*/const d=(S.doorPicked||S.set!=null||!!S.dmat)?(S.door||'tiles'):'';"
assert h.count(a) == 1, h.count(a); h = h.replace(a, b)
js = "<script>/*v114 door tap*/document.addEventListener('click',e=>{if(e.target.closest&&e.target.closest('[data-door]'))S.doorPicked=true;},true);</script>"
j = h.rindex('</body>') if '</body>' in h else len(h); h = h[:j] + js + h[j:]
open(P, 'w').write(h); print('door114 ok')
