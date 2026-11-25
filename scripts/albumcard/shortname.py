"""Short card titles (Tiffany Nov 25 2:51am, Deco Indigo review: "Do you see how tiny that title is? You got to abbreviate it.
Get the text size back up."). A long mat name made the card title shrink until it was unreadable. gen2 runs every title
through short_title() before drawing, so no builder can ship a tiny title. Product-type words go first (Double-Sided,
Leatherette, Neoprene, Premium, Mahjong Mat, Mat, Vegan Leather), then trailing words, until the mat part fits MAX chars.
The full name stays in the manifest, the album page caption and the shop link."""
import re
MAX = 16      # product-type words go when the mat part is longer than this
PAREN = 22    # a (variant) is kept unless still longer than this
HARD = 26     # last resort: drop trailing words
FLUFF = [r'\bdouble[- ]sided\b', r'\bmahjong mat\b', r'\bmahj mat\b', r'\bneoprene\b', r'\bleatherette\b', r'\bpremium\b',
         r'\bsimple middle\b', r'\bartist collab\b', r'\bmat\b', r'\bin tube\b']
import json, os
_OV = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'config', 'card-short-names.json')
OV = json.load(open(_OV)) if os.path.exists(_OV) else {}
def _clean(s): return re.sub(r'\s{2,}', ' ', s).strip(' -,:')
def short_mat(nm, mx=MAX):
    if nm in OV: return OV[nm]
    s = nm.strip()
    if len(s) <= mx: return s
    for f in FLUFF: s = _clean(re.sub(f, '', s, flags=re.I))
    if len(s) > PAREN: s = _clean(re.sub(r'\([^)]*\)', '', s))
    w = s.split()
    while len(' '.join(w)) > HARD and len(w) > 2: w.pop()
    return ' '.join(w).strip(' -,:&') or nm
def short_title(t, mx=MAX):
    if ' + ' not in t: return t
    a, b = t.split(' + ', 1)
    return a + ' + ' + short_mat(b, mx)
if __name__ == '__main__':
    for n in ['Snowflake Reindeer Lodge Double-Sided Leatherette', 'Butterscotch Floral Simple Middle', 'Darjeeling Peacock Mat (Side A: Blue Scales)', 'Calista Leatherette', 'Dark Blue Art Deco Gold Geometric Fans']:
        print(n, '->', short_mat(n))
