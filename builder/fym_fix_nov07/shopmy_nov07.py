"""FYM 1.18: ShopMy mats found missing by the Nov 7 cross-check (Tiffany 7:45pm "This needs a cross check"; report
config/shopmy-crosscheck-nov07.json, check scripts/checks/shopmy_sync_check.py). Copy of builder/fym_fix_nov03/etsy_shopmy_nov03.py
with the Nov 7 spec config/fym-shopmy-nov07.json (made by prep_shopmy_nov07.py, photos assets/mats/shopmy-nov07/, contact sheet
assets/qa/shopmy-nov07/adds.jpg LOOKED at).
1. Adds the spec mats (new packed mc chunk, inline thumb, measured colours, appended to D.order + every set's rank, like v95/nov03).
   b = the store label from the spec ('Etsy', "Dillard's", 'Case-Mate', ...). Link = her go.shopmy.us link, no code claim
   (dc '', pa False, ncn 1 = 'No code available at this time' like every non-partner, gate [137d]). Holiday mats (Vintage Twinkle):
   mf/mt/sh empty, colours in ha (combo-only), hol True.
2. Fixes: 'hide' = hidden + Questionable (Luna EK Hummingbird Floral Frame (Mint): photo is a different mat);
   'link' = shop-link swap to her ShopMy pin (Mahj & Moon Blue Pastel Palm Beach = her 'Palm Beach Preppy' Etsy pin).
3. Repo records (idempotent): mat_photo_flags, fym_questionable, fym-colour-oct25 swatches, mahj-moon-shopmy-links pairing.
Also run builder/fym_fix_oct25/v96_amazon_holiday.py in the same build (her Oct 26 Amazon holiday picks, never shipped): see adds118.sh.
Usage: python3 builder/fym_fix_nov07/shopmy_nov07.py <build_dir>"""
import sys, os, io, json, base64, hashlib, re, struct, tempfile
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
from skimage.color import rgb2lab, lab2rgb
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
sys.path.insert(0, REPO + 'scripts/colors'); sys.path.insert(0, REPO + 'builder/fym_fix_oct25')
from build_accents import measure
from families import read_image
B = sys.argv[1]; REPO = os.environ.get('FYM_REPO', REPO); P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
M, sets = D['mats'], D['sets']
SP = json.load(open(REPO + 'config/fym-shopmy-nov07.json')); SPEC = SP['mats']; FIX = SP.get('fixes', {})
src = open(REPO + 'builder/fym_fix_oct25/v92_splash.py').read()
exec(src[src.index('def kmeans_sw'):src.index('tmpl = ')])  # same swatch measure as v92/v94/v95/nov03
TO = {'teal': 'blue', 'earthy': 'dark', 'brown': 'dark', 'gold': 'yellow'}
TAG = 'nov07-shopmy'
IMG = {}; CH = []; colour_mats = {}; added = []
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
    th = 'mn07' + hashlib.md5(key.encode()).hexdigest()[:8]; IMG[th] = 'data:image/jpeg;base64,' + base64.b64encode(bb.getvalue()).decode()
    sh = {}
    for fam, p in measure(path): fam = TO.get(fam, fam); sh[fam] = sh.get(fam, 0) + p
    fams = [c for c, p in sorted(sh.items(), key=lambda kv: -kv[1]) if p >= 8][:4] or [max(sh, key=sh.get)]
    if x.get('primary') in fams: fams.remove(x['primary']); fams.insert(0, x['primary'])
    if x.get('mf'): fams = list(x['mf'])  # by-eye colours (spec 'mf', also in config/fym-colour-fixes-v116.json 'eye', gate [163])
    o = dict(n=x['name'], bn=x['brand'], b=x.get('b', 'Etsy'), u=x['u'], u0=x['u'], dc='', pa=False, nc=False, rt=False, c=False, ml=False,
             f=f, th=th, w=im.width, h=im.height, ms=kmeans_sw(im), src='shopmy-nov07', add=TAG, ncn=1)
    if x['hol']: o.update(mf=[], mt=[], sh=[], ha=fams, hol=True)
    else: o.update(mf=fams, mt=list(range(len(fams))), sh=[round(sh.get(c, 0), 1) for c in fams], hol=False)
    if x['hid']: o['hid'] = True
    M[key] = o; D['order'].append(key); added.append((x['brand'], x['name'], 'holiday' if x['hol'] else 'year-round', 'HIDDEN' if x['hid'] else 'visible', fams))
    _, tone, _ = read_image(path); colour_mats[key] = {'sw': o['ms'], 'tone': tone}; os.remove(path)
