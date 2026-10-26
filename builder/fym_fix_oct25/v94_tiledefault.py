"""FYM v94 (Tiffany Oct 26 8:24am): Start with tiles opens with NO colour chip selected (Holiday was pre-selected) and shows
every tile set A-Z. Tapping a chip still filters; tapping it again clears back to the full A-Z list. Version label -> 94.
Usage: v94_tiledefault.py <build>"""
import sys
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
old = "if(S.tcol==null)S.tcol=tileOrder()[0];"; n = h.count(old); assert n >= 2, n
h = h.replace(old, "if(S.tcol==null)S.tcol='';/* v94: no default chip, all sets A-Z */")
h = h.replace('Version 93', 'Version 94'); open(P, 'w').write(h); print('patched', n)
