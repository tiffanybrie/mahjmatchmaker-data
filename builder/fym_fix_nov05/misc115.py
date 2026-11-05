"""FYM v115 follow-through (Nov 5, DESK item 2b), run AFTER adds115.py + the Etsy add + v104rank:
 1. Late holiday m-lists = Tiffany's real picks: config/late-holiday-picks-nov03.json (33) + her 12 Santa Baby's Cocktail Hour swipe-book
    yeses (config/swipe-yeses/holiday-oct21.json 'santababy'), as built for the albums in assets/cards/holiday-late-nov04/manifest.json
    (same mat racks). Appended to each set's m (A YES IS A YES), locks + swipe_yeses_map updated so they stay.
 2. OMM Esme RETIRED (doc 90): gone from ohmymahjong.com (products.json + /products/esme-mat-w-tube 404, Nov 4). rt, '(retired)', link ->
    OMM mats collection. Stays in her m-lists (Emerald, Glow Wild) as a pick.
 3. TdT House Tigers Oyster back in stock (store check Nov 3 6:40pm ET, $295): Sold out badge off.
 4. LBB Camellia Kaleidoscope leatherette = material twin of the Camellia Kaleidoscope card already in FYM: 'Also available in leatherette'.
Idempotent. Usage: python3 misc115.py <build_dir>"""
import sys, os, json, re
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
T, M, R, sets = D['tiles'], D['mats'], D['racks'], D['sets']
LK = json.load(open(REPO + 'builder/fym_flags/locks.json')); SYP = REPO + 'builder/fym_flags/swipe_yeses_map.json'; SY = json.load(open(SYP))
log = []
# 1
MAN = json.load(open(REPO + 'assets/cards/holiday-late-nov04/manifest.json'))
BYSLUG = {s['slug']: s for s in sets}
def norm(x): return re.sub(r'[^a-z0-9]', '', x.lower().replace('é', 'e').replace("'", ''))
BYNAME = {}
for s in sets: BYNAME.setdefault(norm(s['name']), s)
MATS = {}
for k, o in M.items():
    if o.get('hid'): continue
    MATS.setdefault((norm(o.get('bn', '')), norm(o['n'].replace(' (retired)', ''))), k)
RK = {}
for k, r in R.items():
    if not r.get('hid'): RK.setdefault(r['n'], k)
miss = []
RALIAS = {'Miss Mahjong Scalloped Iridescent Opal': 'missmahjong.com/iridescent-opal-scalloped-acrylic-racks',
          'Middle & Main Milk Glass Scalloped Acrylic': 'www.middleandmainmahjong.com/milk-glass-collection-mahjong-rack-and-pusher-set-of-4',
          'Middle & Main Hawksbill Heritage Tortoise': 'mm:Hawksbill'}
for n_, k_ in RALIAS.items():
    if k_ in R and not R[k_].get('hid'): RK.setdefault(n_, k_)
MALIAS = {("Bespoke Mahjong", "It's a Vibe Holiday"): 'www.bespokemahjong.com/mahjholidaymat'}
SALIAS = {'sunday': 'sunday-mahjong-sunday'}  # Spring Love + Shangri-La (vault sets) are not FYM sets
for c in MAN:
    s = BYSLUG.get(c['tile']) or BYSLUG.get(SALIAS.get(c['tile'], '')) or BYNAME.get(norm(c['tileName']))
    mk = MALIAS.get((c['brand'], c['mat'])) or MATS.get((norm(c['brand']), norm(c['mat'])))
    if not mk:  # brand spelled differently in FYM (e.g. Soiree All Day)
        cand = [k for (b, n), k in MATS.items() if n == norm(c['mat']) and (b[:5] == norm(c['brand'])[:5])]
        mk = cand[0] if len(cand) == 1 else None
    if not s or not mk: miss.append((c['n'], c['tileName'], c['mat'], 'set' if not s else 'mat')); continue
    racks = [RK[n] for n in c['mat_racks'] if n in RK]
    if len(racks) != len(c['mat_racks']): miss.append((c['n'], 'rack', [n for n in c['mat_racks'] if n not in RK]))
    if not any(e[0] == mk for e in s['m']):
        s['m'].append([mk, racks]); log.append(f"m + {s['name']} <- {M[mk]['bn']} | {M[mk]['n']}")
    elif c['src'] in ('late-picks-nov03', 'santababy-yes'):  # her album card racks for this pair (fills a rack an earlier run missed)
        e_ = next(e for e in s['m'] if e[0] == mk); e_[1].extend(r for r in racks if r not in e_[1])
    if s['slug'] in LK['sets']: LK['sets'][s['slug']]['m'] = s['m']
    if c['src'] == 'santababy-yes':
        L = SY.setdefault(s['slug'], [])
        if mk not in L: L.append(mk)
# 2
k = 'www.ohmymahjong.com/esme-mat-w-tube'
if k in M and not M[k].get('rt'):
    M[k].update(rt=True, n='Esme (retired)', u='https://www.ohmymahjong.com/collections/mahjong-mats'); log.append('Esme retired')
if k in LK['mats']: LK['mats'][k].update(rt=True, n='Esme (retired)')
# 3
t = T.get('tigredetartan.com/house-tigers-mahjong-tile-set-oyster')
if t and (t.get('oos') or t.get('so')): t.pop('oos', None); t.pop('so', None); log.append('House Tigers Oyster in stock')
# 4
k = 'letsbebesties.com/camellia-kaleidoscope-ohbon-studios-artist-mahjong-mat'
if k in M and not M[k].get('altu'):
    M[k].update(alt='Also available in leatherette', altu='https://letsbebesties.com/products/camellia-kaleidoscope-artist-collab-leatherette-mahjong-mat?sca_ref=12515508.SUyXEjJsqV')
    log.append('Camellia Kaleidoscope: also in leatherette')
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]; open(P, 'w').write(h)
json.dump(LK, open(REPO + 'builder/fym_flags/locks.json', 'w'), indent=1, ensure_ascii=False)
json.dump(SY, open(SYP, 'w'), indent=1, ensure_ascii=False)
for l in log: print(l)
print('misc115:', len(log), 'changes; unresolved', miss)
