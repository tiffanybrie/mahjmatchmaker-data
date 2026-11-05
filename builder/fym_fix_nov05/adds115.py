"""FYM v115 = public "Version 1.15" catalog adds (DESK item 2b, Nov 5). Spec: config/fym-adds-nov05.json (builder/fym_fix_nov05/spec115.py).
Mats follow partneradds109 (new packed chunk mc/<n>.webp, inline thumb, colours measured with build_accents.measure, appended to D.order and
every set's rank; v104rank colour-ranks them after). Holiday mats (Christmas / Hanukkah / winter snow) = Holiday only (mf/mt/sh empty, ha).
Sold-out items carry oos=1 (Sold out badge; stock rules). Twins: Isla neoprene card says 'Also available in leatherette' (altu = leatherette).
Tile sets follow v94_partneradds (catalog sets: cat=True, m=[]; t115/ photo, pile thumb, BACKG group, colour rank via v85_colorrank).
Juniper is a CATALOG set (m=[]); Claude's own Juniper picks are not hers.
Writes mat/tile photo flags, locks for the new items, fym-colour records. Idempotent. Usage: python3 adds115.py <build_dir>"""
import sys, os, io, json, base64, hashlib, re, struct, tempfile, shutil, subprocess
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
SPEC = json.load(open(REPO + 'config/fym-adds-nov05.json'))
src = open(REPO + 'builder/fym_fix_oct25/v92_splash.py').read()
exec(src[src.index('def kmeans_sw'):src.index('tmpl = ')])
TO = {'teal': 'blue', 'earthy': 'dark', 'brown': 'dark', 'gold': 'yellow'}
ADD = 'nov05-v115'
IMG = {}; CH = []; colour_mats = {}; colour_sets = {}; added = []; groups = {}

