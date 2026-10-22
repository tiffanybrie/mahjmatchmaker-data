"""FYM rack picks per (set, mat) -- Tiffany Oct 22 (DESK "FYM Sunday build" item 7, started early on her 1:39pm call).
Usage: python3 builder/fym_fix_oct22/rack_picks.py <build_dir> [--locks]

Bug: every pairing in a set carried the SET's racks (locks sets.<slug>.m), so a mat's own picks never showed
(Amara + Chinoiserie Songbird showed PLM Pink / B&B Kelly Green / MR&C Tortoise; PLM Chartreuse + Mahj Mood Clear missing).
Cause: config/mat-racks-picks.json (Tiffany Oct 18: "once we've matched the mats, the mats are matched") was only partly
copied into D.lm, keyed by different ids, and never into the pairing lists.

Rule (Tiffany Oct 22 ~1:58pm, chat answer): a pairing's racks = the MAT's own picks first (registry order), THEN the tile
set's racks (what the pairing already had, plus any rack on that pairing's structured album card that was missing).
Mats with no picks of their own keep the tile set's racks unchanged.

Idempotent. Writes D.lm (registry mats resolved to app mat ids) and every sets[].m rack list; with --locks it also
rewrites builder/fym_flags/locks.json sets.<slug>.m to match (logged in locks _changes) so fym_apply_locks keeps it.
Gate [36] in builder/fym_gate.py re-derives the same rule and fails on any drift."""
import sys, os, json, re, glob, datetime
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '..', '..')) + '/'

def norm(s): return re.sub(r'[^a-z0-9]', '', (s or '').lower().replace('&', 'and').replace('(retired)', ''))
def normm(s): return re.sub(r'(mahjong|mahj|mats?)', '', norm(s))

RACK_ALIAS = {  # approved-name spellings in config files -> app rack ids
    'Miss Mahjong Scalloped Iridescent Opal': 'missmahjong.com/iridescent-opal-scalloped-acrylic-racks',
    'Peace Love Mahjong Acrylic Burl': 'peacelovemahjong.com/acrylic-burlwood-mahjong-racks-pushers-set-of-4',
    'Sunday Mahjong Cola': 'sundaymahjong.com/sunday-cola-mahjong-rack-set',
    'Mahjong Row & Co. Scalloped Tortoise': 'mahjongrowandco.com/scalloped-deluxe-tortoise-rack',
}

MAT_ALIAS = {  # registry 'mat' names the app spells differently -> app mat ids
    "Bam! Let's Mahjong Cottage Bloom": 'www.bamletsmahjong.com/cottage-bloom-mahjong-mat-blue-floral-american-mahjong-mat',
    "Bam! Let's Mahjong Posy Pop Watercolor": 'www.bamletsmahjong.com/posy-pop-watercolor-floral-mahjong-mat',
    'Bespoke Mahjong The Chalet Mat (double-sided)': 'www.bespokemahjong.com/double-the-fun-chaletmat',
}

def rack_id(name, RK, by):
    if name in RK: return name
    if name in RACK_ALIAS and RACK_ALIAS[name] in RK: return RACK_ALIAS[name]
    if name.startswith('Bird & Bamboo ') and 'bb:' + name[14:] in RK: return 'bb:' + name[14:]
    if name.startswith('Peace Love Mahjong ') and 'plm:' + name[19:] in RK: return 'plm:' + name[19:]
    return by.get(norm(name))

def mat_ids(D):
    """registry key -> app mat id(s) for config/mat-racks-picks.json entries"""
    M = D['mats']; by = {}
    for k, v in M.items():
        for key in (normm(v.get('bn', '') + v['n']), normm(v['n'])): by.setdefault(key, []).append(k)
    return by

def registry_picks(D, rep):
    REG = json.load(open(REPO + 'config/mat-racks-picks.json'))
    RK = D['racks']; rby = {norm(v['n']): k for k, v in RK.items()}
    by = mat_ids(D); out = {}
    for key, v in REG.items():
        if not isinstance(v, dict) or not v.get('mat') or not v.get('racks'): continue
        cands = [MAT_ALIAS[v['mat']]] if MAT_ALIAS.get(v['mat']) in D['mats'] else by.get(normm(v['mat']), [])
        if not cands:  # app names a mat by name only (no brand) for some entries
            short = normm(re.sub(r'^(Bam! Let\'s Mahjong|Bespoke Mahjong|BettyJuneJeannette|Mahj & Vine|Anders Ruff|Virora Mahjong|Mahj Squad|Miss Mahjong|Oh My Mahjong|Luxe Mahjong|Sunday Mahjong|Mahj Mood|Rebecca Illustrated|Maison Mahj|Mahjong by SI|Charleston Mahjong Club|Mahjong Row & Co\.)\s+', '', v['mat']))
            cands = by.get(short, [])
        ids = [rack_id(r, RK, rby) for r in v['racks']]
        miss = [r for r, i in zip(v['racks'], ids) if not i]
        if miss: rep['unresolved_racks'].append({'mat': v['mat'], 'racks': miss})
        ids = [i for i in ids if i]
        if not cands: rep['unresolved_mats'].append(v['mat']); continue
        for c in cands: out[c] = ids
    return out

