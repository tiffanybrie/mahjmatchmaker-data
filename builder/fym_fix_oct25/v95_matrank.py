"""FYM v95 mat ranking fix (Tiffany Oct 26 11:31-11:37: Aloha (YMI) led with Songbird Bloom / grey mats; "The back color is a
dominant color... go ahead"). Rebuilds s.cr (the colour ranking used when her picks are off, and the ONLY ranking for unmatched
sets) for every visible NON-holiday set. Faces|backs split photos (69 sets) or a back override get 1; every set gets 2 + 3:
 1. BACK COLOUR re-measured from the CURRENT tile photo (the v85 config back_hex came from old guesses, e.g. Aloha '#91aa9d' sage;
    its backs are white with yellow plumeria): right half of the 1600x700 split = backs. Back = 80% of the set's colour, faces
    (left half, white faces dropped) 20%. A motif on a white back (Aloha) -> the motif's colours 85% of the back + white 15%;
    a plain white back -> white. Grid layouts where the back is one tile in the middle (Virora, MFM) use the most uniform
    coloured block in the photo; tortoise scatters use the whole photo. Overrides: config/fym-back-colour-oct26.json.
 2. Partner-first tie-break: non-partner (allowed) mats get +PEN so a partner mat of about the same colour comes first.
 3. Motif hint (config/fym-motifs-oct26.json): a set whose name matches a motif (Aloha = tropical) lifts mats whose name matches
    the same motif by -MOTIF; never adds colours.
Same score as v85_colorrank.py otherwise (CIEDE2000 both ways, vividness gap, holiday, themes, novelty, retired, Paige Spearin).
Mats not scored (Etsy/Amazon ShopMy adds placed by v95_etsy / v96) keep their positions relative to the end. Her picks (s.m) and
coordinated pairs are untouched (run v92_coordinated AFTER this). Holiday tile sets are skipped (holiday order untouched).
Idempotent (recomputes from the photos each run). Gate [76].
Usage: python3 v95_matrank.py <build_dir> [--report out.json]"""
import sys, os, json, re
import numpy as np
from PIL import Image
from skimage.color import rgb2lab, deltaE_ciede2000
from sklearn.cluster import KMeans
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
C = json.load(open(REPO + '/config/fym-colour-oct25.json'))
X = json.load(open(REPO + '/config/fym-colour-rules.json'))
BO = json.load(open(REPO + '/config/fym-back-colour-oct26.json'))
MO = json.load(open(REPO + '/config/fym-motifs-oct26.json'))
PEN, MOTIF, BW = 6.0, 15.0, .8   # BW: share of the set's colour that is the tile BACK (Tiffany: back is dominant)

def hexs(c): return '#%02x%02x%02x' % tuple(int(round(v * 255)) for v in np.clip(c, 0, 1))
def lab(hx): return rgb2lab(np.array([[[int(hx[k:k + 2], 16) / 255 for k in (1, 3, 5)]]]))[0, 0]
def px(im, box=None):
    if box: im = im.crop(box)
    im = im.copy(); im.thumbnail((240, 240)); return np.asarray(im, float).reshape(-1, 3) / 255