# 1. mats
mcb = re.search(r'MCB=new Set\(\[([0-9, ]+)\]\);', h); chunk = max(int(v) for v in mcb.group(1).split(',')) + 1
maxN = max(int(o['f'].split('/')[1].split('.')[0]) for o in M.values() if o.get('f', '').startswith('m/'))
chunk = max(chunk, maxN // 12 + 1); n0 = chunk * 12
for x in SPEC['mats']:
    key = x['key']
    if key in M: continue
    im = Image.open(REPO + x['img']).convert('RGB'); im.thumbnail((640, 640)); b = io.BytesIO(); im.save(b, 'WEBP', quality=86, method=6)
    f = f'm/{n0 + len(CH)}.webp'; CH.append((f, b.getvalue()))
    path = tempfile.mktemp(suffix='.png'); im.save(path)
    t = im.copy(); t.thumbnail((150, 150)); bb = io.BytesIO(); t.save(bb, 'JPEG', quality=72)
    th = 'm115' + hashlib.md5(key.encode()).hexdigest()[:8]; IMG[th] = 'data:image/jpeg;base64,' + base64.b64encode(bb.getvalue()).decode()
    sh = {}
    for fam, p in measure(path): fam = TO.get(fam, fam); sh[fam] = sh.get(fam, 0) + p
    fams = [c for c, p in sorted(sh.items(), key=lambda kv: -kv[1]) if p >= 8][:4] or [max(sh, key=sh.get)]
    if x.get('colors'): fams = list(x['colors'])
    o = dict(n=x['name'], bn=x['bn'], b=x['b'], u=x['u'], u0=x['u0'], dc=x['dc'], pa=x['pa'], nc=False, rt=False, c=False, ml=False,
             f=f, th=th, w=im.width, h=im.height, ms=kmeans_sw(im), src='adds-nov05', add=ADD)
    if x['hol']: o.update(mf=[], mt=[], sh=[], ha=fams, hol=True)
    else: o.update(mf=fams, mt=list(range(len(fams))), sh=[round(sh.get(c, 0), 1) for c in fams], hol=False)
    for k_ in ('alt', 'altu'):
        if x.get(k_): o[k_] = x[k_]
    if x.get('oos'): o['oos'] = 1
    if x['hid']: o['hid'] = True
    M[key] = o; D['order'].append(key)
    added.append(('mat', x['bn'], x['name'], 'holiday' if x['hol'] else 'year-round', 'sold out' if x.get('oos') else '', fams))
    _, tone, _ = read_image(path); colour_mats[key] = {'sw': o['ms'], 'tone': tone}; os.remove(path)
ix = {m: j for j, m in enumerate(D['order'])}
newm = [ix[k] for k in M if M[k].get('add') == ADD]

# 2. tile sets (catalog: m=[])
def kmeans_faces(im, k=6, minw=.05):
    a = np.asarray(im.resize((120, 100))).astype(float).reshape(-1, 3) / 255; a = a[~(a.min(1) > .82)]
    L = rgb2lab(a.reshape(-1, 1, 3)).reshape(-1, 3); km = KMeans(n_clusters=k, n_init=3, random_state=0).fit(L)
    cnt = np.bincount(km.labels_, minlength=k) / len(L); out = []
    for j in np.argsort(-cnt):
        if cnt[j] < minw: continue
        rgb = np.clip(lab2rgb(km.cluster_centers_[j].reshape(1, 1, 3)).reshape(3), 0, 1)
        out.append(['#%02x%02x%02x' % tuple(int(round(v * 255)) for v in rgb), round(float(cnt[j]), 3)])
    return out
os.makedirs(B + '/t115', exist_ok=True)
tmpl_s = next(s for s in sets if s.get('cat') and not s['m'] and not s.get('hid'))
for x in SPEC['tiles']:
    key, slug = x['key'], x['slug']
    if key in T and T[key].get('add') == ADD: continue
    im = Image.open(REPO + x['img']).convert('RGB'); fn = f't115/{slug}.jpg'
    if os.path.exists(f'{B}/{fn}'): os.remove(f'{B}/{fn}')
    im.save(f'{B}/{fn}', quality=88)
    S_ = min(im.size); sq = im.crop(((im.width - S_) // 2, (im.height - S_) // 2, (im.width + S_) // 2, (im.height + S_) // 2)).resize((360, 360), Image.LANCZOS)
    pk = 'p115' + hashlib.md5(slug.encode()).hexdigest()[:10]; b = io.BytesIO(); sq.save(b, 'JPEG', quality=84)
    IMG[pk] = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
    T[key] = dict(full=fn, n=x['name'], bn=x['bn'], u=x['u'], u0=x['u0'], dc=x['dc'], pa=x['pa'], nc=False, rt=False, pile=pk, cat=True, src=x['img'], add=ADD)
    if x.get('oos'): T[key].update(oos=1, so=1)
    s = next((y for y in sets if y['tile'] == key), None)
    if s is None:
        s = {k_: v for k_, v in tmpl_s.items() if k_ not in ('cr', 'fp', 'fz', 'sb', 'hid', 'tag', 'album')}
        s['rank'] = list(tmpl_s['rank']); sets.append(s)
    s.update(slug=slug, name=x['name'], maker=x['bn'], tile=key, tc=x['tc'], m=[], album='', tag='', cat=True)
    for j in newm:
        if j not in s['rank']: s['rank'].append(j)
    groups.setdefault(x['group'], []).append(x['name'])
    colour_sets[slug] = {'sw': kmeans_faces(im), 'tone': None, 'src': 'photo', 'back': x['tc']}
    added.append(('tiles', x['bn'], x['name'], x['group'], 'sold out' if x.get('oos') else ''))
for s in sets:
    if 'rank' in s:
        for j in newm:
            if j not in s['rank']: s['rank'].append(j)

# write chunks + D + BACKG + thumbs
CHUNKS = sorted({int(f.split('/')[1].split('.')[0]) // 12 for f, _ in CH})
for c in CHUNKS:
    body, hdr = b'', {}
    for f, raw in CH:
        if int(f.split('/')[1].split('.')[0]) // 12 == c: hdr[f] = [len(body), len(raw)]; body += raw
    hj = json.dumps(hdr, separators=(',', ':')).encode(); _p = f'{B}/mc/{c}.webp'
    if os.path.exists(_p): os.remove(_p)  # never write through a hardlink into the source build
    open(_p, 'wb').write(body + hj + struct.pack('<I', len(hj)))
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
if CH: h = h.replace(mcb.group(0), 'MCB=new Set([' + mcb.group(1) + ''.join(f', {c}' for c in CHUNKS) + ']);', 1)
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

# colour ranking (s.cr) for the new tile sets
C = json.load(open(REPO + 'config/fym-colour-oct25.json')); C['sets'].update(colour_sets); C['mats'].update(colour_mats)
json.dump(C, open(REPO + 'config/fym-colour-oct25.json', 'w'), indent=0, ensure_ascii=False)
if colour_sets:
    tmp = tempfile.mkdtemp(); shutil.copy(P, tmp + '/index.html')
    subprocess.run([sys.executable, REPO + 'builder/fym_fix_oct25/v85_colorrank.py', tmp], check=True, capture_output=True)
    h2 = open(tmp + '/index.html').read(); i2 = h2.index('const D=') + 8; D2, _ = json.JSONDecoder().raw_decode(h2[i2:])
    cr = {s['slug']: s.get('cr') for s in D2['sets'] if s['slug'] in colour_sets}; shutil.rmtree(tmp)
    h = open(P).read(); i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
    for s in D['sets']:
        if s['slug'] in cr and cr[s['slug']]: s['cr'] = cr[s['slug']]
    h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]; open(P, 'w').write(h)
    M, T, sets = D['mats'], D['tiles'], D['sets']

# repo-side records (idempotent)
FL = json.load(open(REPO + 'builder/fym_flags/mat_photo_flags.json'))
LK = json.load(open(REPO + 'builder/fym_flags/locks.json'))
for x in SPEC['mats']:
    FL[x['key']] = {'name': x['name'], 'brand': x['bn'], 'flag': 'questionable' if x['hid'] else 'ok', 'note': 'Nov 5 v115 add: ' + x.get('photo_note', '')}
    o = M[x['key']]; LK['mats'][x['key']] = {k: o.get(k) for k in ('n', 'bn', 'f', 'th', 'rt', 'mf', 'mt')}; LK['mats'][x['key']]['hid'] = bool(o.get('hid'))
TF = json.load(open(REPO + 'builder/fym_flags/tile_photo_flags.json'))
for x in SPEC['tiles']:
    TF[x['slug']] = {'name': x['name'], 'maker': x['bn'], 'flag': 'ok', 'note': 'Nov 5 v115: ' + x.get('photo_note', ''), 'photo': T[x['key']]['full']}
json.dump(FL, open(REPO + 'builder/fym_flags/mat_photo_flags.json', 'w'), indent=1, ensure_ascii=False)
json.dump(LK, open(REPO + 'builder/fym_flags/locks.json', 'w'), indent=1, ensure_ascii=False)
json.dump(TF, open(REPO + 'builder/fym_flags/tile_photo_flags.json', 'w'), indent=1, ensure_ascii=False)
for a_ in added: print(*a_)
print('chunks', CHUNKS, 'items', len(added))
