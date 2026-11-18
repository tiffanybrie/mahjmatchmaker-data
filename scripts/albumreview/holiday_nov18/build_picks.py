"""Holiday albums pick sheet (Tiffany Nov 18 7:47am).

Builds one review page: Grinch Green / Nivalee Blue / Apres Ski / Dear Santa /
Spirit of Christmas candidate tabs (mat with the album's tiles inset) plus an
Etsy tab (each Etsy-sold holiday mat with album chips).

usage: python3 build_picks.py <D.json from live FYM> <fym build dir with m/> <out.html>
"""
import base64, io, json, sys, os
from PIL import Image

DJ, BUILD, OUT = sys.argv[1:4]
REPO = os.path.dirname(os.path.abspath(__file__)) + '/../../..'
D = json.load(open(DJ))
SNAP = json.load(open(f'{REPO}/config/partner-products-snapshot.json'))
NEW_DIR = os.environ.get('NEWIMG', '')  # downloaded brand photos for items not in FYM yet


def vis(m):
    return (m.get('hol') or m.get('wfh')) and not (m.get('hid') or m.get('parked') or m.get('ahid'))


def find(spec):
    n, b = spec.split('|')
    hits = [k for k, m in D['mats'].items() if m['n'] == n and m['bn'] == b and vis(m)]
    if len(hits) != 1:
        raise SystemExit(f'resolve {spec}: {hits}')
    return hits[0]


def uri(path, w):
    im = Image.open(path).convert('RGB')
    im.thumbnail((w, w))
    bio = io.BytesIO(); im.save(bio, 'JPEG', quality=74)
    return 'data:image/jpeg;base64,' + base64.b64encode(bio.getvalue()).decode()


def matimg(k, w=460):
    return uri(f"{BUILD}/{D['mats'][k]['f']}", w)


# items not in FYM yet (partner store photos, cleanest listing shot)
NEW = {
    'maison:alpine': ('The Alpine Mat', 'Maison Mahj', 'mm/the-alpine-mat-2.jpg', 'New to the app (Maison ski collection)'),
    'maison:snowfall': ('The Snowfall Mat', 'Maison Mahj', 'mm/the-snowfall-mat-3.jpg', 'New Nov 14 release, not in the app yet'),
    'maison:evergreen': ('The Evergreen Mat', 'Maison Mahj', 'mm/the-evergreen-mat-1.jpg', 'New Nov 14 release, not in the app yet'),
    'maison:winter-garland': ('The Winter Garland Mat', 'Maison Mahj', 'mm/the-winter-garland-mat-1.jpg', 'New Nov 14 release, not in the app yet'),
    'soiree:holiday-chintz': ('Holiday Chintz', 'Soirée All Day', 'new/soireeallday-holiday-chintz-mahjong-mat.jpg', 'Not in the app yet'),
}


# in the website FYM (hidden only in the slim artifact copy, ahid=1): photo from the brand store
LOCAL = {
    'lbb:apres-teal': ('letsbebesties.com/apres-skiing-in-teal-mahjong-mat', 'lbb/apres-skiing-in-teal-mahjong-mat.jpg'),
    'lbb:apres-teal-skiers': ('letsbebesties.com/apres-skiing-in-teal-with-skiers-mahjong-mat', 'lbb/apres-skiing-in-teal-with-skiers-mahjong-mat.jpg'),
    'lbb:apres-green': ('letsbebesties.com/green-apres-skiing-in-teal-with-skiers-mahjong-mat', 'lbb/green-apres-skiing-in-teal-with-skiers-mahjong-mat.jpg'),
    'lbb:alpine-snowflakes': ('letsbebesties.com/alpine-snowflakes-neoprene-mahjong-mat', 'lbb/alpine-snowflakes-neoprene-mahjong-mat.jpg'),
    'lbb:fair-isle': ('letsbebesties.com/fair-isle-pink-snowflakes-mahjong-mat', 'lbb/fair-isle-pink-snowflakes-mahjong-mat.jpg'),
    'lbb:winter-wonderland': ('letsbebesties.com/winter-wonderland-leatherette', 'lbb/winter-wonderland-leatherette.jpg'),
}


def cand(x):
    if x in LOCAL:
        k, p = LOCAL[x]; m = D['mats'][k]
        return {'k': k, 'n': m['n'], 'b': m['bn'], 'img': uri(os.path.join(NEW_DIR, p), 460)}
    if x in NEW:
        n, b, p, note = NEW[x]
        return {'k': x, 'n': n, 'b': b, 'img': uri(os.path.join(NEW_DIR, p), 460), 'note': note}
    k = find(x)
    m = D['mats'][k]
    return {'k': k, 'n': m['n'], 'b': m['bn'], 'img': matimg(k)}


TILES = {
    'holly-jolly-green': 'assets/tiles/holiday/holly-jolly-green.jpg',
    'nivalee-blue': 'assets/tiles/holiday/nivalee-blue.jpg',
    'cmc-apres-ski': 'assets/tiles/holiday/cmc-apres-ski-fill.jpg',
    'dear-santa': 'assets/tiles/holiday/dear-santa-fill.jpg',
    'spirit-of-christmas': 'assets/tiles/holiday/plm-spirit-of-christmas-faces-back-fill.jpg',
}
TITLE = {
    'holly-jolly-green': ("Grinch Green", "Bam! Let's Mahjong Holly Jolly"),
    'nivalee-blue': ('Nivalee Glacier Blue', 'Virora Mahjong'),
    'cmc-apres-ski': ('Après Ski Club', 'Charleston Mahjong Club'),
    'dear-santa': ('Dear Santa', 'Anders Ruff'),
    'spirit-of-christmas': ('Spirit of Christmas', 'Peace Love Mahjong'),
}
CANDS = json.load(open(os.path.join(os.path.dirname(__file__), 'candidates.json')))

sets = {s['slug']: s for s in D['sets']}
albums = []
for sl in ['holly-jolly-green', 'nivalee-blue', 'cmc-apres-ski', 'dear-santa', 'spirit-of-christmas']:
    cur = [{'n': D['mats'][k]['n'], 'b': D['mats'][k]['bn'], 'img': matimg(k, 180)}
           for k, _ in sets[sl]['m'] if k in D['mats']]
    cur_keys = {k for k, _ in sets[sl]['m']}
    cs = []
    for x in CANDS[sl]:
        c = cand(x)
        if c['k'] in cur_keys:
            raise SystemExit(f'{sl}: {x} already in album')
        cs.append(c)
    albums.append({'id': sl, 'name': TITLE[sl][0], 'maker': TITLE[sl][1],
                   'tiles': uri(f'{REPO}/{TILES[sl]}', 520), 'cur': cur, 'cands': cs,
                   'live': len(cur)})

etsy = []
for x, sug in CANDS['etsy']:
    k = find(x); m = D['mats'][k]
    etsy.append({'k': k, 'n': m['n'], 'b': m['bn'], 'img': matimg(k, 380), 'sug': sug})

CHIPS = CANDS['chips']
data = {'albums': albums, 'etsy': etsy, 'chips': CHIPS}
tpl = open(os.path.join(os.path.dirname(__file__), 'page.html')).read()
open(OUT, 'w').write(tpl.replace('/*DATA*/null', json.dumps(data)))
print('albums', [(a['id'], a['live'], len(a['cands'])) for a in albums], 'etsy', len(etsy),
      'bytes', os.path.getsize(OUT))
