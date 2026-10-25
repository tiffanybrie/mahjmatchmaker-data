"""FYM v85 (Tiffany Oct 25 14:43): the match card used a SEPARATE 'HD' tile photo (hd/index.json 't' entries, some pulled from the
brand's listing photos, e.g. Mahjong Row & Co. Ash Burl = a faces close-up) instead of the tile photo the shopper matched to.
Rule: the card's tile picture is ALWAYS the exact photo shown on the swipe screen (tileFull(s)), the cleared mock-ready photo.
Gate [44] keeps it that way.
Usage: python3 v85_cardtile.py <build_dir>  (in place)"""
import sys
P = sys.argv[1] + '/index.html'; h = open(P).read()
a = "hdOr('t',s.tile,pile(s)).then(lk)"
assert h.count(a) == 1
h = h.replace(a, "Promise.resolve(tileFull(s)||pile(s)).then(lk)")
open(P, 'w').write(h); print('ok')
