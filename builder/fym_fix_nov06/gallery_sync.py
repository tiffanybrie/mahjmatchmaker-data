"""Mat Gallery <- Find Your Mat-ch sync (Nov 6 2026; Tiffany 1:22am: the gallery is NOT kept up, Dapper 2 not marked Retired).
Every FYM release now rebuilds the gallery from that release (site/livepatch/fym-preview-oct21/README.md release steps; gate [159b]).

What it does (idempotent; rows it wrote before are replaced):
 1. Drafts one config/mat-gallery-extra-rows.json row (added = 'fym-<version>-sync') for every VISIBLE FYM mat that has no gallery row
    (matched like gate [90]: FYM key, product URL or name + brand). Skipped: '#side-b' second listings, House of Hearts Studio
    (Tiffany Oct 25: "FYM only for now"), crosstags remove_mats imgs/brands (Mahjong Studios), non-partners not on
    builder/fym_flags/nonpartner_allow.json (gate [13] would fail them anyway).
 2. Exports each mat's FYM photo at 640px to assets/mats/gallery/<img>.webp (fym_photos.py reads the website copy's mc packs from
    the fym-site-preview checkout, no network).
 3. Sections = the mat's FYM colour families in FYM order (FYM carries her colour calls), mapped to gallery sections by measuring
    the 640px photo (scripts/colors/build_accents.py measure()): FYM 'blue' -> Teal & Aqua when the photo measures more teal than
    blue; FYM 'dark' -> Earthy when it measures more earthy than dark; a mat with no tonal tag gets Pastels or Brights by lightness
    and saturation. Holiday mats (FYM hol) -> ['holiday'] only (holiday rule); FYM ayr / wfh mats are added to the late-calls
    also_year_round / works_for_holiday lists (they are her calls, already applied in FYM). eye = 0, so build_v5.py's measured
    also-colour pass and accents run on them like any catalog mat, and her late calls are re-applied last as always.
Then: python3 scripts/colors/build_accents.py; python3 site/livepatch/matgallery/build_v6.py <FYM index.html> ... (see README).
Usage: python3 builder/fym_fix_nov06/gallery_sync.py <FYM website index.html> <fym-site checkout> [--write]
       (dry run without --write: prints what it would add)"""
import sys, os, io, json, re, subprocess, unicodedata, tempfile, collections
from PIL import Image
import numpy as np
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO + 'scripts/colors')
from fym_photos import FymPhotos
from families import _hls

IDX, CHECKOUT = sys.argv[1], sys.argv[2]
WRITE = '--write' in sys.argv
h = open(IDX).read(); i = h.index('const D=') + 8; D, _ = json.JSONDecoder().raw_decode(h, i); M = D['mats']
VER = re.search(r'fym-(v\d+)', os.path.abspath(IDX)).group(1)
TAG = f'fym-{VER}-sync'
GAL = REPO + 'site/livepatch/matgallery/'
XP = REPO + 'config/mat-gallery-extra-rows.json'
X = json.load(open(XP))
old_rows = [a for a in X['rows'] if str(a.get('added', '')).endswith('-sync') and str(a.get('added', '')).startswith('fym-')]
X['rows'] = [a for a in X['rows'] if a not in old_rows]

# --- the gallery as build_v5 makes it today (without rows from an earlier run of this script) ---
json.dump(X, open(XP, 'w'), indent=1, ensure_ascii=False)
try:
    out = subprocess.run([sys.executable, GAL + 'build_v5.py', REPO + 'builder/fym_fix_oct20/mat_audit_report.csv', GAL + 'phash_pairs_oct20.json'],
                         capture_output=True, text=True, check=True, cwd=GAL).stdout
finally:
    pass
G = json.loads(re.search(r'<script type="application/json">(.*?)</script>', out, re.S).group(1).replace('<\\/', '</'))

nz = lambda x: re.sub(r'[^a-z0-9]', '', ''.join(c for c in unicodedata.normalize('NFD', str(x or '')) if not unicodedata.combining(c)).lower())
slug = lambda x: re.sub(r'[^a-z0-9]+', '-', unicodedata.normalize('NFD', str(x)).encode('ascii', 'ignore').decode().lower()).strip('-')
import urllib.parse as up


