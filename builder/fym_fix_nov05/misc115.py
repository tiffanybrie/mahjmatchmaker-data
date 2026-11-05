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
# 5. Bespoke double-sided mats: side B right after side A in every rank / cr (gate [78]; the v115 re-rank moved some)
OI = {m: j for j, m in enumerate(D['order'])}
pairs = [(OI[k.split('#')[0]], OI[k]) for k in M if k.endswith('#side-b') and k.split('#')[0] in OI]
for s in sets:
    for fld in ('rank', 'cr'):
        L = s.get(fld)
        if not L: continue
        for ja, jb in pairs:
            if ja in L and jb in L and L.index(jb) != L.index(ja) + 1: L.remove(jb); L.insert(L.index(ja) + 1, jb)
# 6. Etsy / ShopMy (non-partner) adds say 'No code available at this time' like every other non-partner (gate [137d])
for k, o in M.items():
    if o.get('add') == 'nov03-etsy' and not o.get('pa') and not o.get('ncn'): o['ncn'] = 1
# 7. Koi Flower Pond (Luna EK Studio): its 'yellow' measures cream (gate [120]) -> neutral
k = 'www.etsy.com/listing/4573770797/mahjong-mat-non-slip-tabletop-mat-home'
if k in M and 'yellow' in M[k].get('mf', []): M[k].update(mf=['neutral', 'green'], mt=[0, 1], sh=[66.4, 19.2])
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
# 8. Mahj Pit logo on the opening screen (gate [105]; assets/brand/partner-logos/mahj-pit.png)
mb = re.search(r'const BLOGO=(\{.*?\});const BLORD=(\[.*?\]);', h); BL, BO = json.loads(mb.group(1)), json.loads(mb.group(2))
if 'Mahj Pit' not in BL:
    import io, base64
    from PIL import Image
    im = Image.open(REPO + 'assets/brand/partner-logos/mahj-pit.png').convert('RGBA'); im.thumbnail((263, 150)); bb = io.BytesIO(); im.save(bb, 'WEBP', quality=86)
    BL['Mahj Pit'] = 'data:image/webp;base64,' + base64.b64encode(bb.getvalue()).decode()
    BO.insert(BO.index('Splash of Color') + 1 if 'Splash of Color' in BO else len(BO), 'Mahj Pit')
    h = h.replace(mb.group(0), 'const BLOGO=' + json.dumps(BL, ensure_ascii=False) + ';const BLORD=' + json.dumps(BO, ensure_ascii=False) + ';', 1); log.append('Mahj Pit logo')
open(P, 'w').write(h)
# 9. stock records for the new items (sold out per the brand store Nov 4-5) + Esme retired = not in stock (gate [138])
STP = REPO + 'config/fym-stock.json'; ST = json.load(open(STP)); SPEC = json.load(open(REPO + 'config/fym-adds-nov05.json'))
for kd, L_ in (('m', SPEC['mats']), ('t', SPEC['tiles'])):
    for x in L_: ST['items'][f"{kd}:{x['key']}"] = {'in': not x.get('oos'), 'how': 'v115 add (brand store Nov 4-5)', **({'price': x['price']} if x.get('price') else {})}
ST['items']['m:www.ohmymahjong.com/esme-mat-w-tube'] = {'in': False, 'how': 'retired: gone from ohmymahjong.com Nov 4'}
ST['items']['t:tigredetartan.com/house-tigers-mahjong-tile-set-oyster'] = {'in': True, 'how': 'store check Nov 3 6:40pm ET (available, $295)', 'price': 295.0}
json.dump(ST, open(STP, 'w'), indent=0, ensure_ascii=False)
json.dump(LK, open(REPO + 'builder/fym_flags/locks.json', 'w'), indent=1, ensure_ascii=False)
json.dump(SY, open(SYP, 'w'), indent=1, ensure_ascii=False)
for l in log: print(l)
print('misc115:', len(log), 'changes; unresolved', miss)
