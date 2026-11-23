#!/usr/bin/env python3
"""DATE GATE (Tiffany Nov 19 + Nov 23 2026). Reads a LIVE code page three times and prints every date it carries
(long month, short month, ISO). PASS only if all three reads agree and the page shows exactly ONE day.
Run BEFORE any indexing request for an existing page, and after every date edit.
usage: date_gate.py /oh-my-mahjong-discount-code [more slugs]"""
import re, sys, time, random, urllib.request
MON = {m: i + 1 for i, m in enumerate("jan feb mar apr may jun jul aug sep oct nov dec".split())}
def days(slug):
    u = "https://www.mahjmatchmaker.com" + slug + "?dg=" + str(random.randint(1, 10**9))
    t = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=30).read().decode("utf-8", "ignore")
    out = {}
    for m, d, y in re.findall(r"verified (?:on |in )?([A-Z][a-z]{2,8})\.? (\d{1,2}), (20\d\d)", t):
        k = "%s-%02d-%02d" % (y, MON.get(m[:3].lower(), 0), int(d)); out[k] = out.get(k, 0) + 1
    for k in re.findall(r'"dateModified": ?"(20\d\d-\d\d-\d\d)', t) + re.findall(r'<time datetime="(20\d\d-\d\d-\d\d)"', t):
        out[k] = out.get(k, 0) + 1
    return out
bad = 0
for slug in sys.argv[1:]:
    reads = []
    for _ in range(3):
        reads.append(days(slug)); time.sleep(1.5)
    one = all(r == reads[0] for r in reads) and len(reads[0]) == 1
    print(("PASS " if one else "FAIL ") + slug + " " + str(reads[0] if one else reads))
    bad |= (not one)
sys.exit(1 if bad else 0)