def nu(u):
    u = str(u or '')
    if '/discount/' in u and 'redirect=' in u:
        u = re.sub(r'^(https?://[^/]+).*$', r'\1', u) + up.unquote(u.split('redirect=', 1)[1].split('&')[0])
    return re.sub(r'^https?://(www\.)?', '', u.split('?')[0].split('#')[0]).rstrip('/').replace('/products/', '/')


MAN = json.load(open(GAL + 'manifest.json'))
N53 = json.load(open(GAL + 'new53_rows.json'))['manifest']
RA = {a['gallery_id']: a['fym_key'] for a in json.load(open(GAL + 'retired_additions_oct20.json'))}
RA.update({a['img']: a['key'] for a in X['rows']})
GK = lambda im: MAN.get(im) or N53.get(im) or RA.get(im)
GKS = {GK(r[0]) for r in G}; GU = {nu(r[3]) for r in G if r[3]}; GN = {nz(r[1]) + '|' + nz(r[2]) for r in G}
USED = {r[0] for r in G} | set(MAN) | {a['img'] for a in X['rows']}
XT = json.load(open(REPO + 'config/mat-gallery-crosstags.json'))
RMI, RMB = set(XT['remove_mats'].get('imgs', [])), set(XT['remove_mats'].get('brands', []))
RMK = {MAN[i_] for i_ in RMI if i_ in MAN}
import csv as _csv  # the gallery's own dedupe (Oct 20, hidden_oct20.csv): a catalog mat it folded into its twin stays out (e.g. Britt Mills
DUPK = {MAN[r['img']] for r in _csv.DictReader(open(GAL + 'hidden_oct20.csv')) if r['reason'].startswith('duplicate') and r['img'] in MAN}  # neoprene = leatherette photo)
NPA = json.load(open(REPO + 'builder/fym_flags/nonpartner_allow.json'))
PARTNERS = {nz(b) for b in NPA['partners']}  # same lockout as fym_gate.py [9]/[13]
MATCHED = {x[0] for s in D['sets'] if (s.get('album') or s.get('sb')) and not (s.get('hid') or D['tiles'].get(s['tile'], {}).get('hid')) for x in s['m']}
GALLERY_SKIP_BRANDS = {'House of Hearts Studio': 'Tiffany Oct 25 11:06: add ALL its mats to FYM, "FYM only for now"'}
POV = json.load(open(REPO + 'config/mat-gallery-photo-overrides.json'))['mats']
CFIX = json.load(open(REPO + 'config/mat-gallery-sync-colour-fixes.json'))['mats']
CACHE = os.path.join(tempfile.gettempdir(), 'gallery-photo-cache'); os.makedirs(CACHE, exist_ok=True)


def photo_override(k):
    src = POV[k]['src']
    if src.startswith('http'):
        fn = os.path.join(CACHE, re.sub(r'[^A-Za-z0-9._-]', '_', src.split('/')[-1]))
        if not os.path.exists(fn):
            subprocess.run(['curl', '-sSf', '-o', fn, src], check=False)
        return open(fn, 'rb').read() if os.path.exists(fn) and os.path.getsize(fn) > 1000 else None
    return open(REPO + src, 'rb').read()


HOLDS = json.load(open(REPO + 'config/mat-gallery-photo-holds.json'))['mats']
LATE_P = REPO + 'config/tiffany-color-notes/2026-10-20-late-calls.json'
LATE = json.load(open(LATE_P))

# measure() from build_accents without running that script's main body
src = open(REPO + 'scripts/colors/build_accents.py').read()
ns = {'__file__': REPO + 'scripts/colors/build_accents.py'}
exec(compile(src.split('\nout = {')[0], 'build_accents_head', 'exec'), ns)
measure, pick = ns['measure'], ns['pick']


