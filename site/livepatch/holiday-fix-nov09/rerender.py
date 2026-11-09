"""Re-render live holiday/album cards from their LIVE figure (same title, same racks as the caption, same tile set),
with a sharp mat photo and the locked filled tile crops. Usage: python3 rerender.py jobs.json outdir"""
import json, sys, os, re, io, base64, subprocess
R = '/home/claude/mahjmatchmaker-data/'
sys.path.insert(0, R + 'site/livepatch/missed-album-picks-nov07'); sys.path.insert(0, R + 'scripts/albumcard')
import build as B
from PIL import Image
PCT = set(json.load(open(R + 'config/code-truth.json'))['pct'])
def band(brand): return '10% OFF  USE CODE : MAHJMATCH' if brand in PCT else 'SAVE WITH CODE : MAHJMATCH'
jobs = json.load(open(sys.argv[1])); out = sys.argv[2]
cards = []
for j in jobs:
    im = B.flat(Image.open(j['photo']))
    if j.get('crop'): im = im.crop(tuple(j['crop']))
    else:
        im = B.trim(im)
        if B.curled(im): im = im.rotate(-90, expand=True)
        im = B.crop_hol(im) if j['hol'] else B.crop_year(im)
    t = j['tile']
    tile, mat = j['h3'].split(' + ', 1)
    col = B.COLS.get(t) or (B.CC.get(t) or {}).get('col') or j.get('col') or '#1f3a6b'
    c = {'slug': j['file'][:-4], 'set': t, 'title': f"{tile} + {B.CARDTITLE.get(mat, mat)}", 'col': col, 'tile_file': j.get('tile_file') or B.tile_file(t),
         'racks': j['tile_racks'], 'mat_racks': j['mat_racks'], 'file': j['file'], 'code': j.get('code') or band(j['brand']), 'mat': B.uri(im), 'tile_brand': j['tile_brand']}
    if j['hol']: c.update(hol=True, flame=B.FLAME)
    cards.append(c)
spec = {'_note': 'holiday/album fix Nov 9 (blur + tile fill)', 'cards': cards, 'max_racks': 4, 'navy': 'assets/brand/card_navy_logo_v3.png', 'true_len': True}
sp = '/tmp/rerender_spec.json'; json.dump(spec, open(sp, 'w'))
r = subprocess.run(['python3', R + 'scripts/albumcard/gen2.py', sp, out])
sys.exit(r.returncode)
