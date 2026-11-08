"""FYM 1.18 small data fixes (Nov 7 2026). Idempotent. Usage: python3 builder/fym_fix_nov07/fixes118.py <build dir>
1. MATCH-INBOX 'ShopMy-sync fork' (Nov 7):
   (1) LoveShackFancy Fleur -> her ShopMy pin https://go.shopmy.us/p-96227058 (was the plain, non-earning LSF link). APPLIED.
   (2) Mahj & Moon Vintage Garden Floral -> p-98067023: NOT applied. That pin goes to Etsy listing 4371281339, which the Oct 31 by-eye
       pairing (config/mahj-moon-shopmy-links.json) already matched to Vintage Floral Gingham (FYM links it via p-99653834); the pin's
       title 'Vintage Floral Garden' is the Etsy title. Etsy answers 403 to the build, so it could not be looked at: left as is.
2. Gate [103]: Deco (Lagoon) / Deco (Mulberry) card titles = the tile BACK colour of their Nov 7 colour cards (config/colorcards.json:
   Lagoon #0a4f5c, Mulberry #7d3456). The Oct 23 add (bambird_tiles.py) had picked #0d6b6e / #a3195b by guess.
3. Gate [100]: the two Mac + Miller 'Perfectly Imperfect' listings (seconds of Laissez Les Bons Temps Rouler and Sweet Dreams, both
   already in FYM; Sweet Dreams is hidden + locked there) go on config/partner-mat-sweep-ignore.json with that reason."""
import sys, os, json, datetime, re
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
P = sys.argv[1] + '/index.html'; h = open(P).read(); i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:])
M = D['mats']; out = []
k = 'www.loveshackfancy.com/pink-floral-designer-mahjong-mat'
if k in M and M[k].get('u') != 'https://go.shopmy.us/p-96227058':
    M[k]['u'] = M[k]['u0'] = 'https://go.shopmy.us/p-96227058'; M[k]['dc'] = ''; M[k].pop('u_plain', None); out.append('LSF Fleur -> ShopMy p-96227058')
# 4. Ozark Mahjongg (Tiffany Nov 7 10:45pm): the store is https://www.ozarkmahjongg.com (two g; Wix /product-page/<slug>), not the
#    ozarkmahjong.com links we had. Non-partner whole-line allow: plain link, no code claim. All four answer 200 (Nov 7).
OZ = {'ozarkmahjong.com/winslow-1920-noir-mat': 'winslow-1920-noir-mat', 'ozarkmahjong.com/winslow-1920-original-navy-blue-mat': 'winslow-1920-original-navy-blue-mat',
      'ozarkmahjong.com/winslow-1920-rouge-mat': 'winslow-1920-rouge-mat', 'alb2:ozark-mah-jongg-carson-vintage': 'carson-vintage-mat'}
for k, sl in OZ.items():
    u = f'https://www.ozarkmahjongg.com/product-page/{sl}'
    if k in M and M[k].get('u') != u:
        M[k]['u'] = M[k]['u0'] = u; M[k]['dc'] = ''; M[k]['pa'] = False; M[k].pop('u_dead', None); M[k].pop('u_plain', None); out.append(f'Ozark {M[k]["n"]} -> {u}')
# 5. Album links for albums that went live (Juniper LIVE Nov 8 ~12:45am, MATCH-INBOX)
for slug, url in {'juniper': 'https://www.mahjmatchmaker.com/juniper-mahjong-tile-matches'}.items():
    for s in D['sets']:
        if s['slug'] == slug and s.get('album') != url: s['album'] = url; out.append(f'{slug} album -> {url}')
CC = json.load(open(R + 'config/colorcards.json'))['sets']
# gate [103] rule, for every colour card (Nov 7: new cards keep arriving, e.g. Deco (Indigo)): no album title colour -> the card's
# first back colour (or its title colour for an all-ivory back)
_am = re.search(r'const tc=.*?\(\(\)=>\{const h=\((\{[^}]*\})\)\[s\.name\]', h); _alb = set(json.loads(_am.group(1))) if _am else set()
_lum = lambda x: sum(w * int(x[i_:i_ + 2], 16) / 255 for w, i_ in ((.2126, 1), (.7152, 3), (.0722, 5)))
for card, v in CC.items():
    nm = {'Sunday Tile Set': 'Sunday'}.get(v['name'], v['name'])
    if nm in _alb: continue
    b0 = v['backs'][0][1]; want = b0 if _lum(b0) < 0.6 else v.get('col')
    for s in D['sets']:
        if want and s['name'] == nm and (s.get('maker') == v.get('brand') or not v.get('brand')) and (s.get('tc') or '').lower() != want.lower():
            out.append(f"{nm} tc {s.get('tc')} -> {want}"); s['tc'] = want
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[i + e:]; open(P, 'w').write(h)
IG = json.load(open(R + 'config/partner-mat-sweep-ignore.json')); today = datetime.date.today().isoformat(); n = 0
for key, name, base in (('macandmillermahjong.com/laissez-les-bons-temps-rouler-collection-mahjong-mat-perfectly-imperfect',
                         'Perfectly Imperfect Laissez Les Bons Temps Rouler Collection Mahjong Mat', 'Laissez Les Bons Temps Rouler'),
                        ('macandmillermahjong.com/sweet-dreams-collection-mahjong-mat-copy', 'Perfectly Imperfect Sweet Dreams Collection Mahjong Mat', 'Sweet Dreams (hidden + locked in FYM)')):
    if key not in IG['items']:
        IG['items'][key] = {'name': name, 'reason': f"'Perfectly Imperfect' = a seconds/sale listing of {base}, a design already in FYM (not a new mat)", 'added': today}; n += 1
if n: json.dump(IG, open(R + 'config/partner-mat-sweep-ignore.json', 'w'), indent=1, ensure_ascii=False)
print('fixes118:', out, '| sweep-ignore added', n)