def mood(im):
    """Nov 6 (QA round 2: pale mats and dark solids came out Brights): tags for a mat with no tonal tag yet.
    HSV over the whole photo minus a pure-white background and the black peel-corner flap:
      solid (>= 80% of pixels within ~30 RGB of the median colour)  -> 'simple'
      dark (mean value < 0.45)                                        -> 'dark'
      pastel (80th-pct saturation < 0.5 and mean value >= 0.72)       -> 'pastel'
      otherwise                                                       -> 'brights'"""
    rgb = np.asarray(im.convert('RGB').resize((96, 96))).astype(float)
    hsv = np.asarray(im.convert('RGB').resize((96, 96)).convert('HSV')).astype(float) / 255
    S, V = hsv[..., 1], hsv[..., 2]
    keep = ~(((S < 0.04) & (V > 0.97)) | (V < 0.12))
    if keep.sum() < 50: keep = np.ones_like(V, bool)
    med = np.median(rgb[keep], axis=0); solid = float((np.abs(rgb[keep] - med).max(1) < 30).mean()) >= 0.8
    v, s80 = float(V[keep].mean()), float(np.percentile(S[keep], 80))
    out = ['simple'] if solid else []
    if v < 0.45: out.append('dark')
    elif s80 < 0.5 and v >= 0.72: out.append('pastel')
    elif not solid: out.append('brights')
    return out


def hue_checks(im):
    """Nov 6 QA round 2: the family measurement reads cream/beige as 'orange' and FYM reads magenta as 'purple'.
    Returns (saturated-orange share, peach share, magenta share) over the non-white pixels."""
    hsv = np.asarray(im.convert('RGB').resize((96, 96)).convert('HSV')).astype(float)
    H, S, V = hsv[..., 0] * 360 / 255, hsv[..., 1] / 255, hsv[..., 2] / 255
    keep = ~(((S < 0.08) & (V > 0.9)) | (V < 0.12)); n = max(int(keep.sum()), 1)
    org = ((H >= 8) & (H <= 45) & (S > 0.45) & (V > 0.45) & keep).sum() / n
    yel = ((H >= 45) & (H <= 65) & (S > 0.4) & (V > 0.5) & keep).sum() / n
    peach = ((H >= 5) & (H <= 33) & (S > 0.22) & (V > 0.7) & keep).sum() / n  # 'Orange & Peach': soft peach counts, cream (hue ~40, low sat) does not
    soft_y = ((H >= 45) & (H <= 65) & (S > 0.18) & (V > 0.75) & keep).sum() / n
    soft_o = ((H >= 5) & (H <= 45) & (S > 0.18) & (V > 0.75) & keep).sum() / n
    mag = ((H >= 300) & (H <= 345) & (S > 0.4) & (V > 0.4) & keep).sum() / n
    return float(org), float(peach), float(mag), float(yel), float(soft_o), float(soft_y)


