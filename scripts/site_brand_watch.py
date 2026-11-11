#!/usr/bin/env python3
"""Public 'Brand Watch' page (Tiffany Nov 10 8:01am; asked again 7:39pm). Built from config/brand-watch-curated.json,
partners only (no non-partners, no YMI), product news only. Output: site/livepatch/brand-watch/brand-watch.html
(self-contained; the same markup goes into a Squarespace code block on a HIDDEN /brand-watch page until she says yes)."""
import datetime, json, html, os, re, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
d = json.load(open(R + 'config/brand-watch-curated.json')); e = html.escape
# CUSTOMER-FACING WORDS ONLY (Tiffany Nov 11 11:33am: "Pushing Holly Berry" came from a brand email; that language is for us).
# `what` is what shoppers read: plain facts. Our notes go in `action`. The build refuses internal words.
_INTERNAL = re.compile(r"\bpush(ing|es|ed)?\b|affiliate|commission|\bdraft|waiting|her yes|tiffany|claude|codes post|album day|\bteaser\b|sneak peek|\bFYM\b|sca_ref|\bwe\b|\bour\b|told us|per (their|the) email|buyable|\bTBD\b", re.I)
_bad = [(k, x['brand'], x['what']) for k in ('this_week', 'just_dropped', 'sales', 'coming_soon') for x in d[k] if x.get('partner') and _INTERNAL.search(x['what'])]
_CS_WHEN = re.compile(r'no (name or |release )?date|not announced|date not|\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\b|\d{1,2}/\d{1,2}|ships|arriv|christmas|week|today|tomorrow|out now|on sale now|preorder|pre-order', re.I)
_bad += [('coming_soon', x['brand'], x['what'] + '   <- say WHEN, or "No date yet" / "No name or date yet" (Tiffany Nov 11 11:40am)') for x in d['coming_soon'] if x.get('partner') and not x.get('hidden') and not _CS_WHEN.search(x['what'])]
if _bad:
    sys.exit('BRAND WATCH: internal wording in customer text (rewrite the `what` as plain facts):\n' + '\n'.join(f'  {k} | {b} | {w}' for k, b, w in _bad))
# --- Nov 10 9:43pm (Tiffany): links must be CONSISTENT. Rule: a Shop button only when there is something to buy
# (a product page that is in stock or on preorder), and every partner Shop button carries the code the same way.
# Products come from config/partner-products-snapshot.json (the partner watch's own store snapshot) so a restock
# with no URL in the note still gets its real product page + photo.
import unicodedata
from urllib.parse import urlparse, quote
SNAP = json.load(open(R + 'config/partner-products-snapshot.json'))
ROUTES = json.load(open(R + 'config/link-routes.json'))['brands']
AUTO = {h.replace('www.', '') for h in json.load(open(R + 'config/autoapply-hosts.json'))['hosts']}
norm = lambda t: unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode().lower()
def route(brand):
    b = norm(re.sub(r'\s*\(.*?\)', '', brand)).replace('the ', '').strip()
    b = {'mah jongg maven': 'mahjjmaven'}.get(b, b)
    for k, v in ROUTES.items():
        kk = norm(k).replace('the ', '')
        if kk == b or kk.startswith(b) or b.startswith(kk): return v
    return {}
