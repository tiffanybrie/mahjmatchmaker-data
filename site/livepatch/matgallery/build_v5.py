"""Mat Gallery v5 (/mahjong-mats), Oct 20 night. Late Oct 20 (final sort rule): inside a colour section, Tiffany's lead pins, then ONE list
sorted by score high to low (score = measured share of that colour from config/mat-accent-colors.json + 20 if the colour is the mat's
primary; no measurement = 0; ties: primary first, then name), then her tail pins. Mahjong Studios is removed (no brand sort rule).
remove_mats.brands drops whole brands (Mahjong Studios). Tiffany floral:false calls (tiffany-color-notes/2026-10-20-late-calls.json) are enforced.
 v4 plus: 53 new mats from Tiffany's ShopMy shop + partner stores
(new53_rows.json, tagged by Claude's photo review in config/tiffany-color-notes/2026-10-20-new53-claude-tags.json; hidden/duplicate
rows left out), a Simple mood tag (crosstags "simple"; replaces Pastels/Brights), Claude's Pastels->Brights re-check (crosstags
"mood_fix"), and Tiffany's v5 calls (tiffany-color-notes/2026-10-20-v5-calls.json: final_sections + mood_calls, applied last).
Usage: python3 build_v5.py <audit report.csv> <pairs.json> <image commit> > matgallery-v5.html   (writes v5_counts.json)

Mat Gallery v4 (/mahjong-mats), Oct 20 late. v3 plus: Brown & Tan merged into Earthy; tonal re-check (Neutral/Earthy/Dark/B&W, crosstags "tonal_fix");
year-round mats moved out of Holiday (crosstags "holiday_off"); Cognac not retired (no shop button). v3: Same as v2 plus: an Earthy section (muted, low-saturation mats; Tiffany's calls +
Claude's photo picks in config/mat-gallery-crosstags.json "also.earthy"), and within every section the mats whose PRIMARY is that
color come first, "also"-tagged mats below them, Mahjong Studios last of all.

v2 notes:
Changes from v1 (build.py): a mat can sit in several color sections (primary + Tiffany's "also" colors; Multicolor = any mat
tagged multi), retired mats get their own section at the bottom (with a "Hide retired" toggle, default on, that keeps them
out of the color sections), duplicates are collapsed to one card, raw store titles are cleaned, and launch-blocking images
(placeholders, wrong images, no mat in the photo) are hidden.

Inputs: matgallery.html (889 rows, v1 JSON), manifest.json, held-low-98.json, config/mat-color-overrides.json (+ guesses via
scripts/colors/matcolors.py), config/tiffany-color-notes/*.json, and the FYM mat visual audit CSV (argv[1]).
Usage: python3 build_v4.py <audit report.csv> <pairs.json from phash> > matgallery-v4.html
Side outputs: dedupe_oct20.csv, hidden_oct20.csv, v4_counts.json (same folder), and overrides updated in place."""
import json, sys, os, re, csv, html, difflib, glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', '..')
P = lambda *a: os.path.join(ROOT, *a)
AUDIT, PAIRS = sys.argv[1], sys.argv[2]
COMMIT = sys.argv[3] if len(sys.argv) > 3 else '3e8af50f24b40ffdcc7f8c76540feb0b36907f14'  # jsDelivr image base (v5: the commit that adds the new53 webps)
TODAY = '2026-10-20'

t = open(os.path.join(HERE, 'matgallery.html')).read()
F = json.loads(re.search(r'<script type="application/json">(.*?)</script>', t, re.S).group(1).replace('<\\/', '</'))
man = json.load(open(os.path.join(HERE, 'manifest.json')))
held = set(json.load(open(os.path.join(HERE, 'held-low-98.json'))))
XT = json.load(open(P('config/mat-gallery-crosstags.json')))
held -= set(XT['unhold']['imgs'])
FLORALS, FLORALS_ONLY = set(XT.get('florals', [])), set(XT.get('florals_only', []))
XPRIM = XT.get('primary_fix', {})
TONALFIX, HOLOFF = XT.get('tonal_fix', {}), dict(XT.get('holiday_off', {}))
JUNGLE = XT.get('jungle', {})
TONAL = ('neutral', 'earthy', 'dark', 'bw')
XALSO = {}
for col_, imgs_ in XT['also'].items():
    for i_ in imgs_:
        XALSO.setdefault(i_, []).append(col_)
log = lambda *a: print(*a, file=sys.stderr)

# ---------- 1. Tiffany's color calls -> config/mat-color-overrides.json ----------
OV_PATH = P('config/mat-color-overrides.json')
OV = json.load(open(OV_PATH))
G = json.load(open(P('config/mat-color-guesses.json')))['mats']
notes = []
for fn in sorted(glob.glob(P('config/tiffany-color-notes/2026-10-20-*.json'))):
    j_ = json.load(open(fn))
    if str(j_.get('by', '')).startswith('claude'):  # Claude's photo tags are not Tiffany calls
        continue
    for c in j_.get('corrections', []):
        if fn.endswith('-late-calls.json') and not c.get('primary') and 'floral' not in c:
            continue  # also-only late calls (yellow, Oct 20 22:42) are applied in the final late pass only, so Claude's measured also-colours stay
        notes.append(dict(c, _src=os.path.basename(fn)))


def norm(s):
    s = s.lower().replace('&', ' and ').replace('é', 'e').replace('á', 'a')
    s = re.sub(r"[’']", '', s)
    s = re.sub(r'[^a-z0-9]+', ' ', s)
    return ' '.join(w for w in s.split() if w not in ('mahjong', 'mahj', 'mat', 'the', 'and', 'ships', 'rolled', 'neoprene'))


def bnorm(s):
    return re.sub(r'[^a-z]', '', s.lower().replace('&', 'and').replace('mahjongg', 'mahjong').replace('mahjongg', 'mahjong').replace('mah jongg', 'mahjong'))


