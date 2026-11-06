#!/usr/bin/env python3
"""Broken-link sweep of every brand page + hub (Tiffany Nov 6: 'should I believe there are other errors?').
Checks every outbound shop link (status) and, for Shopify product links, whether the product is available.
Usage: python3 scripts/checks/brand_links_check.py  -> docs/status/brand-links.json"""
import re, json, urllib.request, html, datetime, os
from concurrent.futures import ThreadPoolExecutor
UA={'User-Agent':'Mozilla/5.0 (Macintosh) mm-linkcheck'}
def get(u,t=20):
    r=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=t); return r.status, r.geturl(), r.read()
hub=get('https://www.mahjmatchmaker.com/mahjong-discount-codes')[2].decode('utf8','ignore')
pages=['/mahjong-discount-codes']+sorted(set(re.findall(r'href="(/[a-z0-9-]+-discount-code)"',hub)))
links={}
def page_links(p):
    h=get('https://www.mahjmatchmaker.com'+p)[2].decode('utf8','ignore')
    h=re.sub(r'<script(?![^>]*ld\+json).*?</script>','',h,flags=re.S)
    out=set()
    for u in re.findall(r'href="(https?://[^"]+)"',h):
        u=html.unescape(u)
        if any(x in u for x in ['mahjmatchmaker.com','squarespace','instagram.com','facebook.com','pinterest','tiktok','google','w3.org','schema.org','fonts.','jsdelivr','static1']): continue
        out.add(u)
    return p,out
with ThreadPoolExecutor(8) as ex:
    for p,ls in ex.map(page_links,pages):
        for u in ls: links.setdefault(u,set()).add(p)
def check(u):
    try:
        s,final,body=get(u)
        note=''
        m=re.search(r'https?://([^/]+)/products/([^/?#]+)',final)
        if m:
            try:
                j=json.loads(get(f'https://{m.group(1)}/products/{m.group(2)}.js')[2])
                if not j.get('available',True): note='SOLD OUT'
            except Exception: pass
        if re.search(r'/collections/all\b|/$',final) and '/products/' in u: note='REDIRECTED to home/collection (product gone?)'
        return u,s,note
    except urllib.error.HTTPError as e: return u,e.code,''
    except Exception as e: return u,0,str(e)[:60]
with ThreadPoolExecutor(12) as ex: res=list(ex.map(check,sorted(links)))
bad=[{'url':u,'status':s,'note':n,'pages':sorted(links[u])} for u,s,n in res if s>=400 or s==0 or n]
os.makedirs('docs/status',exist_ok=True)
json.dump({'at':datetime.datetime.now().isoformat(timespec='seconds'),'links':len(links),'pages':len(pages),'bad':bad},open('docs/status/brand-links.json','w'),indent=1)
print(f'{len(pages)} pages, {len(links)} outbound links, {len(bad)} problems')
for b in bad: print(f" {b['status']} {b['note']} {b['url'][:110]} <- {', '.join(b['pages'])[:80]}")
