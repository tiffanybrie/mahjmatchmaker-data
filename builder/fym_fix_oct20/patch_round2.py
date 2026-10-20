"""FYM Oct 20 round 2 (staged; Tiffany/main session publishes).
Usage: python3 builder/fym_fix_oct20/patch_round2.py <site_dir> <out_dir>
  site_dir: copy of the live FYM artifact files (index.html + bundles), e.g. scratchpad/fym-oct20
  out_dir : staged copy (site_dir copied there first), e.g. scratchpad/fym-oct20b
Fixes:
 1. Retired mats (rt:true, e.g. OMM Liberty) show a "Retired" label in the mat-door grid / door search (matBtn) and the mat search list (#msr).
 2. Hide Luxe "Bougie Bee" imperfect-sale duplicate.
 3. Hide (and flag in builder/fym_flags/mat_photo_flags.json): Mahj Squad Pink Floral Chinoiserie (corner crop; store has only
    corner crops + table scenes) and Middle & Main Grandmother quilt mats Betty / Martha / Kathryn (store has only angled porch-table shots).
 4. Colour families re-derived from config/mat-color-overrides.json (Tiffany's calls + "also") + config/mat-gallery-crosstags.json,
    the same way the Mat Gallery v4 builds its sections, mapped onto the existing FYM chips. Holiday mats: mf=[] (holiday only), hol=true.
    Locked mats (locks.json) get their locked mf updated in the same commit (Tiffany's colour calls are the approval).
 5. assets/tiles/album/index.json: Petalée -> petalee-pile.jpg, Classic Tortoise -> classic-tortoise-zoom.jpg (match locks.json).
Every string replace asserts its match count. Data is edited via json raw_decode of `const D=`.
"""
import sys, os, json, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..')) + '/'
sys.path.insert(0, REPO + 'scripts/colors')
import matcolors as MC

SITE, OUT = sys.argv[1], sys.argv[2]
shutil.copytree(SITE, OUT, dirs_exist_ok=True)
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
rep = {'retired_mats': [], 'hidden': [], 'locks_changed': [], 'color': {'changed': [], 'holiday_only': [], 'fallback': [], 'kept_not_in_gallery': []}}

# ---------- 2 + 3. hide mats and flag them
HIDE = {
    'luxemahjong.com/bougie-bee-mahjong-mat-imperfect-sale': ('Bougie Bee', 'duplicate',
        'imperfect-sale duplicate of luxemahjong.com/bougie-bee-mahjong-mat (Tiffany Oct 20)'),
    'mahjsquadshop.com/pink-chinoiserie-mahjong-mat-pink-floral-neoprene-mahjongg-mat-pink-chintz-mahj-mat-colorful-floral-mahj-ongg-mat-spring-1':
        ('Pink Floral Chinoiserie', 'partial_crop', 'corner crop, full mat not shown; assets/mats/gallery has the same crop and the Shopify '
         'products.json (8 photos, checked Oct 20) has only corner crops and table scenes with racks/tiles, no clean flat full-mat photo'),
    'www.middleandmainmahjong.com/grandmother-kathryn-vintage-quilt-mat-copy': ('Grandmother "Betty" Vintage Quilt', 'no_flat_photo',
        'quilt mat shot at an angle on a porch table with a lamp; store products.json (checked Oct 20) has no flat product photo'),
    'www.middleandmainmahjong.com/grandmother-martha-vintage-quilt-mat': ('Grandmother "Martha" Vintage Quilt', 'no_flat_photo',
        'quilt mat shot at an angle on a porch table with a lamp; store products.json (checked Oct 20) has no flat product photo'),
    'www.middleandmainmahjong.com/grandmother-kathryn-vintage-quilt-mat': ('Grandmother "Kathryn" Vintage Quilt', 'no_flat_photo',
        'quilt mat shot at an angle on a porch table with a lamp; store products.json (checked Oct 20) has no flat product photo'),
}
for mid, (nm, flag, note) in HIDE.items():
    o = M[mid]
    assert o['n'] == nm, (mid, o['n'])
    o['hid'] = True
    FLAGS[mid] = {'name': o['n'], 'brand': o['bn'], 'flag': flag, 'note': note}
    rep['hidden'].append([mid, o['n'], o['bn'], flag])
    lk = LOCKS['mats'].get(mid)
    if lk and lk.get('hid') is not True:
        rep['locks_changed'].append([mid, 'hid', lk.get('hid'), True]); lk['hid'] = True

