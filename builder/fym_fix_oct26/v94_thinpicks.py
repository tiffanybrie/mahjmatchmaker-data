"""FYM thin-album hearts (NOT PUBLISHED; run in the next FYM build AFTER Ops has pasted the cards live).
Tiffany's 41 hearts in the thin-album review (artifact UQy4YpGD2RR5Z1WqswJWYM, db 'votes', Oct 23-24) became match cards appended
to 9 live albums (site/livepatch/thin-albums-oct26/README.md). They are her real picks (CLAUDE.md FYM rule 4), so each one joins its
set's match list (m) at the END (same place as on the album page), with racks = the set's tile racks (config/tile-racks-picks.json
final_lists) + the mat's racks (config/mat-racks-picks.json), resolved to FYM rack ids by name; labels with no FYM rack are skipped.
Also: locks.json sets.<slug>.m updated (approved change, her hearts), the live album snapshot gets the new cards at the end, D.ao
recomputed (album_order.compute), mat u set to the card's shop link when the FYM mat has none.
Then runs builder/fym_fix_oct22/rack_picks.py --locks (mat's own picks first + D.lm, gate [36]; the 27 new mat entries in
config/mat-racks-picks.json are Claude matpicks, approved null, same as the album cards).
Config: config/fym-thin-picks-oct26.json. Idempotent.
Usage: python3 builder/fym_fix_oct26/v94_thinpicks.py <build_dir>"""
import sys, os, json
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
sys.path.insert(0, REPO + 'builder/fym_fix_oct21')
import album_order
B = sys.argv[1]
CFG = json.load(open(REPO + 'config/fym-thin-picks-oct26.json'))
LOCKS = REPO + 'builder/fym_flags/locks.json'; SNAP = album_order.LIVE
h = open(B + '/index.html').read(); i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
M, R = D['mats'], D['racks']; L = json.load(open(LOCKS))
byname = {}
for k, r in R.items(): byname.setdefault(r.get('n', ''), k)
byname.update({'Middle & Main Hawksbill Heritage Tortoise': 'mm:Hawksbill',  # card label -> FYM rack id (FYM names differ)
               'Miss Mahjong Scalloped Iridescent Opal': 'missmahjong.com/iridescent-opal-scalloped-acrylic-racks',
               'Peace Love Mahjong Acrylic Burl': 'peacelovemahjong.com/acrylic-burlwood-mahjong-racks-pushers-set-of-4'})
A = json.load(open(SNAP)); AS = {a['slug']: a for a in A}
added, skipped, nores = [], [], set()
for p in CFG['picks']:
    s = album_order.set_for_album(D, p['set'])
    if not s or p['key'] not in M: skipped.append((p['set'], p['name'], 'no FYM set' if not s else 'mat not in FYM')); continue
    if any(e[0] == p['key'] for e in s['m']): continue
    racks = []
    for lab in p['racks']:
        k = byname.get(lab)
        if k: racks.append(k)
        else: nores.add(lab)
    s['m'].append([p['key'], list(dict.fromkeys(racks))])
    if s['slug'] in L['sets']: L['sets'][s['slug']]['m'] = s['m']
    if p.get('shop') and not M[p['key']].get('u'): M[p['key']]['u'] = p['shop']
    a = AS.get(p['set'])
    if a is not None and not any(c.get('img', '').endswith('/' + p['file']) for c in a['cards']):
        a['cards'].append({'n': '%02d' % (len(a['cards']) + 1), 'img': p['img'], 'mat': p['name'], 'brand': p['brand'], 'retired': False})
        if isinstance(a.get('n'), int): a['n'] += 1
    added.append((s['slug'], p['name']))
if added: L['_changes'].append(f"2026-10-26: {len(added)} thin-album hearts appended to sets m ({', '.join(sorted({a for a, _ in added}))}); Tiffany's hearts in the thin-album review Oct 23-24 = her real picks (config/fym-thin-picks-oct26.json)")
json.dump(L, open(LOCKS, 'w'), indent=1, ensure_ascii=False)
json.dump(A, open(SNAP, 'w'), indent=0)
D['ao'], _ = album_order.compute(D)
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
open(B + '/index.html', 'w').write(h)
import subprocess
subprocess.run([sys.executable, REPO + 'builder/fym_fix_oct22/rack_picks.py', B, '--locks'], check=True)  # mat picks first, D.lm (gate [36])
print(f'added {len(added)}; skipped {skipped}; rack labels with no FYM rack: {sorted(nores)}')
