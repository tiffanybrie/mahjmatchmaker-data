"""v115 claude.ai ARTIFACT copy (preview 5QjNXjw15MuZTqzDT1ptbp for QA; the main chat publishes the live one after QA).
The artifact is at its 512-file limit, so it keeps the v113/v114 shape: pub114 = b114 with the 276 v113 adds hidden in the artifact only
(ahid, slim entries, out of rank/cr) and chunks 190-243 packed into ONE mc/190.webp. v115 = pub114 + the b115 D with those same
artifact-only hides re-applied, the v115 new chunks (244+) APPENDED into mc/190.webp at q66 (route 190..last -> 190), the 8 new tile photos
inlined as data URIs, their thumbnails inline. If the byte budget is exceeded, the lowest-ranked v115 year-round adds are hidden in THIS copy
only (as artifact113); the website copy has every add. Writes <out>/index.html, <out>/mc/190.webp, <out>/files.json, <out>/kept.json.
PUBLISHED Nov 5 (preview v28) with: A115_MUST="Mahj Pit" A115_TILEPX=480 A115_TILEQ=70 python3 artifact115.py <b114> <b115> <pub114> <out> 0
(the 256 MiB per-version cap: the 6 must-brands at ~2.6 MB were refused, Mahj Pit only at ~2.2 MB fits). Usage: python3 artifact115.py <b114 dir> <b115 dir> <pub114 dir> <out dir> [budget bytes added, default 600000]"""
import sys, os, json, re, struct, io, base64, mimetypes
from PIL import Image
B4, B5, P4, O = sys.argv[1:5]; BUDGET = int(sys.argv[5]) if len(sys.argv) > 5 else 600000
os.makedirs(O + '/mc', exist_ok=True)
def LD(h):
    i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:]); return D, i, i + e
def inl(s):
    out = {}
    for m in re.finditer(r'window\.IMG=Object\.assign\(window\.IMG\|\|\{\},', s):
        o, _ = json.JSONDecoder().raw_decode(s[m.end():]); out.update(o)
    return out
b4, b5, p4 = (open(x + '/index.html').read() for x in (B4, B5, P4))
D4, _, _ = LD(b4); DP, pi, pe = LD(p4); D5, _, _ = LD(b5); M5 = D5['mats']
assert D5['order'][:len(D4['order'])] == D4['order'] == DP['order']
# 1. artifact-only hides from pub114
AH = [k for k, o in DP['mats'].items() if o.get('ahid')]
for k in AH: M5[k] = DP['mats'][k]
for k, t in D5['tiles'].items():
    if k in DP['tiles'] and D4['tiles'].get(k, {}).get('full') == t.get('full'): t['full'] = DP['tiles'][k]['full']
# 2. v115 adds: images from the new chunks
MCB = lambda h: {int(v) for v in re.search(r'MCB=new Set\(\[([0-9, ]+)\]\);', h).group(1).split(',')}
NEWC = sorted(MCB(b5) - MCB(b4)); IMGS = {}
for c in NEWC:
    ab = open(f'{B5}/mc/{c}.webp', 'rb').read(); n = struct.unpack('<I', ab[-4:])[0]
    for f, (a, l) in json.loads(ab[-4 - n:-4]).items(): IMGS[f] = ab[a:a + l]
def q66(raw):
    im = Image.open(io.BytesIO(raw)); b = io.BytesIO(); im.save(b, 'WEBP', quality=66, method=6); return b.getvalue()
TH5 = inl(b5); TH4 = inl(p4)
adds = [k for k, m in M5.items() if m.get('add') in ('nov05-v115', 'nov03-etsy') and not m.get('hid')]
pos = {}
for s in D5['sets']:
    seen = []
    for j in (s.get('cr') or []) + s.get('rank', []):
        k = D5['order'][j] if j < len(D5['order']) else None
        if k in seen or k not in M5 or M5[k].get('hid') or M5[k].get('rt'): continue
        seen.append(k)
    for p_, k in enumerate(seen[:40]): pos[k] = pos.get(k, 0) + (40 - p_)
MUSTB = os.environ.get('A115_MUST', 'Mahj Pit,Oh My Mahjong,Splash of Color,Britt Mills,Noli June').split(',')
must = [k for k in adds if M5[k]['bn'] in MUSTB and (os.environ.get('A115_MUSTHOL', '1') == '1' or True)]
rest = sorted([k for k in adds if k not in must], key=lambda k: -pos.get(k, 0))
cost = lambda k: len(q66(IMGS[M5[k]['f']])) + len(TH5.get(M5[k].get('th'), '')) + 200
used, keep = 0, []
for k in must + rest:
    c_ = cost(k)
    if k in must or used + c_ <= BUDGET: keep.append(k); used += c_