unmatched = []
applied = []
NOTFLORAL = set()  # Tiffany's floral:false calls (late-calls, Oct 20): never Multicolor Florals, whatever crosstags/overrides say
for c in notes:
    if c.get('img'):
        hits_ = [r for r in F if r[0] == c['img']]
        if not hits_:
            unmatched.append(c); continue
    cn = norm(c['name'])
    best = []
    cs = cn.replace(' ', '')
    for r in F:
        same_brand = c['brand'] != '*' and (bnorm(r[2]) == bnorm(c['brand']) or bnorm(r[2]).startswith(bnorm(c['brand'])) or bnorm(c['brand']).startswith(bnorm(r[2])))
        rn = norm(r[1]); rs = rn.replace(' ', '')
        if len(rs) < 4:
            continue
        if cs == rs: sc = 1.0
        elif cs in rs or (same_brand and rs in cs and len(rs) >= 8): sc = 0.95
        else: sc = max(difflib.SequenceMatcher(None, cs, rs).ratio(), difflib.SequenceMatcher(None, cs, rs[:len(cs)]).ratio() - 0.04)
        if not same_brand:  # other brands (or brand '*') only count on a near-exact name hit
            pre = difflib.SequenceMatcher(None, cs, rs[:len(cs) + 2]).ratio()
            if sc < 0.95 and not (c['brand'] == '*' and pre >= 0.9): continue
            sc = max(sc, pre) - 0.01
        best.append((sc, r))
    best.sort(key=lambda x: -x[0])
    if not c.get('img') and (not best or best[0][0] < 0.8):
        unmatched.append(c); continue
    top = best[0][0] if best else 1.0
    hits = [r for sc, r in best if sc >= top - 1e-9]
    if c.get('img'):
        hits = hits_
    if len(hits) > 1 and top < 1.0:  # several equally-close names: only accept if they are the same mat listed twice
        pass
    for r in hits:
        k = man[r[0]]
        rec = dict(OV['mats'].get(k) or {kk: vv for kk, vv in (G.get(k) or {}).items() if kk not in ('prev', 'conf')})
        cp = c.get('primary')  # no primary = an "also"-only call: keep the mat's current primary
        hol = cp == 'holiday'
        if cp == 'earthy':  # gallery-only section; FYM keeps a plain color family
            rec['gallery_primary'] = 'earthy'; newp = c.get('fym_primary', 'neutral')
        elif cp == 'florals':
            rec['floral'] = True; rec.pop('gallery_primary', None); newp = 'multi'
        elif cp in (None, 'holiday'):
            newp = rec.get('primary', 'multi')
        else:
            rec.pop('gallery_primary', None); newp = cp
        rec.update(primary=newp, holiday=hol or (rec.get('holiday', False) if cp is None else False), skip=False, image=r[0], by='tiffany-chat-' + TODAY)
        rec.setdefault('secondary', []); rec.setdefault('tone', 'blend'); rec.setdefault('src', 'claude-look')
        if c.get('also'):
            rec['also'] = c['also'] if cp else list(dict.fromkeys((rec.get('also') or []) + c['also']))
        if 'floral' in c:
            rec['floral'] = bool(c['floral'])
            if not c['floral']:
                rec['also'] = [a for a in (rec.get('also') or []) if a != 'florals']; NOTFLORAL.add(r[0])
        if c.get('note'):
            rec['note'] = c['note']
        OV['mats'][k] = rec
        applied.append((c['brand'], c['name'], r[1], cp, c.get('also', [])))
OV['updated'] = TODAY
FLORALS -= NOTFLORAL; FLORALS_ONLY -= NOTFLORAL
json.dump(OV, open(OV_PATH, 'w'), indent=1, ensure_ascii=False)
sys.path.insert(0, P('scripts/colors'))
import matcolors as MC  # loads the overrides we just wrote

# ---------- audit CSV ----------
AR = list(csv.DictReader(open(AUDIT)))
inv = {v: k for k, v in man.items()}
by_type = {}
for a in AR:
    if a['mat_id'] in inv:
        by_type.setdefault(a['problem_type'], {})[inv[a['mat_id']]] = a
rename = {}
for img, a in by_type.get('raw store title', {}).items():
    m = re.match(r'rename to "(.*)"', a['suggested_fix'])
    if m:
        rename[img] = m.group(1)

# ---------- 2. names + brands ----------
NAMEFIX = {  # different designs that share one store name (audit: ambiguous names); colorway added from the photo/URL
    'mahj-moon--retro-waves': 'Retro Waves \u2013 Pink & Aqua', 'mahj-moon--retro-waves-2': 'Retro Waves \u2013 Purple',
    'mahj-moon--retro-waves-3': 'Retro Waves \u2013 Orange', 'mahj-moon--palm-beach-american': 'Palm Beach American \u2013 Bermuda',
    'mahj-moon--palm-beach-american-2': 'Palm Beach American \u2013 Harbor', 'virora-mahjong--limoncea-mahjong-mat': 'Limoncea with Flower',
    'britt-mills--soir-e-leatherette': 'Soir\u00e9e Leatherette', 'hip-hip-mahjong--hoppy-east-hare-mahjong-mat': 'Hoppy East-Hare',
    'mahj-mood--beyond-the-ribbon-four-winds-social-collab-mat-benefitting-pink-fund-pre-order-ships-end-of-december': 'Beyond the Ribbon (Pink Fund)',
    'mahj-mood--the-eloise-collection-mat-collab-with-four-winds-social': 'The Eloise Collection',
    'charleston-mahjong-club--reversible-vegan-leather-bight-pink-purple': 'Reversible Vegan Leather \u2013 Bright Pink & Purple',
    'tigre-de-tartan--paige-spearin-mahjong-mat-mahj-and-martinis-special-edition-printing': 'Paige Spearin \u201cMahj and Martinis\u201d',
    'tigre-de-tartan--mahjong-mat-printed-needlepoint-canvas-14-mesh-jard-n-de-los-jefes': 'Jard\u00edn de Los Jefes Needlepoint Canvas',
    'splash-of-color--art-deco-designed-mahjong-mat-green-blue-speakeasy-collection': 'Art Deco Green Blue Speakeasy',
    'my-fair-mahjong--color-wave-cobalt-center-light-blue-scallop': 'Color Wave \u2013 Cobalt Center, Light Blue Scallop'}
# Dead shop links (site scan Oct 20, sitescan/broken.csv). '' = no shop button but NOT retired (still sold somewhere / unknown).
LINKFIX = {**{f'mahjong-by-si--{n}': '' for n in ('gatsby', 'highland-heritage-plaid', 'the-hunt-club', 'the-lodge', 'tracing-the-tides', 'vintage-oxblood-leather')},
           'my-fair-mahjong--confetti-lemon-lime': 'https://myfairmahjong.com/products/mahjong-mat-confetti-33-x-33'}  # Mahjong Co no longer sells mats; no other store found
RETIRE = set()  # only confirmed-gone mats; OMM Cognac is just missing from the store listing (no shop button, not retired)
LINKFIX['oh-my-mahjong--cognac'] = ''
WATCH = {'oh-my-mahjong--cognac'}  # "One to watch": likely retired, not confirmed (no shop button, stays in its color sections)
BRANDFIX = {'Mahj and Moon': 'Mahj & Moon', 'Ozark Mah Jongg': 'Ozark Mahjongg'}


