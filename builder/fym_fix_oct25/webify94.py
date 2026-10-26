"""Website copy of FYM v94: webify92 (v92 files @a00edfa, chunk 176) + t94/ t95/ photos + the 2 new t92 Bam Bird tortoise
splits + new mat chunk 179 (Fait a Main), all pinned to the v94 files commit (site-app/fym-v94/ on fym-site-preview).
Usage: python3 webify94.py <build_dir> <v94_files_commit> <out.html>"""
import sys, os, re, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
B, C94, OUT = sys.argv[1:4]; C92 = 'a00edfafc87d1774693b849dba71d6369381c6af'
r = subprocess.run([sys.executable, HERE + '/webify92.py', B, C92, OUT, '176'], check=True)
h = open(OUT).read(); CDN = 'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@'
b92 = CDN + C92 + '/site-app/fym-v92/'; b94 = CDN + C94 + '/site-app/fym-v94/'
h = re.sub(r'(["\'])(t9[45]/)', lambda m: m.group(1) + b94 + m.group(2), h)
for f in ('bam-bird-classic-tortoise-split.jpg', 'bam-bird-emw-tortoise-split.jpg'):
    h = h.replace(b92 + 't92/' + f, b94 + 't92/' + f)
old = "fetch((c===176?'" + b92; assert h.count(old) == 1, h.count(old)
h = h.replace(old, "fetch((c===179?'" + b94 + "':c===176?'" + b92, 1)
assert not re.search(r'["\']t9[0-5]/', h)
open(OUT, 'w').write(h); print('ok v94', len(h))
