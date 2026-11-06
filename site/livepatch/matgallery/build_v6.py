"""Mat Gallery v6 (/mahjong-mats), Nov 6 2026: build_v5.py + a Find Your Mat-ch sync layer. The gallery is rebuilt from EVERY FYM
release (Tiffany Nov 6 1:22am: Dapper 2 still showed "Shop the mat" on the gallery while FYM had it retired; site/livepatch/
fym-preview-oct21/README.md release steps; gate [159b] fails a release whose staged gallery was built from an older FYM version).

Steps (all colour rules stay in build_v5.py: her calls, late calls re-applied last, holiday rule + the two exceptions, crosstags
remove_mats, non-partner lockout, sort rule; this layer never touches sections):
 1. runs build_v5.py (rows = catalog + new53 + config/mat-gallery-extra-rows.json, incl. the FYM sync rows that
    builder/fym_fix_nov06/gallery_sync.py wrote for this release; extra rows with img_commit PENDING get the commit that added
    their webp from git).
 2. matches every row to its FYM mat (key via manifest / new53 / extra rows, else product URL, else name + brand; same as gate [90])
    and copies from FYM:
      - Retired: FYM rt -> grey "Retired" pill, no shop link (Retired section). A row the gallery had as retired but FYM sells
        again (not rt, not hidden, product link) comes back with FYM's link ("label Retired only when confirmed gone").
      - Sold out: FYM oos (and not retired) -> row field 13 = 1: grey "Sold out" pill on the photo, shop link kept, text
        "Sold out · see the mat" (same look as the Christmas gallery, Nov 1).
      - Shop link: FYM's link (it carries the partner / ShopMy links), unless FYM has none or only a collection / our own page.
 3. every shop link of a Shopify code partner -> auto-apply link (builder/fym_fix_nov06/autoapply_links.py; TdT, Squarespace
    stores, ShopMy, Amazon untouched).
 4. stamps the block with the FYM version: <!--mmg-fym:vNNN--> + data-fym="vNNN" on .mmg (gate [159b] reads it).
Card ids / data attributes / classes are unchanged (assets/search/search.js galleryJump relies on the img file name, .mmg-card,
data-r, .mmg-chip[data-f], .mmg-tog, .mmg-brand-sel, .mmg-body, .mmg-shop/.mmg-ret/.mmg-watch).

Usage: python3 build_v6.py <FYM website index.html, e.g. /home/claude/fym-site/site-app/fym-v115/index.html> [image commit]
       > matgallery-v6.html      (writes v6_counts.json + v6_diff.json next to this file)"""
import json, os, re, subprocess, sys, unicodedata, urllib.parse as up

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..')) + '/'
sys.path.insert(0, REPO + 'builder/fym_fix_nov06')
import autoapply_links as AA

ARGS = [a for a in sys.argv[1:] if not a.startswith('--')]
DATA_COMMIT = sys.argv[sys.argv.index('--data-commit') + 1] if '--data-commit' in sys.argv else None
if DATA_COMMIT: ARGS.remove(DATA_COMMIT)
IDX = ARGS[0]
COMMIT = ARGS[1] if len(ARGS) > 1 else 'ae02d66a4404ebec83cae6b54b019aee4a1dc0a9'
VER = re.search(r'fym-(v\d+)', os.path.abspath(IDX)).group(1)
log = lambda *a: print(*a, file=sys.stderr)
h = open(IDX).read(); i = h.index('const D=') + 8; D, _ = json.JSONDecoder().raw_decode(h, i); M = D['mats']

