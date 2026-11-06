"""Sunday Sets albums (Nature Walk, Sunday Blues, Plum Panda, Hummingbird), DRAFT match cards from Tiffany's EXISTING
swipe-book yeses (Sunday Sets book WJT7jTYfXX45917UkEqKyq, db `sundaysets`, votes read Nov 6 2026).
Same pipeline as Juniper (juniper_build.py -> gen2.py, card2.html layout).
- One card per YES (a yes is a yes). Order (draft): TNT recs first (book order), then Sunday Mahjong's own mats, then the
  rest in book order (colour score order).
- Britt Mills neoprene + leatherette twins of one design -> ONE card with a caption note (her Oct 15 Sunday Tile Set rule).
- Holiday yeses (book gate barred them from the deck) are NOT year-round cards: listed in manifest 'holiday_yes' for the
  holiday section. Festive Plaid is also_year_round (late-calls), so it gets a year-round card where she said yes.
- Tile racks (MATCH THE TILES): Peace Love Mahjong only, same shape on every card (Tiffany Nov 6 2:11am: never mix rack
  shapes that lie differently). Sunday's own rack (Cola) has a render only, no real photo (racks.py: real photos only).
- Mat racks (MATCH THE MAT): config/mat-racks-picks.json registry when the mat is listed, else matpick (2 B&B colours).
- Code band: 10% floor, 'SAVE WITH CODE' for the no-% brands (Juniper rule). Title colour = colour-card colour.
Usage: python3 sunday_sets_build.py <workdir> <book.json> <mats.json> <imgroot>; then gen2.py <workdir>/<set>/spec.json <out>"""
import json, io, base64, re, os, sys
from PIL import Image
sys.path.insert(0, '/home/claude/mahjmatchmaker-data/scripts/albumcard')
from matpick import pick
R = '/home/claude/mahjmatchmaker-data/'
W, BOOK, MATS, IMG = sys.argv[1:5]
B = json.load(open(BOOK)); M = json.load(open(MATS))
CCS = json.load(open(R + 'config/colorcards.json'))['sets']
REG = {k: v for k, v in json.load(open(R + 'config/mat-racks-picks.json')).items() if isinstance(v, dict)}
NOPCT = {'Anders Ruff', 'Mahjong Register', 'The Mahjong Press'}
TRACKS = {'nature-walk': ['Peace Love Mahjong Acrylic Burl', 'Peace Love Mahjong Oak'],
          'sunday-blues': ['Peace Love Mahjong Navy', 'Peace Love Mahjong Oak'],
          'plum-panda': ['Peace Love Mahjong Dark Green', 'Peace Love Mahjong Acrylic Burl'],
          'hummingbird': ['Peace Love Mahjong Navy', 'Peace Love Mahjong Acrylic Burl']}
HOLIDAY_IDS = {'evergreen-tartan-mahjong-mat': ('Evergreen Tartan', 'Anders Ruff'), 'clara-mat-in-tube': ('Clara', 'Oh My Mahjong'),
               'heirloom-collection-white-chinoiserie-round-mahjong-mat': ('Heirloom Collection White Chinoiserie Round', 'Mahjong Register')}
DUP_IDS = {'c-rattan-premium-mahjong-mat', 'savannah-leatherette-mahjong-mat'}  # old ids of mats already voted yes (dropped.json 'dup')
FESTIVE = 'sundayma-festive-plaid-premium-mahjong-mat'
_pl = json.load(open(R + 'scripts/swipe/sunday_rebuild_oct29/plan.json'))['map']
PLAN = {k: (v if '/' in str(v) or ':' in str(v) else v) for k, v in _pl.items()}
def footer(b):
    return 'SAVE WITH CODE : MAHJMATCH' if b in NOPCT else '10% OFF  USE CODE : MAHJMATCH'
def flat(im):
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA'); bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[3]); return bg
    return im.convert('RGB')
