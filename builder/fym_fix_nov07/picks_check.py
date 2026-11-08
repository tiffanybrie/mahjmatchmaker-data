"""Gate [170] (Nov 8, FYM 1.18 QA F1: the artifact slimmed 8 of Juniper's 42 picks + picks on 22 other sets; the website copy hid one).
Every mat in any set's Tiffany's-match list (m) must be SHOWN, with a photo that loads, in every copy:
  build      : not hidden, unless the (set, mat) pair is a documented hidden pick in builder/fym_flags/m_hidden_ok.json (retired / removed
               brands, never-rendering picks Tiffany knows about); a shown pick has a photo file (f) and a thumbnail (th)
  website    : newest site-app/fym-vNN/index.html on origin/fym-site-preview: same hidden state as the build for every pick (a pick the
               build shows may not be hidden there), f + th set, its chunk routed (MCB)
  artifact   : the publish folder (default: pub<NN> next to the build dir, or --artifact <dir>) + <dir>.manifest.json written by
               artifact118.py: same hidden state as the build (never 'ahid'), f + th set, and the photo is in the file loadMC fetches
               for it (mc/190.webp pack for 190-<pack_hi>, else mc/<c>.webp), per the manifest; a file the manifest cannot verify FAILS.
Also prints the Juniper count (her picks shown / m length) for each copy.
Usage (module): run(build_dir, argv) -> (fails, infos)"""
import os, re, json, subprocess
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'


def LD(h):
    i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:]); return D


def img_ids(s):
    out = set()
    for m in re.finditer(r'window\.IMG=Object\.assign\(window\.IMG\|\|\{\},', s):
        o, _ = json.JSONDecoder().raw_decode(s[m.end():]); out |= set(o)
    return out


