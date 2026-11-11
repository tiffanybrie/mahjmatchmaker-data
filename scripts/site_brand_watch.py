#!/usr/bin/env python3
"""Public 'Brand Watch' page (Tiffany Nov 10 8:01am; asked again 7:39pm). Built from config/brand-watch-curated.json,
partners only (no non-partners, no YMI), product news only. Output: site/livepatch/brand-watch/brand-watch.html
(self-contained; the same markup goes into a Squarespace code block on a HIDDEN /brand-watch page until she says yes)."""
import json, html, os, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
d = json.load(open(R + 'config/brand-watch-curated.json')); e = html.escape
def link(x):
    for k in ('buy', 'url', 'source'):
        u = x.get(k) or ''
        if u.startswith('http') and 'instagram.com' not in u: return u
    return ''
def clean(b): return re.sub(r'\s*\(image-only\)', '', b)
def card(x):
    u = link(x); when = ' · '.join(t for t in (x.get('day'), x.get('time')) if t)
    btn = f'<a class="bw-btn" href="{e(u)}" target="_blank" rel="noopener">Shop{" · code MAHJMATCH" if "MAHJMATCH" in u else ""}</a>' if u else ''
    return (f'<article class="bw-card"><div class="bw-brand">{e(clean(x["brand"]))}</div>'
            f'<div class="bw-what">{e(x["what"])}</div>' + (f'<div class="bw-when">{e(when)}</div>' if when else '') + btn + '</article>')
P = lambda L: [x for x in L if x.get('partner') and 'yellow mountain' not in x.get('brand', '').lower() and 'ymi' not in x.get('brand', '').lower()]
sec = [('Happening this week', P(d['this_week'])), ('On sale now', P(d['sales'])), ('Coming soon', P(d['coming_soon'])), ('Just dropped', P(d['just_dropped']))]
body = ''.join(f'<section class="bw-sec"><h2>{t}</h2><div class="bw-grid">{"".join(card(x) for x in L)}</div></section>' for t, L in sec if L)
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
.bw-card{{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:16px 18px;display:flex;flex-direction:column;gap:8px;min-width:0}}
.bw-brand{{font:700 13px/1.2 system-ui,sans-serif;letter-spacing:.12em;text-transform:uppercase;color:var(--pink)}}
.bw-what{{font-size:17px}}
.bw-when{{font:500 13px system-ui,sans-serif;color:var(--muted)}}
.bw-btn{{align-self:flex-start;margin-top:4px;background:var(--navy);color:var(--bg);text-decoration:none;font:600 14px system-ui,sans-serif;padding:8px 14px;border-radius:999px}}
</style>
<div class="bw"><div class="bw-week">{e(d.get("week_label",""))}</div><h1>Brand Watch</h1>
<p class="bw-intro">New tile sets, mats, racks, restocks and sales from our partner brands, updated through the day. Use code MAHJMATCH at checkout to save.</p>
{body}</div>'''
open(R + 'site/livepatch/brand-watch/brand-watch.html', 'w').write(page); print(sum(len(L) for _, L in sec), 'items')