def card_records(D):
    """(set slug, mat name) -> tile racks from structured album cards (manifests + gen2 specs)"""
    setby = {}
    for s in D['sets']: setby[norm(s['name'])] = s['slug']; setby[norm(s['slug'])] = s['slug']
    out = {}
    for f in glob.glob(REPO + 'assets/cards/**/manifest.json', recursive=True) + glob.glob(REPO + 'scripts/albumcard/specs/**/*.json', recursive=True):
        try: d = json.load(open(f))
        except Exception: continue
        if not isinstance(d, dict) or not isinstance(d.get('cards'), list): continue
        for c in d['cards']:
            if not isinstance(c, dict) or not c.get('racks'): continue
            slug = setby.get(norm(c.get('set') or c.get('slug') or c.get('title') or d.get('set')))
            mat = c.get('mat') or d.get('mat')
            if slug and mat: out.setdefault((slug, normm(mat)), c['racks'])
    return out

def expected(D, rep=None):
    """returns (lm, {(slug, mat_id): rack list}) per the Oct 22 rule"""
    rep = rep if rep is not None else {'unresolved_racks': [], 'unresolved_mats': []}
    RK = D['racks']; rby = {norm(v['n']): k for k, v in RK.items()}
    reg = registry_picks(D, rep)
    lm = dict(D.get('lm') or {}); lm.update(reg)
    cards = card_records(D); M = D['mats']; want = {}
    for s in D['sets']:
        for e in s.get('m', []):
            mid, cur = e[0], (e[1] if len(e) > 1 and isinstance(e[1], list) else [])
            mp = lm.get(mid, [])
            extra = []
            nm = M.get(mid, {}).get('n', '')
            for r in cards.get((s['slug'], normm(nm)), []) or cards.get((s['slug'], normm(M.get(mid, {}).get('bn', '') + nm)), []):
                i = rack_id(r, RK, rby)
                if i: extra.append(i)
            # tile-set racks = what the pairing had, minus mat picks already placed first
            want[(s['slug'], mid)] = list(dict.fromkeys(mp + [r for r in cur if r in RK or r in mp] + extra))
    return lm, want, rep

if __name__ == '__main__':
    B = sys.argv[1]; P = B + '/index.html'
    h = open(P).read(); i = h.index('const D=') + 8
    D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
    lm, want, rep = expected(D)
    changed = 0; songbird = None
    for s in D['sets']:
        for e in s.get('m', []):
            w = want[(s['slug'], e[0])]
            if (e[1] if len(e) > 1 else None) != w:
                changed += 1
                if len(e) > 1: e[1] = w
                else: e.append(w)
            if s['slug'] == 'amara' and e[0] == 'mahjandvine.com/chinoiserie-song-bird': songbird = w
    D['lm'] = lm
    h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
    open(P, 'w').write(h)
    if '--locks' in sys.argv:
        LP = REPO + 'builder/fym_flags/locks.json'; L = json.load(open(LP)); lc = 0
        for slug, lv in L['sets'].items():
            if 'm' not in lv: continue
            for e in lv['m']:
                w = want.get((slug, e[0]))
                if w is not None and (e[1] if len(e) > 1 else None) != w:
                    lc += 1
                    if len(e) > 1: e[1] = w
                    else: e.append(w)
        L.setdefault('_changes', []).append({'date': datetime.date.today().isoformat(), 'by': 'builder/fym_fix_oct22/rack_picks.py',
            'field': 'm', 'change': f"rack lists per (set, mat): mat's own picks (config/mat-racks-picks.json) first, then the tile set's racks; {lc} pairings",
            'approval': "Tiffany Oct 22 (DESK FYM item 7 + chat ~1:58pm: 'Mat's picks, then tile racks')"})
        json.dump(L, open(LP, 'w'), ensure_ascii=False, indent=1)
        print('locks pairings updated:', lc)
    print('pairings changed:', changed, '| mats with own picks:', len(lm))
    print('Amara + Chinoiserie Songbird ->', [D['racks'][r]['n'] for r in (songbird or [])])
    json.dump(rep, open(B + '/rack_picks_report.json', 'w'), indent=1)
    print('unresolved:', json.dumps(rep)[:600])
