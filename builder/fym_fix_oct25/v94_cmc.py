"""FYM v92: Charleston Mahjong Club uniform tile photo (Tiffany Oct 26 8:43am): every CMC set = a 1600x700 split,
clean faces tray (left) | that colourway's own backs tray (right), edge to edge, white centre line, from Bam Bird's own
listing photos only (no editing tiles in). config/fym-cmc-splits-oct26.json. The swipe strip shows the whole split,
the Mood board circle = centre square (half faces, half backs), Close up band centred. t.fo (original) is kept for locks.
Usage: v94_cmc.py <build>"""
import sys, os, io, json, base64, hashlib
from PIL import Image
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
cfg = json.load(open(REPO + 'config/fym-cmc-splits-oct26.json'))['splits']; IMG = {}; os.makedirs(B + '/t94', exist_ok=True)
for k, v in cfg.items():
    t = D['tiles'].get(k)
    if not t: print('missing tile', k); continue
    im = Image.open(REPO + v['img']).convert('RGB'); fn = 't94/' + os.path.basename(v['img'])
    im.save(B + '/' + fn, quality=88)
    sq = im.crop((450, 0, 1150, 700)).resize((360, 360), Image.LANCZOS); b = io.BytesIO(); sq.save(b, 'JPEG', quality=84)
    pk = 'pc94' + hashlib.md5(fn.encode()).hexdigest()[:10]; IMG[pk] = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
    t.setdefault('fo', t.get('full')); t['full'] = fn; t['pile'] = pk; t['bf'] = [.5, .5]; t['split'] = 1
    print('split', k, '->', fn)
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMG, separators=(',', ':')) + ');</script>'
a = '<script src="b24v1.js"></script>'; assert h.count(a) == 1; h = h.replace(a, a + inl, 1)
open(P, 'w').write(h)
