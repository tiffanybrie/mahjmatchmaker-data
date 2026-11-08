"""FYM 1.18 artifact publish fix (Nov 8): the Artifact tool refuses a single file over its per-file limit (~15 MB binary), and the
1.18 artifact pack mc/190.webp grew to 20 MB (live 1.17 copy: 13.2 MB). Split the pack in two at a chunk boundary:
  mc/190.webp = chunks 190..SPLIT-1, mc/<SPLIT>.webp = chunks SPLIT..PACK_HI (same pack format: images + JSON header + 4-byte length).
Routing in index.html becomes  c>=190&&c<=SPLIT-1?190:c>=SPLIT&&c<=PACK_HI?SPLIT:c  ; manifest gets pack_hi = SPLIT-1 and
pack2 = [SPLIT, PACK_HI]; files.json gains mc/<SPLIT>.webp. picks_check.py (gate [170]) reads pack2. Lossless (bytes copied).
Usage: python3 builder/fym_fix_nov07/split_pack118.py <pub dir> [split chunk, default 241]"""
import sys, os, json, re, struct
P = sys.argv[1].rstrip('/'); SPLIT = int(sys.argv[2]) if len(sys.argv) > 2 else 241
LIMIT = 15 * 10**6
def hdr(raw):
    n = struct.unpack('<I', raw[-4:])[0]; return json.loads(raw[-4 - n:-4])
def write(path, items, raw):
    body, h = b'', {}
    for f, (a, l) in items: h[f] = [len(body), l]; body += raw[a:a + l]
    hj = json.dumps(h, separators=(',', ':')).encode(); out = body + hj + struct.pack('<I', len(hj))
    open(path, 'wb').write(out); return len(out), h
raw = open(f'{P}/mc/190.webp', 'rb').read(); H = hdr(raw)
ch = lambda f: int(f[2:-5]) // 12
idx = open(f'{P}/index.html').read()
r = re.search(r"c>=190&&c<=(\d+)\?190:c", idx); assert r and '?' + str(SPLIT) + ':c' not in idx, 'routing not found or already split'
HI = int(r.group(1)); assert 190 < SPLIT <= HI
items = sorted(H.items(), key=lambda kv: kv[1][0])
A = [(f, v) for f, v in items if ch(f) < SPLIT]; B = [(f, v) for f, v in items if ch(f) >= SPLIT]
assert len(A) + len(B) == len(H)
s1, h1 = write(f'{P}/mc/190.webp', A, raw); s2, h2 = write(f'{P}/mc/{SPLIT}.webp', B, raw)
assert s1 < LIMIT and s2 < LIMIT, (s1, s2)
idx = idx.replace(r.group(0), f"c>=190&&c<={SPLIT - 1}?190:c>={SPLIT}&&c<={HI}?{SPLIT}:c", 1)
open(f'{P}/index.html', 'w').write(idx)
fj = json.load(open(f'{P}/files.json')); fj[f'mc/{SPLIT}.webp'] = f'mc/{SPLIT}.webp'; json.dump(fj, open(f'{P}/files.json', 'w'), indent=1)
mp = P + '.manifest.json'; man = json.load(open(mp))
man['pack_hi'] = SPLIT - 1; man['pack2'] = [SPLIT, HI]
man['files']['mc/190.webp'] = sorted(h1, key=lambda f: int(f[2:-5])); man['files'][f'mc/{SPLIT}.webp'] = sorted(h2, key=lambda f: int(f[2:-5]))
json.dump(man, open(mp, 'w'))
print(json.dumps({'mc/190.webp': [s1, len(h1)], f'mc/{SPLIT}.webp': [s2, len(h2)], 'routing': f'190-{SPLIT - 1} -> 190, {SPLIT}-{HI} -> {SPLIT}'}))
