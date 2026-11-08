"""FYM 1.18: partner mats the missing-mat gate [100] found (partner mat sweep, live since Nov 5). Standing authority: catalog adds that
pass the gates. Photos = the brands' flat product renders (assets/mats/partner-nov07/, LOOKED at Nov 7: whole mat, colours clear).
  Mahj Mood | Playing For Keeps (pre-order, ships January): pink retro hearts, mint accents -> pink, green. Partner code link (auto-apply).
  Fait à Main | Texas Mon Amour Green: green bandana, pink hearts/paisley, white line work -> green, pink, neutral. Same link/no-code
  treatment as the other Texas Mon Amour colourways already in FYM (Peach / Cream / Chocolate Blue).
Each mat copies its link/code fields from a sibling mat of the same brand already in the build; new packed chunk + inline thumb (like
shopmy_nov07.py); appended to D.order + every set's rank (builder/fym_fix_oct30/v104rank.py then colour-ranks them, gate [107]).
The two Mac + Miller 'Perfectly Imperfect' listings are seconds (sale) copies of designs already in FYM: listed in
config/partner-mat-sweep-ignore.json with that reason (by fixes118.py), not added.
Idempotent. Usage: python3 builder/fym_fix_nov07/partner_adds118.py <build dir>"""
import sys, os, io, json, base64, hashlib, re, struct
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
from skimage.color import rgb2lab, lab2rgb
import tempfile
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
M = D['mats']
src = open(REPO + 'builder/fym_fix_oct25/v92_splash.py').read()
exec(src[src.index('def kmeans_sw'):src.index('tmpl = ')])
sys.path.insert(0, REPO + 'scripts/colors'); sys.path.insert(0, REPO + 'builder/fym_fix_oct25'); from families import read_image
colour_mats = {}
TAG = 'nov07-partners'
SPEC = [
    dict(key='mahjmood.com/playing-for-keeps-mat', n='Playing For Keeps', sib='mahjmood.com/90s-girl-mat', img='assets/mats/partner-nov07/mahj-mood-playing-for-keeps.jpg',
         mf=['pink', 'green'], sh=[78.0, 12.0], handle='playing-for-keeps-mat', host='mahjmood.com'),
    dict(key='faitamainstudio.com/texas-mon-amour-mat-green', n='Texas Mon Amour Green', sib='faitamainstudio.com/texas-mon-amour-mat-peach',
         img='assets/mats/partner-nov07/fait-a-main-texas-mon-amour-green.jpg', mf=['green', 'pink', 'neutral'], sh=[70.0, 12.0, 10.0],
         handle='texas-mon-amour-mat-green', host='faitamainstudio.com'),
]
IMG, CH, added = {}, [], []
mcb = re.search(r'MCB=new Set\(\[([0-9, ]+)\]\);', h); chunk = max(int(v) for v in mcb.group(1).split(',')) + 1
maxN = max(int(o['f'].split('/')[1].split('.')[0]) for o in M.values() if str(o.get('f', '')).startswith('m/'))
chunk = max(chunk, maxN // 12 + 1); n0 = chunk * 12
for x in SPEC:
    if x['key'] in M: continue
    sib = M[x['sib']]
    im = Image.open(REPO + x['img']).convert('RGB'); im.thumbnail((640, 640)); b = io.BytesIO(); im.save(b, 'WEBP', quality=86, method=6)
    f = f'm/{n0 + len(CH)}.webp'; CH.append((f, b.getvalue()))
    t = im.copy(); t.thumbnail((150, 150)); bb = io.BytesIO(); t.save(bb, 'JPEG', quality=72)
    th = 'mp07' + hashlib.md5(x['key'].encode()).hexdigest()[:8]; IMG[th] = 'data:image/jpeg;base64,' + base64.b64encode(bb.getvalue()).decode()
    plain = f"https://{x['host']}/products/{x['handle']}"
    u = sib['u'].replace(sib['u0'].split('/products/')[1], x['handle']) if sib.get('u0') and '/products/' in sib['u0'] and sib['u0'].split('/products/')[1] in sib['u'] else plain
    if '/discount/' in sib['u']: u = re.sub(r'redirect=[^&]*', 'redirect=%2Fproducts%2F' + x['handle'], sib['u'])
    o = {k: sib[k] for k in ('bn', 'b', 'dc', 'pa', 'nc', 'ncn') if k in sib}
    o.update(n=x['n'], u=u, u0=plain, rt=False, c=False, ml=False, f=f, th=th, w=im.width, h=im.height, ms=kmeans_sw(im),
             mf=x['mf'], mt=list(range(len(x['mf']))), sh=x['sh'], hol=False, src='partner-sweep-nov07', add=TAG)
    tp = tempfile.mktemp(suffix='.png'); im.save(tp); _, tone, _ = read_image(tp); os.remove(tp); colour_mats[x['key']] = {'sw': o['ms'], 'tone': tone}
    M[x['key']] = o; D['order'].append(x['key']); added.append((o['bn'], o['n'], o['u']))
ix = {m: j for j, m in enumerate(D['order'])}
newm = [ix[k] for k in M if M[k].get('add') == TAG]
for s in D['sets']:
    if 'rank' in s:
        for j in newm:
            if j not in s['rank']: s['rank'].append(j)
CHUNKS = sorted({int(f.split('/')[1].split('.')[0]) // 12 for f, _ in CH})
for c in CHUNKS:
    body, hdr = b'', {}
    for f, raw in CH:
        if int(f.split('/')[1].split('.')[0]) // 12 == c: hdr[f] = [len(body), len(raw)]; body += raw
    hj = json.dumps(hdr, separators=(',', ':')).encode(); open(f'{B}/mc/{c}.webp', 'wb').write(body + hj + struct.pack('<I', len(hj)))
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
if CH: h = h.replace(mcb.group(0), 'MCB=new Set([' + mcb.group(1) + ''.join(f', {c}' for c in CHUNKS) + ']);', 1)
if IMG:
    a = '<script src="b24v1.js"></script>'
    if h.count(a) != 1: a = re.search(r'<script src="b\d+v\d+\.js"></script>', h).group(0)
    h = h.replace(a, a + '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMG, separators=(',', ':')) + ');</script>', 1)
open(P, 'w').write(h)
# repo records: measured swatches for the colour ranking (like shopmy_nov07.py) + photo flags ok (idempotent)
C = json.load(open(REPO + 'config/fym-colour-oct25.json')); C['mats'].update(colour_mats)
json.dump(C, open(REPO + 'config/fym-colour-oct25.json', 'w'), indent=0, ensure_ascii=False)
FL = json.load(open(REPO + 'builder/fym_flags/mat_photo_flags.json'))
for x in SPEC:
    FL.setdefault(x['key'], {'name': x['n'], 'brand': M[x['key']]['bn'], 'flag': 'ok', 'note': 'Nov 7 partner sweep add (gate [100]): brand flat render, whole mat, colours clear (LOOKED at)'})
json.dump(FL, open(REPO + 'builder/fym_flags/mat_photo_flags.json', 'w'), indent=1, ensure_ascii=False)
for a_ in added: print('added', *a_)
print('partner_adds118: chunks', CHUNKS, 'mats', len(added))
