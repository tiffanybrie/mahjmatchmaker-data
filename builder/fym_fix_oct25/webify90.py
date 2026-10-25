"""Website copy of FYM v90 (site-app/fym-v90/index.html on the fym-site-preview branch). The page-block loads the index with
<base href> = site-app/fym-v72/ @ad0675e, so every file NEW since v72 must be pinned absolute:
  webify() (v82: b23 + t78 @3cac1c6, b24 inlined) + t87 @c9236fc + t88 @b22c191 + t89 @<v90 files commit>,
  mc chunks 172 @08edeb1 (v83), 173/174 @b22c191 (v88), 175 @<v90 files commit>, hd/index.json @<v90 files commit>
  (v89 dropped the neon HD copy of PLM Chartreuse).
Usage: python3 webify90.py <build_dir> <files_commit> <out.html>"""
import sys, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from webify import webify
B, FC, OUT = sys.argv[1:4]
CDN = 'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@'
PIN = {'t87': CDN + 'c9236fca7cc1bf3aa23bfd141bcedef06dbccbfe/site-app/fym-v87/', 't88': CDN + 'b22c1911a82bbc4b0d25650788d82bd1a5fe7dd6/site-app/fym-v88/',
       't89': CDN + FC + '/site-app/fym-v90/'}
h = webify(open(B + '/index.html').read(), B)
for d, base in PIN.items(): h = re.sub(r'(["\'])' + d + '/', lambda m: m.group(1) + base + d + '/', h)
old = "fetch('mc/'+c+'.webp')"
assert h.count(old) == 1
h = h.replace(old, "fetch((c===172?'" + CDN + "08edeb1e322afb654ed17e58e127eda2c4e6129e/site-app/fym-v83/':(c===173||c===174)?'" + CDN +
              "b22c1911a82bbc4b0d25650788d82bd1a5fe7dd6/site-app/fym-v88/':c===175?'" + CDN + FC + "/site-app/fym-v90/':'')+'mc/'+c+'.webp')")
old = "fetch('hd/index.json')"; assert h.count(old) == 1
h = h.replace(old, "fetch('" + CDN + FC + "/site-app/fym-v90/hd/index.json')")
assert not re.search(r'["\']t8[789]/', h)
open(OUT, 'w').write(h); print('ok', len(h))
