"""v112 data fixes prepared by the MATCH-INBOX sweep (Nov 1). Each fix names its inbox line. All are decisions Tiffany already
made or standing rules (no new taste calls). Idempotent. Run AFTER adds112.py. Usage: python3 fixes112.py <build_dir>

 1  OMM Dapper 2 RETIRED (doc 90): product URL 404 + gone from ohmymahjong.com/products.json (re-checked Nov 1). rt, '(retired)'
    name like Dapper 1, link -> OMM mats collection. Stays wfh (retired mats leave the decks anyway). Replacement = Tiffany.
 2  Mahjong Row & Co. Scalloped Tortoise is 20" (product page): drop `sm` (Tiffany Oct 26 7:36pm). Lock.
 3  YMI Ivory Pinstripe / Ridge / Stripes = ONE set "Ivory Stripes" (Tiffany Oct 30 10:34am): Stripes (fx-am014-a) stays, gets
    the real YMI photo (assets/fym-photos-oct30/tiles/yellow-mountain-imports-ivory-pinstripe.jpg: full face grid + back), no
    'Photo coming soon'; Pinstripe + Ridge sets/tiles hidden with merged_into (not deleted), their m carried over.
 4  Holiday calls Oct 29 (config/tiffany-color-notes/2026-10-29-holiday-calls.json): PLM Sugarplum Plaid / Blue Stripes / Blue
    Blooms -> holiday (were not in v110); the 8 'works_for_holiday_keep' mats -> wfh (bottom of Holiday). Liberty + Crimson
    Harvest stay year-round (already so).
 5  Chinoiserie Cheer (BJ&J): unhide on the flat photo assets/mats/v95-etsy/chinoiserie-cheer-flat.jpg (Tiffany sent it Oct 29)
    -> photo swap via v97_matwhite mechanics (replace112 below), flag ok, off the Questionable list.
 6  Poppins (OMM) = her real swipe picks (book FG8AbqV3YCXtURkQFbuncj, 19 YES): add to those sets' m (rule 4 'Tiffany's match').
 7  'No code available at this time' (Tiffany Oct 27 9:25am): ncn=1 on every mat/rack/tile of a brand with NO partner piece
    (Sunday, Ozark, Tala, Bougie, BJ&J, Piper Chase, Hutch & Nook, Mahj & Moon, ...). v110 had it on House of Hearts only.
 8  Mahjong Studios rack name '20" Blue Luxury Acrylic Scalloped ... – Yellow' -> drop the stray ' – Yellow' (v105 QA).
"""
import sys, os, io, json, re, base64, shutil
from PIL import Image
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
M, R, T, sets = D['mats'], D['racks'], D['tiles'], D['sets']
LK = json.load(open(REPO + 'builder/fym_flags/locks.json')); log = []; IMG = {}

# 1 Dapper 2
k = 'www.ohmymahjong.com/dapper-mat-w-tube'
if k in M and not M[k].get('rt'):
    M[k].update(rt=True, n='Dapper 2 (retired)', u='https://www.ohmymahjong.com/collections/mahjong-mats')
    LK['mats'].setdefault(k, {}).update(rt=True, n='Dapper 2 (retired)'); log.append('1 Dapper 2 retired')
# 2 MRC tortoise
k = 'mahjongrowandco.com/scalloped-deluxe-tortoise-rack'
if R.get(k, {}).get('sm'):
    R[k].pop('sm'); R[k]['len'] = 20; log.append('2 MRC Scalloped Tortoise: sm removed (20")')
LK.setdefault('racks', {})[k] = {'sm': False, 'len': 20, 'why': 'Tiffany Oct 26 7:36pm: 20" rack, offer with every set'}
# 3 YMI Ivory merge
KEEP, GONE = 'www.ymimports.com/fx-am014-a', ['www.ymimports.com/fx-am022-a', 'www.ymimports.com/fx-am019-a']
ks = next(s for s in sets if s['tile'] == KEEP)
if T[KEEP].get('soon'):
    os.makedirs(B + '/t112', exist_ok=True)
    src = Image.open(REPO + 'assets/fym-photos-oct30/tiles/yellow-mountain-imports-ivory-pinstripe.jpg').convert('RGB')
    src.save(B + '/t112/ymi-ivory-stripes.jpg', quality=88)
    pile = src.crop((0, 0, int(src.width * .45), src.height)); pile.thumbnail((300, 300)); b = io.BytesIO(); pile.save(b, 'JPEG', quality=78)
    IMG['p112ymiivory'] = 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
    T[KEEP].update(full='t112/ymi-ivory-stripes.jpg', pile='p112ymiivory', src='assets/fym-photos-oct30/tiles/yellow-mountain-imports-ivory-pinstripe.jpg')
    T[KEEP].pop('soon', None); ks['name'] = 'Ivory Stripes'; T[KEEP]['n'] = 'Ivory Stripes'
    for g in GONE:
        gs = next((s for s in sets if s['tile'] == g), None)
        if gs:
            have = {e[0] for e in ks['m']}
            ks['m'] += [e for e in gs['m'] if e[0] not in have]
            gs['hid'] = 1; gs['merged_into'] = ks['slug']
        T[g]['hid'] = 1; T[g]['merged_into'] = KEEP
    LK['tiles'][KEEP] = {'set': 'Ivory Stripes', 'src': T[KEEP]['src'], 'full': T[KEEP]['full'], 'pile': 'p112ymiivory'}
    log.append('3 YMI Ivory merged into Ivory Stripes (real photo)')
