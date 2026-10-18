"""Collect every repo path referenced via jsDelivr by live pages + pending blocks.
Usage: python3 collect_inuse.py OUT.json DIR [DIR...]
DIRs contain .html (saved live pages, livepatch blocks, builds). Nested .html/.js/.json/.css
referenced files are expanded locally from git at their pinned commit."""
import re, sys, glob, json, subprocess, os
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RX = re.compile(r"https://cdn\.jsdelivr\.net/gh/tiffanybrie/mahjmatchmaker-data@([0-9a-f]+)/([^\"'\s)<>\\,?#]+)")
out, dirs = sys.argv[1], sys.argv[2:]
refs = {}  # path -> set(commits)
queue = []
for d in dirs:
    for f in glob.glob(d + '/**/*', recursive=True):
        if os.path.isfile(f) and re.search(r'\.(html|js|json|css|csv|md)$', f):
            queue += RX.findall(open(f, errors='ignore').read())
seen = set()
def show(c, p):
    try: return subprocess.run(['git','-C',REPO,'show',f'{c}:{p}'],capture_output=True,timeout=60).stdout
    except Exception: return b''
while queue:
    c, p = queue.pop()
    if (c, p) in seen: continue
    seen.add((c, p)); refs.setdefault(p, set()).add(c)
    if re.search(r'\.(html|js|json|css)$', p):
        queue += RX.findall(show(c, p).decode('utf-8','ignore'))
def order(c):
    r = subprocess.run(['git','-C',REPO,'log','-1','--format=%ct',c],capture_output=True,text=True).stdout.strip()
    return int(r or 0)
cache = {}
res = {}
for p, cs in refs.items():
    for c in cs:
        if c not in cache: cache[c] = order(c)
    res[p] = max(cs, key=lambda c: cache[c])
json.dump(res, open(out,'w'), indent=0, sort_keys=True)
print(len(res), 'paths from', len(seen), 'refs')
