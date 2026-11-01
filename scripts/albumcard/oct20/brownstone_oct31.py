"""Brownstone Bloom album, Oct 31 rebuild (Tiffany Oct 29 8:04am HQ answer: remove B&B Wine; swap the Anders Ruff tortoise,
whose photo made the mock-up messy, for the best-looking tortoise; order is good).
- Tile racks = config/tile-racks-picks.json final_lists brownstone-bloom (Middle & Main Hawksbill Heritage Tortoise +
  Bam Bird Boutique Olive). Brownstone Bloom mat's mat racks = config/mat-racks-picks.json (M&M Hawksbill + PLM Burl).
  Every other card keeps its Oct 24 mat racks (or its registry entry when it has one).
- Order = the Oct 24 order (her order page review/order was never re-saved; "order is good").
- Photos: the Oct 24 sources were gone again, so each mat was re-sourced and matched to its approved Oct 24 card by image
  correlation in the card's un-overlaid window (same photo + same framing): brand Shopify image, else the repo gallery
  photo, else the round-2 candidate photo. Crops under 750px were EDSR x4 super-resolved (opencv dnn_superres).
  Pre-framed crops live in <srcdir>/NN.png (NN = card order); report.json says where each came from.
Usage: python3 brownstone_oct31.py <workdir> <srcdir>; then gen2.py <workdir>/spec.json assets/cards/brownstone-bloom-oct31"""
import json, io, base64, os, sys
from PIL import Image
R = '/home/claude/mahjmatchmaker-data/'; W = sys.argv[1]; SD = sys.argv[2]; os.makedirs(W, exist_ok=True)
OLD = json.load(open(R + 'assets/cards/brownstone-bloom-oct24/manifest.json'))['cards']
REP = json.load(open(SD + '/report.json'))
TRACKS = json.load(open(R + 'config/tile-racks-picks.json'))['final_lists']['brownstone-bloom']
REG = {k: v for k, v in json.load(open(R + 'config/mat-racks-picks.json')).items() if isinstance(v, dict)}
assert 'Bird & Bamboo Wine' not in TRACKS and 'Anders Ruff Tortoise' not in TRACKS, TRACKS
def uri(im, maxs=1600):
    im = im.copy(); im.thumbnail((maxs, maxs), Image.LANCZOS); b = io.BytesIO(); im.convert('RGB').save(b, 'JPEG', quality=92)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
SHORT = {'Midnight Wildflowers with Camel Fringe': 'Midnight Wildflowers'}  # card title only (the full name ran off the card at the 30px minimum)
TILE = 'assets/tiles/anders_ruff_brownstone_bloom_tilebox_CARD-ONLY-edited.jpg'; COL = '#7b2d3b'
cards, man = [], []
for c in OLD:
    n = c['order']; rk = c.get('mat_reg')
    mr = REG[rk]['racks'] if rk and rk in REG else c['mat_racks']
    im = Image.open(f'{SD}/{n:02d}.png').convert('RGB'); r = REP[str(n)]
    cards.append({'slug': f'bb{n:02d}', 'title': f'Brownstone Bloom + {SHORT.get(c["mat"], c["mat"])}', 'col': COL, 'tile_file': TILE, 'racks': TRACKS,
                  'mat_racks': mr, 'file': c['file'], 'code': c['code'], 'mat': uri(im)})
    man.append(dict(c, racks=TRACKS, mat_racks=mr, crop_px=im.width, photo=r.get('src'), photo_corr=r.get('corr'), photo_src_crop_px=r.get('crop_w')))
json.dump({'_note': 'Brownstone Bloom album Oct 31', 'cards': cards, 'max_racks': 4, 'tile_brand': 'Anders Ruff'}, open(W + '/spec.json', 'w'))
json.dump({'set': 'Brownstone Bloom', 'cards': man, 'tile': TILE, 'title_color': COL, 'racks': TRACKS,
           'note': 'Oct 31: Tiffany Oct 29 rack swap (M&M Hawksbill tortoise, no B&B Wine); Oct 24 order; 40 cards'},
          open(W + '/manifest.json', 'w'), indent=1)
print(len(cards), 'cards'); [print(c['order'], c['mat'], c['crop_px'], c['mat_racks']) for c in man]
