"""v116 WEBSITE copy (site-app/fym-v116 on fym-site-preview). b116 differs from b115 outside D only in (checked Nov 6, token diff):
Version strings, BLORD + the tiles-door WM brand set (Mahjong Row out) and one inline window.IMG script (the Mahj Pit rack cut-out).
v116 adds NO new mat chunks and NO new tile photos, so the website copy needs no new asset files: start from the QA'd site v115 index,
 1. swap in the b116 D (tile 'full' = the site v115 value wherever the build path is unchanged from b115),
 2. BLOGO/BLORD + the WM set statement from b116, the rack IMG script before the thumbs115.js tag,
 3. Version 1.16 + TRK_URL (release116.py).
Usage: python3 site116.py <b115 dir> <b116 dir> <fym-site repo dir>"""
import sys, json, re, os, subprocess
B5, B6, SITE = sys.argv[1:4]
VER = sys.argv[4] if len(sys.argv) > 4 else '116'  # Nov 6: 1.16 r2 was relabelled 1.17 -> site116.py <b115> <b> <site> 117
H = os.path.dirname(os.path.abspath(__file__))
OUTD = SITE + f'/site-app/fym-v{VER}'; os.makedirs(OUTD, exist_ok=True)
s5 = open(SITE + '/site-app/fym-v115/index.html').read(); b5 = open(B5 + '/index.html').read(); b6 = open(B6 + '/index.html').read()
def LD(h):
    i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:]); return D, i, i + e
D5, _, _ = LD(b5); DS, si, se = LD(s5); D6, _, _ = LD(b6)
left = []
for k, t in D6['tiles'].items():
    p = t.get('full')
    if not isinstance(p, str) or p.startswith(('http', 'data:')): continue
    if k in DS['tiles'] and D5['tiles'].get(k, {}).get('full') == p: t['full'] = DS['tiles'][k]['full']
    else: left.append((k, p))
assert not left, ('tile photo paths with no website value', left[:5])
h = s5[:si] + json.dumps(D6, ensure_ascii=False, separators=(',', ':')) + s5[se:]
def rep(a, b):
    global h
    assert h.count(a) == 1, (h.count(a), a[:90]); h = h.replace(a, b)
pat = r'const BLOGO=\{.*?\};const BLORD=\[.*?\];'
rep(re.search(pat, h).group(0), re.search(pat, b6).group(0))
wm = r"const WM=new Set\(\[[^\]]*\]\)"
rep(re.search(wm, h).group(0), re.search(wm, b6).group(0))
img = re.search(r'<script>window\.IMG=Object\.assign\(window\.IMG\|\|\{\},\{"rk116mpwhitebeech":[^<]*</script>', b6).group(0)
t115 = re.search(r'<script src="https://cdn\.jsdelivr\.net/gh/tiffanybrie/mahjmatchmaker-data@[0-9a-f]+/site-app/fym-v115/thumbs115\.js"></script>', h).group(0)
rep(t115, t115 + img)
open(OUTD + '/index.html', 'w').write(h)
subprocess.run([sys.executable, H + f'/release{VER}.py', OUTD + '/index.html'], check=True)
print('site116: index', os.path.getsize(OUTD + '/index.html'))