# fixes on existing mats
fixed = []
for k, v in FIX.get('hide', {}).items():
    if k in M and not M[k].get('hid'): M[k]['hid'] = True; fixed.append(('hide', k))
for k, v in FIX.get('link', {}).items():
    if k in M and M[k].get('u') != v['u']: M[k]['u'] = v['u']; M[k]['u0'] = v['u']; M[k]['dc'] = ''; fixed.append(('link', k))
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
# repo-side records (idempotent)
C = json.load(open(REPO + 'config/fym-colour-oct25.json')); C['mats'].update(colour_mats)
json.dump(C, open(REPO + 'config/fym-colour-oct25.json', 'w'), indent=0, ensure_ascii=False)
FL = json.load(open(REPO + 'builder/fym_flags/mat_photo_flags.json'))
Q = json.load(open(REPO + 'builder/fym_flags/fym_questionable.json')); qk = {it['key'] for it in Q['items']}
for x in SPEC:
    FL[x['key']] = {'name': x['name'], 'brand': x['brand'], 'flag': 'questionable' if x['hid'] else 'ok',
                    'note': 'Nov 7 ShopMy cross-check add: ' + (x['reason'] if x['hid'] else ('cropped to the mat' if x['crop'] else 'brand flat render') + ', colours clear')}
    if x['hid'] and x['key'] not in qk:
        Q['items'].append({'key': x['key'], 'img': M[x['key']]['f'] if x['key'] in M else '', 'name': x['name'], 'brand': x['brand'],
                           'reason': x['reason'], 'photo': x['img'], 'added': '2026-11-07'})
for k, v in FIX.get('hide', {}).items():
    FL[k] = {'name': v['name'], 'brand': v['brand'], 'flag': 'questionable', 'note': 'Nov 7 ShopMy cross-check: ' + v['reason']}
    if k not in qk:
        Q['items'].append({'key': k, 'img': M[k]['f'] if k in M else '', 'name': v['name'], 'brand': v['brand'], 'reason': v['reason'],
                           'photo': 'assets/mats/shopmy-nov03/luna-ek-studio-hummingbird-floral-frame-mint.jpg', 'added': '2026-11-07'})
json.dump(FL, open(REPO + 'builder/fym_flags/mat_photo_flags.json', 'w'), indent=1, ensure_ascii=False)
json.dump(Q, open(REPO + 'builder/fym_flags/fym_questionable.json', 'w'), indent=1, ensure_ascii=False)
L = json.load(open(REPO + 'config/mahj-moon-shopmy-links.json'))
for k, v in FIX.get('link', {}).items():
    if k.startswith('mahjandmoon.com/') and k in L and L[k].get('shopmy_url') != v['u']:
        L[k].update(shopmy_url=v['u'], etsy_url=v['etsy_url'], confidence='high', source='Nov 7 ShopMy cross-check: ' + v['why']); L[k].pop('note', None)
json.dump(L, open(REPO + 'config/mahj-moon-shopmy-links.json', 'w'), indent=1, ensure_ascii=False)
for a_ in added: print(*a_)
for f_ in fixed: print('fix', *f_)
print('chunks', CHUNKS, 'mats', len(added), 'fixes', len(fixed))
