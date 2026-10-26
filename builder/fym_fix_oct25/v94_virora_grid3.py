"""FYM v94 (APPROVED by Tiffany Oct 26 9:00am): Virora tile photo with a REAL, face-on back in the match card circle.
Tiffany Oct 26 8:41 (back not visible in the circle) + 8:52 (rejected side-lying cutouts; backs must be a flat top view).
Each image = three of Virora's own 3x3 studio grid photos: faces | grid with a back tile in the centre | faces.
config/fym-virora-backs-oct26.json (9 sets; 7 sets with no face-on back photo keep their current photo).
Same mechanics as v92_tilesplits.py (t.fo keeps the original for locks). Usage: v94_virora_grid3.py <build>"""
import sys, os, io, json, base64, hashlib
from PIL import Image
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
cfg = json.load(open(REPO + 'config/fym-virora-backs-oct26.json'))['splits']; IMG = {}; os.makedirs(B + '/t94', exist_ok=True)
for k, v in cfg.items():
    t = D['tiles'].get(k)
    if not t: print('missing tile', k); continue
    im = Image.open(REPO + v['img']).convert('RGB'); fn = 't94/' + os.path.basename(v['img'])
    im.save(B + '/' + fn, quality=86)
    sq = im.crop((450, 0, 1150, 700)).resize((360, 360), Image.LANCZOS); b = io.BytesIO(); sq.save(b, 'JPEG', quality=84)
    pk = 'p94g' + hashlib.md5(fn.encode()).hexdigest()[:10]; IMG[pk] = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
    t.setdefault('fo', t.get('full')); t['full'] = fn; t['pile'] = pk; t['bf'] = [.5, .5]; t['split'] = 1
    print('virora grid3', k, '->', fn)
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMG, separators=(',', ':')) + ');</script>'
a = '<script src="b24v1.js"></script>'; assert h.count(a) == 1; h = h.replace(a, a + inl, 1)
open(P, 'w').write(h)
