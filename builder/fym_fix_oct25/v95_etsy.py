"""FYM v95: Tiffany's newer Etsy ShopMy mats (Oct 26 10:22am: "at minimum we should bring in Etsy"; Amazon waits for
her picks). Spec: config/fym-etsy-shopmy-oct26.json (21 mats: 14 holiday, 7 year-round; 2 Questionable added hidden).
Pattern = v94_partneradds.py mats (new packed chunk mc/<n>.webp, inline thumb, measured colours, appended to D.order and
every set's rank). Holiday mats (Christmas/winter scenes) live in Holiday only: mf/mt/sh empty, colours in ha (combo-only).
Shop link = her go.shopmy.us link (ShopMy-affiliated, allowed by gate [9]); no code claim (dc '', pa False).
Also writes mat_photo_flags (ok / questionable) and the Questionable list. Idempotent. Usage: python3 v95_etsy.py <build_dir>"""
import sys, os, io, json, base64, hashlib, re, struct, tempfile
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
M, sets = D['mats'], D['sets']
SPEC = json.load(open(REPO + 'config/fym-etsy-shopmy-oct26.json'))['mats']
src = open(REPO + 'builder/fym_fix_oct25/v92_splash.py').read()
exec(src[src.index('def kmeans_sw'):src.index('tmpl = ')])  # same swatch measure as v92/v94
TO = {'teal': 'blue', 'earthy': 'dark', 'brown': 'dark', 'gold': 'yellow'}
IMG = {}; CH = []; colour_mats = {}; added = []
mcb = re.search(r'MCB=new Set\(\[([0-9, ]+)\]\);', h); chunk = max(int(v) for v in mcb.group(1).split(',')) + 1
maxN = max(int(o['f'].split('/')[1].split('.')[0]) for o in M.values() if o.get('f', '').startswith('m/'))
chunk = max(chunk, maxN // 12 + 1); n0 = chunk * 12
for x in SPEC:
    key = x['key']
    if key in M: continue
    im = Image.open(REPO + x['img']).convert('RGB'); im.thumbnail((640, 640)); b = io.BytesIO(); im.save(b, 'WEBP', quality=86, method=6)
    f = f'm/{n0 + len(CH)}.webp'; CH.append((f, b.getvalue()))
    path = tempfile.mktemp(suffix='.png'); im.save(path)
    t = im.copy(); t.thumbnail((150, 150)); bb = io.BytesIO(); t.save(bb, 'JPEG', quality=72)
    th = 'm95' + hashlib.md5(key.encode()).hexdigest()[:8]; IMG[th] = 'data:image/jpeg;base64,' + base64.b64encode(bb.getvalue()).decode()
    sh = {}
    for fam, p in measure(path): fam = TO.get(fam, fam); sh[fam] = sh.get(fam, 0) + p
    fams = [c for c, p in sorted(sh.items(), key=lambda kv: -kv[1]) if p >= 8][:4] or [max(sh, key=sh.get)]
    if x.get('primary') in fams: fams.remove(x['primary']); fams.insert(0, x['primary'])
    o = dict(n=x['name'], bn=x['brand'], b='Etsy', u=x['u'], u0=x['u'], dc='', pa=False, nc=False, rt=False, c=False, ml=False,
             f=f, th=th, w=im.width, h=im.height, ms=kmeans_sw(im), src='shopmy-etsy-oct26', add='oct26-etsy')
    if x['hol']: o.update(mf=[], mt=[], sh=[], ha=fams, hol=True)
    else: o.update(mf=fams, mt=list(range(len(fams))), sh=[round(sh.get(c, 0), 1) for c in fams], hol=False)
    if x['hid']: o['hid'] = True
    M[key] = o; D['order'].append(key); added.append((x['brand'], x['name'], 'holiday' if x['hol'] else 'year-round', 'HIDDEN' if x['hid'] else 'visible', fams))
    _, tone, _ = read_image(path); colour_mats[key] = {'sw': o['ms'], 'tone': tone}; os.remove(path)
ix = {m: j for j, m in enumerate(D['order'])}
newm = [ix[k] for k in M if M[k].get('add') == 'oct26-etsy']
for s in sets:
    if 'rank' in s:
        for j in newm:
            if j not in s['rank']: s['rank'].append(j)
CHUNKS = sorted({int(f.split('/')[1].split('.')[0]) // 12 for f, _ in CH})  # page loads chunk n//12 (MCN=12); split per chunk (bug found Oct 26)
for c in CHUNKS:
    body, hdr = b'', {}
    for f, raw in CH:
        if int(f.split('/')[1].split('.')[0]) // 12 == c: hdr[f] = [len(body), len(raw)]; body += raw
    hj = json.dumps(hdr, separators=(',', ':')).encode(); open(f'{B}/mc/{c}.webp', 'wb').write(body + hj + struct.pack('<I', len(hj)))
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
if CH: h = h.replace(mcb.group(0), 'MCB=new Set([' + mcb.group(1) + ''.join(f', {c}' for c in CHUNKS) + ']);', 1)
if IMG:
    inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMG, separators=(',', ':')) + ');</script>'
    a = '<script src="b24v1.js"></script>'; assert h.count(a) == 1; h = h.replace(a, a + inl, 1)
open(P, 'w').write(h)
# repo-side records (idempotent)
C = json.load(open(REPO + 'config/fym-colour-oct25.json')); C['mats'].update(colour_mats)
json.dump(C, open(REPO + 'config/fym-colour-oct25.json', 'w'), indent=0, ensure_ascii=False)
FL = json.load(open(REPO + 'builder/fym_flags/mat_photo_flags.json'))
Q = json.load(open(REPO + 'builder/fym_flags/fym_questionable.json')); qk = {it['key'] for it in Q['items']}
for x in SPEC:
    FL[x['key']] = {'name': x['name'], 'brand': x['brand'], 'flag': 'questionable' if x['hid'] else 'ok',
                    'note': 'Oct 26 Etsy ShopMy add: ' + (x['reason'] if x['hid'] else ('cropped to the mat' if x['crop'] else 'flat mat photo') + ', colours clear')}
    if x['hid'] and x['key'] not in qk:
        Q['items'].append({'key': x['key'], 'img': M[x['key']]['f'] if x['key'] in M else '', 'name': x['name'], 'brand': x['brand'],
                           'reason': x['reason'], 'photo': x['img'], 'added': '2026-10-26'})
json.dump(FL, open(REPO + 'builder/fym_flags/mat_photo_flags.json', 'w'), indent=1, ensure_ascii=False)
json.dump(Q, open(REPO + 'builder/fym_flags/fym_questionable.json', 'w'), indent=1, ensure_ascii=False)
for a_ in added: print(*a_)
print('chunk', chunk if CH else None, 'mats', len(added))
