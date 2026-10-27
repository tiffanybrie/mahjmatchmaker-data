"""FYM v101 = public "Version 1.5": partner mats the store sweep found missing (Tiffany Oct 27 2:21am: "This is going to get very
old, me chasing down mats") + the Peace Love Mahjong Spirit of Christmas tile set (sold out, still listed = NOT retired).
Spec: config/fym-partner-adds-oct27.json. Mats follow v95_etsy.py (new packed chunk mc/<n>.webp, inline thumb, colours measured
with build_accents.measure, appended to D.order + every set's rank); Bespoke double-sided = two entries (side B '#side-b', right
after side A in rank/cr, same link + code, gate [78]); TdT Domino Faded Carolina + Oxblood (already in FYM under album keys) get
the TdT partner link + code like every other TdT mat. Tile set: brand listing photo (faces + a back), Holiday tile group,
s.sb = her Spirit swipe book (all 10 PLM holiday mats hearted), m in her staged album order with the album card mat racks,
D.ltc = her holiday-picker tile racks, T.so = sold out -> shop list button reads 'Sold out' + tile list says 'sold out'.
Writes mat_photo_flags (ok / questionable), the Questionable list, locks, swipe_yeses_map, display names, fym-colour records.
Idempotent. Usage: python3 v101_partneradds.py <build_dir>"""
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
T, M, R, sets = D['tiles'], D['mats'], D['racks'], D['sets']
SPEC = json.load(open(REPO + 'config/fym-partner-adds-oct27.json'))
src = open(REPO + 'builder/fym_fix_oct25/v92_splash.py').read()
exec(src[src.index('def kmeans_sw'):src.index('tmpl = ')])  # same swatch measure as v92/v94/v95
TO = {'teal': 'blue', 'earthy': 'dark', 'brown': 'dark', 'gold': 'yellow'}
ADD = 'oct27-v101'
IMG = {}; CH = []; colour_mats = {}; colour_sets = {}; added = []

# 1. TdT mats already in FYM under album keys: partner link + code like the other TdT mats (TdT is a partner: MAHJMATCH)
TDT_REF = '11798386.tvil8GTGTp6s2'
for k, x in SPEC['already_in_fym'].items():
    o = M.get(k)
    if not o or not k.startswith('alb2:tigre'): continue
    hd = x['handle']
    o.update(b='tigredetartan.com', u=f'https://tigredetartan.com/discount/MAHJMATCH?redirect=%2Fproducts%2F{hd}%3Fsca_ref%3D{TDT_REF}',
             u0=f'https://tigredetartan.com/products/{hd}?sca_ref={TDT_REF}', dc='https://mahjmatchmaker.com/tigre-de-tartan-discount-code', pa=True)
    added.append(('relink', o['bn'], o['n']))

# 1b. Britt Mills leatherette versions of neoprene mats already in FYM: the neoprene entry says 'Also available in leatherette' and the
#     leatherette gets its own entry below (spec copy_colours_from), the same precedent as Legacy / Quinn / Eden / Novella
for k in SPEC.get('alt_leatherette', {}).get('mats', {}):
    if k in M and not M[k].get('alt'): M[k]['alt'] = 'Also available in leatherette'; added.append(('alt', 'Britt Mills', M[k]['n'], 'also in leatherette'))
# 2. new mats
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
    th = 'm101' + hashlib.md5(key.encode()).hexdigest()[:8]; IMG[th] = 'data:image/jpeg;base64,' + base64.b64encode(bb.getvalue()).decode()
    sh = {}
    for fam, p in measure(path): fam = TO.get(fam, fam); sh[fam] = sh.get(fam, 0) + p
    fams = [c for c, p in sorted(sh.items(), key=lambda kv: -kv[1]) if p >= 8][:4] or [max(sh, key=sh.get)]
    if x.get('colors'): fams = list(x['colors'])  # eye call where the photo's props skew the measure (tile pile, racks)
    if x.get('primary'):
        if x['primary'] in fams: fams.remove(x['primary'])
        fams.insert(0, x['primary'])
    o = dict(n=x['name'], bn=x['bn'], b=x['b'], u=x['u'], u0=x['u0'], dc=x['dc'], pa=x['pa'], nc=False, rt=False, c=False, ml=False,
             f=f, th=th, w=im.width, h=im.height, ms=kmeans_sw(im), src='partner-sweep-oct27', add=ADD)
    if x['hol']: o.update(mf=[], mt=[], sh=[], ha=fams, hol=True)
    else: o.update(mf=fams, mt=list(range(len(fams))), sh=[round(sh.get(c, 0), 1) for c in fams], hol=False)
    if x.get('copy_colours_from') and x['copy_colours_from'] in M:  # same design, other material: same colours as its twin
        tw = M[x['copy_colours_from']]; o.update({k_: json.loads(json.dumps(tw[k_])) for k_ in ('mf', 'mt', 'sh', 'ha', 'hol') if k_ in tw})
        fams = o.get('mf') or o.get('ha') or []
    if x.get('dn'): o['dn'] = x['dn']
    if x.get('side'):
        o['side'] = x['side']; ka = key.split('#')[0]; o['twin'] = ka + '#side-b' if x['side'] == 'A' else ka
    if x['hid']: o['hid'] = True
    M[key] = o; D['order'].append(key)
    added.append(('mat', x['bn'], x['name'], 'HIDDEN' if x['hid'] else 'visible', fams))
    _, tone, _ = read_image(path); colour_mats[key] = {'sw': o['ms'], 'tone': tone}; os.remove(path)
