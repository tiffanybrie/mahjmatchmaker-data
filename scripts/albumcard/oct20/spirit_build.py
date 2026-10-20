"""Spirit of Christmas (Peace Love Mahjong) holiday cards, Oct 20 rebuild.
Her Ready to Ship c5-spirit (Oct 18 1:12pm): saved ORDER for the 10 cards; her other feedback was sent in chat ("Already sent
this") and is NOT in any saved record this build could read, so only these changes are made:
- her order (files renumbered 01-10 in her order),
- mats trimmed of the white product-photo background so the mat fills the card (the Oct 17 cards showed a white frame),
- every card keeps its Oct 17 mat racks (her mat racks were not questioned in the saved notes),
- no tile racks yet: Spirit of Christmas has no approved tile-rack list (open decision with her).
Usage: python3 spirit_build.py <workdir>; then gen2.py <workdir>/spec.json assets/cards/spirit-of-christmas-oct20"""
import json, io, base64, os, sys
from PIL import Image
R = '/home/claude/mahjmatchmaker-data/'; W = sys.argv[1]; os.makedirs(W, exist_ok=True)
SRC = '/tmp/claude-0/-home-claude-mahjmatchmaker-data/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/spirit/m/'
CARDS = [  # her c5-spirit order: (mat name, swipe photo, file slug, Oct 17 mat racks)
 ('Spirit of Christmas', '6.jpg', 'spirit-of-christmas', ['Bird & Bamboo Matcha']),
 ('Vintage Noel', '4.jpg', 'vintage-noel', ['Bird & Bamboo Mauve', 'Bird & Bamboo Basil']),
 ('Merry Mix', '0.jpg', 'merry-mix', ['Bird & Bamboo Cherry Red', 'Bird & Bamboo Light Pink']),
 ('Pretty Little Christmas', '3.jpg', 'pretty-little-christmas', ['Bird & Bamboo Light Blue', 'Bird & Bamboo Forest Green']),
 ('Merry & Striped', '7.jpg', 'merry-striped', ['Bird & Bamboo Brick Red', 'Bird & Bamboo Matcha']),
 ('Tied With A Bow', '12.jpg', 'tied-with-a-bow', ['Bird & Bamboo Light Pink', 'Bird & Bamboo Red']),
 ('Peace Love & Mistletoe', '9.jpg', 'peace-love-mistletoe', ['Bird & Bamboo Evergreen', 'Bird & Bamboo Flamingo']),
 ('Poinsettia & Peace', '5.jpg', 'poinsettia-peace', ['Bird & Bamboo Cherry Red', 'Bird & Bamboo Magenta']),
 ('Nutcracker Noel - Red & Green', '1.jpg', 'nutcracker-noel-red-green', ['Bird & Bamboo Radish', 'Bird & Bamboo Forest Green']),
 ('Nutcracker Noel - Gold', '2.jpg', 'nutcracker-noel-gold', ['Bird & Bamboo Pistachio']),
]
def trim(im):
    g = im.convert('L').point(lambda p: 255 if p < 232 else 0); b = g.getbbox(); return im.crop(b) if b else im
def uri(im):
    im = im.copy(); im.thumbnail((1600, 1600), Image.LANCZOS); b = io.BytesIO(); im.convert('RGB').save(b, 'JPEG', quality=92)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
FLAME = 'data:image/png;base64,' + base64.b64encode(open(R + 'assets/brand/flame-heart-holiday.png', 'rb').read()).decode()
COL = json.load(open(R + 'scripts/albumcard/holiday_title_colors.json')).get('spirit-of-christmas', '#a3192e')
cards, man = [], []
for i, (nm, f, sl, mr) in enumerate(CARDS, 1):
    im = trim(Image.open(SRC + f).convert('RGB'))
    fn = f'{i:02d}-spirit-of-christmas-mahjong-tiles-peace-love-mahjong-{sl}-mat.jpg'
    cards.append({'slug': f'soc{i:02d}', 'title': f'Spirit of Christmas + {nm}', 'col': COL, 'tile_file': 'assets/tiles/holiday/plm-spirit-of-christmas-faces-back.jpg',
                  'racks': [], 'mat_racks': mr, 'file': fn, 'code': '10% OFF  USE CODE : MAHJMATCH', 'mat': uri(im), 'hol': True, 'flame': FLAME})
    man.append({'order': i, 'mat': nm, 'brand': 'Peace Love Mahjong', 'file': fn, 'mat_px': list(im.size), 'mat_racks': mr, 'tile_racks': []})
json.dump({'_note': 'Spirit of Christmas Oct 20', 'cards': cards, 'max_racks': 4, 'tile_brand': 'Peace Love Mahjong'}, open(W + '/spec.json', 'w'))
json.dump({'set': 'Spirit of Christmas', 'cards': man, 'blocked': 'her chat feedback text not on file; tile racks not approved'}, open(W + '/manifest.json', 'w'), indent=1)
print(len(cards))
