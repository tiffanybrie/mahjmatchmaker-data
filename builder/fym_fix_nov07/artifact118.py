"""FYM 1.18 ARTIFACT copy (claude.ai artifact 6epA9HuEdT32zUp79Qv3kd), staged in a publish folder; it does NOT publish.
The artifact is at its caps (Nov 7: 512 of 512 files, 268,184,138 of 268,435,456 bytes = 251 KB free), so 1.18 is applied to the LIVE
artifact copy as a delta (same method as builder/fym_fix_nov06/artifact116_r2.py), not rebuilt:
 1. index = live artifact index.html + every D field the website copy changed from v117 to v118 (artifact-hidden 'ahid' mats keep their
    slim fields; their indexes are dropped from s.rank / s.cr again) + the same code patches (price118, zoomswipe_v118, release118,
    tilerank JS, tiledeckprice118);
 2. new mat photos (website chunks 251+: ShopMy, Amazon holiday picks, partner sweep adds, QA fixes) are appended to the artifact's
    packed file mc/190.webp (chunks 190-250 already live there: 512-file cap); loadMC routes 190-<last> to it; their thumbs go inline;
 3. room: mat chunk files whose every photo belongs to a mat hidden in the artifact AND in 1.18 (and to no hidden mat on any
    Tiffany's-match list) are removed (files map null): they are never fetched.
 4. (QA Nov 8, F1: Juniper showed 34 of 42 here, 22 other sets lost picks) Tiffany's picks are NEVER slimmed: every mat in any set's
    m list that the website copy shows comes back in full (website entry, photo into the pack or its chunk file re-shipped, thumb
    inline). Room is freed by slimming ('ahid') the lowest-ranked NON-partner, non-pick mats whose photos sit in the pack (ShopMy-only
    / Amazon / other non-partner adds), worst best-rank first, only as many as the 3 MB margin needs. A live chunk file (< 190) that
    lacks a photo a visible or pick mat needs (earlier re-packs dropped them, e.g. 4 Soiree All Day picks in mc/171) is re-shipped from
    the build copy with every needed photo. Writes <out>.manifest.json (every final mc file -> the photo names it holds, from the
    live mirror / build copy / this run) for gate [170].
Usage: python3 builder/fym_fix_nov07/artifact118.py <live artifact dir (index.html + mc/190.webp)> <site v117 index> <site v118 index>
         <b118 build dir> <out dir> <live listing sizes json {path: bytes}> <live mirror dir (the live artifact's mc/* files)>"""
import sys, os, json, re, struct, subprocess, copy, shutil
LIVE, S7, S8, B8, OUT, LST = sys.argv[1:7]
MIRROR = sys.argv[7] if len(sys.argv) > 7 else None
H = os.path.dirname(os.path.abspath(__file__))
CAP_TOTAL, CAP_FILES, CAP_INDEX, MARGIN = 256 * 2**20, 512, 16 * 10**6, 3 * 10**6
FILES_MAX, SLACK = 510, 150_000   # coordinator Nov 8: <= 510 files; keep a little over the 3 MB margin
def LD(h):
    i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:]); return D, i, i + e
def pack_hdr(raw):
    n = struct.unpack('<I', raw[-4:])[0]; return json.loads(raw[-4 - n:-4])
def hdr_of(path): return pack_hdr(open(path, 'rb').read())
def tracked(x): return subprocess.run(['git', '-C', H, 'ls-files', '--error-unmatch', x], capture_output=True).returncode == 0
a7, b8, F = open(S7).read(), open(S8).read(), open(LIVE + '/index.html').read()
DA, _, _ = LD(a7); DB, _, _ = LD(b8); DF, fi, fe = LD(F)
AH = {k for k, o in DF['mats'].items() if o.get('ahid')}
# partner mats the artifact had slimmed out ('ahid') come back in full (Nov 7: OMM Lotus Cove was artifact-hidden with no photo while
# Tiffany wanted it in Table view tonight): website entry copied, photo added to the pack, thumb inlined. Nov 8: + every pick.
SLIM_BRANDS = {"Let's Be Besties", 'Luna EK Studio', 'Noli June', 'Betty June & Jeannette'}  # the bulk catalogs slimmed on purpose (size)
PICKS = {x[0] for s_ in DB['sets'] for x in s_.get('m', [])}  # Tiffany's real picks (every set's m): never slimmed (QA Nov 8, F1)
UNSLIM = {k for k in AH if k in DB['mats'] and not DB['mats'][k].get('hid')
          and ((DB['mats'][k].get('pa') and DB['mats'][k].get('bn') not in SLIM_BRANDS) or k in PICKS)}