def km(a, k):
    if len(a) < 60: return []
    k = min(k, max(1, len(a) // 200))
    L = rgb2lab(a.reshape(-1, 1, 3)).reshape(-1, 3); m = KMeans(n_clusters=k, n_init=3, random_state=0).fit(L)
    cnt = np.bincount(m.labels_, minlength=k) / len(L); out = []
    for j in np.argsort(-cnt):
        if cnt[j] < .06: continue
        out.append([hexs(a[m.labels_ == j].mean(0)), float(cnt[j])])
    t = sum(w for _, w in out) or 1; return [[hx, w / t] for hx, w in out]
WHITE = lambda a: (a.min(1) > .80) & (a.max(1) - a.min(1) < .12)
PALE = lambda a: (a.mean(1) > .50) & (a.max(1) - a.min(1) < .10)   # white/ivory/clear incl. its grey shading
def faces_sw(im, box):
    a = px(im, box); a = a[~(a.min(1) > .94)]; a = a[~WHITE(a)]; return km(a, 5)
def back_sw(im, box):
    a = px(im, box); a = a[~(a.min(1) > .95)]           # product background (CMC / Apres scatters on white)
    if len(a) < 60: return [['#f3f1ea', 1.0]], 'white'
    w = PALE(a); col = 1 - w.mean()
    if col >= .5: return km(a[~w], 3), 'solid'
    if (1 - WHITE(a).mean()) >= .6 and a.mean() > .6: return km(a, 2), 'solid-pale'    # ivory / pastel solid backs
    sat = (a.max(1) - a.min(1)) > .18                     # the motif itself (Aloha's yellow plumeria + leaves), not the tinted clear back
    if col >= .08 and sat.mean() >= .03: return [[hx, x * .85] for hx, x in km(a[sat], 3)] + [['#f3f1ea', .15]], 'motif'
    if col >= .08: return [[hx, x * .85] for hx, x in km(a[~w], 3)] + [['#f3f1ea', .15]], 'motif'
    return [['#f3f1ea', 1.0]], 'white'
def uniform_block(im):
    a = np.asarray(im.resize((400, 175)), float) / 255; best = None
    for y in range(0, 175 - 24, 6):
        for x in range(0, 400 - 24, 6):
            blk = a[y:y + 24, x:x + 24].reshape(-1, 3); mu = blk.mean(0)
            if mu.min() > .78 and mu.max() - mu.min() < .12: continue      # white face
            if mu.max() - mu.min() < .10 and mu.mean() < .2: continue     # black shadow
            sd = blk.std(0).mean()
            if best is None or sd < best[0]: best = (sd, mu)
    return hexs(best[1])

M = D['mats']; order = D['order']; OI = {m: j for j, m in enumerate(order)}
_m = re.search(r'BACKG=(\{.*?\});', h); BG = json.loads(_m.group(1)) if _m else {}
HOLSETS = set(BG.get('Holiday', []))
GROUP = {g: set(v) for g, v in BG.items()}
G2F = {'Pink': ['pink'], 'Red': ['red'], 'Blue': ['blue'], 'Green': ['green'], 'Purple': ['purple'], 'Yellow & Orange': ['yellow', 'orange'],
       'Brown': ['dark'], 'Ivory': ['neutral'], 'Natural Patterns': ['dark', 'neutral']}
ROOM = set(json.load(open(REPO + '/config/fym-colour-room-photos.json'))['mats']) if os.path.exists(REPO + '/config/fym-colour-room-photos.json') else set()
def theme_of(name):
    for th, pat in X['themes'].items():
        if re.search(pat, name, re.I): return th
def motif_of(name):
    return [mo for mo, pat in MO['motifs'].items() if re.search(pat, name, re.I)]
def prep(sw):
    L = np.array([lab(hx) for hx, _ in sw]); w = np.array([x for _, x in sw], float); w = w / w.sum()
    return L, w, float(w[np.hypot(L[:, 1], L[:, 2]) >= 38].sum())
keys = [m for m in order if not M[m].get('hid') and m in C['mats'] and C['mats'][m]['sw'] and m not in ROOM]
MTH = {m: theme_of(M[m]['n']) for m in keys}; MMO = {m: motif_of(M[m]['n']) for m in keys}
NOV = {m for m in keys if any(re.search(p, M[m]['n'], re.I) for p in X['novelty'])}
PS = {m for m in keys if re.search(r'paige spearin', M[m]['n'] + ' ' + M[m].get('bn', ''), re.I)}
MP = {m: prep(C['mats'][m]['sw']) for m in keys}
ALL = np.concatenate([MP[m][0] for m in keys]); seg = np.cumsum([0] + [len(MP[m][1]) for m in keys])
VIV_TOL, VIV_K = 0.08, 140.0
GRID = re.compile(MO['grid_back_sets'], re.I); WHOLE = re.compile(MO['whole_photo_sets'], re.I)
rep = {}; n = 0
ONLY = sys.argv[sys.argv.index('--only') + 1].split(',') if '--only' in sys.argv else None
for s in D['sets']:
    if s.get('hid') or s['name'] in HOLSETS: continue
    if ONLY and s['slug'] not in ONLY: continue
    t = D['tiles'].get(s['tile']) or {}
    ov = BO['sets'].get(s['slug'])
    if t.get('soon'): continue
    f = t.get('full'); im = Image.open(B + '/' + f).convert('RGB') if f and os.path.exists(B + '/' + f) else None
    W, H = im.size if im is not None else (0, 0)
    if not (t.get('split') or ov) or im is None:      # other sets: v85 swatches (its back_hex at 0.5) + tie-break + motif only
        bsw = (C['sets'].get(s['slug']) or {}).get('sw'); kind = 'v85'; fsw = []
        if not bsw: continue
    elif ov and ov.get('back'):
        bsw, kind = [[ov['back'], 1.0]], 'override'; fsw = faces_sw(im, None)
    elif WHOLE.search(s['name']):
        a = px(im); a = a[~(a.min(1) > .94)]; bsw, kind = km(a[~WHITE(a)], 4), 'whole'; fsw = []
    elif GRID.search(s['name']) or W / H < 2:
        bsw, kind = [[uniform_block(im), 1.0]], 'grid-block'; fsw = faces_sw(im, None)
    else:
        bsw, kind = back_sw(im, (W // 2, 0, W, H)); fsw = faces_sw(im, (0, 0, W // 2, H))
    sw = [[hx, w * BW] for hx, w in bsw] + [[hx, w * (1 - BW)] for hx, w in fsw] if fsw else bsw
    la, wa, vt = prep(sw)
    if kind != 'v85':   # earthy backs (wood, gold, tortoise: brown/gold hue, not light) are not 'vivid' even when chroma >= 38
        hue = np.degrees(np.arctan2(la[:, 2], la[:, 1])) % 360; ch = np.hypot(la[:, 1], la[:, 2])
        vt = float(wa[(ch >= 38) & ~((hue >= 35) & (hue <= 100) & (la[:, 0] < 76))].sum())
    sth = theme_of(s['name']); smo = motif_of(s['name'])
    gf = set(f for g, names in GROUP.items() if s['name'] in names for f in G2F.get(g, []))
    if kind == 'motif': gf = set()   # her site colour group is the plain tile colour (Aloha = Ivory); the back motif decides instead
    Dm = deltaE_ciede2000(np.repeat(la, len(ALL), 0), np.tile(ALL, (len(la), 1))).reshape(len(la), len(ALL))
    sc = {}
    for j, m in enumerate(keys):
        d = Dm[:, seg[j]:seg[j + 1]]; _, wb, vm = MP[m]
        v = 0.6 * float((d.min(1) * wa).sum()) + 0.4 * float((d.min(0) * wb).sum())
        v += VIV_K * max(0.0, abs(vm - vt) - VIV_TOL)
        if M[m].get('hol'): v += 25
        if gf:
            mf, mt = M[m].get('mf') or [], M[m].get('mt') or []
            tiers = [mt[k] if k < len(mt) else 1 for k, c in enumerate(mf) if c in gf] + [2 for c in (M[m].get('ha') or []) if c in gf]
            v += -15 if (tiers and min(tiers) == 0) else (-8 if tiers else 25)
        th = MTH[m]
        if th: v += -20 if th == sth else 40
        if m in NOV: v += 20
        if M[m].get('rt'): v += 20
        if m in PS: v += 60
        if not M[m].get('pa'): v += PEN                                  # partner-first tie-break
        if smo and set(smo) & set(MMO[m]): v -= MOTIF                   # motif hint
        sc[m] = v
    ranked = sorted(sc, key=lambda m: sc[m])
    front = []
    if not s['m']:
        best60 = set(ranked[:60]); tb = t.get('bn') or s['maker']
        def ingroup(m):
            mf, mt = M[m].get('mf') or [], M[m].get('mt') or []
            return not gf or any(c in gf and (k >= len(mt) or mt[k] == 0) for k, c in enumerate(mf))
        best = sc[ranked[0]]
        front = [m for m in ranked if m in best60 and sc[m] <= best + 20 and M[m].get('bn') == tb and not M[m].get('hol') and ingroup(m)]
    out = front + [m for m in ranked if m not in front]
    old = [order[j] for j in s.get('cr', [])]
    extra = [m for m in old if m not in sc]                 # ShopMy adds etc.: keep, after the scored list's top 300
    new = [OI[m] for m in out[:300]] + [OI[m] for m in extra]
    rep[s['slug']] = {'name': s['name'], 'maker': s['maker'], 'kind': kind, 'sw': [[hx, round(w, 3)] for hx, w in sw],
                      'before': [M[m]['n'] + ' | ' + M[m]['bn'] for m in old[:10]],
                      'after': [M[order[j]]['n'] + ' | ' + M[order[j]]['bn'] for j in new[:10]]}
    s['cr'] = new; n += 1
    if kind != 'v85': s['bsw'] = [[hx, round(w, 3)] for hx, w in sw]
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
open(P, 'w').write(h)
if '--report' in sys.argv: json.dump(rep, open(sys.argv[sys.argv.index('--report') + 1], 'w'), indent=1, ensure_ascii=False)
print('matrank v95: re-ranked', n, 'sets with back colour + partner tie-break + motif')
