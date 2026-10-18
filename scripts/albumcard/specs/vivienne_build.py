"""Vivienne mat edition album (Oct 18). Source of truth = Tiffany's Vivienne swipe book (MwPm52JUmChMHxoZh1mZe2,
collection vivienne-mat-in-tubeswipe + _notes + _status, swiped Oct 13): 16 yeses.
Order: TOP = her written ranking (#1 Pippa, #2 Solara, #3 Coquette, #4 Spring Love, #5 Jade, #6 Papaya Spritz) + her
other starred yes (Pearlescent); BEST = yeses she wrote commentary for (swipe order); MORE = yeses with no note.
Hummingbird WAS a yes (with a loving note), not starred, not in her top 6 -> BEST. (config/matcard/vivienne.json's
Oct 17 note saying it was Claude-added was wrong.)
Tile racks = config/tile-racks-picks.json final_lists (Hummingbird: holiday-picker picks).
Mat racks = her Oct 15 Vivienne list (+B&B Hot Pink Metallic, +B&B Jade, +M&M Scalloped Beechwood, +Miss Mahjong
Cornflower Scallop; Jade & Brass and Petal Purple out) -> config/mat-racks-picks.json 'vivienne'.
Run: python3 scripts/albumcard/specs/vivienne_build.py && python3 scripts/albumcard/gen2.py scripts/albumcard/specs/vivienne.json assets/cards/vivienne"""
import json
R = '/home/claude/mahjmatchmaker-data/'
F = json.load(open(R + 'config/tile-racks-picks.json'))['final_lists']
COL = json.load(open(R + 'scripts/albumcard/holiday_title_colors.json'))
LK = {c['slug']: c for c in json.load(open(R + 'scripts/albumcard/specs/larkspur.json'))['cards']}
ORDER = [  # (swipe id, tier, note-for-caption)
 ('pippa','TOP','#1'), ('solara','TOP','#2'), ('coquette','TOP','#3'), ('vault-spring-love','TOP','#4 (retired)'),
 ('jade','TOP','#5'), ('papaya-spritz','TOP','#6 · pair mat'), ('pearlescent','TOP','starred'),
 ('amara','BEST',''), ('sorbet','BEST',''), ('willow','BEST',''), ('luminaire','BEST',''), ('taylor','BEST',''),
 ('hummingbird','BEST',''), ('palm-royale','MORE',''), ('tortoise','MORE',''), ('moonlight','MORE',''),
]
NAMES = {'vault-spring-love': 'Spring Love', 'papaya-spritz': 'Papaya Spritz', 'palm-royale': 'Palm Royale'}
cards = []
for i, (sid, tier, note) in enumerate(ORDER, 1):
    base = sid.replace('vault-', '')
    name = NAMES.get(sid, base.replace('-', ' ').title())
    lk = LK.get(sid, {})
    c = {'slug': sid, 'order': i, 'tier': tier, 'rank_note': note, 'title': f'{name} + Vivienne',
         'col': lk.get('col') or COL.get(base) or '#7a9a6a',
         'tile_file': lk.get('tile_file') or f'assets/tiles/album/{base}.png' if base == 'hummingbird' else (lk.get('tile_file') or f'assets/tiles/album/{base}.jpg'),
         'tilefit': 'cover', 'file': f'{sid}-mahjong-tiles-oh-my-mahjong-vivienne-mat.jpg'}
    if base == 'hummingbird':
        c['tile_file'] = 'assets/tiles/album/hummingbird.png'; c['tile_brand'] = 'Sunday Mahjong'; c['col'] = '#6f8f5a'
        c['racks'] = ['Middle & Main Hawksbill Heritage Tortoise', 'Miss Mahjong Blonde Tortoise & Brass', 'Middle & Main Scalloped Beechwood']
    else:
        c['racks'] = F.get(base) or lk.get('racks')
    if 'tile_brand' in lk: c['tile_brand'] = lk['tile_brand']
    if base == 'coquette': c['code'] = 'SHOP THE MATCH : MAHJMATCHMAKER.COM'  # Coquette never gets MAHJMATCH; footer wording pending her call
    cards.append(c)
spec = {'_note': __doc__.split('\n')[0] + ' 16 cards, TOP 7 / BEST 6 / MORE 3.', 'mat_file': 'assets/launches/omm-vivienne-mat/01.jpg',
        'mat_crop': [0, 0, 2195, 2195], 'mat_key': 'vivienne', 'max_racks': 4, 'cards': cards}
json.dump(spec, open(R + 'scripts/albumcard/specs/vivienne.json', 'w'), indent=1, ensure_ascii=False)
BANNED = ('Bird & Bamboo Weathered Oak','Bird & Bamboo Provincial','Bird & Bamboo Red Mahogany','Bird & Bamboo Dark Walnut','Bird & Bamboo Almond','Bird & Bamboo Tudor','Bird & Bamboo Clear Stain')
for c in cards:
    bad = [r for r in c['racks'] if r in BANNED]
    print(c['order'], c['tier'], c['slug'], c['racks'], 'BANNED:' + str(bad) if bad else '')
