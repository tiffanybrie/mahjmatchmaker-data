"""FYM v96: Tiffany's Amazon holiday mat picks (Oct 26 11:16am, docs/ANSWERS.md; spec config/fym-amazon-holiday-oct26.json).
1. Adds the 28 picks like v95_etsy.py: photo = ONLY the mat (bags/tubes, #6's line-finder strip, reflections, badges cropped off;
   assets/mats/v96-amazon/), new packed chunk, inline thumb, colours measured from the cropped mat, Holiday only (mf/mt/sh empty,
   colours in ha). Link = her go.shopmy.us link, no code claim (dc '', pa False). Plain plaids/stripes stay Holiday until she moves
   them (CLAUDE.md holiday rule) and are listed for her in the spec (flag_for_her).
2. Partner tie-break (Tiffany 11:16: "preferential treatment towards our true partner brands... nothing would supersede Tiffany's
   picks"): ShopMy mats (this Amazon batch + the v95 Etsy batch, add oct26-amazon / oct26-etsy) are placed INTO every set's colour
   ranking (s.cr, the deck order when picks are off) by the v85 colour score + PEN, so they sit below partner mats of similar colour
   score instead of at the very end. Existing cr order is untouched (her picks always lead the deck; this only places the new mats).
   Holiday tile sets (BACKG Holiday): a ShopMy mat never sits in the first 6 non-pick places while a partner holiday mat matches
   (is in that set's top 30). Holiday chip/list order: new mats are appended to D.order, i.e. after every partner holiday mat.
Gate [74]. Idempotent. Usage: python3 v96_amazon_holiday.py <build_dir>"""
import sys, os, io, json, base64, hashlib, re, struct, tempfile
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
from skimage.color import rgb2lab, lab2rgb, deltaE_ciede2000
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
sys.path.insert(0, REPO + 'scripts/colors'); sys.path.insert(0, REPO + 'builder/fym_fix_oct25')
from build_accents import measure
from families import read_image
PEN = 12.0          # non-partner (ShopMy) tie-break, in v85 colour-score points
SHOPMY_ADDS = ('oct26-amazon', 'oct26-etsy')
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
M, sets = D['mats'], D['sets']
SPEC = json.load(open(REPO + 'config/fym-amazon-holiday-oct26.json'))['mats']
src = open(REPO + 'builder/fym_fix_oct25/v92_splash.py').read()
exec(src[src.index('def kmeans_sw'):src.index('tmpl = ')])  # same swatch measure as v92/v94/v95
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
    th = 'm96' + hashlib.md5(key.encode()).hexdigest()[:8]; IMG[th] = 'data:image/jpeg;base64,' + base64.b64encode(bb.getvalue()).decode()
    sh = {}
    for fam, p in measure(path): fam = TO.get(fam, fam); sh[fam] = sh.get(fam, 0) + p
    fams = [c for c, p in sorted(sh.items(), key=lambda kv: -kv[1]) if p >= 8][:4] or [max(sh, key=sh.get)]
    o = dict(n=x['name'], bn=x['brand'], b='Amazon', u=x['u'], u0=x['u'], dc='', pa=False, nc=False, rt=False, c=False, ml=False,
             f=f, th=th, w=im.width, h=im.height, ms=kmeans_sw(im), src='shopmy-amazon-oct26', add='oct26-amazon')
    if x['hol']: o.update(mf=[], mt=[], sh=[], ha=fams, hol=True)
    else: o.update(mf=fams, mt=list(range(len(fams))), sh=[round(sh.get(c, 0), 1) for c in fams], hol=False)
    if x['hid']: o['hid'] = True
    M[key] = o; D['order'].append(key); added.append((x['name'], 'holiday' if x['hol'] else 'year-round', 'HIDDEN' if x['hid'] else 'visible', fams))
    _, tone, _ = read_image(path); colour_mats[key] = {'sw': o['ms'], 'tone': tone}; os.remove(path)
