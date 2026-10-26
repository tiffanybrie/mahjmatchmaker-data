"""FYM v95: Bespoke Mahjong double-sided ("Double the Fun") mats listed TWICE, one entry per side (Tiffany Oct 26 11:41am:
"I don't want to put both of them up on the same card... have it listed twice so it can show this is one side of it and this
is the other side"; e.g. The Chalet Mat side B = ski lift + skis for Apres Ski Club).
Spec: config/fym-bespoke-2side-oct26.json. Side A = the existing entry, its name gains " (Side A: <label>)" (locks.json
updated to match). Side B = new key "<A key>#side-b": the brand's own side-B listing photo (assets/mats/v95-bespoke-sideb,
white margins trimmed), same shop link + code as side A, colours measured from that photo with the v95_etsy pipeline,
holiday per the photo (ski/snow/Christmas = Holiday: colours combo-only in ha). Short card name dn = side A's dn (no side
label, so the card subtitle fits, gate [72]). Side B sits right after side A in every set's rank/cr. Her picks (s.m, lm,
mord) are NOT touched. Writes mat_photo_flags ok + locks for side B. Idempotent. Gate [78].
Usage: python3 v95_bespoke2side.py <build_dir>"""
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
M, sets = D['mats'], D['sets']
SPEC = json.load(open(REPO + 'config/fym-bespoke-2side-oct26.json'))['mats']
src = open(REPO + 'builder/fym_fix_oct25/v92_splash.py').read()
exec(src[src.index('def kmeans_sw'):src.index('tmpl = ')])  # same swatch measure as v92/v94/v95_etsy
TO = {'teal': 'blue', 'earthy': 'dark', 'brown': 'dark', 'gold': 'yellow'}
COPY = ('b', 'bn', 'u', 'u0', 'dc', 'pa', 'nc', 'rt', 'c', 'ml', 'src')
IMG = {}; CH = []; colour_mats = {}; added = []; renamed = 0
mcb = re.search(r'MCB=new Set\(\[([0-9, ]+)\]\);', h); chunk = max(int(v) for v in mcb.group(1).split(',')) + 1
maxN = max(int(o['f'].split('/')[1].split('.')[0]) for o in M.values() if o.get('f', '').startswith('m/'))
chunk = max(chunk, maxN // 12 + 1); n0 = chunk * 12
for ka, x in SPEC.items():
    A = M.get(ka)
    if not A: print('missing side A', ka); continue
    nA = f"{x['nameA']} (Side A: {x['sideA']})"
    if A['n'] != nA: A['n'] = nA; renamed += 1
    A['side'] = 'A'; A['twin'] = ka + '#side-b'
    if not A.get('dn'):  # short card-subtitle name without the side label ("tiles on the <dn> mat"); MAT label keeps n
        A['dn'] = re.sub(r'\s*\((Double-Sided)\)|^Bespoke x Corey Paige - |^The |\s+Mat$', '', x['nameA']).replace('Grateful Dead x Bespoke Mahjong', 'Grateful Dead').strip()
    kb = ka + '#side-b'
    if kb in M: continue
    im = Image.open(REPO + x['imgB']).convert('RGB'); im.thumbnail((640, 640)); b = io.BytesIO(); im.save(b, 'WEBP', quality=86, method=6)
    f = f'm/{n0 + len(CH)}.webp'; CH.append((f, b.getvalue()))
    path = tempfile.mktemp(suffix='.png'); im.save(path)
    t = im.copy(); t.thumbnail((150, 150)); bb = io.BytesIO(); t.save(bb, 'JPEG', quality=72)
    th = 'm95b' + hashlib.md5(kb.encode()).hexdigest()[:8]; IMG[th] = 'data:image/jpeg;base64,' + base64.b64encode(bb.getvalue()).decode()
    sh = {}
    for fam, p in measure(path): fam = TO.get(fam, fam); sh[fam] = sh.get(fam, 0) + p
    fams = [c for c, p in sorted(sh.items(), key=lambda kv: -kv[1]) if p >= 8][:4] or [max(sh, key=sh.get)]
    o = {k: A[k] for k in COPY if k in A}
    o.update(n=f"{x['nameA']} (Side B: {x['sideB']})", f=f, th=th, w=im.width, h=im.height, ms=kmeans_sw(im),
             add='oct26-bespoke-sideb', side='B', twin=ka)
    if A.get('dn'): o['dn'] = A['dn']
    if x['holB']: o.update(mf=[], mt=[], sh=[], ha=fams, hol=True)
    else: o.update(mf=fams, mt=list(range(len(fams))), sh=[round(sh.get(c, 0), 1) for c in fams], hol=False)
    if A.get('hid'): o['hid'] = True
    M[kb] = o; D['order'].append(kb); added.append((x['nameA'], x['sideB'], 'holiday' if x['holB'] else 'year-round', fams))
    _, tone, _ = read_image(path); colour_mats[kb] = {'sw': o['ms'], 'tone': tone}; os.remove(path)
for ka in SPEC:  # side B shares side A's short card name (re-synced every run)
    if ka in M and ka + '#side-b' in M and M[ka].get('dn'): M[ka + '#side-b']['dn'] = M[ka]['dn']
# rank: side B right after side A (both lists), else at the end
ix = {m: j for j, m in enumerate(D['order'])}
pairs = [(ix[ka], ix[ka + '#side-b']) for ka in SPEC if ka in ix and ka + '#side-b' in ix]
for s in sets:
    for fld in ('rank', 'cr'):
        if fld not in s: continue
        L = s[fld]
        for ja, jb in pairs:
            if jb in L: continue
            if ja in L: L.insert(L.index(ja) + 1, jb)
            elif fld == 'rank': L.append(jb)
CHUNKS = sorted({int(f.split('/')[1].split('.')[0]) // 12 for f, _ in CH})  # the page loads chunk n//12 (MCN=12)
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
if colour_mats:
    C = json.load(open(REPO + 'config/fym-colour-oct25.json')); C['mats'].update(colour_mats)
    json.dump(C, open(REPO + 'config/fym-colour-oct25.json', 'w'), indent=0, ensure_ascii=False)
FL = json.load(open(REPO + 'builder/fym_flags/mat_photo_flags.json'))
LK = json.load(open(REPO + 'builder/fym_flags/locks.json')); lch = False
for ka, x in SPEC.items():
    kb = ka + '#side-b'
    if kb not in M: continue
    FL[kb] = {'name': M[kb]['n'], 'brand': 'Bespoke Mahjong', 'flag': 'ok',
              'note': "Oct 26 double-sided side B: brand's own flat listing photo of that side, colours clear"}
    if ka in LK['mats'] and LK['mats'][ka].get('n') != M[ka]['n']: LK['mats'][ka]['n'] = M[ka]['n']; lch = True
    if kb not in LK['mats']:
        LK['mats'][kb] = {k: M[kb][k] for k in ('n', 'bn', 'f', 'th', 'rt', 'mf', 'mt') if k in M[kb]}
        LK['mats'][kb]['hid'] = bool(M[kb].get('hid')); lch = True
if lch:
    note = '2026-10-26: Bespoke double-sided mats listed twice (Side A / Side B names + side-B entries; Tiffany 11:41am)'
    if note not in LK['_changes']: LK['_changes'].append(note)
    json.dump(LK, open(REPO + 'builder/fym_flags/locks.json', 'w'), indent=1, ensure_ascii=False)
json.dump(FL, open(REPO + 'builder/fym_flags/mat_photo_flags.json', 'w'), indent=1, ensure_ascii=False)
for a_ in added: print(*a_)
print('bespoke2side: side A renamed', renamed, '| side B added', len(added), '| chunks', CHUNKS if CH else None)
