"""Artifact limit (index.html <= 16MB): move every inline <script>window.IMG=Object.assign(...)</script> block out of index.html
and append it to b24v1.js (written as a NEW file, breaking the hardlink). The blocks sit right after <script src="b24v1.js">,
so execution order is unchanged. Usage: python3 v105_imgout.py <build_dir>"""
import re, sys, os
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
pat = re.compile(r'<script>window\.IMG=Object\.assign\(window\.IMG\|\|\{\},\{.*?\}\);</script>', re.S)
a = '<script src="b24v1.js"></script>'; ia = h.index(a) + len(a)
blocks = [m for m in pat.finditer(h) if m.start() >= ia]
first_other = min([m.start() for m in re.finditer(r'<script', h[ia:])] + [10**12])
js = ''.join(m.group(0)[len('<script>'):-len('</script>')] + '\n' for m in blocks)
h2 = pat.sub(lambda m: '' if m.start() >= ia else m.group(0), h)
b24 = open(B + '/b24v1.js').read().rstrip()
os.remove(B + '/b24v1.js'); open(B + '/b24v1.js', 'w').write(b24 + ';\n' + js)
open(P, 'w').write(h2); print('moved', len(blocks), 'IMG blocks', len(js), 'bytes; index', len(h2.encode()))
