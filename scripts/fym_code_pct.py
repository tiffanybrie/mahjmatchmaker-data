"""Verified MAHJMATCH code percentages for price-after-code (Table view price filter, Nov 1).
Source of truth = the live Discount Codes hub at-a-glance list (https://www.mahjmatchmaker.com/mahjong-discount-codes), the same
list the brand pages and the weekly codes post use. Only UNCONDITIONAL "N% off with MAHJMATCH" lines count; anything with a
different code, a minimum or a collection limit (YMI, Noli June $100 min, Soiree The Mahjong Collection) and link-only Tigre de
Tartan stay at retail. Writes config/fym-code-pct.json {brand: pct}. Usage: python3 scripts/fym_code_pct.py"""
import re, html, json, datetime, urllib.request, pathlib
R = pathlib.Path(__file__).resolve().parents[1]
t = urllib.request.urlopen(urllib.request.Request('https://www.mahjmatchmaker.com/mahjong-discount-codes', headers={'User-Agent': 'Mozilla/5.0'}), timeout=40).read().decode('utf-8', 'replace')
txt = html.unescape(re.sub(r'<[^>]+>', '\n', re.sub(r'<script.*?</script>|<style.*?</style>', '', t, flags=re.S)))
L = [l.strip() for l in txt.split('\n') if l.strip()]
upd = next((re.search(r'Updated ([A-Z][a-z]+ \d+, \d{4})', l).group(1) for l in L if re.search(r'Updated [A-Z][a-z]+ \d+, \d{4}', l)), '')
pct, skipped = {}, {}
for i, l in enumerate(L):
    m = re.match(r'^— (\d{1,2})% off (.*)$', l)
    if not m: continue
    brand, rest = L[i - 1], m.group(2)
    if rest.strip() == 'with MAHJMATCH': pct[brand] = int(m.group(1))
    else: skipped[brand] = l
out = {'_about': __doc__.split('\n')[0], 'source': 'https://www.mahjmatchmaker.com/mahjong-discount-codes', 'hub_updated': upd,
       'checked': datetime.date.today().isoformat(), 'pct': dict(sorted(pct.items())), 'retail_only': dict(sorted(skipped.items()))}
json.dump(out, open(R / 'config/fym-code-pct.json', 'w'), indent=1, ensure_ascii=False)
print(len(pct), 'brands with a verified %, retail only:', list(skipped))