# ---------- 4. colour families (Mat Gallery v4 sections -> FYM chips)
XT = json.load(open(REPO + 'config/mat-gallery-crosstags.json'))
man = json.load(open(REPO + 'site/livepatch/matgallery/manifest.json'))   # gallery img slug -> catalog key
inv = {v: k for k, v in man.items()}
FLORALS, FLORALS_ONLY = set(XT.get('florals', [])), set(XT.get('florals_only', []))
XPRIM, TONALFIX, HOLOFF, JUNGLE = XT.get('primary_fix', {}), XT.get('tonal_fix', {}), XT.get('holiday_off', {}), XT.get('jungle', {})
XALSO = {}
for c_, imgs_ in XT['also'].items():
    for i_ in imgs_: XALSO.setdefault(i_, []).append(c_)
TONAL = ('neutral', 'earthy', 'dark', 'bw')
VALID = {'pink', 'red', 'orange', 'yellow', 'green', 'teal', 'blue', 'purple', 'neutral', 'earthy', 'dark', 'bw', 'pastel', 'brights',
         'florals', 'animal', 'holiday', 'multi'}
SEC = {'brown': 'earthy', 'gold': 'yellow', 'peach': 'orange', 'coral': 'orange', 'mustard': 'yellow'}


def gallery_sections(img, key):
    """Same as site/livepatch/matgallery/build_v4.py _sections() (mood layer pastel/brights is not needed: FYM has no such chips)."""
    r = MC.get(key)
    if r is None: return None
    if img in HOLOFF or img in JUNGLE:
        base = HOLOFF.get(img) or JUNGLE[img]
        out = list(base) + [a for a in XALSO.get(img, []) if a not in base]
        return [c for c in out if c in VALID]
    if r.get('holiday'): return ['holiday']
    out = [XPRIM.get(img) or r.get('gallery_primary') or SEC.get(r['primary'], r['primary'])]
    for a in (r.get('also', []) or []) + XALSO.get(img, []):
        a = SEC.get(a, a)
        if a in VALID and a not in out: out.append(a)
    out = [c for c in out if c in VALID]
    if img in TONALFIX:
        fix = TONALFIX[img]
        out = (fix + [c for c in out[1:] if c not in TONAL and c not in fix]) if out and out[0] in TONAL else [c for c in out if c not in TONAL] + fix
    if img in FLORALS_ONLY: return ['florals']
    return out


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


for mid, o in M.items():
    img = inv.get(mid)
    old = list(o.get('mf') or [])
    secs = gallery_sections(img, mid) if img else None
    if img is None:
        if o.get('hol') and old:
            new = []; rep['color']['holiday_only'].append([mid, o['n'], old])
        else:
            new = old; rep['color']['kept_not_in_gallery'].append([mid, o['n'], old])
    elif secs == ['holiday']:
        o['hol'] = True; new = []
        rep['color']['holiday_only'].append([mid, o['n'], old])
    else:
        if secs is not None: o['hol'] = False
        new = to_fym(secs or [])
        if not new:   # florals / multi / pastel-only in the gallery: fall back to the mat's own colours (primary + secondaries)
            r = MC.get(mid) or {}
            new = to_fym(([r['primary']] if r.get('primary') not in (None, 'multi') else []) + list(r.get('secondary') or []))[:3] or old
            rep['color']['fallback'].append([mid, o['n'], secs, new])
    if new != old:
        o['mf'] = new; rep['color']['changed'].append([mid, o['n'], old, new])
    lk = LOCKS['mats'].get(mid)
    if lk is not None and lk.get('mf') != o['mf']:
        rep['locks_changed'].append([mid, 'mf', lk.get('mf'), o['mf']]); lk['mf'] = o['mf']