STOP = set('tiles tile mat mats rack racks set sets new back in stock restock restocked live now the and with of a for drop drops dropped launch launches mahjong mahj sold out pre order preorder full size christmas holiday holidays edition editions pink green red blue yellow white black gold mint teal lilac cream olive coral navy art deco teased tease season coming soon sneak peek collab collection gift card cards store tiles mats acrylic layers'.split())
TEASER = re.compile(r'tease|sneak peek|coming|soon|en route|no date|unannounced|awaiting|will|opened|store|deals start|comment ', re.I)
LIVEWORDS = re.compile(r'dropped|reservations open|taking orders|back in stock|\\bback\\b|in stock|live|restock|pre-?order|now taking orders|arrived|on sale', re.I)
SOLD = re.compile(r'sold out(?! now)|sold out again', re.I)
words = lambda t: {w for w in re.findall(r'[a-z]{3,}', norm(t)) if w not in STOP}
# Tiffany Nov 11 10:14am: tile sets are bigger news than mats/racks: a tile item's photo is the TILES, and tile news leads.
TILEY = lambda x: bool(re.search(r'\btiles?\b|tile set', x['what'], re.I)) and not re.search(r'clutch|bag|case|travel|rack', x['what'], re.I)
def product(x, hosts):
    for k in ('buy', 'url', 'source'):
        u = x.get(k) or ''
        m = re.search(r'/products/([^/?#%]+)', u.replace('%2F', '/'))
        if m:
            for h in hosts:
                for hk, P in SNAP.items():
                    if hk.replace('www.', '') == h.replace('www.', '') and m.group(1) in P: return hk, m.group(1), P[m.group(1)]
            return (urlparse(u).netloc or hosts[0] if hosts else ''), m.group(1), None
    if TEASER.search(x['what']): return None      # a tease / coming-soon line: nothing to buy yet
    if x.get('buy'): return None                    # an explicit buy link (even a store home page) beats any word-guess
    want = words(x['what']); best = None
    for hk, P in SNAP.items():
        if not any(hk.replace('www.', '') == h.replace('www.', '') for h in hosts): continue
        for hd, pr in P.items():
            sc = len(want & words(pr['title'])) + (3 if TILEY(x) and re.search(r'\btiles?\b|tile set', pr['title'], re.I) else 0)   # Nov 11: tiles beat mats for the photo
            if sc >= 1 and any(len(w) >= 5 for w in want & words(pr['title'])) and KIND_OK(x, pr) and (best is None or sc > best[0]): best = (sc, hk, hd, pr)
    return best[1:] if best else None
# Nov 11 12:07pm: a word-guess linked Noli June's "Sue Adores a Scallop" TABLE to their "Sue Puts Out The Good China" TABLECLOTH
# (shared word "Sue"). A guessed product must be the same KIND as the item (tiles / mat / rack / table / tablecloth), else no guess:
# then the item needs an explicit `buy` link (the partner watch sets it from the store).
def KIND_OK(x, pr):
    t = ((x.get('tag') or '') + ' ' + x['what']).lower(); title = pr['title'].lower()
    if re.search(r'table ?cloth', title) != re.search(r'table ?cloth', t) and ('table' in t or 'tablecloth' in title): return False
    if (pr.get('kind') or '').startswith('travel') and 'travel' not in t: return False
    k = (pr.get('kind') or '').replace('travel ', '')
    want = 'tiles' if re.search(r'\btiles?\b|tile set', x.get('tag') or '') else 'rack' if 'rack' in (x.get('tag') or '') else 'mat' if re.search(r'\bmats?\b', x.get('tag') or '') else ''
    return not want or not k or k == want
def shop(x):
    r = route(x['brand']); hosts = r.get('store_hosts') or []
    b = x.get('buy') or ''
    if b and '/products/' not in b.replace('%2F', '/') and not TEASER.search(x['what'].split(';')[0]):   # explicit store/collection link: use it as given
        code = r.get('route') == 'code-site'; h = urlparse(b).netloc.replace('www.', '')
        if code and h in AUTO and '/discount/' not in b: b = f'https://{urlparse(b).netloc}/discount/MAHJMATCH?redirect={quote(urlparse(b).path or "/")}'
        return (b, code), None
    hit = product(x, hosts)
    if not hit:
        head = x['what'].split(';')[0]
        # buyable but we can't pin the exact product (a sale, a collection, a store not in the snapshot):
        # send them to the brand's store with the code rather than leaving a live item with no button
        if hosts and r.get('route') == 'code-site' and (x.get('_sec') == 'sales' or (LIVEWORDS.search(head) and not TEASER.search(head) and not SOLD.search(head))) and 'comment ' not in head.lower():
            code = r.get('route') == 'code-site'; h = hosts[0]
            return ((f'https://{h}/discount/MAHJMATCH' if code and h.replace('www.', '') in AUTO else f'https://{h}/'), code), None
        return None, None
    host, handle, pr = hit
    head = x['what'].split(';')[0]   # 'Emerald back in stock; Ruby Red is sold out' -> judge the item, not its sibling
    fresh_live = bool(LIVEWORDS.search(head)) and not SOLD.search(head)   # the watch saw it newer than the snapshot
    if SOLD.search(head) and 'restock' not in head.lower(): return None, (pr or {}).get('img')
    if TEASER.search(head) and not (pr or {}).get('avail'): return None, (pr or {}).get('img')
    if pr is not None and not (pr.get('avail') or pr.get('pre') or fresh_live): return None, pr.get('img')   # nothing to buy right now
    code = r.get('route') == 'code-site' and 'no promo code' not in x['what'].lower()   # every code partner shows the code, auto-applied or typed
    path = f'/products/{handle}'
    u = (f'https://{host}/discount/MAHJMATCH?redirect={quote(path)}' if code and host.replace('www.', '') in AUTO else f'https://{host}{path}')
    return (u, code), (pr or {}).get('img')
