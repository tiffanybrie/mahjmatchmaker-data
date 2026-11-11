#!/usr/bin/env python3
"""Public 'Brand Watch' page (Tiffany Nov 10 8:01am; asked again 7:39pm). Built from config/brand-watch-curated.json,
partners only (no non-partners, no YMI), product news only. Output: site/livepatch/brand-watch/brand-watch.html
(self-contained; the same markup goes into a Squarespace code block on a HIDDEN /brand-watch page until she says yes)."""
import json, html, os, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
d = json.load(open(R + 'config/brand-watch-curated.json')); e = html.escape
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
    want = words(x['what']); best = None
    for hk, P in SNAP.items():
        if not any(hk.replace('www.', '') == h.replace('www.', '') for h in hosts): continue
        for hd, pr in P.items():
            sc = len(want & words(pr['title']))
            if sc >= 1 and any(len(w) >= 5 for w in want & words(pr['title'])) and (best is None or sc > best[0]): best = (sc, hk, hd, pr)
    return best[1:] if best else None
def shop(x):
    r = route(x['brand']); hosts = r.get('store_hosts') or []
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
def line(x):
    (lk, img) = shop(x); when = ' · '.join(t for t in (x.get('day'), x.get('time')) if t)
    btn = ''
    if lk:
        u, code = lk; btn = f'<a class="bw-btn" href="{e(u)}" target="_blank" rel="noopener">Shop{" · use code MAHJMATCH" if code else ""}</a>'
    return img, (f'<div class="bw-item"><div class="bw-what">{e(x["what"])}</div>' + (f'<div class="bw-when">{e(when)}</div>' if when else '') + btn + '</div>')
def card(group):
    parts = [line(x) for x in group]; img = next((i for i, _ in parts if i), None)
    pic = f'<img class="bw-img" src="{e(img)}" alt="" loading="lazy">' if img else ''
    return f'<article class="bw-card">{pic}<div class="bw-body"><div class="bw-brand">{e(clean(group[0]["brand"]))}</div>{"".join(h for _, h in parts)}</div></article>'
def grouped(L):
    order, G = [], {}
    for x in L:
        k = clean(x['brand']); (order.append(k) if k not in G else None); G.setdefault(k, []).append(x)
    return [G[k] for k in order]
P = lambda L: [x for x in L if x.get('partner') and 'yellow mountain' not in x.get('brand', '').lower() and 'ymi' not in x.get('brand', '').lower()]
for _k in ('this_week', 'sales', 'coming_soon', 'just_dropped'):
    for _x in d[_k]: _x['_sec'] = _k
sec = [('Happening this week', P(d['this_week'])), ('On sale now', P(d['sales'])), ('Coming soon', P(d['coming_soon'])), ('Just dropped', P(d['just_dropped']))]
body = ''.join(f'<section class="bw-sec"><h2>{t}</h2><div class="bw-grid">{"".join(card(g) for g in grouped(L))}</div></section>' for t, L in sec if L)
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
.bw-when{{font:500 13px system-ui,sans-serif;color:var(--muted)}}
.bw-btn{{align-self:flex-start;margin-top:4px;background:var(--navy);color:var(--bg);text-decoration:none;font:600 14px system-ui,sans-serif;padding:8px 14px;border-radius:999px}}
</style>
<div class="bw"><div class="bw-week">{e(d.get("week_label",""))}</div><h1>Brand Watch</h1>
<p class="bw-intro">New tile sets, mats, racks, restocks and sales from our partner brands, updated through the day. Use code MAHJMATCH at checkout to save.</p>
{body}</div>'''
open(R + 'site/livepatch/brand-watch/brand-watch.html', 'w').write(page); print(sum(len(L) for _, L in sec), 'items')
