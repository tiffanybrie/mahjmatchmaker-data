"""FYM 1.22.15 adds (Nov 22 2026; copy of builder/fym_fix_nov21/adds12212.py, itself fym_fix_nov17/adds123.py).
Spec = config/fym-prep-nov22/adds/adds.json (prep run, photo-checked). ADDED: Yellow Mountain Imports Koi (Watercolor) + 4 Let's Be
Besties mats. SKIPPED (see SKIP below, coordinator decision Nov 22): the 5 Noli June tile sets, YMI Qilin Kirin, Mahjong Studios Easter Morning. What this copy does that the template did not (config/fym-prep-nov22/adds/notes.md):
 - SKIP: Mahjong Studios Easter Morning is NOT added. Every Mahjong Studios tile set is hidden in the app (Tiffany Oct 26 9:23am, gate [67]
   fails on a visible one); a single new visible Mahjong Studios set would be a new gate problem. Add it when the brand's sets come back.
 - tile photos are copied from the prep folder to assets/tiles/v12215/<slug>.jpg and T.src points there (notes 1).
 - Yellow Mountain Imports: T.code = the YMI code (the match card prints 'Use code ' + T.code), split=1, bf=[.5,.5] (faces|backs split,
   same fields as the 38 existing YMI sets), u_plain; price as the brand's other 41 sets [p, p, 0] (no discounted price shown:
   the code is first-order only). The two keys are NOT put in config/fym-ymi-splits-oct26.json: gate [63] wants full == 't94/..' and
   already fails for all 38 registered sets since the photos moved to the CDN; registering would add 2 problem lines.
 - thumbs script is anchored after the newest thumbs tag; version strings 1.22.14 -> 1.22.15; V12215PIN symlink for local runs.
 - config/fym-stock.json gets the 11 items (gate [138]); rank12215.py then gives the two YMI split sets their back-weighted colour
   ranking + s.bsw (v95_matrank --only, gate [76]).
 - config/fym-tilerank-nov07.json backs: Koi (Watercolor) = #dad0c5 (measured back tile; without it tilerank read the tan motif blend
   and put the set in a Christmas mat's first 10: gate [168]). Set by hand Nov 22, read by tilerank_v118.py.
New files carry the placeholder V12215PIN/ until committed (pin12215.py). After this: rank12215.py (new mats, v104rank) and
builder/fym_fix_nov07/tilerank_v118.py (D.tso for every mat and set). Usage: python3 adds12215.py <build_dir>"""
import sys, os, io, json, base64, hashlib, re, struct, tempfile, shutil, subprocess
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
from skimage.color import rgb2lab, lab2rgb
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
sys.path.insert(0, REPO + 'scripts/colors'); sys.path.insert(0, REPO + 'builder/fym_fix_oct25')
# build_accents rewrites config/mat-accent-colors.json at import (from config/mat-gallery-extra-rows.json): take its measure() only,
# so an adds run never touches the Mat Gallery colour file (it shrank on Nov 22 when a gallery sync was mid-run in another agent).
_ba = open(REPO + 'scripts/colors/build_accents.py').read(); _ns = {'__file__': REPO + 'scripts/colors/build_accents.py', '__doc__': ''}
exec(compile(_ba[:_ba.index("\nout = {'by'")], 'build_accents(defs)', 'exec'), _ns); measure = _ns['measure']
from families import read_image
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
T, M, sets, TV = D['tiles'], D['mats'], D['sets'], D['tv']
SPEC = json.load(open(REPO + 'config/fym-prep-nov22/adds/adds.json'))
_NJ = "Noli June tile sets are Shopify Collective resales of other makers' designs, store tag no-discount (ANSWERS Oct 31: Noli June tile sets not added; never show another maker's product under a brand)"
SKIP = {'mahjongstudios.com/easter-morning-christian-mahjong-tile-set': 'all Mahjong Studios sets are hidden (gate [67])',
        'nolijune.com/martini-mahjong-tile-set': _NJ + ' (maker margo.rebecca)', 'nolijune.com/sweetheart-mahjong-tile-set': _NJ + ' (maker margo.rebecca)',
        'nolijune.com/mazel-mahjong-tile-set': _NJ + ' (maker margo.rebecca)',
        'nolijune.com/the-chinoiserie-set-mahjong-tiles-luxe-lilac': _NJ + ' (maker Southern Sparrow)',
        'nolijune.com/the-riviera-jet-set-mahjong-tiles-portofino-blue': _NJ + ' (maker Southern Sparrow)',
        'www.ymimports.com/hb-cb005-c': 'Qilin Kirin: discontinued, sold out, Chinese 144-tile set without jokers'}
