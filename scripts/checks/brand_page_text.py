#!/usr/bin/env python3
"""Brand-page text check (added Oct 29 after Tiffany saw 'Tart&aacute;n' on the TdT FAQ).
Fails if any *-discount-code page (or the hub) shows a raw HTML entity in its FAQ JSON-LD
or a double-escaped entity (&amp;xxx;) in visible text. Run by the weekly verified-date task.
Usage: python3 scripts/checks/brand_page_text.py   (exit 1 on any hit)"""
import re, sys, urllib.request
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=30).read().decode('utf-8', 'replace')
sm = get('https://www.mahjmatchmaker.com/sitemap.xml')
urls = [u for u in re.findall(r'<loc>([^<]+)</loc>', sm) if 'discount-code' in u]
fails = []
for u in urls:
    t = get(u)
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
        for h in re.findall(r'.{20}&[a-z]+;.{8}', m.group(1)):
            fails.append((u, 'FAQ JSON entity', h))
    body = re.sub(r'<script.*?</script>|<style.*?</style>', '', t, flags=re.S)
    for h in re.findall(r'.{20}&amp;[a-z]+;.{8}', body):
        fails.append((u, 'double-escaped', h))
for f in fails: print('FAIL', *f)
print(f'{len(urls)} pages checked, {len(fails)} problems')
sys.exit(1 if fails else 0)
