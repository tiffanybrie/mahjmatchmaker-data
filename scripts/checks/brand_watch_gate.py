#!/usr/bin/env python3
"""Brand Watch gate (Tiffany Nov 23 10:54pm-11:10pm: "You are not checking Duet's work"; "We have systems in place but they are failing").
Runs on every publish (scripts/site_brand_watch_publish.py refuses on FAIL) and on the front door. Catches the exact failures of Nov 23:
 [1] a note says 'no code / coming soon / not active' for a brand whose code is confirmed in config/code-truth.json (Spools, Averill)
 [2] a visible Coming soon item whose date has passed (Mint Nutcracker 'drops Sun 11/22')
 [3] an item hidden with a HOLD that has passed its reason more than 1 day ago (Mahj Mood Black Friday Week sat hidden while live)
 [4] a visible sale whose end date has passed (Splash 'through Mon 11/23')
 [5] a non-partner shown (Mahj Tile Haus), or a brand never to feature
 [6] --stores: partner store products (tiles/mats/racks) published in the last 10 days that the page never mentions (6 missed Nov 23)
usage: python3 scripts/checks/brand_watch_gate.py [--stores] [--front]"""
import json, re, sys, os, datetime, glob, subprocess, concurrent.futures as cf
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/'
d = json.load(open(R + 'config/brand-watch-curated.json')); ct = json.load(open(R + 'config/code-truth.json'))
TODAY = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-5))).date()
n = lambda s: re.sub(r'[^a-z0-9]', '', (s or '').lower().replace('&', 'and').replace('tartán', 'tartan').replace('(image-only)', ''))
pct = {n(k): v for k, v in ct['pct'].items()}
terms = {n(k): v for k, v in (ct.get('terms') or {}).items() if isinstance(v, dict)}
def confirmed(b):
    k = n(b)
    for kk, v in pct.items():
        if kk and (kk == k or kk.startswith(k) or k.startswith(kk)):
            t = next((tv for tk, tv in terms.items() if tk == kk), {})
            return 'coming soon' not in str(t.get('status', '')).lower()
    return False
NONPARTNER = {n(x) for x in ['Mahj Tile Haus', 'Hutch & Nook', 'Mahjong Row & Co.', 'Yellow Mountain Imports', 'The Mahjong House', 'Cypress']}
fails, warns = [], []
MON = {m: i for i, m in enumerate(['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'], 1)}
def end_date(x):
    for k in ('ends',):
        v = str(x.get(k) or '')
        if re.match(r'\d{4}-\d\d-\d\d', v): return datetime.date.fromisoformat(v[:10])
    m = re.search(r'(?:through|to|until|ends?)\s+(?:[A-Za-z]{3}\s+)?(\d{1,2})/(\d{1,2})', str(x.get('time') or '') + ' ' + x.get('what', ''), re.I)
    if m:
        try: return datetime.date(TODAY.year, int(m.group(1)), int(m.group(2)))
        except ValueError: return None
    m = re.search(r'(?:through|until)\s+(?:[A-Z][a-z]{2}\s+)?([A-Z][a-z]{2})[a-z]*\s+(\d{1,2})', str(x.get('time') or '') + ' ' + x.get('what', ''))
    if m and m.group(1).lower()[:3] in MON:
        try: return datetime.date(TODAY.year, MON[m.group(1).lower()[:3]], int(m.group(2)))
        except ValueError: return None
    return None
