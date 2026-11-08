"""v118 WEBSITE copy (site-app/fym-v118 on fym-site-preview), same pattern as builder/fym_fix_nov05/site115.py. A website copy differs
from its build only in tile 'full' paths (absolute CDN URLs), its chunk routing and where the thumbnails live. Start from the website
v117 index (= b117 + those differences, checked Nov 7: every D key equal except tiles.full) and
 1. swap in the b118 D (tile 'full' = the website v117 value wherever the build path is unchanged from b117),
 2. MCB gets the new mat chunks (ShopMy / Amazon / partner adds); loadMC routes them to fym-v118/mc/ at the assets commit FC,
 3. thumbnails b118 has and b117 lacks -> fym-v118/thumbs118.js (script tag right after the last thumbs*.js tag),
 4. BACKG / BLOGO+BLORD from b118, then the same code patches as the build: price118.py, zoomswipe_v118.py, release118.py.
Two phases: `assets` copies thumbs118.js + new chunks into the site folder (commit + push = FC), then `<FC>` writes the index.
Usage: python3 builder/fym_fix_nov07/site118.py <b117 dir> <b118 dir> <fym-site repo dir> assets|<FC sha>"""
import sys, json, re, os, shutil, subprocess
B7, B8, SITE, FC = sys.argv[1:5]
H = os.path.dirname(os.path.abspath(__file__))
CDN = 'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@'
OUTD = SITE + '/site-app/fym-v118'; os.makedirs(OUTD + '/mc', exist_ok=True)
s7 = open(SITE + '/site-app/fym-v117/index.html').read(); b7 = open(B7 + '/index.html').read(); b8 = open(B8 + '/index.html').read()
def LD(h):
    i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:]); return D, i, i + e
def img_ids(s):
    out = {}
    for m in re.finditer(r'window\.IMG=Object\.assign\(window\.IMG\|\|\{\},', s):
        o, _ = json.JSONDecoder().raw_decode(s[m.end():]); out.update(o)
    return out
MCB = lambda h: [int(v) for v in re.search(r'MCB=new Set\(\[([0-9, ]+)\]\);', h).group(1).split(',')]
NEWC = sorted(set(MCB(b8)) - set(MCB(b7)))
if FC == 'assets':
    T7 = img_ids(b7); T8 = img_ids(b8); NEW = {k: v for k, v in T8.items() if k not in T7}
    open(OUTD + '/thumbs118.js', 'w').write('window.IMG=Object.assign(window.IMG||{},' + json.dumps(NEW, separators=(',', ':')) + ');')
    for c in NEWC: shutil.copy(f'{B8}/mc/{c}.webp', f'{OUTD}/mc/{c}.webp')
    print('site118 assets: new thumbs', len(NEW), 'chunks', NEWC); sys.exit()
D7, _, _ = LD(b7); DS, si, se = LD(s7); D8, _, _ = LD(b8)
left = []
for k, t in D8['tiles'].items():
    p = t.get('full')
    if not isinstance(p, str) or p.startswith(('http', 'data:')): continue
    if k in DS['tiles'] and D7['tiles'].get(k, {}).get('full') == p: t['full'] = DS['tiles'][k]['full']
    elif any(o.get('full') == p for o in D7['tiles'].values()):
        t['full'] = next(DS['tiles'][k2]['full'] for k2, o in D7['tiles'].items() if o.get('full') == p)
    else: left.append((k, p))
assert not left, ('tile photo paths with no website value', left[:5])
h = s7[:si] + json.dumps(D8, ensure_ascii=False, separators=(',', ':')) + s7[se:]
def rep(a, b):
    global h
    assert h.count(a) == 1, (h.count(a), a[:90]); h = h.replace(a, b)
m = re.search(r'MCB=new Set\(\[([0-9, ]+)\]\);', h); rep(m.group(0), 'MCB=new Set([' + m.group(1) + ''.join(f', {c}' for c in NEWC) + ']);')
rep("MCP[c]=(MCB.has(c)?fetch((", "MCP[c]=(MCB.has(c)?fetch((" + '||'.join(f'c==={c}' for c in NEWC) + f"?'{CDN}{FC}/site-app/fym-v118/':")
pat = r'const BLOGO=\{.*?\};const BLORD=\[.*?\];'
rep(re.search(pat, h).group(0), re.search(pat, b8).group(0))
j8 = b8.index('const BACKG=') + 12; BG8, _ = json.JSONDecoder().raw_decode(b8[j8:])
j = h.index('const BACKG=') + 12; _, e = json.JSONDecoder().raw_decode(h[j:]); h = h[:j] + json.dumps(BG8, ensure_ascii=False) + h[j + e:]
tags = list(re.finditer(r'<script src="https://cdn\.jsdelivr\.net/gh/tiffanybrie/mahjmatchmaker-data@[0-9a-f]+/site-app/fym-v\d+/thumbs\d*\.js"></script>', h))
last = tags[-1].group(0); rep(last, last + f'<script src="{CDN}{FC}/site-app/fym-v118/thumbs118.js"></script>')
open(OUTD + '/index.html', 'w').write(h)
for s_ in ('price118.py', 'zoomswipe_v118.py', 'release118.py'):
    subprocess.run([sys.executable, H + '/' + s_, OUTD + '/index.html'], check=True)
print('site118: index', os.path.getsize(OUTD + '/index.html'), 'new chunks', NEWC)
