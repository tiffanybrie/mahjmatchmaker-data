"""FYM v95: Rackin' Rudolph (Hip Hip) tile photo from Tiffany's Canva v2 (Oct 26 11:55am: v2 puts the red back + green/white
layer in the match circle). v2 has a seam at x~980 (a second copy of the columns to its right), so nothing right of x 978 is used:
- full (app tile view, 16:7 strip): v1 left part + v2 tail = one continuous 1600x700 strip ending on the backs, no seam.
- cf (card circle / close-up, new field): the 700x700 square of v2 ending at x 978 (faces + red back + green layer).
- pile (grid thumbnail): 360px of the square.
The card draws T.cf when set (generic). Removes 'soon'. fo keeps the album photo for gates [1]/[6]. Idempotent.
Usage: python3 v95_rudolph.py <build_dir>"""
import sys, os, io, json, base64, hashlib, shutil
from PIL import Image
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
K = 'hol:rackin-rudolph'; A = REPO + 'assets/tiles/v95/rudolph/'
os.makedirs(B + '/t95r', exist_ok=True)
FULL, CF = 't95r/rackin-rudolph-strip.jpg', 't95r/rackin-rudolph-circle.jpg'
for src, dst in (('rackin-rudolph-strip.jpg', FULL), ('rackin-rudolph-circle.jpg', CF)):
    if os.path.islink(B + '/' + dst) or not os.path.exists(B + '/' + dst): shutil.copyfile(A + src, B + '/' + dst)
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
t = D['tiles'][K]
sq = Image.open(A + 'rackin-rudolph-circle.jpg').convert('RGB').resize((360, 360), Image.LANCZOS)
b = io.BytesIO(); sq.save(b, 'JPEG', quality=84); pk = 'p95' + hashlib.md5(b'rackin-rudolph-circle-v2').hexdigest()[:10]
if t.get('full') != FULL: t.setdefault('fo', t.get('full')); t['full'] = FULL
t['cf'] = CF; t['pile'] = pk; t.pop('soon', None)
for x in ('bf', 'split'): t.pop(x, None)
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
old = "Promise.resolve(tileFull(s)||pile(s)).then(lk)"
new = "Promise.resolve((T[s.tile].cf&&!T[s.tile].soon?T[s.tile].cf:tileFull(s))||pile(s)).then(lk)"
if old in h: assert h.count(old) == 1; h = h.replace(old, new)
assert new in h
if ('"' + pk + '":') not in h:
    inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps({pk: 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()}) + ');</script>'
    a = '<script src="b24v1.js"></script>'; assert h.count(a) == 1; h = h.replace(a, a + inl, 1)
open(P, 'w').write(h); print("rudolph: Canva v2 strip + circle, pile", pk)