# --- 0. extra rows: fill img_commit PENDING from git (the last commit that changed assets/mats/gallery/<img>.webp) ---
XP = REPO + 'config/mat-gallery-extra-rows.json'
X = json.load(open(XP)); fixed = 0
for a in X['rows']:
    if a.get('img_commit') == 'PENDING':
        _p = f"assets/mats/gallery/{a['img']}.webp"
        if subprocess.run(['git', '-C', REPO, 'status', '--porcelain', '--', _p], capture_output=True, text=True).stdout.strip():
            sys.exit(f"build_v6: {_p} has uncommitted changes: commit + push the gallery_sync.py webps first, then rebuild")
        c = subprocess.run(['git', '-C', REPO, 'log', '--format=%H', '-1', '--', _p], capture_output=True, text=True).stdout.strip()  # LAST commit that changed it (a re-picked photo gets a new pin)
        if not c: sys.exit(f"build_v6: {a['img']}.webp is not committed yet: commit the gallery_sync.py webps first, then rebuild")
        a['img_commit'] = c; fixed += 1
if fixed:
    json.dump(X, open(XP, 'w'), indent=1, ensure_ascii=False); log('img_commit filled for', fixed, 'rows')

# --- 1. build_v5 ---
r5 = subprocess.run([sys.executable, os.path.join(HERE, 'build_v5.py'), REPO + 'builder/fym_fix_oct20/mat_audit_report.csv', os.path.join(HERE, 'phash_pairs_oct20.json'), COMMIT],
                    capture_output=True, text=True, cwd=HERE)
if r5.returncode: sys.exit('build_v5 failed:\n' + r5.stderr[-2000:])
out = r5.stdout
m_ = re.search(r'(<script type="application/json">)(.*?)(</script>)', out, re.S)
G = json.loads(m_.group(2).replace('<\\/', '</'))

# --- 2. FYM sync layer ---
nz = lambda x: re.sub(r'[^a-z0-9]', '', ''.join(c for c in unicodedata.normalize('NFD', str(x or '')) if not unicodedata.combining(c)).lower())


def nu(u):
    u = str(u or '')
    if '/discount/' in u and 'redirect=' in u:
        u = re.sub(r'^(https?://[^/]+).*$', r'\1', u) + up.unquote(u.split('redirect=', 1)[1].split('&')[0])
    return re.sub(r'^https?://(www\.)?', '', u.split('?')[0].split('#')[0]).rstrip('/').replace('/products/', '/')


MAN = json.load(open(os.path.join(HERE, 'manifest.json')))
N53 = json.load(open(os.path.join(HERE, 'new53_rows.json')))['manifest']
RA = {a['gallery_id']: a['fym_key'] for a in json.load(open(os.path.join(HERE, 'retired_additions_oct20.json')))}
RA.update({a['img']: a['key'] for a in X['rows']})
ALIAS = {'mahj-mood--beyond-the-ribbon-four-winds-social-collab-mat-benefitting-pink-fund-pre-order-ships-end-of-december': 'four-winds-social--fws-x-mahj-mood-collab-beyond-the-ribbon'}  # build_v5 IMG_ALIAS (row shows the other photo)
GK = lambda im: MAN.get(im) or N53.get(im) or RA.get(im) or MAN.get(ALIAS.get(im, ''))
BYU, BYN = {}, {}
for k, o in M.items():
    for u in (o.get('u0'), o.get('u'), k):
        if u and '/collections/' not in str(u) and 'mahjmatchmaker.com' not in str(u): BYU.setdefault(nu(u), k)
    BYN.setdefault(nz(re.sub(r'\s*\(retired\)', '', o['n'], flags=re.I)) + '|' + nz(o.get('bn')), k)


def fym_key(r):
    k = GK(r[0])
    if k in M: return k, 'key'
    if r[3] and nu(r[3]) in BYU: return BYU[nu(r[3])], 'url'
    k = BYN.get(nz(r[1]) + '|' + nz(r[2]))
    return (k, 'name') if k else (None, None)


def good_link(u):
    return bool(u) and 'mahjmatchmaker.com' not in u and '/collections/' not in up.urlsplit(u).path


