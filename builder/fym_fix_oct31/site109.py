"""v109 (Oct 31 eve) website copy: same as site108 (base = site fym-v108 index, b109 data, Version 1.9.4, new chunks from fym-v109)
PLUS every inline window.IMG thumbnail block moves OUT of the index into site-app/fym-v109/thumbs.js (absolute jsDelivr URL at the
chunks commit FC, loaded synchronously where the first block was) so the index stays well under jsDelivr's 20MB per-file limit.
Website copy of v108 (site-app/fym-v108/index.html on fym-site-preview) from the v107 site index + b108 data (same method as
fym_fix_oct30/site106.py): const D / BACKG / BLOGO from b108; every relative photo path not in the v72 base tree mapped to the absolute
jsDelivr URL an earlier site copy used; window.IMG thumbs b108 has but the site lacks go in inline; new mat chunks (MCB) fetch from the
fym-site-preview commit FC; Version 1.9.3. Fails if a relative t*/ path is left without an absolute URL.
Usage: python3 site108.py <site v107 index> <b108 dir> <out index> <chunks commit> <fym-site repo dir>"""
import sys, json, re, subprocess, glob, os
SI, B, OUT, FC, SITE = sys.argv[1:6]
CDN = 'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@'
h = open(SI).read(); bi = open(B + '/index.html').read()
h = h.replace('Version 1.9.3<', 'Version 1.9.4<').replace('(Version 1.9.3)', '(Version 1.9.4)'); assert h.count('Version 1.9.4') == 2
def swap(name):
    global h
    j = bi.index(name) + len(name); v, _ = json.JSONDecoder().raw_decode(bi[j:])
    k = h.index(name) + len(name); _, e = json.JSONDecoder().raw_decode(h[k:])
    h = h[:k] + json.dumps(v, ensure_ascii=False, separators=(',', ':') if name == 'const D=' else None) + h[k + e:]
swap('const BACKG='); swap('const BLOGO=')
j = bi.index('const D=') + 8; D, _ = json.JSONDecoder().raw_decode(bi[j:])
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
k = h.index('const D=') + 8; _, e = json.JSONDecoder().raw_decode(h[k:])
h = h[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[k + e:]
def img_ids(s):
    out = {}
    for m in re.finditer(r'window\.IMG=Object\.assign\(window\.IMG\|\|\{\},', s):
        o, _ = json.JSONDecoder().raw_decode(s[m.end():]); out.update(o)
    return out
have = img_ids(h); src = img_ids(bi); src.update(img_ids(open(B + '/b24v1.js').read()))
need = {k_: v for k_, v in src.items() if k_ not in have and (k_ in bi)}
if need:
    a = '<script>window.IMG=Object.assign(window.IMG||{},'
    h = h.replace(a, a + json.dumps(need, separators=(',', ':')) + ');</script>' + a, 1)
mb = re.search(r'MCB=new Set\(\[([0-9, ]+)\]\);', bi).group(1); ms = re.search(r'MCB=new Set\(\[([0-9, ]+)\]\);', h)
newc = sorted(set(int(x) for x in mb.split(',')) - set(int(x) for x in ms.group(1).split(',')))
h = h.replace(ms.group(0), 'MCB=new Set([' + mb + ']);', 1)
if newc:
    a = "fetch((c>=196&&c<=204?"; assert h.count(a) == 1
    h = h.replace(a, f"fetch((c>={newc[0]}&&c<={newc[-1]}?'{CDN}{FC}/site-app/fym-v109/':c>=196&&c<=204?", 1)
# thumbs out of the index (jsDelivr 20MB limit): all IMG blocks -> thumbs.js
TH = {}; first = None
while True:
    m = re.search(r'<script>window\.IMG=Object\.assign\(window\.IMG\|\|\{\},', h)
    if not m: break
    o, e = json.JSONDecoder().raw_decode(h[m.end():]); TH.update(o)
    end = h.index('</script>', m.end() + e) + len('</script>')
    if first is None: first = m.start()
    h = h[:m.start()] + h[end:]
open(SITE + '/site-app/fym-v109/thumbs.js', 'w').write('window.IMG=Object.assign(window.IMG||{},' + json.dumps(TH, separators=(',', ':')) + ');')
h = h[:first] + f'<script src="{CDN}{FC}/site-app/fym-v109/thumbs.js"></script>' + h[first:]
open(OUT, 'w').write(h)
print('site109: thumbs', len(TH), 'thumbs.js', os.path.getsize(SITE + '/site-app/fym-v109/thumbs.js'), 'paths fixed', nfix, 'thumbs added', len(need), 'new chunks', newc, 'size', len(h))
