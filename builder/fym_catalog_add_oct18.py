"""Oct 18 FYM catalog audit fill (project doc 72, item 4).
Shop-vs-app compare (doc 65 method, scratchpad fym_audit_oct18/compare.py) found these real gaps
after the catalog rules (no accessories, seconds, singles, sample/tile packs, rummy, riichi/Chinese,
travel/mini, 'coming soon', umbrella-hole mats per the Oct 16 by-eye DROP list):
  tiles: Sunday Blues (Sunday), Pop Diva Mega + Lucky Charms Mega (Bespoke), Classic Mahjong Tile Set
         (Bam Bird Boutique), I Love Mahj (Hip Hip), Amber Jade (Mahjong Studios), and the Yellow Mountain
         Imports American designs not yet in the app (one row per design, available listings only,
         tiles-only listing preferred over the full set).
  mats:  Ditsy Christmas Maraschino (Tigre de Tartan).
  fix:   Yellow Mountain 'The' -> 'The Classic' (name was clipped by the Oct 16 cleaner).
Catalog sets carry cat=True, m=[] (no Tiffany matches) and no color tag (tags only come from Tiffany, doc 50).
Usage: python3 fym_catalog_add_oct18.py <index.html> <feeds dir> <out dir>"""
import json, sys, re, io, os, base64, hashlib, subprocess
import numpy as np
from PIL import Image
sys.path.insert(0, '/tmp/cc')
from profile import prof
from skimage.color import rgb2lab, deltaE_ciede2000
idx_html, FEEDS, OUT = sys.argv[1:4]
t = open(idx_html).read(); i0 = t.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(t[i0:])
os.makedirs(OUT + '/img', exist_ok=True); os.makedirs(OUT + '/t12', exist_ok=True); os.makedirs(OUT + '/mc', exist_ok=True)
nd = lambda d: d.replace('www.', '')
BR = {}
for kind in ('mats', 'racks', 'tiles'):
    for k, v in D[kind].items():
        if '/' not in k or ':' in k.split('/')[0]: continue
        dom = nd(k.split('/')[0]); q = v['u'].split('?', 1)[1] if '?' in v.get('u', '') else ''
        q = '&'.join(p for p in q.split('&') if not p.startswith('variant='))
        BR.setdefault(dom, dict(bn=v['bn'], b=v.get('b', v['bn']), dc=v.get('dc', ''), q=q, host=k.split('/')[0]))
def feed(dom):
    for f in (f'{FEEDS}/{dom}.json', f'{FEEDS}/www.{dom}.json'):
        if os.path.exists(f): return {p['handle']: p for p in json.load(open(f))}
    return {}
TILES = [('sundaymahjong.com', 'sunday-blues-tile-set', 'Sunday Blues'),
         ('bespokemahjong.com', 'pop-diva-mega-tiles', 'Pop Diva Mega'),
         ('bespokemahjong.com', 'lucky-charms-mega-tiles', 'Lucky Charms Mega'),
         ('bambirdboutique.com', 'tiles-box-die', 'Classic Mahjong Tile Set'),
         ('hiphipmahjong.com', 'i-love-mahj-tiles', 'I ❤️ Mahj'),
         ('mahjongstudios.com', 'amber-jade-mahjong-tiles', 'Amber Jade')]
# Yellow Mountain Imports: available American designs not in the app yet
have_ymi = {re.sub(r'[^a-z]', '', v['n'].lower()) for k, v in D['tiles'].items() if 'ymimports' in k}
have_ymi |= {'theclassic', 'koifish', 'koi'}
ymi = feed('ymimports.com'); cand = {}
for h, p in ymi.items():
    ti = p['title']
    if not re.search(r'^(Traditional )?American Mahjong (Set|Tiles)', ti) or re.search(r'chinese|riichi|travel|mini', ti, re.I): continue
    vs = p.get('variants') or []
    if not any(v.get('available') for v in vs): continue
    m = re.search(r'["“”]([^"“”]{2,40})["“”]', ti)
    if not m: continue
    name = m.group(1).strip(); key = re.sub(r'[^a-z]', '', name.lower())
    if key in have_ymi: continue
    tiles_only = ti.startswith('American Mahjong Tiles')
    if key not in cand or (tiles_only and not cand[key][2]): cand[key] = (h, name, tiles_only)
