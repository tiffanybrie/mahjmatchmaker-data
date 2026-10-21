"""FYM Oct 21 (evening), STAGED ONLY: Tiffany's final holiday cleanup, mirrored from Mat Gallery v5.
Usage: python3 builder/fym_fix_oct21/holiday_cleanup.py <fym_dir> [gallery_html]
Her final definition: Holiday = ONLY Christmas, Hanukkah and winter snowy/ski scenes (late-calls holiday_definition).
 1. Re-derives mf / mt / ha / hol / sh from the gallery row (same mapping as builder/fym_fix_oct20/sync_accent_fixes.py) for the
    mats this cleanup touches: late-calls corrections dated Oct 21 for Pumpkin Plaid, Pumpkin Patch (out of Holiday), Sugarplum,
    Frosted Flowers (into Holiday), plus every also_year_round / works_for_holiday mat. Every other gallery mat is re-derived as a
    safety check and reported if it would change (nothing else is written).
 2. also_year_round (flag ayr): hol=true AND their colours in single-colour chips (mf/mt/sh from the gallery colour sections).
 3. works_for_holiday (flag wfh): stays year-round (hol=false); setsForMat offers holiday tile sets for it (ok = hol || wfh).
    late-calls works_for_holiday.fym_keys covers FYM-only mats (OMM Dapper 2 is held out of the gallery).
 4. Locked mats get mf/mt/hol updated in builder/fym_flags/locks.json (gallery colours / her calls are the approved source).
"""
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
LATE = json.load(open(REPO + 'config/tiffany-color-notes/2026-10-20-late-calls.json'))
AYR = set(LATE.get('also_year_round', {}).get('mats', {}))
WFH = set(LATE.get('works_for_holiday', {}).get('imgs', []))
WFH_KEYS = set(LATE.get('works_for_holiday', {}).get('fym_keys', []))
MOVED = {'anders-ruff--pumpkin-plaid-mahjong-mat', 'bam-let-s-mahjong--pumpkin-patch-mahjong-mat-fall-halloween-mahjong-mat',
         'oh-my-mahjong--sugarplum', 'peace-love-mahjong--frosted-flowers'}
TARGET = AYR | WFH | MOVED
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
    """gallery row -> (mf, mt, ha, hol, sh). ['holiday'] = holiday only; 'holiday' among colour sections = also_year_round."""
    secs, acc, cop, hacc, shr = r[5], r[8], r[9], r[10], ACC.get(r[0], {})
    if secs == ['holiday']:
        return [], [], to_fym(hacc), True, []
    hol = 'holiday' in secs
    secs = [c for c in secs if c != 'holiday']; cop = [c for c in cop if c != 'holiday']
    prim = to_fym([secs[0]] + list(cop)); also = to_fym(secs[1:], prim); ac = to_fym(acc, prim + also)
    mf, mt = prim + also + ac, [0] * len(prim) + [1] * len(also) + [2] * len(ac)
    return mf, mt, to_fym(hacc, mf), hol, [round(sum(shr.get(g, 0) for g in FROM[f]), 1) for f in mf]


ALIAS = ('mahj-mood--beyond-the-ribbon-four-winds-social-collab-mat-benefitting-pink-fund-pre-order-ships-end-of-december',
         'four-winds-social--fws-x-mahj-mood-collab-beyond-the-ribbon')
rep = {'changed': [], 'other_would_change': [], 'locks_changed': [], 'flags': {}, 'missing': []}
seen = set()
for r in G:
    img = ALIAS[1] if (r[0] == ALIAS[0] and r[2] == 'Four Winds Social') else r[0]
    k = img2key.get(img)
    if k not in M:
        if img in TARGET: rep['missing'].append(img)
        continue
    o = M[k]; mf, mt, ha, hol, sh = derive(r)
    cur = (o.get('mf'), o.get('mt'), o.get('ha') or [], bool(o.get('hol')), o.get('sh'))
    new = (mf, mt, ha, hol, sh)
    if img not in TARGET:
        if cur != new: rep['other_would_change'].append([o['n'], cur, new])
        continue
    seen.add(img)
    rep['changed'].append([o['n'], o.get('bn'), {'mf': [cur[0], mf], 'mt': [cur[1], mt], 'ha': [cur[2], ha], 'hol': [cur[3], hol], 'sh': [cur[4], sh]}])
    o['mf'], o['mt'], o['hol'], o['sh'] = mf, mt, hol, sh
    if ha: o['ha'] = ha
    else: o.pop('ha', None)
    lk = LOCKS['mats'].get(k)
    if lk is not None:
        for f, v in (('mf', mf), ('mt', mt), ('hol', hol)):
            if f in lk and lk[f] != v: rep['locks_changed'].append([k, f, lk[f], v]); lk[f] = v
# flags: ayr / wfh (cleared everywhere else so a removed name drops out on the next run)
AYRK = {img2key[i] for i in AYR if i in img2key}; WFHK = {img2key[i] for i in WFH if i in img2key} | WFH_KEYS
for k, o in M.items():
    for f, on in (('ayr', k in AYRK), ('wfh', k in WFHK)):
        if on:
            o[f] = True; rep['flags'].setdefault(f, []).append(o['n'])
        else:
            o.pop(f, None)
assert all(M[k].get('hol') for k in AYRK if k in M), 'also_year_round mat not hol'
assert not any(M[k].get('hol') for k in WFHK if k in M), 'works_for_holiday mat is hol'
# UI: holiday tile sets are offered for works_for_holiday mats too (mat door, setsForMat)
OLD = 'const ok=r=>M[id].hol||!HOL.has(r.s.name);'
NEW = 'const ok=r=>M[id].hol||M[id].wfh||!HOL.has(r.s.name);/* Oct 21: works_for_holiday mats (wfh) count as holiday for holiday tile sets */'
pre, post = h[:i], h[e:]
if OLD in post:
    post = post.replace(OLD, NEW); rep['ui'] = 'setsForMat ok patched (hol || wfh)'
elif NEW in post:
    rep['ui'] = 'already patched'
else:
    raise SystemExit('setsForMat ok() not found')
open(IDX, 'w').write(pre + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + post)
json.dump(LOCKS, open(LOCKS_P, 'w'), indent=1, ensure_ascii=False)
json.dump(rep, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'holiday_cleanup_report.json'), 'w'), indent=1, ensure_ascii=False)
print('changed', len(rep['changed']), '| locks', len(rep['locks_changed']), '| other would change (not written)', len(rep['other_would_change']),
      '| missing', rep['missing'], '|', rep['ui'])
for n, b, d in rep['changed']:
    print(f"  {b} | {n}: hol {d['hol'][0]}->{d['hol'][1]}  mf {d['mf'][0]} -> {d['mf'][1]}  ha {d['ha'][1]}")
for f, v in rep['flags'].items(): print(' ', f, v)
for x in rep['other_would_change'][:10]: print('  OTHER', x)