drop = [k for k, m in M5.items() if m.get('add') in ('nov05-v115', 'nov03-etsy') and k not in keep]
for k in drop:
    o = M5[k]; M5[k] = {x: o[x] for x in ('n', 'bn', 'b', 'f', 'th', 'add', 'mf', 'mt', 'hol', 'u', 'pa') if x in o}; M5[k].update(hid=True, ahid=1, f='', th='')
DS = {D5['order'].index(k) for k in AH + drop}
for s_ in D5['sets']:
    for fld in ('rank', 'cr'):
        if fld in s_: s_[fld] = [j for j in s_[fld] if j not in DS]
# new tile photos inline
for t in D5['tiles'].values():
    p = t.get('full', '')
    if isinstance(p, str) and p.startswith('t115/'):
        im = Image.open(B5 + '/' + p).convert('RGB'); TS = int(os.environ.get('A115_TILEPX', '760')); im.thumbnail((TS, TS)); bb = io.BytesIO(); im.save(bb, 'JPEG', quality=int(os.environ.get('A115_TILEQ', '78')))  # byte budget
        t['full'] = 'data:image/jpeg;base64,' + base64.b64encode(bb.getvalue()).decode()
h = p4[:pi] + json.dumps(D5, ensure_ascii=False, separators=(',', ':')) + p4[pe:]
def rep(a, b):
    global h
    assert h.count(a) == 1, (h.count(a), a[:90]); h = h.replace(a, b)
m = re.search(r'MCB=new Set\(\[([0-9, ]+)\]\);', h); rep(m.group(0), 'MCB=new Set([' + m.group(1) + ''.join(f', {c}' for c in NEWC) + ']);')
rep("fetch('mc/'+(c>=190&&c<=243?190:c)+'.webp')", f"fetch('mc/'+(c>=190&&c<={NEWC[-1]}?190:c)+'.webp')")
bl5 = re.search(r'const BLOGO=\{.*?\};const BLORD=\[.*?\];', b5).group(0); blh = re.search(r'const BLOGO=\{.*?\};const BLORD=\[.*?\];', h).group(0)
h = h.replace(blh, bl5, 1)  # brand logos (Mahj Pit, v115)
j5 = b5.index('const BACKG=') + 12; BG5, _ = json.JSONDecoder().raw_decode(b5[j5:])
j = h.index('const BACKG=') + 12; _, e = json.JSONDecoder().raw_decode(h[j:]); h = h[:j] + json.dumps(BG5, ensure_ascii=False) + h[j + e:]
need = {k: v for k, v in TH5.items() if k not in TH4 and (k in h)}
tag = '<script src="b24v1.js">'; assert h.count(tag) == 1
h = h.replace(tag, '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(need, separators=(',', ':')) + ');</script>' + tag, 1)
# append the kept images to the published pack
ab = open(P4 + '/mc/190.webp', 'rb').read(); n = struct.unpack('<I', ab[-4:])[0]; hdr = json.loads(ab[-4 - n:-4]); body = ab[:-4 - n]
for f, raw in IMGS.items():
    if f in hdr or f'"{f}"' not in h: continue
    q = q66(raw); hdr[f] = [len(body), len(q)]; body += q
hj = json.dumps(hdr, separators=(',', ':')).encode()
open(O + '/mc/190.webp', 'wb').write(body + hj + struct.pack('<I', len(hj)))
open(O + '/index.html', 'w').write(h)
import subprocess
subprocess.run([sys.executable, os.path.dirname(os.path.abspath(__file__)) + '/release115.py', O + '/index.html'], check=True)
sz = os.path.getsize(O + '/index.html'); assert sz < 16 * 10**6 - 30000, sz
json.dump({'mc/190.webp': os.path.basename(O) + '/mc/190.webp'}, open(O + '/files.json', 'w'), indent=1)
json.dump({'kept': keep, 'dropped': drop}, open(O + '/kept.json', 'w'), indent=1)
print('artifact115: adds', len(adds), 'kept', len(keep), 'dropped here', len(drop), '| index', sz, 'delta', sz - len(p4.encode()),
      '| pack', os.path.getsize(O + '/mc/190.webp'), 'delta', os.path.getsize(O + '/mc/190.webp') - len(ab))
