"""FYM v71: Tiffany's swipe-book YES votes go into her match lists (Tiffany Oct 21 6:44pm, Tinselle Ruby Red showed only
Festive Plaid + The Polo Club: "No way I only match those two"). Rule 4: Tiffany's match = album pick OR swipe-book yes.
Usage: python3 builder/fym_fix_oct21/swipe_yeses.py <build_dir> [--report]
Reads config/swipe-yeses/*.json (vote snapshots from each swipe book's db), maps book ids to FYM mat keys / set slugs,
adds every missing yes to the set's m (racks = the set's tile racks: D.lt, else racks every existing entry shares),
marks the set sb=true when it has yeses but no album (otherwise the runtime guard would blank m), updates locks.json
(approved: her own recorded yeses) and writes builder/fym_flags/swipe_yeses_map.json {slug: [mat keys]} for gate [25]
(m must contain every recorded yes that is a visible mat). Yeses that cannot be mapped or point at hidden mats are reported."""
import sys, os, json, glob, re
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '..', '..')) + '/'
B = sys.argv[1]; REPORT = '--report' in sys.argv
P = os.path.join(B, 'index.html'); h = open(P).read(); i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
M = D['mats']
SET_ALIAS = {'sunday': 'sunday-mahjong-sunday', 'plum-panda': 'sunday-mahjong-plum-panda', 'hummingbird': 'sunday-mahjong-hummingbird',
             'nature-walk': 'sunday-mahjong-nature-walk', 'sunday-blues': 'sunday-mahjong-sunday-blues', 'december-1994': 'sunday-mahjong-december-1994'}
slugs = {s['slug'] for s in D['sets']}
def set_slug(x):
    x = re.sub(r'^hol-', '', x); x = SET_ALIAS.get(x, x)
    return x if x in slugs else None
nz = lambda s: re.sub(r'[^a-z0-9]', '', (s or '').lower().replace('&', 'and'))
def mat_by_name(n, bn):
    c = [k for k, o in M.items() if nz(o['n']).startswith(nz(n)) and (not bn or nz(o.get('bn')) == nz(bn))]
    c.sort(key=lambda k: (bool(M[k].get('hid')), len(M[k]['n'])))
    return c[0] if c else None
def mat_by_handle(hd):
    c = [k for k in M if k.split('/', 1)[-1].split('?')[0] == hd or k.split('/', 1)[-1].startswith(hd)]
    c.sort(key=lambda k: (bool(M[k].get('hid')), len(k)))
    if c: return c[0]
    if hd == 'omm-merry-mahjong': return mat_by_name('Merry Mahjong', 'Oh My Mahjong')
    if hd == 'polo-club': return mat_by_name('The Polo Club', None)
    if hd == 'festive-plaid': return mat_by_name('Festive Plaid', 'Sunday Mahjong')
    if hd == 'cmc-ski-club-red-sweater': return next((k for k in M if 'ski' in k and 'red-sweater' in k), None)
    if hd == 'holidayloveredgreen': return next((k for k in M if 'holiday-love' in k.lower() and 'red' in M[k]['n'].lower()), None)
    return None
want, unmapped = {}, []
for f in sorted(glob.glob(REPO + 'config/swipe-yeses/*.json')):
    for bk, b in json.load(open(f))['books'].items():
        for g, it in b['yes']:
            if b['mode'] == 'tile':
                sl = set_slug(g); mk = (mat_by_name(*b['items'][it]) if b.get('items', {}).get(it) else mat_by_handle(it))
            else:
                sl = set_slug(it); gm = b['groups'].get(g); mk = mat_by_name(*gm) if gm else None
            if not sl or not mk: unmapped.append((bk, g, it, sl, mk)); continue
            want.setdefault(sl, []); (mk in want[sl]) or want[sl].append(mk)
L = json.load(open(REPO + 'builder/fym_flags/locks.json'))
added, hidden, sbset = {}, [], []
for s in D['sets']:
    ks = want.get(s['slug'])
    if not ks: continue
    have = {e[0] for e in s['m']}
    base = list((D.get('lt') or {}).get(s['slug']) or ([r for r in s['m'][0][1] if all(r in e[1] for e in s['m'])] if s['m'] else []))
    for k in ks:
        if k in have: continue
        if M[k].get('hid'): hidden.append((s['slug'], M[k]['n'])); continue
        s['m'].append([k, base]); have.add(k); added.setdefault(s['slug'], []).append(M[k]['n'])
    if added.get(s['slug']) and not (s.get('album') or s.get('sb')):
        s['sb'] = True; sbset.append(s['slug'])
    if s['slug'] in added and s['slug'] in L['sets']:
        L['sets'][s['slug']]['m'] = s['m']
        if s.get('sb'): L['sets'][s['slug']]['sb'] = True
json.dump({sl: [k for k in ks if not M[k].get('hid')] for sl, ks in want.items()}, open(REPO + 'builder/fym_flags/swipe_yeses_map.json', 'w'), indent=1)
print('sets with yeses', len(want), '| sets changed', len(added), '| entries added', sum(map(len, added.values())), '| sb set on', sbset)
for sl, n in sorted(added.items()): print(f'  {sl}: +{len(n)} ' + ', '.join(n))
if hidden: print('skipped hidden mats:', hidden)
if unmapped: print('unmapped yeses (no FYM set / mat):', len(unmapped)); [print('  ', u) for u in unmapped[:40]]
if not REPORT:
    if added:
        L['_changes'].append({'date': '2026-10-21', 'set': ','.join(sorted(added)), 'field': 'm' + (' + sb' if sbset else ''),
                              'change': f"added {sum(map(len, added.values()))} swipe-book YES picks (config/swipe-yeses)" + (f"; sb=true on {sbset}" if sbset else ''),
                              'approval': "Tiffany Oct 21 6:44pm: her swipe-book yeses are her matches (Tinselle Ruby Red showed only 2). Rule 4 real picks."})
        json.dump(L, open(REPO + 'builder/fym_flags/locks.json', 'w'), ensure_ascii=False, indent=1)
    h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
    open(P, 'w').write(h)