before = {}  # live (staged) page before this build, for the diff
try:
    _s = open(os.path.join(HERE, 'matgallery-v5.html')).read()
    before = {r[0]: r for r in json.loads(re.search(r'<script type="application/json">(.*?)</script>', _s, re.S).group(1).replace('<\\/', '</'))}
except Exception:
    pass
stats = {'matched': {}, 'retired_from_fym': [], 'unretired_from_fym': [], 'sold_out': [], 'link_from_fym': 0, 'autoapply': {}, 'unmatched': []}
for r in G:
    while len(r) < 14: r.append(0 if len(r) in (12, 13) else [])
    k, how = fym_key(r)
    stats['matched'][how or 'none'] = stats['matched'].get(how or 'none', 0) + 1
    o = M.get(k) if k else None
    if o is None:
        stats['unmatched'].append(f'{r[2]} | {r[1]}')
    else:
        if o.get('rt'):
            if not r[4]: stats['retired_from_fym'].append(f'{r[2]} | {r[1]} ({r[0]})')
            r[4], r[3] = 1, ''
        elif r[4] and not o.get('hid') and good_link(o.get('u')):
            stats['unretired_from_fym'].append(f'{r[2]} | {r[1]} ({r[0]}): FYM sells it again -> {o["u"]}')
            r[4], r[3] = 0, o['u']
        if not r[4]:
            if r[7]: keep_own = True  # 'One to watch' rows (OMM Cognac, Oct 20): no shop button on purpose; FYM's link must not bring one back
            else: keep_own = r[3] and AA.host_of(r[3]) in AA.SKIP and AA.host_of(r[3]) != 'go.shopmy.us'  # TdT (Oct 30: leave exactly as is), Squarespace stores, Maison: never take FYM's form
            if good_link(o.get('u')) and o['u'] != r[3] and not keep_own:
                r[3] = o['u']; stats['link_from_fym'] += 1
            if o.get('oos'):
                r[13] = 1; stats['sold_out'].append(f'{r[2]} | {r[1]}')
    if r[3]:
        r[3], st = AA.autoapply(r[3])
        b = stats['autoapply'].setdefault(r[2], {}); b[st] = b.get(st, 0) + 1

# --- 2a. dead shop links (config/mat-gallery-link-fixes.json, Nov 6): '' = no shop button, not retired, no badge (Oct 20 Mahjong by SI precedent)
LFIX = json.load(open(REPO + 'config/mat-gallery-link-fixes.json'))['mats']
for r in G:
    if r[0] in LFIX:
        r[3] = AA.autoapply(LFIX[r[0]]['url'])[0] if LFIX[r[0]]['url'] else ''
stats['link_fixes'] = sorted(f"{v['name']}: {'new link' if v['url'] else 'no shop button'}" for k, v in LFIX.items() if k in {r[0] for r in G})

# --- 2b. duplicate photos (config/mat-gallery-dedupe-v6.json, Claude photo review; Oct 20 dedupe style): drop the twin, keep one card,
# note under the name (row field 14, e.g. 'Also available in leatherette'), optional second shop link (field 15: [label, url]).
# A pHash + colour sweep flags NEW look-alike pairs that are neither merged nor listed as not_dupes (v6_counts.json 'dupe_candidates').
DUP = json.load(open(REPO + 'config/mat-gallery-dedupe-v6.json'))
GI = {r[0]: r for r in G}
for d_, mm_ in DUP['merge'].items():
    k_ = GI.get(mm_['keep'])
    if d_ not in GI or k_ is None: continue
    while len(k_) < 16: k_.append(0 if len(k_) < 14 else '')
    if mm_.get('note'): k_[14] = mm_['note']
    if mm_.get('shop2') and not k_[4]:
        k_[15] = [mm_['shop2'][0], AA.autoapply(GI[d_][3] or mm_['shop2'][1])[0]]
