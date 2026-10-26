"""FYM v92: Splash of Color mats, batch 2 (Tiffany Oct 25 9:46pm: "just go ahead and bring in another batch of the splash of color mats").
Oct 23 rule: Splash is browse-only (no albums, no Splash tiles), added in batches. 28 in-stock mats picked by eye for variety from
splashofcolorco.com/products.json; photo = Splash's flat product shot (mat on white with the storage bag), cropped to the mat so it
fills the frame (rule 6(3b)); the curled corner showing the backing is part of their standard shot. Holiday = only Christmas/Hanukkah
(Scandinavian Christmas Birds, Star of David Hanukkah). Spec + crops: config/fym-splash-batch2-oct25.json, assets/mats/v92-splash/.
Usage: python3 v92_splash.py <build_dir>"""
import sys, os, io, json, base64, hashlib, re, struct
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
from skimage.color import rgb2lab, lab2rgb
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
sys.path.insert(0, REPO + 'scripts/colors')
from build_accents import measure
from families import read_image
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
M, sets = D['mats'], D['sets']
SPEC = json.load(open(REPO + 'config/fym-splash-batch2-oct25.json'))['mats']
def kmeans_sw(im, k=8, minw=.03):
    a = np.asarray(im.convert('RGB').resize((72, 72))).astype(float).reshape(-1, 3) / 255
    a = a[~(a.min(1) > .94)]
    if len(a) < 50: return []
    L = rgb2lab(a.reshape(-1, 1, 3)).reshape(-1, 3); km = KMeans(n_clusters=k, n_init=3, random_state=0).fit(L)
    cnt = np.bincount(km.labels_, minlength=k) / len(L); out = []
    for j in np.argsort(-cnt):
        if cnt[j] < minw: continue
        rgb = np.clip(lab2rgb(km.cluster_centers_[j].reshape(1, 1, 3)).reshape(3), 0, 1)
        out.append(['#%02x%02x%02x' % tuple(int(round(x * 255)) for x in rgb), round(float(cnt[j]), 3)])
    return out
tmpl = next(v for v in M.values() if v.get('bn') == 'Splash of Color' and '%2Fproducts%2F' in v.get('u', '') and 'sca_ref' in v['u'])
def link(handle):
    u = re.sub(r'%2Fproducts%2F[^%&]+', '%2Fproducts%2F' + handle, tmpl['u'], count=1)
    u0 = re.sub(r'/products/[^?&#]+', '/products/' + handle, tmpl['u0'], count=1)
    return u, u0
IMG = {}; CH = []; added = []; colour_mats = {}
mcb = re.search(r'MCB=new Set\(\[([0-9, ]+)\]\);', h); chunk = max(int(v) for v in mcb.group(1).split(',')) + 1
maxN = max(int(o['f'].split('/')[1].split('.')[0]) for o in M.values() if o.get('f', '').startswith('m/')); chunk = max(chunk, maxN // 12 + 1); n0 = chunk * 12
TO = {'teal': 'blue', 'earthy': 'dark', 'brown': 'dark', 'gold': 'yellow'}
for x in SPEC:
    key = 'splashofcolorco.com/' + x['handle']
    if key in M and not M[key].get('hid'): continue
    im = Image.open(REPO + x['img']).convert('RGB'); im.thumbnail((640, 640)); b = io.BytesIO(); im.save(b, 'WEBP', quality=86, method=6)
    f = f'm/{n0 + len(CH)}.webp'; CH.append((f, b.getvalue()))
    path = f'/tmp/v92s_{len(CH)}.png'; im.save(path)
    t = im.copy(); t.thumbnail((150, 150)); bb = io.BytesIO(); t.save(bb, 'JPEG', quality=72)
    th = 'm92' + hashlib.md5(key.encode()).hexdigest()[:8]; IMG[th] = 'data:image/jpeg;base64,' + base64.b64encode(bb.getvalue()).decode()
    sh = {}
    for fam, p in measure(path): fam = TO.get(fam, fam); sh[fam] = sh.get(fam, 0) + p
    u, u0 = link(x['handle']); hol = bool(x.get('holiday')); cols = list(x['colors'])
    o = dict(n=x['name'], bn='Splash of Color', b='splashofcolorco.com', u=u, u0=u0, dc=tmpl.get('dc', ''), pa=True, nc=False, rt=False, c=False, ml=False,
             f=f, th=th, w=im.width, h=im.height, mf=[] if hol else cols, mt=[] if hol else [0] + [1] * (len(cols) - 1),
             sh=[] if hol else [round(sh.get(c, 0), 1) for c in cols], ms=kmeans_sw(im), hol=hol, src='splash-b2-oct25', add='splash-b2-oct25')
    if hol: o['ha'] = cols
    M[key] = o; D['order'].append(key); added.append(x['name'])
    _, tone, _ = read_image(path); colour_mats[key] = {'sw': o['ms'], 'tone': tone}
ix = {m: j for j, m in enumerate(D['order'])}
for s in sets:
    for k in [k for k in M if M[k].get('add') == 'splash-b2-oct25']:
        if ix[k] not in s['rank']: s['rank'].append(ix[k])
body, hdr = b'', {}
for f, raw in CH: hdr[f] = [len(body), len(raw)]; body += raw
if CH:
    hj = json.dumps(hdr, separators=(',', ':')).encode(); open(f'{B}/mc/{chunk}.webp', 'wb').write(body + hj + struct.pack('<I', len(hj)))
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
if CH: h = h.replace(mcb.group(0), 'MCB=new Set([' + mcb.group(1) + f', {chunk}]);', 1)
inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMG, separators=(',', ':')) + ');</script>'
a = '<script src="b24v1.js"></script>'; assert h.count(a) == 1; h = h.replace(a, a + inl, 1)
open(P, 'w').write(h)
C = json.load(open(REPO + 'config/fym-colour-oct25.json')); C['mats'].update(colour_mats)
json.dump(C, open(REPO + 'config/fym-colour-oct25.json', 'w'), indent=0, ensure_ascii=False)
for n in added: print('added', n)
print('chunk', chunk if CH else None, 'mats', len(added))