ix = {m: j for j, m in enumerate(D['order'])}
newm = [ix[k] for k in M if M[k].get('add') == ADD]
pairs = [(ix[k.split('#')[0]], ix[k]) for k in M if M[k].get('add') == ADD and k.endswith('#side-b') and k.split('#')[0] in ix]
for s in sets:
    for fld in ('rank', 'cr'):
        if fld not in s: continue
        L = s[fld]
        if fld == 'rank':
            for j in newm:
                if j not in L: L.append(j)
        for ja, jb in pairs:  # side B right after side A (gate [78])
            if ja in L:
                if jb in L: L.remove(jb)
                L.insert(L.index(ja) + 1, jb)

# 3. Spirit of Christmas tile set
os.makedirs(B + '/t101', exist_ok=True)
MAN = json.load(open(REPO + 'assets/cards/spirit-of-christmas-oct20/manifest.json'))
HPP = json.load(open(REPO + 'config/holiday-picker-picks.json'))
rk_by_name = {r['n']: k for k, r in R.items() if not r.get('hid')}
plm_hol = {o['n']: k for k, o in M.items() if k.startswith('peacelovemahjong.com/mahjong-mats-holiday?v=') and not o.get('hid')}
LM = D.get('lm') or {}
for x in SPEC['tiles']:
    key, slug = x['key'], x['slug']
    im = Image.open(REPO + x['img']).convert('RGB'); fn = f't101/{slug}.jpg'; im.save(f'{B}/{fn}', quality=88)
    S_ = min(im.size); sq = im.crop(((im.width - S_) // 2, 0, (im.width - S_) // 2 + S_, S_)).resize((360, 360), Image.LANCZOS)
    pk = 'p101' + hashlib.md5(slug.encode()).hexdigest()[:10]; b = io.BytesIO(); sq.save(b, 'JPEG', quality=84)
    IMG[pk] = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
    T[key] = dict(full=fn, n=x['name'], bn=x['bn'], u=x['u'], dc=x['dc'], pa=x['pa'], nc=False, rt=False, pile=pk, src=x['img'], u0=x['u0'], so=1, add=ADD)
    m = []
    for c in sorted(MAN['cards'], key=lambda c: c['order']):
        mk = plm_hol.get(c['mat'])
        if not mk: print('UNRESOLVED mat', c['mat']); continue
        racks = list(LM.get(mk) or [])
        for rn in c['mat_racks']:
            rk = rk_by_name.get(rn)
            if rk and rk not in racks: racks.append(rk)
            elif not rk: print('UNRESOLVED rack', rn)
        m.append([mk, racks])
    s = next((y for y in sets if y['slug'] == slug), None)
    if s is None:
        tmpl = next(y for y in sets if y['slug'] == 'dear-santa')
        s = dict(slug=slug, name=x['name'], maker=x['bn'], tile=key, tc=x['tc'], tag='', album='', rank=list(tmpl['rank']), m=[], cr=[])
        sets.append(s)
        for j in newm:
            if j not in s['rank']: s['rank'].append(j)
    s.update(name=x['name'], maker=x['bn'], tile=key, tc=x['tc'], sb=True, m=m)
    D['ltc'][slug] = HPP[slug]['picks']
    added.append(('tiles', x['bn'], x['name'], f'{len(m)} picks', 'sold out'))
    a = np.asarray(im.resize((120, 100))).astype(float).reshape(-1, 3) / 255; a = a[~(a.min(1) > .82)]
    L = rgb2lab(a.reshape(-1, 1, 3)).reshape(-1, 3); km = KMeans(n_clusters=6, n_init=3, random_state=0).fit(L)
    cnt = np.bincount(km.labels_, minlength=6) / len(L); sw = []
    for j in np.argsort(-cnt):
        if cnt[j] < .05: continue
        rgb = np.clip(lab2rgb(km.cluster_centers_[j].reshape(1, 1, 3)).reshape(3), 0, 1)
        sw.append(['#%02x%02x%02x' % tuple(int(round(v * 255)) for v in rgb), round(float(cnt[j]), 3)])
    colour_sets[slug] = {'sw': sw, 'tone': 'clean', 'src': 'photo', 'back': None}

# write chunks + D
CHUNKS = sorted({int(f.split('/')[1].split('.')[0]) // 12 for f, _ in CH})  # page loads chunk n//12 (MCN=12)
for c in CHUNKS:
    body, hdr = b'', {}
    for f, raw in CH:
        if int(f.split('/')[1].split('.')[0]) // 12 == c: hdr[f] = [len(body), len(raw)]; body += raw
    hj = json.dumps(hdr, separators=(',', ':')).encode(); open(f'{B}/mc/{c}.webp', 'wb').write(body + hj + struct.pack('<I', len(hj)))
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
if CH: h = h.replace(mcb.group(0), 'MCB=new Set([' + mcb.group(1) + ''.join(f', {c}' for c in CHUNKS) + ']);', 1)
j = h.index('const BACKG=') + len('const BACKG='); BG, bend = json.JSONDecoder().raw_decode(h[j:]); bend += j
for x in SPEC['tiles']:
    if x['name'] not in BG[x['group']]: BG[x['group']].append(x['name'])
h = h[:j] + json.dumps(BG, ensure_ascii=False) + h[bend:]
# sold out (T.so): shop list button + tile list label. Sold out != retired (config/tile-retired.json rule)
if '/*v101 sold out*/' not in h:
    a = "${o.rt?'Retired':'Shop ›'}"; assert h.count(a) == 1, h.count(a)
    h = h.replace(a, "${o.rt?'Retired':(o.so?'Sold out ›':'Shop ›')/*v101 sold out*/}", 1)
    a = "<small>${esc(s.maker)}</small>"; n_ = h.count(a); assert n_ >= 1
    h = h.replace(a, "<small>${esc(s.maker)}${(T[s.tile]||{}).so?' · sold out':''}</small>")
if IMG:
    inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMG, separators=(',', ':')) + ');</script>'
    a = '<script src="b24v1.js"></script>'; assert h.count(a) == 1; h = h.replace(a, a + inl, 1)
open(P, 'w').write(h)

# colour ranking (s.cr) for the new tile set: v85_colorrank on a scratch copy, copy back only that set's cr (as v94)
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
Q = json.load(open(REPO + 'builder/fym_flags/fym_questionable.json')); qk = {it['key'] for it in Q['items']}
LK = json.load(open(REPO + 'builder/fym_flags/locks.json'))
for x in SPEC['mats']:
    FL[x['key']] = {'name': x['name'], 'brand': x['bn'], 'flag': 'questionable' if x['hid'] else 'ok',
                    'note': 'Oct 27 partner sweep add (v101): ' + (x.get('reason') or x.get('photo_note', ''))}
    if x['hid'] and x['key'] not in qk:
        Q['items'].append({'key': x['key'], 'img': M[x['key']]['f'], 'name': x['name'], 'brand': x['bn'], 'reason': x['reason'], 'photo': x['img'], 'added': '2026-10-27'})
    o = M[x['key']]
    LK['mats'][x['key']] = {k: o.get(k) for k in ('n', 'bn', 'f', 'th', 'rt', 'hid', 'mf', 'mt')}; LK['mats'][x['key']]['hid'] = bool(o.get('hid'))
TF = json.load(open(REPO + 'builder/fym_flags/tile_photo_flags.json'))
for x in SPEC['tiles']:
    t = T[x['key']]; s = next(y for y in sets if y['slug'] == x['slug'])
    LK['tiles'][x['key']] = {'set': x['name'], 'src': x['img'], 'full': t['full'], 'pile': t['pile']}
    LK['sets'][x['slug']] = {'m': s['m'], 'sb': True, 'name': x['name']}
    TF[x['slug']] = {'flag': 'ok', 'note': 'Oct 27 v101: ' + x['photo_note']}
    SY = json.load(open(REPO + 'builder/fym_flags/swipe_yeses_map.json')); SY[x['slug']] = [e[0] for e in s['m']]
    json.dump(SY, open(REPO + 'builder/fym_flags/swipe_yeses_map.json', 'w'), indent=1, ensure_ascii=False)
LK.setdefault('_changes', []) if isinstance(LK.get('_changes'), list) else None
if isinstance(LK.get('_changes'), list) and not any('v101' in str(c) for c in LK['_changes']):
    LK['_changes'].append('2026-10-27 v101: partner sweep mats (Britt Mills House Print, TdT Domino Blonde + Estate Sale + Fair Isle Cashmere (hidden), Bespoke x Brooks Brothers Oxford Classic A/B, PLM Vegan Leather x4) + Spirit of Christmas tile set (her Spirit swipe book picks)')
DN = json.load(open(REPO + 'config/fym-mat-display-names-oct26.json'))
for x in SPEC['mats']:
    if x.get('dn'): DN['dn'][x['key']] = x['dn']
json.dump(DN, open(REPO + 'config/fym-mat-display-names-oct26.json', 'w'), indent=1, ensure_ascii=False)
json.dump(FL, open(REPO + 'builder/fym_flags/mat_photo_flags.json', 'w'), indent=1, ensure_ascii=False)
json.dump(Q, open(REPO + 'builder/fym_flags/fym_questionable.json', 'w'), indent=1, ensure_ascii=False)
json.dump(LK, open(REPO + 'builder/fym_flags/locks.json', 'w'), indent=1, ensure_ascii=False)
json.dump(TF, open(REPO + 'builder/fym_flags/tile_photo_flags.json', 'w'), indent=1, ensure_ascii=False)
for a_ in added: print(*a_)
print('chunks', CHUNKS, 'items', len(added))
