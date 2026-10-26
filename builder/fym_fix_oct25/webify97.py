"""Website copy of FYM v97 (Version 1.1): webify95 chain (v95 files @b80d857) + v97 files (mat chunks 184-185, t97/ tile
photos, hd/index.json without the old PLM HD racks) pinned to the v97 files commit (site-app/fym-v97/ on fym-site-preview).
Usage: python3 webify97.py <build_dir> <v97_files_commit> <out.html>"""
import sys, os, re, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
B, C97, OUT = sys.argv[1:4]
subprocess.run([sys.executable, HERE + '/webify95.py', B, 'b80d85708b2cbc54f9c6fead8a5d3fc5fb58fe93', OUT], check=True)
h = open(OUT).read(); CDN = 'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@'; b97 = CDN + C97 + '/site-app/fym-v97/'
b95 = CDN + 'b80d85708b2cbc54f9c6fead8a5d3fc5fb58fe93/site-app/fym-v95/'
h, n = re.subn(re.escape("fetch('" + b95 + "hd/index.json')"), "fetch('" + b97 + "hd/index.json')", h); assert n == 1, n
old = "fetch((c>=180&&c<=183?'"; assert h.count(old) == 1, h.count(old)
h = h.replace(old, "fetch((c>=184&&c<=185?'" + b97 + "':c>=180&&c<=183?'", 1)
h, nr = re.subn(r'(["\'])(t97/)', lambda m: m.group(1) + b97 + m.group(2), h); assert nr >= 3, nr
assert not re.search(r'["\']t97/', h)
open(OUT, 'w').write(h); print('ok v97', len(h), 't97 refs', nr)
