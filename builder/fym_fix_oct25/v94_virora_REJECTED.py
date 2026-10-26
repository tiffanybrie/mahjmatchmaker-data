"""REJECTED by Tiffany Oct 26 8:52am (cut-out backs on their side + fake shadow look photoshopped). DO NOT RUN.
FYM v94: Virora uniform tile photo (Tiffany Oct 26 8:41am: "you can't see the tile back ... in the circle match card").
Every Virora set = a 1600x700 split from Virora's own listing image 00: faces flat lay (left) | the set's own back tile cut from the
same photo, 3 whole tiles inside the Mood board circle + 3 more filling the swipe strip (same layout as the CMC option C revision).
config/fym-virora-splits-oct26.json. Same mechanics as v92_tilesplits.py (t.fo keeps the original for locks).
Usage: v94_virora.py <build>"""
import sys, os, io, json, base64, hashlib
from PIL import Image
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
sys.exit('v94_virora REJECTED Oct 26 8:52, do not run')
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
cfg = json.load(open(REPO + 'config/fym-virora-splits-oct26_REJECTED.json'))['splits']; IMG = {}; os.makedirs(B + '/t94', exist_ok=True)
for k, v in cfg.items():
    t = D['tiles'].get(k)
    if not t: print('missing tile', k); continue
    im = Image.open(REPO + v['img']).convert('RGB'); fn = 't94/' + os.path.basename(v['img'])
    im.save(B + '/' + fn, quality=86)
    sq = im.crop((450, 0, 1150, 700)).resize((360, 360), Image.LANCZOS); b = io.BytesIO(); sq.save(b, 'JPEG', quality=84)
    pk = 'p94v' + hashlib.md5(fn.encode()).hexdigest()[:10]; IMG[pk] = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
    t.setdefault('fo', t.get('full')); t['full'] = fn; t['pile'] = pk; t['bf'] = [.5, .5]; t['split'] = 1
    print('virora split', k, '->', fn)
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMG, separators=(',', ':')) + ');</script>'
a = '<script src="b24v1.js"></script>'; assert h.count(a) == 1; h = h.replace(a, a + inl, 1)
open(P, 'w').write(h)
