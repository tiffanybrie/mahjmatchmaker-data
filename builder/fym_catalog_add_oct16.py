"""Oct 16 catalog fill (doc 65): add the partner mats + racks the shop-vs-app check found missing.
Low catalog bar (doc 55): real product, listing photo that shows it. New mats get the next m/N numbers in
NEW mc chunks; thumbs + rack photos go in a new IMG bundle. Ranks are re-sorted by palette similarity
(her own matches stay first). Usage: python3 fym_catalog_add_oct16.py <live index.html> <report.json> <feeds dir> <out dir>"""
import json, sys, re, io, os, base64, hashlib, subprocess, collections
import numpy as np
from PIL import Image
sys.path.insert(0, '/tmp/cc'); sys.path.insert(0, '/tmp/sw')
from profile import prof, PAL
from skimage.color import rgb2lab, deltaE_ciede2000
idx_html, REP, FEEDS, OUT = sys.argv[1:5]
t = open(idx_html).read(); i0 = t.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(t[i0:])
rep = json.load(open(REP))
L = json.load(open('/home/claude/mahjmatchmaker-data/catalog/locked_decisions.json'))
SKIPDOM = {'splashofcolorco.com', 'themahjongpress.com'}
nd = lambda d: d.replace('www.', '')
# brand info from existing items of the same shop
BR = {}
for kind in ('mats', 'racks'):
    for k, v in D[kind].items():
        if '/' not in k or ':' in k.split('/')[0]: continue
        dom = nd(k.split('/')[0]); q = v['u'].split('?', 1)[1] if '?' in v.get('u', '') else ''
        q = '&'.join(p for p in q.split('&') if not p.startswith('variant='))
        BR.setdefault(dom, dict(bn=v['bn'], b=v['b'], dc=v.get('dc', ''), q=q, host=k.split('/')[0]))
def feed(dom):
    for f in (f'{FEEDS}/{dom}.json', f'{FEEDS}/www.{dom}.json'):
        if os.path.exists(f): return json.load(open(f))
    return []
def hx(img):
    a = np.asarray(img.convert('RGB').resize((80, 80))).reshape(-1, 3)
    keep = ~((a.min(1) > 225) & (a.max(1) - a.min(1) < 18)); a = a[keep] if keep.sum() > 200 else a
    m = np.median(a, 0).astype(int); return '#%02x%02x%02x' % tuple(m)
names = list(PAL); plab = rgb2lab(np.array([[int(PAL[n][i:i+2], 16) / 255 for i in (0, 2, 4)] for n in names])[None])[0]
def lab(h): return rgb2lab(np.array([[[int(h[i:i+2], 16) / 255 for i in (1, 3, 5)]]]))[0, 0]
FAM = {'pink': 'blush,pink,hot pink,berry', 'red': 'red,burgundy', 'orange': 'peach,coral,terracotta,rust,orange',
       'yellow': 'butterscotch,mustard,gold,butter yellow,lemon', 'green': 'sage,olive,moss,chartreuse,kelly green,emerald,hunter green,forest,mint,seafoam',
       'blue': 'light blue,sky blue,french blue,cobalt,navy,denim,teal,turquoise,aqua', 'purple': 'lavender,lilac,purple,plum',
       'neutral': 'white,ivory,cream,beige,taupe,tan,camel,gray', 'dark': 'brown,chocolate,walnut,charcoal,black'}
C2F = {c: f for f, v in FAM.items() for c in v.split(',')}
def fams(sw):
    out = []
    for i, (n, h, s) in enumerate(sw):
        f = C2F.get(n)
        if not f: continue
        if f in ('neutral', 'dark') and not (i == 0 and s >= .25) and s < .3: continue
        if s >= .1 or (i < 2 and s >= .07):
            if f not in out: out.append(f)
    return out[:3]
def trim(im):
    g = im.convert('L').point(lambda p: 255 if p < 238 else 0); bb = g.getbbox(); return im.crop(bb) if bb else im