AFX_P = REPO + 'config/mat-accent-photo-fixes.json'
AFX = json.load(open(AFX_P))
AFX['mats'] = {i_: v_ for i_, v_ in AFX['mats'].items() if not str(v_.get('src', '')).startswith('gallery_sync')}  # rebuilt each run
skipped = collections.Counter(); rows = []; P = FymPhotos(CHECKOUT, os.path.relpath(os.path.abspath(IDX), CHECKOUT))
late_add = {'works_for_holiday': [], 'also_year_round': []}
for k, m in M.items():
    if m.get('hid') or '#side-b' in k: continue
    us = {nu(m.get('u0')), nu(m.get('u')), nu(k)} - {''}
    if k in GKS or us & GU or (nz(re.sub(r'\s*\(retired\)', '', m['n'], flags=re.I)) + '|' + nz(m.get('bn'))) in GN or (nz(m['n']) + '|' + nz(m.get('bn'))) in GN:
        continue
    bn = m.get('bn')
    if bn in GALLERY_SKIP_BRANDS: skipped[bn + ' (FYM only for now)'] += 1; continue
    if bn in RMB or k in RMK: skipped['removed brand/mat'] += 1; continue
    if k in DUPK: skipped['gallery duplicate (hidden_oct20.csv)'] += 1; continue
    if k in HOLDS: skipped['gallery photo hold (config/mat-gallery-photo-holds.json)'] += 1; continue
    partner = bool(m.get('pa')) or nz(bn) in PARTNERS or bn in NPA['brands'] or k in NPA['mats'] or str(m.get('u', '')).startswith(NPA['shopmy_prefix']) or k in MATCHED
    if not partner: skipped['non-partner not allowed'] += 1; print('  not allowed (gate [13] lockout):', bn, '|', m['n']); continue
    raw = photo_override(k) if k in POV else P.get(m['f'])
    if raw is None: skipped['no FYM photo'] += 1; continue
    name = re.sub(r'\s*\(retired\)\s*$', '', m.get('dn') or m['n'], flags=re.I).strip()
    img = slug(bn) + '--' + slug(name)[:70]
    base_img, n_ = img, 2
    while img in USED: img = f'{base_img}-{n_}'; n_ += 1
    USED.add(img)
    im = Image.open(io.BytesIO(raw)).convert('RGB')
    if k in POV and POV[k].get('crop'):
        W_, H_ = im.size; x0, y0, x1, y1 = POV[k]['crop']; im = im.crop((int(x0 * W_), int(y0 * H_), int(x1 * W_), int(y1 * H_)))
    im.thumbnail((640, 640))  # shrinks only: a small photo stays at its native size, never upscaled
    tmp = os.path.join(tempfile.gettempdir(), img + '.webp'); im.save(tmp, 'WEBP', quality=84)
    acc, sh = pick(measure(tmp))
    secs = []
    for c in (m.get('mf') or []):
        if c == 'blue': c = 'teal' if sh.get('teal', 0) > sh.get('blue', 0) else 'blue'
        elif c == 'dark': c = 'earthy' if sh.get('earthy', 0) > sh.get('dark', 0) else 'dark'
        if c not in secs: secs.append(c)
    if not secs:
        secs = [max((f for f in sh if f in ('pink', 'red', 'orange', 'yellow', 'green', 'teal', 'blue', 'purple', 'neutral', 'earthy', 'dark')), key=lambda f: sh[f], default='neutral')]
    for t_ in mood(im):
        if t_ == 'dark' and any(c in ('dark', 'earthy', 'bw') for c in secs): continue
        if t_ in ('pastel', 'brights') and any(c in ('neutral', 'earthy', 'dark', 'bw') for c in secs): continue
        if t_ not in secs: secs.append(t_)
    eye_ = 0
    org_, peach_, mag_, yel_, softo_, softy_ = hue_checks(im)
    prim_ = (m.get('mf') or [None])[0]  # FYM's first colour survives the cream test when the photo has >= 20% soft tint of it (pastel yellow tie-dye)
    if org_ < 0.04 and peach_ < 0.12 and not (prim_ == 'orange' and softo_ >= 0.2):  # no real orange in the photo: an FYM/measured 'orange' is cream or beige
        secs = [c for c in secs if c != 'orange'] or ['neutral']
        AFX['mats'][img] = {'drop': ['orange'], 'gallery_only': True, 'src': f'gallery_sync {TAG}', 'why': f'saturated orange {org_:.0%}, peach {peach_:.0%} of the photo (cream/beige read as orange)'}
    if yel_ < 0.04 and not (prim_ == 'yellow' and softy_ >= 0.2):  # cream/ivory read as yellow: never a yellow section or accent
        secs = [c for c in secs if c != 'yellow'] or ['neutral']
        AFX['mats'].setdefault(img, {'drop': [], 'gallery_only': True, 'src': f'gallery_sync {TAG}', 'why': ''})
        AFX['mats'][img]['drop'] = sorted(set(AFX['mats'][img]['drop']) | {'yellow'}); AFX['mats'][img]['why'] += f' saturated yellow {yel_:.0%} (cream read as yellow)'
    if mag_ >= 0.15 and 'pink' not in secs and 'holiday' not in secs:  # magenta reads 'purple' in FYM: pink leads when it is the main colour
        secs = (['pink'] + secs) if (secs and secs[0] == 'purple' and mag_ >= 0.25) else (secs[:1] + ['pink'] + secs[1:])
    if not secs or secs[0] in ('pastel', 'brights', 'simple', 'dark'):  # a colour must lead: best measured colour that survived the cream tests
        _gone = set(AFX['mats'].get(img, {}).get('drop', []))
        _best = max((f for f in sh if f in ('pink', 'red', 'orange', 'yellow', 'green', 'teal', 'blue', 'purple', 'neutral', 'earthy') and f not in _gone and f not in secs), key=lambda f: sh[f], default='neutral')
        secs = [_best] + secs
    if k in CFIX: secs = list(CFIX[k]['secs']); eye_ = 1
    if eye_:  # a by-eye fix that leaves out orange/yellow: the measured cream/gold 'orange'/'yellow' must not come back as an accent either
        _dr = [c for c in ('orange', 'yellow') if c not in secs]
        if _dr:
            AFX['mats'].setdefault(img, {'drop': [], 'gallery_only': True, 'src': f'gallery_sync {TAG}', 'why': ''})
            AFX['mats'][img]['drop'] = sorted(set(AFX['mats'][img]['drop']) | set(_dr)); AFX['mats'][img]['why'] += ' by-eye colour fix'
    if img in AFX['mats'] and str(AFX['mats'][img].get('src', '')).startswith('gallery_sync'):  # a colour the final sections keep is never also dropped
        AFX['mats'][img]['drop'] = [c for c in AFX['mats'][img]['drop'] if c not in secs]
        if not AFX['mats'][img]['drop']: AFX['mats'].pop(img)  # Claude photo-review colour fix (config/mat-gallery-sync-colour-fixes.json)
    hol = bool(m.get('hol'))
    if secs == ['holiday']: hol = True  # a colour fix moved it INTO Holiday (photo clearly shows Christmas)
    if hol and not m.get('ayr'):
        secs = ['holiday']
    elif hol and m.get('ayr'):
        late_add['also_year_round'].append((img, f"{bn} {name}", [c for c in secs if c != 'holiday']))
        secs = [c for c in secs if c != 'holiday'] + ['holiday']
    if m.get('wfh') and not hol:
        late_add['works_for_holiday'].append((img, f"{bn} {name}", k))
    code = re.sub(r'^https?://(www\.)?mahjmatchmaker\.com', '', m.get('dc') or '') if m.get('pa') else ''
    rows.append({'img': img, 'key': k, 'name': name, 'brand': bn, 'url': '' if m.get('rt') else (m.get('u') or ''), 'code': code, 'secs': secs,
                 'img_commit': 'PENDING', 'eye': eye_, 'added': TAG, 'ret': 1 if m.get('rt') else 0,
                 'note': f"{TAG} (gallery_sync.py): photo = {('override ' + POV[k]['src']) if k in POV else ('FYM ' + VER + ' ' + m['f'])} (<= 640px, never upscaled); sections = FYM colours {m.get('mf')} mapped by the measured photo"
                         f" (shares {dict(sorted(sh.items(), key=lambda kv: -kv[1])[:4])}){'; holiday' if hol else ''}{('; colour fix: ' + CFIX[k]['why']) if k in CFIX else ''}; measured also-colours + accents by build_v5.py.",
                 '_tmp': tmp})

