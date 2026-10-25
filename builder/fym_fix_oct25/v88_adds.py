"""FYM v88: partner catalog audit adds + fixes (Tiffany Oct 25 15:24: "I want everything checked across all the partner brands").
Source: docs/catalog-audit-oct25.md (+ config/catalog-audit-oct25-missing.json); photos picked by eye per item into
<scratch>/v88spec/spec.json + img/ (independent agent, contact sheets). In-stock (or pre-order) items only.
Skipped on purpose: Mahjong Studios 'All In One' (= Essential set in a bundle), Bird & Bamboo 19" (size option of racks already in),
Splash of Color / Let's Be Besties (awaiting Tiffany), Britt Mills leatherette re-issues of designs already in.
Fixes: My Fair Mahjong wooden racks relinked to /products/wooden-racks (old URL 301s) + Macaron Purple colour fixed + Natural Wood added;
unhide in-stock items hidden by Oct 18 positional scripts with no recorded reason (TdT tortoise rack, 5 Bird & Bamboo wood stains,
Bam black wooden racks) and the 5 Mac + Miller mats locked hidden while 'Coming Soon' (now in stock).
Usage: python3 v88_adds.py <build_dir> <spec_dir>"""
import sys, os, io, json, base64, hashlib, re, struct
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
from skimage.color import rgb2lab, lab2rgb
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
sys.path.insert(0, REPO + 'scripts/colors')
from build_accents import measure
from families import read_image
B, SP = sys.argv[1], sys.argv[2]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
T, R, M, sets = D['tiles'], D['racks'], D['mats'], D['sets']
SPEC = json.load(open(SP + '/spec.json'))
SKIP = {('Mahjong Studios', 'All In One (Essential)'), ('Bird & Bamboo', 'Bird & Bamboo 19" Painted Wood')}
BN = {'The Royal Mahjong Society': 'Royal Mahjong Society'}
def kmeans_sw(im, k=8, minw=.03, faces=False):
    a = np.asarray(im.convert('RGB').resize((72, 72))).astype(float).reshape(-1, 3) / 255
    a = a[~((a.min(1) > .82) & (a.max(1) - a.min(1) < .12))] if faces else a[~(a.min(1) > .94)]
    if len(a) < 50: return []
    L = rgb2lab(a.reshape(-1, 1, 3)).reshape(-1, 3); km = KMeans(n_clusters=k, n_init=3, random_state=0).fit(L)
    cnt = np.bincount(km.labels_, minlength=k) / len(L); out = []
    for j in np.argsort(-cnt):
        if cnt[j] < minw: continue
        rgb = np.clip(lab2rgb(km.cluster_centers_[j].reshape(1, 1, 3)).reshape(3), 0, 1)
        out.append(['#%02x%02x%02x' % tuple(int(round(x * 255)) for x in rgb), round(float(cnt[j]), 3)])
    return out
def example(bn):
    for kind in ('tiles', 'mats', 'racks'):
        for k, v in D[kind].items():
            if v.get('bn') == bn and v.get('u') and v.get('pa') and ('%2Fproducts%2F' in v['u'] or '/products/' in v['u']): return v
    raise SystemExit('no link template for ' + bn)
def link(bn, handle, variant=None):
    v = example(bn); u = v['u']
    if '%2Fproducts%2F' in u:
        u = re.sub(r'%2Fproducts%2F[^%&]+(%3Fvariant%3D\d+)?', '%2Fproducts%2F' + handle + (f'%3Fvariant%3D{variant}' if variant else ''), u, count=1)
        if variant and '%3Fvariant%3D' in u and '%3Fsca_ref' in u: u = u.replace('%3Fsca_ref', '%26sca_ref')
    else:
        u = re.sub(r'/products/[^?&#]+', '/products/' + handle, u, count=1)
        if variant: u = u.split('?')[0] + f'?variant={variant}' + ('&' + u.split('?', 1)[1] if '?' in u else '')
    return u, v.get('dc', '')
