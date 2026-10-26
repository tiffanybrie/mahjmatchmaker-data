"""FYM v94: partners with nothing in the app (Tiffany Oct 26 8:38am: "make sure everyone is in the app. If I send this to a
partner brand and they come back and say, hey, we don't see ourselves, that's not good").
Adds Mahjong Co. Kaleidoscope tiles (their only product; real photo of faces + pink backs, framed 16:7) and 7 Fait à Main
full-size mats (their flat product shots, white margins trimmed). Spec + skips: config/fym-partner-adds-oct26.json.
Fait à Main has no affiliate link/code yet -> plain links, pa False, dc '' (no code claim). Catalog sets m=[]. Idempotent.
Usage: python3 v94_partneradds.py <build_dir>"""
import sys, os, io, json, base64, hashlib, re, struct, subprocess, shutil, tempfile
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
from skimage.color import rgb2lab, lab2rgb
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
sys.path.insert(0, REPO + 'scripts/colors'); sys.path.insert(0, REPO + 'builder/fym_fix_oct25')
from build_accents import measure
from families import read_image
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
T, M, sets = D['tiles'], D['mats'], D['sets']
SPEC = json.load(open(REPO + 'config/fym-partner-adds-oct26.json'))
src = open(REPO + 'builder/fym_fix_oct25/v92_splash.py').read()
exec(src[src.index('def kmeans_sw'):src.index('tmpl = ')])  # same swatch measure as v92
def kmeans_faces(im, k=6, minw=.05):
    import numpy as np
    from sklearn.cluster import KMeans
    from skimage.color import rgb2lab, lab2rgb
    a = np.asarray(im.convert('RGB').resize((96, 42))).astype(float).reshape(-1, 3) / 255
    a = a[~((a.min(1) > .82) & (a.max(1) - a.min(1) < .12))]; a = a[~((a[:, 2] - a[:, 0] > .12) & (a[:, 2] > .75) & (a[:, 1] > .7))]  # tile white + blue backdrop
    L = rgb2lab(a.reshape(-1, 1, 3)).reshape(-1, 3); km = KMeans(n_clusters=k, n_init=3, random_state=0).fit(L)
    cnt = np.bincount(km.labels_, minlength=k) / len(L); out = []
    for j in np.argsort(-cnt):
        if cnt[j] < minw: continue
        rgb = np.clip(lab2rgb(km.cluster_centers_[j].reshape(1, 1, 3)).reshape(3), 0, 1)
        out.append(['#%02x%02x%02x' % tuple(int(round(x * 255)) for x in rgb), round(float(cnt[j]), 3)])
    return out
IMG = {}; added = []; colour_sets = {}; colour_mats = {}; groups = {}
os.makedirs(B + '/t94', exist_ok=True)
tmpl_s = next(s for s in sets if s.get('cat') and not s['m'])
for x in SPEC['tiles']:
    key = x['key']
    if key in T and not T[key].get('hid'): continue
    im = Image.open(REPO + x['img']).convert('RGB'); slug = re.sub(r'[^a-z0-9]+', '-', (x['brand'] + ' ' + x['name']).lower()).strip('-')
    fn = f't94/{slug}.jpg'; im.save(f'{B}/{fn}', quality=86)
    pk = 'p94' + hashlib.md5(slug.encode()).hexdigest()[:10]; sq = im.crop((450, 0, 1150, 700)).resize((360, 360), Image.LANCZOS)
    b = io.BytesIO(); sq.save(b, 'JPEG', quality=84); IMG[pk] = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
    T[key] = dict(n=x['name'], bn=x['brand'], full=fn, pile=pk, u=x['u'], u0=x['u0'], dc=x['dc'], pa=x['pa'], nc=False, rt=False, cat=True, add='oct26-partners', bf=[.5, .5])
    s = next((y for y in sets if y['tile'] == key), None)
    if s is None:
        s = {k_: v for k_, v in tmpl_s.items() if k_ not in ('cr', 'fp', 'fz', 'sb', 'hid')}; s.update(slug=slug, tile=key, m=[], album='', tag='', cat=True); sets.append(s)
    s.update(name=x['name'], maker=x['brand'], tc=x['tc'])
    groups.setdefault(x['group'], []).append(x['name']); added.append(('tile', x['brand'], x['name']))
    colour_sets[slug] = {'sw': kmeans_faces(im), 'tone': None, 'src': 'photo', 'back': x['tc']}
