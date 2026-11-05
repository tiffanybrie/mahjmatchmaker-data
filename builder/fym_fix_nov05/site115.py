"""v115 WEBSITE copy (site-app/fym-v115 on fym-site-preview). The site copy of a build differs from the build index ONLY in tile 'full'
paths (absolute CDN URLs) + its own script/chunk routing (checked Nov 5: b114 D vs site v114 D). So: start from the QA'd site v114 index and
 1. swap in the b115 D (tile 'full': the site v114 value where the build path is unchanged; new t115/ photos -> fym-v115 at commit FC),
 2. MCB gets the new chunks; loadMC routes them to fym-v115/mc/ at FC,
 3. BACKG = the b115 one, thumbnails the v112/v113 thumb files lack -> fym-v115/thumbs115.js (script tag after thumbs113.js),
 4. Version 1.15 + TRK_URL (release115.py).
Two phases: `assets` copies thumbs115.js + new chunks + t115 photos into the site folder (commit + push = FC), then `<FC>` writes the index.
Usage: python3 site115.py <b114 dir> <b115 dir> <fym-site repo dir> assets|<FC sha>"""
import sys, json, re, os, shutil, subprocess
B4, B5, SITE, FC = sys.argv[1:5]
H = os.path.dirname(os.path.abspath(__file__))
CDN = 'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@'
OUTD = SITE + '/site-app/fym-v115'; os.makedirs(OUTD + '/mc', exist_ok=True); os.makedirs(OUTD + '/t115', exist_ok=True)
s4 = open(SITE + '/site-app/fym-v114/index.html').read(); b4 = open(B4 + '/index.html').read(); b5 = open(B5 + '/index.html').read()
def LD(h):
    i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:]); return D, i, i + e
def img_ids(s):
    out = {}
    for m in re.finditer(r'window\.IMG=Object\.assign\(window\.IMG\|\|\{\},', s):
        o, _ = json.JSONDecoder().raw_decode(s[m.end():]); out.update(o)
    return out
MCB = lambda h: {int(v) for v in re.search(r'MCB=new Set\(\[([0-9, ]+)\]\);', h).group(1).split(',')}
NEWC = sorted(MCB(b5) - MCB(b4))
if FC == 'assets':
    OLD = img_ids(open(SITE + '/site-app/fym-v112/thumbs.js').read()); OLD.update(img_ids(open(SITE + '/site-app/fym-v113/thumbs113.js').read()))
    TH = img_ids(b5); NEW = {k: v for k, v in TH.items() if k not in OLD}
    open(OUTD + '/thumbs115.js', 'w').write('window.IMG=Object.assign(window.IMG||{},' + json.dumps(NEW, separators=(',', ':')) + ');')
    for c in NEWC: shutil.copy(f'{B5}/mc/{c}.webp', f'{OUTD}/mc/{c}.webp')
    for f in os.listdir(B5 + '/t115'): shutil.copy(f'{B5}/t115/{f}', f'{OUTD}/t115/{f}')
    print('site115 assets: new thumbs', len(NEW), 'chunks', NEWC, 't115', len(os.listdir(OUTD + '/t115'))); sys.exit()
D4, _, _ = LD(b4); DS, si, se = LD(s4); D5, _, _ = LD(b5)
nfix = 0
for k, t in D5['tiles'].items():
    p = t.get('full')
    if not isinstance(p, str) or p.startswith(('http', 'data:')): continue
    if p.startswith('t115/'): t['full'] = f'{CDN}{FC}/site-app/fym-v115/{p}'; nfix += 1
    elif k in DS['tiles'] and D4['tiles'].get(k, {}).get('full') == p: t['full'] = DS['tiles'][k]['full']
    elif any(o.get('full') == p for o in D4['tiles'].values()):
        t['full'] = next(DS['tiles'][k2]['full'] for k2, o in D4['tiles'].items() if o.get('full') == p)
h = s4[:si] + json.dumps(D5, ensure_ascii=False, separators=(',', ':')) + s4[se:]
def rep(a, b):
    global h
    assert h.count(a) == 1, (h.count(a), a[:90]); h = h.replace(a, b)
m = re.search(r'MCB=new Set\(\[([0-9, ]+)\]\);', h); rep(m.group(0), 'MCB=new Set([' + m.group(1) + ''.join(f', {c}' for c in NEWC) + ']);')
rep("MCP[c]=(MCB.has(c)?fetch((", f"MCP[c]=(MCB.has(c)?fetch((c>={NEWC[0]}&&c<={NEWC[-1]}?'{CDN}{FC}/site-app/fym-v115/':")
bl5 = re.search(r'const BLOGO=\{.*?\};const BLORD=\[.*?\];', b5).group(0); blh = re.search(r'const BLOGO=\{.*?\};const BLORD=\[.*?\];', h).group(0)
h = h.replace(blh, bl5, 1)  # brand logos (Mahj Pit, v115)
j5 = b5.index('const BACKG=') + 12; BG5, _ = json.JSONDecoder().raw_decode(b5[j5:])
j = h.index('const BACKG=') + 12; _, e = json.JSONDecoder().raw_decode(h[j:]); h = h[:j] + json.dumps(BG5, ensure_ascii=False) + h[j + e:]
t113 = re.search(r'<script src="https://cdn\.jsdelivr\.net/gh/tiffanybrie/mahjmatchmaker-data@[0-9a-f]+/site-app/fym-v113/thumbs113\.js"></script>', h).group(0)
rep(t113, t113 + f'<script src="{CDN}{FC}/site-app/fym-v115/thumbs115.js"></script>')
open(OUTD + '/index.html', 'w').write(h)
subprocess.run([sys.executable, H + '/release115.py', OUTD + '/index.html'], check=True)
left = [t['full'] for t in D5['tiles'].values() if isinstance(t.get('full'), str) and not t['full'].startswith(('http', 'data:'))
        and t['full'] not in {o.get('full') for o in DS['tiles'].values()}]
print('site115: index', os.path.getsize(OUTD + '/index.html'), 'new t115 paths', nfix, 'new chunks', NEWC, 'unmapped relative paths', left[:5])