def run(B, argv=()):
    F, I = [], []
    hb = open(os.path.join(B, 'index.html')).read(); DB = LD(hb)
    ok = {(x['set'], x['key']) for x in json.load(open(REPO + 'builder/fym_flags/m_hidden_ok.json'))['allowed']}
    pairs = [(s['slug'], x[0]) for s in DB['sets'] for x in s.get('m', [])]
    vis = lambda s: not (s.get('hid') or DB['tiles'].get(s['tile'], {}).get('hid'))
    VS = {s['slug'] for s in DB['sets'] if vis(s)}
    shown_b = set()
    for sl, k in pairs:
        o = DB['mats'].get(k)
        if o is None: F.append(f'[170] build: {sl} pick {k} is not a mat'); continue
        if o.get('hid'):
            if (sl, k) not in ok and sl in VS: F.append(f"[170] build: {sl} pick {o.get('n')} ({o.get('bn')}) is hidden and not a documented hidden pick (m_hidden_ok.json)")
            continue
        shown_b.add(k)
        if not o.get('f') or not o.get('th'): F.append(f"[170] build: {sl} pick {o.get('n')} has no photo (f/th)")
    def juniper(D):
        s = next((s for s in D['sets'] if s['slug'] == 'juniper'), None)
        if not s: return 'no Juniper set'
        return f"{sum(1 for x in s['m'] if not D['mats'].get(x[0], {}).get('hid'))}/{len(s['m'])}"
    I.append(f'build Juniper {juniper(DB)}')
    def copy_check(name, D, html, chunk_ok):
        bad = 0
        for sl, k in pairs:
            if k not in shown_b: continue
            o = D['mats'].get(k)
            if not o or o.get('hid') or o.get('ahid'):
                F.append(f"[170] {name}: {sl} pick {DB['mats'][k].get('n')} ({DB['mats'][k].get('bn')}) is hidden{' (artifact slim ahid)' if o and o.get('ahid') else ''} although the build shows it"); bad += 1; continue
            if not o.get('f') or not o.get('th'): F.append(f"[170] {name}: {sl} pick {o.get('n')} has no photo (f/th)"); bad += 1; continue
            why = chunk_ok(o['f'])
            if why: F.append(f"[170] {name}: {sl} pick {o.get('n')} ({o.get('bn')}) photo {o['f']} will not load: {why}"); bad += 1
        I.append(f'{name} Juniper {juniper(D)}')
        return bad
    # website copy
    try:
        g = lambda *a: subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True, timeout=120).stdout
        nn = sorted(int(x) for x in re.findall(r'fym-v(\d+)', g('ls-tree', '--name-only', 'origin/fym-site-preview', 'site-app/')))
        hs = g('show', f'origin/fym-site-preview:site-app/fym-v{nn[-1]}/index.html'); DS = LD(hs)
        mcb = {int(v) for v in re.search(r'MCB=new Set\(\[([0-9, ]+)\]\);', hs).group(1).split(',')}
        def site_ok(f):
            m = re.fullmatch(r'm/(\d+)\.webp', f)
            if not m: return None if f.startswith(('http', 'data:')) else 'not a chunk photo'
            return None if int(m.group(1)) // 12 in mcb else f'chunk {int(m.group(1)) // 12} not routed (MCB)'
        copy_check(f'website fym-v{nn[-1]}', DS, hs, site_ok)
    except Exception as e: F.append(f'[170] website copy check did not run: {e}')
    # artifact folder
    A = None
    if '--artifact' in argv: A = argv[argv.index('--artifact') + 1]
    else:
        m = re.search(r'(\d+)$', os.path.basename(os.path.abspath(B)))
        if m: A = os.path.join(os.path.dirname(os.path.abspath(B)), 'pub' + m.group(1))
    if A and os.path.exists(os.path.join(A, 'index.html')):
        try:
            ha = open(os.path.join(A, 'index.html')).read(); DA = LD(ha)
            man = json.load(open(A.rstrip('/') + '.manifest.json'))
            r = re.search(r"c>=190&&c<=(\d+)\?190:c", ha); hi = int(r.group(1)) if r else 189
            # Nov 8 (1.18 publish): a second pack (split_pack118.py) when mc/190.webp passes the tool's per-file limit
            r2 = re.search(r"\?190:c>=(\d+)&&c<=(\d+)\?(\d+):c", ha); p2 = [int(r2.group(1)), int(r2.group(2))] if r2 and r2.group(1) == r2.group(3) else None
            if (man.get('pack2') or None) != p2: F.append(f"[170] artifact: manifest pack2 {man.get('pack2')} != page routing {p2}")
            if man.get('pack_hi') != hi: F.append(f"[170] artifact: manifest pack range 190-{man.get('pack_hi')} != page routing 190-{hi} (re-run artifact118.py)")
            def art_ok(f):
                m = re.fullmatch(r'm/(\d+)\.webp', f)
                if not m: return None if f.startswith('data:') else 'not a chunk photo'
                c = int(m.group(1)) // 12; p = 'mc/190.webp' if 190 <= c <= hi else f'mc/{p2[0]}.webp' if p2 and p2[0] <= c <= p2[1] else f'mc/{c}.webp'
                if p not in man['files']:
                    return None if f'mc/{c}.json' in man['files'] and p == f'mc/{c}.webp' else f'{p} is not in the artifact'
                if man['files'][p] is None: return f'{p} contents not verifiable (no live mirror copy)'
                return None if f in man['files'][p] else f'not in {p}'
            copy_check('artifact ' + os.path.basename(A.rstrip('/')), DA, ha, art_ok)
            # [170b] (QA2 Nov 8: Fait a Main Texas Mon Amour Chocolate Blue + 5 holiday mats were slimmed): no partner-brand mat
            # (config/fym-partner-coverage.json, code applies or not), no allowed non-partner (nonpartner_allow.json) and, in the
            # holiday season, no holiday mat may be artifact-slimmed ('ahid') while the build shows it. Exempt: the bulk catalogs
            # slimmed by design before 1.18 (manifest slim_by_design_brands: LBB, Luna EK, Noli June, BJ&J).
            cov = {n for b in json.load(open(REPO + 'config/fym-partner-coverage.json'))['brands'] for n in b['fym_names']}
            na = json.load(open(REPO + 'builder/fym_flags/nonpartner_allow.json'))
            prot = cov | set(na.get('partners', [])) | set(na.get('brands', {})); pm = set(na.get('mats', {}))
            byd = set(man.get('slim_by_design_brands', [])); hs = man.get('holiday_season', 'HOLIDAY_SEASON=true' in ha)
            holre = re.compile(r'(?i)christmas|hanukk?ah|chanukah|menorah|dreidel|santa|holiday|xmas|noel|snow|winter|reindeer|nutcracker|merry|jingle|ornament|gingerbread|candy cane|poinsettia|sleigh|tinsel|festive')
            for k, o in DA['mats'].items():
                b = DB['mats'].get(k)
                if not o.get('ahid') or not b or b.get('hid') or b.get('bn') in byd: continue
                why = ('partner brand' if b.get('bn') in cov or b.get('bn') in na.get('partners', []) else 'allowed non-partner' if b.get('bn') in prot or k in pm
                       else 'holiday mat in the holiday season' if hs and (b.get('hol') or b.get('wfh') or b.get('ayr') or holre.search(b.get('n', ''))) else None)
                if why: F.append(f"[170b] artifact: {b.get('n')} ({b.get('bn')}) is slimmed (ahid) but is a {why}")
            I.append(f"artifact slimmed outside the by-design catalogs: {sum(1 for k, o in DA['mats'].items() if o.get('ahid') and DB['mats'].get(k, {}).get('bn') not in byd and not DB['mats'].get(k, {}).get('hid'))}")
        except Exception as e: F.append(f'[170] artifact copy check did not run: {e}')
    else: I.append(f'artifact folder not found ({A}); artifact copy not checked')
    return F, I