DROP = re.compile(r'\btube\b|caddy|mat band|mat storage|mat sleeve|clear mat sleeves|protective|coming this|starter|umbrella|roll with it|roller|single \(one\)|lucite pusher|less than perfect|odd lots|imperfect|rack pack|mahjong game set|mah-jinn|protective|scrabble|tile pushers|\btiles$|\btote\b', re.I)  # checked by eye Oct 16: accessories, seconds, bundles, singles
BAD = re.compile(r'tube|bag|storage|size|dimension|measure|chart|guide|logo|box|packag', re.I)
def pick_img(p):
    ims = p.get('images') or []
    if isinstance(ims, str):
        try: ims = eval(ims)
        except Exception: ims = []
    good = [x for x in ims if not BAD.search((x.get('alt') or '') + ' ' + x.get('src', '').split('/')[-1])]
    return (good or ims or [None])[0]
def get(url, fn):
    if not os.path.exists(fn): subprocess.run(['curl', '-s', '-m', '40', url, '-o', fn])
    return Image.open(fn)
def clean_mat(n):
    n = re.sub(r'^(NEW|PRE-?ORDER|【[^】]*】)[:!\s-]*', '', n, flags=re.I)
    n = re.sub(r'\s*[-|–]\s*(PREORDER|Pre-?Order).*$', '', n, flags=re.I)
    n = re.sub(r'\b(Mahjong|Mahj)\s+(Game\s+)?(Play(ing)?\s+)?Mat\b,?\s*', '', n, flags=re.I).strip(' -|,:')
    n = re.sub(r'\s*Mat$', '', n).strip(' -|,:')
    return n or 'Mahjong Mat'
def clean_rack(n, bn):
    n = re.sub(r'\s*(Mahjong\s+)?Racks?\b.*$', '', n, flags=re.I).strip(' -|,:') or n
    return (bn + ' ' + n).strip()
os.makedirs(OUT + '/img', exist_ok=True); os.makedirs(OUT + '/mc', exist_ok=True)
B = {}  # bundle hash -> data uri
def uri(im, fmt, q, w):
    im = im.copy(); im.thumbnail((w, w)); b = io.BytesIO()
    im.convert('RGBA' if fmt == 'WEBP' else 'RGB').save(b, fmt, quality=q)
    v = f'data:image/{fmt.lower()};base64,' + base64.b64encode(b.getvalue()).decode(); h = hashlib.md5(v.encode()).hexdigest()[:10]; B[h] = v; return h