mcb = re.search(r'MCB=new Set\(\[([0-9, ]+)\]\);', h); chunk = max(int(v) for v in mcb.group(1).split(',')) + 1
maxN = max(int(o['f'].split('/')[1].split('.')[0]) for o in M.values() if o.get('f', '').startswith('m/')); chunk = max(chunk, maxN // 12 + 1); n0 = chunk * 12; CH = []
TO = {'teal': 'blue', 'earthy': 'dark', 'brown': 'dark', 'gold': 'yellow'}
for x in SPEC['mats']:
    key = 'faitamainstudio.com/' + x['handle']
    if key in M and not M[key].get('hid'): continue
    im = Image.open(REPO + x['img']).convert('RGB'); im.thumbnail((640, 640)); b = io.BytesIO(); im.save(b, 'WEBP', quality=86, method=6)
    f = f'm/{n0 + len(CH)}.webp'; CH.append((f, b.getvalue()))
    path = tempfile.mktemp(suffix='.png'); im.save(path)
    t = im.copy(); t.thumbnail((150, 150)); bb = io.BytesIO(); t.save(bb, 'JPEG', quality=72)
    th = 'm94' + hashlib.md5(key.encode()).hexdigest()[:8]; IMG[th] = 'data:image/jpeg;base64,' + base64.b64encode(bb.getvalue()).decode()
    sh = {}
    for fam, p in measure(path): fam = TO.get(fam, fam); sh[fam] = sh.get(fam, 0) + p
    cols = list(x['colors']); u = 'https://faitamainstudio.com/products/' + x['handle']
    M[key] = dict(n=x['name'], bn='Fait à Main', b='faitamainstudio.com', u=u, u0=u, dc='', pa=False, nc=False, rt=False, c=False, ml=False,
                  f=f, th=th, w=im.width, h=im.height, mf=cols, mt=[0] + [1] * (len(cols) - 1), sh=[round(sh.get(c, 0), 1) for c in cols],
                  ms=kmeans_sw(im), hol=False, src='partner-adds-oct26', add='oct26-partners')
    D['order'].append(key); added.append(('mat', 'Fait à Main', x['name']))
    _, tone, _ = read_image(path); colour_mats[key] = {'sw': M[key]['ms'], 'tone': tone}; os.remove(path)
ix = {m: j for j, m in enumerate(D['order'])}
newm = [ix[k] for k in M if M[k].get('add') == 'oct26-partners']
for s in sets:
    for j in newm:
        if j not in s['rank']: s['rank'].append(j)
body, hdr = b'', {}
for f, raw in CH: hdr[f] = [len(body), len(raw)]; body += raw
if CH:
    hj = json.dumps(hdr, separators=(',', ':')).encode(); open(f'{B}/mc/{chunk}.webp', 'wb').write(body + hj + struct.pack('<I', len(hj)))
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
if CH: h = h.replace(mcb.group(0), 'MCB=new Set([' + mcb.group(1) + f', {chunk}]);', 1)
j = h.index('const BACKG=') + len('const BACKG='); BG, bend = json.JSONDecoder().raw_decode(h[j:]); bend += j
for g, names in groups.items():
    BG.setdefault(g, [])
    for n in names:
        if n not in BG[g]: BG[g].append(n)
h = h[:j] + json.dumps(BG, ensure_ascii=False) + h[bend:]
if IMG:
    inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMG, separators=(',', ':')) + ');</script>'
    a = '<script src="b24v1.js"></script>'; assert h.count(a) == 1; h = h.replace(a, a + inl, 1)
open(P, 'w').write(h)
C = json.load(open(REPO + 'config/fym-colour-oct25.json')); C['sets'].update(colour_sets); C['mats'].update(colour_mats)
json.dump(C, open(REPO + 'config/fym-colour-oct25.json', 'w'), indent=0, ensure_ascii=False)
# colour ranking (s.cr) for the new tile set only: run v85_colorrank on a scratch copy and copy back just those sets' cr
if colour_sets:
    tmp = tempfile.mkdtemp(); shutil.copy(P, tmp + '/index.html')
    subprocess.run([sys.executable, REPO + 'builder/fym_fix_oct25/v85_colorrank.py', tmp], check=True, capture_output=True)
    h2 = open(tmp + '/index.html').read(); i2 = h2.index('const D=') + 8; D2, _ = json.JSONDecoder().raw_decode(h2[i2:])
    cr = {s['slug']: s.get('cr') for s in D2['sets'] if s['slug'] in colour_sets}; shutil.rmtree(tmp)
    h = open(P).read(); i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
    for s in D['sets']:
        if s['slug'] in cr and cr[s['slug']]: s['cr'] = cr[s['slug']]
    h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]; open(P, 'w').write(h)
for a_ in added: print(*a_)
print('chunk', chunk if CH else None, 'items', len(added))
