"""Website copy of FYM v95: webify94 chain (v92 files @a00edfa, v94 files @fc121b3) + v95 files (mc/180 Etsy, Bam Bird tortoise
scatters in t92/, hd/index.json with the rotated/resized racks' HD copies dropped) pinned to the v95 files commit.
Usage: python3 webify95.py <build_dir> <v95_files_commit> <out.html>"""
import sys, os, re, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
B, C95, OUT = sys.argv[1:4]
subprocess.run([sys.executable, HERE + '/webify94.py', B, 'fc121b3264f440ae7269ef77a0063988b1cfa0d2', OUT], check=True)
h = open(OUT).read(); CDN = 'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@'; b95 = CDN + C95 + '/site-app/fym-v95/'
b92 = CDN + 'a00edfafc87d1774693b849dba71d6369381c6af/site-app/fym-v92/'
for f in ('bam-bird-classic-tortoise-scatter.jpg', 'bam-bird-emw-tortoise-scatter.jpg'):
    h = h.replace(b92 + 't92/' + f, b95 + 't92/' + f)
h, n = re.subn(r"fetch\('" + re.escape(b92) + r"hd/index\.json'\)", "fetch('" + b95 + "hd/index.json')", h); assert n == 1, n
old = "fetch((c===179?'"; assert h.count(old) == 1
h = h.replace(old, "fetch((c===180?'" + b95 + "':c===179?'", 1)
assert 'fym-v95/t92/bam-bird-classic-tortoise-scatter.jpg' in h
open(OUT, 'w').write(h); print('ok v95', len(h))
