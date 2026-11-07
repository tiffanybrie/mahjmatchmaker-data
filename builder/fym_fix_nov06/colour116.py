"""FYM 1.16 colour fixes, carried over from the Mat Gallery v6 work (Nov 6 QA round 2; builder/fym_fix_nov06/gallery_sync.py).
FYM tagged cream/beige mats 'orange' or 'yellow' and magenta mats 'purple' only. Same rule as gallery_sync.hue_checks() on the
mat's own FYM photo (the build's mc packs, 96px HSV, white + black removed):
  - 'orange' stays only with >= 4% saturated orange or >= 12% peach (or it is the primary and the photo has >= 20% soft orange tint)
  - 'yellow' stays only with >= 4% saturated yellow (or it is the primary with >= 20% soft yellow tint)
  - >= 15% magenta also counts as pink: pink is added after the primary (or leads, when the primary is purple and magenta >= 25%)
  - the by-eye fixes in config/mat-gallery-sync-colour-fixes.json (gallery sections) set the mat's FYM colours directly
    (teal -> blue, earthy -> dark; mood tags simple/pastel/brights dropped; 'holiday' fixes are not applied here: FYM hol is her call)
NEVER touched: mats whose colours are locked (builder/fym_flags/locks.json mats.mf: approved values, edit only with her OK) and every
mat named in her colour calls (config/tiffany-color-notes/*.json, not Claude's own claude-tags file). Visible ones the rule WOULD
change are listed under 'skipped' (for her OK). mf / mt / sh stay parallel; a dropped
colour's share is removed, an added pink gets its measured magenta share; mt keeps each colour's old tier (0 = the first colour).
Writes config/fym-colour-fixes-v116.json (what changed and why). Idempotent. Usage: python3 colour116.py <build dir>"""
import sys, os, io, json, re, glob, struct, unicodedata
import numpy as np
from PIL import Image
H_ = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(H_, '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read(); i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:])
MCN = int(re.search(r'MCN=(\d+)', h).group(1)); M = D['mats']
LK = json.load(open(REPO + 'builder/fym_flags/locks.json'))['mats']
CFIX = json.load(open(REPO + 'config/mat-gallery-sync-colour-fixes.json'))['mats']
# By-eye FYM colours (QA Nov 6 night, 1.17 item d): kept in this script's own output file under 'eye' and preserved on every run.
# They win over the rule and the gallery fixes. Each one was set after LOOKING at the FYM photo. Gate [163] fails when the rule leaves a
# mat neutral-only, or drops it to one colour from several, without an 'eye' entry.
OUTP = REPO + 'config/fym-colour-fixes-v116.json'
EYE = (json.load(open(OUTP)).get('eye') or {}) if os.path.exists(OUTP) else {}


def slug(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode().lower()
    return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', s)).strip('-')


CALLS = set()  # gallery img slugs + 'brand|name' named anywhere in her colour calls
for f in glob.glob(REPO + 'config/tiffany-color-notes/*.json'):
    if 'claude-tags' in f: continue  # Claude's own photo tags, not her calls
    txt = open(f).read()
    CALLS |= set(re.findall(r'"([a-z0-9-]+--[a-z0-9-]+)"', txt))
    def walk(o):
        if isinstance(o, dict):
            if 'brand' in o and 'name' in o: CALLS.add(slug(o['brand']) + '--' + slug(o['name']))
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(json.load(open(f)))

PK = {}
def photo(f):
    c = int(f.split('/')[1].split('.')[0]) // MCN
    if c not in PK:
        p = f'{B}/mc/{c}.webp'
        if not os.path.exists(p): PK[c] = None
        else:
            raw = open(p, 'rb').read(); n = struct.unpack('<I', raw[-4:])[0]; PK[c] = (raw, json.loads(raw[-4 - n:-4]))
    pk = PK[c]
    if not pk or f not in pk[1]: return None
    a, l = pk[1][f]; return Image.open(io.BytesIO(pk[0][a:a + l])).convert('RGB')


def hue_checks(im):  # = gallery_sync.hue_checks
    hsv = np.asarray(im.resize((96, 96)).convert('HSV')).astype(float)
    H, S, V = hsv[..., 0] * 360 / 255, hsv[..., 1] / 255, hsv[..., 2] / 255
    keep = ~(((S < 0.08) & (V > 0.9)) | (V < 0.12)); n = max(int(keep.sum()), 1)
    org = ((H >= 8) & (H <= 45) & (S > 0.45) & (V > 0.45) & keep).sum() / n
    yel = ((H >= 45) & (H <= 65) & (S > 0.4) & (V > 0.5) & keep).sum() / n
    peach = ((H >= 5) & (H <= 33) & (S > 0.22) & (V > 0.7) & keep).sum() / n
    soft_y = ((H >= 45) & (H <= 65) & (S > 0.18) & (V > 0.75) & keep).sum() / n
    soft_o = ((H >= 5) & (H <= 45) & (S > 0.18) & (V > 0.75) & keep).sum() / n
    mag = ((H >= 300) & (H <= 345) & (S > 0.4) & (V > 0.4) & keep).sum() / n
    return float(org), float(peach), float(mag), float(yel), float(soft_o), float(soft_y)


GMAP = {'teal': 'blue', 'earthy': 'dark', 'bw': 'dark'}
FAM = {'blue', 'pink', 'green', 'dark', 'neutral', 'orange', 'red', 'purple', 'yellow'}
log, skipped = {}, {'locked': [], 'her colour call': [], 'by-eye holiday (FYM hol is her call)': [], 'no photo': []}
for k, m in M.items():
    mf = list(m.get('mf') or [])
    if not mf and k not in CFIX: continue
    name = re.sub(r'\s*\(retired\)\s*$', '', m.get('n', ''), flags=re.I)
    locked = k in LK and 'mf' in LK[k]
    call = slug(m.get('bn')) + '--' + slug(name) in CALLS
    sh = list(m.get('sh') or [None] * len(mf)); sh += [None] * (len(mf) - len(sh))
    shd = dict(zip(mf, sh)); why = []
    if k in EYE:
        new = [c for c in EYE[k]['mf'] if c in FAM]
        if new != mf: why.append('by-eye (FYM QA): ' + EYE[k]['why'])
        mf = new
    elif k in CFIX:
        secs = CFIX[k]['secs']
        if 'holiday' in secs: skipped['by-eye holiday (FYM hol is her call)'].append(k); continue
        new = []
        for c in secs:
            c = GMAP.get(c, c)
            if c in FAM and c not in new: new.append(c)
        if new and new != mf: why.append('by-eye: ' + CFIX[k]['why'])
        mf = new or mf
    else:
        im = photo(m['f']) if m.get('f') else None
        if im is None:
            if 'orange' in mf or 'yellow' in mf: skipped['no photo'].append(k)
            continue
        org, peach, mag, yel, so, sy = hue_checks(im); prim = mf[0] if mf else None
        if 'orange' in mf and org < 0.04 and peach < 0.12 and not (prim == 'orange' and so >= 0.2):
            mf.remove('orange'); why.append(f'orange dropped: saturated orange {org:.1%}, peach {peach:.1%} (cream/beige read as orange)')
        if 'yellow' in mf and yel < 0.04 and not (prim == 'yellow' and sy >= 0.2):
            mf.remove('yellow'); why.append(f'yellow dropped: saturated yellow {yel:.1%} (cream read as yellow)')
        if mag >= 0.15 and 'pink' not in mf and mf:
            mf = (['pink'] + mf) if (mf[0] == 'purple' and mag >= 0.25) else (mf[:1] + ['pink'] + mf[1:])
            shd['pink'] = round(mag * 100, 1); why.append(f'pink added: magenta {mag:.1%} (magenta read as purple only)')
        if not mf: mf = ['neutral']; why.append('nothing left: neutral')
    if not why: continue
    if locked or call:  # reported only: her approved / called colours are never changed here
        if not m.get('hid'): skipped['locked' if locked else 'her colour call'].append({'key': k, 'name': m.get('n'), 'brand': m.get('bn'), 'now': m.get('mf'), 'rule would give': mf, 'why': '; '.join(why)})
        continue
    old = {x: m.get(x) for x in ('mf', 'mt', 'sh')}
    m['mf'] = mf
    mtd = dict(zip(old['mf'] or [], old['mt'] or []))
    m['mt'] = [0 if j == 0 else max(1, mtd.get(c, 1)) for j, c in enumerate(mf)]
    m['sh'] = [shd.get(c) if shd.get(c) is not None else 0.0 for c in mf]
    for kk in ('ha',):  # a combo-only colour that is now a real colour is not listed twice
        if m.get(kk): m[kk] = [c for c in m[kk] if c not in mf] or None
    log[k] = {'name': m.get('n'), 'brand': m.get('bn'), 'hid': bool(m.get('hid')), 'from': old['mf'], 'to': mf, 'why': '; '.join(why)}
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[i + e:]; open(P, 'w').write(h)
json.dump({'about': __doc__.split('\n')[0], 'build': os.path.basename(os.path.abspath(B)), 'eye': EYE, 'changed': log,
           'skipped': skipped}, open(OUTP, 'w'), indent=1, ensure_ascii=False)
vis = [v for v in log.values() if not v['hid']]
c_ = lambda s: sum(1 for v in vis if s in v['why'])
print(f"colour116: changed {len(log)} mats ({len(vis)} visible): orange dropped {c_('orange dropped')}, yellow dropped {c_('yellow dropped')}, "
      f"pink added {c_('pink added')}, by-eye {c_('by-eye')} | skipped " + ', '.join(f'{a} {len(b)}' for a, b in skipped.items()))