def clean(n):
    n = re.sub(r'\[[^\]]*\]', '', n)
    n = re.sub(r'\([^)]*(33|in\b|waterproof|retired)[^)]*\)', '', n, flags=re.I)
    n = re.sub(r'\(\s*retired\s*\)', '', n, flags=re.I)
    n = re.sub(r'\b(pre[- ]?order|preorder)\b[^|]*', '', n, flags=re.I)
    n = re.sub(r'\bships\s+rolled\b', '', n, flags=re.I)
    n = re.sub(r'\d+(\.\d+)?\s*("|in|inch(es)?)?\s*[x×]\s*\d+(\.\d+)?\s*("|in|inch(es)?|cm)?', '', n, flags=re.I)
    n = re.sub(r'\b\d+\s*(in|cm)\b', '', n, flags=re.I)
    n = re.sub(r'\b(mahjong|mahj)\s+(playing\s+|table\s+)?mats?\b', '', n, flags=re.I)
    n = re.sub(r'\s*[|]\s*', ' | ', n)
    n = re.sub(r'(\s*[-–|:/]\s*)+$', '', n.strip())
    n = re.sub(r'^(\s*[-–|:/]\s*)+', '', n)
    n = re.sub(r'\s*-\s*(-\s*)+', ' - ', n)
    n = re.sub(r'\s+([!?.,])', r'\1', n)
    n = re.sub(r'\s+(Mahjong\s+Playing|Mahjong\s+Game|Mat)$', '', n.strip(), flags=re.I)
    n = re.sub(r'\s{2,}', ' ', n).strip(' -–|:/')
    if n.isupper() and len(n) > 4:
        n = re.sub(r"\b([A-Z])([A-Z']*)\b", lambda m: m.group(1) + m.group(2).lower(), n)
    return n


rows = []
for r in F:
    if r[0] in held:
        continue
    img, name, brand, url, ret, _sec, code = r
    raw = name
    if img in LINKFIX:
        url = LINKFIX[img]
    ret = 1 if (ret or img in RETIRE or re.search(r'\(\s*retired\s*\)', name, re.I) or img in by_type.get('"(retired)" in name but not flagged retired', {})) else 0
    nm = NAMEFIX.get(img) or clean(rename.get(img, name)) or clean(name) or name
    brand = BRANDFIX.get(brand, brand)
    rows.append(dict(img=img, key=man[img], name=nm, raw=raw, brand=brand, url='' if ret else url, ret=ret, code=code, old=_sec))

# v5: Tiffany's permanent excludes (crosstags remove_mats): never in the gallery, whatever a scrape brings in
RM = XT.get('remove_mats', {})
RMI, RMB = set(RM.get('imgs', [])), set(RM.get('brands', []))  # brands: whole-brand removals (Mahjong Studios, Oct 20)
rows = [x for x in rows if x['img'] not in RMI and x['brand'] not in RMB]
removed_mats = [i for i in RM.get('imgs', [])]

# ---------- 3. hide ----------
hidden = {}  # img -> reason


def hide(img, why):
    if img not in hidden:
        hidden[img] = why


R = {x['img']: x for x in rows}
for img in by_type.get('placeholder image', {}):
    if img in R: hide(img, 'placeholder image ("Photo coming soon")')
for img, a in by_type.get('wrong image (shows another mat)', {}).items():
    if img in R: hide(img, 'wrong image: ' + a['detail'])
for img, a in by_type.get('lifestyle/table scene', {}).items():
    if img in R and 'no mat visible' in a['detail']: hide(img, 'image shows no mat: ' + a['detail'])

# ---------- 4. dedupe ----------
groups = []  # (keep, [drop], reason)


def score_keep(x):  # cleanest name and a working URL win
    s = 0
    if x['url']: s += 100
    if x['key'].startswith('alb'): s -= 20
    if re.search(r'ships rolled|\d+\s*x\s*\d+|pre-?order|imperfect|copy', x['raw'] + ' ' + x['key'], re.I): s -= 30
    if re.search(r'mahjong mat', x['raw'], re.I): s -= 5
    if re.search(r'sca_ref|ref=|\?.*aff', x['url'] or ''): s += 3
    s -= len(x['raw']) / 100
    return s


def add_group(imgs, reason, keep=None):
    # a listing hidden for a wrong image never links groups (its photo is another mat's photo)
    imgs = [i for i in dict.fromkeys(imgs) if i in R and not hidden.get(i, '').startswith('wrong')]
    if len(imgs) < 2:
        return
    for g in groups:  # merge overlapping groups
        if set(g['all']) & set(imgs):
            g['all'] = list(dict.fromkeys(g['all'] + imgs)); g['reason'] += '; ' + reason
            if keep: g['keep'] = keep
            return
    groups.append({'all': imgs, 'reason': reason, 'keep': keep})


pairs = json.load(open(PAIRS))
for d, cd, a, b in pairs:
    if d <= 6 and cd <= 5 and a in R and b in R and R[a]['brand'] == R[b]['brand']:
        add_group([a, b], f'same image (phash {d}, color diff {cd})')
# same-brand names that differ only by size / Ships Rolled / Mahjong Mat suffixes
nk = {}
for x in rows:
    k = (bnorm(x['brand']), norm(clean(x['raw'])))
    nk.setdefault(k, []).append(x['img'])
for k, imgs in nk.items():
    if len(imgs) > 1 and k[1] and len({R[i]['raw'] for i in imgs}) == len(imgs) and not any(i in NAMEFIX for i in imgs):  # identical store names = different colorways
        add_group(imgs, 'same name after removing size/Ships Rolled/Mahjong Mat')
# audit-listed duplicates (same mat listed twice / collab under both brands)
for t_ in ('duplicate mat (same/near-identical name in brand)', 'duplicate mat (same image hash)'):
    for img, a in by_type.get(t_, {}).items():
        m = re.search(r'#(\d+)', a['detail'])
        if m:
            other = [inv[b['mat_id']] for b in AR if b['seq'] == m.group(1) and b['mat_id'] in inv]
            if other: add_group([img, other[0]], 'audit: ' + a['detail'][:80])
