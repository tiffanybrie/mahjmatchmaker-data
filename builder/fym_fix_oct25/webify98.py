"""Website copy of FYM v98 (Version 1.2): webify97 chain (v97 files @2260733) + v98 hd/index.json (single-rack HD files in r98/,
rewritten to absolute jsDelivr URLs in the site copy) pinned to the v98 files commit (site-app/fym-v98/ on fym-site-preview).
Usage: python3 webify98.py <build_dir> <v98_files_commit> <out.html>"""
import sys, os, re, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
B, C98, OUT = sys.argv[1:4]
subprocess.run([sys.executable, HERE + '/webify97.py', B, '2260733c178e1035e0e7813485b32b31f6e4b09d', OUT], check=True)
h = open(OUT).read(); CDN = 'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@'
b97 = CDN + '2260733c178e1035e0e7813485b32b31f6e4b09d/site-app/fym-v97/'; b98 = CDN + C98 + '/site-app/fym-v98/'
h, n = re.subn(re.escape("fetch('" + b97 + "hd/index.json')"), "fetch('" + b98 + "hd/index.json')", h); assert n == 1, n
open(OUT, 'w').write(h); print('ok v98', len(h))
