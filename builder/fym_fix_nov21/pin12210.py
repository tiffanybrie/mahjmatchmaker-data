"""Swap the V12210PIN/ placeholder in the FYM v123 build for its pinned jsDelivr address. Usage: python3 pin123.py <index.html> <commit sha>"""
import sys, re
p, sha = sys.argv[1], sys.argv[2]; assert re.fullmatch(r'[0-9a-f]{40}', sha)
h = open(p).read(); n = h.count('V12210PIN/'); assert n > 0
h = h.replace('V12210PIN/', f'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@{sha}/site-app/fym-v122-10/'); open(p, 'w').write(h); print('pinned', n)
