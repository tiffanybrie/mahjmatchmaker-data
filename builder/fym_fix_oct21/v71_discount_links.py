"""FYM v71: auto-applied code links for Shopify partner stores (coordinator ask from Tiffany, Oct 21 evening).
Usage: python3 builder/fym_fix_oct21/v71_discount_links.py <build_dir>
A link https://<host>/discount/<CODE>?redirect=<url-encoded /products/<handle>?<affiliate query>> sets Shopify's discount_code cookie
and 302s to the product page with the affiliate parameter intact (sca_ref = UpPromote, ref = GoAffPro), so the code applies at
checkout and the referral still tracks (both apps also credit the coupon code itself).
Verified Oct 21 with curl (builder/fym_fix_oct21/discount_check_oct21.json): per brand, a sample product was added to a cart, the
discount URL visited, and /cart.js showed the code `applicable: true` with a real discount. Only those brands convert.
NOT converted: brands where the code was not applicable on any sampled product (Britt Mills, Mahjong Register, Yellow Mountain
Imports' own code), stores whose product .js did not answer (Royal Mahjong Society, Hip Hip Mahjong), non-Shopify stores
(Squarespace: Soiree, Amanda Toppe, Wren; Etsy; ShopMy), and no-code items (nc). Idempotent; original link kept in `u0`."""
import sys, os, json, urllib.parse
B = sys.argv[1]; P = os.path.join(B, 'index.html')
HERE = os.path.dirname(os.path.abspath(__file__))
CHK = json.load(open(os.path.join(HERE, 'discount_check_oct21.json')))
OK = {r['domain']: r['host'] for r in CHK if r.get('ok')}
h = open(P).read(); i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
cnt = {}
for kind in ('mats', 'tiles', 'racks'):
    for k, o in D[kind].items():
        u = o.get('u', '')
        if not o.get('pa') or o.get('nc') or '/discount/' in u or '/products/' not in u: continue
        p = urllib.parse.urlparse(u)
        if p.netloc not in OK: continue
        code = o.get('code') or 'MAHJMATCH'
        red = p.path + ('?' + p.query if p.query else '')
        o['u0'] = u
        o['u'] = f"https://{OK[p.netloc]}/discount/{urllib.parse.quote(code, safe='')}?redirect=" + urllib.parse.quote(red, safe='')
        cnt[p.netloc] = cnt.get(p.netloc, 0) + 1
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
open(P, 'w').write(h)
for d, n in sorted(cnt.items(), key=lambda x: -x[1]): print(f'{n:4d} {d}')
print('converted', sum(cnt.values()), 'links across', len(cnt), 'brands')
