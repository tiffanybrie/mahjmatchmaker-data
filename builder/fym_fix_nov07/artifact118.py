"""FYM 1.18 ARTIFACT copy (claude.ai artifact 6epA9HuEdT32zUp79Qv3kd), staged in a publish folder; it does NOT publish.
The artifact is at its caps (Nov 7: 512 of 512 files, 268,184,138 of 268,435,456 bytes = 251 KB free), so 1.18 is applied to the LIVE
artifact copy as a delta (same method as builder/fym_fix_nov06/artifact116_r2.py), not rebuilt:
 1. index = live artifact index.html + every D field the website copy changed from v117 to v118 (artifact-hidden 'ahid' mats keep their
    slim fields; their indexes are dropped from s.rank / s.cr again) + the same code patches (price118, zoomswipe_v118, release118);
 2. new mat photos (website chunks 251-257: ShopMy, Amazon holiday picks, partner sweep adds) are appended to the artifact's packed
    file mc/190.webp (chunks 190-250 already live there: 512-file cap); loadMC routes 190-<last> to it; their thumbs go inline;
 3. room: mat chunk files whose every photo belongs to a mat hidden in the artifact AND in 1.18 (and to no hidden mat on any
    Tiffany's-match list) are removed (files map null): they are never fetched.
Usage: python3 builder/fym_fix_nov07/artifact118.py <live artifact dir (index.html + mc/190.webp)> <site v117 index> <site v118 index>
         <b118 build dir> <out dir> <live listing sizes json {path: bytes}>"""
import sys, os, json, re, struct, subprocess
LIVE, S7, S8, B8, OUT, LST = sys.argv[1:7]
H = os.path.dirname(os.path.abspath(__file__))
CAP_TOTAL, CAP_FILES, CAP_INDEX, MARGIN = 256 * 2**20, 512, 16 * 10**6, 3 * 10**6
def LD(h):
    i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:]); return D, i, i + e
def pack_hdr(raw):
    n = struct.unpack('<I', raw[-4:])[0]; return json.loads(raw[-4 - n:-4])
a7, b8, F = open(S7).read(), open(S8).read(), open(LIVE + '/index.html').read()
DA, _, _ = LD(a7); DB, _, _ = LD(b8); DF, fi, fe = LD(F)
AH = {k for k, o in DF['mats'].items() if o.get('ahid')}
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
                    if top == 'tiles' and f == 'full': continue  # the artifact keeps its own relative tile photo paths
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
mcb = lambda x: [int(v) for v in re.search(r'MCB=new Set\(\[([0-9, ]+)\]\);', x).group(1).split(',')]
NEWC = sorted(set(mcb(b8)) - set(mcb(F)))
m = re.search(r'MCB=new Set\(\[([0-9, ]+)\]\);', h); h = h.replace(m.group(0), 'MCB=new Set([' + m.group(1) + ''.join(f', {c}' for c in NEWC) + ']);', 1)
r = re.search(r"c>=190&&c<=(\d+)\?190:c", h); assert r, 'artifact pack routing not found'
h = h.replace(r.group(0), f"c>=190&&c<={max(NEWC + [int(r.group(1))])}?190:c", 1)
# thumbs of the new mats (inline, like the r2 rack thumb)
def img_ids(s):
    out = {}
    for mm in re.finditer(r'window\.IMG=Object\.assign\(window\.IMG\|\|\{\},', s):
        o, _ = json.JSONDecoder().raw_decode(s[mm.end():]); out.update(o)
    return out
IMG8 = img_ids(open(B8 + '/index.html').read()); have = img_ids(F)
newth = {DF['mats'][k]['th']: IMG8[DF['mats'][k]['th']] for k in DF['mats'] if k not in DA['mats'] and DF['mats'][k].get('th') in IMG8 and DF['mats'][k]['th'] not in have}
tag = '<script src="b24v1.js">'; assert h.count(tag) == 1
h = h.replace(tag, '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(newth, separators=(',', ':')) + ');</script>' + tag)
os.makedirs(OUT + '/mc', exist_ok=True)
open(OUT + '/index.html', 'w').write(h)
for s_ in [x for x in ('price118.py', 'zoomswipe_v118.py', 'tableview_v118.py', 'doors_v118.py', 'release118.py') if subprocess.run(['git', '-C', H, 'ls-files', '--error-unmatch', x], capture_output=True).returncode == 0]:  # code patches (tableview/doors patch render() in place)
    subprocess.run([sys.executable, H + '/' + s_, OUT + '/index.html'], check=True, capture_output=True)
# tile ranking (FYM 1.18, tilerank_v118.py): the copy inherits D.tso/D.tsoB from the build's D; only its JS patch is applied here
if subprocess.run(['git', '-C', H, 'ls-files', '--error-unmatch', 'tilerank_v118.py'], capture_output=True).returncode == 0:
    sys.path.insert(0, H); import tilerank_v118 as _TR
    _p = OUT + '/index.html'; _h, _did = _TR.patch_js(open(_p).read()); open(_p, 'w').write(_h)
