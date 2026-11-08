"""Mat Gallery vs Find Your Mat-ch coverage, ONE definition for gate [90] and scripts/checks/coverage_check.py (Nov 7 2026, FYM 1.18;
gap audit B5: gate [90] said 1 missing while the live gallery v117 lacked 24 visible FYM mats, because the two checks used different
denominators and [90] treated config/mat-gallery-extra-rows.json rows as if they were in the built page).

compare(D, G) with D = an FYM build's D, G = the BUILT gallery rows (site/livepatch/matgallery/data/matgallery-vNNN.json) ->
  missing:  visible FYM mats with no gallery card, after the accounted-for ones below (matched by FYM key via the gallery manifests /
            extra rows, product URL (u / u0 / key) or name + brand with neoprene / leatherette / vegan leather / 'mat' / 'mahjong' ignored)
  shown_hidden: gallery cards whose FYM mat is hidden in FYM
  accounted: {reason: [names]} visible FYM mats that are out of the gallery ON PURPOSE:
            House of Hearts Studio (Tiffany Oct 25: FYM only), crosstags remove_mats (brands / imgs), '#side-b' second listings and
            twins, gallery photo holds (config/mat-gallery-photo-holds.json 'mats', with a reason), duplicate-photo merges whose kept
            twin IS in the gallery (config/mat-gallery-dedupe-v6.json 'merge', hidden_oct20.csv duplicates)."""
import json, os, re, csv, html, unicodedata, urllib.parse
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
GAL = R + 'site/livepatch/matgallery/'


def nz(x):
    x = ''.join(c for c in unicodedata.normalize('NFD', html.unescape(str(x or ''))) if not unicodedata.combining(c)).lower()
    return re.sub(r'[^a-z0-9]', '', x.replace('&', 'and').replace('+', 'and'))


def nu(u):
    u = str(u or '')
    if '/discount/' in u and 'redirect=' in u:
        u = re.sub(r'^(https?://[^/]+).*$', r'\1', u) + urllib.parse.unquote(u.split('redirect=', 1)[1].split('&')[0])
    return re.sub(r'^https?://(www\.)?', '', u.split('?')[0].split('#')[0]).rstrip('/').replace('/products/', '/')


def nameb(n, b):
    return nz(re.sub(r'\s*\(retired\)', '', re.sub(r'\b(neoprene|leatherette|vegan leather|mahjong|mat)\b', '', n or '', flags=re.I), flags=re.I)) + '|' + nz(b)


def lj(p, d=None):
    try: return json.load(open(p))
    except Exception: return d


def compare(D, G):
    M = D['mats']
    MAN = lj(GAL + 'manifest.json', {}); N53 = (lj(GAL + 'new53_rows.json', {}) or {}).get('manifest', {})
    RA = {a['gallery_id']: a['fym_key'] for a in lj(GAL + 'retired_additions_oct20.json', [])}
    XR = lj(R + 'config/mat-gallery-extra-rows.json', {'rows': []})['rows']
    RA.update({a['img']: a['key'] for a in XR})
    GK = lambda im: MAN.get(im) or N53.get(im) or RA.get(im)
    IMG_OF = {}
    for im, k in list(MAN.items()) + list(N53.items()) + list(RA.items()): IMG_OF.setdefault(k, set()).add(im)
    GIDS = {r[0] for r in G}
    GKS = {GK(r[0]) for r in G}; GU = {nu(r[3]) for r in G if r[3]}; GN = {nameb(r[1], r[2]) for r in G}
    XT = lj(R + 'config/mat-gallery-crosstags.json', {}).get('remove_mats', {})
    RMB = set(XT.get('brands', [])); RMK = {MAN.get(i) for i in XT.get('imgs', [])}
    HOLD = lj(R + 'config/mat-gallery-photo-holds.json', {}) or {}
    HOLDK = set(HOLD.get('mats', {})); HOLDI = set(HOLD.get('imgs', {}))
    DUP = (lj(R + 'config/mat-gallery-dedupe-v6.json', {}) or {}).get('merge', {})
    try: DUPK = {MAN[r['img']] for r in csv.DictReader(open(GAL + 'hidden_oct20.csv')) if r['reason'].startswith('duplicate') and r['img'] in MAN}
    except Exception: DUPK = set()
    def in_gal(k, v):
        return k in GKS or bool({nu(v.get('u')), nu(v.get('u0')), nu(k)} - {''} & GU) or nameb(v['n'], v['bn']) in GN
    missing, acc = [], {}
    for k, v in M.items():
        if v.get('hid'): continue
        why = None
        if v['bn'] == 'House of Hearts Studio': why = 'House of Hearts (FYM only, Oct 25)'
        elif v['bn'] in RMB or k in RMK: why = 'removed brand/mat (crosstags)'
        elif '#side-b' in k or v.get('twin'): why = 'side B / twin listing'
        if why is None and in_gal(k, v): continue
        if why is None and (k in HOLDK or IMG_OF.get(k, set()) & HOLDI): why = 'gallery photo hold (with reason)'
        if why is None:
            for im in IMG_OF.get(k, set()):
                if im in DUP and DUP[im]['keep'] in GIDS: why = 'duplicate photo merged into its twin'; break
                if im in DUP and DUP[im]['keep'] in HOLDI: why = 'gallery photo hold (with reason)'; break  # twin held with it (TdT/Mahj Pit French Mural)
        if why is None and k in DUPK: why = 'duplicate (hidden_oct20.csv)'
        if why: acc.setdefault(why, []).append(f"{v['bn']}: {v['n']}"); continue
        missing.append(k)
    UK = {}
    for k, v in M.items():
        for u in (v.get('u'), v.get('u0'), v.get('u_dead')):
            if u: UK.setdefault(nu(u), k)
    NK = {nameb(v['n'], v['bn']): k for k, v in M.items()}
    RBN = set((lj(R + 'config/code-truth.json', {}) or {}).get('removed_brands', {}))
    shown_hidden, unmapped = [], 0
    for r in G:
        k = GK(r[0]); k = k if k in M else (UK.get(nu(r[3])) or NK.get(nameb(r[1], r[2])))
        if not k: unmapped += 1
        elif M[k].get('hid'):
            if r[2] in RBN: acc.setdefault('removed brand: her album-matched mats kept in the gallery (Nov 6 1:33pm)', []).append(f'{r[2]}: {r[1]}')
            else: shown_hidden.append((r[0], k))
    eligible = sum(1 for k, v in M.items() if not v.get('hid')) - sum(len(x) for w, x in acc.items() if not w.startswith('removed brand: her'))
    return dict(missing=missing, shown_hidden=shown_hidden, accounted=acc, unmapped=unmapped, eligible=eligible)