maxN = max(int(v['f'].split('/')[1].split('.')[0]) for v in D['mats'].values())
N = (maxN // 12 + 1) * 12; firstN = N; MCH = collections.defaultdict(dict)
added = {'mats': [], 'racks': []}; flagged = []
for dom, rows in rep.items():
    if dom in SKIPDOM: continue
    fd = {x['handle'].rstrip('/').split('/')[-1]: x for x in feed(dom)}
    br = BR.get(dom)
    for r in rows:
        if r['inapp'] or r['rule'] or r['cat'] not in ('mats', 'racks'): continue
        p = fd.get(r['h'])
        if not p or not br: flagged.append((dom, r['t'], 'no feed/brand info')); continue
        host = br['host']; key = f"{host}/{r['h']}"
        if L.get(key, {}).get('status') == 'rejected': continue
        if DROP.search(p['title']) or r['h'].startswith('sn-se'): flagged.append((dom, r['t'], 'left out: not a mat/rack product')); continue
        im0 = pick_img(p)
        if not im0: flagged.append((dom, r['t'], 'no photo')); continue
        src = im0['src'].split('?')[0] + '?width=1400'
        try: im = get(src, OUT + '/img/' + hashlib.md5(src.encode()).hexdigest()[:12] + '.jpg').convert('RGB')
        except Exception: flagged.append((dom, r['t'], 'photo download failed')); continue
        u = r['url'] if r['url'].startswith('http') else 'https://' + host + '/products/' + r['h']
        u = u.split('?')[0] + (('?' + br['q']) if br['q'] else '')
        base = dict(bn=br['bn'], b=br['b'], u=u, dc=br['dc'], pa=True, nc=False, rt=False, c=False, ml=False, add='oct16')
        if r['cat'] == 'mats':
            im = trim(im); full = im.copy(); full.thumbnail((640, 640)); b = io.BytesIO(); full.save(b, 'WEBP', quality=82)
            f = f'm/{N}.webp'; MCH[N // 12][f] = 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode(); N += 1
            pr = prof(im, p['title']) or {'sw': [], 'tone': 'neutral'}
            D['mats'][key] = dict(base, n=clean_mat(p['title']), f=f, th=uri(im, 'JPEG', 70, 150), w=full.width, h=full.height,
                                  mf=fams(pr['sw']), ms=[[h, round(s, 2)] for n, h, s in pr['sw']], hol=pr['tone'] == 'holiday')
            D['order'].append(key); added['mats'].append(key)
        else:
            h = hx(im); L0 = lab(h); n = names[int(np.argmin(deltaE_ciede2000(np.repeat(L0[None], len(names), 0), plab)))]
            D['racks'][key] = dict(base, n=clean_rack(p['title'], br['bn']), sk=False, hx=h, rf=[C2F[n]], im=uri(im, 'JPEG', 78, 420))
            added['racks'].append(key)
# re-rank: her matches first, then everything by palette similarity (doc: same scoring as /tmp/sw/prep.py)
SWJ = json.load(open('/tmp/sw/swipe.json')); TS = SWJ['ts']
order = D['order']; ix = {m: i for i, m in enumerate(order)}
ML = {m: [(lab(h), w) for h, w in D['mats'][m]['ms']] for m in order if D['mats'][m]['ms']}
def sim(A, Bv):
    la = np.array([a for a, _ in A]); wa = np.array([w for _, w in A]); lb = np.array([b for b, _ in Bv])
    Dm = deltaE_ciede2000(np.repeat(la, len(lb), 0), np.tile(lb, (len(la), 1))).reshape(len(la), len(lb))
    return float((Dm.min(1) * wa).sum() / wa.sum())
for s in D['sets']:
    her = [m for m, _ in s['m'] if m in ix]
    T = [(lab(h), w) for h, w in TS.get(s['slug'], [])]
    if not T: s['rank'] = s['rank'] + [ix[m] for m in added['mats']]; continue
    rest = [m for m in order if m not in her]
    sc = sorted(((0.6 * sim(T, ML[m]) + 0.4 * sim(ML[m], T) + (25 if D['mats'][m].get('hol') else 0)) if m in ML else 999, m) for m in rest)
    s['rank'] = [ix[m] for m in dict.fromkeys(her)] + [ix[m] for _, m in sc]
    assert len(s['rank']) == len(order), s['slug']
for c, o in MCH.items(): json.dump(o, open(f'{OUT}/mc/{c}.json', 'w'), separators=(',', ':'))
open(OUT + '/b5v1.js', 'w').write('window.IMG=Object.assign(window.IMG||{},' + json.dumps(B, separators=(',', ':')) + ');')
t2 = t[:i0] + json.dumps(D, separators=(',', ':'), ensure_ascii=False) + t[i0 + end:]
t2 = t2.replace('<script src="b4v11.js"></script>', '<script src="b4v11.js"></script><script src="b5v1.js"></script>', 1)
assert 'b5v1.js' in t2
open(OUT + '/index.html', 'w').write(t2)
json.dump(dict(added=added, flagged=flagged, chunks=sorted(MCH)), open(OUT + '/added.json', 'w'), indent=1)
print('mats', len(D['mats']), 'racks', len(D['racks']), 'added', {k: len(v) for k, v in added.items()}, 'flagged', len(flagged), 'chunks', sorted(MCH))
