"""FYM v94: zoom snaps to exactly 1 near 1 (QA Oct 26: +,+,-,- left z.s=1.0000000000000002, and with zoom persisting,
drag-swipe stayed dead on every later card). Idempotent. Gate [68]. Usage: v94_zoomsnap.py <build>"""
import sys
P = sys.argv[1] + '/index.html'; h = open(P).read()
old = "const zoomAt=(ns,cx,cy,a)=>{ns=Math.max(1,Math.min(4,ns));"
new = "const zoomAt=(ns,cx,cy,a)=>{ns=Math.max(1,Math.min(4,ns));if(Math.abs(ns-1)<0.02)ns=1;/* v94 snap */"
if new not in h:
    assert h.count(old) == 1; h = h.replace(old, new); open(P, 'w').write(h); print('zoom snap added')
