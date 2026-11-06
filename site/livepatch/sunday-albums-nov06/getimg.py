import json, subprocess, struct, re, os, io, sys
from PIL import Image
R = '/home/claude/mahjmatchmaker-data'
files = open('/dev/shm/sun/mcfiles.txt').read().split()
def ver(p): return int(re.search(r'fym-v(\d+)', p).group(1))
os.makedirs('/dev/shm/sun/newimg', exist_ok=True)
CACHE = {}
def chunk(c):
    cands = sorted([p for p in files if p.endswith(f'/mc/{c}.webp')], key=ver)
    if not cands: return None
    p = cands[-1]
    if p not in CACHE:
        CACHE[p] = subprocess.run(['git', '-C', R, 'show', 'origin/fym-site-preview:' + p], capture_output=True).stdout
    return CACHE[p]
def get(f, out):
    n = int(re.search(r'(\d+)', f).group(1)); ab = chunk(n // 12)
    if ab is None: return 'no chunk %d' % (n // 12)
    hl = struct.unpack('<I', ab[-4:])[0]; h = json.loads(ab[-4 - hl:-4].decode())
    k = next((x for x in (f, str(n), 'm/%d.webp' % n, '%d' % n) if x in h), None)
    if k is None: return 'key not in header; sample keys %s' % list(h)[:3]
    a, l = h[k]; Image.open(io.BytesIO(ab[a:a + l])).convert('RGB').save(out, quality=92); return 'ok'
if __name__ == '__main__':
    M = json.load(open('/dev/shm/sun/mats.json'))
    for key in sys.argv[1:]:
        slug = re.sub(r'[^a-z0-9]+', '-', key.lower()).strip('-')[-80:]
        print(key, get(M[key]['f'], f'/dev/shm/sun/newimg/{slug}.jpg'))
