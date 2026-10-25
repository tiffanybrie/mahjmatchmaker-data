"""FYM v84 (Tiffany Oct 25 14:12, approved): door buttons 'Start with tiles' / 'Start with a mat' (were 'I have tiles' / 'I have a mat').
Her husband: 'what if I don't have either?' (gift buyers, first-timers). Tour step 1 no longer says 'what you have'.
Usage: python3 v84_doors.py <build_dir>  (in place)"""
import sys
P = sys.argv[1] + '/index.html'; h = open(P).read()
R = [
    ('>I have tiles<small>', '>Start with tiles<small>', 1),
    ('>I have a mat<small>', '>Start with a mat<small>', 1),
    ("p:'Start with what you have: tap \\u201cI have tiles\\u201d or \\u201cI have a mat\\u201d, then pick yours just below:",
     "p:'Tap \\u201cStart with tiles\\u201d or \\u201cStart with a mat\\u201d, then pick one just below:", 1),
]
for a, b, n in R:
    assert h.count(a) == n, (a, h.count(a)); h = h.replace(a, b)
assert 'I have tiles' not in h and 'I have a mat' not in h
open(P, 'w').write(h); print('ok')
