"""FYM v93 (Tiffany Oct 26 12:36am: keep the 6 Mahjong by SI mats, "are they just linked incorrectly?"): yes. They came into
the catalog from mahjongco.com product pages that no longer exist (404). The same products live on Mahjong by SI's own
store under the same handles, so the shop links now go there (non-partner: no code, no commission). Version label -> 93.
Usage: v93_mahjongbysi.py <build>"""
import sys, json
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i; n = 0
for k, m in D['mats'].items():
    if m.get('b') == 'Mahjong by SI' and 'mahjongco.com/products/' in m.get('u', ''):
        m['u'] = 'https://www.mahjongbysi.com/products/' + m['u'].split('/products/')[1]; n += 1
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
h = h.replace('Version 92', 'Version 93'); open(P, 'w').write(h); print('relinked', n)
