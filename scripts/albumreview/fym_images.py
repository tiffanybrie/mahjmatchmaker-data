"""Full-size Find Your Mat-ch mat photos, read straight from git (no network).

The website copy of FYM (branch fym-site-preview, site-app/fym-vNN/index.html) loads mat photos ('f': 'm/1045.webp')
from packed chunk files mc/<c>.webp, c = number // MCN. Each chunk = webp blobs + a JSON index {f: [offset, len]} + a
4-byte little-endian index length at the end. Newer chunks live in the folders the page's loadMC() names (pinned
commits); older ones in site-app/fym-v72 | fym-oct21d | fym-v71 /mc/.

  from fym_images import image_bytes
  b = image_bytes(['m/1045.webp', ...])   # {f: webp bytes}
CLI: python3 scripts/albumreview/fym_images.py <outdir> m/1045.webp [...]"""
import json, re, struct, subprocess, sys, os
R = '/home/claude/mahjmatchmaker-data/'
BRANCH = 'origin/fym-site-preview'


def _git(spec):
    return subprocess.run(['git', '-C', R, 'show', spec], capture_output=True).stdout


def latest_index():
    names = subprocess.run(['git', '-C', R, 'ls-tree', '--name-only', BRANCH, 'site-app/'], capture_output=True, text=True).stdout.split()
    v = max((n for n in names if re.match(r'site-app/fym-v\d+$', n)), key=lambda n: int(n.split('-v')[1]))
    return v, _git(f'{BRANCH}:{v}/index.html').decode('utf8', 'replace')


def _rules(h):
    mcn = int(re.search(r'MCN=(\d+)', h).group(1))
    seg = h[h.index('MCP[c]=(MCB.has(c)?fetch('):][:12000]
    rules = []
    for m in re.finditer(r"\(?(c(?:===\d+(?:\|\|c===\d+)*|>=\d+&&c<=\d+))\)?\?'https://cdn\.jsdelivr\.net/gh/[^@]+@([0-9a-f]+)/([^']+)'", seg):
        nums = list(map(int, re.findall(r'\d+', m.group(1))))
        s = set(range(nums[0], nums[1] + 1)) if '>=' in m.group(1) else set(nums)
        rules.append((s, m.group(2), m.group(3)))
    return mcn, rules


def _unpack(b):
    n = struct.unpack('<I', b[-4:])[0]
    idx = json.loads(b[-4 - n:-4])
    return {f: b[a:a + l] for f, (a, l) in idx.items()}


def image_bytes(fs):
    v, h = latest_index()
    mcn, rules = _rules(h)
    want = {}
    for f in fs:
        want.setdefault(int(re.search(r'(\d+)', f).group(1)) // mcn, []).append(f)
    out = {}
    for c, group in want.items():
        cands = [f'{sha}:{p}mc/{c}.webp' for s, sha, p in rules if c in s]
        cands += [f'{BRANCH}:{v}/mc/{c}.webp'] + [f'{BRANCH}:site-app/{o}/mc/{c}.webp' for o in ('fym-v72', 'fym-oct21d', 'fym-v71')]
        for spec in cands:
            b = _git(spec)
            if not b: continue
            try: d = _unpack(b)
            except Exception: continue
            for f in group:
                if f in d and f not in out: out[f] = d[f]
            if all(f in out for f in group): break
    return out


if __name__ == '__main__':
    o = sys.argv[1]; os.makedirs(o, exist_ok=True)
    got = image_bytes(sys.argv[2:])
    for f, b in got.items(): open(os.path.join(o, f.replace('/', '_')), 'wb').write(b)
    print(len(got), 'of', len(sys.argv[2:]))