# 4 holiday calls
HC = json.load(open(REPO + 'config/tiffany-color-notes/2026-10-29-holiday-calls.json'))
def find(full):
    for k_, o in M.items():
        if o.get('hid'): continue
        if full.lower() == (o.get('bn', '') + ' ' + o['n']).lower() or (full.lower().startswith(o.get('bn', '').lower()) and o['n'].lower() in full.lower() and len(o['n']) > 5):
            return k_
FIX4 = {'Bam Bird Boutique Vegan Leather Caramel': 'www.bambirdboutique.com/origami-leather-mat?v=51114566746421',
        'Mahj Mood Sleigh All Day': 'mahjmood.com/sleigh-all-day-mat', 'Sunday Mahjong Golden Gingham': 'sundaymahjong.com/golden-gingham-premium-mahjong-mat'}
for nm in HC['holiday']:
    k_ = FIX4.get(nm) or find(nm)
    if k_ and not M[k_].get('hol'):
        o = M[k_]; fams = o.get('mf') or o.get('ha') or []
        o.update(hol=True, ha=fams, mf=[], mt=[], sh=[]); log.append('4 holiday: ' + nm)
    elif not k_: log.append('4 NOT FOUND (check by hand): ' + nm)
for nm in HC['works_for_holiday_keep']:
    k_ = FIX4.get(nm) or find(nm)
    if k_ and not M[k_].get('wfh'): M[k_]['wfh'] = True; log.append('4 wfh: ' + nm)
    elif not k_: log.append('4 wfh NOT FOUND (check by hand): ' + nm)
# 6 Poppins picks
PK = 'www.ohmymahjong.com/poppins-mat-in-tube'
YES = ['Lola', 'Moonlight', 'Osler', 'Preppy Soirée', 'Coquette', 'Birdie', 'Amara', 'Dandy', 'Glitterville', 'Petalée', 'Lilac Soirée',
       'Luminaire', 'Taylor', 'Glow Wild', 'La Fete', 'Spring Love', 'Talulah', 'Gemma', 'Pearlescent']
if PK in M:
    for nm in YES:
        s = next((s for s in sets if s['name'] == nm and not s.get('hid')), None)
        if not s: log.append('6 set not found: ' + nm); continue
        if not any(e[0] == PK for e in s['m']):
            s['m'].append([PK, []]); LK['sets'].setdefault(s['slug'], {})['m'] = s['m']
            log.append('6 Poppins -> ' + nm)
# 7 ncn
partner_brands = {o.get('bn') for X in (M, R, T) for o in X.values() if isinstance(o, dict) and o.get('pa') and not o.get('nc')}
n7 = 0
for X in (M, R, T):
    for o in X.values():
        if isinstance(o, dict) and o.get('bn') and o['bn'] not in partner_brands and not o.get('dc') and not o.get('ncn'):
            o['ncn'] = 1; n7 += 1
log.append(f'7 ncn set on {n7} non-partner items')
# 8 MS rack name
for o in R.values():
    if o.get('bn') == 'Mahjong Studios' and o['n'].startswith('20" Blue Luxury') and o['n'].endswith(' – Yellow'):
        o['n'] = o['n'][:-len(' – Yellow')]; log.append('8 MS rack name fixed')

h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
if IMG:
    inl = '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(IMG, separators=(',', ':')) + ');</script>'
    a = '<script src="b24v1.js"></script>'; assert h.count(a) == 1; h = h.replace(a, a + inl, 1)
open(P, 'w').write(h)
json.dump(LK, open(REPO + 'builder/fym_flags/locks.json', 'w'), indent=1, ensure_ascii=False)
print('\n'.join(log))

# 5 Chinoiserie Cheer photo swap + unhide (v97_matwhite mechanics, own config so already-applied rows never re-run)
CC = 'www.etsy.com/listing/4537268829/chinoiserie-cheer-mahjong-mat'
src = open(REPO + 'builder/fym_fix_oct25/v97_matwhite.py').read()
for a_, b_ in [("config/fym-mat-white-oct26.json", "config/fym-mat-replace-nov01.json"),
               ("if not m or m.get('w97') or m.get('hid'): continue", "if not m or m.get('w97') or m.get('w112'): continue"),
               ("m['w97'] = fo['action']", "m['w112'] = fo['action']; m.pop('hid', None)"),
               ("'mt97'", "'mt112'")]:
    assert a_ in src, 'v97_matwhite changed: ' + a_
    src = src.replace(a_, b_)
exec(compile(src, 'replace112', 'exec'), {'__name__': '__main__', '__file__': REPO + 'builder/fym_fix_oct25/v97_matwhite.py'})
FL = json.load(open(REPO + 'builder/fym_flags/mat_photo_flags.json'))
FL[CC] = dict(FL.get(CC, {}), flag='ok', note='Nov 1 v112: flat photo from Tiffany\'s Etsy screenshots (Oct 29), unhidden')
json.dump(FL, open(REPO + 'builder/fym_flags/mat_photo_flags.json', 'w'), indent=1, ensure_ascii=False)
Q = json.load(open(REPO + 'builder/fym_flags/fym_questionable.json'))
Q['items'] = [it for it in Q['items'] if it.get('key') != CC]
json.dump(Q, open(REPO + 'builder/fym_flags/fym_questionable.json', 'w'), indent=1, ensure_ascii=False)
LK = json.load(open(REPO + 'builder/fym_flags/locks.json'))
if CC in LK['mats']: LK['mats'][CC]['hid'] = False
json.dump(LK, open(REPO + 'builder/fym_flags/locks.json', 'w'), indent=1, ensure_ascii=False)
