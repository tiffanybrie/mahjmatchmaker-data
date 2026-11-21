"""Swap the V1228PIN/ placeholder in the FYM v123 build for its pinned jsDelivr address. Usage: python3 pin123.py <index.html> <commit sha>"""
import sys, re
p, sha = sys.argv[1], sys.argv[2]; assert re.fullmatch(r'[0-9a-f]{40}', sha)
h = open(p).read(); n = h.count('V1228PIN/'); assert n > 0
h = h.replace('V1228PIN/', f'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@{sha}/site-app/fym-v122-8/'); open(p, 'w').write(h); print('pinned', n)