SPEC['tiles'] = [x for x in SPEC['tiles'] if x['key'] not in SKIP]
YMI = 'Yellow Mountain Imports'; YMICODE = 'MAHJMATCH10-YMI-2025'
src = open(REPO + 'builder/fym_fix_oct25/v92_splash.py').read()
exec(src[src.index('def kmeans_sw'):src.index('tmpl = ')])
TO = {'teal': 'blue', 'earthy': 'dark', 'brown': 'dark', 'gold': 'yellow'}
ADD = 'nov22-v12215'; PIN = 'V12215PIN/'
IMG = {}; CH = []; colour_mats = {}; colour_sets = {}; added = []; groups = {}
# 0. repoint (same product, store handle changed): update u / u0 on the existing item, keep its key and everything else
import urllib.parse as _up
REPOINTED = []
for (oldkey, _nm), newkey in SPEC.get('repoint', []):
    o = M.get(oldkey)
    if not o: continue
    oh = oldkey.split('/', 1)[1].split('?')[0]; nh = newkey.split('/', 1)[1]
    for f_ in ('u', 'u0', 'u_plain'):
        if o.get(f_):
            v = o[f_].replace(_up.quote(oh, safe=''), _up.quote(nh, safe='')).replace(oh, nh)
            if v != o[f_]: o[f_] = v; REPOINTED.append((oldkey, f_))
print('repointed fields', len(REPOINTED), 'on', len({k for k, _ in REPOINTED}), 'mats')

def crop(im, box):
    if not box: return im
    W, H = im.size; return im.crop((round(box[0] * W), round(box[1] * H), round(box[2] * W), round(box[3] * H)))

