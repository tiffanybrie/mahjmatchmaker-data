#!/usr/bin/env python3
"""Dead space check (Tiffany Nov 23 11:27pm, yellow-marked an empty band: "Yellow is wasted space, USE IT!!!"; also 10:5xpm "you have
way more room than that at the top"). For 9:16 pieces: inside the usable band (top 180 / bottom 150 of 1920, brand guide), any run
of near-blank rows (one flat colour across the content width) taller than 6% of the height FAILS. Run on every story/reel frame
before it is sent.  usage: python3 scripts/checks/dead_space_check.py <image> [...]"""
import sys
from PIL import Image
bad = 0
for p in sys.argv[1:]:
    im = Image.open(p).convert('L'); W, H = im.size; s = H / 1920
    top, bot = int(180 * s), H - 2   # Nov 23 11:35pm: the bottom zone may not be blank either (no text there, but imagery); x0, x1 = int(W * .15), int(W * .85)
    px = im.load(); run = best = 0; at = 0
    for y in range(top, bot):
        row = [px[x, y] for x in range(x0, x1, max(1, W // 200))]
        flat = max(row) - min(row) < 10
        run = run + 1 if flat else 0
        if run > best: best, at = run, y - run + 1
    lim = .06 * H
    ok = best <= lim
    bad += not ok
    print(f"{'PASS' if ok else 'FAIL'} {p}: biggest empty band {best}px ({best / H:.0%} of height) at y={at}")
sys.exit(1 if bad else 0)
