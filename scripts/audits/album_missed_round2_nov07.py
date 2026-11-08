#!/usr/bin/env python3
"""Album missed-mats ROUND 2 scorer (Nov 7 2026, Tiffany 10:06pm feedback on round 1).

Round 1 capped each album to its top ~12 by score, so a mat that fits MANY sets was offered to one album only, and
the colour score diluted bright multicolour mats. Round 2 re-scores the SAME never-considered pool (same candidate
rules + per-album cutoff as scripts/audits/album_missed_mats_nov07.py) against EVERY live album with no per-album cap:

  back   = share of the mat that is the set's BACK colour (CIEDE2000; back_alt hexes for patterned backs like
           tortoise / speckle), plus a bonus when the mat's DOMINANT colour is the back colour (Sunday Mahjong!)
  hits   = how many of the set's other colours (layers, colour-card faces, tile-photo accents) appear in the mat
           at >= 3.5% each; scored by count, not by share, so a bright multicolour mat is not diluted
  fit    = share of the mat's coloured area that some tile colour explains; unexplained colour is a clash penalty
  tone   = doc 76 gate (clean tiles never on muddy mats, earthy tiles never on neon mats)

Tile profiles = config/tile-tones.json corrected by LOOKING at the album tile photos (PROFILE_FIX below; contact
sheet assets/qa/album-missed-nov07-r2/profiles.jpg).

Usage: python3 scripts/audits/album_missed_round2_nov07.py <albums_html_dir> <fym_index.html> <staged_palettes.json> <out.json>
"""
import json, os, re, sys, collections
import numpy as np
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.insert(0, os.path.join(R, 'scripts/colors')); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import palette as P
from album_missed_mats_nov07 import ALB, CC_KEY, BAN, EXCL, add_date, norm, album_cards, fam_shares

# Corrections from the album tile photos (Nov 7 round 2). back_alt = other shades of a patterned/2-tone back.
PROFILE_FIX = {
    'malachite': {'back_hex': '#445344', 'back_alt': ['#2f3d33', '#5d6e5a'], 'layer_hex': ['#7b3e43', '#d0b1b9'],
                  'tone': 'transitional'},
    'lola': {'back_hex': '#1f5fd0', 'back_alt': ['#176acf', '#3d74d8'], 'layer_hex': ['#b4ccea', '#7f9cc8']},
    'luminaire': {'back_hex': '#c7cce6', 'back_alt': ['#b9b4dc'], 'layer_hex': ['#f2c1c1', '#a59bb5']},
    'solara': {'back_hex': '#e98273', 'back_alt': ['#df6f5f'], 'layer_hex': ['#bb5949', '#9bad8d']},
    'sunday-tile-set': {'back_hex': '#b48739', 'back_alt': ['#a87a2e', '#c39a52'], 'layer_hex': ['#e2cdae']},
    'smith': {'back_hex': '#a95133', 'back_alt': ['#773325', '#8e4128'], 'layer_hex': ['#1f2450', '#9caec2']},
    'tortoise': {'back_hex': '#8a4a1c', 'back_alt': ['#421b10', '#99460c', '#b06a2a'], 'layer_hex': ['#d1bd97'],
                 'tone': 'earthy'},
    'glow-wild': {'back_alt': ['#9b4e38', '#2a1414']},
    'talulah': {'back_hex': '#a4cacb', 'back_alt': ['#b98e7f', '#935f4e'], 'layer_hex': ['#57afad', '#d5b3bb']},
    'heritage': {'back_alt': ['#935233']},
    'heritage-2-0': {'back_alt': ['#d1916d', '#9a4a2f']},
    'willow': {'layer_hex': ['#1c4a67', '#c4a363']},
}
NEAR, MID, FAR = 12, 19, 25
from functools import lru_cache
from skimage.color import deltaE_ciede2000


@lru_cache(maxsize=None)
def _lab(h): return tuple(float(x) for x in P.lab(h))


_DE = {}


def dE(a, b):
    v = _DE.get((a, b))
    if v is None:
        v = _DE[(a, b)] = float(deltaE_ciede2000(np.array([_lab(a)]), np.array([_lab(b)]))[0])
    return v


def prefill(xs, ys):
    """Vectorised CIEDE2000 for every (x, y) pair: the per-pair skimage call made round 2 take minutes."""
    xs = sorted(set(xs)); ys = sorted(set(ys))
    X = np.array([_lab(h) for h in xs]); Y = np.array([_lab(h) for h in ys])
    for i, h in enumerate(xs):
        d = deltaE_ciede2000(np.repeat(X[i:i + 1], len(ys), 0), Y)
        for j, g in enumerate(ys): _DE[(g, h)] = _DE[(h, g)] = float(d[j])


def chroma_of(h):
    L = _lab(h); return float(np.hypot(L[1], L[2])), L[0]


def hue(h):
    L = _lab(h); return float(np.degrees(np.arctan2(L[2], L[1])) % 360)