stats['dupes_merged'] = sorted(f"{GI[d_][2]} | {GI[d_][1]} -> {GI[mm_['keep']][1]}" for d_, mm_ in DUP['merge'].items() if d_ in GI and mm_['keep'] in GI)
G = [r for r in G if not (r[0] in DUP['merge'] and DUP['merge'][r[0]]['keep'] in GI)]
HOLDI = json.load(open(REPO + 'config/mat-gallery-photo-holds.json')).get('imgs', {})  # catalog rows held for their photo (re-QA Nov 6: TdT French Mural)
stats['held_rows'] = sorted(f'{GI[i_][2]} | {GI[i_][1]}' for i_ in HOLDI if i_ in GI)
G = [r for r in G if r[0] not in HOLDI]
for r in G:
    while len(r) < 16: r.append(0 if len(r) < 14 else '')
try:
    import numpy as _np
    from PIL import Image as _Im
    from scipy.fft import dctn as _dct
    _ok = {tuple(sorted(p_)) for p_ in DUP.get('not_dupes', [])}
    _H, _C, _ids = [], [], []
    for r in G:
        _f = REPO + f'assets/mats/gallery/{r[0]}.webp'
        if not os.path.exists(_f): continue
        _a = _np.asarray(_Im.open(_f).convert('L').resize((32, 32)), float); _d = _dct(_a, norm='ortho')[:8, :8]
        _H.append((_d > _np.median(_d)).ravel()); _C.append(_np.asarray(_Im.open(_f).convert('RGB').resize((8, 8)), float)); _ids.append(r[0])
    _H, _C = _np.array(_H), _np.array(_C); cand = []
    for i_ in range(len(_ids)):
        for j_ in _np.where((_H[i_ + 1:] != _H[i_]).sum(1) <= 12)[0] + i_ + 1:
            if _np.abs(_C[i_] - _C[j_]).mean() < 8 and tuple(sorted((_ids[i_], _ids[j_]))) not in _ok: cand.append([_ids[i_], _ids[j_]])
    stats['dupe_candidates'] = cand
    if cand: log(f'WARNING: {len(cand)} look-alike photo pairs not reviewed (v6_counts.json dupe_candidates): merge them or list them as not_dupes in config/mat-gallery-dedupe-v6.json')
except Exception as _e:
    stats['dupe_candidates'] = f'sweep did not run: {_e}'