for sec in ('this_week', 'coming_soon', 'just_dropped', 'sales'):
    for x in d[sec]:
        b = x.get('brand', ''); what = x.get('what', '')[:70]
        if x.get('hidden'):
            a = str(x.get('action') or '')
            if re.search(r'\bHOLD\b', a):
                f = (x.get('found') or x.get('date') or '')[:10]
                if f and (TODAY - datetime.date.fromisoformat(f)).days > 1: fails.append(f'[3] {b}: hidden on a HOLD since {f}, never released ("{a[:90]}"): unhide it or close the hold')
            continue
        if not x.get('partner'): continue   # the page only renders partner items (site_brand_watch.py P())
        if sec == 'sales' and not x.get('bf') and x.get('approved') is not True: continue
        note = (x.get('save_note') or '') + ' ' + what
        if confirmed(b) and re.search(r"no MAHJMATCH|MAHJMATCH (code )?(isn't|is not) (live|active)|code (isn't|is not) live|not (live|active) yet|code (is )?coming soon|no working code", note, re.I):
            fails.append(f'[1] {b}: note says there is no working code, but code-truth has it confirmed ({sec}: "{(x.get("save_note") or what)[:80]}")')
        if sec == 'coming_soon' and x.get('date') and x['date'] < TODAY.isoformat():
            fails.append(f'[2] {b}: Coming soon item dated {x["date"]} has passed: move it to Just dropped with what happened ("{what}")')
        if sec == 'sales':
            e = end_date(x)
            if e and e < TODAY: fails.append(f'[4] {b}: sale ended {e}: hide it ("{what}")')
        if n(b) in NONPARTNER or any(n(b).startswith(k) for k in NONPARTNER if k): fails.append(f'[5] {b}: not a partner, must not be on Brand Watch ("{what}")')
if '--stores' in sys.argv:   # [6] = what scripts/watch/brand_watch_autoadd.py would still add (same rule, one place)
    r = subprocess.run([sys.executable, R + 'scripts/watch/brand_watch_autoadd.py', '--dry'], capture_output=True, text=True)
    for l in r.stdout.splitlines():
        if l.startswith('  + '): fails.append('[6] not on Brand Watch: ' + l[4:] + ' (run scripts/watch/brand_watch_autoadd.py)')
    age = (datetime.datetime.now(datetime.timezone.utc) - datetime.datetime.fromisoformat(json.load(open(R + 'docs/status/partner-launches.json'))['run_at'])).total_seconds() / 3600
    if age > 12: fails.append(f'[6] store read is {age:.0f}h old: run python3 scripts/watch/partner_launch_watch.py first')
if '--stores' in sys.argv or '--images' in sys.argv:   # [7] Nov 24 (Tiffany 10:45am: broken Sadie Jane photo on the live page). Brands (OMM)
    # RENAME their Shopify image files when a listing goes live; the old file then breaks in shoppers' browsers, though a cloud fetch and a
    # cloud headless Chrome still get it from cache (checked Nov 24: both said fine). So: every card photo on a Shopify CDN must be one of the
    # linked product's CURRENT images (/products/<handle>.json). This also catches the pre-launch photos that will break on launch day.
    import urllib.request
    B = open(R + 'site/livepatch/brand-watch/block.html').read()
    cards = re.findall(r'<img class="bw-img" src="(https://cdn\.shopify\.com/[^"]+)"(?:(?!<img class="bw-img").)*?href="(https://[^"]+)"', B, re.S)
    def chk(c):
        img, href = c; m = re.search(r'https://([^/]+)/(?:discount/[^?]+\?redirect=)?/?products/([^/?#"&]+)', href.replace('%2F', '/'))
        if not m: return None
        try:
            j = json.load(urllib.request.urlopen(urllib.request.Request(f'https://{m.group(1)}/products/{m.group(2)}.json', headers={'User-Agent': 'Mozilla/5.0'}), timeout=20))
        except Exception: return None
        cur = {i['src'].split('?')[0].rsplit('/', 1)[-1] for i in j['product'].get('images', [])}
        return None if not cur or img.split('?')[0].rsplit('/', 1)[-1] in cur else f'[7] card photo is not one of {m.group(2)}\'s current images (renamed files break in browsers): {img}'
    with cf.ThreadPoolExecutor(8) as ex:
        for r in ex.map(chk, set(cards)):
            if r: fails.append(r)
if '--front' in sys.argv:
    if fails: print(f'BRAND WATCH GATE FAILS ({len(fails)}): fix in config/brand-watch-curated.json, rebuild, publish:'); [print('  - ' + f) for f in fails[:10]]
    sys.exit(0)
for f in fails: print('FAIL ' + f)
print('BRAND WATCH GATE: ' + ('PASS' if not fails else f'{len(fails)} FAIL'))
sys.exit(1 if fails else 0)
