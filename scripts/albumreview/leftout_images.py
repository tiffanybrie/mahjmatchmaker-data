"""Give every left-out mat of an album an 'img' (its FYM photo) so build_review.py can show it.
usage: python3 scripts/albumreview/leftout_images.py <set>   (writes assets/albums/leftout/<set>/*.jpg and updates the leftout json)"""
import json, re, sys, io, os
from PIL import Image
R = '/home/claude/mahjmatchmaker-data/'
sys.path.insert(0, R + 'scripts/albumreview')
from fym_images import latest_index, image_bytes
S = sys.argv[1]
rec = json.load(open(R + f'config/album-records/{S}.json')); lo = rec['leftout']
data = json.load(open(R + lo['file'])); L = data[lo['key']]
_, h = latest_index()
m = re.search(r'const D=(\{.*?\});\s*\n', h, re.S) or re.search(r'const D=(\{.*\})', h)
D = json.loads(m.group(1)) if m else None
mats = D['mats'] if isinstance(D.get('mats'), dict) else {x.get('k') or x.get('id'): x for x in D['mats']}
slug = lambda s: re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
need = {}
for x in L:
    if x.get('img') and os.path.exists(R + x['img']): continue
    mm = mats.get(x.get('fym'))
    if mm and mm.get('f'): need[x['fym']] = mm['f']
B = image_bytes(list(set(need.values())))
os.makedirs(R + f'assets/albums/leftout/{S}', exist_ok=True); n = 0
for x in L:
    f = need.get(x.get('fym'))
    if not f or f not in B or not B[f]: continue
    p = f"assets/albums/leftout/{S}/{slug(x['brand'])}-{slug(x['name'])}.jpg"
    Image.open(io.BytesIO(B[f])).convert('RGB').save(R + p, quality=85); x['img'] = p; n += 1
miss = [x['name'] for x in L if not x.get('img')]
json.dump(data, open(R + lo['file'], 'w'), indent=1, ensure_ascii=False)
print(f'{S}: {n} images written, {len(miss)} without a photo', miss[:10])