def near_share(targets, pal, near=NEAR, mid=MID, far=FAR):
    s = 0.0
    for h, w in pal:
        d = min(dE(t, h) for t in targets)
        s += w if d < near else (w * .6 if d < mid else (w * .25 if d < far else 0))
    return s


def profile(slug, T, CC, tkey):
    t = dict(T[tkey]); t.update(PROFILE_FIX.get(slug, {}))
    cc = CC.get(CC_KEY.get(slug, ''), {})
    back = [t['back_hex']] + list(t.get('back_alt') or [])
    layers = list(t.get('layer_hex') or [])
    faces = [h for _, h in cc.get('faces', [])]
    # tile-photo accents: chromatic palette colours that are not the back (white tile bodies / neutrals skipped)
    acc = []
    for h, w in t.get('palette') or []:
        c, L = chroma_of(h)
        if c < 14 or L > 90: continue
        if min(dE(b, h) for b in back) < 14: continue
        acc.append(h)
    keys = []
    for h in layers + faces + acc:
        if chroma_of(h)[0] < 10: continue
        if all(dE(h, k) >= 10 for k in keys) and min(dE(b, h) for b in back) >= 12: keys.append(h)
    allc = back + layers + faces + [h for h, _ in t.get('palette') or []]
    return {'back': back, 'keys': keys[:8], 'all': allc, 'tone': t.get('tone'), 'back_neutral': chroma_of(back[0])[0] < 14}


def back_tol(prof):
    """Pastel / near-neutral backs get tighter tolerances, or every cream or blush mat 'matches' them."""
    c, L = chroma_of(prof['back'][0])
    if c < 12: return (8, 12, 16)
    if c < 26 and L > 68: return (9, 14, 19)
    return (12, 19, 25)


def score(prof, pal):
    if not pal: return 0, {}
    tot = sum(w for _, w in pal) or 1; pal = [(h, w / tot) for h, w in pal]
    tol = back_tol(prof)
    back = near_share(prof['back'], pal, *tol)
    # hue-family credit for a chromatic back: lighter/darker shades of the same hue still read as the back colour
    bc, bL = chroma_of(prof['back'][0])
    if bc >= 26:
        bh = hue(prof['back'][0]); fam = 0.0
        for h, w in pal:
            c, L = chroma_of(h)
            if c >= 22 and .5 * bc <= c <= 1.6 * bc and abs((hue(h) - bh + 180) % 360 - 180) < 18: fam += w
        back = max(back, .7 * fam)
    chrom = [(h, w) for h, w in pal if chroma_of(h)[0] >= 15]
    cs = sum(w for _, w in chrom)
    # dominant-colour = back (Sunday Mahjong: a butterscotch mat for butterscotch backs), graded by distance
    dom_back = 0.0
    for h, w in sorted(pal, key=lambda x: -x[1])[:2]:
        if w < .15: continue
        d = min(dE(b, h) for b in prof['back'])
        dom_back = max(dom_back, 1.0 if d < tol[0] - 2 else (.5 if d < tol[1] else 0))
    # multicolour credit by COUNT of the set's colours present (>= 3.5% each), never diluted by share
    hits = 0
    for k in prof['keys']:
        if sum(w for h, w in pal if dE(k, h) < 13) >= .035: hits += 1
    tile = prof['back'] + prof['keys']
    bh0 = hue(prof['back'][0]); bc0 = chroma_of(prof['back'][0])[0]

    def explained(h):
        if min(dE(a, h) for a in tile) < 17: return True
        # tonal shades of a chromatic back (a chestnut leather's darker/lighter browns on a wood-back set)
        return bc0 >= 20 and abs((hue(h) - bh0 + 180) % 360 - 180) < 15 and chroma_of(h)[0] <= 1.6 * bc0
    expl = sum(w for h, w in chrom if explained(h))
    unexpl = cs - expl
    fit = expl / cs if cs > .05 else (1.0 if prof['back_neutral'] else .4)
    need_hits = 2 if prof['back_neutral'] else 0
    ok = (back >= .1 and hits >= need_hits) or dom_back >= .5 or (hits >= 2 and fit >= .6) or (hits >= 3 and fit >= .45)
    why = {'back': round(back, 2), 'dom_back': dom_back, 'hits': hits, 'fit': round(fit, 2), 'unexpl': round(unexpl, 2)}
    if not ok: return 0, why
    bw = 1.5 if prof['back_neutral'] else 2.5
    s = bw * min(back, .5) / .5 + 1.0 * dom_back + 1.6 * min(hits, 5) / 5 + 1.0 * fit
    s -= 3.0 * max(0, unexpl - .2)
    ch = (sum(chroma_of(h)[0] * w for h, w in chrom) / cs) if cs else 0
    if ch > 35 and prof['tone'] == 'clean' and hits >= 2: s += .5  # bright multicolour mat on a bright set
    t = 1.0
    if prof['tone'] == 'clean' and ch < 16 and not prof['back_neutral']: t = .4
    if prof['tone'] == 'earthy' and ch > 50: t = .45
    why['ch'] = round(ch)
    return round(max(0, s) * t, 3), why


