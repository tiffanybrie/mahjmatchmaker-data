#!/usr/bin/env python3
"""Live check of every brand code page + the hub (Tiffany Nov 6: 'how do we make it that things can't slip?').
FAILS when any VISIBLE text or SEO tag on a page:
  - shows a 'verified' date older than verified_max_age_days, or two different verified dates,
  - shows a % for a brand that differs from config/code-truth.json (pct), or ANY % for a brand whose truth says pct:null.
COVERAGE (Nov 7 gap audit A4: 11 of 38 hub brands had no truth entry and passed silently). FAILS when:
  - a brand on the live hub, or a live *-discount-code page in the sitemap, has no entry in code-truth.json (pct or terms),
  - a hub row's offer disagrees with its truth (wrong %, a % for a no-% brand, missing scope/minimum/perk = terms.hub_must),
  - the hub's "All N" / ItemList numberOfItems differs from the number of brand rows,
  - Tigre de Tartan's code shows as TEXT where visitors see it (truth terms code_visible=image_only, Tiffany Oct 30),
  - a brand page's meta description states a % without its scope (terms desc_must),
  - a removed_pages URL answers 200, or is still in the sitemap more than sitemap_lag_days after removed_brands.since (WARN before).
HTML comments and <script> code comments are ignored. Exit 1 on any fail.
Usage: python3 scripts/checks/live_codes_check.py [--json out.json]
A job that edits codes/dates is NOT done until this prints 'PASS'."""
import re, sys, json, datetime, html, unicodedata, urllib.request, urllib.error
ROOT='https://www.mahjmatchmaker.com'
truth=json.load(open('config/code-truth.json')); P=truth['pct']; MAXAGE=truth.get('verified_max_age_days',9)
T=truth.get('terms',{}); AL=truth.get('aliases',{}); LAG=truth.get('sitemap_lag_days',3)
MON={m:i+1 for i,m in enumerate(['january','february','march','april','may','june','july','august','september','october','november','december'])}
def nz(x):
    x=''.join(c for c in unicodedata.normalize('NFD',html.unescape(str(x or ''))) if not unicodedata.combining(c)).lower()
    return re.sub(r'[^a-z0-9]','',x.replace('&','and').replace('+','and'))
KNOWN=set(P)|set(T)
NZB={}
for b in KNOWN:
    for n in [b]+AL.get(b,[]): NZB[nz(n)]=b
def names(b): return [b]+AL.get(b,[])
def pct_of(b):
    if b in P: return P[b]
    return T.get(b,{}).get('pct')
def get(u):
    r=urllib.request.Request(u+('&' if '?' in u else '?')+'nc='+str(datetime.datetime.now().timestamp()),headers={'User-Agent':'Mozilla/5.0 mm-check'})
    return urllib.request.urlopen(r,timeout=30).read().decode('utf8','ignore')
