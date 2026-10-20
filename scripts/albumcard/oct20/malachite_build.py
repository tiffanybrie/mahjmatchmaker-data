"""Malachite new matches, Oct 20 rebuild (Ready to Ship l-mal-cards2 + c5-malachite-new).
Her 3 changes (Oct 18 12:58pm): brighten the Jardin needlepoint photo (assets/mats/clean/jardin-de-los-jefes-canvas-bright.jpg,
made by specs/malachite-new/brighten_jardin.py); cancel Manor Garden; White Lotus mat racks use MMSIO, not Dijon.
Order = her saved c5-malachite-new order minus Manor Garden. Tile racks = final_lists malachite. Mat racks = the ones on the
Oct 17 cards she reviewed, except Garden Party Deep Green, which takes her Oct 20 9:33am registry pick (one set of racks per mat).
Usage: python3 malachite_build.py <workdir>; then gen2.py <workdir>/spec.json assets/cards/malachite-oct20"""
import json, io, base64, sys, os
from PIL import Image
R = '/home/claude/mahjmatchmaker-data/'; W = sys.argv[1]; os.makedirs(W, exist_ok=True)
TR = json.load(open(R + 'config/tile-racks-picks.json'))['final_lists']['malachite']
REG = json.load(open(R + 'config/mat-racks-picks.json'))
MMSIO = 'Miss Mahjong Scalloped Iridescent Opal'
CARDS = [  # name, brand (card + link), mat photo, crop, mat racks
 ('Serenity', 'Amanda Toppe', 'assets/mats/amanda-toppe/serenity.jpg', None, ['Bird & Bamboo Petal Purple', 'Bird & Bamboo Moss']),
 ('Midori Shadows', 'Golden Pond Mahjong', 'assets/mats/golden-pond-mahjong/midori-shadows.jpg', None, ['Bird & Bamboo Red', 'Bird & Bamboo Peony']),
 ('Garden Party Deep Green', 'Miss Mahjong', 'assets/mats/miss-mahjong/garden-party-deep-green-corner.jpg', [0, 0, 820, 820], REG['miss-mahjong-deep-green-garden-party']['racks']),
 ('White Lotus', 'Mahj Tile Haus', 'assets/mats/mahj-tile-haus/white-lotus-WATERMARKED-no-social.jpg', None, [MMSIO, 'Bird & Bamboo Moss']),
 ('Garden Party Powder Blue', 'Miss Mahjong', 'assets/mats/miss-mahjong/garden-party-powder-blue-corner.jpg', [0, 0, 810, 810], ['Bird & Bamboo Powder Blue', 'Bird & Bamboo Light Pink']),
 ('Jardín de los Jefes', 'Tigre de Tartan', 'assets/mats/clean/jardin-de-los-jefes-canvas-bright.jpg', None, ['Bird & Bamboo Radish', 'Bird & Bamboo Basil']),
 ('Garden Party Lavender', 'Miss Mahjong', 'assets/mats/miss-mahjong/garden-party-lavender-corner.jpg', [0, 0, 800, 800], ['Bird & Bamboo French Blue', 'Bird & Bamboo Lilac']),
 ('Pink Tiger', 'YOLO Mahjong', 'assets/mats/yolo-mahjong/pink-tiger-flat-v2.jpg', [8, 8, 732, 732], ['Bird & Bamboo Carrot', 'Bird & Bamboo Dark Teal']),
]
FILES = {'Serenity': 'amanda-toppe-serenity', 'Midori Shadows': 'golden-pond-mahjong-midori-shadows', 'Garden Party Deep Green': 'miss-mahjong-garden-party-deep-green',
         'White Lotus': 'mahj-tile-haus-white-lotus', 'Garden Party Powder Blue': 'miss-mahjong-garden-party-powder-blue',
         'Jardín de los Jefes': 'tigre-de-tartan-jardin-de-los-jefes', 'Garden Party Lavender': 'miss-mahjong-garden-party-lavender', 'Pink Tiger': 'yolo-mahjong-pink-tiger'}
def uri(im):
    im = im.convert('RGB'); im.thumbnail((1400, 1400)); b = io.BytesIO(); im.save(b, 'JPEG', quality=90)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
cards, man = [], []
for i, (nm, brand, f, box, mr) in enumerate(CARDS, 1):
    im = Image.open(R + f)
    if box: im = im.crop(tuple(box))
    fn = f"malachite-mahjong-tiles-{FILES[nm]}-mat.jpg"
    cards.append({'slug': f'mal{i:02d}', 'title': f'Malachite + {nm}', 'col': '#37503b', 'tile_file': 'assets/tiles/album/malachite.jpg', 'tilefit': 'cover',
                  'racks': TR, 'mat_racks': mr, 'file': fn, 'mat': uri(im), 'code': '10% OFF  USE CODE : MAHJMATCH'})
    man.append({'order': i, 'mat': nm, 'brand': brand, 'file': fn, 'src': f, 'racks': TR, 'mat_racks': mr})
json.dump({'_note': 'Malachite new matches Oct 20', 'cards': cards, 'max_racks': 4, 'tile_brand': 'Miss Mahjong'}, open(W + '/spec.json', 'w'))
json.dump({'set': 'Malachite', 'cancelled': ['Manor Garden'], 'cards': man}, open(W + '/manifest.json', 'w'), indent=1, ensure_ascii=False)
print(len(cards), 'cards')
