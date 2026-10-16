"""Oct 16: build data6.json for gen_hol3.py. Tile-side racks = Tiffany's holiday picker picks (db picks, exported to
config/holiday-picker-picks.json) or her locked final_lists; only the cards that are live (holiday_manifest.json)."""
import json, sys
R = '/home/claude/mahjmatchmaker-data/'
D = json.load(open(sys.argv[1])); out = sys.argv[2]
F = json.load(open(R + 'config/tile-racks-picks.json'))['final_lists']
PK = json.load(open(R + 'config/holiday-picker-picks.json'))
LIVE = {(x['tile'], x['mat']) for x in json.load(open(R + 'scripts/albumcard/holiday_manifest.json'))}
URL = {'www.middleandmainmahjong.com/milk-glass-collection-mahjong-rack-and-pusher-set-of-4': 'Middle & Main Milk Glass Scalloped Acrylic',
       'www.middleandmainmahjong.com/golden-grain-beechwood-mahjong-rack-and-pusher-set-of-4': 'Middle & Main Scalloped Beechwood',
       'missmahjong.com/jade-and-brass-acrylic-racks': 'Miss Mahjong Jade & Brass',
       'missmahjong.com/blonde-tortoise-and-brass-acrylic-racks': 'Miss Mahjong Blonde Tortoise & Brass',
       'missmahjong.com/iridescent-opal-scalloped-acrylic-racks': 'Miss Mahjong Scalloped Iridescent Opal',
       'www.bambirdboutique.com/wooden-mahjong-rack-pusher-set': 'Bam Bird Boutique Walnut',
       'mm:Hawksbill': 'Middle & Main Hawksbill Heritage Tortoise'}
def norm(k):
    if k.startswith('Bird & Bamboo '): return 'bb:' + k[len('Bird & Bamboo '):]
    if k.startswith('plm:'): return 'Peace Love Mahjong ' + k[4:]
    return URL.get(k, k)
src = {}
for g in D['G']:
    t = g['t']
    if t in PK: tl = [norm(k) for k in PK[t]['picks']]; src[t] = 'picker'
    elif t in F: tl = [norm(k) for k in F[t]]; src[t] = 'locked'
    else: tl = None; src[t] = 'default'
    g['rows'] = [r for r in g['rows'] if (t, r['m']) in LIVE]
    for r in g['rows']:
        if tl: r['tiles'] = tl
json.dump(D, open(out, 'w'))
print({k: sum(1 for v in src.values() if v == k) for k in ('picker', 'locked', 'default')}, sum(len(g['rows']) for g in D['G']), 'rows')
