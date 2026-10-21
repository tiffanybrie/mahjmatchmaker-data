"""Tiffany's picks follow her LIVE album order (Oct 21, QA/Tiffany: Papaya Spritz showed Greenly, Goldie, Preppy Pink, Heiress...
while her live album starts Heiress, Press for Mahjong, Greenly).
Cause: set match lists (m) were built from album/card manifests as they stood on Oct 17-18 (fym_albumsync_oct17, fym_fix_oct18/patch_data)
and never re-synced when she reordered an album. m is LOCKED (membership + racks), so this script does NOT touch m.
It writes D.ao = {set slug: [mat ids in live album order]} and the app sorts each set's m by D.ao at load
(ids not on the live page keep their relative order after the album ones).
Source: scripts/social/its_a_match/albums-live-oct21.json (snapshot of every live album page: cards in page order, mat + brand).
Matching is restricted to the set's own m list (brand must match, then best name-token overlap), so no new picks can appear.
Gate [16] re-runs this matcher and fails if any set's rendered pick order disagrees with its live album.
Usage: python3 builder/fym_fix_oct21/album_order.py <build_dir> [--report]"""
import sys, os, json, re
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
LIVE = REPO + 'scripts/social/its_a_match/albums-live-oct21.json'
STOP = {'mat', 'mats', 'mahjong', 'mahj', 'the', 'and', 'retired', 'neoprene', 'leatherette', 'scalloped', 'in', 'tube', 'game', 'copy',
        'pre', 'order', 'american', 'mahjongg', 'a', 'of', 'vegan', 'leather', 'x'}

def toks(s):
    s = re.sub(r'\(.*?\)', ' ', (s or '').lower()).replace('&', ' and ').replace('’', '').replace("'", '')
    return {t for t in re.findall(r'[a-z0-9]+', s) if t not in STOP}

def nb(s):
    s = (s or '').lower().replace('&', 'and')
    for w in ('mahjongg', 'mahjong', 'mahj', 'holiday', 'co.', 'design', 'designs', 'boutique'): s = s.replace(w, '')
    return re.sub(r'[^a-z]', '', s)

def set_for_album(D, slug):
    for s in D['sets']:
        if s.get('album', '').rstrip('/').endswith('/' + slug + '-mahjong-tile-matches'): return s
    slug = {'sunday-tile-set': 'sunday-mahjong-sunday'}.get(slug, slug)
    c = [s for s in D['sets'] if s['slug'].endswith('-' + slug) or s['slug'] == slug]
    return c[0] if len(c) == 1 else None

def _t(s):
    s = re.sub(r'\byotd\b', 'year dragon', (s or '').lower())
    return toks(s)

def score(card, mid, M):
    """None if brand differs or no name overlap; else a sortable score (higher = better)."""
    m = M.get(mid)
    if not m: return None
    bt = nb(card['brand']); mb = nb(m.get('bn', ''))
    if not (mb == bt or (len(bt) > 3 and (bt in mb or mb in bt))): return None
    nt = _t(card['mat']); mt_n = _t(m.get('n', ''))
    mt = mt_n | (_t(mid.split('/')[-1].replace('-', ' ')) if '/' in mid else set())
    if not nt: return None
    hit = lambda t, pool: t in pool or (len(t) == 1 and any(x.startswith(t) for x in pool))
    ov = sum(1 for t in nt if hit(t, mt))
    if ov == 0: return None
    miss_m = sum(1 for t in mt_n if not hit(t, nt) and not (len(t) == 1 and any(x.startswith(t) for x in nt)))
    exact = int(nt == mt_n)
    ret = int(bool(m.get('rt')) == bool(card.get('retired')))
    return (exact, ov - len(nt), -miss_m, ret)

def assign(cards, cands, M):
    """global greedy: best (card, mat) pairs first, so 'YOTD Purple' cannot take 'YOTD Plum' from the exact 'YOTD Plum' card."""
    pairs = []
    for ci, c in enumerate(cards):
        for mid in cands:
            sc = score(c, mid, M)
            if sc is not None: pairs.append((sc, -ci, mid, ci))
    pairs.sort(reverse=True)
    got, used = {}, set()
    for sc, _, mid, ci in pairs:
        if ci in got or mid in used: continue
        got[ci] = mid; used.add(mid)
    return got

def compute(D):
    A = json.load(open(LIVE)); M = D['mats']
    ao, rep = {}, []
    for a in A:
        s = set_for_album(D, a['slug'])
        if not s or not s.get('m'): rep.append((a['slug'], 'no set / empty m')); continue
        cands = [e[0] for e in s['m']]
        got = assign(a['cards'], cands, M)
        order = [got[i] for i in range(len(a['cards'])) if i in got]
        ao[s['slug']] = order
        rep.append((a['slug'], f'{len(order)}/{len(a["cards"])} cards matched, m={len(cands)}'))
    return ao, rep

def sorted_m(s, ao):
    o = ao.get(s['slug'])
    if not o: return [e[0] for e in s['m']]
    pos = {k: i for i, k in enumerate(o)}
    ids = [e[0] for e in s['m']]
    return sorted(ids, key=lambda k: (pos.get(k, 1e6), ids.index(k)))

if __name__ == '__main__':
    p = os.path.join(sys.argv[1], 'index.html'); h = open(p).read(); i = h.find('const D=') + 8
    D, end = json.JSONDecoder().raw_decode(h, i)
    ao, rep = compute(D)
    mism = [s['slug'] for s in D['sets'] if s['slug'] in ao and [e[0] for e in s['m']] != sorted_m(s, ao)]
    for r in rep: print(' ', *r)
    print('sets whose stored m order differs from the live album:', len(mism), mism)
    if '--report' in sys.argv: sys.exit(0)
    D['ao'] = ao
    h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
    open(p, 'w').write(h); print('wrote D.ao for', len(ao), 'sets')