# --- 2c. LINK CHECK (Nov 6: 10 dead links shipped in v6): GET every shop link (and second shop link), following redirects.
# A 404/410 FAILS the build (fix it in config/mat-gallery-link-fixes.json: a new handle, or '' = no shop button). Other errors
# (403 bot walls on Etsy/ShopMy, timeouts) only warn. Always on for a pinned build (--data-commit); MMG_LINKCHECK=0 skips it
# for a local preview only.
if DATA_COMMIT or os.environ.get('MMG_LINKCHECK', '1') != '0':
    from concurrent.futures import ThreadPoolExecutor
    _L = {}
    for r in G:
        if r[3]: _L.setdefault(r[3], []).append(f'{r[2]} | {r[1]} ({r[0]})')
        if len(r) > 15 and r[15] and r[15][1]: _L.setdefault(r[15][1], []).append(f'{r[2]} | {r[1]} (second shop link)')
    def _chk(u):
        for _t in range(3):
            o = subprocess.run(['curl', '-sSL', '-g', '-o', '/dev/null', '-m', '40', '--max-redirs', '10', '-A', 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1', '-w', '%{http_code}', u], capture_output=True, text=True).stdout.strip()
            if o in ('200', '404', '410'): return u, o
        return u, o
    with ThreadPoolExecutor(16) as ex: _res = dict(ex.map(_chk, list(_L)))
    _dead = {u: c for u, c in _res.items() if c in ('404', '410')}
    _odd = {u: c for u, c in _res.items() if c not in ('200', '404', '410')}
    stats['linkcheck'] = {'checked': len(_res), 'ok': sum(1 for c in _res.values() if c == '200'), 'dead': {u: _L[u] for u in _dead}, 'other': {u: [c] + _L[u] for u, c in _odd.items()}}
    json.dump(stats, open(os.path.join(HERE, 'v6_counts.json'), 'w'), indent=1, ensure_ascii=False)
    log(f"link check: {len(_res)} links, {stats['linkcheck']['ok']} ok, {len(_dead)} dead (404/410), {len(_odd)} other (warn: {sorted(set(_odd.values()))})")
    if _dead:
        sys.exit('build_v6 LINK CHECK FAILED (dead shop links; add each to config/mat-gallery-link-fixes.json with a new handle or url \'\'):\n' + '\n'.join(f'  {c} {u}  <- {"; ".join(_L[u])}' for u, c in _dead.items()))
else:
    log('link check skipped (MMG_LINKCHECK=0, local preview only; a pinned --data-commit build always checks)')

# --- 3. HTML: data, sold-out pill, stamp ---
# The rows (~1,500 mats, ~430 KB) live in data/matgallery-<ver>.json, loaded from jsDelivr pinned at --data-commit, so the
# Squarespace code block stays small (~60 KB). Without --data-commit (local preview) the rows are inlined as before.
os.makedirs(os.path.join(HERE, 'data'), exist_ok=True)
DREL = f'site/livepatch/matgallery/data/matgallery-{VER}.json'
open(REPO + DREL, 'w').write(json.dumps(G, separators=(',', ':'), ensure_ascii=False))
if DATA_COMMIT:
    durl = f'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@{DATA_COMMIT}/{DREL}'
    out = out[:m_.start(1)] + f'<script type="application/json" data-src="{durl}">' + out[m_.end(1):m_.start(2)] + out[m_.end(2):]
    PRE = "(function(){var r=document.currentScript.parentNode,R=JSON.parse(r.querySelector('script[type=\"application/json\"]').textContent),"
    assert PRE in out, 'build_v5 JS prefix changed: update build_v6.py'
    out = out.replace(PRE, "(function(){var r=document.currentScript.parentNode,tot0=r.querySelector('.mmg-total');if(tot0)tot0.textContent='Loading mats\u2026';"
                      "fetch(r.querySelector('script[type=\"application/json\"]').getAttribute('data-src')).then(function(x){if(!x.ok)throw 0;return x.json()}).then(function(R){var ", 1)
    END = "go()})();</script></div>"
    assert out.rstrip().endswith(END)
    out = out.rstrip()[:-len(END)] + "go()}).catch(function(){var t=r.querySelector('.mmg-total');if(t)t.textContent='The mats did not load. Please refresh the page.'})})();</script></div>\n"
else:
    data = json.dumps(G, separators=(',', ':'), ensure_ascii=False).replace('</', '<\\/')
    out = out[:m_.start(2)] + data + out[m_.end(2):]
OLD_CARD = "function card(x,i){var shop=x[3]?'<a class=\"mmg-shop\" href=\"'+esc(x[3])+'\" target=\"_blank\" rel=\"sponsored noopener\">Shop the mat</a>'"
assert OLD_CARD in out, 'card() changed in build_v5.py: update build_v6.py'
out = out.replace(OLD_CARD, "function card(x,i){var shop=x[3]?'<a class=\"mmg-shop\" href=\"'+esc(x[3])+'\" target=\"_blank\" rel=\"sponsored noopener\">'+(x[13]?'Sold out \\u00b7 see the mat':'Shop the mat')+'</a>'")
OLD_IMG = "return '<li class=\"mmg-card\" data-b=\"'"
assert OLD_IMG in out
out = out.replace("var img='<img src=", "var img=(x[13]&&!x[4]?'<em class=\"mmg-pill\">Sold out</em>':'')+'<img src=", 1)
out = out.replace(OLD_IMG, "return '<li class=\"mmg-card'+(x[13]&&!x[4]?' is-sold':'')+'\" data-b=\"'", 1)
OLD_NAME = "<span class=\"mmg-name\">'+esc(x[1])+'</span>'"
assert OLD_NAME in out, 'card name markup changed'
out = out.replace(OLD_NAME, OLD_NAME + "+(x[14]?'<span class=\"mmg-also\">'+esc(x[14])+'</span>':'')", 1)
out = out.replace("+shop+'</div></li>'", "+shop+(x[15]&&x[15][1]&&!x[4]?'<a class=\"mmg-shop mmg-shop2\" href=\"'+esc(x[15][1])+'\" target=\"_blank\" rel=\"sponsored noopener\">'+esc(x[15][0])+'</a>':'')+'</div></li>'", 1)
assert 'mmg-shop2' in out, 'card end markup changed'
CSS6 = '.mmg-also{display:block;font-size:.82em;color:#6f655d;font-style:italic;margin-top:.15em}.mmg-shop2{margin-top:2px!important;padding-top:2px!important;font-size:.78em!important}.mmg-img{position:relative}.mmg-pill{position:absolute;top:8px;left:8px;z-index:2;background:#9a8f86;color:#fff;font-style:normal;font-weight:700;font-size:10px;line-height:1;letter-spacing:.12em;text-transform:uppercase;padding:5px 9px;border-radius:10px;box-shadow:0 1px 4px rgba(0,0,0,.18);pointer-events:none}.mmg-card.is-sold .mmg-img img{opacity:.82}\n'
out = out.replace('</style>', CSS6 + '</style>', 1)
out = out.replace('<div class="mmg">', f'<div class="mmg" data-fym="{VER}">', 1)
out = f'<!--mmg-fym:{VER} built by site/livepatch/matgallery/build_v6.py from Find Your Mat-ch {VER}; gate [159b]-->\n' + out
sys.stdout.write(out)

# --- 4. counts + diff vs the staged v5 page ---
after = {r[0]: r for r in G}
diff = {'fym_version': VER, 'before_rows': len(before), 'after_rows': len(after),
        'before_active': sum(1 for r in before.values() if not r[4]), 'after_active': sum(1 for r in after.values() if not r[4]),
        'before_retired': sum(1 for r in before.values() if r[4]), 'after_retired': sum(1 for r in after.values() if r[4]),
        'added': sorted(f'{r[2]} | {r[1]} ({i})' for i, r in after.items() if i not in before),
        'removed': sorted(f'{r[2]} | {r[1]} ({i})' for i, r in before.items() if i not in after),
        'newly_retired': sorted(f'{r[2]} | {r[1]} ({i})' for i, r in after.items() if r[4] and i in before and not before[i][4]),
        'unretired': sorted(f'{r[2]} | {r[1]} ({i})' for i, r in after.items() if not r[4] and i in before and before[i][4]),
        'sections_changed': sorted(f'{r[2]} | {r[1]}: {before[i][5]} -> {r[5]}' for i, r in after.items() if i in before and before[i][5] != r[5]),
        'added_by_brand': {}}
for s_ in diff['added']:
    b = s_.split(' | ')[0]; diff['added_by_brand'][b] = diff['added_by_brand'].get(b, 0) + 1
diff['added_by_brand'] = dict(sorted(diff['added_by_brand'].items(), key=lambda kv: -kv[1]))
json.dump(diff, open(os.path.join(HERE, 'v6_diff.json'), 'w'), indent=1, ensure_ascii=False)
json.dump(stats, open(os.path.join(HERE, 'v6_counts.json'), 'w'), indent=1, ensure_ascii=False)
log(f"v6 ({VER}): rows {len(before)} -> {len(after)} (active {diff['before_active']} -> {diff['after_active']}, retired {diff['before_retired']} -> {diff['after_retired']}); "
    f"added {len(diff['added'])}, removed {len(diff['removed'])}, newly retired {len(diff['newly_retired'])}, unretired {len(diff['unretired'])}, sold out {len(stats['sold_out'])}; match {stats['matched']}")
