"""FYM 1.22.12: the 6 Mahjong by SI mats that came in before the code was confirmed carry plain links (QA note on 1.22.11).
Give them the code link (code-truth: MAHJMATCH confirmed Nov 11), pa True and the brand's code page, like the 3 added in 1.22.11.
Usage: python3 si_codelinks12212.py <build dir>"""
import sys, json, urllib.parse
P = sys.argv[1] + '/index.html'; h = open(P).read(); i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
n = 0
for k, m in D['mats'].items():
    u = m.get('u', '')
    if m.get('bn') == 'Mahjong by SI' and u.startswith('https://www.mahjongbysi.com/products/'):
        path = u.split('mahjongbysi.com', 1)[1]
        m['u0'] = u; m['u'] = 'https://www.mahjongbysi.com/discount/MAHJMATCH?redirect=' + urllib.parse.quote(path, safe='')
        m['pa'] = True; m['nc'] = False; m['dc'] = 'https://www.mahjmatchmaker.com/mahjong-by-si-discount-code'; n += 1
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]; open(P, 'w').write(h); print('code links set on', n, 'Mahjong by SI mats')
