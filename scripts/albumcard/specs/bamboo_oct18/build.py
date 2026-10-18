"""Oct 18: re-render album cards whose Mahj & Moon mat photo had a bamboo background, using the cut-out mats
in assets/mats/clean/bamboo-cut/. Osler (4, live): tile racks = config/tile-racks-picks.json final list; mat racks =
the B&B picks printed on the live cards. Petalee (4, not live): from scratchpad/petbuild/spec.json, mat swapped only.
Usage: python3 build.py <workdir>; then gen2.py <workdir>/osler.json and <workdir>/petalee.json"""
import json, io, base64, os, sys
from PIL import Image
R = '/home/claude/mahjmatchmaker-data/'
S = '/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/'
W = sys.argv[1]; os.makedirs(W, exist_ok=True)
CUT = R + 'assets/mats/clean/bamboo-cut/mahj-and-moon-%s.jpg'
def uri(p):
    im = Image.open(p).convert('RGB'); b = io.BytesIO(); im.save(b, 'JPEG', quality=94)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
F = json.load(open(R + 'config/tile-racks-picks.json'))['final_lists']
OS = [('blue-floral-bird', 'Blue Floral Bird', 'blue-floral-bird-american', ['Bird & Bamboo Powder Blue', 'Bird & Bamboo Shell Pink']),
      ('blue-heritage-toile', 'Blue Heritage Toile', 'blue-heritage-toile', ['Bird & Bamboo Dark Navy', 'Bird & Bamboo Powder Blue']),
      ('blue-koi-chinoiserie', 'Blue Koi Chinoiserie', 'blue-koi-chinoiserie', ['Bird & Bamboo Cornflower Blue', 'Bird & Bamboo Persimmon']),
      ('equestrian', 'Equestrian', 'equestrian', ['Bird & Bamboo Powder Blue', 'Bird & Bamboo Cherry Red'])]
osler = {'max_racks': 4, 'cards': []}
for slug, name, cut, mr in OS:
    osler['cards'].append({'slug': 'osler-' + slug, 'title': f'Osler + {name}', 'col': '#456fbe', 'tile_file': 'assets/tiles/album/osler.jpg',
        'tilefit': 'cover', 'racks': F['osler'], 'mat_racks': mr, 'mat': uri(CUT % cut), 'code': '10% OFF  USE CODE : MAHJMATCH',
        'file': f'osler-mahjong-tiles-mahj-and-moon-{slug}-mat.jpg'})
json.dump(osler, open(W + '/osler.json', 'w'))
P = json.load(open(S + 'petbuild/spec.json'))
CUTP = {'seashell-american': 'seashell-american', 'blue-pastel-palm-beach': 'blue-pastel-palm-beach',
        'pastel-tie-dye-american': 'pastel-tie-dye-american', 'pastel-palm-beach': 'pastel-palm-beach'}
pet = {k: v for k, v in P.items() if k != 'cards'}; pet['cards'] = []
for c in P['cards']:
    if 'mahj-and-moon' not in c['file']: continue
    key = c['file'].split('mahj-and-moon-')[1].rsplit('-mat', 1)[0]
    c = dict(c); c['mat'] = uri(CUT % CUTP[key]); pet['cards'].append(c)
json.dump(pet, open(W + '/petalee.json', 'w'))
print(len(osler['cards']), len(pet['cards']))
