"""v108 (Oct 31): the 97 non-partner adds (Bougie Mahjong, Mahj & Moon) are colour-ranked by v104rank, but they must not push out a set's
established top 5 colour-deck mats (QA'd in 1.9.2; e.g. Aloha's yellow-plumeria leads, gate [76]). For each set: the first 5 visible
non-v108 mats of the source build's s.cr stay the first 5; v108 mats ranked inside them move to just after them (same relative order).
Usage: python3 v108cr.py <source b107 index> <b108 dir>"""
import sys, json
S, B = sys.argv[1], sys.argv[2]; P = B + '/index.html'
def load(p):
    h = open(p).read(); i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:]); return h, i, i + e, D
_, _, _, D0 = load(S); h, i, end, D = load(P)
o0 = D0['order']; o1 = D['order']; M = D['mats']
NEW = {j for j, k in enumerate(o1) if M.get(k, {}).get('add') == 'oct31-v108'}
vis = lambda k: k in M and not M[k].get('hid') and not M[k].get('rt')
src = {s['slug']: s.get('cr', []) for s in D0['sets']}
moved = 0
for s in D['sets']:
    cr = s.get('cr'); old = src.get(s['slug'])
    if not cr or not old: continue
    lead = [o1.index(o0[j]) for j in old if vis(o0[j])][:5]  # same keys, indices in the new order
    lead = [j for j in lead if j in cr]
    if not lead: continue
    cut = max(cr.index(j) for j in lead)
    early_new = [j for j in cr[:cut + 1] if j in NEW]
    if not early_new: continue
    rest = [j for j in cr if j not in early_new]
    at = rest.index(lead[-1]) + 1 if lead[-1] in rest else len(rest)
    s['cr'] = rest[:at] + early_new + rest[at:]; moved += 1
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]; open(P, 'w').write(h)
print('v108cr: sets adjusted', moved)