for key, (h, name, _) in sorted(cand.items()): TILES.append(('ymimports.com', h, name))
MATS = [('tigredetartan.com', 'mahjong-mat-ditsy-christmas-maraschino', 'Ditsy Christmas Maraschino')]
B = {}
def uri(im, w, fmt='WEBP', q=76):
    im = im.copy(); im.thumbnail((w, w)); b = io.BytesIO(); im.convert('RGB').save(b, fmt, quality=q)
    v = f'data:image/{fmt.lower()};base64,' + base64.b64encode(b.getvalue()).decode(); hh = hashlib.md5(v.encode()).hexdigest()[:10]; B[hh] = v; return hh
BAD = re.compile(r'box|packag|case|bag|size|dimension|chart|guide|logo|rack|lifestyle|tube|storage', re.I)
def flat_graphic(im):
    q = im.convert('RGB').resize((96, 96)).quantize(16); hs = sorted(q.histogram()[:16], reverse=True)
    return sum(hs[:3]) / max(1, sum(hs)) > 0.86
def photo(p, pick_idx=None):
    ims = p.get('images') or []
    good = [x for x in ims if not BAD.search((x.get('alt') or '') + ' ' + x.get('src', '').split('/')[-1].split('?')[0])] or ims
    order = ([ims[pick_idx]] if pick_idx is not None and pick_idx < len(ims) else []) + good
    for x in order[:5]:
        src = x['src'].split('?')[0] + '?width=1200'; fn = OUT + '/img/' + hashlib.md5(src.encode()).hexdigest()[:12] + '.jpg'
        if not os.path.exists(fn): subprocess.run(['curl', '-s', '-m', '40', src, '-o', fn])
        try: im = Image.open(fn).convert('RGB')
        except Exception: continue
        if not flat_graphic(im): return im, src
    return None, None
def lab(h): return rgb2lab(np.array([[[int(h[i:i+2], 16) / 255 for i in (1, 3, 5)]]]))[0, 0]
PICK = json.load(open(OUT + '/pick.json')) if os.path.exists(OUT + '/pick.json') else {}
added = {'tiles': [], 'mats': []}; flagged = []
nT = 0; rows = []
for dom, h, name in TILES:
    p = feed(dom).get(h); br = BR.get(dom)
    if not p or not br: flagged.append((dom, h, 'no feed/brand')); continue
    key = f"{br['host']}/{h}"
    if key in D['tiles']: continue
    im, src = photo(p, PICK.get(key))
    if im is None: flagged.append((dom, h, 'no usable photo')); continue
    u = f"https://{br['host']}/products/{h}" + (('?' + br['q']) if br['q'] else '')
    full = im.copy(); full.thumbnail((900, 900)); fn = f't12/{nT}.jpg'; full.save(OUT + '/' + fn, quality=80); nT += 1
    pr = prof(im, name) or {'sw': []}
    sw = [[hx, round(s, 2)] for nm, hx, s in pr.get('sw', [])]
    colored = [hx for hx, s in sw if np.hypot(*lab(hx)[1:]) > 18] or [hx for hx, s in sw] or ['#888888']
    avail = any(v.get('available') for v in (p.get('variants') or []))
    D['tiles'][key] = dict(full=fn, n=name, bn=br['bn'], u=u, dc=br['dc'], pa=True, nc=False, rt=False, pile=uri(im, 360), cat=True, add='oct18')
    rows.append((key, name, br['bn'], colored[0], sw)); added['tiles'].append((key, name, br['bn'], avail, src))
