"""v108 spec builder (Oct 31): NON-PARTNER brands Tiffany chose 'Bring in now' on the Brands to Bring In page (Oct 31 ~2:20pm,
artifact S3aCFRLs7eqmvjpZGepMJw db picks). Shopify brands from the LIVE store feeds: Bougie Mahjong (whole mat line) + Mahj & Moon
(mats not yet in FYM; the ones already in FYM are unhidden by partneradds108). pa False, no code, plain store links (Mahj & Moon ShopMy
links pending Ops, config/mahj-moon-shopmy-links.json). Holiday by PHOTO (CLAUDE.md: Christmas / Hanukkah / winter snowy only).
Writes config/fym-nonpartner-adds-oct31.json + assets/mats/v108/*.jpg. Usage: python3 spec108.py <feed dir with <store>.<p>.json + img/>"""
import sys, json, os
import numpy as np
from PIL import Image
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
F = sys.argv[1]
def trimcopy(src, dst):  # gate [89]: trim the white margin (mat fills the frame)
    im = Image.open(src).convert('RGB'); a = np.asarray(im).astype(int); nw = ~(a.min(2) > 238)
    ys, xs = np.where(nw)
    if len(xs): im = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    im.save(dst, quality=92)
def feed(s):
    L = []
    for p in (1, 2, 3):
        try: L += json.load(open(f'{F}/{s}.{p}.json'))['products']
        except Exception: pass
    return L
import re
def nm(t):
    t = re.split(r'\s[|–-]\s', t)[0]
    t = re.sub(r'(?i)\b(american\s+)?mahjong\s+(mat|table\s*\w*)\b', '', t)
    return re.sub(r'\s+', ' ', t).strip(' -–|')
HOL = {'buffalo-plaid-snow-day-mahjong-mat', 'chinoiserie-christmas-conservatory-mahjong-mat', 'country-club-christmas-mahjong-mat',
       'peppermint-chinoiserie-christmas-mahjong-mat', 'midnight-woodland-christmas-mahjong-mat', 'pastel-christmas-tree-mahjong-mat'}
H = open(sys.argv[2]).read(); i = H.index('const D=') + 8; D, _ = json.JSONDecoder().raw_decode(H[i:]); M = D['mats']
have_mm = {k.split('/', 1)[1] for k in M if k.startswith('mahjandmoon.com/')} | {(o.get('u') or '').split('/products/')[-1].split('?')[0] for o in M.values() if o.get('bn') == 'Mahj & Moon'}
mats = []
for store, bn, pre, types in (('bougiemahjong.com', 'Bougie Mahjong', 'bougie', None), ('mahjandmoon.com', 'Mahj & Moon', 'mm', ('Mahjong Mats', 'Round Mahjong Mat', 'Scalloped Mahjong Mats'))):
    for p in feed(store):
        h = p['handle']
        if types is None and 'Mat' not in p['product_type']: continue
        if types and p['product_type'] not in types: continue
        if pre == 'mm' and h in have_mm: continue
        if not any(v['available'] for v in p['variants']): continue
        src = f'{F}/img/{pre}__{h}__0.jpg'
        if not os.path.exists(src): continue
        dst = f'assets/mats/v108/{pre}-{h[:80]}.jpg'; trimcopy(src, REPO + dst)
        mats.append(dict(key=f'{store}/{h}', name=nm(p['title']), bn=bn, b=store, u=f'https://{store}/products/{h}', u0=f'https://{store}/products/{h}',
                         dc='', pa=False, img=dst, hol=h in HOL, hid=False, reason='', photo_note='brand image 0: flat render, fills the frame (non-partner add Oct 31)'))
json.dump(dict(_about=__doc__, made='2026-10-31', mats=mats), open(REPO + 'config/fym-nonpartner-adds-oct31.json', 'w'), indent=1, ensure_ascii=False)
from collections import Counter
print(len(mats), 'mats', Counter(m['bn'] for m in mats), sum(m['hol'] for m in mats), 'holiday')
for m in mats: print(' ', m['bn'], '|', m['name'])
