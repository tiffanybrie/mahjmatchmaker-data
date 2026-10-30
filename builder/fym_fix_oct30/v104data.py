"""FYM v104 data fixes (Oct 30). Usage: python3 builder/fym_fix_oct30/v104data.py <build_dir>
1. Tile photos (Tiffany Oct 30 2:51am: no 'Photo coming soon' without checking every brand photo): config/fym-tile-photo-fills-oct30.json
   -> T[key].full = t104/<slug>.jpg (copied from assets/fym-photos-oct30/tiles), T[key].pile = NEW inline thumb id (p104*; old chunk
   ids left unused so no hardlinked b*.js chunk is touched), 'soon' dropped, src = the new asset.
2. Wren Mats Simply: dead link -> live page.
3. Anders Ruff Brownstone Bloom rack picks (config/mat-racks-picks.json, commit b91efc5a, Tiffany Oct 29 HQ brownstone-shortlist):
   D.lm = registry; every pairing with that mat = her mat picks first, AR Tortoise dropped (swapped for M&M Hawksbill); locks follow."""
import sys, os, io, json, base64, hashlib, shutil
from PIL import Image
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
sys.path.insert(0, REPO + 'builder/fym_fix_oct22')
from rack_picks import registry_picks
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
T, M = D['tiles'], D['mats']
F = json.load(open(REPO + 'config/fym-tile-photo-fills-oct30.json'))
os.makedirs(B + '/t104', exist_ok=True); IMG = {}; n = 0
for e in F['tiles']:
    t = T.get(e['key'])
    if not t or e.get('kind') == 'none': continue
    slug = os.path.basename(e['full']).rsplit('.', 1)[0]; fn = f't104/{slug}.jpg'
    shutil.copy(REPO + e['full'], f'{B}/{fn}')
    im = Image.open(REPO + e['thumb']).convert('RGB'); b = io.BytesIO(); im.save(b, 'JPEG', quality=84)
    pk = 'p104' + hashlib.md5(e['key'].encode()).hexdigest()[:10]
    IMG[pk] = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
    t['full'] = fn; t['pile'] = pk; t.pop('soon', None); t['src'] = e['full']; n += 1
w = T.get('www.wrenmats.com/opgv5o7mztp8eu7krduztz8x70u1ms')
if w: w['u'] = 'https://www.wrenmats.com/shop-tiles/p/opgv5o7mztp8eu7krduztz8x70u1ms'
# Brownstone
rep = {'unresolved_racks': [], 'unresolved_mats': []}
REG = registry_picks(D, rep)
BS = 'shop.andersruff.com/brownstone-bloom-mahjong-mat'; ART = 'shop.andersruff.com/tortoise-acrylic-rack-set-straight-pushers'
want = REG[BS]; D.setdefault('lm', {})[BS] = want
LP = REPO + 'builder/fym_flags/locks.json'; LK = json.load(open(LP)); ch = []
for s in D['sets']:
    for e in s.get('m', []):
        if e[0] != BS: continue
        cur = e[1] if len(e) > 1 else []
        new = list(want) + [r for r in cur if r not in want and r != ART]
        if len(e) > 1: e[1] = new
        else: e.append(new)
        ch.append(s['slug'])
        ls = (LK.get('sets') or {}).get(s['slug'])
        if ls and isinstance(ls.get('m'), list):
            for le in ls['m']:
                if le[0] == BS:
                    if len(le) > 1: le[1] = new
                    else: le.append(new)
if isinstance(LK.get('_changes'), list) and not any('v104 Brownstone' in str(c) for c in LK['_changes']):
    LK['_changes'].append('2026-10-30 v104 Brownstone Bloom mat racks: M&M Hawksbill Heritage Tortoise replaces AR Tortoise (Tiffany Oct 29, config/mat-racks-picks.json)')
json.dump(LK, open(LP, 'w'), indent=1, ensure_ascii=False)
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMG, separators=(',', ':')) + ');</script>'
a = '<script src="b24v1.js"></script>'; assert h.count(a) == 1; h = h.replace(a, a + inl, 1)
open(P, 'w').write(h)
print('tiles', n, 'brownstone pairings', ch, 'lm', want)