h = open(OUT + '/index.html').read()
# pack: live mc/190.webp + the new chunks' photos
raw = open(LIVE + '/mc/190.webp', 'rb').read(); hdr = pack_hdr(raw); body = raw[:-4 - struct.unpack('<I', raw[-4:])[0]]
hd2 = dict(hdr); added = 0
for c in NEWC:
    r_ = open(f'{B8}/mc/{c}.webp', 'rb').read(); hh = pack_hdr(r_)
    for f, (a_, l_) in hh.items():
        if f in hd2: continue
        hd2[f] = [len(body), l_]; body += r_[a_:a_ + l_]; added += 1
hj = json.dumps(hd2, separators=(',', ':')).encode(); open(OUT + '/mc/190.webp', 'wb').write(body + hj + struct.pack('<I', len(hj)))
# room: chunk files with no photo a visible (artifact or 1.18) mat or a Tiffany's-match mat uses
L = json.load(open(LST))
use = {}
for k, o in DF['mats'].items(): use.setdefault(o.get('f'), []).append(k)
inm = {x[0] for s in DF['sets'] for x in s.get('m', [])}
def needed(f): return any((not DF['mats'][k].get('hid')) or k in inm for k in use.get(f, []))
drop = []
for p in L:
    mm = re.fullmatch(r'mc/(\d+)\.(webp|json)', p)
    if not mm or int(mm.group(1)) >= 190: continue
    c = int(mm.group(1)); keys = [f'm/{c * 12 + j}.webp' for j in range(12)]
    if not any(needed(f) for f in keys): drop.append(p)
# still short of the 3 MB margin: re-pack (never re-encode) chunk files whose local build copy is byte-identical to the live one
# (same size), keeping only the photos a visible / Tiffany's-match mat uses (fym_artifact_fit.py note: rebuild the header)
repacked, saved = [], 0
cands = []
for p in L:
    mm = re.fullmatch(r'mc/(\d+)\.webp', p)
    if not mm or p in drop or int(mm.group(1)) >= 190: continue
    src = f'{B8}/{p}'
    if not os.path.exists(src) or os.path.getsize(src) != L[p]: continue
    raw_ = open(src, 'rb').read(); hh = pack_hdr(raw_)
    keep = {f: v for f, v in hh.items() if needed(f)}
    if len(keep) == len(hh) or not keep: continue
    cands.append((sum(l for f, (a, l) in hh.items() if f not in keep), p, raw_, keep))
NEED_FREE = CAP_TOTAL - MARGIN - (sum(L.values()) - L['index.html'] - L['mc/190.webp'] - sum(L[p] for p in drop) + len(h.encode()) + os.path.getsize(OUT + '/mc/190.webp'))
for sv, p, raw_, keep in sorted(cands, key=lambda x: -x[0]):
    if saved >= -NEED_FREE + 200000: break
    body_, hd_ = b'', {}
    for f, (a, l) in sorted(keep.items(), key=lambda kv: kv[1][0]): hd_[f] = [len(body_), l]; body_ += raw_[a:a + l]
    hj_ = json.dumps(hd_, separators=(',', ':')).encode(); open(OUT + '/' + p, 'wb').write(body_ + hj_ + struct.pack('<I', len(hj_)))
    saved += L[p] - os.path.getsize(OUT + '/' + p); repacked.append(p); L[p] = os.path.getsize(OUT + '/' + p)
files = {'mc/190.webp': 'mc/190.webp', **{p: p for p in repacked}, **{p: None for p in drop}}
json.dump(files, open(OUT + '/files.json', 'w'), indent=1)
idx = len(h.encode()); pk = os.path.getsize(OUT + '/mc/190.webp')
tot = sum(L.values()) - L['index.html'] - L['mc/190.webp'] - sum(L[p] for p in drop) + idx + pk
nf = len(L) - len(drop)
print(json.dumps({'repacked': repacked, 'repack_saved': saved, 'field_changes': n, 'new_chunks': NEWC, 'photos_added_to_pack': added, 'new_thumbs': len(newth), 'dropped_files': drop,
                  'dropped_bytes': sum(L[p] for p in drop), 'index_bytes': idx, 'pack_bytes': pk, 'total_bytes': tot, 'files': nf,
                  'free_bytes': CAP_TOTAL - tot, 'fits_with_3MB_margin': tot <= CAP_TOTAL - MARGIN and nf <= CAP_FILES and idx <= CAP_INDEX,
                  'fits': tot <= CAP_TOTAL and nf <= CAP_FILES and idx <= CAP_INDEX}, indent=1))
