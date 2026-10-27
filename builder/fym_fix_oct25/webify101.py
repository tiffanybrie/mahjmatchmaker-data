"""Website copy of FYM v101 (Version 1.5): v100 site chain (webify98 + v100 hd index @7251aac) + v101 files (mat chunks 186-187,
t101/ Spirit of Christmas tile photo) pinned to the v101 files commit (site-app/fym-v101/ on fym-site-preview).
Usage: python3 webify101.py <build_dir> <v101_files_commit> <out.html>"""
import sys, os, re, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
B, C, OUT = sys.argv[1:4]; CDN = 'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@'
subprocess.run([sys.executable, HERE + '/webify98.py', B, '1714c0cb1caf85f3b49023a44afdebbf356ac68c', OUT], check=True, capture_output=True)
h = open(OUT).read()
old = "fetch('" + CDN + "1714c0cb1caf85f3b49023a44afdebbf356ac68c/site-app/fym-v98/hd/index.json')"; assert h.count(old) == 1
h = h.replace(old, "fetch('" + CDN + "7251aac7d9e2e09db6b215bc7f6305827c59ad55/site-app/fym-v100/hd/index.json')")
b101 = CDN + C + '/site-app/fym-v101/'
old = "fetch((c>=184&&c<=185?'"; assert h.count(old) == 1, h.count(old)
h = h.replace(old, "fetch((c>=186&&c<=187?'" + b101 + "':c>=184&&c<=185?'", 1)
h, nr = re.subn(r'(["\'])(t101/)', lambda m: m.group(1) + b101 + m.group(2), h); assert nr >= 1, nr
assert not re.search(r'["\']t101/', h)
open(OUT, 'w').write(h); print('ok v101', len(h), 't101 refs', nr)