# 1. mats
mcb = re.search(r'MCB=new Set\(\[([0-9, ]+)\]\);', h); chunk = max(int(v) for v in mcb.group(1).split(',')) + 1
maxN = max(int(o['f'].split('/')[1].split('.')[0]) for o in M.values() if o.get('f', '').startswith('m/'))
chunk = max(chunk, maxN // 12 + 1); n0 = chunk * 12
for x in SPEC['mats']:
    key = x['key']
    if key in M: continue
    im = crop(Image.open(REPO + x['img']).convert('RGB'), x.get('box')); im.thumbnail((640, 640)); b = io.BytesIO(); im.save(b, 'WEBP', quality=84, method=6)
    f = f'm/{n0 + len(CH)}.webp'; CH.append((f, b.getvalue()))
    path = tempfile.mktemp(suffix='.png'); im.save(path)
    t = im.copy(); t.thumbnail((150, 150)); bb = io.BytesIO(); t.save(bb, 'WEBP', quality=68, method=6)
    th = 'm12215' + hashlib.md5(key.encode()).hexdigest()[:8]; IMG[th] = 'data:image/webp;base64,' + base64.b64encode(bb.getvalue()).decode()
    sh = {}
    for fam, p in measure(path): fam = TO.get(fam, fam); sh[fam] = sh.get(fam, 0) + p
    fams = [c for c, p in sorted(sh.items(), key=lambda kv: -kv[1]) if p >= 8][:4] or [max(sh, key=sh.get)]
    o = dict(n=x['name'], bn=x['bn'], b=x['bn'], u=x['u'], dc=x['dc'], pa=x['pa'], nc=False, rt=False, c=False, ml=False,
             f=f, th=th, w=im.width, h=im.height, ms=kmeans_sw(im), src='adds-nov22', add=ADD)
    if x.get('u0'): o['u0'] = x['u0']
    if x['hol']: o.update(mf=[], mt=[], sh=[], ha=fams, hol=True)
    else: o.update(mf=fams, mt=list(range(len(fams))), sh=[round(sh.get(c, 0), 1) for c in fams], hol=False)
    if x.get('oos'): o['oos'] = 1
    if x.get('pre'): o['pre'] = 1
    M[key] = o; D['order'].append(key)
    TV['cls'][key] = x['cls']; TV['pm'][key] = x['pm']
    if x['cls'] == 'C': TV['why'][key] = x['why']
    added.append(('mat', x['bn'], x['name'], 'holiday' if x['hol'] else 'year-round', 'sold out' if x.get('oos') else '', x['cls'], fams))
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
os.makedirs(B + '/t12215', exist_ok=True)
tmpl_s = next(s for s in sets if s.get('cat') and not s['m'] and not s.get('hid'))
for x in SPEC['tiles']:
    key, slug = x['key'], x['slug']
    if key in T and T[key].get('add') == ADD: continue
    asrc = f'assets/tiles/v12215/{slug}.jpg'; os.makedirs(REPO + 'assets/tiles/v12215', exist_ok=True); shutil.copyfile(REPO + x['img'], REPO + asrc)
    im = Image.open(REPO + asrc).convert('RGB'); im.thumbnail((1400, 1400)); fn = f't12215/{slug}.jpg'
    if os.path.exists(f'{B}/{fn}'): os.remove(f'{B}/{fn}')
    im.save(f'{B}/{fn}', quality=86)
    S_ = min(im.size); sq = im.crop(((im.width - S_) // 2, (im.height - S_) // 2, (im.width + S_) // 2, (im.height + S_) // 2)).resize((300, 300), Image.LANCZOS)
    pk = 'p12215' + hashlib.md5(slug.encode()).hexdigest()[:10]; b = io.BytesIO(); sq.save(b, 'WEBP', quality=72, method=6)
    IMG[pk] = 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()
    T[key] = dict(full=PIN + fn, n=x['name'], bn=x['bn'], u=x['u'], dc=x['dc'], pa=x['pa'], nc=bool(x.get('nc')), rt=False, pile=pk, cat=True, src=asrc, add=ADD)
    if x['bn'] == YMI:
        assert YMICODE in x['u']; T[key].update(code=YMICODE, split=1, bf=[0.5, 0.5], u_plain=x['u0']); x['pt'] = [x['pt'][0], x['pt'][0], 0]
    if x.get('u0'): T[key]['u0'] = x['u0']
    if x.get('pre'): T[key]['pre'] = 1
    if x.get('oos'): T[key].update(oos=1, so=1)
    s = next((y for y in sets if y['tile'] == key), None)
    if s is None:
        s = {k_: v for k_, v in tmpl_s.items() if k_ not in ('cr', 'fp', 'fz', 'sb', 'hid', 'tag', 'album')}
        s['rank'] = list(tmpl_s['rank']); sets.append(s)
    s.update(slug=slug, name=x['name'], maker=x['bn'], tile=key, tc=x['tc'], m=[], album='', tag='', cat=True)
    for j in newm:
        if j not in s['rank']: s['rank'].append(j)
    bk = {'b': x['back']['b']}
    if x['back'].get('patch'):
        pim = Image.open(REPO + x['back']['patch']); pb = io.BytesIO(); pim.save(pb, 'WEBP', quality=80)
        bk['p'] = 'data:image/webp;base64,' + base64.b64encode(pb.getvalue()).decode()
    TV['backs'][slug] = bk; TV['pt'][key] = x['pt']
    groups.setdefault(x['group'], []).append(x['name'])
    colour_sets[slug] = {'sw': kmeans_faces(im), 'tone': None, 'src': 'photo', 'back': x['back']['b']}
    added.append(('tiles', x['bn'], x['name'], x['group'], x['back']['b']))
for s in sets:
    if 'rank' in s:
        for j in newm:
            if j not in s['rank']: s['rank'].append(j)

# write chunks + D + BACKG + thumbs + loadMC pin for the new chunks
CHUNKS = sorted({int(f.split('/')[1].split('.')[0]) // 12 for f, _ in CH})
os.makedirs(B + '/mc', exist_ok=True)
for c in CHUNKS:
    body, hdr = b'', {}
    for f, raw in CH:
        if int(f.split('/')[1].split('.')[0]) // 12 == c: hdr[f] = [len(body), len(raw)]; body += raw
    hj = json.dumps(hdr, separators=(',', ':')).encode(); _p = f'{B}/mc/{c}.webp'
    if os.path.exists(_p): os.remove(_p)
    open(_p, 'wb').write(body + hj + struct.pack('<I', len(hj)))
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
if CH:
    h = h.replace(mcb.group(0), 'MCB=new Set([' + mcb.group(1) + ''.join(f', {c}' for c in CHUNKS) + ']);', 1)
    a = 'MCP[c]=(MCB.has(c)?fetch(('; assert h.count(a) == 1
    h = h.replace(a, a + f"c>={CHUNKS[0]}&&c<={CHUNKS[-1]}?'{PIN}':", 1)
j = h.index('const BACKG=') + len('const BACKG='); BG, bend = json.JSONDecoder().raw_decode(h[j:]); bend += j
for g, names in groups.items():
    BG.setdefault(g, [])
    for n in names:
        if n not in BG[g]: BG[g].append(n)
h = h[:j] + json.dumps(BG, ensure_ascii=False) + h[bend:]
if IMG:
    open(B + '/thumbs12215.js', 'w').write('window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMG, separators=(',', ':')) + ');')
    a = re.findall(r'<script src="[^"]+/thumbs\w*\.js"></script>', h)[-1]; assert h.count(a) == 1
    if 'thumbs12215.js' not in h: h = h.replace(a, a + f'<script src="{PIN}thumbs12215.js"></script>', 1)
assert h.count('1.22.14') == 2; h = h.replace('1.22.14', '1.22.15')
if not os.path.lexists(B + '/V12215PIN'): os.symlink('.', B + '/V12215PIN')
open(P, 'w').write(h)

# colour ranking (s.cr) for the new tile sets (v85_colorrank, as adds115)
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

# repo-side records
FL = json.load(open(REPO + 'builder/fym_flags/mat_photo_flags.json'))
LK = json.load(open(REPO + 'builder/fym_flags/locks.json'))
for x in SPEC['mats']:
    FL[x['key']] = {'name': x['name'], 'brand': x['bn'], 'flag': 'ok', 'note': 'Nov 22 v12215 add (photo check: config/fym-prep-nov22/adds/notes.md, every listing photo viewed)' + (' cropped to the mat' if x.get('box') else '')}
    o = M[x['key']]; LK['mats'][x['key']] = {k: o.get(k) for k in ('n', 'bn', 'f', 'th', 'rt', 'mf', 'mt')}; LK['mats'][x['key']]['hid'] = bool(o.get('hid'))
TF = json.load(open(REPO + 'builder/fym_flags/tile_photo_flags.json'))
for x in SPEC['tiles']:
    TF[x['slug']] = {'name': x['name'], 'maker': x['bn'], 'flag': 'ok', 'note': 'Nov 22 v12215 add (prep: config/fym-prep-nov22/adds/adds.json)', 'photo': T[x['key']]['full']}
json.dump(FL, open(REPO + 'builder/fym_flags/mat_photo_flags.json', 'w'), indent=1, ensure_ascii=False)
json.dump(LK, open(REPO + 'builder/fym_flags/locks.json', 'w'), indent=1, ensure_ascii=False)
json.dump(TF, open(REPO + 'builder/fym_flags/tile_photo_flags.json', 'w'), indent=1, ensure_ascii=False)
# stock (gate [138]: every sold-out flag in D comes from config/fym-stock.json): the prep run read each product's .js on Nov 22
ST = json.load(open(REPO + 'config/fym-stock.json'))
for kd, xs, pk in (('m', SPEC['mats'], 'pm'), ('t', SPEC['tiles'], 'pt')):
    for x in xs: ST['items'][f"{kd}:{x['key']}"] = {'in': not x.get('oos'), 'how': 'shopify product (prep Nov 22, config/fym-prep-nov22/adds)', 'price': x[pk][0]}
json.dump(ST, open(REPO + 'config/fym-stock.json', 'w'), indent=0, ensure_ascii=False)
for a_ in added: print('  ', a_)
print('skipped', SKIP)
print('added', len(added), 'chunks', CHUNKS, 'inline thumbs KB', round(sum(len(v) for v in IMG.values()) / 1024))
