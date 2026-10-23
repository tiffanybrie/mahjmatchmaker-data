"""FYM v78 decisions (Tiffany Oct 23 3:25-3:27pm):
 - Middle & Main's 5 state sets must NOT be hidden: unhide with a real layout photo of the tiles (picked by eye from the
   brand's own images, Oct 23): Barrier Island #2, Charleston #2, Palmetto #6, Peach & Pine #2, Sunshine #4.
 - Bespoke mega/XL sets stay out (racks are mostly 20-inch; a mega set could lead to the wrong racks): stay hidden, reason recorded.
 - OMM Debutantes are travel sets: stay hidden, reason recorded.
Usage: python3 v78_answers.py <build_dir> <mm img dir>"""
import sys, io, json, base64, hashlib, os
from PIL import Image
B, IM = sys.argv[1:3]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
PICK = {'middle-main-mahjong-barrier-island': ('barrier-island-tiles-a-southern-shoreline-inspired-mahjong-set', 2),
        'middle-main-mahjong-charleston': ('charleston-tiles-a-south-carolina-inspired-mahjong-set', 2),
        'middle-main-mahjong-palmetto': ('palmetto-tiles-a-south-carolina-inspired-mahjong-set', 6),
        'middle-main-mahjong-peach-pine': ('peach-pine-tiles-a-georgia-inspired-mahjong-set', 2),
        'middle-main-mahjong-sunshine': ('sunshine-tiles-a-florida-inspired-mahjong-set', 4)}
os.makedirs(B + '/t78', exist_ok=True); IMGS = {}
js = B + '/b23v1.js'; txt = open(js).read(); IMGS = json.loads(txt[txt.index(',') + 1:txt.rindex(')')])
for s in D['sets']:
    if s['slug'] in PICK:
        hnd, n = PICK[s['slug']]; im = Image.open(f'{IM}/{hnd}-{n}.jpg').convert('RGB')
        full = im.copy(); full.thumbnail((1000, 1000)); fn = f't78/{s["slug"]}.jpg'; full.save(f'{B}/{fn}', quality=88)
        w, hh = im.size; q = min(w, hh); pp = im.crop(((w - q) // 2, (hh - q) // 2, (w - q) // 2 + q, (hh - q) // 2 + q)).resize((360, 360), Image.LANCZOS)
        b = io.BytesIO(); pp.save(b, 'JPEG', quality=84); pk = 'p78' + hashlib.md5(s['slug'].encode()).hexdigest()[:10]
        IMGS[pk] = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
        D['tiles'][s['tile']].update(full=fn, pile=pk); D['tiles'][s['tile']].pop('hid', None); D['tiles'][s['tile']].pop('soon', None); s.pop('hid', None)
        print('shown', s['name'], fn)
open(js, 'w').write('window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMGS) + ');')
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]; open(P, 'w').write(h)
