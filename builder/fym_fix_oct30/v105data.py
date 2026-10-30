"""FYM v105 (Version 1.9, Oct 30) data: Bespoke double-sided mats = two full sides (Tiffany STANDING Oct 30 10:30am:
"use the image that shows BOTH sides together and crop it 2 times so you have the front and the back. Goes for all Bespoke
double sided mats"). Audit of every Bespoke double-sided mat in b104 (scratchpad/search105/bespoke_ds_before.jpg): the 21 A/B
pairs already show both full sides; two were still wrong:
 - Gray Malin Getaway Dogs (hidden, one entry, old photo): Side A = pool dogs, Side B = ski-lift dogs, from Bespoke's own full
   flat render of each side (photos 2 + 3 on the product page; photo 1 shows both together). Unhidden (her OK 10:19am).
 - Jungle (Dhonk collab, HOT PINK AND TURQUOISE): one entry 'Jungle Turquoise'. Kept as Side A (her 8 album picks point at it,
   photo unchanged) + NEW Side B 'Jungle Hot Pink' cropped from Bespoke's photo 1 (both sides side by side).
New photos go in a new packed chunk mc/<n>.webp (same format as partneradds.py), thumbs inline (moved out of index by the build),
colours measured like partneradds.py, appended to every set's rank (v104rank.py then colour-ranks them; side B right after A).
Usage: python3 v105data.py <build_dir>"""
import sys, os, io, json, base64, hashlib, re, struct, tempfile
from PIL import Image
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
sys.path.insert(0, REPO + 'scripts/colors'); sys.path.insert(0, REPO + 'builder/fym_fix_oct25')
from build_accents import measure
from families import read_image
import numpy as np
from sklearn.cluster import KMeans
from skimage.color import rgb2lab, lab2rgb
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
M = D['mats']; sets = D['sets']
src = open(REPO + 'builder/fym_fix_oct25/v92_splash.py').read()
exec(src[src.index('def kmeans_sw'):src.index('tmpl = ')])
TO = {'teal': 'blue', 'earthy': 'dark', 'brown': 'dark', 'gold': 'yellow'}
ADD = 'oct30-v105-bespoke-ds'
GM = 'www.bespokemahjong.com/bespoke-x-gray-malin-double-sided-mat-double-the-fun-gray-malin-beach-club-mat-copy'
JG = 'www.bespokemahjong.com/double-the-fun-dhonkcollabmat'
A = REPO + 'assets/mats/'
JOBS = [  # key, image or None (keep), name, dn, side, base fields from
    (GM, A + 'graymalin-oct30/gray-malin-getaway-dogs-side-a-pool.jpg', 'Gray Malin Getaway Dogs (Side A: Pool)', 'Gray Malin Getaway Dogs', 'A'),
    (GM + '#side-b', A + 'graymalin-oct30/gray-malin-getaway-dogs-side-b-ski-lift.jpg', 'Gray Malin Getaway Dogs (Side B: Ski Lift)', 'Gray Malin Getaway Dogs', 'B'),
    (JG, None, None, None, 'A'),
    (JG + '#side-b', A + 'bespoke-ds-oct30/jungle-side-b-hot-pink.jpg', 'Jungle Hot Pink', None, 'B'),
]
if not os.path.exists(A + 'bespoke-ds-oct30/jungle-side-b-hot-pink.jpg'):
    os.rename(A + 'bespoke-ds-oct30/jungle-side-a-hot-pink.jpg', A + 'bespoke-ds-oct30/jungle-side-b-hot-pink.jpg')
if M.get(GM + '#side-b', {}).get('add') == ADD:
    print('already applied'); sys.exit(0)
