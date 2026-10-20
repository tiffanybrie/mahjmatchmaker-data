"""Jasmine new matches (Oct 20, Tiffany picked from round 2: mats with Jasmine's jade greens + raspberry pink, not all green):
Mahj & Vine Chinoiserie Songbird, Mahj & Vine Porcelain Bloom, Anders Ruff Palm Beach Pink Cabana Blue, Virora Liliora.
Tile racks = config/tile-racks-picks.json final_lists['jasmine'] (B&B Periwinkle Blue + B&B Hot Pink, Oct 20).
Mat racks = matpick.pick (Claude's B&B picks). One gen2 spec per mat.
Run: python3 scripts/albumcard/specs/jasmine_oct20_build.py"""
import json, subprocess, sys
R = '/home/claude/mahjmatchmaker-data/'
sys.path.insert(0, R + 'scripts/albumcard')
from matpick import pick
from PIL import Image
F = json.load(open(R + 'config/tile-racks-picks.json'))['final_lists']
MATS = [('chinoiserie-songbird', 'Mahj & Vine', 'Chinoiserie Songbird', 'Songbird', [135, 245, 1930, 1945]),
        ('porcelain-bloom', 'Mahj & Vine', 'Porcelain Bloom', 'Porcelain Bloom', [135, 245, 1930, 1945]),
        ('palm-beach-pink-cabana-blue', 'Anders Ruff', 'Palm Beach Pink Cabana Blue', 'Palm Beach', [0, 0, 1250, 1250]),
        ('liliora', 'Virora Mahjong', 'Liliora', 'Liliora', [9, 79, 1279, 1567]),
        # Oct 20 9:23am round 3: her green picks from sheet 1 (#1, #2, #9, #11) + #3/#4 from round 2
        ('secret-garden', 'Anders Ruff', 'Secret Garden', 'Secret Garden', [0, 0, 743, 743]),
        ('jade-green-chinoiserie', 'Mahj Squad', 'Jade Green Chinoiserie', 'Jade Chinoiserie', [0, 0, 1000, 1000]),
        ('deep-green-garden-party', 'Miss Mahjong', 'Deep Green Garden Party', 'Garden Party', [0, 0, 1500, 1071]),
        ('flirty-leopards-mint-julep', 'Bespoke Mahjong', 'Flirty Leopards Mint Julep', 'Flirty Leopards', [0, 0, 798, 802]),
        ('zesty-plume', 'Mahj & Vine', 'Zesty Plume', 'Zesty Plume', [135, 245, 1930, 1945]),
        ('flora-belle', 'Anders Ruff', 'Flora Belle', 'Flora Belle', [0, 0, 1250, 1250])]
import sys as _s
ONLY = set(_s.argv[1:])
MR = json.load(open(R + 'config/mat-racks-picks.json'))
for slug, brand, name, short, crop in MATS:
    if ONLY and slug not in ONLY: continue
    f = f'assets/mats/jasmine-oct20/{slug}.jpg'
    key = f'{brand.lower().replace(" & ", "-and-").replace(" ", "-")}-{slug}'
    if key not in MR:
        im = Image.open(R + f).convert('RGB').crop(tuple(crop))
        MR[key] = {'mat': f'{brand} {name}', 'racks': pick(im, exclude=['Hot Pink', 'Periwinkle Blue']), 'files': [f],
                   'approved': None, '_note': 'Claude matpick Oct 20 (Jasmine new matches)'}
    json.dump(MR, open(R + 'config/mat-racks-picks.json', 'w'), indent=1, ensure_ascii=False)
    bslug = brand.lower().replace(' & ', '-and-').replace(' ', '-')
    spec = {'_note': f'Jasmine + {name} (Oct 20)', 'mat_file': f, 'mat_crop': crop, 'mat_key': key, 'max_racks': 4,
            'cards': [{'slug': f'jasmine-{key}', 'set': 'jasmine', 'title': f'Jasmine + {short}', 'col': '#36a272',
                       'tile_file': 'assets/tiles/album/jasmine.jpg', 'tilefit': 'cover', 'racks': F['jasmine'],
                       'file': f'jasmine-mahjong-tiles-{bslug}-{slug}-mat.jpg'}]}
    sp = R + f'scripts/albumcard/specs/jasmine_oct20_{slug}.json'
    json.dump(spec, open(sp, 'w'), indent=1, ensure_ascii=False)
    subprocess.run(['python3', R + 'scripts/albumcard/gen2.py', sp, R + 'assets/cards/jasmine-oct20'], check=True)
