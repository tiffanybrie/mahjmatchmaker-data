"""FYM Oct 21 (afternoon), STAGED ONLY: Tiffany's holiday definition + the low FYM photo bar (CLAUDE.md rule 6, commit 437b26e).
Usage: python3 builder/fym_fix_oct21/holiday_props.py <fym_dir> [gallery_html]
 1. Holiday: every FYM mat whose Mat Gallery v5 row is Holiday-only (secs == ['holiday']) but is not hol in FYM gets mf=[], mt=[],
    hol=true, ha = its measured colours (combo-only), sh=[] (same derive as sync_accent_fixes.py / round 3). Oct 21: Ski Club Red
    Sweater Border (her call), Ski Club Periwinkle Center + Virora Hiverelle (ski/snow photos, her definition). Locked mats get
    mf/mt/hol updated in locks.json (gallery colours are the approved source). Any other gallery-vs-FYM holiday mismatch is reported.
 2. Low photo bar: the 8 mats hidden this morning for no_flat_photo (props/room shots) are un-hidden (hid=None, photo unchanged =
    the fym-oct20e photo) and flagged ok_fym_props; locked mats flagged locked_needs_approval whose photo still shows the mat and
    its colours -> ok_fym_props. Gray Malin (corner close-up, no whole mat) keeps locked_needs_approval.
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
LOCKS_P = REPO + 'builder/fym_flags/locks.json'; LOCKS = json.load(open(LOCKS_P))
FLAGS_P = REPO + 'builder/fym_flags/mat_photo_flags.json'; FLAGS = json.load(open(FLAGS_P))
FYM = ['pink', 'red', 'orange', 'yellow', 'green', 'blue', 'purple', 'neutral', 'dark']
TO_FYM = {'teal': ['blue'], 'aqua': ['blue'], 'navy': ['blue'], 'earthy': ['dark'], 'brown': ['dark'], 'black': ['dark'], 'bw': ['dark', 'neutral'],
          'white': ['neutral'], 'ivory': ['neutral'], 'cream': ['neutral'], 'gold': ['yellow'], 'coral': ['orange'], 'peach': ['orange'],
          'lavender': ['purple'], 'mustard': ['yellow']}


def to_fym(cols):
    out = []
    for c in cols:
        for x in TO_FYM.get(c, [c]):
            if x in FYM and x not in out: out.append(x)
    return out


rep = {'holiday_set': [], 'holiday_mismatch_other': [], 'locks_changed': [], 'unhidden': [], 'flag_ok_fym_props': [], 'flag_kept': []}
for r in G:
    k = img2key.get(r[0])
    if k not in M: continue
    o = M[k]; ghol = r[5] == ['holiday']
    if ghol and not o.get('hol'):
        ha = to_fym(r[10] or [])
        rep['holiday_set'].append([o['n'], o.get('bn'), {'mf': o.get('mf'), 'ha': o.get('ha')}, {'mf': [], 'ha': ha}])
        o['mf'], o['mt'], o['hol'], o['sh'] = [], [], True, []
        if ha: o['ha'] = ha
        else: o.pop('ha', None)
        lk = LOCKS['mats'].get(k)
        if lk is not None:
            for f, v in (('mf', []), ('mt', []), ('hol', True)):
                if f in lk and lk[f] != v: rep['locks_changed'].append([k, f, lk[f], v]); lk[f] = v
    elif bool(o.get('hol')) != ghol:
        rep['holiday_mismatch_other'].append([o['n'], o.get('bn'), r[5], o.get('hol')])

NOTE = 'FYM OK per Tiffany Oct 21 low bar; not clean enough for album cards'
KEEP = {'www.bespokemahjong.com/graymalingamemat': 'corner close-up of the mat (no whole-mat view); rule 6 still hides corner close-ups, waiting on Tiffany'}
for k, f in FLAGS.items():
    fl = f.get('flag')
    if fl == 'no_flat_photo' and str(f.get('note', '')).startswith('Oct 21 QA'):
        o = M[k]; assert o.get('hid') is True, k
        lk = LOCKS['mats'].get(k, {}); assert lk.get('hid') in (None, False), k
        o['hid'] = None; rep['unhidden'].append([o['n'], o.get('bn'), o.get('f')])
    elif fl == 'locked_needs_approval':
        if k in KEEP:
            f['note'] = f.get('note', '') + ' | Oct 21 low bar: kept, ' + KEEP[k]; rep['flag_kept'].append([f['name'], KEEP[k]]); continue
    else:
        continue
    f['flag'] = 'ok_fym_props'; f['was'] = fl; f['note'] = NOTE + ' (was ' + fl + ': ' + f.get('note', '') + ')'
    f.pop('candidate', None) if f.get('candidate') is None else None
    rep['flag_ok_fym_props'].append([f['name'], f['brand'], fl])

open(IDX, 'w').write(h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[e:])
json.dump(LOCKS, open(LOCKS_P, 'w'), indent=1, ensure_ascii=False)
json.dump(FLAGS, open(FLAGS_P, 'w'), indent=1, ensure_ascii=False)
json.dump(rep, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'holiday_props_report.json'), 'w'), indent=1, ensure_ascii=False)
print('holiday set', len(rep['holiday_set']), '| other mismatches', len(rep['holiday_mismatch_other']), '| locks', len(rep['locks_changed']),
      '| unhidden', len(rep['unhidden']), '| ok_fym_props', len(rep['flag_ok_fym_props']), '| kept', len(rep['flag_kept']))
for x in rep['holiday_set'] + rep['holiday_mismatch_other'] + rep['locks_changed'] + rep['unhidden'] + rep['flag_kept']: print(' ', x)
