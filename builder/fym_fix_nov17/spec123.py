"""FYM 1.23 spec (Nov 17): the 233 photo-checked new items (224 pass + 9 cropped; 68 already in the app removed) from the staged partner
adds (config/fym-partner-adds-nov08/nov10/nov16, nov12-coverage, catalog-adds-nov08-lagoon, adds-nov10-cabana). Review page:
builder/fym_flags/fym123_photo_check.json. Writes config/fym-adds-nov17-v123.json, read by adds123.py.
Links copy each brand's live route in v122 (affiliate ref + MAHJMATCH auto-apply). Table view class decided by eye per photo (contact
sheets Nov 17): flat product renders = A; Mahjong Register fold-over corner photos and Maison Mahj room/angled shots = C with a reason.
Tile backs: confirmed from listing photos only (Noli June Holiday Soiree red, Breezy Blue periwinkle); Luxe Lilac HELD (not added).
Usage: python3 spec123.py <prev dir>"""
import sys, json, re, os
PV = sys.argv[1]; R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
items = json.load(open(PV + '/items.json')); V = json.load(open(PV + '/verdicts.json')); PR = json.load(open(PV + '/prices.json'))
BK = json.load(open(PV + '/backs123.json'))['confirmed']
go = [x for x in V if x['verdict'] in ('pass', 'crop')]
DC = lambda s: f'https://mahjmatchmaker.com/{s}-discount-code'
def route(b, h, it):
    q = lambda r: '%2Fproducts%2F' + h + r
    if b == "Let's Be Besties": return (f'https://letsbebesties.com/discount/MAHJMATCH?redirect={q("%3Fsca_ref%3D12515508.SUyXEjJsqV")}', f'https://letsbebesties.com/products/{h}?sca_ref=12515508.SUyXEjJsqV', DC('lets-be-besties'), True)
    if b == 'Britt Mills': return (f'https://brittmillsdesign.com/discount/MAHJMATCH?redirect={q("%3Fsca_ref%3D11205153.24gc8ncLZw3")}', f'https://brittmillsdesign.com/products/{h}', DC('britt-mills'), True)
    if b == 'Mahjong Register': return (f'https://mahjongregister.com/discount/MAHJMATCH?redirect={q("")}', None, 'https://www.mahjmatchmaker.com/mahjong-register-discount-code', True)
    if b == 'Mahjong Row & Co.': return (f'https://mahjongrowandco.com/discount/MAHJMATCH?redirect={q("%3Fsca_ref%3D12475363.JLitn0fWe79Xnn")}', f'https://mahjongrowandco.com/products/{h}?sca_ref=12475363.JLitn0fWe79Xnn', DC('mahjong-row-and-co'), True)
    if b == 'YOLO Mahjong': return (f'https://www.yolomahjong.com/discount/MAHJMATCH?redirect={q("%3Fsca_ref%3D12572562.5IBLjBHZ1vuX4J")}', f'https://www.yolomahjong.com/products/{h}?sca_ref=12572562.5IBLjBHZ1vuX4J', DC('yolo-mahjong'), True)
    if b == 'Mahj Mood': return (f'https://mahjmood.com/discount/MAHJMATCH?redirect={q("%3Fref%3DMahjmatchmaker")}', f'https://mahjmood.com/products/{h}', DC('mahj-mood'), True)
    if b == 'Miss Mahjong': return (f'https://missmahjong.com/discount/MAHJMATCH?redirect={q("%3Fref%3Dmahjmatch")}', f'https://missmahjong.com/products/{h}?ref=mahjmatch', DC('miss-mahjong'), True)
    if b == 'Noli June': return (f'https://nolijune.com/discount/MAHJMATCH?dt_id=3655694&redirect={q("")}', f'https://nolijune.com/products/{h}', DC('noli-june'), True)
    if b == 'Splash of Color': return (it['u'], f'https://splashofcolorco.com/products/{h}', DC('splash-of-color'), True)
    if b == 'Soirée All Day': return (it['u'], None, DC('soiree-all-day'), True)
    if b == 'Wren Mats': return (it['u'], None, DC('wren-mats'), True)
    if b in ('Maison Mahj', 'Silk Mahjong'): return (it['u'], None, '', False)
    raise SystemExit('no route for ' + b)
RATIO = {"Let's Be Besties": (1, 0), 'Britt Mills': (.85, 1), 'Mahjong Register': (1, 0), 'Mahjong Row & Co.': (.9, 1), 'Maison Mahj': (1, 0),
         'Noli June': (1, 0), 'Silk Mahjong': (1, 0), 'Soirée All Day': (1, 0), 'Splash of Color': (.9, 1), 'Wren Mats': (.9, 1),
         'YOLO Mahjong': (.9, 1), 'Mahj Mood': (.9, 1), 'Miss Mahjong': (.9, 1), 'Charleston Mahjong Club': (.9, 1)}