def clean(b): return re.sub(r'\s*\(image-only\)', '', b)
def stamp(f):   # Tiffany Nov 11 10:04am: every update timestamped (when WE posted it), like a live ticker
    if not f: return ''
    try:
        t = datetime.datetime.fromisoformat(f)
        return t.strftime('%a %-m/%-d') + (t.strftime(' · %-I:%M%p').replace('AM', 'am').replace('PM', 'pm') + ' ET' if 'T' in f else '')
    except Exception: return ''
# Tiffany Nov 11 10:23am: every partner gets a photo (be fair). If the snapshot doesn't have the product yet (brand-new drop),
# read the product's own image from its live page (/products/<handle>.js); teasers with no product page get an `img` in the list.
_LIVE = {}
def live_img(x):
    import subprocess
    for k in ('buy', 'url', 'source'):
        u = (x.get(k) or '').replace('%2F', '/')
        m = re.search(r'https?://([^/]+)/.*?/products/([^/?#&]+)', u) or re.search(r'https?://([^/]+)/products/([^/?#&]+)', u)
        if not m or 'instagram' in m.group(1): continue
        key = m.group(1) + '/' + m.group(2)
        if key not in _LIVE:
            try:
                d = json.loads(subprocess.run(['curl', '-sL', '--max-time', '15', f'https://{m.group(1)}/products/{m.group(2)}.js'], capture_output=True, text=True).stdout)
                f = d.get('featured_image') or ''; _LIVE[key] = ('https:' + f) if f.startswith('//') else f
            except Exception: _LIVE[key] = ''
        if _LIVE[key]: return _LIVE[key]
    return None
def line(x):
    (lk, img) = shop(x); img = x.get('img') or img or live_img(x)   # Nov 11: explicit photo > snapshot > the live product page
    when = ' · '.join(t for t in (x.get('day'), x.get('time')) if t)
    btn = ''
    if lk:
        u, code = lk; btn = f'<a class="bw-btn" href="{e(u)}" target="_blank" rel="noopener">Shop{" · use code MAHJMATCH" if code and 'tigre' not in x['brand'].lower() else ""}</a>' + (save_line(x['brand']) if code else '')
    st = stamp(x.get('found'))
    return img, (f'<div class="bw-item">' + (f'<div class="bw-stamp">Added {e(st)}</div>' if st else '') + f'<div class="bw-what">' + ('<span class="bw-kind bw-k-new">New</span>' if not RESTOCK(x) and x.get('_sec') != 'sales' else '<span class="bw-kind bw-k-re">Restock</span>' if RESTOCK(x) else '') + f'{e(re.sub(r"^NEW:\s*", "", x["what"]))}</div>' + (f'<div class="bw-when">When: {e(when)}</div>' if when else '') + ''.join(f'<div class="bw-hist">Earlier{(" · " + e(stamp(h.get("found")))) if h.get("found") else ""}: {e(h["what"])}</div>' for h in (x.get('history') or [])) + btn + '</div>')
# NEWS RANK (Tiffany Nov 11 10:29am): a tile set (travel too: big ticket) > new racks > rack restocks > mat restocks.
# Brand-new beats a restock of something everyone has seen; brands known for something get their own order (config/brand-known-for.json).
def KIND(x):   # the item's tag decides first ("mat ... pair with Catrina tiles" is a mat), then the words
    t = (x.get('tag') or '').lower()
    if re.search(r'\btiles?\b|tile set', t): return 0
    if 'rack' in t: return 1
    if re.search(r'\bmats?\b', t): return 2
    w = x['what']
    if re.search(r'\btiles?\b|tile set|travel set', w, re.I) and not re.search(r'clutch|bag|case|numbered flower|pair with', w, re.I): return 0
    return 1 if re.search(r'\bracks?\b|pusher', w, re.I) else 2 if re.search(r'\bmats?\b', w, re.I) else 3
RESTOCK = lambda x: bool(x.get('restock')) or (not x.get('new') and bool(re.search(r'back in stock|restock|\bback\b|coming back', x['what'], re.I)))
try: KNOWN = {k.lower(): v for k, v in json.load(open(R + 'config/brand-known-for.json')).items() if not k.startswith('_')}
except Exception: KNOWN = {}
def RANK(x):
    k = KNOWN.get(clean(x['brand']).lower())
    if k: return (k.index(['tiles', 'racks', 'mats', 'other'][KIND(x)]) if ['tiles', 'racks', 'mats', 'other'][KIND(x)] in k else 9, RESTOCK(x))   # her order for that brand: kind first
    return (0 if KIND(x) == 0 else 1, RESTOCK(x), KIND(x))   # default: any tile set, then new before restock, then racks > mats
