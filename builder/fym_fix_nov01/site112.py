"""v112 website copy (site-app/fym-v112 on fym-site-preview). Unlike site109 (data-only), v112 changes the app CODE too, so the
site index is made from the b112 build index itself plus the website-only transforms the v111 site copy carries:
 1. b23v1.js from its absolute fym-v82 CDN URL; b24v1.js is NOT loaded (its thumbnails live in thumbs.js)
 2. every window.IMG thumbnail (index inline + b24v1.js + the v109 thumbs.js) -> site-app/fym-v112/thumbs.js, loaded where the first
    block was (keeps the index < 15MB, jsDelivr 20MB/file)
 3. mat chunks: 190-212 from the CDN folders v111 used; NEW chunks 213-217 from fym-v112/mc/ at commit FC
 4. hd/index.json = the frozen fym-v100 one, plus the PLM Chartreuse A HD entries (inline data:) merged in
 5. relative tile/rack photo paths not in the v72 base tree -> absolute CDN URLs (earlier site copies; t112/ from fym-v112 at FC)
 6. sign-in 'unavailable' message: website wording (Main Nov 1): no 'Open Find Your Mat-ch on mahjmatchmaker.com'
Two phases: `assets` copies thumbs.js / mc/213-217 / t112 into the site folder (commit + push them, that commit = FC), then
`<FC>` writes the index.
Usage: python3 site112.py <b112 dir> <fym-site repo dir> assets|<FC sha>"""
import sys, json, re, subprocess, glob, os, shutil
B, SITE, FC = sys.argv[1:4]
CDN = 'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@'
OUTD = SITE + '/site-app/fym-v112'; os.makedirs(OUTD + '/mc', exist_ok=True); os.makedirs(OUTD + '/t112', exist_ok=True)
v111 = open(SITE + '/site-app/fym-v111/index.html').read(); bi = open(B + '/index.html').read()
def img_ids(s):
    out = {}
    for m in re.finditer(r'window\.IMG=Object\.assign\(window\.IMG\|\|\{\},', s):
        o, _ = json.JSONDecoder().raw_decode(s[m.end():]); out.update(o)
    return out
NEWC = [c for c in range(213, 230) if os.path.exists(f'{B}/mc/{c}.webp')]
if FC == 'assets':
    TH = img_ids(open(SITE + '/site-app/fym-v109/thumbs.js').read()); TH.update(img_ids(open(B + '/b24v1.js').read())); TH.update(img_ids(bi))
    open(OUTD + '/thumbs.js', 'w').write('window.IMG=Object.assign(window.IMG||{},' + json.dumps(TH, separators=(',', ':')) + ');')
    for c in NEWC: shutil.copy(f'{B}/mc/{c}.webp', f'{OUTD}/mc/{c}.webp')
    for p in glob.glob(B + '/t112/*'): shutil.copy(p, OUTD + '/t112/')
    print('site112 assets: thumbs', len(TH), 'thumbs.js', os.path.getsize(OUTD + '/thumbs.js'), 'chunks', NEWC); sys.exit()
h = bi
def rep(a, b):
    global h
    assert h.count(a) == 1, (h.count(a), a[:90]); h = h.replace(a, b)
# 1
b23 = re.search(r'<script src="https://cdn\.jsdelivr\.net/gh/tiffanybrie/mahjmatchmaker-data@[0-9a-f]+/site-app/fym-v82/b23v1\.js"></script>', v111).group(0)
rep('<script src="b23v1.js"></script><script src="b24v1.js"></script>', b23)
# 2
first = None
while True:
    m = re.search(r'<script>window\.IMG=Object\.assign\(window\.IMG\|\|\{\},', h)
    if not m: break
    o, e = json.JSONDecoder().raw_decode(h[m.end():]); end = h.index('</script>', m.end() + e) + len('</script>')
    if first is None: first = m.start()
    h = h[:m.start()] + h[end:]
if first is None: first = h.index(b23)  # b112 keeps no inline IMG blocks: load thumbs.js where b24v1.js was
h = h[:first] + f'<script src="{CDN}{FC}/site-app/fym-v112/thumbs.js"></script>' + h[first:]
# 3
mv = re.search(r"MCP\[c\]=\(MCB\.has\(c\)\?fetch\(\((c>=205.*?)'mc/'\+c\+'\.webp'\)", v111); assert mv, 'v111 chunk fetch not found'
rep("MCP[c]=(MCB.has(c)?fetch('mc/'+c+'.webp')", f"MCP[c]=(MCB.has(c)?fetch((c>={NEWC[0]}&&c<={NEWC[-1]}?'{CDN}{FC}/site-app/fym-v112/':" + mv.group(1) + "'mc/'+c+'.webp')")
# 4
HDX = {k: v for k, v in json.load(open(B + '/hd/index.json'))['r'].items() if v.startswith('file:data:')}
hdv = re.search(r"fetch\('(https://cdn\.jsdelivr\.net/gh/tiffanybrie/mahjmatchmaker-data@[0-9a-f]+/site-app/fym-v100/hd/index\.json)'\)", v111).group(1)
rep("HDI=fetch('hd/index.json').then(r=>r.ok?r.json():{})", f"HDI=fetch('{hdv}').then(r=>r.ok?r.json():{{}}).then(x=>{{x.r=Object.assign(x.r||{{}},{json.dumps(HDX, separators=(',', ':'))});return x;}})/*v112 PLM Chartreuse A HD*/")
# 5
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
            if p.startswith('t112/'): o[fld] = f'{CDN}{FC}/site-app/fym-v112/{p}'; nfix += 1
            elif p in AMAP: o[fld] = AMAP[p]; nfix += 1
            else: left.append(p)
assert not left, f'relative photo paths with no absolute URL: {left[:8]}'
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[i + e:]
# 6
rep("Sign-in isn’t available here right now. Open Find Your Mat-ch on <b>mahjmatchmaker.com</b> to sign in.", "Sign-in isn’t available right now. Please try again later.")
open(OUTD + '/index.html', 'w').write(h)
print('site112: index', len(h.encode()), 'paths fixed', nfix, 'new chunks', NEWC, 'hd extra', list(HDX))
