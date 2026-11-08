"""FYM 1.18 (if in time, else 1.19): Ozark Mahjongg catalog add + real-domain links (Tiffany Nov 7 10:45pm: the store is
https://www.ozarkmahjongg.com (Wix, /product-page/<slug>); our ozarkmahjong.com links were a parked wrong domain, and FYM had only 4 of
the store's 15 mats). Spec config/fym-ozark-nov07.json (photos assets/mats/ozark-nov07/, contact sheets assets/qa/ozark-nov07/ LOOKED at).
Ozark = NON-partner WHOLE-LINE allow (Oct 20, builder/fym_flags/nonpartner_allow.json): plain shop link, NO code claim.
1. Adds the 11 spec mats like shopmy_nov07.py (new packed mc chunk, inline thumb, by-eye colours 'mf' with measured shares, appended to
   D.order + every set's rank; v104rank colour-ranks them after). dc '', pa False, ncn 1 ('No code available at this time').
   Every Ozark mat is OUT OF STOCK on the store (Wix inventory, Nov 7) -> oos 1 (Sold out badge, not retired; config/fym-stock.json
   carries in:false for each, gate [138]). 4 close-up-only mats: hidden + Questionable (gate [3]/[3d]).
   Table view: the 7 visible ones are flat top-down store photos cropped to the mat -> D.tv.cls 'A' (the FYM photo is the whole mat).
2. The 4 existing Ozark mats (keys keep the old 'ozarkmahjong.com/' prefix: IDs, not links) get u/u0 = the real product page and oos 1.
   Idempotent with fixes118.py, which re-points the same four.
3. Repo records at build time (idempotent; --dry skips them): mat_photo_flags, fym_questionable, locks (n/bn/f/th/rt/mf/mt/hid of the
   new mats, so colour116 never re-tags the by-eye colours), fym-colour-oct25 swatches.
Run after adds118.sh / partner_adds118.py and BEFORE deadlinks116 / v104rank / colour116 / fym_apply_locks.
Usage: python3 builder/fym_fix_nov07/ozark_v119.py <build_dir> [--dry]"""
import sys, os, io, json, base64, hashlib, re, struct, tempfile
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
from skimage.color import rgb2lab, lab2rgb
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
sys.path.insert(0, REPO + 'scripts/colors'); sys.path.insert(0, REPO + 'builder/fym_fix_oct25')
from build_accents import measure
from families import read_image
B = sys.argv[1]; DRY = '--dry' in sys.argv; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
M, sets = D['mats'], D['sets']
SP = json.load(open(REPO + 'config/fym-ozark-nov07.json')); SPEC = SP['mats']
src = open(REPO + 'builder/fym_fix_oct25/v92_splash.py').read()
exec(src[src.index('def kmeans_sw'):src.index('tmpl = ')])  # same swatch measure as v92/v94/v95/nov03/nov07
TO = {'teal': 'blue', 'earthy': 'dark', 'brown': 'dark', 'gold': 'yellow'}
TAG = 'nov07-ozark'
IMG = {}; CH = []; colour_mats = {}; added = []; fixed = []
mcb = re.search(r'MCB=new Set\(\[([0-9, ]+)\]\);', h); chunk = max(int(v) for v in mcb.group(1).split(',')) + 1
maxN = max(int(o['f'].split('/')[1].split('.')[0]) for o in M.values() if str(o.get('f', '')).startswith('m/'))
chunk = max(chunk, maxN // 12 + 1); n0 = chunk * 12
for x in SPEC:
    key = x['key']
    if key in M: continue
    im = Image.open(REPO + x['img']).convert('RGB'); im.thumbnail((640, 640)); b = io.BytesIO(); im.save(b, 'WEBP', quality=86, method=6)
    f = f'm/{n0 + len(CH)}.webp'; CH.append((f, b.getvalue()))
    path = tempfile.mktemp(suffix='.png'); im.save(path)
    t = im.copy(); t.thumbnail((150, 150)); bb = io.BytesIO(); t.save(bb, 'JPEG', quality=72)
    th = 'mo07' + hashlib.md5(key.encode()).hexdigest()[:8]; IMG[th] = 'data:image/jpeg;base64,' + base64.b64encode(bb.getvalue()).decode()
    sh = {}
    for fam, p in measure(path): fam = TO.get(fam, fam); sh[fam] = sh.get(fam, 0) + p
    fams = list(x['mf'])  # by eye (looked at on assets/qa/ozark-nov07/adds.jpg)
    o = dict(n=x['name'], bn=x['brand'], b=x['b'], u=x['u'], u0=x['u'], dc='', pa=False, nc=False, rt=False, c=False, ml=False,
             f=f, th=th, w=im.width, h=im.height, ms=kmeans_sw(im), src='ozark-nov07', add=TAG, ncn=1)
    if x['hol']: o.update(mf=[], mt=[], sh=[], ha=fams, hol=True)
    else: o.update(mf=fams, mt=list(range(len(fams))), sh=[round(sh.get(c, 0), 1) for c in fams], hol=False)
    if x.get('oos'): o['oos'] = 1
    if x['hid']: o['hid'] = True
    M[key] = o; D['order'].append(key)
    added.append((x['name'], f"${x['price']:.0f}", 'sold out' if x.get('oos') else 'in stock', 'HIDDEN+Questionable' if x['hid'] else 'visible', fams))
    _, tone, _ = read_image(path); colour_mats[key] = {'sw': o['ms'], 'tone': tone}; os.remove(path)
# existing Ozark mats: real-domain links + sold out
for k, sl in SP['existing'].items():
    if k not in M: continue
    u = f"{SP['store']}/product-page/{sl}"
    o = M[k]
    if o.get('u') != u or o.get('u0') != u:
        o['u'] = o['u0'] = u; o['dc'] = ''; o['pa'] = False; o.pop('u_dead', None); o.pop('u_plain', None); fixed.append(('link', o['n'], u))
    if not o.get('oos'): o['oos'] = 1; fixed.append(('sold out', o['n']))
# Table view class for the new visible mats (flat top-down store photo cropped to the mat)
TV = D.get('tv')
if TV is not None:
    TV.setdefault('cls', {}); TV.setdefault('why', {})
    for x in SPEC:
        if x.get('tableview') and not x['hid'] and x['key'] in M:
            TV['cls'][x['key']] = x['tableview']; TV['why'].pop(x['key'], None)
ix = {m: j for j, m in enumerate(D['order'])}
newm = [ix[k] for k in M if M[k].get('add') == TAG]
for s in sets:
    if 'rank' in s:
        for j in newm:
            if j not in s['rank']: s['rank'].append(j)
CHUNKS = sorted({int(f.split('/')[1].split('.')[0]) // 12 for f, _ in CH})  # page loads chunk n//12 (MCN=12)
os.makedirs(f'{B}/mc', exist_ok=True)
for c in CHUNKS:
    body, hdr = b'', {}
    for f, raw in CH:
        if int(f.split('/')[1].split('.')[0]) // 12 == c: hdr[f] = [len(body), len(raw)]; body += raw
    hj = json.dumps(hdr, separators=(',', ':')).encode(); open(f'{B}/mc/{c}.webp', 'wb').write(body + hj + struct.pack('<I', len(hj)))
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
if CH: h = h.replace(mcb.group(0), 'MCB=new Set([' + mcb.group(1) + ''.join(f', {c}' for c in CHUNKS) + ']);', 1)
if IMG:
    inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMG, separators=(',', ':')) + ');</script>'
    a = '<script src="b24v1.js"></script>'
    if h.count(a) != 1: a = re.search(r'<script src="b\d+v\d+\.js"></script>', h).group(0)  # website copy (no b24 tag)
    h = h.replace(a, a + inl, 1)
open(P, 'w').write(h)
if not DRY:  # repo-side records (idempotent)
    C = json.load(open(REPO + 'config/fym-colour-oct25.json')); C['mats'].update(colour_mats)
    json.dump(C, open(REPO + 'config/fym-colour-oct25.json', 'w'), indent=0, ensure_ascii=False)
    FL = json.load(open(REPO + 'builder/fym_flags/mat_photo_flags.json'))
    Q = json.load(open(REPO + 'builder/fym_flags/fym_questionable.json')); qk = {it['key'] for it in Q['items']}
    LK = json.load(open(REPO + 'builder/fym_flags/locks.json'))
    for x in SPEC:
        FL[x['key']] = {'name': x['name'], 'brand': x['brand'], 'flag': 'questionable' if x['hid'] else 'ok',
                        'note': 'Nov 7 Ozark add: ' + (x['reason'] if x['hid'] else x['photo_note'] + ', colours clear')}
        if x['hid'] and x['key'] not in qk:
            Q['items'].append({'key': x['key'], 'img': M[x['key']]['f'] if x['key'] in M else '', 'name': x['name'], 'brand': x['brand'],
                               'reason': x['reason'], 'photo': x['img'], 'added': '2026-11-07'})
        if x['key'] in M:
            o = M[x['key']]; LK['mats'][x['key']] = {k: o.get(k) for k in ('n', 'bn', 'f', 'th', 'rt', 'mf', 'mt')}; LK['mats'][x['key']]['hid'] = bool(o.get('hid'))
    json.dump(FL, open(REPO + 'builder/fym_flags/mat_photo_flags.json', 'w'), indent=1, ensure_ascii=False)
    json.dump(Q, open(REPO + 'builder/fym_flags/fym_questionable.json', 'w'), indent=1, ensure_ascii=False)
    json.dump(LK, open(REPO + 'builder/fym_flags/locks.json', 'w'), indent=1, ensure_ascii=False)
for a_ in added: print(*a_)
for f_ in fixed: print('fix', *f_)
print('ozark_v119: chunks', CHUNKS, 'mats', len(added), 'fixes', len(fixed), '(dry: no repo records)' if DRY else '')
