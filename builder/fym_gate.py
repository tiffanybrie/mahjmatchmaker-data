"""FYM publish gate. Run before EVERY publish of the Find Your Match artifact:
    python3 builder/fym_gate.py <build_dir>
Exits non-zero and prints every failure. Checks (add one for each bug type Tiffany reports):
 1  album / swipe-book sets show their canonical album tile photo (D.tiles[..].src == locked src, file exists, pixels match)
 2  no visible set without an album / swipe book carries a "Tiffany's match" list (m)
 3  no visible set flagged no_tiles (builder/fym_flags/tile_photo_flags.json); no visible mat flagged no_mat (mat_photo_flags.json)
 4  UI wording: no crush / nope / pass / "Pick your crush" / hard-coded "save 10%"
 5  colour-dot click selector bug (.dots [data-fam])
 6  locked values (builder/fym_flags/locks.json) unchanged
 7  misc: every T.full file exists, no relative shop URLs, no prototype email box, every <script src> exists
"""
import sys, os, json, re
import numpy as np
from PIL import Image, ImageOps
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')) + '/'
sys.path.insert(0, REPO + 'builder')
from fym_apply_locks import diffs

B = sys.argv[1]
h = open(os.path.join(B, 'index.html')).read()
i = h.find('const D=') + 8
D, end = json.JSONDecoder().raw_decode(h, i)
UI = h[:i] + h[end:]
T, M = D['tiles'], D['mats']
locks = json.load(open(REPO + 'builder/fym_flags/locks.json'))
tflags = json.load(open(REPO + 'builder/fym_flags/tile_photo_flags.json'))
mflags = json.load(open(REPO + 'builder/fym_flags/mat_photo_flags.json'))
albums = json.load(open(REPO + 'work/albums.json'))
F = []
vis = lambda s: not (s.get('hid') or T.get(s['tile'], {}).get('hid'))

def flat(p):
    im = Image.open(p).convert('RGBA'); bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[3]); return bg
def sig(im): return np.asarray(ImageOps.fit(im, (48, 48)).convert('L'), dtype=float)

# 1. album photos
alb_names = {a['tile'].lower() for a in albums}
ALIAS = {'heritage 1.0': 'heritage', 'miss classic jade': 'jade', 'miss classic malachite': 'malachite', 'classic tortoise': 'tortoise'}
seen = set()
for s in D['sets']:
    has_album = bool(s.get('album')) or bool(s.get('sb')) or ALIAS.get(s['name'].lower(), s['name'].lower()) in alb_names and not s.get('cat')
    if not has_album or s['slug'] in seen: continue
    seen.add(s['slug'])
    t = T[s['tile']]; lk = locks['tiles'].get(s['tile'])
    if not lk: F.append(f"[1] {s['name']}: album set has no locked album photo in locks.json"); continue
    if t.get('src') != lk['src']: F.append(f"[1] {s['name']}: tile src {t.get('src')!r} != album photo {lk['src']!r}"); continue
    sp = REPO + lk['src']; fp = os.path.join(B, t['full'])
    if not os.path.exists(sp): F.append(f"[1] {s['name']}: album photo missing {lk['src']}"); continue
    if not os.path.exists(fp): F.append(f"[1] {s['name']}: FYM photo file missing {t['full']}"); continue
    a, o = flat(sp), flat(fp)
    d = float(np.abs(sig(a) - sig(o)).mean())
    if d > 3 or abs(a.size[0] / a.size[1] - o.size[0] / o.size[1]) > 0.03:
        F.append(f"[1] {s['name']}: FYM photo {t['full']} is not the album photo {lk['src']} (pixel diff {d:.1f})")

# 2. her lists only on album / swipe-book sets
for s in D['sets']:
    if vis(s) and s['m'] and not (s.get('album') or s.get('sb')):
        F.append(f"[2] {s['name']} ({s['maker']}): has a Tiffany's-match list ({len(s['m'])}) but no album / swipe book")
if "D.sets.forEach(s=>{if(!(s.album||s.sb))s.m=[];})" not in UI:
    F.append("[2] runtime guard (album||sb) missing from the app script")

# 3. photo flags
for s in D['sets']:
    f = tflags.get(s['slug'])
    if f and f.get('flag') == 'no_tiles' and vis(s):
        F.append(f"[3] {s['name']} ({s['maker']}): visible but tile photo flagged no_tiles ({f.get('note','')})")
for mid, f in mflags.items():
    m = M.get(mid)
    if m and f.get('flag') == 'no_mat' and not m.get('hid'):
        F.append(f"[3] mat {m['n']} ({m.get('bn')}): visible but photo flagged no_mat")

# 4. wording (UI text only; product names inside D, CSS and code comments are exempt)
TXT = re.sub(r'<style>.*?</style>', ' ', UI, flags=re.S); TXT = re.sub(r'/\*.*?\*/', ' ', TXT, flags=re.S)
for pat, why in ((r'(?<!Color )\b[Cc]rush\b', 'crush'), (r'\bCRUSH\b', 'CRUSH'), (r'(?i)\bnope\b', 'nope'), (r'Pick your crush', 'Pick your crush'),
                 (r'(?i)[>\'"`\s]pass[<\'"`\s,.!]|\bto pass\b|aria-label="Pass"', 'pass'), (r'(?i)save 10%', 'hard-coded 10%')):
    for m in re.finditer(pat, TXT):
        F.append(f"[4] UI text contains {why!r}: ...{TXT[max(0, m.start()-50):m.end()+30]!r}")
# 5. colour-dot selector
if ".dots [data-fam]" in UI: F.append("[5] colour-dot click selector '.dots [data-fam]' (dots live in .frow; filter can't switch)")

# 6. locks
for x in diffs(D, locks):
    F.append(f"[6] locked value changed: {x[0]} {x[1]} {x[2]} build={json.dumps(x[3], ensure_ascii=False)[:60]} locked={json.dumps(x[4], ensure_ascii=False)[:60]}")

# 7. misc
for k, t in T.items():
    if not os.path.exists(os.path.join(B, t['full'])): F.append(f"[7] tile photo file missing: {t['full']} ({t.get('n')})")
for kind in ('tiles', 'mats', 'racks'):
    for k, o in D[kind].items():
        if o.get('u', '').startswith('/'): F.append(f"[7] relative shop URL {kind} {k}: {o['u']}")
if 'class="mailbox"' in UI or 'function mail(' in UI: F.append("[7] prototype email box still present")
for src in re.findall(r'<script src="([^"]+)"', UI) + json.loads((re.search(r'window\.__LAZY=(\[[^\]]*\])', UI) or [None, '[]'])[1]):
    if not os.path.exists(os.path.join(B, src)): F.append(f"[7] script missing: {src}")

if F:
    print(f"FYM GATE: FAIL ({len(F)} problems)")
    for f in F: print('  ' + f)
    sys.exit(1)
print(f"FYM GATE: PASS  (album sets checked: {len(seen)}, sets: {len(D['sets'])}, visible: {sum(1 for s in D['sets'] if vis(s))}, locks: tiles {len(locks['tiles'])} sets {len(locks['sets'])} mats {len(locks['mats'])})")
