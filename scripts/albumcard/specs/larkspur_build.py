"""Larkspur album spec: tile racks (lower left) = Tiffany's approved final_lists (config/tile-racks-picks.json).
Rewrites specs/larkspur.json in place; then: python3 scripts/albumcard/gen2.py scripts/albumcard/specs/larkspur.json <outdir>
Oct 15 1pm (Tiffany): her per-set changes live in final_lists (see its _note_oct15). Pippa is rendered twice
(pippa-cherry-red / pippa-magenta) until she picks one. Up to 4 racks per card (card2.html: same angle, same length)."""
import json, os
R = '/home/claude/mahjmatchmaker-data/'
SP = R + 'scripts/albumcard/specs/larkspur.json'
spec = json.load(open(SP)); F = json.load(open(R + 'config/tile-racks-picks.json'))['final_lists']
KEY = {'vault-lilac-soiree': 'lilac-soiree', 'vault-spring-love': 'spring-love'}
VARIANTS = {'pippa': ['cherry-red', 'magenta']}
cards = []
for c in spec['cards']:
    base = c['slug'].split('--')[0] if '--' in c['slug'] else c['slug']
    if base.startswith('pippa'): base = 'pippa'
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
spec['_note'] = spec['_note'].split(' Oct 15')[0] + ' Oct 15: up to 4 tile racks, all the same angle/length; Pippa in two versions (Cherry Red / Magenta) for her pick.'
json.dump(spec, open(SP, 'w'), indent=1, ensure_ascii=False)
print(len(cards), 'cards')
