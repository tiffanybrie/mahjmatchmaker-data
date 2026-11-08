"""FYM 1.18 (Nov 7 2026): new TILES-FOR-A-MAT ranking (mat door, tile step). Gate [168] (tilerank_check.py).
Tiffany Nov 7 10:33pm (screenshot): mat door -> OMM Lotus Cove (pink/green/teal lotus + koi on pink) -> about 10 deep it suggests
Halloween tile sets (white tiles, black/orange faces): "horribly matching tiles".

WHY IT WAS BAD (diagnosis): setsForMat0() ordered a mat's tile sets by the mat's POSITION inside each set's s.rank (the tiles door's
mat list). A position is not a score: "Lotus Cove is mat #29 of 1,713 for Hocus Pocus" only says it beats most mats for that set
(Hocus Pocus's measured 'back' was #a2cab0 sage, its real backs are black), not that Hocus Pocus suits Lotus Cove. Themed sets were
never demoted on this side (v95 only demotes themed MATS), neutral/white sets rank every pastel mat high, and the deck put EVERY
album set ahead of every catalog set (Sunday Blues / Classic Jade before pink catalog sets for a pink mat).

NEW SCORE (one number per mat x set, same scale for every set):
 back   0.38  how much of the mat is the tile BACK colour (back = the dominant tile colour). Back = config/tableview-back-colors.json
              (checked by eye; Malachite #3d4a3d) > config/fym-tilerank-nov07.json backs > v95 bsw > v85 back. Neutral backs
              (white/ivory/black/grey) count at ~1/3 for a colourful mat (a white set never wins by default).
 accent 0.17  the set's layer/face colours (v95 bsw face part + v85 photo swatches, neutrals and back-like shades dropped) on the mat.
 cover  0.30  how much of the mat's OWN colour (neutrals dropped) shows up in the set (back full, accents 3/4): a pink/green mat
              gets nothing from black/orange faces.
 two    0.10  Tiffany's two-colour coordination: mat carries the back colour AND a face/layer colour of another hue.
 comp   0.05  her complement rule: back hue opposite the mat's dominant hue, only when the mat also carries a set colour.
 + coordinated brand pair (config/fym-coordinated.json) +0.30 (and never theme-demoted), album set +0.02, partner tiles +0.02, motif +0.06 only when the colour
   score is already >= 0.42 (Nov 7 8:07pm: motif lifts a mat that fits, never leads).
 Themed sets (Halloween, July 4th, Easter, Hanukkah) and holiday sets (page BACKG.Holiday): -5 (bottom) for any mat without that
 theme (holiday sets: only holiday / works-for-holiday mats; holiday mats get +0.08 for holiday sets). Her picks stay first (app).
OUTPUT: D.tso[order index] = the mat's top TOPN visible sets, packed 2 base-36 chars per D.sets index (best first); D.tsoB = indices
of themed + holiday sets (always below the list for a mat they are not listed for). The app's setsForMat0 uses D.tso when present
(else the old s.rank position), and tAll() sorts album + catalog sets as ONE list by that order (BCAP brand cap still runs).
The tiles door (s.cr, mats-for-tiles) is NOT changed: she is happy with it; --compare prints how this scorer's mats-for-tiles top 10
overlaps s.cr for a sample.
Usage: python3 tilerank_v118.py <build_dir> [--report out.json] [--compare]"""
import sys, os, json, re
import numpy as np
from skimage.color import rgb2lab, deltaE_ciede2000
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
TOPN = 120
MARK = '/*v118 tilerank*/'


def load(p):
    h = open(p).read(); i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); return h, i, end + i, D


def backg(h):
    i = h.index('const BACKG=') + 12; return json.JSONDecoder().raw_decode(h[i:])[0]


def lab(hx): return rgb2lab(np.array([[[int(hx[k:k + 2], 16) / 255 for k in (1, 3, 5)]]]))[0, 0]


def ceff(L):  # chroma, lifted for dark colours (navy, forest, malachite read 'low chroma' but have a clear hue)
    c = np.hypot(L[..., 1], L[..., 2]); return c * (1 + np.clip((45 - L[..., 0]) / 45, 0, 1) * .6)


def cw(L): return np.clip((ceff(L) - 6) / 14, 0, 1)   # 0 = neutral (white/ivory/grey/black), 1 = clearly coloured


