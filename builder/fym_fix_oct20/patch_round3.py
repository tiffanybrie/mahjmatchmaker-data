"""FYM Oct 20 round 3 (staged; the main session publishes).
Usage: python3 builder/fym_fix_oct20/patch_round3.py <site_dir> <out_dir> <gallery_html>
  site_dir    : base build (index.html + bundles), e.g. scratchpad/fym-oct20d (read only)
  out_dir     : staged build, e.g. scratchpad/fym-oct20e (copied from site_dir only if it does not exist yet; index.html is
                always re-derived from site_dir/index.html, so the script can be re-run)
  gallery_html: Mat Gallery v5 output, i.e. `python3 site/livepatch/matgallery/build_v5.py ...` (see its README); its JSON rows are
                the source of truth for colours (Tiffany's calls, her removals, crosstags, Claude also-colours, measured accents).
Changes:
 1. Colours from Mat Gallery v5: every FYM mat with a gallery row gets mf = primary + also + accent colours mapped onto FYM's chips
    (same map as round 2: teal->blue, earthy->dark "Brown & black", bw->dark+neutral; mood tags Simple/Pastels/Brights/Florals/
    Animal are not FYM chips), mt = tier per mf entry (0 primary, 1 also, 2 accent). Holiday mats: mf=[] (out of single-colour
    chips), ha = their measured colours (counted only when 2+ chips are selected, like the gallery). Mats with no gallery row keep
    their mf (mt = first 0, rest 1). Locked mats get mf + mt updated in locks.json (her gallery calls are her approval).
 2. Sort inside a colour chip: primary, also, accent-only; Mahjong Studios last within each tier (mat door + in-deck; her picks
    still lead the deck).
 3. Multi-select colour chips with AND logic (mat door chips + in-deck colour dots, mats and racks); tap again to unselect;
    "Most matched"/rainbow dot = clear; zero results -> friendly message + Clear colors button, chips stay usable (never locks).
 4. 42 new mats live in gallery v5 (new53_rows.json): images from assets/mats/gallery/<img>.webp packed into new mc/<n>.webp
    chunks, 150px thumbnails in b16v1.js (lazy). Non-code brands (ShopMy/Etsy/Tala): pa=false, dc='' (no MAHJMATCH claim).
    Mahj & Vine Citrus Grove (partner): pa=true + the Mahj & Vine code page + sca_ref link. Each new mat is inserted into every
    set's rank right after its closest existing mat by palette. Photo review -> builder/fym_flags/mat_photo_flags.json.
 5. Retired additions: Peri-twinkle + Garden Party (clean flat renders, already rt=true + visible) take their gallery colours;
    Holy Mahj + Queen Bee stay hidden (stopgap crops).
Every string replace asserts its match count. Data is edited via json raw_decode of `const D=`.
"""
import sys, os, json, shutil, re, io, base64, hashlib, struct, functools
import numpy as np
from PIL import Image
from skimage.color import rgb2lab

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..')) + '/'
GAL = REPO + 'site/livepatch/matgallery/'
SITE, OUT, GHTML = sys.argv[1], sys.argv[2], sys.argv[3]
if not os.path.exists(OUT):
    shutil.copytree(SITE, OUT)
h = open(os.path.join(SITE, 'index.html')).read()


def R(old, new, cnt=1):
    global h
    n = h.count(old)
    assert n == cnt, (n, old[:120])
    h = h.replace(old, new)


i = h.find('const D=') + 8
D, end = json.JSONDecoder().raw_decode(h, i)
M = D['mats']
LOCKS_P = REPO + 'builder/fym_flags/locks.json'
FLAGS_P = REPO + 'builder/fym_flags/mat_photo_flags.json'
LOCKS = json.load(open(LOCKS_P))
FLAGS = json.load(open(FLAGS_P))
FYM = ['pink', 'red', 'orange', 'yellow', 'green', 'blue', 'purple', 'neutral', 'dark']
rep = {'chip_counts_before': {}, 'chip_counts_after': {}, 'chip_tiers_after': {}, 'color': {'changed': 0, 'holiday': 0, 'no_gallery_row_kept': 0,
       'no_fym_chip': []}, 'locks_changed': [], 'new_mats': [], 'new_mats_hidden': [], 'retired': []}


