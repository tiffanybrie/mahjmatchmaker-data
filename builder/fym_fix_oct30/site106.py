"""Website copy of v106 (site-app/fym-v106/index.html on fym-site-preview) from the v105 site index + b106.
 - code: the v106 replacements (racks/mats brand filter, Noli June note, Version 1.9.1) applied to the site index
 - data: const D, const BACKG and const BLOGO from b106
 - PHOTO PATHS: the website loads from the v72 base folder, so every tile photo added since needs its absolute jsDelivr
   URL. site105.py replaced D with the app's D and LOST those rewrites (live 1.9: every tile photo outside fym-v72 404'd,
   e.g. t104/amahj-round-top-stamped.jpg naturalWidth 0). Here every relative path in D is mapped back to the absolute URL
   any earlier site copy used for it (site-app/fym-v8x..v105), and new files (t106/) to the commit that holds them.
   Fails if any relative t*/ path is left that does not exist under the v72 base tree.
 - thumbs: window.IMG ids used by b106 but missing from the site index go in as one inline block
 - mat chunks 190+ : URL pinned to the fym-site-preview commit holding them
Usage: python3 site106.py <site v105 index> <b106 dir> <out index> <files commit> <fym-site repo dir>"""
import sys, json, re, os, subprocess, glob
SI, B, OUT, FC, SITE = sys.argv[1:6]
CDN = 'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@'
h = open(SI).read()
def rep(a, b, n=1):
    global h
    c = h.count(a); assert c == n, (c, a[:90]); h = h.replace(a, b)
rep("if(f.her){const U=uni();ids=ids.filter(r=>hr.includes(r)||U.includes(r));}",
    "if(f.her){const U=uni(),hu=r=>hr.includes(r)||U.includes(r);ids=f.brand?[...ids.filter(hu),...ids.filter(r=>!hu(r))]:ids.filter(hu);}/*v106: a picked brand shows ALL its racks, her picks first (Tiffany Oct 30 5:14pm)*/")
rep("if(f.her)ids=ids.filter(herMat);",
    "if(f.her&&f.brand){const hs=new Set(ids.filter(herMat));ids=[...hs,...MSL(colorPool()).filter(x=>!hs.has(x))];}else if(f.her)ids=ids.filter(herMat);/*v106: brand = all its mats, her picks first*/")
rep("function bnote(b){", "const BMIN={'Noli June':'10% off $100+'};/*v106: Noli June code has a $100 minimum*/\nfunction bnote(b){")
rep("return BCODE[b]?`<p class=\"bnote ok\"><span>✦ Save 10% or more at ${esc(b)} with code <b>MAHJMATCH</b></span></p>`",
    "return BCODE[b]?(BMIN[b]?`<p class=\"bnote ok\"><span>✦ ${BMIN[b]} at ${esc(b)} with code <b>MAHJMATCH</b></span></p>`:`<p class=\"bnote ok\"><span>✦ Save 10% or more at ${esc(b)} with code <b>MAHJMATCH</b></span></p>`)")
rep("o=b=>`<option value=\"${esc(b)}\"${cur===b?' selected':''}>${esc(b)} (${n[b]})</option>`",
    "o=b=>`<option value=\"${esc(b)}\"${cur===b?' selected':''}>${esc(b)} (${n[b]})${BMIN[b]?' \\u00b7 '+BMIN[b]:''}</option>`")
h = h.replace('Version 1.9<', 'Version 1.9.1<').replace('(Version 1.9)', '(Version 1.9.1)'); assert h.count('Version 1.9.1') == 2
bi = open(B + '/index.html').read()
def swap(name):
    global h
    j = bi.index(name) + len(name); v, _ = json.JSONDecoder().raw_decode(bi[j:])
    k = h.index(name) + len(name); _, e = json.JSONDecoder().raw_decode(h[k:])
    h = h[:k] + json.dumps(v, ensure_ascii=False, separators=(',', ':') if name == 'const D=' else None) + h[k + e:]
    return v
swap('const BACKG='); swap('const BLOGO=')
j = bi.index('const D=') + 8; D, _ = json.JSONDecoder().raw_decode(bi[j:])
# relative -> absolute photo URLs, from every earlier site copy
AMAP = {}
for f in sorted(glob.glob(SITE + '/site-app/fym-v*/index.html')):
    t = open(f).read()
    for m in re.finditer(r'https://cdn\.jsdelivr\.net/gh/tiffanybrie/mahjmatchmaker-data@[0-9a-f]{7,40}/site-app/fym-v\d+/((?:t\d+r?|r9\d\w*|m)/[^"\'\s]+?\.(?:jpg|jpeg|png|webp))', t):
        AMAP.setdefault(m.group(1), m.group(0))
base_tree = set(subprocess.run(['git', '-C', SITE, 'ls-tree', '-r', '--name-only', 'ad0675e42242c3abad40cac9f539a265220e26eb', 'site-app/fym-v72/'], capture_output=True, text=True, check=True).stdout.split())
in_base = lambda p: ('site-app/fym-v72/' + p) in base_tree
nfix, left = 0, []
for kind in ('tiles', 'mats', 'racks'):
    for o in D[kind].values():
        for fld in ('full', 'f'):
            p = o.get(fld)
            if not isinstance(p, str) or p.startswith(('http', 'data:', 'blob:')) or not re.match(r't\d+r?/|r9\d', p): continue
            if in_base(p): continue
            if p.startswith('t106/'): o[fld] = f'{CDN}{FC}/site-app/fym-v106/{p}'; nfix += 1
            elif p in AMAP: o[fld] = AMAP[p]; nfix += 1
            else: left.append(p)
assert not left, f'relative photo paths with no absolute URL: {left[:8]}'
k = h.index('const D=') + 8; _, e = json.JSONDecoder().raw_decode(h[k:])
h = h[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[k + e:]
# thumbs
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
# new mat chunks: MCB + URL mapping
mb = re.search(r'MCB=new Set\(\[([0-9, ]+)\]\);', bi).group(1); ms = re.search(r'MCB=new Set\(\[([0-9, ]+)\]\);', h)
newc = sorted(set(int(x) for x in mb.split(',')) - set(int(x) for x in ms.group(1).split(',')))
h = h.replace(ms.group(0), 'MCB=new Set([' + mb + ']);', 1)
if newc:
    a = "fetch((c===189?"
    assert h.count(a) == 1
    h = h.replace(a, f"fetch((c>={newc[0]}&&c<={newc[-1]}?'{CDN}{FC}/site-app/fym-v106/':c===189?", 1)
open(OUT, 'w').write(h)
print('site106: paths fixed', nfix, 'thumbs added', len(need), 'new chunks', newc, 'size', len(h))
