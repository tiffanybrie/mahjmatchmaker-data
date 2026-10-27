"""Website copy of FYM v99 (Version 1.3): webify98 chain (v98 hd index @1714c0c) + v99 hd/index.json (adds r99 single-rack
cut-outs as absolute jsDelivr URLs, site-app/fym-v99/ on fym-site-preview).
Usage: python3 webify99.py <build_dir> <v99_hd_index_commit> <out.html>"""
import sys, os, re, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
B, C99, OUT = sys.argv[1:4]
subprocess.run([sys.executable, HERE + '/webify98.py', B, '1714c0cb1caf85f3b49023a44afdebbf356ac68c', OUT], check=True)
h = open(OUT).read(); CDN = 'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@'
b98 = CDN + '1714c0cb1caf85f3b49023a44afdebbf356ac68c/site-app/fym-v98/'; b99 = CDN + C99 + '/site-app/fym-v99/'
h, n = re.subn(re.escape("fetch('" + b98 + "hd/index.json')"), "fetch('" + b99 + "hd/index.json')", h); assert n == 1, n
open(OUT, 'w').write(h); print('ok v99', len(h))
