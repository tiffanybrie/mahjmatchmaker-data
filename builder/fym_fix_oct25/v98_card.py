"""FYM v98 (Version 1.2) match card rack placement (docs/MATCH-INBOX.md, Tiffany Oct 26 6:19pm): on the Mood board ('tri') card
the racks sat too high on the mat, covering its centre (the horse emblem on Mac + Miller Heirloom Fire + Fortune), with too much
gap between two racks. Same fix Main made in the partner graphics drawCard: rh=Math.min(bot-top-lch-30,n*150) and
ry=bot-rh-lch+20 (racks lower, rows tighter). Applies to every format (Story / Post / Pin); the Close up ('stack') card already
keeps racks in their own band below the mat. Idempotent. Gate [91]. Usage: v98_card.py <build>"""
import sys
P = sys.argv[1] + '/index.html'; h = open(P).read()
old = "rh=Math.min(bot-top-lch-30,Math.max(2*r+40,n*170)),rx=30,ry=Math.max(top+110,Math.min(cy-rh/2+48,bot-rh-lch-10));"
new = "rh=Math.min(bot-top-lch-30,n*150),rx=30,ry=bot-rh-lch+20/*v98 racks low*/;"
if new not in h:
    assert h.count(old) == 1, h.count(old); h = h.replace(old, new); open(P, 'w').write(h); print('v98 card racks lowered')
else: print('v98 card already applied')
