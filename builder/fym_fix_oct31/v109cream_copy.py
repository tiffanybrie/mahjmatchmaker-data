"""Copy the v109cream data change (D.mats + D.sets from the rebuilt app index) into an existing copy's index (website
fym-v109 index or artifact pub109 index) without touching anything else (tiles/paths/thumbs differ per copy on purpose).
Usage: python3 v109cream_copy.py <rebuilt app index> <copy index in> <copy index out>"""
import sys, json
A, I, O = sys.argv[1:4]
def load(p):
    h = open(p).read(); i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:]); return h, i, D, e + i
_, _, NA, _ = load(A); h, i, D, e = load(I)
for k in ('mats', 'sets'): D[k] = NA[k]
open(O, 'w').write(h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[e:])
print('copied mats+sets ->', O)
