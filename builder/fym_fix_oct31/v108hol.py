"""v108 (Oct 31): holiday-tag fix for mats brought in / unhidden by v108 (Bougie, Mahj & Moon, Hutch & Nook).
CLAUDE.md holiday rule (Tiffany Oct 21 FINAL): ONLY Christmas, Hanukkah and winter snowy/ski scenes are Holiday.
Valentine's / Thanksgiving / fall / Halloween / Easter / patriotic / Derby live in their colour sections.
v108 QA (Oct 31): Mahj & Moon 'Valentine Hearts American' and 'Harvest Pumpkin Thanksgiving' came in hol=True (old store tag).
Each photo checked by eye (scratchpad hol108/sheet.jpg): hearts on red/pink; pumpkins on cream with orange/green.
Colours measured from the brand photo cropped to the mat (bamboo floor removed, 9% inset) with build_accents.measure;
families pooled like the v108 adds (teal->blue, earthy/brown->dark, gold->yellow), >= 8% share, top 4.
'Festive Citrus Chinoiserie' stays Holiday (no Christmas graphic, but a holiday-tagged mat stays until Tiffany moves it; asked in MATCH-INBOX).
Each fixed mat is taken out of every set's rank/cr and appended at the end of rank, so v104rank.py (run next) re-places it by colour.
Usage: python3 v108hol.py <build_dir>   (runs after partneradds108.py, before v104rank.py)."""
import sys, json
B = sys.argv[1]; P = B + '/index.html'
FIX = {  # key -> (families in share order, shares) measured Oct 31 from the store photo (mahjandmoon.com/products/<handle>.json image 0)
    'mahjandmoon.com/valentine-hearts-american-mahjong-mat': (['red', 'pink'], [54.0, 46.0]),
    'mahjandmoon.com/harvest-pumpkin-thanksgiving-mahjong-mat': (['yellow', 'dark', 'orange'], [39.9, 29.8, 21.3]),
}
h = open(P).read(); i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
M = D['mats']; O = D['order']; OI = {k: j for j, k in enumerate(O)}
done = []
for k, (fams, sh) in FIX.items():
    o = M.get(k)
    if not o: continue
    o.update(hol=False, mf=fams, mt=list(range(len(fams))), sh=sh, ha=[])
    j = OI[k]
    for s in D['sets']:
        for fld in ('rank', 'cr'):
            L = s.get(fld)
            if L and j in L: L.remove(j)
        if 'rank' in s: s['rank'].append(j)
    done.append(o['n'])
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
open(P, 'w').write(h)
print('v108hol: not holiday ->', done)