ART = r'\s+(?:by\s+Charmaine J\.W\.|Lillian Claire Designs|OHBoN Studios|BeachyMahj|BeachMahj|STM|AC Studios|Wanda Viola|Bam Bird Andy Albert Artist Collective|Andy Albert Artist Collective)(?=\s|$)'
def clean(n, b, KEY=''):
    n = re.sub(r'\s+', ' ', n).strip()
    n = re.sub(r'\s*\((?:Shipped Rolled Up|Ship Rolled up)\)', '', n, flags=re.I)
    n = re.sub(r'\s*\d+(?:\.\d+)?"\s*x\s*\d+(?:\.\d+)?"', '', n)
    n = re.sub(r'\s+–\s+Neoprene 33"', ' Neoprene', n)
    n = re.sub(r'\s+Mahjong Mats?\b', '', n); n = re.sub(ART + r'.*$', '', n); n = re.sub(r'\s+Artist$', '', n)
    if b == 'Mahjong Register': n = n.replace('Double-Sided Mahjong Mat', 'Double-Sided').replace('Double-Sided Neoprene', 'Double-Sided Neoprene')
    if b == 'Wren Mats': n = re.sub(r'\s+Mat$', '', n)
    if n == 'Year of the Horse' and 'wanda-viola' in KEY: n = 'Year of the Horse (Wanda Viola)'  # live LBB already has a different 'Year of the Horse'
    return n.strip()
TILE = {290: ('Playing For Keeps', 'mahj-mood-playing-for-keeps', 'Purple', {'pre': 1}),
        292: ('Miss Darling (Lilac)', 'miss-mahjong-miss-darling-lilac', 'Purple', {}),
        296: ('Holiday Soirée', 'noli-june-holiday-soiree', 'Holiday', {}),
        297: ('Best In Show (Pink)', 'noli-june-best-in-show-pink', 'Pink', {}),
        298: ('Chinoiserie Polished Pink', 'noli-june-chinoiserie-polished-pink', 'Pink', {}),
        299: ('Chinoiserie Breezy Blue', 'noli-june-chinoiserie-breezy-blue', 'Blue', {})}
C_WHY = {273: 'its photo shows the mat folded over to show both sides.', 274: 'its photo shows the mat folded over to show both sides.',
         275: 'its photo shows the mat folded over to show both sides.', 276: 'its photo shows the mat folded over to show both sides.',
         277: 'no flat, top-down photo of this mat yet.', 278: 'no flat, top-down photo of this mat yet.',
         279: 'its photo has its own colored racks on it.', 280: 'no flat, top-down photo of this mat yet.'}
def tc_of(hx):  # card title colour: the set's back colour, deepened when pale (white-ish titles do not read)
    import colorsys
    r, g, b = (int(hx[k:k + 2], 16) / 255 for k in (1, 3, 5)); hh, l, s = colorsys.rgb_to_hls(r, g, b)
    if l > .55: l = .45; s = min(1, s * 1.25)
    r, g, b = colorsys.hls_to_rgb(hh, l, s); return '#%02x%02x%02x' % tuple(round(v * 255) for v in (r, g, b))
mats, tiles, held = [], [], []
for x in go:
    i = x['i']; it = items[i]; b = it['brand']; h = it['key'].split('/', 1)[1]
    price = PR['prices'].get(str(i)); price = price if price is not None else float(str(it['price']).replace('$', ''))
    lo, fl = RATIO[b]; pm = [float(price), round(price * lo, 2), fl]
    if it['kind'] == 'tile':
        if i == 0:
            cb = json.load(open(R + 'config/fym-adds-nov10-cabana.json'))['tiles'][0]
            tiles.append(dict(i=0, key=cb['key'], slug=cb['slug'], name=cb['name'], bn=b, u=cb['u_fallback'], u0=cb['u0'], dc=cb['dc'], pa=True, img=cb['img'],
                              tc=cb['tc'], group=cb['group'], back={'b': cb['back']['hex'], 'patch': cb['back']['patch']}, pt=pm, oos=0, hol=False, note='ShopMy pin pending: MAHJMATCH code link'))
            continue
        if i not in TILE: held.append((i, b, it['name'], 'back colour not confirmed')); continue
        nm, slug, grp, extra = TILE[i]; u, u0, dc, pa = route(b, h, it); bk = BK[str(i)]
        tiles.append(dict(i=i, key=it['key'], slug=slug, name=nm, bn=b, u=u, u0=u0, dc=dc, pa=pa, img=it['img'], tc=tc_of(bk), group=grp,
                          back={'b': bk}, pt=pm, oos=0, hol=grp == 'Holiday', **extra))
        continue
    u, u0, dc, pa = (route(b, handle, it) if (handle := h) else None)
    if b in ("Let's Be Besties",) or b == 'Britt Mills':
        hs = dict(json.load(open(PV + '/handles.json'))).get('letsbebesties.com' if b != 'Britt Mills' else 'brittmillsdesign.com', [])
        hd = dict((a, c) for a, c in hs).get(i)
        if hd: u, u0, dc, pa = route(b, hd, it)
    cls = 'C' if i in C_WHY else 'A'
    mats.append(dict(i=i, key=it['key'], name=clean(it['name'], b, it['key']), bn=b, u=u, u0=u0, dc=dc, pa=pa, img=it['img'], box=x.get('box'),
                     hol=bool(it['hol']), oos=1 if i in PR['soldout'] else 0, pm=pm, cls=cls, why=C_WHY.get(i, '')))
held += [(300, 'Noli June', 'THE CHINOISERIE SET - LUXE LILAC', 'back colour not confirmed: listing photos show only blurred, pink-lit face-down tiles')]
held = [h_ for h_ in held if h_[0] != 300] + [held[-1]]
out = {'_about': __doc__.split('\n')[0] + ' ' + 'Generated by builder/fym_fix_nov17/spec123.py.', 'made': '2026-11-17', 'mats': mats, 'tiles': tiles,
       'held': [dict(i=a, brand=b, name=c, why=d) for a, b, c, d in held]}
json.dump(out, open(R + 'config/fym-adds-nov17-v123.json', 'w'), indent=1, ensure_ascii=False)
print(len(mats), 'mats', len(tiles), 'tiles', 'held', out['held'])