mcb = re.search(r'MCB=new Set\(\[([0-9, ]+)\]\);', h)
maxN = max(int(o['f'].split('/')[1].split('.')[0]) for o in M.values() if o.get('f', '').startswith('m/'))
chunk = max(max(int(v) for v in mcb.group(1).split(',')) + 1, maxN // 12 + 1); n0 = chunk * 12
CH, IMG, colour_mats, log = [], {}, {}, []
for key, img, name, dn, side in JOBS:
    ka = key.split('#')[0]; base = M[ka]
    o = M.get(key) or {k: base[k] for k in ('b', 'bn', 'u', 'u0', 'dc', 'pa', 'nc', 'rt', 'c', 'ml', 'src')}
    if img:
        im = Image.open(img).convert('RGB'); im.thumbnail((640, 640)); b = io.BytesIO(); im.save(b, 'WEBP', quality=86, method=6)
        f = f'm/{n0 + len(CH)}.webp'; CH.append((f, b.getvalue()))
        t = im.copy(); t.thumbnail((150, 150)); bb = io.BytesIO(); t.save(bb, 'JPEG', quality=72)
        th = 'm105' + hashlib.md5(key.encode()).hexdigest()[:8]; IMG[th] = 'data:image/jpeg;base64,' + base64.b64encode(bb.getvalue()).decode()
        path = tempfile.mktemp(suffix='.png'); im.save(path); sh = {}
        for fam, p in measure(path): fam = TO.get(fam, fam); sh[fam] = sh.get(fam, 0) + p
        fams = [c for c, p in sorted(sh.items(), key=lambda kv: -kv[1]) if p >= 8][:4] or [max(sh, key=sh.get)]
        o.update(f=f, th=th, w=im.width, h=im.height, ms=kmeans_sw(im), mf=fams, mt=list(range(len(fams))),
                 sh=[round(sh.get(c, 0), 1) for c in fams], hol=False)
        o.pop('ha', None)
        _, tone, _ = read_image(path); colour_mats[key] = {'sw': o['ms'], 'tone': tone}; os.remove(path)
        log.append((key, name or o.get('n'), fams))
    if name: o['n'] = name
    if dn: o['dn'] = dn
    o['side'] = side; o['twin'] = ka + '#side-b' if side == 'A' else ka
    o.pop('hid', None)
    if key not in M: o['add'] = ADD; M[key] = o; D['order'].append(key)
    else: M[key] = o
M[GM + '#side-b']['add'] = ADD; M[JG + '#side-b']['add'] = ADD
ix = {m: j for j, m in enumerate(D['order'])}
for ka in (GM, JG):
    ja, jb = ix[ka], ix[ka + '#side-b']
    for s in sets:
        for fld in ('rank', 'cr'):
            if fld not in s: continue
            L = s[fld]
            if fld == 'rank' and ja not in L: L.append(ja)
            if ja in L:
                if jb in L: L.remove(jb)
                L.insert(L.index(ja) + 1, jb)
for c in sorted({int(f.split('/')[1].split('.')[0]) // 12 for f, _ in CH}):
    body, hdr = b'', {}
    for f, raw in CH:
        if int(f.split('/')[1].split('.')[0]) // 12 == c: hdr[f] = [len(body), len(raw)]; body += raw
    hj = json.dumps(hdr, separators=(',', ':')).encode(); p = f'{B}/mc/{c}.webp'
    if os.path.exists(p): os.remove(p)
    open(p, 'wb').write(body + hj + struct.pack('<I', len(hj)))
    h = h.replace(mcb.group(0), 'MCB=new Set([' + mcb.group(1) + f', {c}' + ']);', 1)
    print('chunk', c)
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMG, separators=(',', ':')) + ');</script>'
a = '<script src="b24v1.js"></script>'; assert h.count(a) == 1; h = h.replace(a, a + inl, 1)
open(P, 'w').write(h)
# repo records
C = json.load(open(REPO + 'config/fym-colour-oct25.json')); C['mats'].update(colour_mats)
json.dump(C, open(REPO + 'config/fym-colour-oct25.json', 'w'), indent=0, ensure_ascii=False)
FL = json.load(open(REPO + 'builder/fym_flags/mat_photo_flags.json'))
LK = json.load(open(REPO + 'builder/fym_flags/locks.json'))
for key, img, name, dn, side in JOBS:
    o = M[key]
    if img: FL[key] = {'name': o['n'], 'brand': o['bn'], 'flag': 'ok', 'note': 'Oct 30 v105: Bespoke double-sided = full side (Tiffany STANDING 10:30am)'}
    LK['mats'][key] = {k: o.get(k) for k in ('n', 'bn', 'f', 'th', 'rt', 'hid', 'mf', 'mt')}; LK['mats'][key]['hid'] = bool(o.get('hid'))
if isinstance(LK.get('_changes'), list):
    LK['_changes'].append('2026-10-30 v105 Bespoke double-sided: Gray Malin Getaway Dogs split Side A Pool / Side B Ski Lift (unhidden, Tiffany 10:19am); Jungle Turquoise = Side A + new Side B Jungle Hot Pink')
json.dump(FL, open(REPO + 'builder/fym_flags/mat_photo_flags.json', 'w'), indent=1, ensure_ascii=False)
json.dump(LK, open(REPO + 'builder/fym_flags/locks.json', 'w'), indent=1, ensure_ascii=False)
for x in log: print(x)