# SAVINGS LINE (Tiffany Nov 11 11:41am): under every code button, say exactly what the code gets you at that brand,
# from config/code-truth.json (Maison Mahj = free shipping on tile sets, not a %). Tigre de Tartan's code is image-only: no typed line.
_CT = json.load(open(R + 'config/code-truth.json'))
_ckey = lambda b: re.sub(r'[^a-z0-9]', '', clean(b).lower().replace('&', 'and').replace('tartán', 'tartan'))
_CTA = {_ckey(k): v for k, v in (_CT.get('aliases') or {}).items() if isinstance(v, str)}
def save_line(brand):
    k = _ckey(brand); k2 = _ckey(_CTA.get(k, brand))
    t = next((v for kk, v in (_CT.get('terms') or {}).items() if _ckey(kk) in (k, k2)), {})
    pct = t.get('pct') if t else None
    if pct is None: pct = next((v for kk, v in _CT['pct'].items() if _ckey(kk) in (k, k2) or _ckey(kk).startswith(k) or k.startswith(_ckey(kk))), None)
    if t.get('code_visible') == 'image_only' or 'tigre' in k: return ''
    b = clean(brand)
    if t.get('perk'): what = 'for ' + t['perk'].replace('complimentary', 'free')
    elif pct: what = f'to save {pct}%' + (f' on orders over ${t["min_order"]}' if t.get('min_order') else '') + (f' (not on {t["scope"].replace("excludes ", "")})' if str(t.get('scope', '')).startswith('excludes') else '')
    else: what = ''
    return f'<div class="bw-save">Use code <b>MAHJMATCH</b> at {e(b)}' + (f' {e(what)}' if what else '') + '.</div>'
CAP = 2   # Tiffany Nov 11 10:17am: big-inventory brands (Let's Be Besties: 175 new mats) can't dominate; 2 per brand per section, then "See all"
bslug = lambda b: re.sub(r'[^a-z0-9]+', '-', clean(b).lower()).strip('-')
def card(group, cap=CAP, label=''):
    rank = sorted(group, key=RANK)   # Nov 11 10:29am news rank inside a brand
    shown = rank[:cap] if cap else rank
    parts = [line(x) for x in shown]; img = next((i for i, _ in parts if i), None)
    pic = f'<img class="bw-img" src="{e(img)}" alt="" loading="lazy">' if img else ''
    more = (f'<a class="bw-more" href="#{bslug(group[0]["brand"])}">+{len(group) - cap} more · see everything from {e(clean(group[0]["brand"]))} &rarr;</a>' if cap and len(group) > cap else '')
    return f'<article class="bw-card">{pic}<div class="bw-body"><div class="bw-brand">{e(clean(group[0]["brand"]))}' + (f'<span class="bw-tag bw-t-{bslug(label)}">{e(label)}</span>' if label else '') + f'</div>{"".join(h for _, h in parts)}{more}</div></article>'
def grouped(L):
    order, G = [], {}
    for x in L:
        k = clean(x['brand']); (order.append(k) if k not in G else None); G.setdefault(k, []).append(x)
    gs = [G[k] for k in order]
    return sorted(gs, key=lambda g: (min(BIG(x) for x in g) if 'BIG' in globals() else 1, min(RANK(x)[:1] for x in g)))   # stable: tile news first, then the rest in date order
P = lambda L: [x for x in L if x.get('partner') and not x.get('hidden') and 'yellow mountain' not in x.get('brand', '').lower() and 'ymi' not in x.get('brand', '').lower()]
for _k in ('this_week', 'sales', 'coming_soon', 'just_dropped'):
    for _x in d[_k]: _x['_sec'] = _k
# Tiffany Nov 11 10:04am: launches first, then just dropped, then sales, then coming soon; newest first; no item twice.
TODAY = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-5))).strftime('%Y-%m-%d')
LIVE = re.compile(r'\blive\b|back in stock|restock(ed)?\b|arrived|in stock|sold out', re.I)
launch, dropped = [], []
for x in d['this_week']:
    (launch if (x.get('date') or '') >= TODAY and (re.search(r'\blaunch', x['what'], re.I) or not LIVE.search((x.get('time') or '') + ' ' + x['what'])) else dropped).append(x)
