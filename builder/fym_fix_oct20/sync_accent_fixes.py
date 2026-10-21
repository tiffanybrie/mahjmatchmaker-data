"""Mirror Claude's photo accent fixes (config/mat-accent-photo-fixes.json, Oct 21) from Mat Gallery v5 into a staged FYM build.
Usage: python3 builder/fym_fix_oct20/sync_accent_fixes.py <fym_dir> [gallery_html]
Only the mats listed in the fixes file are re-derived (mf / mt / ha / hol / sh), with the same mapping as the round-3 colour sync
(gallery row -> FYM chips: teal->blue, earthy->dark, bw->dark+neutral; sh = measured share pooled per chip, using the FIXED shares).
As a safety check it re-derives every other gallery mat too and reports any that would change (should be 0; nothing else is written).
Locked mats get mf/mt/hol updated in builder/fym_flags/locks.json (same rule as round 3: gallery colours are the approved source)."""
import sys, os, json, re
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
GAL = REPO + 'site/livepatch/matgallery/'
FYMD = sys.argv[1]
GHTML = sys.argv[2] if len(sys.argv) > 2 else GAL + 'matgallery-v5.html'
IDX = os.path.join(FYMD, 'index.html')
h = open(IDX).read(); i = h.find('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h, i); M = D['mats']
G = json.loads(re.search(r'<script type="application/json">(.*?)</script>', open(GHTML).read(), re.S).group(1).replace('<\\/', '</'))
man = json.load(open(GAL + 'manifest.json')); N53 = json.load(open(GAL + 'new53_rows.json'))
img2key = dict(man); img2key.update(N53['manifest'])
img2key.update({a['gallery_id']: a['fym_key'] for a in json.load(open(GAL + 'retired_additions_oct20.json'))})
img2key.update({a['img']: a['key'] for a in json.load(open(REPO + 'config/mat-gallery-extra-rows.json'))['rows']})
RAWACC = json.load(open(REPO + 'config/mat-accent-colors.json'))
PFIX = json.load(open(REPO + 'config/mat-accent-photo-fixes.json'))['mats']
ACC = {}
for img, v in RAWACC['mats'].items():
    sh = dict(v['shares'])
    for a, b in PFIX.get(img, {}).get('move', {}).items():
        x = sh.pop(a, 0); sh[b] = round(sh.get(b, 0) + x, 1)
    for a in PFIX.get(img, {}).get('drop', []):
        sh.pop(a, None)
    ACC[img] = sh
LOCKS_P = REPO + 'builder/fym_flags/locks.json'; LOCKS = json.load(open(LOCKS_P))
FYM = ['pink', 'red', 'orange', 'yellow', 'green', 'blue', 'purple', 'neutral', 'dark']
TO_FYM = {'teal': ['blue'], 'aqua': ['blue'], 'navy': ['blue'], 'earthy': ['dark'], 'brown': ['dark'], 'black': ['dark'], 'bw': ['dark', 'neutral'],
          'white': ['neutral'], 'ivory': ['neutral'], 'cream': ['neutral'], 'gold': ['yellow'], 'coral': ['orange'], 'peach': ['orange'],
          'lavender': ['purple'], 'mustard': ['yellow']}
FROM = {f: [f] + [g for g, v in TO_FYM.items() if f in v] for f in FYM}


def to_fym(cols, skip=()):
    out = []
    for c in cols:
        for x in TO_FYM.get(c, [c]):
            if x in FYM and x not in out and x not in skip: out.append(x)
    return out


def derive(r):
    secs, acc, cop, hacc, shr = r[5], r[8], r[9], r[10], ACC.get(r[0], {})
    if secs == ['holiday']:
        mf, mt, ha, hol = [], [], to_fym(hacc), True
    else:
        prim = to_fym([secs[0]] + list(cop)); also = to_fym(secs[1:], prim); ac = to_fym(acc, prim + also)
        mf, mt, ha, hol = prim + also + ac, [0] * len(prim) + [1] * len(also) + [2] * len(ac), to_fym(hacc, prim + also + ac), False
    return mf, mt, ha, hol, [round(sum(shr.get(g, 0) for g in FROM[f]), 1) for f in mf]


ALIAS = ('mahj-mood--beyond-the-ribbon-four-winds-social-collab-mat-benefitting-pink-fund-pre-order-ships-end-of-december',
         'four-winds-social--fws-x-mahj-mood-collab-beyond-the-ribbon')
rep = {'fixed': [], 'other_would_change': [], 'locks_changed': []}
for r in G:
    img = ALIAS[1] if (r[0] == ALIAS[0] and r[2] == 'Four Winds Social') else r[0]
    k = img2key.get(img)
    if k not in M: continue
    o = M[k]; mf, mt, ha, hol, sh = derive(r)
    cur = (o.get('mf'), o.get('mt'), o.get('ha') or [], bool(o.get('hol')), o.get('sh'))
    new = (mf, mt, ha, hol, sh)
    if img not in PFIX:
        if cur != new: rep['other_would_change'].append([o['n'], cur, new])
        continue
    rep['fixed'].append([o['n'], o['bn'], {'mf': [cur[0], mf], 'mt': [cur[1], mt], 'ha': [cur[2], ha], 'sh': [cur[4], sh]}])
    o['mf'], o['mt'], o['hol'], o['sh'] = mf, mt, hol, sh
    if ha: o['ha'] = ha
    else: o.pop('ha', None)
    lk = LOCKS['mats'].get(k)
    if lk is not None:
        for f, v in (('mf', mf), ('mt', mt), ('hol', hol)):
            if f in lk and lk[f] != v: rep['locks_changed'].append([k, f, lk[f], v]); lk[f] = v
open(IDX, 'w').write(h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[e:])
json.dump(LOCKS, open(LOCKS_P, 'w'), indent=1, ensure_ascii=False)
json.dump(rep, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'accent_fix_sync_report.json'), 'w'), indent=1, ensure_ascii=False)
print('fixed', len(rep['fixed']), '| locks updated', len(rep['locks_changed']), '| other mats that would change (not written)', len(rep['other_would_change']))
for n, b, d in rep['fixed']:
    print(f"  {b} | {n}: mf {d['mf'][0]} -> {d['mf'][1]}  sh {d['sh'][0]} -> {d['sh'][1]}")
for x in rep['other_would_change'][:10]:
    print('  OTHER', x)
