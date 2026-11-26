"""FYM 1.23.1 (Nov 26): Tiffany's album picks for the three Bam Bird Deco sets (Indigo, Mulberry, Lagoon) go into each set's
Tiffany's-match list (s.m = [[mat key, [rack keys]]], album order = assets/cards/<album>/manifest.json card order) and s.album = <album slug>,
s.cat = False, so 'Tiffany's Picks' shows (Tiffany Nov 26 9:36am: no Tiffany's Picks for Indigo). Mats not in the app yet are reported
(not added; they need an all-or-nothing bring-in). Hidden mats are skipped (gate [11]). Also written to builder/fym_flags/locks.json.
Usage: python3 builder/fym_fix_nov26/deco_picks.py <build dir> [--report out.json]"""
import sys, os, json, re
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'
h = open(P).read(); i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:]); e += i
M = D['mats']; RK = D['racks']
nz = lambda s: re.sub(r'[^a-z0-9]', '', (s or '').lower().replace('&', 'and'))
FIX = {'Deco Dragon (Indigo)': 'www.bambirdboutique.com/deco-neoprene-mahjong-mat-copy-2?v=67663098282293',
       'Deco Dragon (Lagoon)': 'www.bambirdboutique.com/deco-neoprene-mahjong-mat-copy-2?v=67663098315061',
       'Deco Dragon (Mulberry)': 'www.bambirdboutique.com/deco-neoprene-mahjong-mat-copy-2?v=67663098347829'}
BBR = {'Bam Bird Boutique Indigo': 'www.bambirdboutique.com/wooden-mahjong-rack-pusher-set?v=52307844137269',
       'Bam Bird Boutique Mulberry Wood': 'www.bambirdboutique.com/wooden-mahjong-rack-pusher-set?v=52307844202805',
       'Bam Bird Boutique Teal Wood': 'www.bambirdboutique.com/wooden-mahjong-rack-pusher-set?v=52307844235573',
       'Bam Bird Boutique Lagoon Wood': 'www.bambirdboutique.com/wooden-mahjong-rack-pusher-set?v=53275469938997'}
RN = {}
for k, r in RK.items(): RN.setdefault(nz((r.get('bn') or '') + ' ' + (r.get('n') or '')), k); RN.setdefault(nz(r.get('n')), k)
NB = {}
for k, o in M.items(): NB.setdefault((nz(o['n']), nz(o.get('bn'))), []).append(k)
def mat(c):
    if c['mat'] in FIX: return FIX[c['mat']]
    if c.get('fym') in M: return c['fym']
    nm = re.sub(r'\s*\(retired\)', '', c['mat'])
    for key in [(nz(nm), nz(c['brand'])), (nz(c['mat']), nz(c['brand']))]:
        if len(NB.get(key, [])) == 1: return NB[key][0]
    cand = [k for k, o in M.items() if nz(o.get('bn')) == nz(c['brand']) and nz(o['n']) and (nz(nm) in nz(o['n']) or nz(o['n']) in nz(nm))]
    return cand[0] if len(cand) == 1 else None
SETS = {'deco-indigo': 'bam-bird-boutique-deco-indigo', 'deco-mulberry': 'bam-bird-boutique-deco-mulberry', 'deco-lagoon': 'bam-bird-boutique-deco'}
L = json.load(open(R + 'builder/fym_flags/locks.json')); L.setdefault('sets', {})
rep = {}
for alb, slug in SETS.items():
    s = next(x for x in D['sets'] if x['slug'] == slug)
    C = json.load(open(R + f'assets/cards/{alb}/manifest.json'))['cards']
    m, seen, r = [], set(), {'added': 0, 'not_in_app': [], 'hidden': []}
    for c in C:
        k = mat(c)
        if not k: r['not_in_app'].append(f"{c['mat']} ({c['brand']})"); continue
        if M[k].get('hid'): r['hidden'].append(f"{c['mat']} ({c['brand']})"); continue
        if k in seen: continue
        seen.add(k)
        rk = [x for x in (BBR.get(n) or RN.get(nz(n)) for n in c.get('racks') or []) if x in RK]
        m.append([k, rk]); r['added'] += 1
    s['m'] = m; s['album'] = alb; s['cat'] = False
    L['sets'].setdefault(slug, {})['m'] = m
    rep[alb] = r
h = h[:i] + json.dumps(D, separators=(',', ':'), ensure_ascii=False) + h[e:]
open(P, 'w').write(h); json.dump(L, open(R + 'builder/fym_flags/locks.json', 'w'), indent=1, ensure_ascii=False)
print(json.dumps(rep, indent=1, ensure_ascii=False))
if '--report' in sys.argv: json.dump(rep, open(sys.argv[sys.argv.index('--report') + 1], 'w'), indent=1, ensure_ascii=False)