def hue(L): return np.degrees(np.arctan2(L[..., 2], L[..., 1])) % 360


def family(hx):
    """Colour family of one hex, same names as the mats' mf (teal counts as green AND blue)."""
    L = lab(hx); c = float(ceff(L)); h = float(hue(L)); l = float(L[0])
    if c < 9: return {'neutral'} if l >= 38 else {'dark'}
    if l >= 75 and c < 30 and (h >= 330 or h < 62): return {'pink', 'orange'} if h >= 30 and h < 62 else {'pink', 'purple'} if h >= 330 else {'pink'}   # blush / peach / pastel pink
    if h >= 345 or h < 40: return {'pink'} if (l >= 58 and h < 40 and (h >= 345 or h < 30)) or (h >= 345 and l >= 50) else {'red'} | ({'pink'} if l >= 50 else set())
    if h < 70: return {'orange'} if not (l < 50 and c < 40) else {'dark', 'orange'}
    if h < 105: return {'yellow'} if l >= 60 else {'yellow', 'dark'}
    if h < 170: return {'green'}
    if h < 240: return {'green', 'blue'}
    if h < 295: return {'blue'} if l < 75 or c > 25 else {'blue', 'purple'}
    return {'purple'} if l < 72 else {'purple', 'pink'}


def theme_re(cfg):
    return {k: re.compile(p, re.I) for k, p in cfg['themed'].items()}


def model(B, D, h):
    """Everything the scorer needs, from the build + configs."""
    cfg = json.load(open(REPO + '/config/fym-tilerank-nov07.json'))
    TV = json.load(open(REPO + '/config/tableview-back-colors.json'))
    C = json.load(open(REPO + '/config/fym-colour-oct25.json'))
    MOm = json.load(open(REPO + '/config/fym-motifs-oct26.json'))['motifs']; MOm = {**MOm, **cfg['motifs']}
    CO = {k: set(v) for k, v in json.load(open(REPO + '/config/fym-coordinated.json')).items() if not k.startswith('_')}
    BG = backg(h); HOL = set(BG.get('Holiday', []))
    TH = theme_re(cfg); NT = set(cfg['not_themed'])
    M, T, S, O = D['mats'], D['tiles'], D['sets'], D['order']
    vis = [n for n, s in enumerate(S) if not s.get('hid') and not (T.get(s['tile']) or {}).get('hid')]

    def theme(name):
        if name in NT: return None
        for k, r in TH.items():
            if r.search(name): return k

    def motifs(name): return {k for k, p in MOm.items() if re.search(p, name, re.I)}
    sets = {}
    for n in vis:
        s = S[n]; sl = s['slug']
        if sl in TV and isinstance(TV[sl], dict) and TV[sl].get('back'): bk, src = TV[sl]['back'], 'tableview'
        elif sl in cfg['backs']: bk, src = cfg['backs'][sl], 'tilerank-config'
        elif s.get('bsw'): bk, src = s['bsw'][0][0], 'bsw'
        elif (C['sets'].get(sl) or {}).get('back'): bk, src = C['sets'][sl]['back'], 'v85'
        elif (C['sets'].get(sl) or {}).get('sw'): bk, src = C['sets'][sl]['sw'][0][0], 'v85sw'
        else: bk, src = s.get('tc') or '#f3f1ea', 'tc'
        Lb = lab(bk)
        acc = []
        bsw = s.get('bsw') or []
        if bsw:   # v95: back part sums to .8, faces .2: faces = entries after the back part
            tot = 0; k = 0
            while k < len(bsw) and tot < .79: tot += bsw[k][1]; k += 1
            acc += [[hx, w * 2.0] for hx, w in bsw[k:]]
        acc += [[hx, w] for hx, w in ((C['sets'].get(sl) or {}).get('sw') or [])]
        A, W = [], []
        for hx, w in acc:
            L = lab(hx)
            if cw(L) < .45 or w < .03: continue
            if float(deltaE_ciede2000(L[None], Lb[None])[0]) < 12: continue
            if any(float(deltaE_ciede2000(L[None], a[None])[0]) < 6 for a in A):
                W[[float(deltaE_ciede2000(L[None], a[None])[0]) < 6 for a in A].index(True)] += w; continue
            A.append(L); W.append(w)
        W = np.array(W, float); W = W / W.sum() if len(W) else W
        th = 'holiday' if s['name'] in HOL else theme(s['name'])
        sets[n] = {'back': bk, 'src': src, 'Lb': Lb, 'A': np.array(A).reshape(-1, 3), 'Aw': W, 'theme': th,
                   'mot': motifs(s['name']), 'alb': not s.get('cat'), 'pa': bool((T.get(s['tile']) or {}).get('pa')),
                   'co': CO.get(sl, set()), 'fam': family(bk)}
    mats = {}
    for k, m in M.items():
        if m.get('hid') or k not in set(O): continue
        sw = m.get('ms') or (C['mats'].get(k) or {}).get('sw')
        if not sw: continue
        L = np.array([lab(hx) for hx, _ in sw]); s_ = np.array([w for _, w in sw], float); s_ = s_ / s_.sum()
        c = cw(L); q = s_ * (.2 + .8 * c); q = q / q.sum()
        mc = float((s_ * c).sum()); p = s_ * c; p = p / p.sum() if p.sum() > .05 else q
        th = theme(m['n'])
        mats[k] = {'L': L, 's': s_, 'q': q, 'p': p, 'mc': mc, 'theme': th, 'hol': bool(m.get('hol')), 'wfh': bool(m.get('wfh')),
                   'mot': motifs(m['n'])}
    return {'sets': sets, 'mats': mats, 'HOL': HOL, 'BG': BG, 'vis': vis}