def visible(o): return not o.get('hid')


def counts():
    return {c: sum(1 for o in M.values() if visible(o) and c in (o.get('mf') or [])) for c in FYM}


rep['chip_counts_before'] = counts()

# ---------- gallery v5 rows -> FYM keys
G = json.loads(re.search(r'<script type="application/json">(.*?)</script>', open(GHTML).read(), re.S).group(1).replace('<\\/', '</'))
man = json.load(open(GAL + 'manifest.json'))
N53 = json.load(open(GAL + 'new53_rows.json'))
RADD = json.load(open(GAL + 'retired_additions_oct20.json'))
RA = {a['gallery_id']: a['fym_key'] for a in RADD}
ALIAS = ('mahj-mood--beyond-the-ribbon-four-winds-social-collab-mat-benefitting-pink-fund-pre-order-ships-end-of-december',
         'four-winds-social--fws-x-mahj-mood-collab-beyond-the-ribbon')   # build_v5 IMG_ALIAS shows the FWS row with the Mahj Mood photo
GK = {}
for r in G:
    img = ALIAS[1] if (r[0] == ALIAS[0] and r[2] == 'Four Winds Social') else r[0]
    k = man.get(img) or N53['manifest'].get(img) or RA.get(img)
    assert k and k not in GK, (img, k)
    GK[k] = dict(img=img, row=r)
assert len(GK) == len(G) == 800, len(G)

TO_FYM = {'teal': ['blue'], 'aqua': ['blue'], 'navy': ['blue'], 'earthy': ['dark'], 'brown': ['dark'], 'black': ['dark'], 'bw': ['dark', 'neutral'],
          'white': ['neutral'], 'ivory': ['neutral'], 'cream': ['neutral'], 'gold': ['yellow'], 'coral': ['orange'], 'peach': ['orange'],
          'lavender': ['purple'], 'mustard': ['yellow']}   # same map as round 2 (patch_round2.py)


def to_fym(cols, skip=()):
    out = []
    for c in cols:
        for x in TO_FYM.get(c, [c]):
            if x in FYM and x not in out and x not in skip: out.append(x)
    return out


def fym_colors(r):
    secs, acc, cop = r[5], r[8], r[9]
    hacc = r[10] if len(r) > 10 else []
    if secs == ['holiday']:
        return [], [], to_fym(hacc), True
    prim = to_fym([secs[0]] + list(cop))
    also = to_fym(secs[1:], prim)
    ac = to_fym(acc, prim + also)
    return prim + also + ac, [0] * len(prim) + [1] * len(also) + [2] * len(ac), [], False


for mid, o in M.items():
    g = GK.get(mid)
    old = list(o.get('mf') or [])
    if g is None:
        o['mt'] = [0] + [1] * (len(old) - 1) if old else []
        rep['color']['no_gallery_row_kept'] += 1
        continue
    mf, mt, ha, hol = fym_colors(g['row'])
    o['mf'], o['mt'], o['hol'] = mf, mt, hol
    if ha: o['ha'] = ha
    else: o.pop('ha', None)
    rep['color']['holiday'] += hol
    if not mf and not hol: rep['color']['no_fym_chip'].append([mid, o['n'], g['row'][5]])
    if mf != old: rep['color']['changed'] += 1
for mid, lk in LOCKS['mats'].items():
    o = M.get(mid)
    if o is None or 'mf' not in lk: continue
    for f in ('mf', 'mt'):
        if lk.get(f) != o[f]:
            rep['locks_changed'].append([mid, f, lk.get(f), o[f]]); lk[f] = o[f]