class _NoRedir(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*a,**k): return None
def status(u):
    try:
        return urllib.request.build_opener(_NoRedir).open(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 mm-check'}),timeout=30).status
    except urllib.error.HTTPError as e: return e.code
    except Exception as e: return f'error {e}'
def visible(h):
    h=re.sub(r'<!--.*?-->','',h,flags=re.S)
    h=re.sub(r'<script(?![^>]*ld\+json)[^>]*>.*?</script>','',h,flags=re.S)
    return html.unescape(h)
def body_text(h):
    """What a visitor reads: no head/title/meta, no scripts (incl. JSON-LD), no alt text."""
    h=re.sub(r'<!--.*?-->','',h,flags=re.S)
    h=re.sub(r'<head\b.*?</head>','',h,flags=re.S|re.I)
    h=re.sub(r'<(script|style|title|noscript)[^>]*>.*?</\1>','',h,flags=re.S|re.I)
    return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',h)))
def dates(t):
    out=[]
    for m in re.finditer(r'verified[^0-9A-Za-z]{0,40}?(?:<[^>]+>\s*)*(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\.? (\d{1,2}),? (20\d\d)',t,flags=re.I):
        mo=m.group(1).lower(); mo=next(v for k,v in MON.items() if k.startswith(mo[:3]))
        out.append(datetime.date(int(m.group(3)),mo,int(m.group(2))))
    for m in re.finditer(r'Verified:</dt><dd>([A-Za-z]+) (\d{1,2}), (20\d\d)',t):
        out.append(datetime.date(int(m.group(3)),MON[m.group(1).lower()],int(m.group(2))))
    return out
hub=get(ROOT+'/mahjong-discount-codes')
today=datetime.date.today(); fails=[]; warns=[]; info=[]
REMOVED_PAGES={rp:(b,o) for b,o in truth.get('removed_brands',{}).items() for rp in o.get('removed_pages',[])}
# ---- COVERAGE 1: every hub row has a truth entry and its offer matches
rows=re.findall(r'<li[^>]*>\s*<a href="([^"]+)"[^>]*>\s*<strong>(.*?)</strong>(.*?)</li>',hub,flags=re.S)
if not rows: fails.append('hub: no brand rows parsed (layout changed? fix the parser before trusting this check)')
hub_map={}
for href,nm,rest in rows:
    name=html.unescape(re.sub(r'<[^>]+>','',nm)).strip()
    b=NZB.get(nz(name))
    row_txt=re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',rest))).strip()
    row_all=re.sub(r'\s+',' ',html.unescape(re.sub(r'<img[^>]*alt="([^"]*)"[^>]*>',r' \1 ',rest))); row_all=re.sub(r'<[^>]+>',' ',row_all)
    if not b: fails.append(f'hub: "{name}" has NO entry in config/code-truth.json (add pct or terms from the partner email; "page only, unconfirmed" if nothing confirms it)'); continue
    if href.startswith('/'): hub_map[href]=b
    pc=pct_of(b); shown=[int(x) for x in re.findall(r'(\d{1,2})%',row_all)]
    if pc is None and shown: fails.append(f'hub row {b}: shows {shown[0]}% but truth has no confirmed % ("{row_txt[:80]}")')
    if pc is not None and pc not in shown: fails.append(f'hub row {b}: does not show {pc}% off (truth {pc}%): "{row_txt[:80]}"')
    if pc is not None and any(n!=pc for n in shown): fails.append(f'hub row {b}: shows {shown} (truth {pc}%)')
    t=T.get(b,{})
    if t.get('hub_must') and not re.search(t['hub_must'],row_all): fails.append(f'hub row {b}: offer should say /{t["hub_must"]}/ (truth: {t.get("perk") or t.get("scope") or t.get("code")}) but says "{row_txt[:80]}"')
    if t.get('code_visible')=='image_only' and t.get('code') and t['code'] in row_txt: fails.append(f'hub row {b}: code {t["code"]} shows as TEXT (must be the image only, Tiffany Oct 30)')
# hub count claims
m=re.search(r'All (\d+) mahjong discount codes',body_text(hub))
if m and int(m.group(1))!=len(rows): fails.append(f'hub: heading says "All {m.group(1)}" but lists {len(rows)} brands')
for n in set(re.findall(r'"numberOfItems":\s*(\d+)',hub)):
    if int(n)!=len(rows): fails.append(f'hub: ItemList numberOfItems {n} but lists {len(rows)} brands')
for n in set(re.findall(r'at most of the (\d+) mahjong brands',hub)):
    if int(n)!=len(rows): fails.append(f'hub: FAQ says "most of the {n} mahjong brands" but lists {len(rows)}')
# ---- COVERAGE 2: every live *-discount-code page (hub-linked + sitemap) has a truth brand
try: SM=[u.replace(ROOT,'') for u in re.findall(r'<loc>([^<]+)</loc>',get(ROOT+'/sitemap.xml'))]
except Exception as e: SM=[]; fails.append(f'sitemap fetch error {e}')
sm_code=[u for u in SM if re.fullmatch(r'/[a-z0-9-]+-discount-code(-\d+)?',u)]
pages=sorted((set(hub_map)|set(sm_code))-set(REMOVED_PAGES))
PB=dict(truth.get('page_brand',{})); PB.update(hub_map)
for pg in pages:
    if pg in PB: continue
    s_=nz(re.sub(r'-discount-code(-\d+)?$','',pg))
    b=NZB.get(s_) or NZB.get('the'+s_)
    if b: PB[pg]=b
    else: fails.append(f'{pg}: live brand code page with NO entry in config/code-truth.json (add the brand, or page_brand if the slug differs)')
for b,t in T.items():
    if t.get('status','').startswith('page only'): info.append(f'{b}: {t.get("code")} {str(t["pct"])+"%" if t.get("pct") else (t.get("perk") or "no %")} = page only, unconfirmed ({t["source"][:90]})')
NOPCT=[b for b in KNOWN if pct_of(b) is None]
def brand_pct_fails(name,t,where):
    for b in KNOWN:
        p=pct_of(b)
        for bn in names(b):
            for m in re.finditer(re.escape(bn)+r'[^.%<;]{0,60}?(\d{1,2})% off|(\d{1,2})% (?:off )?at '+re.escape(bn),t):
                n=int(m.group(1) or m.group(2))
                if p is None: fails.append(f'{where}: {b} shows {n}% but truth has no confirmed %: "{m.group(0)[:90]}"')
                elif n!=p: fails.append(f'{where}: {b} shows {n}% (truth {p}%): "{m.group(0)[:90]}"')
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
    b=PB.get(path); tb=T.get(b,{}) if b else {}
    if tb.get('code_visible')=='image_only' and tb.get('code') and tb['code'] in body_text(h):
        fails.append(f'{path}: {b} code {tb["code"]} shows as visible TEXT (image/auto-apply link only, Tiffany Oct 30)')
    if tb.get('desc_must'):
        dm=re.search(r'<meta name="description" content="([^"]*)"',h)
        if dm and re.search(r'\d+%',dm.group(1)) and not re.search(tb['desc_must'],html.unescape(dm.group(1))):
            fails.append(f'{path}: SEO description states a % without the scope /{tb["desc_must"]}/: "{html.unescape(dm.group(1))[:110]}"')
    # page-level % for its own brand (title/description)
    for b in KNOWN:
        p=pct_of(b)
        if p is None: continue
        if b.lower().split()[0] in path and re.search(re.escape(b)+r' Discount Code: (\d+)% Off',t):
            n=int(re.search(re.escape(b)+r' Discount Code: (\d+)% Off',t).group(1))
            if n!=p: fails.append(f'{path}: SEO title says {n}% (truth {p}%)')
        for m in re.finditer(r'Save (\d+)% at '+re.escape(b),t):
            if int(m.group(1))!=p: fails.append(f'{path}: "Save {m.group(1)}% at {b}" (truth {p}%)')
        for m in re.finditer(r'MAHJMATCH saves (\d+)% on eligible '+re.escape(b),t):
            if int(m.group(1))!=p: fails.append(f'{path}: FAQ says {m.group(1)}% (truth {p}%)')
        for m in re.finditer(r'MAHJMATCH</span> for (\d+)% off at '+re.escape(b),h):
            if int(m.group(1))!=p: fails.append(f'{path}: code box says {m.group(1)}% (truth {p}%)')
# REMOVED PAGES: must not answer 200; must leave the sitemap within sitemap_lag_days of removed_brands.since
for rp,(b,o) in REMOVED_PAGES.items():
    st=status(ROOT+rp)
    if st==200: fails.append(f'{rp}: removed {b} page still answers 200')
    if rp in SM:
        age=(today-datetime.date.fromisoformat(o.get('since',str(today)))).days
        msg=f'{rp}: removed {b} page still in sitemap.xml ({age} days since {o.get("since")}; status {st})'
        (warns if age<=LAG else fails).append(msg+(' WARN: sitemap lag allowed up to %d days'%LAG if age<=LAG else ''))
# REMOVED BRANDS (Tiffany Nov 6: Mahjong Row & Co. out of the site completely): crawl the whole sitemap; any visible mention FAILS.
RB=truth.get('removed_brands',{})
if RB:
    urls=[ROOT+u for u in SM]
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
cov=sum(1 for _ in rows)
print(f'LIVE CODES CHECK {today}: {len(pages)} brand pages + hub ({len(rows)} hub brands, all with truth: {"yes" if not any("NO entry" in f for f in fails) else "NO"}) · ' + ('PASS' if not fails else f'FAIL ({len(fails)})'))
for f in fails: print(' -',f)
for w in warns: print(' WARN',w)
for i in info: print(' INFO',i)
import os
os.makedirs('docs/status',exist_ok=True)
json.dump({'at':datetime.datetime.now().isoformat(timespec='seconds'),'date':str(today),'pages':len(pages),'hub_brands':len(rows),'fails':fails,'warns':warns,'unconfirmed':info},open('docs/status/live-check.json','w'),indent=1)
if '--json' in sys.argv: json.dump({'date':str(today),'pages':len(pages),'fails':fails},open(sys.argv[sys.argv.index('--json')+1],'w'),indent=1)
sys.exit(1 if fails else 0)