add_group(['my-fair-mahjong--confetti-green', 'my-fair-mahjong--confetti-lemon-lime'], 'audit: same mat, same photo (Confetti Lemon Lime = Confetti Green)', keep='my-fair-mahjong--confetti-green')
add_group(['four-winds-social--fws-x-mahj-mood-collab-rally-in-pink', 'mahj-mood--rally-in-pink'], 'collab listed under both brands', keep='mahj-mood--rally-in-pink')
add_group(['four-winds-social--fws-x-mahj-mood-eloise', 'mahj-mood--the-eloise-collection-mat-collab-with-four-winds-social'], 'collab listed under both brands', keep='mahj-mood--the-eloise-collection-mat-collab-with-four-winds-social')

dd_rows = []
for g in groups:
    cands = [i for i in g['all'] if i not in hidden]  # a wrong-image listing never wins
    if not cands:
        continue
    keep = g['keep'] if g['keep'] in cands else max(cands, key=lambda i: score_keep(R[i]))
    # wrong-image Peace Love / Let's Mahj On pairs: the hidden one is already out, nothing else to drop
    drops = [i for i in g['all'] if i != keep]
    for i in drops:
        if i not in hidden:
            hide(i, f'duplicate of {keep} ({g["reason"][:90]})')
    dd_rows.append([len(dd_rows) + 1, R[keep]['brand'], keep, R[keep]['name'], R[keep]['url'] or '(retired)', ' | '.join(drops),
                    ' | '.join(R[i]['raw'] for i in drops), ' | '.join('hidden: wrong image' if hidden[i].startswith('wrong') else 'hidden: duplicate' for i in drops), g['reason']])

# ---------- 5. sections ----------
COL = [('pink', 'Pink'), ('red', 'Red'), ('orange', 'Orange & Peach'), ('yellow', 'Yellow & Mustard'), ('green', 'Green'), ('teal', 'Teal & Aqua'),
       ('blue', 'Blue'), ('purple', 'Purple & Lilac'), ('neutral', 'Neutral & Ivory'), ('earthy', 'Earthy'), ('dark', 'Dark & Moody'),
       ('bw', 'Black & White'), ('simple', 'Simple'), ('pastel', 'Pastels'), ('brights', 'Brights'), ('florals', 'Multicolor Florals'), ('animal', 'Animal Prints'),
       ('holiday', 'Holiday'), ('multi', 'Multicolor')]  # 'multi' is retired as a section in v4: never assigned (see sections())
SEC = {'brown': 'earthy', 'gold': 'yellow', 'peach': 'orange', 'coral': 'orange', 'mustard': 'yellow'}
VALID = {c for c, _ in COL}


def sections(x):
    """v4 mood layer: plain Multicolor is retired; every mat with no Neutral/Earthy/Dark/B&W tag lands in Pastels or Brights."""
    out = _sections(x)
    if out == ['holiday']:
        return out
    r = MC.get(x['key']) or {}
    prim_multi = out[0] == 'multi'
    out = [c for c in out if c != 'multi']
    if not any(c in TONAL for c in out) and 'pastel' not in out:
        low = r.get('tone') == 'muted' and (r.get('chroma') or 0) < 0.4  # soft muted mats read pastel, everything else bright
        mood = 'pastel' if low else 'brights'
        out = [mood] + out if (prim_multi or not out) else out + [mood]
    elif prim_multi and 'pastel' in out:
        out = ['pastel'] + [c for c in out if c != 'pastel']
    return out or ['brights']


def _sections(x):
    r = MC.get(x['key'])
    if r is None:
        return [SEC.get(x['old'], x['old'])]
    if x['img'] in HOLOFF or x['img'] in JUNGLE:  # year-round mat that only had the holiday flag / jungle mat (green first)
        base = HOLOFF.get(x['img']) or JUNGLE[x['img']]
        out = list(base) + [a for a in XALSO.get(x['img'], []) if a not in base]
        return [c for c in out if c in VALID]
    if r.get('holiday'):
        return ['holiday']  # holiday mats never appear in color sections
    out = [XPRIM.get(x['img']) or r.get('gallery_primary') or SEC.get(r['primary'], r['primary'])]
    for a in (r.get('also', []) or []) + XALSO.get(x['img'], []):
        a = SEC.get(a, a)
        if a in VALID and a not in out:
            out.append(a)
    out = [c for c in out if c in VALID] or [SEC.get(x['old'], x['old'])]
    if x['img'] in TONALFIX:  # Claude's tonal re-check replaces only the Neutral/Earthy/Dark/B&W tags
        fix = TONALFIX[x['img']]
        if out[0] in TONAL:
            out = fix + [c for c in out[1:] if c not in TONAL and c not in fix]
        else:
            out = [c for c in out if c not in TONAL] + fix
    if x['img'] in FLORALS_ONLY:
        return ['florals']
    if x['img'] in FLORALS or r.get('floral') or 'florals' in (r.get('also') or []):  # floral multis go to Multicolor Florals instead of Multicolor
        out = ['florals' if c == 'multi' else c for c in out]  # keeps florals in the primary slot when the mat is a multi
        if 'florals' not in out: out.append('florals')
        out = list(dict.fromkeys(out))
    return out


vis = [x for x in rows if x['img'] not in hidden]
for x in vis:
    x['secs'] = sections(x)

# ---------- v5 layer ----------
V5 = json.load(open(P('config/tiffany-color-notes/2026-10-20-v5-calls.json')))
FINAL = V5.get('final_sections', {})  # Tiffany's v5 color calls: win over every crosstag (jungle, primary_fix, ...)
MOODB = {m['img'] for m in V5.get('mood_calls', []) if m['mood'] == 'brights'} | set(XT.get('mood_fix', {}).get('brights', []))
MOODP = {m['img'] for m in V5.get('mood_calls', []) if m['mood'] == 'pastel'}
SIMPLE = set(XT.get('simple', {}).get('tiffany', [])) | set(XT.get('simple', {}).get('claude', []))
MOODS = ('pastel', 'brights')
LATE = json.load(open(P('config/tiffany-color-notes/2026-10-20-late-calls.json')))
LATE_RM = {c['img']: list(c['remove']) for c in LATE.get('corrections', []) if c.get('remove')}  # her explicit colour removals (Gaylord teal)
TALA = json.load(open(P('config/tala-shopmy-links.json')))['links']  # Tiffany Oct 20: Tala Mahj links go to her ShopMy links
v5log = {'final': [], 'to_brights': [], 'simple': []}
REMOVED = {}


