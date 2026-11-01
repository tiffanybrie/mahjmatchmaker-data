"""Mat Gallery sync (gate [90] warning: 274 visible FYM mats with no Mat Gallery row in the v112 test build, mostly the Oct 31
non-partner brand adds + Oct 25-30 partner adds). Drafts one row per missing mat into config/mat-gallery-extra-rows.json
(added '2026-11-01-v112', eye null) and exports its FYM photo at 640px to assets/mats/gallery/<img>.webp, the same way the Oct 26
sync / Oct 27 v101 rows were made. Sections = the mat's FYM colour families in order (holiday mats -> ['holiday'] only, the
holiday rule); gallery-only families (brights / florals / pastel / simple / earthy / teal) are NOT guessed: the gallery builder's
colour pass (build_v5.py + config/mat-accent-colors.json) adds those, and her late calls are re-applied last as always.
Run AFTER the v112 build passed the gates, on that build. Then rebuild the staged gallery (site/livepatch/matgallery/build_v5.py),
gate [13]/[90] again, paste. Usage: python3 gallery_rows112.py <build_dir> [--write]  (without --write: dry run, prints counts)"""
import sys, os, io, json, re, struct, unicodedata, urllib.parse
from PIL import Image
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; WRITE = '--write' in sys.argv
h = open(B + '/index.html').read(); i = h.index('const D=') + 8; D, _ = json.JSONDecoder().raw_decode(h[i:]); M = D['mats']
g = open(REPO + 'site/livepatch/matgallery/matgallery-v5.html').read()
nz = lambda x: re.sub(r'[^a-z0-9]', '', ''.join(c for c in unicodedata.normalize('NFD', str(x or '')) if not unicodedata.combining(c)).lower())
def nu(u):
    u = str(u or '')
    if '/discount/' in u and 'redirect=' in u:
        u = re.sub(r'^(https?://[^/]+).*$', r'\1', u) + urllib.parse.unquote(u.split('redirect=', 1)[1].split('&')[0])
    return re.sub(r'^https?://(www\.)?', '', u.split('?')[0].split('#')[0]).rstrip('/').replace('/products/', '/')
G = json.loads(re.search(r'<script type="application/json">(.*?)</script>', g, re.S).group(1).replace('<\\/', '</'))
GU = {nu(r[3]) for r in G}; GN = {nz(r[1]) + '|' + nz(r[2]) for r in G}; GI = {r[0] for r in G}
X = json.load(open(REPO + 'config/mat-gallery-extra-rows.json'))
XK = {a['key'] for a in X['rows']}; XU = {nu(a.get('url')) for a in X['rows']}
imgs = {}
for fn in os.listdir(B + '/mc'):
    if fn.endswith('.webp'):
        raw = open(B + '/mc/' + fn, 'rb').read(); n = struct.unpack('<I', raw[-4:])[0]
        for f, (a, l) in json.loads(raw[-4 - n:-4]).items(): imgs[f] = (fn, a, l)
CODE = {}
for o in M.values():
    if o.get('dc') and o.get('bn'): CODE.setdefault(o['bn'], re.sub(r'^https?://(www\.)?mahjmatchmaker\.com', '', o['dc']))
rows = []
for k, m in M.items():
    if m.get('hid') or '#side-b' in k or k in XK: continue
    us = {nu(m.get('u0')), nu(m.get('u')), nu(k)}
    if us & XU: continue
    if us & GU or (nz(m['n']) + '|' + nz(m.get('bn'))) in GN: continue    # already a staged row (gate [90] matching)
    img = nz(m.get('bn'))[:24] + '--' + re.sub(r'[^a-z0-9]+', '-', unicodedata.normalize('NFD', m['n']).encode('ascii', 'ignore').decode().lower()).strip('-')[:60]
    secs = ['holiday'] if m.get('hol') else [c for c in (m.get('mf') or [])][:4]
    if m.get('ayr') and 'holiday' not in secs: secs = secs + ['holiday']
    rows.append({'img': img, 'key': k, 'name': m['n'].replace(' (retired)', ''), 'brand': m.get('bn'), 'url': m.get('u'), 'code': CODE.get(m.get('bn'), '') if m.get('pa') else '',
                 'secs': secs, 'eye': None, 'added': '2026-11-01-v112', 'note': f"Nov 1 v112 gallery sync draft: photo = FYM {m.get('f')} at 640px; sections = FYM colour families (gallery colour pass adds the rest)."})
print('rows to add', len(rows))
if WRITE:
    for r in rows:
        f = M[r['key']].get('f'); src = imgs.get(f)
        if not src: r['note'] += ' NO PHOTO FOUND'; continue
        raw = open(B + '/mc/' + src[0], 'rb').read()[src[1]:src[1] + src[2]]
        im = Image.open(io.BytesIO(raw)).convert('RGB'); im.thumbnail((640, 640)); im.save(REPO + f"assets/mats/gallery/{r['img']}.webp", 'WEBP', quality=84)
    X['rows'] += rows; json.dump(X, open(REPO + 'config/mat-gallery-extra-rows.json', 'w'), indent=1, ensure_ascii=False)
    print('written', len(rows))
