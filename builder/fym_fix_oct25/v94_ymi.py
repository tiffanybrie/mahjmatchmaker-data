"""FYM v94: Yellow Mountain Imports uniform tile photo (Tiffany Oct 26 8:48am: "all of Yellow Mountain imports tiles,
including Canyon Clay, Celestial Harmony, they all have the same problem that the original [Aloha] did").
Every YMI set = a 1600x700 split from YMI's own listing photos: faces tray (left) | flat, face-on backs tray (right),
white centre line, so the Mood board circle (centre square x450-1150) shows faces AND the back colour (8:52 rule: backs
must be straight-on, real, nothing that looks Photoshopped). config/fym-ymi-splits-oct26.json; gate [63].
t.fo (original) is kept for locks. Mojave (formerly soon: only a lone back + coin shot) now has a real split -> soon off.
Run after v94_soonlast.py. Idempotent. Usage: v94_ymi.py <build>"""
import sys, os, io, json, base64, hashlib
from PIL import Image
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
C = json.load(open(REPO + 'config/fym-ymi-splits-oct26.json')); IMG = {}; os.makedirs(B + '/t94', exist_ok=True)
for k, v in C['splits'].items():
    t = D['tiles'].get(k)
    if not t: print('missing tile', k); continue
    fn = 't94/' + os.path.basename(v['img'])
    im = Image.open(REPO + v['img']).convert('RGB'); im.save(B + '/' + fn, quality=88)
    pk = 'p94' + hashlib.md5(fn.encode()).hexdigest()[:10]
    if t.get('full') != fn or t.get('pile') != pk:
        sq = im.crop((450, 0, 1150, 700)).resize((360, 360), Image.LANCZOS); b = io.BytesIO(); sq.save(b, 'JPEG', quality=84)
        IMG[pk] = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
        if t.get('full') != fn: t.setdefault('fo', t.get('full'))
        t['full'] = fn; t['pile'] = pk; t['bf'] = [.5, .5]; t['split'] = 1
        print('split', v['name'], '->', fn)
for k in C.get('soon', []):
    if k in D['tiles'] and not D['tiles'][k].get('soon'): D['tiles'][k]['soon'] = 1; print('Photo coming soon:', D['tiles'][k]['n'])
for k in C.get('unsoon', []):
    if k in D['tiles'] and D['tiles'][k].pop('soon', None): print('photo now ok, soon off:', D['tiles'][k]['n'])
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
if IMG:
    inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMG, separators=(',', ':')) + ');</script>'
    a = '<script src="b24v1.js"></script>'; assert h.count(a) == 1; h = h.replace(a, a + inl, 1)
open(P, 'w').write(h)