print(f'{VER}: {len(rows)} gallery rows to add (previous {TAG}-style rows replaced: {len(old_rows)})')
print('  by brand:', dict(collections.Counter(r['brand'] for r in rows).most_common()))
print('  holiday:', sum(1 for r in rows if r['secs'] == ['holiday']), ' retired:', sum(r['ret'] for r in rows))
print('  skipped:', dict(skipped))
print('  late-calls adds:', {k: [x[1] for x in v] for k, v in late_add.items()})
if WRITE:
    for a in old_rows:  # webps of rows an earlier run wrote and this run no longer makes
        if a['img'] not in {r['img'] for r in rows} and os.path.exists(REPO + f"assets/mats/gallery/{a['img']}.webp"):
            os.remove(REPO + f"assets/mats/gallery/{a['img']}.webp")
    for r in rows:
        os.replace(r.pop('_tmp'), REPO + f"assets/mats/gallery/{r['img']}.webp")
    X['rows'] += rows
    json.dump(X, open(XP, 'w'), indent=1, ensure_ascii=False)
    wfh = LATE['works_for_holiday']
    for img, nm, k in late_add['works_for_holiday']:
        if img not in wfh['imgs']:
            wfh['imgs'].append(img); wfh.setdefault('names', {})[img] = nm + f' (FYM wfh flag = her call; added by {TAG})'
    ayr = LATE['also_year_round']['mats']
    for img, nm, secs in late_add['also_year_round']:
        ayr.setdefault(img, {'name': nm, 'sections': secs, 'note': f'FYM ayr flag (her call); added by {TAG}'})
    json.dump(LATE, open(LATE_P, 'w'), indent=1, ensure_ascii=False)
    json.dump(AFX, open(AFX_P, 'w'), indent=1, ensure_ascii=False)
    print('written', len(rows), 'rows + webps; img_commit = PENDING until the webps are committed; build_v6.py fills it from git (the commit that added the file)')
else:
    for r in rows: os.remove(r['_tmp'])
    json.dump(dict(X, rows=X['rows'] + old_rows), open(XP, 'w'), indent=1, ensure_ascii=False)  # dry run: leave the config as it was