def uri(im, maxs=1400):
    im = im.copy(); im.thumbnail((maxs, maxs)); b = io.BytesIO(); im.convert('RGB').save(b, 'JPEG', quality=90)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
def crop(im):  # Juniper/Papaya default framing: whole mat for small photos, 72% bottom-left zoom for big ones
    im = flat(im); Wd, H = im.size; z = .72 if Wd >= 900 else 1.0
    cw = int(Wd * z); ch = int(cw / .973)
    if ch > H: ch = H; cw = int(ch * .973)
    return im.crop((0, H - ch, cw, H))
BOX = json.load(open(R + 'scripts/albumcard/specs/sunday_sets_box.json'))  # by-eye crop fixes: id -> [l,t,r,b] or "full"
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower().replace('&', 'and').replace("'", '').replace('’', '').replace('–', '-')).strip('-')
def reg_for(name):
    k = slug(name)
    return (k, REG[k]['racks']) if k in REG else (None, None)
def parse(label):
    tnt = label.startswith('TNT rec · '); np_ = label.endswith(' · non-partner')
    l = label[len('TNT rec · '):] if tnt else label
    if np_: l = l[:-len(' · non-partner')]
    nm, brand = l.rsplit(' · ', 1)
    return nm.strip(), brand.strip(), tnt, np_
# Oct 18 (Tiffany): no bright painted racks (Carrot, Radish, Red) on moody / brown / burgundy / leather mats
MOODY = re.compile(r'leather|cognac|caramel|palomino|oxblood|rattan|saffron|brownstone|burgundy|crimson|mocha|harvest|dapper|domino|winslow|vintage|study|polo|hawthorne|astor|vanderbilt|fringe', re.I)
BRIGHT = ['Bird & Bamboo Carrot', 'Bird & Bamboo Radish', 'Bird & Bamboo Red', 'Bird & Bamboo Persimmon']
SHORT = {'Bespoke x Brooks Brothers Oxford Classic (Side A: Oxford Stripe)': 'Oxford Stripe',
         'Bespoke x Brooks Brothers Oxford Classic (Side B: Navy)': 'Oxford Classic Navy',
         "Let's Be Refined! – Refined Blue/Soft Blue Border": "Let's Be Refined Blue & Soft Blue",
         "Let's Be Refined! – Soft Blue": "Let's Be Refined Soft Blue", "Let's Be Refined! – Refined Blue": "Let's Be Refined Blue",
         'Bandana – Blue/Pink accents': 'Bandana Blue & Pink', 'Bandana – Olive Green/Dusty Lilac accents': 'Bandana Olive & Lilac',
         'MCM – Geo Bloom- Blue': 'MCM Geo Bloom Blue', 'Darjeeling Peacock Mat (Side A: Blue Scales)': 'Darjeeling Peacock Blue Scales',
         'Cannage Blonde (Blonde Caned)': 'Cannage Blonde', 'The Paradise - Island Green': 'The Paradise Island Green',
         'Year of the Dragon - Periwinkle': 'Year of the Dragon Periwinkle', 'YOTD Black': 'Year of the Dragon Black',
         'Vegan Leather – Cognac': 'Cognac Vegan Leather', 'Vegan Leather – Caramel': 'Caramel Vegan Leather',
         'Vegan Leather – Navy': 'Navy Vegan Leather', 'Vegan Leather – Slate Blue': 'Slate Blue Vegan Leather',
         'Midnight Wildflowers with Camel Fringe': 'Midnight Wildflowers'}
def clean(nm):
    nm = SHORT.get(nm, nm)
    nm = re.sub(r'\s*\((?:[^)]*,\s*)?retired\)', '', nm, flags=re.I)
    nm = re.sub(r'^Year of the Dragon Mat - ', 'Year of the Dragon ', nm)
    nm = nm.replace('Tigre de Tartán x Miss Mahjong: “El Último Refresco”', 'El Último Refresco')
    return nm.strip()