K = lambda d: np.exp(-(d / 13.0) ** 2)


def score_set(st, MD, keys):
    """Scores of every mat in keys for one set (vector)."""
    mats = MD['mats']
    allL = np.concatenate([mats[k]['L'] for k in keys]); seg = np.cumsum([0] + [len(mats[k]['L']) for k in keys])
    n = len(allL)
    db = deltaE_ciede2000(np.repeat(st['Lb'][None], n, 0), allL)
    kb = K(db)
    nA = len(st['A'])
    if nA:
        da = deltaE_ciede2000(np.repeat(st['A'], n, 0), np.tile(allL, (nA, 1))).reshape(nA, n); ka = K(da)
    cwb = float(cw(st['Lb'])); hb = float(hue(st['Lb']))
    out = np.zeros(len(keys)); parts = []
    for j, k in enumerate(keys):
        m = mats[k]; a, b = seg[j], seg[j + 1]
        kbj = kb[a:b]
        backCov = float((m['q'] * kbj).sum())
        nb = .22 + .55 * (1 - m['mc'])                       # neutral back: counts ~1/3 for a colourful mat, more for a neutral mat
        backFit = min(1.0, backCov / .30) * (nb + (1 - nb) * cwb)
        if nA:
            kaj = ka[:, a:b]
            pres = np.minimum(1.0, (kaj * m['q'][None]).sum(1) / .12)
            accFit = float((st['Aw'] * pres).sum())
            cover = float((m['p'] * np.maximum(kbj * (.35 + .65 * cwb), kaj.max(0) * .75)).sum())
        else:
            pres = np.zeros(0); accFit = 0.0
            cover = float((m['p'] * kbj * (.35 + .65 * cwb)).sum())
        two = 0.0
        if nA and cwb >= .5 and backCov >= .12:
            hA = hue(st['A']); dh = np.abs((hA - hb + 180) % 360 - 180)
            other = pres[(dh > 35)]
            if len(other): two = min(min(1.0, backCov / .25), float(other.max()))
        comp = 0.0
        dom = int(np.argmax(m['p'])); Ld = m['L'][dom]
        if cwb >= .6 and float(cw(Ld)) >= .6:
            dh = abs((float(hue(Ld)) - hb + 180) % 360 - 180)
            if dh >= 140 and (accFit >= .3 or cover >= .3): comp = 1.0
        v = .38 * backFit + .17 * accFit + .30 * cover + .10 * two + .05 * comp
        if st['mot'] & m['mot'] and v >= .42: v += .06
        co = k in st['co']
        if co: v += .30
        if st['alb']: v += .02
        if st['pa']: v += .02
        th = None if co else st['theme']   # the brand made this mat for this themed set (e.g. Bam! Gingham x Hocus Pocus)
        if th == 'holiday':
            if m['hol']: v += .08
            elif not m['wfh']: v -= 5
        elif th:
            if m['theme'] != th: v -= 5
            else: v += .15
        out[j] = v
        parts.append((round(backFit, 3), round(accFit, 3), round(cover, 3), round(two, 2), comp))
    return out, parts


