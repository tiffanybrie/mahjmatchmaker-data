"""FYM v104 (Oct 30) rank fix: mats that were APPENDED to the end of every set's ranking instead of colour-ranked.
QA Oct 30 (v104 E1): the 7 new partner sweep mats (and, it turned out, ~65 earlier adds since Oct 25: v101 partner sweep, Etsy/ShopMy,
Fait a Main, Bespoke side B, House of Hearts, Oct 25 audit) sat at the tail of EVERY s.rank in identical order, so in the mat door
(setsForMat sorts sets by s.rank position) every one of them showed the same tile order (non-partner Coquette first), and in the
tiles door they were missing from s.cr (colour deck) entirely.
Fix, without disturbing any existing order:
 1. STUCK = visible mats whose position from the END of s.rank is <= TAIL in every set (appended, never ranked).
 2. Full colour ranking per set from the same scorers the build uses, run on a scratch copy with the 300 cut-off removed:
    v95_matrank.py (non-holiday sets: back colour, partner-first tie-break, motif) and v85_colorrank.py (holiday tile sets).
 3. s.rank: drop STUCK, then put each STUCK mat in at the same relative depth as its score in that set's full ranking
    (so the mat door, which sorts sets by s.rank position, lists the sets the mat scores best for).
    s.cr: each STUCK mat goes right after its nearest better-scored neighbour (anchor), but only for STUCK mats inside that set's scored top 300 (the cr cut-off), and never ahead of the set's leading
    coordinated / pinned block (anything already at the front stays at the front).
Her picks (s.m), D.mord and every non-STUCK position are untouched. Idempotent. Gate [107].
Usage: python3 v104rank.py <build_dir> [--report out.json]"""
import sys, os, json, shutil, tempfile, io, contextlib
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
TAIL = 130
B = sys.argv[1]; P = B + '/index.html'


def load(p):
    h = open(p).read(); i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); return h, i, end + i, D


h, i, end, D = load(P)
M, O, S = D['mats'], D['order'], D['sets']; OI = {k: j for j, k in enumerate(O)}
tail = {k: 0 for k in M}; seen = {k: 0 for k in M}
for s in S:
    r = s['rank']; L = len(r)
    for p, j in enumerate(r): k = O[j]; tail[k] = max(tail[k], L - p); seen[k] += 1
STUCK = {OI[k] for k, m in M.items() if not m.get('hid') and seen[k] and tail[k] <= TAIL}
print('stuck mats', len(STUCK))


def full_rank(script, holiday_only):
    """Run a builder ranking script on a scratch copy with the 300 cut-off removed; return {slug: [order idx...]}."""
    tmp = tempfile.mkdtemp()
    for f in os.listdir(B):
        if f != 'index.html': os.symlink(os.path.join(os.path.abspath(B), f), os.path.join(tmp, f))
    shutil.copy(P, tmp + '/index.html')
    path = REPO + '/builder/fym_fix_oct25/' + script
    src = open(path).read()
    assert src.count('out[:300]') == 1, script
    src = src.replace('out[:300]', 'out')
    old = sys.argv; sys.argv = [path, tmp]
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(src, path, 'exec'), {'__file__': path, '__name__': '__main__'})
    finally:
        sys.argv = old
    _, _, _, D2 = load(tmp + '/index.html'); shutil.rmtree(tmp)
    import re
    hb = open(P).read(); mm = re.search(r'BACKG=(\{.*?\});', hb); HOL = set(json.loads(mm.group(1)).get('Holiday', [])) if mm else set()
    return {s['slug']: s.get('cr') or [] for s in D2['sets'] if (s['name'] in HOL) == holiday_only}


FULL = full_rank('v95_matrank.py', False); FULL.update(full_rank('v85_colorrank.py', True))


def place(cur, full, movable, front_keep):
    """cur: existing list. Remove movable, re-insert each after its nearest preceding non-movable neighbour in `full`."""
    base = [j for j in cur if j not in movable]
    inbase = set(base)
    after = {}  # anchor -> [movable...] in full order
    lead = []
    last = None
    for j in full:
        if j in movable: (after.setdefault(last, []) if last is not None else lead).append(j)
        elif j in inbase: last = j
    out = base[:front_keep] + lead + base[front_keep:] if lead else list(base)
    res = []
    for j in out:
        res.append(j)
        if j in after: res.extend(after[j])
    placed = set(res)
    res += [j for j in cur if j in movable and j not in placed]  # unscored (no colour data): stay at the end, as before
    return res


COORD = {k: [OI[m] for m in v if m in OI] for k, v in json.load(open(REPO + '/config/fym-coordinated.json')).items() if not k.startswith('_')}
rep = {}; nr = nc = 0
for s in S:
    full = FULL.get(s['slug'])
    if not full: continue
    co = set(COORD.get(s['slug'], []))
    def lead_n(L):  # her coordinated brand mats sit first (v92, gate [57]): never insert ahead of them
        n = 0
        while n < len(L) and L[n] in co: n += 1
        return n
    # s.rank (what the mat door sorts sets by): each STUCK mat goes in at the same RELATIVE depth as its colour score in this set
    # (top 1% of the full scored list -> top 1% of rank). The anchor method (used for s.cr below) inherits the old rank's quirks.
    base = [j for j in s['rank'] if j not in STUCK]; ln = lead_n(base); fi = {j: n for n, j in enumerate(full)}
    ins = sorted(((max(ln, round(fi[j] / len(full) * len(base))), fi[j], j) for j in STUCK if j in fi and j in set(s['rank'])))
    newr = []; q = 0
    for n, j in enumerate(base):
        while q < len(ins) and ins[q][0] <= n: newr.append(ins[q][2]); q += 1
        newr.append(j)
    newr += [x[2] for x in ins[q:]] + [j for j in s['rank'] if j in STUCK and j not in fi]
    assert sorted(newr) == sorted(s['rank']), s['slug']
    if newr != s['rank']: s['rank'] = newr; nr += 1
    cr = s.get('cr') or []
    if cr:
        top = set(full[:300]); movc = {j for j in STUCK if j in top}
        keep = [j for j in cr if j not in STUCK]; ks = set(keep)
        sub = [j for j in full if j in movc or j in ks]
        newc = place(keep + sorted(movc), sub, movc, lead_n(keep))
        newc = [j for j in newc if j in ks or j in movc]
        if newc != cr: s['cr'] = newc; nc += 1
    rep[s['slug']] = [M[O[j]]['n'] + ' | ' + M[O[j]]['bn'] for j in (s.get('cr') or s['rank'])[:8]]
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
open(P, 'w').write(h)
if '--report' in sys.argv: json.dump(rep, open(sys.argv[sys.argv.index('--report') + 1], 'w'), indent=1, ensure_ascii=False)
print('v104rank: stuck', len(STUCK), '| rank changed', nr, '| cr changed', nc, 'of', len(S))