ix = {m: j for j, m in enumerate(D['order'])}
newm = [ix[k] for k in M if M[k].get('add') == 'oct26-amazon']
for s in sets:
    if 'rank' in s:
        for j in newm:
            if j not in s['rank']: s['rank'].append(j)

# ---- 2. place ShopMy mats into each set's colour ranking (v85 score + PEN) ----
C = json.load(open(REPO + 'config/fym-colour-oct25.json')); C['mats'].update(colour_mats)
X = json.load(open(REPO + 'config/fym-colour-rules.json'))
ROOM = set(json.load(open(REPO + 'config/fym-colour-room-photos.json'))['mats']) if os.path.exists(REPO + 'config/fym-colour-room-photos.json') else set()
_m = re.search(r'BACKG=(\{.*?\});', h); BG = json.loads(_m.group(1)) if _m else {}
HOLSETS = set(BG.get('Holiday', [])); GROUP = {g: set(v) for g, v in BG.items()}
G2F = {'Pink': ['pink'], 'Red': ['red'], 'Blue': ['blue'], 'Green': ['green'], 'Purple': ['purple'], 'Yellow & Orange': ['yellow', 'orange'],
       'Brown': ['dark'], 'Ivory': ['neutral'], 'Natural Patterns': ['dark', 'neutral']}
def lab(hx): return rgb2lab(np.array([[[int(hx[k:k + 2], 16) / 255 for k in (1, 3, 5)]]]))[0, 0]
_PC = {}
def prep(sw):
    if not sw: return None
    L = np.array([lab(hx) for hx, _ in sw]); w = np.array([x for _, x in sw], float); w = w / w.sum()
    return L, w, float(w[np.hypot(L[:, 1], L[:, 2]) >= 38].sum())
def mprep(m):
    if m not in _PC: _PC[m] = prep((C['mats'].get(m) or {}).get('sw'))
    return _PC[m]
def theme_of(name):
    for th_, pat in X['themes'].items():
        if re.search(pat, name, re.I): return th_
    return None
def score(s, tp, m):  # == v85_colorrank.py per-mat score
    la, wa, vt = tp; mp = mprep(m)
    if mp is None: return 1e9
    lb, wb, vm = mp
    d = deltaE_ciede2000(np.repeat(la, len(lb), 0), np.tile(lb, (len(la), 1))).reshape(len(la), len(lb))
    v = 0.6 * float((d.min(1) * wa).sum()) + 0.4 * float((d.min(0) * wb).sum()) + 140.0 * max(0.0, abs(vm - vt) - 0.08)
    o = M[m]; hol_set = s['name'] in HOLSETS
    if o.get('hol'): v += (-25 if hol_set else 25)
    gf = set(f for g, names in GROUP.items() if s['name'] in names for f in G2F.get(g, []))
    if gf:
        mf, mt = o.get('mf') or [], o.get('mt') or []
        tiers = [mt[j] if j < len(mt) else 1 for j, c in enumerate(mf) if c in gf] + [2 for c in (o.get('ha') or []) if c in gf]
        v += -15 if (tiers and min(tiers) == 0) else (-8 if tiers else 25)
    th_ = theme_of(o['n'])
    if th_: v += -20 if th_ == theme_of(s['name']) else 40
    if any(re.search(p, o['n'], re.I) for p in X['novelty']): v += 20
    if o.get('rt'): v += 20
    if re.search(r'paige spearin', o['n'] + ' ' + o.get('bn', ''), re.I): v += 60
    return v
