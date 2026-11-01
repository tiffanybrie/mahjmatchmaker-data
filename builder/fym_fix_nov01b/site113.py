"""v113 website copy (site-app/fym-v113 on fym-site-preview), made from the b113 build index the same way as
fym_fix_nov01/site112.py, with:
 1. b23v1.js from its absolute fym-v82 CDN URL; b24v1.js NOT loaded
 2. thumbnails: v112's thumbs.js stays (absolute CDN URL at its commit); only thumbnails it lacks (the v113 adds) go into
    site-app/fym-v113/thumbs113.js (small file, no 16 MB re-upload)
 3. mat chunks: v112's CDN routing for <= 217 kept; NEW chunks (218+) from fym-v113/mc/ at commit FC
 4. hd/index.json = the frozen fym-v100 one (as v112)
 5. relative tile/rack photo paths not in the v72 base tree -> absolute CDN URLs from earlier site copies
 6. sign-in 'unavailable' message: website wording
Two phases: `assets` copies thumbs113.js + new chunks into the site folder (commit + push = FC), then `<FC>` writes the index.
Usage: python3 site113.py <b113 dir> <fym-site repo dir> assets|<FC sha>"""
import sys, json, re, subprocess, glob, os, shutil
B, SITE, FC = sys.argv[1:4]
CDN = 'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@'
OUTD = SITE + '/site-app/fym-v113'; os.makedirs(OUTD + '/mc', exist_ok=True)
v112 = open(SITE + '/site-app/fym-v112/index.html').read(); bi = open(B + '/index.html').read()
def img_ids(s):
    out = {}
    for m in re.finditer(r'window\.IMG=Object\.assign\(window\.IMG\|\|\{\},', s):
        o, _ = json.JSONDecoder().raw_decode(s[m.end():]); out.update(o)
    return out
NEWC = [c for c in range(218, 300) if os.path.exists(f'{B}/mc/{c}.webp')]
th112 = re.search(r'<script src="(https://cdn\.jsdelivr\.net/gh/tiffanybrie/mahjmatchmaker-data@[0-9a-f]+/site-app/fym-v112/thumbs\.js)"></script>', v112).group(1)
if FC == 'assets':
    OLD = img_ids(open(SITE + '/site-app/fym-v112/thumbs.js').read())
    TH = img_ids(open(B + '/b24v1.js').read()); TH.update(img_ids(bi))
    NEW = {k: v for k, v in TH.items() if k not in OLD}
    assert all(OLD[k] == v for k, v in TH.items() if k in OLD), 'a v112 thumbnail changed value'
    open(OUTD + '/thumbs113.js', 'w').write('window.IMG=Object.assign(window.IMG||{},' + json.dumps(NEW, separators=(',', ':')) + ');')
    for c in NEWC: shutil.copy(f'{B}/mc/{c}.webp', f'{OUTD}/mc/{c}.webp')
    print('site113 assets: new thumbs', len(NEW), 'thumbs113.js', os.path.getsize(OUTD + '/thumbs113.js'), 'chunks', NEWC); sys.exit()
h = bi
def rep(a, b):
    global h
    assert h.count(a) == 1, (h.count(a), a[:90]); h = h.replace(a, b)
b23 = re.search(r'<script src="https://cdn\.jsdelivr\.net/gh/tiffanybrie/mahjmatchmaker-data@[0-9a-f]+/site-app/fym-v82/b23v1\.js"></script>', v112).group(0)
rep('<script src="b23v1.js"></script><script src="b24v1.js"></script>', b23)
first = None
while True:
    m = re.search(r'<script>window\.IMG=Object\.assign\(window\.IMG\|\|\{\},', h)
    if not m: break
    o, e = json.JSONDecoder().raw_decode(h[m.end():]); end = h.index('</script>', m.end() + e) + len('</script>')
    if first is None: first = m.start()
    h = h[:m.start()] + h[end:]
if first is None: first = h.index(b23)
h = h[:first] + f'<script src="{th112}"></script><script src="{CDN}{FC}/site-app/fym-v113/thumbs113.js"></script>' + h[first:]
mv = re.search(r"MCP\[c\]=\(MCB\.has\(c\)\?fetch\(\((c>=213.*?)'mc/'\+c\+'\.webp'\)", v112); assert mv, 'v112 chunk fetch not found'
rep("MCP[c]=(MCB.has(c)?fetch('mc/'+c+'.webp')", f"MCP[c]=(MCB.has(c)?fetch((c>={NEWC[0]}&&c<={NEWC[-1]}?'{CDN}{FC}/site-app/fym-v113/':" + mv.group(1) + "'mc/'+c+'.webp')")
hdv = re.search(r"fetch\('(https://cdn\.jsdelivr\.net/gh/tiffanybrie/mahjmatchmaker-data@[0-9a-f]+/site-app/fym-v100/hd/index\.json)'\)", v112).group(1)
HDX = {k: v for k, v in json.load(open(B + '/hd/index.json'))['r'].items() if v.startswith('file:data:')}
assert not HDX, 'inline HD entries need the v112 merge code'
rep("HDI=fetch('hd/index.json').then(r=>r.ok?r.json():{})", f"HDI=fetch('{hdv}').then(r=>r.ok?r.json():{{}})")
i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:])
AMAP = {}
for f in sorted(glob.glob(SITE + '/site-app/fym-v*/index.html')):
    t = open(f).read()
    for m in re.finditer(r'https://cdn\.jsdelivr\.net/gh/tiffanybrie/mahjmatchmaker-data@[0-9a-f]{7,40}/site-app/fym-v\d+/((?:t\d+r?|r9\d\w*|m)/[^"\'\s]+?\.(?:jpg|jpeg|png|webp))', t):
        AMAP.setdefault(m.group(1), m.group(0))
base_tree = set(subprocess.run(['git', '-C', SITE, 'ls-tree', '-r', '--name-only', 'ad0675e42242c3abad40cac9f539a265220e26eb', 'site-app/fym-v72/'], capture_output=True, text=True, check=True).stdout.split())
nfix, left = 0, []
for kind in ('tiles', 'mats', 'racks'):
    for o in D[kind].values():
        for fld in ('full', 'f'):
            p = o.get(fld)
            if not isinstance(p, str) or p.startswith(('http', 'data:', 'blob:')) or not re.match(r't\d+r?/|r9\d', p): continue
            if ('site-app/fym-v72/' + p) in base_tree: continue
            if p in AMAP: o[fld] = AMAP[p]; nfix += 1
            else: left.append(p)
assert not left, f'relative photo paths with no absolute URL: {left[:8]}'
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[i + e:]
rep("Sign-in isn’t available here right now. Open Find Your Mat-ch on <b>mahjmatchmaker.com</b> to sign in.", "Sign-in isn’t available right now. Please try again later.")
open(OUTD + '/index.html', 'w').write(h)
print('site113: index', len(h.encode()), 'paths fixed', nfix, 'new chunks', NEWC)