for k in UNSLIM: DF['mats'][k] = dict(DB['mats'][k])
AH -= UNSLIM
LINK = {'u', 'u0', 'u_dead', 'u_plain', 'dc', 'pa', 'oos', 'alt', 'altu', 'hid', 'rt'}
n = 0
for top in DB:
    a, b = DA.get(top), DB[top]
    if a == b: continue
    if isinstance(b, dict) and isinstance(a, dict):
        for k in set(a) | set(b):
            if a.get(k) == b.get(k): continue
            if k not in b: DF[top].pop(k, None); n += 1; continue
            if k not in a or k not in DF[top]: DF[top][k] = b[k]; n += 1; continue
            if isinstance(a[k], dict) and isinstance(b[k], dict):
                for f in set(a[k]) | set(b[k]):
                    if a[k].get(f) == b[k].get(f): continue
                    if top == 'mats' and k in AH and f not in LINK: continue
                    if top == 'tiles' and f == 'full':  # the artifact keeps its own relative tile photo paths; new t118/ album photos ship as files
                        if '/site-app/fym-v118/t118/' in str(b[k][f]): DF[top][k][f] = 't118/' + b[k][f].split('/t118/')[1]; n += 1
                        continue
                    if f in b[k]: DF[top][k][f] = b[k][f]
                    else: DF[top][k].pop(f, None)
                    n += 1
            else: DF[top][k] = b[k]; n += 1
    elif top == 'sets':
        assert len(a) == len(b) == len(DF['sets'])
        for x, y, z in zip(a, b, DF['sets']):
            assert x.get('slug') == y.get('slug') == z.get('slug')
            for f in set(x) | set(y):
                if x.get(f) != y.get(f):
                    if f in y: z[f] = y[f]
                    else: z.pop(f, None)
                    n += 1
    else: DF[top] = b; n += 1
assert DF['order'] == DB['order']
DFM, AHM = DF, set(AH)
mcb = lambda x: [int(v) for v in re.search(r'MCB=new Set\(\[([0-9, ]+)\]\);', x).group(1).split(',')]
NEWC = sorted(set(mcb(b8)) - set(mcb(F)))
_r = re.search(r"c>=190&&c<=(\d+)\?190:c", F); assert _r, 'artifact pack routing not found'
PACK_HI = max(NEWC + [int(_r.group(1))])
chunk_of = lambda f: int(f[2:-5]) // 12 if isinstance(f, str) and re.fullmatch(r'm/\d+\.webp', f) else None
inpack = lambda f: chunk_of(f) is not None and 190 <= chunk_of(f) <= PACK_HI
LIVE_PACK = hdr_of(LIVE + '/mc/190.webp')
def photo_len(f):
    if f in LIVE_PACK: return LIVE_PACK[f][1]
    c = chunk_of(f); p = f'{B8}/mc/{c}.webp'
    if c is not None and os.path.exists(p): return hdr_of(p).get(f, [0, 0])[1]
    return 0
# slim candidates: visible here, not a pick, not a partner mat (no code), photo in the pack, not referenced anywhere else in D
_rest = json.dumps({k: v for k, v in DFM.items() if k not in ('mats', 'tv', 'order', 'tso', 'tsoB', 'sets')}, ensure_ascii=False) + json.dumps(
    [{k: v for k, v in s_.items() if k not in ('rank', 'cr')} for s_ in DFM['sets']], ensure_ascii=False)
_oi = {k: j for j, k in enumerate(DFM['order'])}
_best = {}
for s_ in DFM['sets']:
    if s_.get('hid'): continue
    for pos, j in enumerate(s_.get('rank', [])): _best[j] = min(_best.get(j, 1e9), pos)
CANDS = [k for k, o in DFM['mats'].items() if not o.get('hid') and k not in PICKS and not o.get('pa') and inpack(o.get('f'))
         and json.dumps(k, ensure_ascii=False) not in _rest]
CANDS.sort(key=lambda k: (-_best.get(_oi.get(k), 1e9), k))
def img_ids(s):
    out = {}
    for mm in re.finditer(r'window\.IMG=Object\.assign\(window\.IMG\|\|\{\},', s):
        o, _ = json.JSONDecoder().raw_decode(s[mm.end():]); out.update(o)
    return out
