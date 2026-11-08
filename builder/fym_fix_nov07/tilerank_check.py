"""FYM gate [168] (Nov 7 2026, FYM 1.18; Tiffany 10:33pm: Lotus Cove's mat door showed Halloween tile sets ~10 deep).
Checks the tiles-for-a-mat ranking built by tilerank_v118.py, replaying the mat door's deck (setsForMat0 + tAll: her picks first,
holiday sets only for holiday / works-for-holiday mats, album + catalog sorted as one list by D.tso, BCAP brand cap 6, no two of
one brand in a row):
 a. the app code is patched (marker + D.tso helpers + TSOM in tAll) and D.tso covers every visible mat;
 b. FAIL: a visible non-holiday mat has a themed or holiday tile set (D.tsoB) in its first 15 tile sets, unless it is her pick
    or the brand's coordinated pair (config/fym-coordinated.json);
 c. colour families, 30 most-matched mats: the first 10 RANKED tile sets' (after her picks) BACK colours should share a colour family with the mat (mat
    families = mf + ha + every measured swatch >= 5%). Misses are printed; FAIL when a mat has fewer than 6 of 10.
Usage: python3 tilerank_check.py <build_dir>   (exit 1 on FAIL)"""
import sys, os, json, collections
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
import tilerank_v118 as TR


def deck(D, BG, k, OI):
    M, S, T = D['mats'], D['sets'], D['tiles']; m = M[k]; ix = OI[k]
    s = D['tso'][ix]; q = {int(s[j:j + 2], 36): j // 2 for j in range(0, len(s), 2)}; tb = set(D.get('tsoB') or [])
    HOL = set(BG.get('Holiday', []))
    her, rest = [], []
    for n, st in enumerate(S):
        if st.get('hid') or (T.get(st['tile']) or {}).get('hid'): continue
        if any(x[0] == k for x in st['m']): her.append(n); continue
        if not (m.get('hol') or m.get('wfh')) and st['name'] in HOL: continue
        p = q[n] if n in q else 1e6 + (1e6 if n in tb else 0) + max(0, st['rank'].index(ix) if ix in st['rank'] else 1e5)
        rest.append((p, n))
    rest = [n for _, n in sorted(rest)]
    bo = lambda n: (T.get(S[n]['tile']) or {}).get('bn') or S[n]['maker']
    out, pend, cnt = [], rest[:], collections.Counter()
    while pend and len(out) < 30:
        last = bo(out[-1]) if out else None
        j = next((j for j, x in enumerate(pend) if cnt[bo(x)] < 6 and bo(x) != last), None)
        if j is None: j = next((j for j, x in enumerate(pend) if cnt[bo(x)] < 6), None)
        if j is None: break
        x = pend.pop(j); out.append(x); cnt[bo(x)] += 1
    return her, out + pend


def run(B):
    h, i, end, D = TR.load(B + '/index.html'); BG = TR.backg(h); F = []
    for mk in (TR.MARK + 'const TSOC=', 'BCAP(TSOM([...g.alb,...g.cat])', TR.MARK + 'const TQ=TSO(ix)'):
        if mk not in h: F.append(f"[168] app code not patched ({mk[:40]}): run builder/fym_fix_nov07/tilerank_v118.py")
    M, S, O = D['mats'], D['sets'], D['order']; OI = {k: j for j, k in enumerate(O)}
    if not D.get('tso') or len(D['tso']) != len(O): F.append('[168] D.tso missing or wrong length'); return F
    vis = [k for k, m in M.items() if not m.get('hid') and k in OI]
    nos = [k for k in vis if not D['tso'][OI[k]] and (m := M[k]).get('ms')]
    if nos: F.append(f"[168] {len(nos)} visible mats with colour data have no tile order (D.tso): {nos[:5]}")
    CO = {kk: set(v) for kk, v in json.load(open(TR.REPO + '/config/fym-coordinated.json')).items() if not kk.startswith('_')}
    TB = set(D.get('tsoB') or []); bad = []; HOLN = set(BG.get('Holiday', []))
    cfg = json.load(open(TR.REPO + '/config/fym-tilerank-nov07.json'))
    for k in vis:
        if M[k].get('hol') or not D['tso'][OI[k]]: continue
        her, rest = deck(D, BG, k, OI)
        top = (her + rest)[:15]
        mth = TR.theme_re(cfg)
        mt = next((t for t, r in mth.items() if r.search(M[k]['n'])), None) if M[k]['n'] not in cfg['not_themed'] else None
        def allowed(n):
            nm = S[n]['name']
            if n in her or k in CO.get(S[n]['slug'], ()): return True
            if nm in HOLN: return bool(M[k].get('wfh'))           # works-for-holiday mats count as holiday (Oct 21)
            return nm not in cfg['not_themed'] and mt is not None and mth[mt].search(nm) is not None
        th = [S[n]['name'] for n in top if n in TB and not allowed(n)]
        if th: bad.append(f"{M[k]['n']} ({M[k]['bn']}): {', '.join(th)}")
    if bad: F.append(f"[168] {len(bad)} non-holiday mats have a themed/holiday tile set in their first 15: " + '; '.join(bad[:8]))
    # c. colour families on the 30 most-matched mats
    TV = json.load(open(TR.REPO + '/config/tableview-back-colors.json'))
    C = json.load(open(TR.REPO + '/config/fym-colour-oct25.json'))
    def back(s):
        if isinstance(TV.get(s['slug']), dict) and TV[s['slug']].get('back'): return TV[s['slug']]['back']
        if s['slug'] in cfg['backs']: return cfg['backs'][s['slug']]
        if s.get('bsw'): return s['bsw'][0][0]
        return (C['sets'].get(s['slug']) or {}).get('back') or s.get('tc') or '#f3f1ea'
    cnt = collections.Counter(x[0] for s in S for x in s['m'])
    pop = [k for k, _ in cnt.most_common() if k in OI and not M[k].get('hid') and D['tso'][OI[k]]][:30]
    tot = hit = 0; miss = []
    for k in pop:
        m = M[k]; fam = set(m.get('mf') or []) | set(m.get('ha') or [])
        for hx, w in (m.get('ms') or []):
            if w >= .05: fam |= TR.family(hx)
        her, rest = deck(D, BG, k, OI); top = rest[:10]   # the ranking's own first 10 (her picks are her call and come first)
        ok = [n for n in top if TR.family(back(S[n])) & fam]
        tot += len(top); hit += len(ok)
        ms = [f"{S[n]['name']} ({back(S[n])})" for n in top if n not in ok]
        if ms: miss.append(f"{m['n']}: {len(ok)}/10, misses " + ', '.join(ms))
        if len(ok) < 6: F.append(f"[168] {m['n']} ({m['bn']}): only {len(ok)} of its first 10 tile sets share a colour family with it ({', '.join(ms)})")
    print(f"FYM GATE INFO [168] colour families: {hit}/{tot} of the first-10 tile sets share a back colour family with the mat (30 most-matched mats)")
    for x in miss: print('  [168] ' + x)
    return F


if __name__ == '__main__':
    F = run(sys.argv[1])
    if F:
        print(f"[168] FAIL ({len(F)})"); [print('  ' + f) for f in F]; sys.exit(1)
    print('[168] PASS: tiles-for-a-mat ranking')
