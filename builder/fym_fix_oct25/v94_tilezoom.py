"""FYM v94: tile photos zoomed so the match-card circle is completely filled with tiles (Tiffany Oct 26 9:03am PLM,
9:04am My Fair Mahjong, 9:05am PLM OG Desert Dreams + OG Pretty in Pink -> straight-on aerial like the rest of PLM).
config/fym-tilezoom-oct26.json: tile key -> square crop of the brand's own listing photo (largest square inside the
tile grid). t.full = that square, pile = same square at 360px, bf centred. t.fo keeps the original for locks. Gate [66].
Usage: v94_tilezoom.py <build>"""
import sys, os, io, json, base64, hashlib
from PIL import Image
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
cfg = json.load(open(REPO + 'config/fym-tilezoom-oct26.json'))['tiles']; IMG = {}; os.makedirs(B + '/t94', exist_ok=True)
for k, v in cfg.items():
    t = D['tiles'].get(k)
    if not t: print('missing tile', k); continue
    fn = 't94/' + os.path.basename(v['img'])
    if t.get('full') == fn: continue
    im = Image.open(REPO + v['img']).convert('RGB'); im.save(B + '/' + fn, quality=88)
    sq = im.resize((360, 360), Image.LANCZOS); b = io.BytesIO(); sq.save(b, 'JPEG', quality=84)
    pk = 'pz94' + hashlib.md5(fn.encode()).hexdigest()[:10]; IMG[pk] = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
    t.setdefault('fo', t.get('full')); t['full'] = fn; t['pile'] = pk; t['bf'] = [.5, .5]; t.pop('split', None)
    print('zoom', t['n'], '->', fn)
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
if IMG:
    inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMG, separators=(',', ':')) + ');</script>'
    a = '<script src="b24v1.js"></script>'; assert h.count(a) == 1; h = h.replace(a, a + inl, 1)
open(P, 'w').write(h)