dropped += d['just_dropped']
seen = set()
def uniq(L):
    out = []
    for x in L:
        k = (clean(x['brand']).lower(), re.sub(r'\W+', ' ', x['what'].lower())[:40])
        if k in seen: continue
        seen.add(k); out.append(x)
    return out
newest = lambda L: sorted(L, key=lambda x: x.get('found') or x.get('date') or '', reverse=True)
cut = (datetime.datetime.now() - datetime.timedelta(days=10)).strftime('%Y-%m-%d')
BIG = lambda x: 0 if ('oh my mahjong' in x['brand'].lower() and TILEY(x)) else 1   # Tiffany Nov 11 10:22am: OMM tile launch day always leads
# SALES (Tiffany Nov 11 11:37am): a sale usually replaces our code, so a sale shows ONLY on her yes (`approved: true`).
# Black Friday is a standing yes (too big to hide) and gets its own section at the very top; a huge sale (OMM warehouse) she
# approves with `big: true` leads too. "On sale now" read like "for sale": the section is just "Sale".
ALLS = d['sales'] + [x for x in d['coming_soon'] + d['this_week'] + d['just_dropped'] if x.get('bf')]
BF = [x for x in ALLS if x.get('bf')]
SALE = [x for x in d['sales'] if not x.get('bf') and x.get('approved') is True]
sec = [('Black Friday deals', uniq(P(BF))),
       ('Big sale', uniq(P(newest([x for x in SALE if x.get('big')])))),
       ('Launching now', uniq(P(sorted(launch, key=lambda x: (BIG(x), x.get('date') or '', x.get('time') or ''))))),
       ('Just dropped', uniq(P(newest([x for x in dropped if not x.get('bf') and (x.get('found') or x.get('date') or '9') >= cut])))),
       ('Sale', uniq(P(newest([x for x in SALE if not x.get('big')])))),
       ('Coming soon', uniq(P(newest([x for x in d['coming_soon'] if not x.get('bf')]))))]
_pend = [x['brand'] for x in d['sales'] if x.get('partner') and not x.get('hidden') and not x.get('bf') and x.get('approved') is None]
if _pend: print('BRAND WATCH: sales waiting on her yes (hidden until then): ' + ', '.join(_pend), file=sys.stderr)
body = ''.join(f'<section class="bw-sec"><h2>{t}</h2><div class="bw-grid">{"".join(card(g, label=t) for g in grouped(L))}</div></section>' for t, L in sec if L)
# One page per brand (Tiffany Nov 11 10:17am): every brand's full list lives on its own page; the main page feeds from them.
# In the preview these are #<brand> views of the same file; on the website they become /brand-watch/<brand> pages.
_allb = {}
for t, L in sec:
    for x in L: _allb.setdefault(bslug(x['brand']), (clean(x['brand']), []))[1].append((t, x))
bpages = ''.join(f'<section class="bw-bpage" id="p-{k}" hidden><a class="bw-back" href="#">&larr; All brands</a><h2 class="bw-bh">{e(n)}</h2>'
                 + ''.join(f'<h3 class="bw-bsec">{t}</h3><div class="bw-grid">' + ''.join(card([x], cap=0, label=t) for x in sorted([x for tt, x in L if tt == t], key=RANK)) + '</div>' for t in dict.fromkeys(tt for tt, _ in L))   # Nov 11 10:21am: full page = a photo on every item we have one for
                 + '</section>' for k, (n, L) in _allb.items())
body = f'<div id="bw-main">{body}</div>{bpages}'

