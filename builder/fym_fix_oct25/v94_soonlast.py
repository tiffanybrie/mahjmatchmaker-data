"""FYM v94 (Tiffany Oct 26 8:25-8:27am):
1. Mahjong Studios '2-Color Blue Studio' -> name 'Blue Studio'; its photo (a blue tile behind the set) is not good enough and it
   was the FIRST set in the A-Z list -> 'Photo coming soon' (t.soon).
2. Every 'Photo coming soon' tile set sorts to the BOTTOM of the tile lists (A-Z, brand and colour groups), never alphabetically.
3. Yellow Mountain Imports Aloha: the match-card circle showed a clear side view of one tile -> compilation from YMI's own
   listing photos (faces grid img 6 | plumeria backs img 7), 1600x700, so swipe strip, circle and band all show faces + backs.
Usage: v94_soonlast.py <build>"""
import sys, os, io, json, base64, hashlib
from PIL import Image
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
s = next(x for x in D['sets'] if x['slug'] == 'mahjong-studios-2-color-blue-studio'); s['name'] = 'Blue Studio'
t = D['tiles'][s['tile']]; t['soon'] = 1
if t.get('n', '').startswith('2-Color'): t['n'] = 'Blue Studio'
a = next(x for x in D['sets'] if x['slug'] == 'yellow-mountain-imports-aloha'); ta = D['tiles'][a['tile']]
os.makedirs(B + '/t94', exist_ok=True); fn = 't94/ymi-aloha-split.jpg'
im = Image.open(REPO + 'assets/tiles/v94/ymi-aloha-split.jpg').convert('RGB'); im.save(B + '/' + fn, quality=88)
sq = im.crop((450, 0, 1150, 700)).resize((360, 360), Image.LANCZOS); bb = io.BytesIO(); sq.save(bb, 'JPEG', quality=84)
pk = 'p94' + hashlib.md5(fn.encode()).hexdigest()[:10]
ta.setdefault('fo', ta.get('full')); ta['full'] = fn; ta['pile'] = pk; ta['bf'] = [.5, .5]; ta['split'] = 1
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
SO = "(!!T[a[0].tile].soon-!!T[b[0].tile].soon)||"
old = "sort((a,b)=>a[0].name.localeCompare(b[0].name))"; n = h.count(old); assert n >= 2, n
h = h.replace(old, "sort((a,b)=>" + SO + "a[0].name.localeCompare(b[0].name))")
old2 = "return (BACKG[S.tcol]||[]).flatMap(n=>all.filter(x=>x[0].name===n)).map("; assert h.count(old2) == 1
h = h.replace(old2, "return (BACKG[S.tcol]||[]).flatMap(n=>all.filter(x=>x[0].name===n)).sort((a,b)=>!!T[a[0].tile].soon-!!T[b[0].tile].soon).map(")
inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps({pk: 'data:image/jpeg;base64,' + base64.b64encode(bb.getvalue()).decode()}, separators=(',', ':')) + ');</script>'
anc = '<script src="b24v1.js"></script>'; assert h.count(anc) == 1; h = h.replace(anc, anc + inl, 1)
open(P, 'w').write(h); print('Blue Studio soon; soon sorts last (', n, 'A-Z sorts + colour groups ); Aloha split')
