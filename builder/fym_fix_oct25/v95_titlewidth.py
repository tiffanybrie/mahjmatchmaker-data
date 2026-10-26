"""FYM v95: match-card title never runs wider than the mat/button column (Tiffany Oct 26 10:48am: long names like
EAST MEETS WEST TORTOISE SHELL 'scream' and overhang the mat edges; the mat + blue button form the centre column).
Title width cap = 74% of the card width (= the mat/button column); short names keep their size. Idempotent. Gate [71].
Usage: v95_titlewidth.py <build>"""
import sys
P = sys.argv[1] + '/index.html'; h = open(P).read()
old = "SW=CT==='B'?150:0,TW=W-120-2*SW;"
new = "SW=CT==='B'?150:0,TW=Math.min(W-120-2*SW,W*.74)/* v95 title within mat column */;"
if new not in h:
    assert h.count(old) == 1; h = h.replace(old, new); open(P, 'w').write(h); print('title width capped')