def candidates(fym_html, staged_pc):
    s = open(fym_html).read(); i = s.find('const D='); D, _ = json.JSONDecoder().raw_decode(s[i + 8:])
    fym_dir = os.path.dirname(fym_html); out = []
    for k, m in D['mats'].items():
        ad = add_date(m.get('add'))
        if not ad: continue
        if m.get('hid') or m.get('rt') or m.get('oos') or m.get('so') or m.get('parked') or m.get('u_dead'): continue
        if BAN.search(m.get('bn', '') + ' ' + m.get('n', '')) or EXCL.search(m.get('n', '') + ' ' + k): continue
        if m.get('bn') == 'Splash of Color': continue
        out.append({'key': k, 'name': m['n'], 'brand': m['bn'], 'src': 'FYM ' + m.get('add'), 'add': ad,
                    'pa': bool(m.get('pa')), 'hol': bool(m.get('hol')) and not m.get('ayr'),
                    'img': os.path.join(fym_dir, m['f']), 'pal': m.get('ms') or [], 'url': m.get('u0') or m.get('u')})
    for f, tag in (('config/fym-shopmy-nov07.json', 'staged ShopMy (never in catalog)'),
                   ('config/fym-amazon-holiday-oct26.json', 'staged Amazon holiday pick (never in catalog)')):
        for m in json.load(open(os.path.join(R, f)))['mats']:
            if m.get('hid') or m['key'] not in staged_pc: continue
            out.append({'key': m['key'], 'name': m['name'], 'brand': m['brand'], 'src': tag, 'add': '11-07', 'pa': False,
                        'hol': bool(m.get('hol')), 'img': os.path.join(R, m['img']), 'pal': staged_pc[m['key']],
                        'url': m.get('u')})
    return out, {x['slug']: x for x in D['sets']}


# Selection used for the by-eye pass (Nov 7): absolute score, near the mat's best album, or an album's top 12.
def select(d, T=4.3, rel=.85, relmin=3.7, floorN=12, floormin=3.0):
    best=collections.defaultdict(float)
    for p in d['pairs']: best[p['key']]=max(best[p['key']],p['score'])
    byA=collections.defaultdict(list)
    for p in d['pairs']: byA[p['album']].append(p)
    rank={}
    for a,ps in byA.items():
        for i,p in enumerate(sorted(ps,key=lambda p:-p['score'])): rank[(a,p['key'])]=i
    out=[]
    for p in d['pairs']:
        s=p['score']; r=rank[(p['album'],p['key'])]
        why = 'abs' if s>=T else 'rel' if (best[p['key']]>=T and s>=relmin and s>=rel*best[p['key']]) else 'floor' if (r<floorN and s>=floormin) else None
        if why: out.append(dict(p, sel=why))
    return out

def main(adir, fym_html, staged_p, out):
    T = json.load(open(os.path.join(R, 'config/tile-tones.json')))['sets']
    CC = json.load(open(os.path.join(R, 'config/colorcards.json')))['sets']
    IDX = json.load(open(os.path.join(R, 'assets/tiles/album/index.json')))
    cands, SETS = candidates(fym_html, json.load(open(staged_p)))
    profs = {slug: profile(slug, T, CC, tk) for slug, (_, tk, _, _) in ALB.items()}
    prefill([h for c in cands for h, _ in c['pal']], [h for p in profs.values() for h in p['back'] + p['keys']])
    albums, pairs = {}, []
    for slug, (iname, tkey, fslug, cut) in ALB.items():
        prof = profs[slug]
        cards = album_cards(os.path.join(adir, slug + '.html'))
        have_n = {norm(c['name']) for c in cards}; have_h = {c['handle'].lower() for c in cards if c['handle']}
        fm = {x[0] for x in (SETS.get(fslug) or {}).get('m', [])} if fslug else set()
        albums[slug] = {'name': iname, 'tile_img': IDX[iname]['file'], 'cutoff': '2026-' + cut, 'live_cards': len(cards),
                        'profile': prof}
        for c in cands:
            if c['add'] <= cut: continue
            h = c['key'].split('/')[-1].lower()
            hid = re.search(r'/listing/(\d+)', c['key']); asin = re.search(r'/dp/([A-Z0-9]{10})', c['key'])
            if c['key'] in fm or norm(c['name']) in have_n or h in have_h or (hid and hid.group(1) in have_h) \
                    or (asin and asin.group(1).lower() in have_h):
                continue
            sc, why = score(prof, c['pal'])
            if sc > 0: pairs.append({'album': slug, 'key': c['key'], 'score': sc, 'why': why})
    mats = {c['key']: {k: c[k] for k in ('name', 'brand', 'src', 'add', 'pa', 'hol', 'img', 'url', 'pal')} for c in cands}
    json.dump({'albums': albums, 'mats': mats, 'pairs': pairs}, open(out, 'w'), indent=0)
    print('candidates', len(cands), 'qualified pairs', len(pairs))


if __name__ == '__main__':
    main(*sys.argv[1:5])