def v5(img, secs):
    if secs == ['holiday']:
        return secs
    if img in FINAL:
        REMOVED[img] = [c for c in secs if c not in FINAL[img] and c not in MOODS + TONAL + ('animal', 'simple')] + LATE_RM.get(img, [])  # her removals never come back as accents (the old blanket teal strip is gone, Oct 20 late: teal is only removed where she said so, late-calls 'remove')
        keep = [c for c in secs if c in MOODS + TONAL + ('animal',)]  # mood + tonal tags stay unless her call says otherwise
        secs = list(dict.fromkeys(FINAL[img] + keep)); v5log['final'].append(img)
        if not any(c in TONAL or c in MOODS for c in secs):
            secs.append('brights')
    if img in MOODP and 'brights' in secs:
        secs = list(dict.fromkeys(['pastel' if c == 'brights' else c for c in secs]))
    if img in MOODB and 'pastel' in secs:
        secs = ['brights' if c == 'pastel' else c for c in secs]; secs = list(dict.fromkeys(secs)); v5log['to_brights'].append(img)
    if img in SIMPLE:
        first_mood = next((i for i, c in enumerate(secs) if c in MOODS), len(secs))
        rest = [c for c in secs if c not in MOODS]
        rest = [c for c in rest if c != 'simple']; first_mood = min(first_mood, len(rest))
        secs = rest[:first_mood] + ['simple'] + rest[first_mood:]; v5log['simple'].append(img)
    return secs


for x in vis:
    x['secs'] = v5(x['img'], x['secs'])

# ---------- v5: 53 new mats (Claude photo review; hidden = not a clean flat mat, or duplicate) ----------
N53 = json.load(open(os.path.join(HERE, 'new53_rows.json')))
TAG53 = json.load(open(P('config/tiffany-color-notes/2026-10-20-new53-claude-tags.json')))['mats']
BRAND53 = {'Etsy shop (name TBD)': 'Etsy'}
hidden53 = {}
added53 = []
for r in N53['rows']:
    img, name, brand, url, ret, _c, code = r
    t = TAG53[img]
    if img in RMI or BRAND53.get(brand, brand) in RMB:
        continue
    if t.get('hidden'):
        hidden53[img] = t['hidden']; continue
    x = dict(img=img, key=N53['manifest'][img], name=name, raw=name, brand=BRAND53.get(brand, brand), url='' if ret else url, ret=ret, code=code, old=_c, new53=1)
    x['secs'] = v5(img, list(t['sections']))
    vis.append(x); added53.append(img)

# ---------- late Oct 20: mats Tiffany brought in by hand (config/mat-gallery-extra-rows.json, e.g. Mahj Tile Haus Imperial Lotus) ----------
XROWS = json.load(open(P('config/mat-gallery-extra-rows.json')))['rows']
IMGB = {}
for a in XROWS:
    if a['img'] in RMI or a['brand'] in RMB: continue
    vis.append(dict(img=a['img'], key=a['key'], name=a['name'], raw=a['name'], brand=a['brand'], url=a['url'], ret=0, code=a.get('code', ''), old=a['secs'][0], secs=v5(a['img'], list(a['secs'])), xrow=1))
    IMGB[a['img']] = a['img_commit']

# ---------- v5: retired additions (another agent's audit, retired_additions_oct20.json): Holy Mahj + Queen Bee new rows (stopgap
# crop photos), Peri-twinkle + Garden Party come back via crosstags unhold; all four use the audit's colors ----------
RADD = json.load(open(os.path.join(HERE, 'retired_additions_oct20.json')))
VR = {x['img']: x for x in vis}
for a in RADD:
    if a['gallery_id'] in RMI or a['brand'] in RMB:
        continue
    c = a['colors']; secs = list(dict.fromkeys([c['primary']] + c.get('also', []) + c.get('tags', [])))
    if not any(t in TONAL or t in MOODS for t in secs): secs.append('brights')
    if a['gallery_id'] in VR:
        VR[a['gallery_id']]['secs'] = secs; VR[a['gallery_id']]['ret'] = 1; VR[a['gallery_id']]['url'] = ''
    else:
        vis.append(dict(img=a['gallery_id'], key=a.get('fym_key', ''), name=a['name'], raw=a['name'], brand=a['brand'], url='', ret=1, code='', old=c['primary'], secs=secs, radd=1))

# ---------- v5: second colors by Claude (Tiffany: she only sends main-color fixes; Claude identifies SECOND colors) ----------
# For every mat she hasn't called (no v5 final call, no tiffany-chat override, not one of the 53 Claude photo-tagged by eye): a color
# measured at >= 15% of the mat (accents file 'major') becomes an also-color. Logged to config/mat-also-claude-v5.json.
ACC = json.load(open(P('config/mat-accent-colors.json')))['mats']
for x in vis:
    REMOVED.setdefault(x['img'], [])
    REMOVED[x['img']] = list(dict.fromkeys(REMOVED[x['img']] + LATE_RM.get(x['img'], [])))
    if x['img'] in TALA and x['url']:
        x['url'] = TALA[x['img']]
TCALLED = set(FINAL) | {x['img'] for x in vis if str((MC.get(x['key']) or {}).get('by', '')).startswith('tiffany')}
COLS8 = ('pink', 'red', 'orange', 'yellow', 'green', 'teal', 'blue', 'purple')
NEIGH = {'purple': ('pink', 'blue'), 'pink': ('purple', 'red', 'orange'), 'blue': ('purple', 'teal'), 'teal': ('blue', 'green'), 'green': ('teal', 'yellow'),
         'red': ('pink', 'orange'), 'orange': ('red', 'yellow', 'pink'), 'yellow': ('orange', 'green'),
         'earthy': ('red', 'orange', 'yellow'), 'neutral': ('orange', 'yellow', 'pink'), 'dark': (), 'bw': ()}
also_log = {}
for x in vis:
    if x['img'] in TCALLED or x.get('new53') or x['secs'] == ['holiday']:
        continue
    # spot check (30 promotions by eye): neighbouring hues of the primary are where the measurement misreads (violet->blue,
    # lavender->pink, rust leather->red, peach cream->orange), so those stay accents (tier 3), never also-colors
    nb = NEIGH.get(x['secs'][0], ())
    add = [c for c in ACC.get(x['img'], {}).get('major', []) if c not in x['secs'] and c not in REMOVED.get(x['img'], []) and c not in nb]
    if add:
        i = next((k for k, c in enumerate(x['secs']) if k > 0 and c not in COLS8), len(x['secs']))  # never displaces the primary
        x['secs'] = x['secs'][:i] + add + x['secs'][i:]
        also_log[x['img']] = add
