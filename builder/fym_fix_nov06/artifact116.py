"""v116 claude.ai ARTIFACT copy. Same shape as pub115 (builder/fym_fix_nov05/artifact115.py): the artifact sits at its 512-file limit and
near the 256 MiB per-version cap, so it keeps pub115's artifact-only hides (ahid, slim entries out of rank/cr) and its packed mc/190.webp.
v116 adds no mat photos and no tile photos, so: pub115 index + the b116 D with pub115's ahid entries re-applied (and their indexes out of
every rank / cr), tile 'full' = the pub115 value where the build path is unchanged, BLOGO/BLORD + WM set from b116, the rack IMG script
before b24v1.js, Version 1.16 + TRK_URL. mc/190.webp is pub115's file unchanged (hard link). Writes <out>/index.html, <out>/mc/190.webp,
<out>/files.json. Usage: python3 artifact116.py <b115 dir> <b116 dir> <pub115 dir> <out dir>"""
import sys, os, json, re, subprocess
B5, B6, P5, O = sys.argv[1:5]
VER = sys.argv[5] if len(sys.argv) > 5 else '116'  # release script: release<VER>.py (1.17 = 117)
os.makedirs(O + '/mc', exist_ok=True)
def LD(h):
    i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:]); return D, i, i + e
b5, b6, p5 = (open(x + '/index.html').read() for x in (B5, B6, P5))
D5, _, _ = LD(b5); DP, pi, pe = LD(p5); D6, _, _ = LD(b6); M6 = D6['mats']
assert D6['order'] == DP['order'], 'mat order changed: artifact115-style index remap needed'
AH = [k for k, o in DP['mats'].items() if o.get('ahid')]
for k in AH:
    o = dict(DP['mats'][k])
    for f in ('u', 'u0', 'dc', 'pa'):  # links follow the build (auto-apply / dead-link fixes), photo stays hidden here
        if f in M6.get(k, {}): o[f] = M6[k][f]
    M6[k] = o
DS = {D6['order'].index(k) for k in AH}
for s_ in D6['sets']:
    for fld in ('rank', 'cr'):
        if fld in s_: s_[fld] = [j for j in s_[fld] if j not in DS]
left = []
for k, t in D6['tiles'].items():
    p = t.get('full')
    if not isinstance(p, str) or p.startswith('data:'): continue
    if k in DP['tiles'] and D5['tiles'].get(k, {}).get('full') == p: t['full'] = DP['tiles'][k]['full']
    elif not p.startswith('http'): left.append((k, p))
assert not left, left[:5]
h = p5[:pi] + json.dumps(D6, ensure_ascii=False, separators=(',', ':')) + p5[pe:]
def rep(a, b):
    global h
    assert h.count(a) == 1, (h.count(a), a[:90]); h = h.replace(a, b)
pat = r'const BLOGO=\{.*?\};const BLORD=\[.*?\];'
rep(re.search(pat, h).group(0), re.search(pat, b6).group(0))
wm = r"const WM=new Set\(\[[^\]]*\]\)"
rep(re.search(wm, h).group(0), re.search(wm, b6).group(0))
img = re.search(r'<script>window\.IMG=Object\.assign\(window\.IMG\|\|\{\},\{"rk116mpwhitebeech":[^<]*</script>', b6).group(0)
tag = '<script src="b24v1.js">'; rep(tag, img + tag)
open(O + '/index.html', 'w').write(h)
dst = O + '/mc/190.webp'
if os.path.exists(dst): os.remove(dst)
os.link(P5 + '/mc/190.webp', dst)
json.dump({'mc/190.webp': os.path.basename(O) + '/mc/190.webp'}, open(O + '/files.json', 'w'), indent=1)
subprocess.run([sys.executable, os.path.dirname(os.path.abspath(__file__)) + f'/release{VER}.py', O + '/index.html'], check=True)
sz = os.path.getsize(O + '/index.html'); assert sz < 16 * 10**6 - 30000, sz
print('artifact116: ahid kept', len(AH), '| index', sz, 'delta vs pub115', sz - len(p5.encode()))
