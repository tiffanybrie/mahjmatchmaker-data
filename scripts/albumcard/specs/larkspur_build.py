"""Larkspur album spec: tile racks (lower left) = Tiffany's approved final_lists (config/tile-racks-picks.json).
Rewrites specs/larkspur.json in place; then: python3 scripts/albumcard/gen2.py scripts/albumcard/specs/larkspur.json <outdir>
Oct 15 1pm (Tiffany): her per-set changes live in final_lists (see its _note_oct15). Up to 4 racks per card (card2.html: same angle, same length).
Oct 15 6:50pm: she picked Magenta for Pippa -> ONE pippa card (final_lists 'pippa'); see _note_oct15_evening for the other changes."""
import json, os
R = '/home/claude/mahjmatchmaker-data/'
SP = R + 'scripts/albumcard/specs/larkspur.json'
spec = json.load(open(SP)); F = json.load(open(R + 'config/tile-racks-picks.json'))['final_lists']
KEY = {'vault-lilac-soiree': 'lilac-soiree', 'vault-spring-love': 'spring-love'}
VARIANTS = {}  # Oct 15 evening: Pippa = Magenta only
cards = []
for c in spec['cards']:
    base = c['slug'].split('--')[0] if '--' in c['slug'] else c['slug']
    if base.startswith('pippa'):
        base = 'pippa'
        if any(x['slug'] == 'pippa' for x in cards): continue
        c = dict(c, slug='pippa', file='pippa-mahjong-tiles-oh-my-mahjong-larkspur-mat.jpg')
    if base in VARIANTS:
        if any(x['slug'].startswith(base + '-') for x in cards): continue
        for v in VARIANTS[base]:
            k = f'{base}-{v}'
            cards.append(dict(c, slug=k, racks=F[k], file=f'{base}-mahjong-tiles-oh-my-mahjong-larkspur-mat-{v}.jpg'))
        continue
    k = KEY.get(base, base)
    if k in F: c = dict(c, racks=F[k])
    cards.append(c)
spec['cards'] = cards; spec['max_racks'] = 4
spec['_note'] = spec['_note'].split(' Oct 15')[0] + ' Oct 15: up to 4 tile racks, all the same angle/length. Oct 15 evening: one Pippa card (Magenta); racks off the left edge, tile logo flag (card2.html).'
json.dump(spec, open(SP, 'w'), indent=1, ensure_ascii=False)
print(len(cards), 'cards')
