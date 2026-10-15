"""December 1994 holiday cards: the 26 YES mats (db xmastiles2, 31 yes) not yet live (5 live:
Evergreen & Tartan, Tartan Tidings, Tartan Toile Noel, Polo Club, Festive Plaid).
Writes data_d94.json (data5 + the new december-1994 rows) for scripts/albumcard/gen_hol.py.
Racks: tile racks = B&B Radish + Almond (the same 2 used on all 5 live December 1994 cards, Claude's defaults
she OK'd for the holiday launch); third (mat) pick = nearest B&B colour to the mat's main colour, as before."""
import json, io, base64, os
import numpy as np
from PIL import Image
from skimage.color import rgb2lab, deltaE_ciede2000
S = '/tmp/claude-0/-home-claude-mahjmatchmaker-data/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/'
R = '/home/claude/mahjmatchmaker-data/'
D = json.load(open(S + 'holracks/data5.json'))
X = {i['id']: i for i in json.load(open('/tmp/sun/xmas2.json'))['items']}
ys = [x.split('__', 1)[1] for x in json.load(open(S + 'db/xmastiles2_yes.json'))]
X_order = json.load(open('/tmp/sun/xmas2.json'))['order']
LIVE = {'evergreen-tartan-mahjong-mat', 'tartan-tidings-mahjong-mat', 'tartan-toile-noel-mahjong-mat', 'polo-club', 'festive-plaid'}
BB = {x['name']: x['hex'] for x in json.load(open(R + 'work/bbracks.json'))}
BBL = {k: rgb2lab(np.array([[[int(v[1:3], 16), int(v[3:5], 16), int(v[5:7], 16)]]]) / 255.)[0, 0] for k, v in BB.items() if 'Metallic' not in k and k not in ('Radish', 'Almond', 'Clear')}
def uri(im):
    im = im.copy(); im.thumbnail((1600, 1600)); b = io.BytesIO(); im.convert('RGB').save(b, 'JPEG', quality=90)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
def flat(im):
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA'); im = im.crop(im.getbbox()); bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[3]); return bg
    return im.convert('RGB')
def trimw(im):
    g = im.convert('L').point(lambda p: 255 if p < 235 else 0); return im.crop(g.getbbox())
CUT = '/tmp/sun/alb_cut/'
SRC = {  # prefixed studio ids -> best isolated photo we have
 'c-cognac-mat': '/tmp/mb/cut/www.ohmymahjong.com__cognac-mat.png',
 'c-hollivia': '/tmp/mb/cut/www.viroramahjong.com__hollivia.png',
 'c-origami-leather-mat': S + 'bambird_brown_leather.jpg',  # brown: the colour she swiped (studio photo); the cut-out was the multi-colour stack
 'c-rattan-premium-mahjong-mat': CUT + 'sundayma-rattan-premium-mahjong-mat.png',
 'c-the-study-mat': CUT + 'mahjsqua-the-study-mat.png',
 's-golden-gingham-sunday-mahjong': CUT + 'sundayma-golden-gingham-premium-mahjong-mat.png',
 's-highland-heritage-plaid-mahjong-by-si': CUT + 'mahjongb-mahjong-by-si-highland-house-mahjong-mat.png',
 's-tartan-tweed-let-s-be-besties': '/tmp/sun/alb_src/letsbebe-tartan-tweed-mahjong-mat_0.jpg',
 's-the-hunt-club-mahjong-by-si': CUT + 'mahjongb-mahjong-by-si-the-hunt-club-mahjong-mat.png',
 's-vintage-oxblood-leather-mahjong-by-si': CUT + 'mahjongb-mahjong-mat-vintage-oxblood-leather-sclp.png',
 's-vegan-leather-sunday-mahjong': S + 'bvl_full.jpg',
 'britt-crimson-harvest': S + 'dec_src/britt-crimson-harvest.png',
}
RENAME = {'britt-crimson-harvest': 'crimson-harvest-neoprene-mahjong-mat'}  # gen_hol SKIPs the old id (left out of the generic launch as non-holiday); she said yes to it for December 1994
others = {}
for g in D['G']:
    for r in g['rows']: others.setdefault(r['m'], r)
def third(im):
    im = flat(im); im.thumbnail((200, 200)); a = np.asarray(im).reshape(-1, 3) / 255.
    a = a[(a.max(1) < .97)]  # drop white background
    lab = rgb2lab(a[None])[0]
    from scipy.cluster.vq import kmeans2
    np.random.seed(0); c, l = kmeans2(lab, 5, minit='++', seed=0)
    cnt = np.bincount(l, minlength=5); best = None
    for k in np.argsort(-cnt):
        ch = np.hypot(c[k, 1], c[k, 2])
        if ch > 12 or best is None: best = c[k]
        if ch > 12: break
    return min(BBL, key=lambda n: deltaE_ciede2000(best, BBL[n]))
grp = next(g for g in D['G'] if g['t'] == 'december-1994')
order = sorted(ys, key=lambda y: X_order.get(y, 999) if isinstance(X_order, dict) else 0)
new = []; picks = {}
for y in ys:
    if y in LIVE: continue
    lab = X[y]['label']; nm, br = [s.strip() for s in lab.split('·')]
    m = RENAME.get(y, y)
    if y in SRC:
        p = SRC[y]; im = Image.open(p)
        if y == 's-vegan-leather-sunday-mahjong': im = im.convert('RGB').crop((130, 0, 3120, 3820))
        elif p.endswith('.jpg'): im = trimw(im.convert('RGB'))
        else: im = flat(im)
        D['BIG'][m] = uri(im)
        row = {'m': m, 'n': nm, 'b': br, 'img': X[y]['img']}
    elif y in others:
        o = others[y]; row = {'m': y, 'n': o['n'], 'b': o['b'], 'img': o.get('img', X[y]['img'])}
    else:
        row = {'m': y, 'n': nm, 'b': br, 'img': X[y]['img']}
    t = third(Image.open(S + 'dec_src/' + y + '.png'))
    row['def'] = ['bb:Radish', 'bb:Almond', 'bb:' + t]; row['star'] = False
    new.append(row); picks[y] = t
grp['rows'] = grp['rows'] + new
json.dump(D, open(S + 'dec1994_v1/data_d94.json', 'w'))
json.dump({'only': [f"december-1994:{r['m']}" for r in new], 'third_pick': picks}, open(S + 'dec1994_v1/only.json', 'w'), indent=1)
for r in new: print(r['m'], '|', r['n'], '|', r['b'], '|', r['def'][2])
print(len(new))