# mats -> new mc chunk
maxN = max(int(v['f'].split('/')[1].split('.')[0]) for v in D['mats'].values())
N = (maxN // 12 + 1) * 12; MCH = {}
for dom, h, name in MATS:
    p = feed(dom).get(h); br = BR.get(dom)
    if not p or not br: flagged.append((dom, h, 'no feed/brand')); continue
    key = f"{br['host']}/{h}"
    if key in D['mats']: continue
    im, src = photo(p)
    if im is None: flagged.append((dom, h, 'no usable photo')); continue
    g = im.convert('L').point(lambda q: 255 if q < 238 else 0); bb = g.getbbox(); im = im.crop(bb) if bb else im
    full = im.copy(); full.thumbnail((640, 640)); b = io.BytesIO(); full.save(b, 'WEBP', quality=82)
    f = f'm/{N}.webp'; MCH.setdefault(N // 12, {})[f] = 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode(); N += 1
    pr = prof(im, p['title']) or {'sw': [], 'tone': 'neutral'}
    FAMS = {'red': 'red', 'green': 'green', 'pink': 'pink', 'blue': 'blue'}
    u = f"https://{br['host']}/products/{h}" + (('?' + br['q']) if br['q'] else '')
    D['mats'][key] = dict(n=name, bn=br['bn'], b=br['b'], u=u, dc=br['dc'], pa=True, nc=False, rt=False, c=False, ml=False, add='oct18',
                          f=f, th=uri(im, 150, 'JPEG', 70), w=full.width, h=full.height, mf=['red', 'green'],
                          ms=[[hx, round(s, 2)] for nm, hx, s in pr['sw']], hol=True)
    D['order'].append(key); added['mats'].append((key, name, br['bn'], src))
ix = {m: i for i, m in enumerate(D['order'])}
for k, _, _, _ in added['mats']:
    for s in D['sets']: s['rank'].append(ix[k])
# YMI name fix
for k, v in D['tiles'].items():
    if 'ymimports' in k and v['n'] == 'The': v['n'] = 'The Classic'
for s in D['sets']:
    if s['maker'].startswith('Yellow') and s['name'] == 'The': s['name'] = 'The Classic'
# new catalog sets, ranked by palette similarity (same scoring as Oct 16)
order = D['order']; ML = {m: [(lab(hx), w) for hx, w in D['mats'][m]['ms']] for m in order if D['mats'][m]['ms']}
def sim(A, Bv):
    la = np.array([a for a, _ in A]); wa = np.array([w for _, w in A]); lb = np.array([b for b, _ in Bv])
    Dm = deltaE_ciede2000(np.repeat(la, len(lb), 0), np.tile(lb, (len(la), 1))).reshape(len(la), len(lb))
    return float((Dm.min(1) * wa).sum() / wa.sum())
slugs = {s['slug'] for s in D['sets']}
for key, name, bn, tc, sw in rows:
    slug = re.sub(r'[^a-z0-9]+', '-', f'{bn}-{name}'.lower()).strip('-')[:80]
    while slug in slugs: slug += '-2'
    slugs.add(slug)
    T = [(lab(hx), w) for hx, w in sw] if sw else None
    if T:
        sc = sorted(((0.6 * sim(T, ML[m]) + 0.4 * sim(ML[m], T) + (25 if D['mats'][m].get('hol') else 0)) if m in ML else 999, m) for m in order)
        rank = [ix[m] for _, m in sc]
    else: rank = list(range(len(order)))
    D['sets'].append(dict(slug=slug, name=name, maker=bn, tile=key, tc=tc, tag='', album='', rank=rank, m=[], cat=True))
t2 = t[:i0] + json.dumps(D, separators=(',', ':'), ensure_ascii=False) + t[i0 + end:]
last = re.findall(r'<script src="b\dv\d+\.js"></script>', t2)[-1]
t2 = t2.replace(last, last + '<script src="b9v1.js"></script>', 1)
open(OUT + '/index.html', 'w').write(t2)
open(OUT + '/b9v1.js', 'w').write('window.IMG=Object.assign(window.IMG||{},' + json.dumps(B, separators=(',', ':')) + ');')
for c, o in MCH.items(): json.dump(o, open(f'{OUT}/mc/{c}.json', 'w'), separators=(',', ':'))
json.dump(dict(added=added, flagged=flagged, chunks=sorted(MCH)), open(OUT + '/added_oct18.json', 'w'), indent=1, ensure_ascii=False)
print('tiles', len(D['tiles']), 'sets', len(D['sets']), 'mats', len(D['mats']), 'added', {k: len(v) for k, v in added.items()}, 'flagged', flagged, 'chunks', sorted(MCH))
