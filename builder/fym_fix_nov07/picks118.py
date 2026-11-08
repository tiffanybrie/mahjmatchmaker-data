"""FYM 1.18: Tiffany's yeses from the album missed-mats page (Nov 7; config/picks/missed-mats-round1-2026-11-07.txt). A YES IS A YES:
each "Album: Mat (Brand), ..." pair goes into that tile set's Tiffany's-match list (s.m, entry [mat key, []]: no rack picks yet), at the
end of her existing list. "(holiday)" lines too: holiday mats already sit in year-round sets' m lists (40 sets in v117; the app keeps
holiday mats in holiday use). The approved list is also written to builder/fym_flags/locks.json (sets.<slug>.m), so locks never undo it.
Mapping: album name -> docs/audits/album-missed-mats-2026-11-07.json album slug -> the FYM set whose album URL is /<slug>-mahjong-tile-matches
(or config/album-fym-sets.json colorcards); mat name + brand -> the key the audit listed for that album (exact pair), else a unique
name + brand match among FYM mats. Not added (reported): albums with no FYM set (retired vault sets), mats hidden in FYM (gate [11]),
pairs that cannot be mapped. Idempotent. Usage: python3 builder/fym_fix_nov07/picks118.py <build dir> [--report out.json]"""
import sys, os, json, re, unicodedata
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'
h = open(P).read(); i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:]); e += i
nz = lambda x: re.sub(r'[^a-z0-9]', '', ''.join(c for c in unicodedata.normalize('NFD', str(x or '').replace('&', 'and')) if not unicodedata.combining(c)).lower())
AUD = json.load(open(R + 'docs/audits/album-missed-mats-2026-11-07.json'))['albums']
CC = json.load(open(R + 'config/album-fym-sets.json'))['colorcards']
BYNAME = {nz(v['name']): k for k, v in AUD.items()}
def set_for(slug):
    for s in D['sets']:
        if re.search(rf'/{re.escape(slug)}-mahjong-tile-matches(?:$|[#?/])', s.get('album') or ''): return s
    if CC.get(slug):
        return next((s for s in D['sets'] if s['slug'] == CC[slug]), None)
    return None
def split_pairs(t):  # "Mat (Brand), Mat (X) (Brand)" -> [(mat, brand)]; brand = the LAST (...) of each item
    out, depth, cur = [], 0, ''
    for ch in t:
        depth += ch == '('; depth -= ch == ')'
        if ch == ',' and depth == 0: out.append(cur.strip()); cur = ''
        else: cur += ch
    if cur.strip(): out.append(cur.strip())
    res = []
    for it in out:
        m = re.match(r'^(.*)\(([^()]*)\)\s*$', it)
        res.append((m.group(1).strip(), m.group(2).strip()) if m else (it, ''))
    return res
M = D['mats']; NB = {}
for k, o in M.items(): NB.setdefault((nz(o['n']), nz(o.get('bn'))), []).append(k)
rep = {'added': [], 'already': [], 'no_fym_set': [], 'hidden': [], 'unmapped': []}
L = json.load(open(R + 'builder/fym_flags/locks.json'))
for line in open(R + 'config/picks/missed-mats-round1-2026-11-07.txt'):
    if ':' not in line or line.startswith('My yeses'): continue
    alb, rest = line.split(':', 1); alb = alb.strip(); base = re.sub(r'\s*\(holiday\)\s*$', '', alb)
    aslug = BYNAME.get(nz(base)); s = set_for(aslug) if aslug else None
    for mat, brand in split_pairs(rest.strip()):
        if not s: rep['no_fym_set'].append(f'{alb}: {mat} ({brand})'); continue
        cand = [x['key'] for x in AUD[aslug].get('strong', []) if nz(x['name']) == nz(mat) and nz(x['brand']) == nz(brand)]
        if not cand: cand = NB.get((nz(mat), nz(brand)), [])
        if not cand: cand = [k for (n_, b_), ks in NB.items() if n_ == nz(mat) for k in ks if brand in ('Etsy', 'Amazon')]  # store label vs maker
        cand = [k for k in dict.fromkeys(cand) if k in M]
        if len(cand) != 1: rep['unmapped'].append(f'{alb}: {mat} ({brand}) -> {cand or "no FYM mat"}'); continue
        k = cand[0]
        if M[k].get('hid'): rep['hidden'].append(f"{alb}: {mat} ({brand}) = {k}"); continue
        if any(x[0] == k for x in s['m']): rep['already'].append(f'{s["name"]}: {mat}'); continue
        s['m'].append([k, []]); rep['added'].append(f"{s['name']} ({s['slug']}): {mat} ({brand}){' [holiday line]' if alb != base else ''}")
    if s and s['slug'] in L['sets']: L['sets'][s['slug']]['m'] = s['m']
    elif s: L['sets'][s['slug']] = {'m': s['m'], 'name': s['name']}
open(P, 'w').write(h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[e:])
json.dump(L, open(R + 'builder/fym_flags/locks.json', 'w'), indent=1, ensure_ascii=False)
print('picks118:', {k: len(v) for k, v in rep.items()})
for k in ('no_fym_set', 'hidden', 'unmapped'):
    for x in rep[k]: print(' ', k, '|', x)
if '--report' in sys.argv: json.dump(rep, open(sys.argv[sys.argv.index('--report') + 1], 'w'), indent=1, ensure_ascii=False)
