"""v114 UI (Tiffany Nov 3 2:27pm, ANSWERS): RACK STEP: the rack menu / filter row moves from BETWEEN the chosen mat and the rack
photo to BELOW the rack deck, so the mat and the rack sit right next to each other (she keeps hitting it making 'pick your racks'
social: you can't see mat + racks together). Same layout the mat step already has (tile photo + mat deck together, view / filters /
search in .s2ctl below the deck). Gate [148]. Idempotent. Usage: python3 ui114b.py <build dir or index.html>"""
import sys, os
P = sys.argv[1]; P = P if P.endswith('.html') else os.path.join(P, 'index.html'); h = open(P).read()
if '/*v114 rack filters below*/' in h: print('ui114b already'); sys.exit()
a = """<div class="rfil">${filters('r')}</div>${deck('r')}</div>`+acts('r')"""
assert h.count(a) == 1, h.count(a)
h = h.replace(a, """${deck('r')}</div><div class="s2ctl rctl"><div class="rfil">${filters('r')}</div></div>`+acts('r')""")
h = h.replace('</style>', '/*v114 rack filters below*/</style>', 1)
open(P, 'w').write(h); print('ui114b ok')
