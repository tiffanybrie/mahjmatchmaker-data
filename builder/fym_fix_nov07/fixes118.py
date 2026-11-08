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
import sys, os, json, datetime
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
P = sys.argv[1] + '/index.html'; h = open(P).read(); i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:])
M = D['mats']; out = []
k = 'www.loveshackfancy.com/pink-floral-designer-mahjong-mat'
if k in M and M[k].get('u') != 'https://go.shopmy.us/p-96227058':
    M[k]['u'] = M[k]['u0'] = 'https://go.shopmy.us/p-96227058'; M[k]['dc'] = ''; M[k].pop('u_plain', None); out.append('LSF Fleur -> ShopMy p-96227058')
CC = json.load(open(R + 'config/colorcards.json'))['sets']
for card, nm in (('deco-lagoon', 'Deco (Lagoon)'), ('deco-mulberry', 'Deco (Mulberry)')):
    want = CC[card]['backs'][0][1]
    for s in D['sets']:
        if s['name'] == nm and s.get('tc', '').lower() != want.lower(): out.append(f"{nm} tc {s.get('tc')} -> {want}"); s['tc'] = want
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[i + e:]; open(P, 'w').write(h)
IG = json.load(open(R + 'config/partner-mat-sweep-ignore.json')); today = datetime.date.today().isoformat(); n = 0
for key, name, base in (('macandmillermahjong.com/laissez-les-bons-temps-rouler-collection-mahjong-mat-perfectly-imperfect',
                         'Perfectly Imperfect Laissez Les Bons Temps Rouler Collection Mahjong Mat', 'Laissez Les Bons Temps Rouler'),
                        ('macandmillermahjong.com/sweet-dreams-collection-mahjong-mat-copy', 'Perfectly Imperfect Sweet Dreams Collection Mahjong Mat', 'Sweet Dreams (hidden + locked in FYM)')):
    if key not in IG['items']:
        IG['items'][key] = {'name': name, 'reason': f"'Perfectly Imperfect' = a seconds/sale listing of {base}, a design already in FYM (not a new mat)", 'added': today}; n += 1
if n: json.dump(IG, open(R + 'config/partner-mat-sweep-ignore.json', 'w'), indent=1, ensure_ascii=False)
print('fixes118:', out, '| sweep-ignore added', n)