order = D['order']; OI = {m: j for j, m in enumerate(order)}
shop = [m for m in order if M[m].get('add') in SHOPMY_ADDS and not M[m].get('hid') and m not in ROOM and mprep(m)]
shop_ix = {OI[m] for m in M if M[m].get('add') in SHOPMY_ADDS}
placed = 0; report = {}
for s in sets:
    if 'cr' not in s: continue
    cs = C['sets'].get(s['slug']) or {}; sw = cs.get('sw')
    if s['name'] in X['back_only_sets'] and cs.get('back'): sw = [[cs['back'], 1.0]]
    tp = prep(sw)
    before = list(s['cr'])
    base = [j for j in s['cr'] if j not in shop_ix]           # idempotent: drop earlier placements
    if not tp: s['cr'] = base; continue
    picks = {e[0] if isinstance(e, list) else e for e in (s.get('m') or [])}; hol_set = s['name'] in HOLSETS
    bsc = [score(s, tp, order[j]) for j in base]
    # cr = brand-front block + score order; only place inside the score-ordered tail (never ahead of the brand-front block)
    k0 = 0
    if not s.get('m'):
        tb = (D['tiles'].get(s['tile']) or {}).get('bn') or s['maker']
        while k0 < len(base) and M[order[base[k0]]].get('bn') == tb: k0 += 1
    # holiday sets: the first 6 non-pick places stay partner/other mats while a partner holiday mat matches (top 30)
    floor = 0
    if hol_set:
        partner_hol = any(M[order[j]].get('pa') and M[order[j]].get('hol') for j in base[:30])
        if partner_hol:
            n = 0
            for k, j in enumerate(base):
                if order[j] not in picks: n += 1
                if n == 6: floor = k + 1; break
    ins = sorted(((score(s, tp, m) + PEN, m) for m in shop), key=lambda t: t[0])
    out = list(base); osc = list(bsc)
    for v, m in ins:
        k = max(k0, floor)
        while k < len(osc) and osc[k] <= v: k += 1
        if k >= 300: continue
        out.insert(k, OI[m]); osc.insert(k, v); placed += 1
    s['cr'] = out[:300 + len(shop)]
    if hol_set: report[s['slug']] = {'name': s['name'], 'before': [M[order[j]]['n'] + ' | ' + M[order[j]]['bn'] for j in before[:10]],
                                     'after': [M[order[j]]['n'] + ' | ' + M[order[j]]['bn'] for j in s['cr'][:10]]}
if CH:
    body, hdr = b'', {}
    for f, raw in CH: hdr[f] = [len(body), len(raw)]; body += raw
    hj = json.dumps(hdr, separators=(',', ':')).encode(); open(f'{B}/mc/{chunk}.webp', 'wb').write(body + hj + struct.pack('<I', len(hj)))
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
if CH: h = h.replace(mcb.group(0), 'MCB=new Set([' + mcb.group(1) + f', {chunk}]);', 1)
if IMG:
    inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMG, separators=(',', ':')) + ');</script>'
    a = '<script src="b24v1.js"></script>'; assert h.count(a) == 1; h = h.replace(a, a + inl, 1)
open(P, 'w').write(h)
json.dump(report, open(B + '/v96_amazon_order_report.json', 'w'), indent=1, ensure_ascii=False)
# repo-side records (idempotent)
C2 = json.load(open(REPO + 'config/fym-colour-oct25.json')); C2['mats'].update(colour_mats)
json.dump(C2, open(REPO + 'config/fym-colour-oct25.json', 'w'), indent=0, ensure_ascii=False)
FL = json.load(open(REPO + 'builder/fym_flags/mat_photo_flags.json'))
for x in SPEC:
    FL[x['key']] = {'name': x['name'], 'brand': x['brand'], 'flag': 'questionable' if x['hid'] else 'ok',
                    'note': 'Oct 26 Amazon ShopMy holiday pick: cropped to the mat only' + (' (' + x['note'] + ')' if x.get('note') else '')}
json.dump(FL, open(REPO + 'builder/fym_flags/mat_photo_flags.json', 'w'), indent=1, ensure_ascii=False)
for a_ in added: print(*a_)
print('chunk', chunk if CH else None, 'mats', len(added), '| ShopMy mats placed into colour rankings:', placed)