json.dump({'by': 'claude-photo-review', 'date': '2026-10-20', 'method': 'measured palette (config/mat-accent-colors.json, thresholds eye-checked on contact sheets): a color covering >= 15% of the mat is promoted to an also-color. Never applied to mats Tiffany has called (her v5 final calls or any tiffany-chat override) or to the 53 new mats (tagged by eye in tiffany-color-notes/2026-10-20-new53-claude-tags.json).',
           'count': len(also_log), 'mats': also_log}, open(P('config/mat-also-claude-v5.json'), 'w'), indent=1, ensure_ascii=False)

# ---------- v5: accent colors (config/mat-accent-colors.json, claude-measured): tier 3 in color sections + AND filter ----------
ACC = json.load(open(P('config/mat-accent-colors.json')))['mats']
ACOL = {'pink', 'red', 'orange', 'yellow', 'green', 'teal', 'blue', 'purple', 'neutral', 'earthy', 'dark'}
for x in vis:
    if x['secs'] == ['holiday']:  # holiday mats stay out of color sections; their measured colors only count in combos (Holiday + Red)
        x['acc'] = []; x['hacc'] = [a for a in ACC.get(x['img'], {}).get('accents', []) if a in ACOL]; continue
    x['acc'] = [a for a in ACC.get(x['img'], {}).get('accents', []) if a in ACOL and a not in x['secs'] and a not in REMOVED.get(x['img'], [])]
    if x['img'] in V5.get('accent_calls', {}):  # Tiffany named this mat's accents: hers replace the measured ones
        x['acc'] = []
    for a in V5.get('accent_calls', {}).get(x['img'], []):  # Tiffany's own accent calls
        if a not in x['secs'] and a not in x['acc']: x['acc'].append(a)
# ---------- late Oct 20: Tiffany's late calls (tiffany-color-notes/2026-10-20-late-calls.json) re-applied LAST so nothing above undoes them ----------
LEAD, TAIL, LEADP = LATE.get('lead', {}), LATE.get('tail', {}), set(LATE.get('lead_primary', []))
late_log = {}
VI = {x['img']: x for x in vis}
for c in LATE.get('corrections', []):
    x = VI.get(c.get('img'))
    if x is None:
        late_log[c.get('img')] = 'not in gallery'; continue
    cp = c.get('primary')
    if cp == 'holiday':
        x['hacc'] = [a for a in ACC.get(x['img'], {}).get('accents', []) if a in ACOL]; x['secs'] = ['holiday']; x['acc'] = []
        late_log[x['img']] = x['secs']; continue
    secs = [a for a in x['secs'] if a != 'holiday' and a not in c.get('remove', [])]
    x['acc'] = [a for a in x['acc'] if a not in c.get('remove', [])]
    if c.get('floral') is False:
        secs = [a for a in secs if a != 'florals']
    if cp:
        secs = [cp] + [a for a in secs if a != cp]
    for a in c.get('also', []):
        if a not in secs:
            i = next((k for k, v in enumerate(secs) if k > 0 and v in MOODS + ('simple',)), len(secs)); secs.insert(i, a)
    if not any(a in TONAL or a in MOODS or a == 'simple' for a in secs):
        secs.append('brights')
    x['secs'] = secs; x['acc'] = [a for a in x['acc'] if a not in secs]
    late_log[x['img']] = secs
for sec, imgs in LEAD.items():  # lead mats: pinned to the top of that section, and that section is their primary
    for img in imgs:
        x = VI.get(img)
        if x is None:
            late_log[img] = 'lead not in gallery'; continue
        if sec in LEADP and x['secs'][0] != sec:  # green leads: that section is their primary (Tiffany 22:45)
            x['secs'] = [sec] + [a for a in x['secs'] if a != sec]; x['acc'] = [a for a in x['acc'] if a != sec]
        elif sec not in x['secs']:  # other leads (teal): keep the primary, make sure the mat is in the section
            i = next((k for k, v in enumerate(x['secs']) if k > 0 and v in MOODS + TONAL + ('simple', 'florals', 'animal')), len(x['secs'])); x['secs'].insert(i, sec)
            x['acc'] = [a for a in x['acc'] if a != sec]
        late_log.setdefault(img, x['secs'])
for sec, imgs in TAIL.items():
    for img in imgs:
        if img not in VI: late_log[img] = 'tail not in gallery'
# ---------- late Oct 20 (item J): album colours as a COMBO-ONLY hint (row field 10, like holiday accents). A set colour is added only
# where the photo measures >= combo_only.min_pct of it (blue + teal pooled), never where she removed it. Single sections never change.
ALB = json.load(open(P('config/mat-album-combo-colors.json')))
CMIN = LATE.get('combo_only', {}).get('min_pct', 5.0)
combo_log = {}
for x in vis:
    sh = ACC.get(x['img'], {}).get('shares', {})
    for st in ALB['album_sets'].get(x['img'], []):
        for c in ALB['set_colors'][st]:
            if c in x['secs'] or c in x['acc'] or c in (x.get('hacc') or []) or c in REMOVED.get(x['img'], []): continue
            v = sum(sh.get(f, 0) for f in ('blue', 'teal') if f not in REMOVED.get(x['img'], [])) if c in ('blue', 'teal') else sh.get(c, 0)  # a colour she removed never counts toward the pool
            if v >= CMIN:
                x['hacc'] = (x.get('hacc') or []) + [c]; combo_log.setdefault(x['img'], {})[c] = [round(v, 1), st]
order = {c: i for i, (c, _) in enumerate(COL)}
# STANDING RULE (Tiffany, Oct 20): Mahjong Studios always sorts to the bottom of every section
vis.sort(key=lambda x: (x['brand'] == 'Mahjong Studios', x['brand'].lower(), x['name'].lower()))

active = [x for x in vis if not x['ret']]
retired = [x for x in vis if x['ret']]
cnt = {c: sum(1 for x in active if c in x['secs'] or c in x['acc']) for c, _ in COL}
COP = V5.get('coprimary', {})
tiers = {c: {'primary': sum(1 for x in active if x['secs'][0] == c or c in COP.get(x['img'], [])), 'also': sum(1 for x in active if c in x['secs'][1:] and c not in COP.get(x['img'], [])),
             'accent': sum(1 for x in active if c in x['acc'])} for c, _ in COL}
cnt_with_ret = {c: sum(1 for x in vis if c in x['secs'] or c in x['acc']) for c, _ in COL}
cnt['retired'] = len(retired)

