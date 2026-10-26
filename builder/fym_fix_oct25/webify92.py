"""Website copy of FYM v92: webify91 (v90 files @e54df6a, t91 @97c0f18) + t92 (Bam Bird split photos) + hd/index.json
re-pinned to the v92 files commit (Bespoke HD copies dropped) + any NEW mat chunks (Splash batch) pinned to the v92 files commit.
Usage: python3 webify92.py <build_dir> <v92_files_commit> <out.html> [new chunk numbers...]"""
import sys, os, re, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
B, C92, OUT = sys.argv[1:4]; NEW = [int(x) for x in sys.argv[4:]]
subprocess.run([sys.executable, HERE + '/webify91.py', B, '97c0f18bd9e6d81629e6cca649b84610853c0031', OUT], check=True)
h = open(OUT).read(); CDN = 'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@'; base = CDN + C92 + '/site-app/fym-v92/'
h = re.sub(r'(["\'])t92/', lambda m: m.group(1) + base + 't92/', h)
h, n = re.subn(r"fetch\('" + re.escape(CDN) + r"[0-9a-f]+/site-app/fym-v90/hd/index\.json'\)", "fetch('" + base + "hd/index.json')", h); assert n == 1
if NEW:
    old = "fetch((c===172?"; assert h.count(old) == 1
    h = h.replace(old, "fetch((" + '||'.join('c===%d' % c for c in NEW) + "?'" + base + "':c===172?", 1)
assert not re.search(r'["\']t9[012]/', h)
open(OUT, 'w').write(h); print('ok v92', len(h))
