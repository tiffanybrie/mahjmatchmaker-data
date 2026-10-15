"""December 1994 tile-rack comparison (Tiffany, Oct 15: "let me see B&B Red, Brick Red, Cherry Red and Evergreen to
help me make decision. I don't think we'll use almond. More inclined to use PLM Oak to pick up on golden tones of
backs and reindeer.")
3 representative December 1994 cards x 5 options. Each option REPLACES Almond as the 2nd tile rack; Radish stays as
the 1st (lower left, as on the 5 live cards); the mat pick stays in the B&B chart (upper right).
B&B = generated (builder/bbrack.py, doc 48); PLM Oak = real photo (assets/racks/card/).
Usage: python3 december_1994_rack_options.py <data_d94.json> <outdir>   (renders via gen_hol.py)"""
import json, sys, os, subprocess, copy
R = '/home/claude/mahjmatchmaker-data/'
src, out = sys.argv[1], sys.argv[2]
CARDS = ['candy-cane-lane-mahjong-mat', 'c-cognac-mat', 's-highland-heritage-plaid-mahjong-by-si']
OPTS = {'bb-red': 'bb:Red', 'bb-brick-red': 'bb:Brick Red', 'bb-cherry-red': 'bb:Cherry Red', 'bb-evergreen': 'bb:Evergreen',
        'plm-oak': 'Peace Love Mahjong Oak'}
D0 = json.load(open(src))
for name, k in OPTS.items():
    D = copy.deepcopy(D0); D.setdefault('RK', {})['Peace Love Mahjong Oak'] = ['Peace Love Mahjong Oak']
    g = next(g for g in D['G'] if g['t'] == 'december-1994')
    for r in g['rows']:
        if r['m'] in CARDS: r['def'] = ['bb:Radish', k] + [x for x in r['def'] if x not in ('bb:Radish', 'bb:Almond')]
    p = f'{out}/work/{name}.json'; os.makedirs(os.path.dirname(p), exist_ok=True); json.dump(D, open(p, 'w'))
    subprocess.run(['python3', R + 'scripts/albumcard/gen_hol.py', p, f'{out}/cards/{name}'] + [f'december-1994:{c}' for c in CARDS], check=True)
