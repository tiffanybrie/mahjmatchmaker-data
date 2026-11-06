"""FYM 1.16: MATCH-INBOX build items that need no taste decision (standing authority: broken link fixes, catalog adds that pass gates).
 1. LBB handle changes (inbox Nov 1 + Nov 2): the old product URLs now 301 to new handles; links point straight at the new handle
    (keys unchanged; auto-apply form + sca_ref kept): Flutter for a Cause, Save the TaTas, Purple Royal Peacock, Royal Peacock,
    Green Apres Skiing with Skiers, Aggies Game Day, Vibrant Vortex Simple Middle (now 'Open Middle').
 2. TdT Domino Blonde (inbox Nov 2): its rules-printed material version becomes the card's second shop link
    ('Also available with rules printed'), like the Britt Mills / LBB material twins. TdT is link-only (no code text).
 3. Britt Mills Merrywood + Nutcracker NEOPRENE sold out (inbox Nov 1 stock pass; re-checked brittmillsdesign.com .js Nov 6:
    available false): Sold out badge (their leatherette twins stay in stock).
 4. Brownstone Bloom album is live (inbox Nov 1; /brownstone-bloom-mahjong-tile-matches): the set's album link.
Idempotent. Usage: python3 inbox116.py <build dir>"""
import sys, os, json
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read(); i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:])
M = D['mats']; log = []
LBB = {'letsbebesties.com/flutter-for-a-cause-mahjong-mat-charity-donation-included': ('flutter-for-a-cause-mahjong-mat-charity-donation-included', 'flutter-for-a-cause-mahjong-mat'),
       'letsbebesties.com/save-the-tatas-charity-donation-included-neoprene-mahjong-mat': ('save-the-tatas-charity-donation-included-neoprene-mahjong-mat', 'save-the-tatas-mahjong-mat'),
       'letsbebesties.com/royal-peacock-mahjong-mat': ('royal-peacock-mahjong-mat', 'royal-purple-peacock-mahjong-mat'),
       'letsbebesties.com/royal-peacock-mahjong-mat-2': ('royal-peacock-mahjong-mat-2', 'royal-blue-peacock-mahjong-mat'),
       'letsbebesties.com/green-apres-skiing-in-teal-with-skiers-mahjong-mat': ('green-apres-skiing-in-teal-with-skiers-mahjong-mat', 'green-apres-skiing-with-skiers-mahjong-mat'),
       'letsbebesties.com/texas-a-m-mahjong-mat': ('texas-a-m-mahjong-mat', 'aggies-game-day-mahjong-mat'),
       'letsbebesties.com/vibrant-vortex-with-simple-middle-mahjong-mat': ('vibrant-vortex-with-simple-middle-mahjong-mat', 'vibrant-vortex-open-middle-mahjong-mat')}
for k, (old, new) in LBB.items():
    o = M.get(k)
    if not o: log.append(('MISSING', k)); continue
    for f in ('u', 'u0', 'u_plain'):
        v = o.get(f)
        if not v: continue
        for pre, q in (('%2Fproducts%2F', '%3F'), ('/products/', '?')):
            if pre + old + q in v: v = v.replace(pre + old + q, pre + new + q)
            elif v.endswith(pre + old): v = v[:-len(old)] + new
        o[f] = v
    if new in o.get('u', ''): log.append(('relink', o['n'], new))
k = 'tigredetartan.com/mahjong-mat-domino-blonde'
if k in M and not M[k].get('altu'):
    M[k].update(alt='Also available with rules printed', altu='https://tigredetartan.com/products/mahjong-mat-domino-blonde-rules-edition?sca_ref=11798386.tvil8GTGTp6s2')
    log.append(('alt', 'Domino Blonde', 'rules edition'))
for k in ('brittmillsdesign.com/merrywood-neoprene-mahjong-mat-arriving-late-october', 'brittmillsdesign.com/nutcracker-neoprene-mahjong-mat-arriving-late-october'):
    if k in M and not M[k].get('oos'): M[k]['oos'] = 1; log.append(('sold out', M[k]['n']))
for s in D['sets']:
    if s['slug'] == 'anders-ruff-brownstone-bloom' and not s.get('album'):
        s['album'] = 'https://www.mahjmatchmaker.com/brownstone-bloom-mahjong-tile-matches'; log.append(('album link', s['name']))
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[i + e:]; open(P, 'w').write(h)
ST = json.load(open(REPO + 'config/fym-stock.json'))
for k in ('brittmillsdesign.com/merrywood-neoprene-mahjong-mat-arriving-late-october', 'brittmillsdesign.com/nutcracker-neoprene-mahjong-mat-arriving-late-october'):
    ST['items'][f'm:{k}'] = {'in': False, 'how': 'brittmillsdesign.com /products/<handle>.js available=false, Nov 6 (v116)'}
json.dump(ST, open(REPO + 'config/fym-stock.json', 'w'), indent=0, ensure_ascii=False)
for l in log: print(*l)
print('inbox116:', len(log), 'changes')