# ---------- 5. retired additions
for a in RADD:
    o = M[a['fym_key']]
    assert o['rt'] is True, a['fym_key']
    if a['name'] in ('Peri-twinkle', 'Garden Party'):
        assert not o.get('hid') and a['fym_key'] in GK, a['fym_key']   # clean flat render, already visible: gallery colours applied above
    else:
        assert o.get('hid') is True, a['fym_key']                         # Holy Mahj / Queen Bee: stopgap crops stay hidden
    rep['retired'].append([a['fym_key'], o['n'], 'visible' if not o.get('hid') else 'hidden', o['mf']])

# ---------- 4. new mats (gallery v5 new53 rows that are live in the gallery)
NEWROWS = [(k, g) for k, g in GK.items() if k not in M]
assert len(NEWROWS) == 42, len(NEWROWS)
PHOTO_FAIL = {   # Claude photo review Oct 20 (contact sheet of all 42): mat must be shown flat, no tiles/racks/props
    'betty-june-jeannette--the-most-wonderful-time-of-the-year': ('no_flat_photo', 'listing render shows tiles + racks set up on the mat '
                                                                 '(game-in-progress mockup); no flat mat-only photo. Gallery v5 shows it; FYM waits for a flat photo.')}
mv = next(o for o in M.values() if o['bn'] == 'Mahj & Vine' and o['pa'] and '?' in o['u'])
MV_Q, MV_DC = mv['u'].split('?', 1)[1], mv['dc']
BRAND_B = {'Mahj & Vine': mv['b']}
B = {}   # thumbnail bundle


def thumb(im):
    t = im.copy(); t.thumbnail((150, 150)); b = io.BytesIO(); t.convert('RGB').save(b, 'JPEG', quality=70)
    v = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
    k = 'mt' + hashlib.md5(v.encode()).hexdigest()[:8]
    assert k not in B; B[k] = v; return k


