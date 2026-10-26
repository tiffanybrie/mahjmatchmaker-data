"""Website copy of FYM v91: webify90 (t87/t88/t89 + chunks 172-175 + hd index, files @e54df6a site-app/fym-v90) + t91 pinned.
Usage: python3 webify91.py <build_dir> <t91_commit> <out.html>"""
import sys, os, re, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
B, C91, OUT = sys.argv[1:4]
subprocess.run([sys.executable, HERE + '/webify90.py', B, 'e54df6a6fff2d3e2df48aee1a2f606993e0f38ca', OUT], check=True)
h = open(OUT).read(); base = 'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@' + C91 + '/site-app/fym-v91/'
h = re.sub(r'(["\'])t91/', lambda m: m.group(1) + base + 't91/', h)
assert not re.search(r'["\']t9[01]/', h)
open(OUT, 'w').write(h); print('ok v91')