TWIN = re.compile(r'\s+(leatherette|neoprene)$', re.I)
summary = {}
for sid in ['nature-walk', 'sunday-blues', 'plum-panda', 'hummingbird']:
    CC = CCS[sid]; V = B['V'][sid]; items = B['items']
    yes = [i for i in B['order'][sid] if V.get(i, ('',))[0] == 'y']
    rows, hol = [], []
    for iid in yes:
        it = items[iid]; nm, brand, tnt, np_ = parse(it['label'])
        m = M.get(it.get('key')) or {}
        if brand == 'Tigre de Tartán': brand = 'Tigre de Tartan'
        if brand == 'Etsy' and m.get('bn'): brand = m['bn']
        rows.append(dict(id=iid, name=nm, brand=brand, tnt=tnt, nonpartner=np_, retired=bool(m.get('rt')) or 'retired' in nm.lower(),
                         img=IMG + it['img'], key=it.get('key'), hidden=bool(m.get('hid'))))
    yes_keys = {items[i].get('key') for i in yes}
    for iid, (v, *_ ) in V.items():
        if v != 'y' or iid in B['order'][sid] or iid in DUP_IDS: continue
        if f'tnt-{sid}-{iid}' in B['order'][sid]: continue  # same mat, now shown as the TNT rec item
        k = PLAN.get(iid)
        alt = next((j for j in B['order'][sid] if k and items[j].get('key') == k), None)
        if alt is not None and k in yes_keys: continue  # already a yes under its new id
        if alt is not None:  # her old-id yes; the rebuilt item has a new id and no vote -> still her yes
            it = items[alt]; nm, brand, tnt, np_ = parse(it['label']); m = M.get(k) or {}
            rows.append(dict(id=iid, name=nm, brand=brand, tnt=tnt, nonpartner=np_, retired=bool(m.get('rt')),
                             img=IMG + it['img'], key=k, hidden=bool(m.get('hid')), old_id=True)); yes_keys.add(k); continue
        if iid == FESTIVE: rows.append(dict(id=iid, name='Festive Plaid Premium', brand='Sunday Mahjong', tnt=False, nonpartner=False,
                                            retired=False, img=None, key='sundaymahjong.com/festive-plaid-premium-mahjong-mat', hidden=False, festive=True)); continue
        hol.append({'vote_id': iid, 'mat': HOLIDAY_IDS.get(iid, (iid, '?'))[0], 'brand': HOLIDAY_IDS.get(iid, (iid, '?'))[1]})
    # order: TNT recs, then Sunday Mahjong's own, then the rest (book order)
    rows = [r for r in rows if r['tnt']] + [r for r in rows if not r['tnt'] and r['brand'] == 'Sunday Mahjong'] + \
           [r for r in rows if not r['tnt'] and r['brand'] != 'Sunday Mahjong']
    # twins: Britt Mills (etc.) neoprene/leatherette of one design -> one card + note
    seen, keep = {}, []
    for r in rows:
        base = (r['brand'], TWIN.sub('', r['name']).lower())
        if base in seen:
            k = seen[base]; other = 'leatherette' if 'leatherette' in r['name'].lower() else 'neoprene'
            k['note'] = f'Also available in {other}'; k.setdefault('twins', []).append(r['id']); continue
        seen[base] = r; keep.append(r)
    TR = TRACKS[sid]; cards, man = [], []
    # tile photo as a data URI: assets/tiles/album/index.json lists hummingbird.png as a LOOSE pile (pre-Oct 29 cut-out),
    # which draws the new fill-frame photo across the whole card. Same pixels gen2 would use (RGB, 900px, q88).
    _t = Image.open(R + CC['tile']).convert('RGB'); _t.thumbnail((900, 900)); _b = io.BytesIO(); _t.save(_b, 'JPEG', quality=88)
    TILE = 'data:image/jpeg;base64,' + base64.b64encode(_b.getvalue()).decode()
    for r in keep:
        if r['brand'] == 'Britt Mills' and r['name'] == 'Calista Neoprene' and not r.get('note'):
            r['note'] = 'Also available in leatherette (Calista Leatherette, added to the catalog Nov 1)'
        if r.get('festive'):
            k = 'sundaymahjong.com/festive-plaid-premium-mahjong-mat'
            r['img'] = R + 'assets/mats/holiday/hd/sunday-festive-plaid.jpg'; src = Image.open(r['img'])
        else:
            src = Image.open(r['img'])
        if src is None: man.append({'mat': r['name'], 'brand': r['brand'], 'skipped': 'no photo'}); continue
        b = BOX.get(r['id'])
        if b == 'center':  # round-cornered product shot on black: frame the middle of the mat
            f = flat(src); s = int(min(f.size) * .66); x0, y0 = (f.width - s) // 2, (f.height - s) // 2; m = f.crop((x0, y0, x0 + s, y0 + s))
        else:
            m = flat(src) if b == 'full' else (flat(src).crop(tuple(b)) if b else crop(src))
        nm = clean(r['name'] if r['brand'] != 'Britt Mills' else TWIN.sub('', r['name']))
        rk, mr = reg_for(nm)
        mr = [l for l in (mr or []) if l not in TR]
        bad = BRIGHT if MOODY.search(nm) else []
        if len(mr) < 2:
            for l in pick(m, exclude=TR + mr + bad):
                if l not in mr and l not in bad and len(mr) < 2: mr.append(l)
        fn = f"{sid}-mahjong-tiles-{slug(r['brand'])}-{slug(nm)}-mat.jpg"
        n = len(cards) + 1; code = footer(r['brand'])
        cards.append({'slug': f"{sid[:2]}{n:02d}", 'title': f"{CC['name']} + {re.sub(r' (Premium)$', '', nm)}", 'col': CC['col'],
                      'tile_file': TILE, 'tilefit': 'cover', 'racks': TR, 'mat_racks': mr, 'file': fn, 'code': code, 'mat': uri(m)})
        man.append({'order': n, 'vote_id': r['id'], 'mat': nm, 'mat_full': r['name'], 'brand': r['brand'], 'tnt_rec': r['tnt'], 'non_partner_tnt': r['nonpartner'],
                    'retired_mat': r['retired'], 'file': fn, 'code': code, 'src': r['img'] or 'festive.jpg', 'fym_key': r['key'],
                    'racks': TR, 'mat_racks': mr, 'mat_reg': rk, 'caption_note': r.get('note'), 'twins_merged': r.get('twins', []),
                    'flag': ('Paige Spearin x TdT: no commission (CLAUDE.md 6.4); her yes, kept' if 'paige' in (r['key'] or '') else None)})
    os.makedirs(W + '/' + sid, exist_ok=True)
    json.dump({'_note': f"{CC['name']} album DRAFT (Nov 6) from her Sunday Sets swipe-book yeses", 'cards': cards, 'max_racks': 4,
               'tile_brand': 'Sunday Mahjong'}, open(W + f'/{sid}/spec.json', 'w'))
    json.dump({'set': CC['name'], 'status': 'DRAFT: her swipe-book yeses, Claude draft order + racks', 'title_color': CC['col'],
               'tile': CC['tile'], 'tile_racks': TR, 'cards': man, 'holiday_yes': hol,
               'racks_note': 'tile racks = PLM only (same shape); mat racks = registry or matpick'},
              open(W + f'/{sid}/manifest.json', 'w'), indent=1, ensure_ascii=False)
    summary[sid] = {'yes_votes': len(yes) + sum(1 for i, (v, *_) in V.items() if v == 'y' and i not in B['order'][sid]),
                    'cards': len(cards), 'holiday_yes': [h['mat'] for h in hol],
                    'merged': [(r['name'], r.get('twins')) for r in keep if r.get('twins')]}
print(json.dumps(summary, indent=1))
