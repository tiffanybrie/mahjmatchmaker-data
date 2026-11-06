#!/usr/bin/env python3
"""Live check of every brand code page + the hub (Tiffany Nov 6: 'how do we make it that things can't slip?').
FAILS when any VISIBLE text or SEO tag on a page:
  - shows a 'verified' date older than verified_max_age_days, or two different verified dates,
  - shows a % for a brand that differs from config/code-truth.json.
HTML comments and <script> code comments are ignored. Exit 1 on any fail.
Usage: python3 scripts/checks/live_codes_check.py [--json out.json]
A job that edits codes/dates is NOT done until this prints 'PASS'."""
import re, sys, json, datetime, html, urllib.request
ROOT='https://www.mahjmatchmaker.com'
truth=json.load(open('config/code-truth.json')); P=truth['pct']; MAXAGE=truth.get('verified_max_age_days',9)
MON={m:i+1 for i,m in enumerate(['january','february','march','april','may','june','july','august','september','october','november','december'])}
def get(u):
    r=urllib.request.Request(u+('&' if '?' in u else '?')+'nc='+str(datetime.datetime.now().timestamp()),headers={'User-Agent':'Mozilla/5.0 mm-check'})
    return urllib.request.urlopen(r,timeout=30).read().decode('utf8','ignore')
def visible(h):
    h=re.sub(r'<!--.*?-->','',h,flags=re.S)
    h=re.sub(r'<script(?![^>]*ld\+json)[^>]*>.*?</script>','',h,flags=re.S)
    return html.unescape(h)
def dates(t):
    out=[]
    for m in re.finditer(r'verified[^0-9A-Za-z]{0,40}?(?:<[^>]+>\s*)*(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\.? (\d{1,2}),? (20\d\d)',t,flags=re.I):
        mo=m.group(1).lower(); mo=next(v for k,v in MON.items() if k.startswith(mo[:3]))
        out.append(datetime.date(int(m.group(3)),mo,int(m.group(2))))
    for m in re.finditer(r'Verified:</dt><dd>([A-Za-z]+) (\d{1,2}), (20\d\d)',t):
        out.append(datetime.date(int(m.group(3)),MON[m.group(1).lower()],int(m.group(2))))
    return out
hub=get(ROOT+'/mahjong-discount-codes')
pages=sorted(set(re.findall(r'href="(/[a-z0-9-]+-discount-code)"',hub)))
today=datetime.date.today(); fails=[]
def brand_pct_fails(name,t,where):
    for b,p in P.items():
        for m in re.finditer(re.escape(b)+r'[^.%<]{0,60}?(\d{1,2})% off|(\d{1,2})% (?:off )?at '+re.escape(b),t):
            n=int(m.group(1) or m.group(2))
            if n!=p: fails.append(f'{where}: {b} shows {n}% (truth {p}%): "{m.group(0)[:90]}"')
from concurrent.futures import ThreadPoolExecutor
def fetch(path):
    try: return path, (hub if path=='/mahjong-discount-codes' else get(ROOT+path)), None
    except Exception as e: return path, None, e
with ThreadPoolExecutor(10) as ex: got=list(ex.map(fetch,['/mahjong-discount-codes']+pages))
for path,h,err in got:
    if err: fails.append(f'{path}: fetch error {err}'); continue
    t=visible(h); ds=dates(t)
    if path!='/mahjong-discount-codes':
        if ds:
            if len(set(ds))>1: fails.append(f'{path}: {len(set(ds))} different verified dates {sorted(set(map(str,ds)))}')
            if (today-min(ds)).days>MAXAGE: fails.append(f'{path}: verified {min(ds)} is {(today-min(ds)).days} days old')
    brand_pct_fails(path,t,path)
    # page-level % for its own brand (title/description)
    for b,p in P.items():
        if b.lower().split()[0] in path and re.search(re.escape(b)+r' Discount Code: (\d+)% Off',t):
            n=int(re.search(re.escape(b)+r' Discount Code: (\d+)% Off',t).group(1))
            if n!=p: fails.append(f'{path}: SEO title says {n}% (truth {p}%)')
        for m in re.finditer(r'Save (\d+)% at '+re.escape(b),t):
            if int(m.group(1))!=p: fails.append(f'{path}: "Save {m.group(1)}% at {b}" (truth {p}%)')
        for m in re.finditer(r'MAHJMATCH saves (\d+)% on eligible '+re.escape(b),t):
            if int(m.group(1))!=p: fails.append(f'{path}: FAQ says {m.group(1)}% (truth {p}%)')
        for m in re.finditer(r'MAHJMATCH</span> for (\d+)% off at '+re.escape(b),h):
            if int(m.group(1))!=p: fails.append(f'{path}: code box says {m.group(1)}% (truth {p}%)')
# REMOVED BRANDS (Tiffany Nov 6: Mahjong Row & Co. out of the site completely): crawl the whole sitemap; any visible mention FAILS.
RB=truth.get('removed_brands',{})
if RB:
    try: urls=re.findall(r'<loc>([^<]+)</loc>',get(ROOT+'/sitemap.xml'))
    except Exception as e: urls=[]; fails.append(f'sitemap fetch error {e}')
    def fetch2(u):
        try: return u,get(u)
        except Exception as e: return u,None
    with ThreadPoolExecutor(12) as ex: allp=list(ex.map(fetch2,urls))
    for u,h in allp:
        if not h: continue
        t=visible(h)
        path=u.replace(ROOT,'') or '/'
        for b,o in RB.items():
            if path in o.get('removed_pages',[]): continue
            if path in o.get('allow_mentions',{}):  # mentions allowed (her old match cards, Halloween blog): only dead links + code claims fail
                n=sum(t.count(f'href="{rp}') + t.count(f'href="{ROOT}{rp}') for rp in o.get('removed_pages',[]))
                if n: fails.append(f"{path}: {n} link(s) to a hidden {b} page")
                n=len(re.findall(o.get('pct_claim_pattern','$^'),t))
                if n: fails.append(f"{path}: {b} still shown with a code/% ({n}x)")
                continue
            n=len(re.findall(o['pattern'],t,flags=re.I))
            if n: fails.append(f"{path}: removed brand {b} still shows ({n}x)")
fails=sorted(set(fails))
print(f'LIVE CODES CHECK {today}: {len(pages)} brand pages + hub · ' + ('PASS' if not fails else f'FAIL ({len(fails)})'))
for f in fails: print(' -',f)
import os
os.makedirs('docs/status',exist_ok=True)
json.dump({'at':datetime.datetime.now().isoformat(timespec='seconds'),'date':str(today),'pages':len(pages),'fails':fails},open('docs/status/live-check.json','w'),indent=1)
if '--json' in sys.argv: json.dump({'date':str(today),'pages':len(pages),'fails':fails},open(sys.argv[sys.argv.index('--json')+1],'w'),indent=1)
sys.exit(1 if fails else 0)
