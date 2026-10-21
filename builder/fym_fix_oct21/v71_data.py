"""FYM v71 data changes (Oct 21 evening). Usage: python3 builder/fym_fix_oct21/v71_data.py <build_dir>
Run AFTER soiree_holiday.py (the v71 base = live v70 + Soiree holiday mats). Idempotent.
1. The Kerry (Betty June & Jeannette): Tiffany's real pick (live album card #4, Oct 21) in 11 sets' match lists (m).
   Racks = the set's tile racks (racks every existing entry shares) + config/mat-racks-picks.json kerry racks.
   Mat u = her ShopMy link https://go.shopmy.us/p-96114928 (not Etsy). Jasmine is NOT included (her call).
   locks.json sets.<slug>.m updated to match (approved change), live album snapshot gets the Kerry card at #4,
   then D.ao is recomputed with album_order.compute.
2. December 1994 (Sunday Mahjong) tile photo: Tiffany Oct 21 6:20pm "really not looking great inside of the picker".
   New photo = Sunday Mahjong's product image 1 (box + tile backs + faces on the plaid mat), footer bar cropped off.
   full = whole image minus footer; pile (picker circle) = square crop on the box label + faces. Lock updated."""
import sys, os, json, io, base64, shutil
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
REPO = os.path.abspath(os.path.join(HERE, '..', '..')) + '/'
B = sys.argv[1]
LOCKS = REPO + 'builder/fym_flags/locks.json'
SNAP = REPO + 'scripts/social/its_a_match/albums-live-oct21.json'
h = open(B + '/index.html').read(); i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
M, R, T = D['mats'], D['racks'], D['tiles']
L = json.load(open(LOCKS))
chg = []

# ---- 1. Kerry
KERRY = 'www.etsy.com/listing/4493549326/the-kerry-mahjong-mat-watercolor-pink'
SHOPMY = 'https://go.shopmy.us/p-96114928'
KR = ['bb:Ballet Pink', 'missmahjong.com/iridescent-opal-scalloped-acrylic-racks', 'mahjmood.com/copy-scalloped-clear-acrylic-rack-and-pusher-set-of-4']
SETS = ['pearlescent', 'moonlight', 'la-fete', 'willow', 'talulah', 'coquette', 'birdie', 'dandy', 'luminaire', 'taylor', 'sorbet']
assert KERRY in M and all(r in R for r in KR)
M[KERRY]['u'] = SHOPMY
done = []
for s in D['sets']:
    if s['slug'] not in SETS or not s.get('album'): continue
    if any(e[0] == KERRY for e in s['m']): done.append(s['slug']); continue
    base = [r for r in s['m'][0][1] if all(r in e[1] for e in s['m'])] or list(s['m'][0][1])
    racks = list(dict.fromkeys(base + KR))
    s['m'].insert(min(3, len(s['m'])), [KERRY, racks])
    done.append(s['slug'])
    if s['slug'] in L['sets']:
        L['sets'][s['slug']]['m'] = s['m']
assert sorted(set(done)) == sorted(SETS), (done, SETS)
chg.append({'date': '2026-10-21', 'set': ','.join(SETS), 'field': 'm',
            'change': f'added The Kerry ({KERRY}) at #4 with tile racks + Kerry racks {KR}',
            'approval': "Tiffany Oct 21 3:39pm: Kerry cards into these 11 live albums (Jasmine dropped on her call); album cards live Oct 21 evening (site/livepatch/kerry-oct21/README.md). Her real pick, approved change."})
# live album snapshot: Kerry card is #4 on each of the 11 live pages
A = json.load(open(SNAP))
for a in A:
    if a['slug'] in SETS and not any('kerry' in c['mat'].lower() for c in a['cards']):
        a['cards'].insert(3, {'n': '04', 'img': '', 'mat': 'The Kerry', 'brand': 'Betty June & Jeannette', 'retired': False})
        for k, c in enumerate(a['cards']): c['n'] = '%02d' % (k + 1)
        if isinstance(a.get('n'), int): a['n'] += 1
json.dump(A, open(SNAP, 'w'), indent=0)
import album_order
D['ao'], _ = album_order.compute(D)

# ---- 2. December 1994 photo
DEC = 'sundaymahjong.com/december-1994-tile-set-preorder-est-nov-27'
SRC = 'assets/tiles/sunday_mahjong_december_1994_box_brand_oct21.jpg'
FULL = 't16/sunday-mahjong-december-1994-v71.jpg'
PILE = 'p16sundaydec94v71'
raw = os.environ.get('DEC94_BRAND', '')
if not os.path.exists(REPO + SRC):
    im = Image.open(raw).convert('RGB').crop((0, 0, 1200, 1015)); im.save(REPO + SRC, quality=90)
im = Image.open(REPO + SRC).convert('RGB')
full = im.copy(); full.thumbnail((1000, 1000)); full.save(os.path.join(B, FULL), quality=86)
pile = im.crop((250, 355, 910, 1015))  # 660x660: box label + backs + faces (circle crop in the picker)
pile = pile.resize((360, 360), Image.LANCZOS); b = io.BytesIO(); pile.save(b, 'JPEG', quality=82)
open(os.path.join(B, 'b20v1.js'), 'w').write('window.IMG=Object.assign(window.IMG||{},' + json.dumps({PILE: 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()}) + ');')
T[DEC].update(src=SRC, full=FULL, pile=PILE)
for s in D['sets']:
    if s['tile'] == DEC: s['fp'] = [0.5, 0.62]
L['tiles'][DEC].update(src=SRC, full=FULL, pile=PILE)
chg.append({'date': '2026-10-21', 'tile': DEC, 'field': 'src/full/pile',
            'change': f'{SRC} (Sunday Mahjong product image 1: box + tile backs + faces, footer cropped) replaces the tilebox CARD-ONLY close-up',
            'approval': "Tiffany Oct 21 6:20pm: 'really not looking great inside of the picker. We need a different photo for December 1994.'"})
if not any(c.get('change', '').startswith(SRC) for c in L['_changes']):
    L['_changes'] += chg
elif not any('The Kerry' in c.get('change', '') for c in L['_changes']):
    L['_changes'].append(chg[0])
json.dump(L, open(LOCKS, 'w'), ensure_ascii=False, indent=1)
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
last = '<script src="b19v1.js"></script>'
if 'b20v1.js' not in h: h = h.replace(last, last + '<script src="b20v1.js"></script>', 1)
open(B + '/index.html', 'w').write(h)
print('kerry sets', len(done), 'ao sets', len(D['ao']), 'dec94', FULL, PILE)
