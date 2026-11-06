"""Sunday Sets: NEW mats only (added to Find Your Mat-ch after her Oct 29 swipe), one short phone-first review page.
Every mat is shown WITH the set's tiles in one view (match-card style: mat full, tiles inset bottom-right, tap to zoom).
Full mat names + brands. Hearts / X are kept on her phone (localStorage) and 'Copy my picks' gives one line to paste in chat
(same pattern as the Juniper faces page). Images are relative files under images/.
Usage: python3 build_page.py <outdir>"""
import json, re, os, sys, html
from PIL import Image
R = '/home/claude/mahjmatchmaker-data/'
OUT = sys.argv[1]; os.makedirs(OUT + '/images', exist_ok=True)
M = json.load(open('/dev/shm/sun/mats.json'))
CC = json.load(open(R + 'config/colorcards.json'))['sets']
SUN = {'gg': 'sundaymahjong.com/green-gingham-premium-mahjong-mat', 'bg': 'sundaymahjong.com/blue-gingham-premium-mahjong-mat',
       'br': 'sundaymahjong.com/rattan-premium-mahjong-mat-blue', 'ruby': 'sundaymahjong.com/vegan-leather-premium-mahjong-mat?v=ruby',
       'forrest': 'sundaymahjong.com/vegan-leather-premium-mahjong-mat?v=forrest'}
PICKS = {  # by-eye picks from the colour-ranked new-catalog pool (scripts: newmats.py score.py, pick_new.py), Sunday's own new mats first
    'nature-walk': [SUN['ruby'], SUN['forrest'], SUN['gg'], 'www.yolomahjong.com/journey-to-the-west-collection-mat-31-5-shipped-rolled',
                    'www.etsy.com/listing/4581591001/mahjong-mat-non-slip-tabletop-mat-home', 'letsbebesties.com/harvest-leaves-neoprene-mahjong-mat',
                    'faitamainstudio.com/texas-mon-amour-mat-chocolate-blue', 'bougiemahjong.com/palm-garden-tropical-mahjong-mat'],
    'sunday-blues': [SUN['bg'], SUN['br'], 'bougiemahjong.com/cobalt-garden-mahjong-mat', 'bougiemahjong.com/imperial-koi-pond-mahjong-mat',
                     'www.yolomahjong.com/crane-moon-mahjong-mat-floral-chinese-mahjong-table-mat-for-mahjong-set-31-5-x-31-5-inch',
                     'www.etsy.com/listing/4544761281/mahjong-mat-non-slip-tabletop-mat-home', 'letsbebesties.com/slate-steel-mahjong-mat'],
    'plum-panda': [SUN['ruby'], SUN['forrest'], 'letsbebesties.com/amethyst-garden-mahjong-mat', 'www.etsy.com/listing/4544761281/mahjong-mat-non-slip-tabletop-mat-home',
                   'nolijune.com/soiree-at-sues', 'www.etsy.com/listing/4568416056/f-te-peacock', 'letsbebesties.com/cranberry-tapestry-neoprene-mahjong-mat'],
    'hummingbird': [SUN['gg'], SUN['bg'], SUN['br'], SUN['ruby'], SUN['forrest'], 'www.etsy.com/listing/4574925306/mahjong-mat-non-slip-tabletop-mat-home',
                    'www.etsy.com/listing/4581591001/mahjong-mat-non-slip-tabletop-mat-home', 'bougiemahjong.com/cobalt-garden-mahjong-mat',
                    'www.yolomahjong.com/crane-moon-mahjong-mat-floral-chinese-mahjong-table-mat-for-mahjong-set-31-5-x-31-5-inch']}
WHY = {SUN['ruby']: "Sunday's own: deep red vegan leather", SUN['forrest']: "Sunday's own: forest green vegan leather",
       SUN['gg']: "Sunday's own, new colourway", SUN['bg']: "Sunday's own, new colourway", SUN['br']: "Sunday's own, new colourway"}
def slug(k): return re.sub(r'[^a-z0-9]+', '-', k.lower()).strip('-')[-70:]
def save(src, dst, mx):
    im = Image.open(src).convert('RGB'); im.thumbnail((mx, mx)); im.save(dst, 'JPEG', quality=86, optimize=True)
files = ['index.html']
sets = []
for sid, keys in PICKS.items():
    c = CC[sid]; tf = f'images/tiles-{sid}.jpg'; save(R + c['tile'], OUT + '/' + tf, 700); files.append(tf)
    mats = []
    for k in keys:
        f = f'images/mat-{slug(k)}.jpg'
        if not os.path.exists(OUT + '/' + f): save('/dev/shm/sun/newimg/' + re.sub(r'[^a-z0-9]+', '-', k.lower()).strip('-')[-80:] + '.jpg', OUT + '/' + f, 1100); files.append(f)
        m = M[k]
        mats.append({'id': f'{sid}__{slug(k)}', 'key': k, 'name': m['n'], 'brand': m['bn'], 'img': f, 'added': m.get('add', '').split('-')[0],
                     'why': WHY.get(k, ''), 'sale': not m.get('pa', True) and False})
    sets.append({'id': sid, 'name': c['name'], 'col': c['col'], 'sub': c['sub'], 'tile': tf, 'mats': mats})
data = json.dumps({'sets': sets}, ensure_ascii=False)
page = open('/dev/shm/sun/page_tpl.html').read().replace('__DATA__', data)
open(OUT + '/index.html', 'w').write(page)
json.dump(files, open(OUT + '/files.json', 'w'), indent=1)
print(sum(len(s['mats']) for s in sets), 'mats;', len(files), 'files')
