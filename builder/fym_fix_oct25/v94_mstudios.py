"""FYM v94: Mahjong Studios tile photos, config-driven (config/fym-mstudios-oct26.json; Tiffany Oct 26 8:48am, which
replaces her 8:42 'all Photo coming soon'). Per set: keep | white_bg | pile_photo (new real photo, black cut to white,
square like the kept sets) | soon | hide. Brands whose visible sets are ALL 'Photo coming soon' sort last in Shop by
brand (generic). Run after v94_soonlast.py. Idempotent. Gate [62].
Usage: python3 v94_mstudios.py <build_dir>"""
import sys, os, io, json, base64, hashlib
from PIL import Image
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
cfg = json.load(open(REPO + 'config/fym-mstudios-oct26.json'))['sets']; IMG = {}; os.makedirs(B + '/t94', exist_ok=True)
sets = {s['tile']: s for s in D['sets']}
for k, v in cfg.items():
    t = D['tiles'].get(k)
    if not t: print('missing tile', k); continue
    do = v['do']
    if do in ('keep', 'white_bg', 'pile_photo'): t.pop('soon', None)
    if do == 'soon': t['soon'] = 1
    if do == 'hide' and k in sets: sets[k]['hid'] = True
    if do in ('white_bg', 'pile_photo'):
        fn = 't94/ms-' + os.path.basename(v['img'])
        if t.get('full') != fn:
            im = Image.open(REPO + v['img']).convert('RGB'); im.save(B + '/' + fn, quality=88)
            sq = im.resize((360, 360), Image.LANCZOS); b = io.BytesIO(); sq.save(b, 'JPEG', quality=84)
            pk = 'p94' + hashlib.md5(fn.encode()).hexdigest()[:10]; IMG[pk] = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
            t.setdefault('fo', t.get('full')); t['full'] = fn; t['pile'] = pk
            for x in ('bf', 'split'): t.pop(x, None)
    print(do, t['n'])
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
old = "n[s.maker]=(n[s.maker]||0)+1;pa[s.maker]=pa[s.maker]||!!t.pa;});const B=Object.keys(n).sort((a,b)=>a.localeCompare(b))"
new = ("n[s.maker]=(n[s.maker]||0)+1;pa[s.maker]=pa[s.maker]||!!t.pa;so[s.maker]=(so[s.maker]??true)&&!!t.soon;});"
       "const B=Object.keys(n).sort((a,b)=>(so[a]-so[b])||a.localeCompare(b))")
if old in h:
    assert h.count(old) == 1
    h = h.replace(old, new).replace("function brandMenu(){const all=D.sets.filter(VIS),pa={},n={};",
                                    "function brandMenu(){const all=D.sets.filter(VIS),pa={},n={},so={};", 1)
    assert 'so={}' in h; print('brand menu: all-soon brands last')
if IMG:
    inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMG, separators=(',', ':')) + ');</script>'
    a = '<script src="b24v1.js"></script>'; assert h.count(a) == 1; h = h.replace(a, a + inl, 1)
open(P, 'w').write(h)