# ---------- side outputs ----------
with open(os.path.join(HERE, 'dedupe_oct20.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['group', 'brand', 'kept_img', 'kept_name', 'kept_url', 'dropped_imgs', 'dropped_raw_names', 'what_happened', 'why'])
    w.writerows(dd_rows)
with open(os.path.join(HERE, 'hidden_oct20.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['img', 'catalog_key', 'brand', 'name_in_catalog', 'reason'])
    for img, why in sorted(hidden.items(), key=lambda kv: (kv[1].split(':')[0].split(' (')[0], kv[0])):
        w.writerow([img, R[img]['key'], R[img]['brand'], R[img]['raw'], why])
    Fi = {r[0]: r for r in F}
    for t_, lab in (('placeholder image', 'placeholder image'), ('wrong image (shows another mat)', 'wrong image'), ('lifestyle/table scene', 'image shows no mat')):
        for img, a in sorted(by_type.get(t_, {}).items()):
            if img in held and (t_ != 'lifestyle/table scene' or 'no mat visible' in a['detail']):
                w.writerow([img, man[img], BRANDFIX.get(Fi[img][2], Fi[img][2]), Fi[img][1], f'already out (held low-confidence list); would also be hidden: {lab}: {a["detail"][:100]}'])
json.dump({'new53_added': added53, 'new53_hidden': hidden53, 'new53_sections': {x['img']: x['secs'] for x in vis if x.get('new53')},
           'v5_final_calls': v5log['final'], 'v5_pastel_to_brights': v5log['to_brights'], 'v5_simple': v5log['simple'],
           'removed_mats': removed_mats, 'late_calls_applied': late_log, 'combo_only_album': combo_log, 'claude_also_added': len(also_log), 'section_tiers_active': tiers,
           'section_counts_active': cnt, 'section_counts_if_retired_shown': cnt_with_ret, 'unique_active_mats': len(active),
           'retired': len(retired), 'hidden': len(hidden), 'dedupe_groups': len(dd_rows), 'held_low_out': len(held),
           'applied_color_calls': applied, 'unmatched_color_calls': unmatched,
           'renamed': {x['img']: [x['raw'], x['name']] for x in vis if x['raw'] != x['name']}},
          open(os.path.join(HERE, 'v5_counts.json'), 'w'), indent=1, ensure_ascii=False)

# ---------- HTML ----------
CSS = open(os.path.join(HERE, 'style.css')).read() + '.mmg-hint{font-size:.85em;color:#6f655d;margin:.2em 0 .6em}\n.mmg-combo .mmg-empty{display:none}\n.mmg-chip.mmg-tog{border-style:dashed}\n.mmg-watch{margin-top:auto;align-self:flex-start;border:1.5px solid #9a8f86;color:#6f655d;font-size:.68em;font-weight:700;letter-spacing:.06em;padding:2px 8px;border-radius:10px}\n.mmg-chip.mmg-tog[aria-pressed="true"]{border-style:solid}\n'
# Row fields: [img, name, brand, url, ret, secs, code, watch, acc, coprimary, combo-only colours (holiday accents + album hint), shares]
# Image swaps (Tiffany Oct 20): use a clean flat photo when a store's photo has text/cropping
IMG_ALIAS = {'four-winds-social--fws-x-mahj-mood-collab-beyond-the-ribbon': 'mahj-mood--beyond-the-ribbon-four-winds-social-collab-mat-benefitting-pink-fund-pre-order-ships-end-of-december'}
data = json.dumps([[IMG_ALIAS.get(x['img'], x['img']), x['name'], x['brand'], x['url'], x['ret'], x['secs'], x['code'], 1 if x['img'] in WATCH else 0, x['acc'], V5.get('coprimary', {}).get(x['img'], []), x.get('hacc') or [],
                   {c: s for c, s in ACC.get(x['img'], {}).get('shares', {}).items() if c in x['secs'] or c in x['acc']}] for x in vis],
                  separators=(',', ':'), ensure_ascii=False).replace('</', '<\\/')
chips = ('<button type="button" class="mmg-chip" data-f="all" aria-pressed="true">All / Clear</button>'
         + ''.join(f'<button type="button" class="mmg-chip" data-f="{c}" aria-pressed="false">{html.escape(l)}</button>' for c, l in COL if cnt[c])
         + (f'<button type="button" class="mmg-chip" data-f="retired" aria-pressed="false">Retired</button>' if retired else '')
         + '<button type="button" class="mmg-chip mmg-tog" data-t="ret" aria-pressed="true">Hide retired</button>')
brands = sorted({x['brand'] for x in vis}, key=str.lower)
opts = '<option value="">All brands</option>' + ''.join(f'<option>{html.escape(b)}</option>' for b in brands)
secs = ''.join(f'<section class="mmg-sec" data-c="{c}"><h2 class="mmg-h">{html.escape(l)} mahjong mats</h2><ul class="mmg-grid"></ul><p class="mmg-empty">No mats here from that brand yet.</p></section>'
               for c, l in COL if cnt_with_ret[c])
secs = '<section class="mmg-combo" hidden><h2 class="mmg-h"></h2><ul class="mmg-grid"></ul><p class="mmg-empty">No mats with all of those yet — try removing one.</p></section>' + secs
secs += '<section class="mmg-sec" data-c="retired"><h2 class="mmg-h">Retired mats</h2><p class="mmg-intro">No longer sold, kept here so you can see what goes with the tiles you already own.</p><ul class="mmg-grid"></ul><p class="mmg-empty">No retired mats from that brand.</p></section>' if retired else ''
JS = r"""(function(){var r=document.currentScript.parentNode,R=JSON.parse(r.querySelector('script[type="application/json"]').textContent),B='https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@__C__/assets/mats/gallery/',f='all',br='',hr=true,LD=__LEAD__,TL=__TAIL__,IB=__IB__;
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function card(x,i){var shop=x[3]?'<a class="mmg-shop" href="'+esc(x[3])+'" target="_blank" rel="sponsored noopener">Shop the mat</a>':(x[4]?'<span class="mmg-ret">Retired</span>':(x[7]?'<span class="mmg-watch">One to watch</span>':''));var img='<img src="'+(IB[x[0]]?B.replace(/@[0-9a-f]+\//,'@'+IB[x[0]]+'/'):B)+x[0]+'.webp" alt="'+esc(x[2]+' '+x[1])+' mahjong mat" loading="lazy" decoding="async" width="640" height="640">';return '<li class="mmg-card" data-b="'+esc(x[2])+'" data-i="'+i+'"'+(x[4]?' data-r="1"':'')+'>'+(x[3]?'<a class="mmg-img" href="'+esc(x[3])+'" target="_blank" rel="sponsored noopener">'+img+'</a>':'<span class="mmg-img">'+img+'</span>')+'<div class="mmg-body"><span class="mmg-brand">'+esc(x[2])+'</span><span class="mmg-name">'+esc(x[1])+'</span>'+(x[6]?'<a class="mmg-code" href="'+esc(x[6])+'">'+esc(x[2])+' guide</a>':'')+shop+'</div></li>'}
function sk(x,c){var ld=(LD[c]||[]).indexOf(x[0]);if(ld>-1)return -10+ld/100;var tl=(TL[c]||[]).indexOf(x[0]);if(tl>-1)return 5+tl/100;var s=(x[11]&&x[11][c])||0,p=([x[5][0]].concat(x[9]).indexOf(c)>-1&&x[5].indexOf(c)>-1)?1:0;return 1-(s+20*p)/1000-p/1e6}/* Oct 20 late rule: Tiffany's lead mats first, then ONE list by score high to low (score = measured share of the colour + 20 if it is the mat's primary; no measurement = 0; ties: primary first, then name), then her tail mats */
function has(x,c,m){return x[5].indexOf(c)>-1||x[8].indexOf(c)>-1||(m&&x[10]&&x[10].indexOf(c)>-1)}function tier(x,C){var pr=[x[5][0]].concat(x[9]);if(C.some(function(c){return pr.indexOf(c)>-1})&&C.every(function(c){return x[5].indexOf(c)>-1}))return 0;if(C.every(function(c){return x[5].indexOf(c)>-1})){var p=0;C.forEach(function(c){p=Math.max(p,x[5].indexOf(c))});return 1+Math.min(p-1,3)/10}return 2}
r.querySelectorAll('.mmg-sec').forEach(function(s){var c=s.dataset.c,h='';var L=[];R.forEach(function(x,i){if(c==='retired'?x[4]:has(x,c))L.push(i)});L.sort(function(a,b){function k(i){var x=R[i];return c==='retired'?(x[2]==='Mahjong Studios'?0.5:0):sk(x,c)}return k(a)-k(b)||(c==='retired'?0:R[a][1].toLowerCase().localeCompare(R[b][1].toLowerCase()))||a-b});L.forEach(function(i){h+=card(R[i],i)});s.querySelector('.mmg-grid').innerHTML=h});
var chips=r.querySelectorAll('.mmg-chip[data-f]'),tog=r.querySelector('.mmg-tog'),sel=r.querySelector('.mmg-brand-sel'),tot=r.querySelector('.mmg-total'),cmb=r.querySelector('.mmg-combo'),S=[],LB={};
chips.forEach(function(x){LB[x.dataset.f]=x.textContent});
function combo(){var L=[],h='';R.forEach(function(x,i){if(S.every(function(c){return has(x,c,1)})&&(!br||x[2]===br)&&!(hr&&x[4]))L.push(i)});L.sort(function(a,b){function k(i){var x=R[i];return(x[2]==='Mahjong Studios'?0.5:0)+tier(x,S)}return k(a)-k(b)||a-b});L.forEach(function(i){h+=card(R[i],i)});cmb.querySelector('.mmg-h').textContent='Mats with '+S.map(function(c){return LB[c]}).join(' + ');cmb.querySelector('.mmg-grid').innerHTML=h;cmb.querySelector('.mmg-empty').style.display=L.length?'none':'block';return L.length}
function go(){var seen={},all=0,f=S.length===1?S[0]:(S.length?'':'all');chips.forEach(function(x){var on=x.dataset.f==='all'?!S.length:S.indexOf(x.dataset.f)>-1;x.setAttribute('aria-pressed',on?'true':'false')});tog.setAttribute('aria-pressed',hr?'true':'false');
if(S.length>1){r.querySelectorAll('.mmg-sec').forEach(function(s){s.hidden=true});cmb.hidden=false;var n=combo();tot.textContent=n+(n===1?' mat':' mats');return}
cmb.hidden=true;cmb.querySelector('.mmg-grid').innerHTML='';
r.querySelectorAll('.mmg-sec').forEach(function(s){var c=s.dataset.c,on=f==='all'||c===f,n=0;s.hidden=!on;if(!on)return;s.querySelectorAll('.mmg-card').forEach(function(d){var ok=(!br||d.dataset.b===br)&&!(hr&&c!=='retired'&&d.dataset.r);d.hidden=!ok;if(ok){n++;if(!seen[d.dataset.i]){seen[d.dataset.i]=1;all++}}});s.querySelector('.mmg-empty').style.display=n?'none':'block';if(!n&&f==='all')s.hidden=true});tot.textContent=all+(all===1?' mat':' mats')}
chips.forEach(function(x){x.addEventListener('click',function(){var c=x.dataset.f,i=S.indexOf(c);if(c==='all'){S=[]}else if(c==='retired'){S=i>-1?[]:['retired']}else{S=S.filter(function(v){return v!=='retired'});i=S.indexOf(c);if(i>-1)S.splice(i,1);else S.push(c)}go()})});tog.addEventListener('click',function(){hr=!hr;go()});sel.addEventListener('change',function(){br=sel.value;go()});go()})();""".replace('__C__', COMMIT).replace('__LEAD__', json.dumps(LEAD)).replace('__TAIL__', json.dumps(TAIL)).replace('__IB__', json.dumps(IMGB))
print(f"""<style>{CSS}</style>
<div class="mmg"><span class="mmg-eyebrow">The Mat Library</span>
<h1 class="mmg-title">Mahjong Mats by Color</h1>
<p class="mmg-intro">Every mat in my matching library, all in one place. Browse by color or pick a brand, then tap any mat to shop it. Want to see which tiles go with a mat? <a href="/mahjong-tile-matches">See my tile matches</a>, and watch for Find Your Match, coming 10.27.</p>
<p class="mmg-hint">Tap one color to see that section, or tap two or more to find mats that have all of them.</p>
<div class="mmg-chips" role="group" aria-label="Filter mats by color">{chips}</div>
<div class="mmg-tools"><label for="mmg-brand">Brand</label><select id="mmg-brand" class="mmg-brand-sel">{opts}</select><span class="mmg-total" aria-live="polite"></span></div>
{secs}
<script type="application/json">{data}</script>
<script>{JS}</script></div>""")
log('active', len(active), 'retired', len(retired), 'hidden', len(hidden), 'groups', len(dd_rows), 'unmatched', len(unmatched))
log(json.dumps(cnt))