page = f'''<title>Brand Watch</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
:root{{--bg:#fbf6ef;--card:#ffffff;--ink:#1d2b4f;--navy:#054689;--pink:#c8325f;--muted:#5a6b85;--line:#ecdfd2}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#141a2b;--card:#1d2540;--ink:#eef1f8;--navy:#9cc2ff;--pink:#ff8fb1;--muted:#a9b3c9;--line:#2c3656;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#141a2b;--card:#1d2540;--ink:#eef1f8;--navy:#9cc2ff;--pink:#ff8fb1;--muted:#a9b3c9;--line:#2c3656;color-scheme:dark}}
body{{background:var(--bg);color:var(--ink);font:16px/1.45 Georgia,'Times New Roman',serif}}
.bw{{max-width:1100px;margin:0 auto;padding-block:28px 48px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}}
.bw h1{{font-size:clamp(30px,6vw,46px);color:var(--navy);margin:0 0 6px;text-wrap:balance}}
.bw-intro{{color:var(--muted);max-width:62ch;margin:0 0 8px}}
.bw-week{{font:600 13px/1 system-ui,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--pink)}}
.bw-sec h2{{font-size:22px;color:var(--navy);margin:34px 0 12px;padding-bottom:8px;border-bottom:2px solid var(--line)}}
.bw-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px}}
.bw-card{{background:var(--card);border:1px solid var(--line);border-radius:16px;overflow:hidden;display:flex;flex-direction:column;min-width:0}}
.bw-img{{width:100%;aspect-ratio:4/3;object-fit:cover;display:block;background:var(--line);max-width:100%}}
.bw-body{{padding:14px 18px 16px;display:flex;flex-direction:column;gap:12px}}
.bw-item{{display:flex;flex-direction:column;gap:6px}}
.bw-item+.bw-item{{border-top:1px solid var(--line);padding-top:12px}}
.bw-brand{{font:700 13px/1.2 system-ui,sans-serif;letter-spacing:.12em;text-transform:uppercase;color:var(--pink)}}
.bw-what{{font-size:17px}}
.bw-stamp{{font:600 12px system-ui,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:var(--pink)}}
.bw-updated{{font:500 14px system-ui,sans-serif;color:var(--muted);margin:0 0 4px}}
.bw-more{{font:600 14px system-ui,sans-serif;color:var(--pink);text-decoration:none;margin-top:4px}}
.bw-back{{font:600 14px system-ui,sans-serif;color:var(--navy);text-decoration:none;display:inline-block;margin-top:18px}}
.bw-bh{{font-size:30px;color:var(--navy);margin:10px 0 0}}
.bw-bsec{{font-size:18px;color:var(--navy);margin:22px 0 10px}}
.bw-kind{{display:inline-block;margin-right:6px;font:700 10px/1 system-ui,sans-serif;letter-spacing:.08em;text-transform:uppercase;padding:3px 6px;border-radius:4px;vertical-align:1px}}.bw-k-new{{background:#e8457a;color:#fff}}.bw-k-re{{background:var(--line);color:var(--navy)}}
.bw-hist{{margin-top:4px;font-size:12px;color:var(--muted,#5a6478);border-left:2px solid var(--line);padding-left:8px}}
.bw-save{{margin-top:6px;font-size:12.5px;color:var(--muted,#5a6478)}}.bw-save b{{letter-spacing:.04em}}
.bw-tag{{display:inline-block;margin-left:8px;vertical-align:1px;font:700 10px/1 system-ui,sans-serif;letter-spacing:.08em;text-transform:uppercase;padding:4px 8px;border-radius:999px;background:var(--line);color:var(--navy)}}
.bw-t-launching-now{{background:var(--pink);color:#fff}}
.bw-t-just-dropped{{background:var(--navy);color:var(--bg)}}
.bw-t-sale{{background:#e7b33c;color:#1d2b4f}}
.bw-t-black-friday-deals{{background:#111;color:#fff}}
.bw-t-big-sale{{background:#e7b33c;color:#1d2b4f}}
.bw-sec h2{{position:sticky;top:env(safe-area-inset-top,0px);background:var(--bg);z-index:2;padding-top:8px}}
.bw-when{{font:500 13px system-ui,sans-serif;color:var(--muted)}}
.bw-btn{{align-self:flex-start;margin-top:4px;background:var(--navy);color:var(--bg);text-decoration:none;font:600 14px system-ui,sans-serif;padding:8px 14px;border-radius:999px}}
</style>
<div class="bw"><div class="bw-week">{e(d.get("week_label",""))}</div><h1>Brand Watch</h1>
<p class="bw-updated">Last updated {e(stamp(d.get("updated")))}</p>
<p class="bw-intro">New tile sets, mats, racks, restocks and sales from our partner brands, updated through the day. Use code MAHJMATCH at checkout to save.</p>
{body}</div>
<script>(function(){{function r(){{var h=(location.hash||'').slice(1),p=h&&document.getElementById('p-'+h);document.getElementById('bw-main').hidden=!!p;document.querySelectorAll('.bw-bpage').forEach(function(s){{s.hidden=s!==p}});if(p)window.scrollTo(0,0)}}window.addEventListener('hashchange',r);r()}})();</script>'''
open(R + 'site/livepatch/brand-watch/brand-watch.html', 'w').write(page); print(sum(len(L) for _, L in sec), 'items')