IMG8 = img_ids(open(B8 + '/index.html').read()); HAVE = img_ids(F)


def emit(SL):
    """Write the publish folder with the mats in SL slimmed ('ahid') on top of the merge; returns the summary."""
    if os.path.isdir(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT + '/mc', exist_ok=True)
    DF = copy.deepcopy(DFM); AH = AHM | set(SL)
    for k in SL:
        o = DF['mats'][k]; DF['mats'][k] = {x: o[x] for x in ('n', 'bn', 'b', 'add', 'mf', 'mt', 'hol', 'u', 'u0', 'pa', 'dc', 'rt') if x in o}
        DF['mats'][k].update(hid=True, ahid=1, f='', th='')
    # size (Nov 7, 1.18 at the artifact cap): every mat HIDDEN in this copy (incl. the artifact-only 'ahid' slim mats) leaves s.rank / s.cr
    # and its Table view entries (mo vendor photos, fa, cls, why, pm, cv, pf): hidden mats are never dealt, drawn or priced
    HID = {k for k, o in DF['mats'].items() if o.get('hid')}
    for _f in ('mo', 'fa', 'cls', 'why', 'pm', 'cv', 'pf'):
        if isinstance(DF.get('tv', {}).get(_f), dict):
            for k in [k for k in DF['tv'][_f] if k in HID]: DF['tv'][_f].pop(k)
    DS = {j for j, k in enumerate(DF['order']) if k in AH or k in HID}
    for s in DF['sets']:
        for fld in ('rank', 'cr'):
            if fld in s: s[fld] = [j for j in s[fld] if j not in DS]
    for g in ('mats', 'racks', 'tiles'):  # build-only link metadata (0 refs in app code), as the 1.16/1.17 artifact copies
        for o in DF[g].values():
            for f in ('u_plain', 'u_dead'): o.pop(f, None)
    h = F[:fi] + json.dumps(DF, ensure_ascii=False, separators=(',', ':')) + F[fe:]
    # chunk routing: new website chunks -> the artifact pack mc/190.webp
    m = re.search(r'MCB=new Set\(\[([0-9, ]+)\]\);', h); h = h.replace(m.group(0), 'MCB=new Set([' + m.group(1) + ''.join(f', {c}' for c in NEWC) + ']);', 1)
    r = re.search(r"c>=190&&c<=(\d+)\?190:c", h); h = h.replace(r.group(0), f"c>=190&&c<={PACK_HI}?190:c", 1)
    # thumbs of new / un-slimmed / re-photographed visible mats (inline, like the r2 rack thumb)
    newth = {}
    for k, o in DF['mats'].items():
        th = o.get('th')
        if o.get('hid') or not th or th in HAVE or th not in IMG8: continue
        if k not in DA['mats'] or k in UNSLIM or DA['mats'][k].get('th') != th: newth[th] = IMG8[th]
    tag = '<script src="b24v1.js">'; assert h.count(tag) == 1
    h = h.replace(tag, '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(newth, separators=(',', ':')) + ');</script>' + tag)
    open(OUT + '/index.html', 'w').write(h)
    for s_ in [x for x in ('price118.py', 'zoomswipe_v118.py', 'tableview_v118.py', 'doors_v118.py', 'release118.py') if tracked(x)]:  # code patches (tableview/doors patch render() in place)
        subprocess.run([sys.executable, H + '/' + s_, OUT + '/index.html'], check=True, capture_output=True)
    # tile ranking (FYM 1.18, tilerank_v118.py): the copy inherits D.tso/D.tsoB from the build's D; only its JS patch is applied here
    if tracked('tilerank_v118.py'):
        sys.path.insert(0, H); import tilerank_v118 as _TR
        _p = OUT + '/index.html'; _h, _did = _TR.patch_js(open(_p).read()); open(_p, 'w').write(_h)
    if tracked('tiledeckprice118.py'):  # QA Nov 8 F2, after price118 + the tilerank JS
        subprocess.run([sys.executable, H + '/tiledeckprice118.py', OUT + '/index.html'], check=True, capture_output=True)
    h = open(OUT + '/index.html').read()
    used = {}
    for k, o in DF['mats'].items(): used.setdefault(o.get('f'), []).append(k)
    inm = {x[0] for s in DF['sets'] for x in s.get('m', [])}
    def needed(f): return any((not DF['mats'][k].get('hid')) or k in inm for k in used.get(f, []))
    # pack: live mc/190.webp minus photos nothing needs any more + new chunks' photos + pack-range photos of un-slimmed mats
    raw = open(LIVE + '/mc/190.webp', 'rb').read(); body0 = raw[:-4 - struct.unpack('<I', raw[-4:])[0]]
    body, hd2, added, removed = b'', {}, 0, 0
    ownedM = {o.get('f') for o in DFM['mats'].values()}  # photos a mat owned before this run's slimming (orphans are kept as before)
    for f, (a_, l_) in sorted(LIVE_PACK.items(), key=lambda kv: kv[1][0]):
        if (f in used or f in ownedM) and not needed(f): removed += 1; continue
        hd2[f] = [len(body), l_]; body += body0[a_:a_ + l_]
    want = {o.get('f') for k, o in DF['mats'].items() if needed(o.get('f')) and inpack(o.get('f'))}
    for f in sorted(want - set(hd2), key=lambda f: int(f[2:-5])):
        src = f'{B8}/mc/{chunk_of(f)}.webp'
        if not os.path.exists(src): continue
        r_ = open(src, 'rb').read(); hh = pack_hdr(r_)
        if f in hh: a_, l_ = hh[f]; hd2[f] = [len(body), l_]; body += r_[a_:a_ + l_]; added += 1
    hj = json.dumps(hd2, separators=(',', ':')).encode(); open(OUT + '/mc/190.webp', 'wb').write(body + hj + struct.pack('<I', len(hj)))
    L = json.load(open(LST))
    files = {'mc/190.webp': 'mc/190.webp'}
    # room: chunk files with no photo a visible (artifact or 1.18) mat or a Tiffany's-match mat uses
    drop = []
    for p in L:
        mm = re.fullmatch(r'mc/(\d+)\.(webp|json)', p)
        if not mm or int(mm.group(1)) >= 190: continue
        c = int(mm.group(1)); keys = [f'm/{c * 12 + j}.webp' for j in range(12)]
        if not any(needed(f) for f in keys): drop.append(p)
    # what each final chunk file < 190 holds: this run's copy, else the live mirror, else a byte-identical build copy
    def known(p):
        if os.path.exists(f'{OUT}/{p}'): return set(hdr_of(f'{OUT}/{p}'))
        if MIRROR and os.path.exists(f'{MIRROR}/{p}') and os.path.getsize(f'{MIRROR}/{p}') == L.get(p): return set(hdr_of(f'{MIRROR}/{p}'))
        if os.path.exists(f'{B8}/{p}') and os.path.getsize(f'{B8}/{p}') == L.get(p): return set(hdr_of(f'{B8}/{p}'))
        return None
    # re-ship: a needed photo (visible / pick mat, chunk < 190) missing from its live chunk file
    reship, unknown = [], []
    needc = {}
    for f in used:
        c = chunk_of(f)
        if c is not None and c < 190 and needed(f): needc.setdefault(c, set()).add(f)
    for c, fs in sorted(needc.items()):
        p = f'mc/{c}.webp'
        if p not in L and f'mc/{c}.json' in L: continue  # json chunk (inline data URIs), shipped whole
        kn = known(p) if p in L else set()
        if kn is None: unknown.append(p); continue
        if fs <= kn: continue
        src = f'{B8}/{p}'
        if not os.path.exists(src): print('WARNING: no build copy to re-ship', p, sorted(fs - kn)[:3]); continue
        r_ = open(src, 'rb').read(); hh = pack_hdr(r_); keep_ = {f: hh[f] for f in sorted(fs | (kn & set(hh))) if f in hh}
        body_, hd_ = b'', {}
        for f, (a, l) in sorted(keep_.items(), key=lambda kv: kv[1][0]): hd_[f] = [len(body_), l]; body_ += r_[a:a + l]
        hj_ = json.dumps(hd_, separators=(',', ':')).encode(); open(f'{OUT}/{p}', 'wb').write(body_ + hj_ + struct.pack('<I', len(hj_)))
        reship.append(p); files[p] = p; L[p] = os.path.getsize(f'{OUT}/{p}')
    # still short of the margin: re-pack (never re-encode) chunk files whose local build copy is byte-identical to the live one
    # (same size), keeping only the photos a visible / Tiffany's-match mat uses (fym_artifact_fit.py note: rebuild the header)
    T118F = {}
    for o in DF['tiles'].values():
        if str(o.get('full', '')).startswith('t118/'):
            os.makedirs(OUT + '/t118', exist_ok=True); shutil.copy(f"{B8}/{o['full']}", f"{OUT}/{o['full']}"); T118F[o['full']] = o['full']
    def total():
        return (sum(v for p, v in L.items() if p not in drop and p not in ('index.html', 'mc/190.webp')) + len(h.encode())
                + os.path.getsize(OUT + '/mc/190.webp') + sum(os.path.getsize(f'{OUT}/{p}') for p in T118F))
    repacked, saved, cands = [], 0, []
    for p in L:
        mm = re.fullmatch(r'mc/(\d+)\.webp', p)
        if not mm or p in drop or p in reship or int(mm.group(1)) >= 190: continue
        src = f'{B8}/{p}'
        if not os.path.exists(src) or os.path.getsize(src) != L[p]: continue
        raw_ = open(src, 'rb').read(); hh = pack_hdr(raw_)
        keep = {f: v for f, v in hh.items() if needed(f)}
        if len(keep) == len(hh) or not keep: continue
        cands.append((sum(l for f, (a, l) in hh.items() if f not in keep), p, raw_, keep))
    for sv, p, raw_, keep in sorted(cands, key=lambda x: -x[0]):
        if total() <= CAP_TOTAL - MARGIN - SLACK: break
        body_, hd_ = b'', {}
        for f, (a, l) in sorted(keep.items(), key=lambda kv: kv[1][0]): hd_[f] = [len(body_), l]; body_ += raw_[a:a + l]
        hj_ = json.dumps(hd_, separators=(',', ':')).encode(); open(OUT + '/' + p, 'wb').write(body_ + hj_ + struct.pack('<I', len(hj_)))
        saved += L[p] - os.path.getsize(OUT + '/' + p); repacked.append(p); files[p] = p; L[p] = os.path.getsize(OUT + '/' + p)
    files.update(T118F); files.update({p: None for p in drop})
    json.dump(files, open(OUT + '/files.json', 'w'), indent=1)
    # manifest for gate [170]: every final mc file -> photo names (None = not verifiable here)
    man = {'pack_hi': PACK_HI, 'files': {}}
    for p in sorted(L):
        if not p.startswith('mc/') or p in drop: continue
        if p == 'mc/190.webp': man['files'][p] = sorted(hd2); continue
        if p.endswith('.json'): man['files'][p] = None; continue
        kn = known(p); man['files'][p] = sorted(kn) if kn is not None else None
    json.dump(man, open(OUT.rstrip('/') + '.manifest.json', 'w'))
    idx = len(h.encode()); tot = total()
    nf = len([p for p in L if p not in drop]) + len(T118F)
    return {'slimmed_now': len(SL), 'slimmed_bytes': sum(photo_len(DFM['mats'][k]['f']) for k in SL), 'unslimmed': len(UNSLIM),
            'unslimmed_picks': sorted(k for k in UNSLIM if k in PICKS), 'reshipped': reship, 'unverifiable_chunks': unknown,
            'repacked': repacked, 'repack_saved': saved, 'new_chunks': NEWC, 'pack_photos_added': added, 'pack_photos_removed': removed,
            'new_thumbs': len(newth), 'dropped_files': drop, 'index_bytes': idx, 'pack_bytes': os.path.getsize(OUT + '/mc/190.webp'),
            'total_bytes': tot, 'files': nf, 'free_bytes': CAP_TOTAL - tot,
            'fits_with_3MB_margin': tot <= CAP_TOTAL - MARGIN and nf <= FILES_MAX and idx <= CAP_INDEX,
            'fits': tot <= CAP_TOTAL and nf <= CAP_FILES and idx <= CAP_INDEX}


SL = []
for it in range(8):
    st = emit(SL)
    over = st['total_bytes'] - (CAP_TOTAL - MARGIN - SLACK)
    if over <= 0 and st['files'] <= FILES_MAX: break
    need, add = max(over, 0) + 100_000, []
    for k in CANDS:
        if k in SL: continue
        add.append(k); need -= photo_len(DFM['mats'][k]['f'])
        if need <= 0: break
    if not add: break
    SL += add
st['slimmed_mats'] = [f"{DFM['mats'][k]['bn']} | {DFM['mats'][k]['n']}" for k in SL]
print(json.dumps(st, indent=1, ensure_ascii=False))