def score_all(B, D, h):
    MD = model(B, D, h)
    keys = sorted(MD['mats']); SC = {}; PT = {}
    for n, st in MD['sets'].items():
        v, parts = score_set(st, MD, keys); SC[n] = v; PT[n] = parts
    return MD, keys, SC, PT


def pack(ix): return ''.join(np.base_repr(i, 36).rjust(2, '0').lower() for i in ix)


JS_P_OLD = 'const p=SO?(SO.indexOf(i)<0?1e9:SO.indexOf(i)):(ix<0?1e9:s.rank.indexOf(ix));'
JS_P_NEW = (MARK + 'const TQ=TSO(ix);const p=TQ?(TQ.has(i)?TQ.get(i):(1e6+(TSOB.has(i)?1e6:0)+Math.max(0,ix<0?1e5:s.rank.indexOf(ix)))):'
            'SO?(SO.indexOf(i)<0?1e9:SO.indexOf(i)):(ix<0?1e9:s.rank.indexOf(ix));')
JS_HELP = (MARK + 'const TSOC={},TSOB=new Set(D.tsoB||[]);function TSO(ix){if(!D.tso||ix<0||!D.tso[ix])return null;if(TSOC[ix])return TSOC[ix];'
           'const s=D.tso[ix],m=new Map();for(let k=0;k<s.length;k+=2)m.set(parseInt(s.substr(k,2),36),k/2);return TSOC[ix]=m;}'
           'function TSOM(a){return D.tso?a.slice().sort((x,y)=>x.p-y.p):a;}\n')
JS_T_OLD = 'BCAP([...g.alb,...g.cat],NOK,r=>TB(r.s))'
JS_T_NEW = 'BCAP(TSOM([...g.alb,...g.cat]),NOK,r=>TB(r.s))'


def patch_js(h):
    if MARK in h: return h, False
    for o in (JS_P_OLD, JS_T_OLD): assert h.count(o) == 1, 'anchor not found once: ' + o[:50]
    h = h.replace(JS_P_OLD, JS_P_NEW).replace(JS_T_OLD, JS_T_NEW)
    a = h.index('function setsForMat(id)'); h = h[:a] + JS_HELP + h[a:]
    return h, True


def main():
    B = sys.argv[1]; P = B + '/index.html'
    h, i, end, D = load(P)
    MD, keys, SC, PT = score_all(B, D, h)
    O = D['order']; OI = {k: j for j, k in enumerate(O)}
    vis = MD['vis']; tso = [''] * len(O)
    rep = {}
    for jk, k in enumerate(keys):
        col = sorted(vis, key=lambda n: -SC[n][jk])[:TOPN]
        tso[OI[k]] = pack(col)
        if '--report' in sys.argv:
            rep[k] = [[D['sets'][n]['name'], round(float(SC[n][jk]), 3), MD['sets'][n]['back']] for n in col[:15]]
    D['tso'] = tso
    D['tsoB'] = sorted(n for n, st in MD['sets'].items() if st['theme'])
    h2 = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
    h2, did = patch_js(h2)
    open(P, 'w').write(h2)
    if '--report' in sys.argv: json.dump(rep, open(sys.argv[sys.argv.index('--report') + 1], 'w'), indent=0, ensure_ascii=False)
    print(f"tilerank v118: {len(keys)} mats ranked over {len(vis)} sets (top {TOPN} stored, {len(D['tsoB'])} themed/holiday sets bottom); "
          f"js {'patched' if did else 'already patched'}; +{(len(h2) - len(h)) // 1024} KB")
    if '--compare' in sys.argv:   # mats-for-tiles: this scorer vs s.cr (the tiles door she is happy with)
        ov = []
        for n in vis[:: max(1, len(vis) // 40)]:
            cr = [O[j] for j in (D['sets'][n].get('cr') or [])][:10]
            mine = [keys[j] for j in np.argsort(-SC[n])[:10]]
            ov.append(len(set(cr) & set(mine)))
        print('mats-for-tiles top-10 overlap with s.cr (sample of', len(ov), 'sets): mean', round(float(np.mean(ov)), 2), 'dist', sorted(ov))


if __name__ == '__main__':
    main()