def palette(im):
    q = im.convert('RGB').resize((96, 96)).quantize(6, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette(); hist = q.histogram()[:6]; tot = sum(hist)
    sw = sorted(((hist[j] / tot, '#%02x%02x%02x' % tuple(pal[j * 3:j * 3 + 3])) for j in range(6) if hist[j]), reverse=True)[:5]
    return [[hx, round(s, 2)] for s, hx in sw]


@functools.lru_cache(None)
def lab(hx): return rgb2lab(np.array([[[int(hx[j:j + 2], 16) / 255 for j in (1, 3, 5)]]]))[0, 0]


def pdist(A, Bv):   # symmetric weighted min-deltaE76 between two palettes
    def one(X, Y):
        lx = np.array([lab(a) for a, _ in X]); wx = np.array([w for _, w in X]); ly = np.array([lab(b) for b, _ in Y])
        d = np.sqrt(((lx[:, None, :] - ly[None, :, :]) ** 2).sum(-1)).min(1)
        return float((d * wx).sum() / wx.sum())
    return 0.5 * one(A, Bv) + 0.5 * one(Bv, A)


maxN = max(int(o['f'].split('/')[1].split('.')[0]) for o in M.values())
N = (maxN // 12 + 1) * 12
CH = {}   # chunk -> [(f, bytes)]
ix = {m: j for j, m in enumerate(D['order'])}
RL0 = [len(s['rank']) for s in D['sets']]
cand = [m for m in D['order'] if visible(M[m]) and not M[m]['rt'] and M[m].get('ms')]
cand_ms = {m: M[m]['ms'] for m in cand}
for key, g in NEWROWS:
    r, img = g['row'], g['img']
    p = REPO + 'assets/mats/gallery/' + img + '.webp'
    raw = open(p, 'rb').read(); assert raw[:4] == b'RIFF' and raw[8:12] == b'WEBP', p
    im = Image.open(io.BytesIO(raw)).convert('RGB')
    f = f'm/{N}.webp'; CH.setdefault(N // 12, []).append((f, raw)); N += 1
    mf, mt, ha, hol = fym_colors(r)
    brand, url = r[2], r[3]
    partner = brand == 'Mahj & Vine'
    if partner: url = url + ('&' if '?' in url else '?') + MV_Q
    o = dict(n=r[1], bn=brand, b=BRAND_B.get(brand, brand), u=url, dc=MV_DC if partner else '', pa=partner, nc=False, rt=bool(r[4]), c=False,
             ml=False, f=f, th=thumb(im), w=im.width, h=im.height, mf=mf, mt=mt, ms=palette(im), hol=hol, src='gallery-v5', add='oct20r3')
    if ha: o['ha'] = ha
    if img in PHOTO_FAIL:
        o['hid'] = True
        FLAGS[key] = {'name': o['n'], 'brand': brand, 'flag': PHOTO_FAIL[img][0], 'note': PHOTO_FAIL[img][1]}
        rep['new_mats_hidden'].append([key, o['n'], brand, PHOTO_FAIL[img][0]])
    else:
        FLAGS[key] = {'name': o['n'], 'brand': brand, 'flag': 'ok', 'note': 'Oct 20 round 3 photo review: flat mat render (gallery v5 photo), no tiles/props'}
    M[key] = o
    # rank: right after the closest existing mat by palette (holiday mats only next to holiday mats and vice versa)
    pool = [m for m in cand if bool(M[m]['hol']) == hol] or cand
    near = min(pool, key=lambda m: pdist(o['ms'], cand_ms[m]))
    ni = len(D['order']); D['order'].append(key); ix[key] = ni
    for s in D['sets']:
        rk = s['rank']
        if ix[near] in rk: rk.insert(rk.index(ix[near]) + 1, ni)
        else: rk.append(ni)
    rep['new_mats'].append([key, o['n'], brand, 'partner+code' if partner else 'no code (pa=false)', url, mf, mt, ha, 'hidden' if o.get('hid') else 'visible',
                            'next to ' + M[near]['n']])
assert all(len(s['rank']) == RL0[j] + len(NEWROWS) for j, s in enumerate(D['sets']))

# mc chunks (same binary pack as the existing mc/86..163.webp: concatenated webps + JSON {f:[offset,len]} + uint32 LE length)
new_chunks = sorted(CH)
for c, items in CH.items():
    assert not os.path.exists(os.path.join(SITE, 'mc', f'{c}.webp')) and not os.path.exists(os.path.join(SITE, 'mc', f'{c}.json')), c
    body, hdr = b'', {}
    for f, raw in items:
        hdr[f] = [len(body), len(raw)]; body += raw
    hj = json.dumps(hdr, separators=(',', ':')).encode()
    open(os.path.join(OUT, 'mc', f'{c}.webp'), 'wb').write(body + hj + struct.pack('<I', len(hj)))
assert not os.path.exists(os.path.join(SITE, 'b16v1.js'))
open(os.path.join(OUT, 'b16v1.js'), 'w').write('window.IMG=Object.assign(window.IMG||{},' + json.dumps(B, separators=(',', ':')) + ');')

rep['chip_counts_after'] = counts()
rep['chip_tiers_after'] = {c: {t: sum(1 for o in M.values() if visible(o) and c in o['mf'] and o['mt'][o['mf'].index(c)] == j)
                               for j, t in enumerate(('primary', 'also', 'accent'))} for c in FYM}
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]

# ---------- UI: lazy thumbnail bundle + new mc chunks
lz = re.search(r'window\.__LAZY=(\[[^\]]*\]);', h)
R(lz.group(0), 'window.__LAZY=' + json.dumps(json.loads(lz.group(1)) + ['b16v1.js']) + ';')
mcb = re.search(r'MCB=new Set\(\[([0-9, ]+)\]\);', h)
assert max(int(x) for x in mcb.group(1).split(',')) < new_chunks[0]
R(mcb.group(0), 'MCB=new Set([' + mcb.group(1) + ''.join(f', {c}' for c in new_chunks) + ']);')

# ---------- 2 + 3. colour tiers, sort, multi-select AND
R("const MSL=ids=>{const a=[],z=[];ids.forEach(id=>(M[id]&&M[id].bn==='Mahjong Studios'?z:a).push(id));return a.concat(z);};",
  "const MSL=ids=>{const a=[],z=[];ids.forEach(id=>(M[id]&&M[id].bn==='Mahjong Studios'?z:a).push(id));return a.concat(z);};\n"
  "/* Oct 20 r3: colour tiers (mt: 0 primary, 1 also, 2 accent; ha = holiday mats' colours, counted only in 2+ chip combos) + multi-select AND chips */\n"
  "const MTI=(id,c)=>{const o=M[id],i=(o.mf||[]).indexOf(c);return i>-1?(o.mt?o.mt[i]:(i?1:0)):((o.ha||[]).includes(c)?2:9);};\n"
  "const HASC=(id,C)=>C.length<2?(M[id].mf||[]).includes(C[0]):C.every(c=>MTI(id,c)<9);\n"
  "const CTIER=(id,C)=>{if(C.length<2)return MTI(id,C[0]);const t=C.map(c=>MTI(id,c));return t.some(x=>x>1)?2:(t.includes(0)?0:1);};\n"
  "const CSORT=(ids,C)=>ids.map((id,i)=>[CTIER(id,C)*2+(M[id].bn==='Mahjong Studios'?1:0),i,id]).sort((a,b)=>a[0]-b[0]||a[1]-b[1]).map(x=>x[2]);/* primary, also, accent; Mahjong Studios last within each tier */\n"
  "const NOAND='No mats with all of those yet \\u2014 try removing one.';\n"
  "const TOG=(C,c)=>!c?[]:(C.includes(c)?C.filter(x=>x!==c):[...C,c]);")
R("if(f.fam)ids=ids.filter(id=>M[id].mf.includes(f.fam));",
  "if(f.fam.length){const C=f.fam;ids=ids.filter(id=>HASC(id,C));ids=[...ids.filter(herMat),...CSORT(ids.filter(id=>!herMat(id)),C)];}")
R("if(f.fam)ids=ids.filter(r=>R[r].rf.includes(f.fam));", "if(f.fam.length)ids=ids.filter(r=>f.fam.every(c=>(R[r].rf||[]).includes(c)));")
R('aria-pressed="${!f.fam}" title="All colors"', 'aria-pressed="${!f.fam.length}" title="All colors"')
R('aria-pressed="${f.fam===x}" title="${FAMN[x]}"', 'aria-pressed="${f.fam.includes(x)}" title="${FAMN[x]}"')
R("fam:'',brand:'',her:false", "fam:[],brand:'',her:false", 7)
R("if(b=q('.frow [data-fam]')){S.f[b.dataset.k].fam=b.dataset.fam;rerender(b.dataset.k);return;}",
  "if(b=q('.frow [data-fam]')){const f=S.f[b.dataset.k];f.fam=TOG(f.fam,b.dataset.fam);rerender(b.dataset.k);return;}\n"
  " if(b=q('[data-fclear]')){S.f[b.dataset.fclear].fam=[];rerender(b.dataset.fclear);return;}")
R(" if(!q.length&&S.f[k].her)return `",
  " if(!q.length&&S.f[k].fam.length>1&&!(k==='m'?matDeck():rackDeck()).length)return `<div class=\"deck ${k}\"><div class=\"empty\">${k==='m'?NOAND:NOAND.replace('mats','racks')}<button type=\"button\" class=\"big gh\" style=\"width:auto;padding:10px 16px\" data-fclear=\"${k}\">Clear colors</button></div></div>`;\n"
  " if(!q.length&&S.f[k].her)return `")
# mat door
R("if(S.dfam)ids=ids.filter(id=>(M[id].mf||[]).includes(S.dfam));\n return MSL(ids.sort((a,b)=>(c[b]||0)-(c[a]||0)||M[a].n.localeCompare(M[b].n)));}",
  "const C=S.dfams||[];if(C.length)ids=ids.filter(id=>HASC(id,C));\n ids=MSL(ids.sort((a,b)=>(c[b]||0)-(c[a]||0)||M[a].n.localeCompare(M[b].n)));return C.length?CSORT(ids,C):ids;}")
R('<p>Mats by color</p><button type="button" data-dfam="" aria-pressed="${!S.dfam}" style="--c:#1f3a6b">Most matched</button>`+FAMS.map(f=>`<button type="button" data-dfam="${f}" aria-pressed="${S.dfam===f}"',
  '<p>Mats by color</p><small class="thint">Tap two or more colors to find mats with all of them</small><button type="button" data-dfam="" aria-pressed="${!(S.dfams||[]).length}" style="--c:#1f3a6b">${(S.dfams||[]).length?\'Clear colors \\u2715\':\'Most matched\'}</button>`+FAMS.map(f=>`<button type="button" data-dfam="${f}" aria-pressed="${(S.dfams||[]).includes(f)}"')
R("if(b=q('[data-dfam]')){S.dfam=b.dataset.dfam;DOOR.lim=36;renderTiles();return;}",
  "if(b=q('[data-dfam]')){S.dfams=TOG(S.dfams||[],b.dataset.dfam);DOOR.lim=36;renderTiles();return;}")
R('<div class="tgrid mgrid" id="mdgrid">${ids.slice(0,DOOR.lim).map(matBtn).join(\'\')}</div>',
  '<div class="tgrid mgrid" id="mdgrid">${ids.length?ids.slice(0,DOOR.lim).map(matBtn).join(\'\'):`<p class="dempty">${NOAND}</p>`}</div>')
R("if(v.length<2){g.innerHTML=doorMats().slice(0,DOOR.lim).map(matBtn).join('');return;}",
  "if(v.length<2){const L=doorMats();g.innerHTML=L.length?L.slice(0,DOOR.lim).map(matBtn).join(''):`<p class=\"dempty\">${NOAND}</p>`;return;}")
R(".tchips button[aria-pressed=true]{background:var(--c);color:#fff}",
  ".tchips button[aria-pressed=true]{background:var(--c);color:#fff}\n"
  ".tchips .thint{display:block;font-size:12px;color:#6f655d;margin:-4px 0 6px}\n"
  ".dempty{grid-column:1/-1;text-align:center;font:600 15px var(--body);color:#3a2a2e;padding:18px 8px;margin:0}")
assert 'S.dfam=' not in h and 'S.dfam)' not in h and "S.dfam===" not in h

open(os.path.join(OUT, 'index.html'), 'w').write(h)
json.dump(LOCKS, open(LOCKS_P, 'w'), indent=1, ensure_ascii=False)
json.dump(FLAGS, open(FLAGS_P, 'w'), indent=1, ensure_ascii=False)
rep['new_chunks'] = new_chunks
json.dump(rep, open(os.path.join(HERE, 'round3_report.json'), 'w'), indent=1, ensure_ascii=False)
c = rep['color']
print('ok', len(h), '| mf changed', c['changed'], '| holiday', c['holiday'], '| no gallery row (kept)', c['no_gallery_row_kept'],
      '| no FYM chip', len(c['no_fym_chip']), '| locks updated', len(rep['locks_changed']), '| new mats', len(rep['new_mats']),
      '(hidden', len(rep['new_mats_hidden']), ') | chunks', new_chunks)
for col in FYM:
    print(f"  {col:8s} {rep['chip_counts_before'][col]:4d} -> {rep['chip_counts_after'][col]:4d}  {rep['chip_tiers_after'][col]}")
