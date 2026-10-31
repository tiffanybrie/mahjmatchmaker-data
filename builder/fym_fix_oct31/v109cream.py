"""v109 (Oct 31 eve): cream/ivory backgrounds were read as YELLOW on new non-partner mats (v108 re-QA: Mahj & Moon
'Harvest Pumpkin Thanksgiving' led the Yellow chip on a 39.9% 'yellow' that is its cream background; pumpkins only orange 21.3%).
Measured each new-brand mat that carries yellow (Bougie, Mahj & Moon, Hutch & Nook, Betty June & Jeannette, Piper Chase) for
SATURATED yellow (hue 30-68 deg, sat >= .25, val >= .35, 6% inset) vs cream (hue 20-70, sat < .30, val >= .60) and looked at
every photo (scratchpad cream109/cand.jpg). Mats where the 'yellow' was cream/beige -> yellow replaced by 'neutral'
(the builder's cream/ivory family) when cream >= 8% and neutral absent, else yellow dropped. Kept as yellow (real yellow seen):
Katelyn (Yellow) mustard border, Amalfi Soleil, Celestial Sun, Lemon groves/blossoms, Limoncello, Champagne Conservatory, Collins
(chartreuse centre), and mats whose yellow came from Tiffany's calls (share 0). Each changed mat is taken out of every set's
rank/cr and appended so v104rank.py (run next) re-places it by colour. Gate [120] guards yellow primaries.
Usage: python3 v109cream.py <build_dir>  (after partneradds109.py, before v104rank.py)."""
import sys, json
B = sys.argv[1]; P = B + '/index.html'
SET = {  # key -> (families, tiers, shares), measured Oct 31 eve
    'mahjandmoon.com/harvest-pumpkin-thanksgiving-mahjong-mat': (['orange', 'neutral', 'dark'], [0, 1, 2], [21.3, 59.3, 29.8]),
}
SWAP = {  # key -> cream share (neutral added at yellow's tier if neutral absent and cream >= 8; else yellow dropped)
    'bougiemahjong.com/pastel-opaline-mahjong-mat': 31.2,
    'bougiemahjong.com/linen-blossom-mahjong-mat': 84.7,
    'bougiemahjong.com/blue-porcelain-estate-mahjong-mat': 33.3,
    'bougiemahjong.com/palm-court-tennis-club-mahjong-mat': 26.3,
    'bougiemahjong.com/palm-garden-tropical-mahjong-mat': 24.2,
    'www.etsy.com/listing/4478449828/hollywood': 0,
}
h = open(P).read(); i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
M = D['mats']; OI = {k: j for j, k in enumerate(D['order'])}; done = []
def rerank(k):
    j = OI[k]
    for s in D['sets']:
        for fld in ('rank', 'cr'):
            L = s.get(fld)
            if L and j in L: L.remove(j)
        if 'rank' in s: s['rank'].append(j)
for k, (mf, mt, sh) in SET.items():
    o = M.get(k)
    if not o: continue
    o.update(mf=mf, mt=mt, sh=sh); rerank(k); done.append(o['n'] + ' -> ' + '/'.join(mf))
for k, cream in SWAP.items():
    o = M.get(k)
    if not o or 'yellow' not in (o.get('mf') or []): continue
    mf, mt, sh = list(o['mf']), list(o.get('mt') or range(len(o['mf']))), list(o.get('sh') or [0] * len(o['mf']))
    y = mf.index('yellow')
    if 'neutral' not in mf and cream >= 8: mf[y], sh[y] = 'neutral', cream
    else: del mf[y]; del mt[y]; del sh[y]
    o.update(mf=mf, mt=mt, sh=sh); rerank(k); done.append(o['n'] + ' -> ' + '/'.join(mf))
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
open(P, 'w').write(h)
print('v109cream:', done)