def host(url): return url.split('//')[1].split('/')[0]
IMG = {}; groups = {}; added = []; colour_sets = {}; colour_mats = {}
os.makedirs(B + '/t88', exist_ok=True)
tmpl_s = next(s for s in sets if s.get('cat') and not s['m'])
def thumb(im, key, sz=360):
    w, hh = im.size; q = min(w, hh); pp = im.crop(((w - q) // 2, (hh - q) // 2, (w - q) // 2 + q, (hh - q) // 2 + q)).resize((sz, sz), Image.LANCZOS)
    b = io.BytesIO(); pp.save(b, 'JPEG', quality=84); IMG[key] = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
# ---- tiles
for x in SPEC['tiles']:
    bn = BN.get(x['brand'], x['brand'])
    if (bn, x['name']) in SKIP or (x['brand'], x['name']) in SKIP: continue
    key = host(x['product_url']) + '/' + x['handle'] + (f"?v={x['variant_id']}" if x.get('variant_id') else '')
    if key in T and not T[key].get('hid'): continue
    u, dc = link(bn, x['handle'], x.get('variant_id'))
    im = Image.open(SP + '/' + x['img']).convert('RGB'); slug = re.sub(r'[^a-z0-9]+', '-', (bn + ' ' + x['name']).lower()).strip('-')[:80]
    full = im.copy(); full.thumbnail((1000, 1000)); fn = f't88/{slug}.jpg'; full.save(f'{B}/{fn}', quality=88)
    pk = 'p88' + hashlib.md5(slug.encode()).hexdigest()[:10]; thumb(im, pk)
    T[key] = dict(n=x['name'], bn=bn, full=fn, pile=pk, u=u, u0=x['product_url'], dc=dc, pa=True, nc=False, rt=False, cat=True, add='oct25-audit',
                  **({'pre': 1} if x.get('pre_order') else {}))
    s = next((y for y in sets if y['tile'] == key), None)
    if s is None: s = dict(tmpl_s); s.update(slug=slug, tile=key, m=[], album='', tag='', cat=True); s.pop('cr', None); sets.append(s)
    s.update(name=x['name'], maker=bn, tc=x['tc']); s.pop('hid', None)
    groups.setdefault(x['group'], []).append(x['name']); added.append(('tile', bn, x['name']))
    colour_sets[s['slug']] = {'sw': kmeans_sw(im, 6, .05, faces=True), 'tone': None, 'src': 'photo', 'back': None}
# ---- mats (new image chunk)
mcb = re.search(r'MCB=new Set\(\[([0-9, ]+)\]\);', h); chunk = max(int(v) for v in mcb.group(1).split(',')) + 1
maxN = max(int(o['f'].split('/')[1].split('.')[0]) for o in M.values()); chunk = max(chunk, maxN // 12 + 1); n0 = chunk * 12; CH = []
TO = {'teal': 'blue', 'earthy': 'dark', 'brown': 'dark', 'gold': 'yellow'}
for x in SPEC['mats']:
    bn = BN.get(x['brand'], x['brand'])
    key = host(x['product_url']) + '/' + x['handle'] + (f"?v={x['variant_id']}" if x.get('variant_id') else '')
    if key in M and not M[key].get('hid'): continue
    im = Image.open(SP + '/' + x['img']).convert('RGB')
    if 'Emerald Mirage' in x['name'] and im.size[0] >= 3000: im = im.crop((737, 690, 2993, 2946))
    im.thumbnail((640, 640)); b = io.BytesIO(); im.save(b, 'WEBP', quality=86, method=6)
    f = f'm/{n0 + len(CH)}.webp'; CH.append((f, b.getvalue()))
    path = f'/tmp/v88_{len(CH)}.png'; im.save(path)
    t = im.copy(); t.thumbnail((150, 150)); bb = io.BytesIO(); t.save(bb, 'JPEG', quality=72)
    th = 'm8' + hashlib.md5(key.encode()).hexdigest()[:8]; IMG[th] = 'data:image/jpeg;base64,' + base64.b64encode(bb.getvalue()).decode()
    sh = {}
    for fam, p in measure(path): fam = TO.get(fam, fam); sh[fam] = sh.get(fam, 0) + p
    u, dc = link(bn, x['handle'], x.get('variant_id'))
    if bn == 'Wren Mats': u = x['product_url']  # Squarespace shop: product URL is /mats/p/<slug>
    hol = bool(x.get('holiday')); cols = list(x['colors'])
    o = dict(n=x['name'], bn=bn, b=bn, u=u, u0=x['product_url'], dc=dc, pa=True, nc=False, rt=False, c=False, ml=False, f=f, th=th, w=im.width, h=im.height,
             mf=[] if hol else cols, mt=[] if hol else [0] + [1] * (len(cols) - 1), sh=[] if hol else [round(sh.get(c, 0), 1) for c in cols],
             ms=kmeans_sw(im), hol=hol, src='audit-oct25', add='oct25-audit')
    if hol: o['ha'] = cols
    M[key] = o; D['order'].append(key); added.append(('mat', bn, x['name']))
    _, tone, _ = read_image(path); colour_mats[key] = {'sw': o['ms'], 'tone': tone}
ix = {m: j for j, m in enumerate(D['order'])}
for s in sets:
    for k in [k for k in M if M[k].get('add') == 'oct25-audit']:
        if ix[k] not in s['rank']: s['rank'].append(ix[k])
# ---- racks
FIN = json.load(open(REPO + 'config/rack-finishes.json'))
mfm_img = None
for x in SPEC['racks']:
    bn = BN.get(x['brand'], x['brand'])
    if (bn, x['name']) in SKIP: continue
    if bn == 'My Fair Mahjong':  # relink the 5 existing painted-wood racks; add Natural Wood
        old = 'myfairmahjong.com/wooden-painted-mahjong-racks-20-set-of-4-blue-and-pink-sets-magnetic-attached-pusher' + (f"?v={x['variant_id']}" if x.get('variant_id') else '')
        u, dc = link(bn, 'wooden-racks', x.get('variant_id'))
        hit = old if old in R else next((k for k, v in R.items() if v['bn'] == bn and v['n'] == x['name']), None)
        if hit is None and 'Purple' in x['name']: hit = 'myfairmahjong.com/wooden-painted-mahjong-racks-20-set-of-4-blue-and-pink-sets-magnetic-attached-pusher'
        if hit and 'Natural' not in x['name']:
            R[hit]['u'] = u; R[hit]['u0'] = x['product_url']
            if 'Purple' in x['name']: R[hit].update(n='My Fair Mahjong Macaron Purple Wood', hx=x['hx'], rf=['purple'])
            added.append(('rack relink', bn, R[hit]['n'])); continue
    key = host(x['product_url']) + '/' + x['handle'] + (f"?v={x['variant_id']}" if x.get('variant_id') else '')
    if key in R and not R[key].get('hid'): continue
    im = Image.open(SP + '/' + x['img']).convert('RGB')
    if bn == 'My Fair Mahjong' and 'Natural' in x['name']: w, hh = im.size; im = im.crop((int(w * 5 / 6), 0, w, hh))
    rk = 'rk88' + hashlib.md5(key.encode()).hexdigest()[:8]; t = im.copy(); t.thumbnail((700, 700)); bb = io.BytesIO(); t.save(bb, 'JPEG', quality=84)
    IMG[rk] = 'data:image/jpeg;base64,' + base64.b64encode(bb.getvalue()).decode()
    u, dc = link(bn, x['handle'], x.get('variant_id'))
    fam = x['family'] if x['family'] in ('pink', 'red', 'orange', 'yellow', 'green', 'blue', 'purple', 'neutral', 'dark') else 'dark'
    rf = [fam] + (['wood'] if 'natural wood' in x.get('finish', '') else []) + (['tortoise'] if 'tortoise' in x.get('finish', '').lower() and 'not tortoise' not in x.get('finish', '').lower() else [])
    R[key] = dict(n=x['name'], bn=bn, b=bn, u=u, u0=x['product_url'], dc=dc, pa=True, nc=False, rt=False, c=False, ml=False, add='oct25-audit', sk=False, hx=x['hx'], rf=rf, im=rk)
    if 'wood' in rf: FIN['wood'][key] = x['name']
    added.append(('rack', bn, x['name']))
# ---- unhides (audit: in stock, hidden with no recorded reason)
UNHIDE_R = {'tigredetartan.com/february-preorder-tortoise-scalloped-acrylic-mahjong-racks-with-magnetic-pushers-set-of-4-with-dust-bag': ['tortoise'],
            'bb:Almond': ['wood'], 'bb:Weathered Oak': ['wood'], 'bb:Provincial': ['wood'], 'bb:Red Mahogany': ['wood'], 'bb:Dark Walnut': ['wood'],
            'www.bamletsmahjong.com/wooden-mahjong-racks-pushers-black-4-set': []}
for k, fins in UNHIDE_R.items():
    if k in R:
        R[k].pop('hid', None)
        for fn_ in fins:
            if fn_ not in R[k]['rf']: R[k]['rf'] = R[k]['rf'] + [fn_]
            FIN[fn_][k] = R[k]['n']
        added.append(('unhide rack', R[k]['bn'], R[k]['n']))
L = json.load(open(REPO + 'builder/fym_flags/locks.json'))
for k in ['www.macandmillermahjong.com/mg-flower-mat-name-tbd', 'www.macandmillermahjong.com/let-the-good-times-toile-mat',
          'www.macandmillermahjong.com/heirloom-collection-navy-chinoiserie-mahjong-mat', 'www.macandmillermahjong.com/heirloom-fire-fortune-mahjong-mat',
          'www.macandmillermahjong.com/laissez-les-bons-temps-rouler-mahjong-mat-pre-order-ships-march-2026']:
    if k in M:
        M[k].pop('hid', None); M[k]['n'] = M[k]['n'].replace(' (Coming Soon)', '')
        if k in L['mats']: L['mats'][k]['hid'] = False; L['mats'][k]['n'] = M[k]['n']
        added.append(('unhide mat', M[k]['bn'], M[k]['n']))
L.setdefault('_changes', []).append('2026-10-25: 5 Mac + Miller mats unhidden (were locked hidden while Coming Soon; now in stock, partner catalog audit)')
json.dump(L, open(REPO + 'builder/fym_flags/locks.json', 'w'), indent=1, ensure_ascii=False)
json.dump(FIN, open(REPO + 'config/rack-finishes.json', 'w'), indent=1, ensure_ascii=False)
# ---- write
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
inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMG, separators=(',', ':')) + ');</script>'
a = '<script src="b24v1.js"></script>'; assert h.count(a) == 1; h = h.replace(a, a + inl, 1)
open(P, 'w').write(h)
C = json.load(open(REPO + 'config/fym-colour-oct25.json')); C['sets'].update(colour_sets); C['mats'].update(colour_mats)
json.dump(C, open(REPO + 'config/fym-colour-oct25.json', 'w'), indent=0, ensure_ascii=False)
for a_ in added: print(*a_)
print('chunk', chunk if CH else None, 'items', len(added))