rep['retired_mats'] = [[k, o['n'], o['bn'], bool(o.get('hid'))] for k, o in M.items() if o.get('rt')]
assert M['www.ohmymahjong.com/liberty-mat-w-tube']['rt'] is True
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]

# ---------- 1. Retired label: mat-door grid / door search (matBtn) and mat search list (#msr)
R("function matBtn(id){", "const MN=id=>M[id].rt?M[id].n.replace(/\\s*\\(retired\\)/i,''):M[id].n;/* name without '(retired)' when the Retired pill shows */\nfunction matBtn(id){")
R("function matBtn(id){return `<button type=\"button\" data-dmat=\"${esc(id)}\"><img src=\"${matTh(id)}\" alt=\"\" loading=\"lazy\"><span>${esc(M[id].n)}</span><small>${esc(M[id].bn||'')}</small></button>`;}",
  "function matBtn(id){return `<button type=\"button\" data-dmat=\"${esc(id)}\"><img src=\"${matTh(id)}\" alt=\"\" loading=\"lazy\"><span>${esc(MN(id))}</span><small>${esc(M[id].bn||'')}</small>${M[id].rt?'<b class=\"rtd\">Retired</b>':''}</button>`;}")
R("<span><b>${esc(M[id].n)}</b><small>${esc(M[id].bn||'')}${M[id].alt?' · '+esc(M[id].alt.replace(/^Also available/,'also')):''}</small></span></button>`",
  "<span><b>${esc(MN(id))}</b><small>${esc(M[id].bn||'')}${M[id].alt?' · '+esc(M[id].alt.replace(/^Also available/,'also')):''}</small>${M[id].rt?'<em class=\"rtd\">Retired</em>':''}</span></button>`")
R("/* Oct 20 */\n", "/* Oct 20 */\n.rtd{display:inline-block;margin-top:2px;font:700 10px var(--body);font-style:normal;color:#fff;background:#8a7579;border-radius:999px;padding:2px 7px;letter-spacing:.02em}\n.msr .rtd{margin:3px 0 0 6px}\n")

open(os.path.join(OUT, 'index.html'), 'w').write(h)
json.dump(LOCKS, open(LOCKS_P, 'w'), indent=1, ensure_ascii=False)
json.dump(FLAGS, open(FLAGS_P, 'w'), indent=1, ensure_ascii=False)

# ---------- 5. album tile index matches the locked album photos
AIX_P = REPO + 'assets/tiles/album/index.json'
AIX = json.load(open(AIX_P))
for nm, fn in (('Petalée', 'assets/tiles/album/petalee-pile.jpg'), ('Classic Tortoise', 'assets/tiles/album/classic-tortoise-zoom.jpg')):
    assert nm in AIX, nm
    assert os.path.exists(REPO + fn), fn
    assert any(v['set'] == nm and v['src'] == fn for v in LOCKS['tiles'].values()), (nm, fn)
    if AIX[nm]['file'] != fn:
        AIX[nm].setdefault('prev_file', AIX[nm]['file']); AIX[nm]['file'] = fn
        AIX[nm]['note'] = (AIX[nm].get('note', '') + ' | Oct 20: file = locked FYM album photo (locks.json)').strip(' |')
json.dump(AIX, open(AIX_P, 'w'), indent=1, ensure_ascii=False)

json.dump(rep, open(os.path.join(HERE, 'round2_report.json'), 'w'), indent=1, ensure_ascii=False)
c = rep['color']
print('ok', len(h), '| hidden', len(rep['hidden']), '| retired mats', len(rep['retired_mats']), '| mf changed', len(c['changed']),
      '| holiday-only', len(c['holiday_only']), '| fallback', len(c['fallback']), '| not in gallery (kept)', len(c['kept_not_in_gallery']),
      '| locks updated', len(rep['locks_changed']))
