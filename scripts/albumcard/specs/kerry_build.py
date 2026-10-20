"""Kerry mat (BettyJuneJeannette, Etsy) match cards, Oct 20 2am. Tiffany picks: Pearlescent (Jasmine dropped Oct 20: greens clash), Moonlight,
La Fete, Willow, Talulah + Coquette. Mat racks (Tiffany): Miss Mahjong Scalloped Iridescent Opal, a clear scallop
(brand TBD, no photo yet), B&B Ballet Pink. Kerry has no affiliate yet -> footer SHOP THE MATCH.
Run: python3 scripts/albumcard/specs/kerry_build.py && python3 scripts/albumcard/gen2.py scripts/albumcard/specs/kerry.json assets/cards/kerry"""
import json
R = '/home/claude/mahjmatchmaker-data/'
F = json.load(open(R + 'config/tile-racks-picks.json'))['final_lists']
COL = json.load(open(R + 'scripts/albumcard/holiday_title_colors.json'))
MR = json.load(open(R + 'config/mat-racks-picks.json'))
MR['kerry'] = {'mat': 'BettyJuneJeannette The Kerry', 'racks': ['Bird & Bamboo Ballet Pink', 'Miss Mahjong Scalloped Iridescent Opal', 'Mahj Mood Scalloped Clear Acrylic'],
               'files': ['assets/mats/etsy/bettyjunejeannette/kerry-2.jpg'], 'approved': '2026-10-20',
               '_note': 'Tiffany Oct 20 2am: MMSIO at least, probably a clear scallop (which brand? no photo yet), B&B Ballet Pink.'}
json.dump(MR, open(R + 'config/mat-racks-picks.json', 'w'), indent=1, ensure_ascii=False)
SETS = [('pearlescent', 'Pearlescent'), ('moonlight', 'Moonlight'), ('la-fete', 'La Fete'),
        ('willow', 'Willow'), ('talulah', 'Talulah'), ('coquette', 'Coquette'),
        ('birdie', 'Birdie'), ('dandy', 'Dandy'), ('luminaire', 'Luminaire'), ('taylor', 'Taylor'), ('sorbet', 'Sorbet')]  # Oct 20 noon: Tiffany approved these 5 too
cards = []
for i, (s, n) in enumerate(SETS, 1):
    cards.append({'slug': f'{s}-kerry', 'set': s, 'order': i, 'title': f'{n} + Kerry', 'col': COL.get(s, '#7a9a6a'),
                  'tile_file': f'assets/tiles/album/{s}.jpg', 'tilefit': 'cover', 'racks': F[s],
                  'file': f'{s}-mahjong-tiles-bettyjunejeannette-kerry-mat.jpg'})
spec = {'_note': __doc__.split('\n')[0], 'mat_file': 'assets/mats/etsy/bettyjunejeannette/kerry-2.jpg',
        'mat_crop': [181, 558, 2049, 2429], 'mat_key': 'kerry', 'max_racks': 4,
        'code': 'SHOP THE MATCH : MAHJMATCHMAKER.COM', 'cards': cards}
json.dump(spec, open(R + 'scripts/albumcard/specs/kerry.json', 'w'), indent=1, ensure_ascii=False)
for c in cards: print(c['title'], c['racks'])
