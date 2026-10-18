"""Mat-edition albums into FYM (Oct 18): Vivienne, Larkspur, Peony & Parasol.
Idempotent patch on the PENDING FYM build (scratchpad/fymfix2/build/index.html; re-run after any rebuild of that file):
1. Each tile set on a mat-edition album card gets that mat in its Tiffany's-matches list (s.m), appended after its own
   album order if missing, with the card's tile racks (labels -> rack ids).
2. D.mord = {mat id: [set indices in the mat album's order]}; setsForMat() sorts "her" sets by that order when the mat has
   one, so the mat door shows the mat album in her order (Vivienne: her swipe ranking; Larkspur/Peony: album order).
Sets not in FYM (vault Spring Love / Lilac Soiree) are reported, not added.
Usage: python3 patch.py [path/to/index.html]"""
import json, re, sys
REPO = '/home/claude/mahjmatchmaker-data/'
B = sys.argv[1] if len(sys.argv) > 1 else '/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/fymfix2/build/index.html'
s = open(B).read(); i = s.index('const D=') + 8; j = s.index('\n', i)
line = s[i:j]; tail = line[len(line.rstrip()) - 1:] if line.rstrip().endswith(';') else ''
D = json.loads(line.rstrip()[:-1]); M = D['mats']; R = D['racks']
byname = {}
for x in D['sets']:  # duplicate names (e.g. two Seabreezes): keep the album / Oh My Mahjong one
    if x['name'] not in byname or (x.get('album') and not byname[x['name']].get('album')) or (x.get('maker') == 'Oh My Mahjong' and byname[x['name']].get('maker') != 'Oh My Mahjong'): byname[x['name']] = x
IDX = {id(x): k for k, x in enumerate(D['sets'])}
RN = {v['n']: k for k, v in R.items()}
def rid(label):
    if label.startswith('Bird & Bamboo '): return 'bb:' + label[len('Bird & Bamboo '):]
    return RN.get(label)
ALIAS = {'jade': 'Miss Classic Jade', 'tortoise': 'Classic Tortoise', 'heritage-2-0': 'Heritage 2.0'}
def setname(slug):
    slug = slug.replace('vault-', '')
    if slug in ALIAS and ALIAS[slug] in byname: return ALIAS[slug]
    import unicodedata
    norm = lambda t: re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode().lower())
    k = norm(slug)
    return next((n for n in byname if norm(n) == k), None)
def specs():
    viv = json.load(open(REPO + 'scripts/albumcard/specs/vivienne.json'))
    yield 'www.ohmymahjong.com/vivienne-mat-in-tube', [(c['slug'], c['racks']) for c in viv['cards']]
    lk = {c['slug']: c for c in json.load(open(REPO + 'scripts/albumcard/specs/larkspur.json'))['cards']}
    lo = json.load(open(REPO + 'config/larkspur-album-order.json'))['larkspur']  # her approved Larkspur order
    yield 'www.ohmymahjong.com/larkspur-mat-in-tube', [(sl, lk[sl]['racks']) for sl in lo if sl in lk]
    pp = json.load(open(REPO + 'scripts/albumcard/specs/peony_parasol_spec.json'))
    yield 'splashofcolorco.com/peony-and-parasol', [(c['file'].split('-mahjong-tiles-')[0], c['racks']) for c in pp['cards']]
D.setdefault('mord', {}); report = {}
for mid, cards in specs():
    assert mid in M, mid
    order, added, absent = [], [], []
    for slug, racks in cards:
        n = setname(slug)
        if not n: absent.append(slug); continue
        st = byname[n]; order.append(IDX[id(st)])
        if not any(x[0] == mid for x in st['m']):
            st['m'].append([mid, [r for r in (rid(l) for l in racks) if r]]); added.append(n)
    removed = []
    for k, x in enumerate(D['sets']):  # catalog sets (no album) can't be her match for a mat-edition mat unless on its album
        if x.get('cat') and not x.get('album') and k not in order and any(y[0] == mid for y in x['m']):
            x['m'] = [y for y in x['m'] if y[0] != mid]; removed.append(x['name'] + ' (' + x['maker'] + ')')
    D['mord'][mid] = order
    report[M[mid]['n']] = {'order': [D['sets'][k]['name'] + ' (' + D['sets'][k]['maker'] + ')' for k in order], 'added': added, 'removed_unsupported': removed, 'not_in_fym': absent}
OLD = "const her=rows.filter(r=>r.her).map(r=>Object.assign(r,{hp:r.s.m.findIndex(x=>x[0]===id)})).sort((a,b)=>a.hp-b.hp)"
NEW = "const MO=(D.mord||{})[id];const her=rows.filter(r=>r.her).map(r=>Object.assign(r,{hp:MO&&MO.indexOf(r.i)>=0?MO.indexOf(r.i)-1e6:r.s.m.findIndex(x=>x[0]===id)})).sort((a,b)=>a.hp-b.hp)"
s2 = s[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + ';' + s[j:]
if NEW not in s2:
    assert s2.count(OLD) == 1, 'setsForMat signature changed'
    s2 = s2.replace(OLD, NEW)
open(B, 'w').write(s2)
json.dump(report, open(REPO + 'builder/fym_mated_oct18/report.json', 'w'), indent=1, ensure_ascii=False)
print(json.dumps(report, indent=1, ensure_ascii=False))
