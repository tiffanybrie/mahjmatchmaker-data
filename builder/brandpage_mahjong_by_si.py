"""Mahjong by SI V1 brand page (Nov 11, 2026). Template: brand-pages/lets-be-besties.html CSS (same as the Mah Jongg Maven builder).
Usage: python3 brandpage_mahjong_by_si.py <shopify products.json list (all pages)> <shop link or homepage> <verified date text> <out.html>
- Direct partner (Mahjong by SI's own affiliate app). Stacie Francombe said yes Nov 6; Jenna set up code MAHJMATCH Nov 9.
  10% off mats for shoppers, up to 5% commission. Cart test Nov 11: MAHJMATCH applicable, 10% off a $50 mat.
- Affiliate link not available yet (created when the free account is set up), so links go to the plain shop until then.
- About: facts from mahjongbysi.com/pages/about and /pages/faq only, read Nov 11, 2026."""
import json, sys, html, re, os
PROD, LINK, VDATE, OUT = sys.argv[1:5]
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
HOST = 'https://www.mahjongbysi.com'
BN = 'Mahjong by SI'
A = json.load(open(PROD))
M = [p for p in A if p['product_type'] == 'Mahjong Mat' and 'b2b' not in p['tags']
     and any(v['available'] for v in p['variants']) and p['images']]
used = set()
def clean(t):
    t = t.split('|')[0].strip()
    t = re.sub(r'^Mahjong by SI™\s*', '', t)
    t = re.sub(r'\s*Mahjong Mat$', '', t).strip()
    return t
def pick(f, n):
    out, words = [], set()
    for p in M:
        if p['handle'] in used or not f(p): continue
        w = clean(p['title']).split()[0].lower()
        if w in words: continue  # one per design family (e.g. one Palazzo, one Party)
        words.add(w); used.add(p['handle']); out.append(p)
        if len(out) == n: break
    return out
def lo(p): return min(float(v['price']) for v in p['variants'] if v['available'])
def url(p):
    u = f"{HOST}/products/{p['handle']}"
    if LINK.rstrip('/') != HOST and '?' in LINK:  # affiliate ref like ?ref=xxx
        u += '?' + LINK.split('?', 1)[1]
    return u
def img(p, w=700):
    s = p['images'][0]['src']
    return s + ('&' if '?' in s else '?') + f'width={w}'
def card(p, kind):
    name = clean(p['title'])
    alt = html.escape(f'{BN} {name} mahjong {kind}')
    tags = p['tags']
    shapes = []
    if 'mat_round' in tags: shapes.append('round')
    if 'mat_scalloped' in tags: shapes.append('scalloped')
    det = 'Sizes from 20" travel up' if 'size_20' in tags else ('SI Signature faux leather, ' + ' and '.join(shapes) if shapes else 'Several sizes')
    return f'''<div class="card">
<img src="{img(p)}" alt="{alt}" loading="lazy">
<div class="in">
<h3>{html.escape(name, quote=False)}</h3>
<p>{html.escape(det, quote=False)}. From ${lo(p):,.0f}.</p>
<a class="go" href="{url(p)}" target="_blank" rel="noopener">Shop it &rarr;</a>
</div>
</div>'''
T = lambda t: (lambda p: t in p['tags'])
NEW = pick(T('new_arrival'), 6)
FLO = pick(T('style_florals'), 6)
COA = pick(T('style_coastal'), 6)
CHI = pick(T('style_chinoiserie'), 6)
HOL = pick(T('christmas'), 3) + pick(lambda p: 'hanukkah' in p['title'].lower() or 'menorah' in p['title'].lower() or 'mazel' in p['title'].lower() or 'shalom' in p['title'].lower(), 3)
SHP = pick(T('mat_round'), 3) + pick(T('mat_scalloped'), 3)
tpl = open(R + 'brand-pages/lets-be-besties.html').read()
css = tpl[:tpl.index('</style>') + 8]
FAQ = [(f"Is there a {BN} discount code?", f"Yes. Use code MAHJMATCH at checkout on mahjongbysi.com for 10% off your mahjong mat."),
       (f"What is {BN} known for?", "Printed mahjong mats, with hundreds of designs from an in-house designer and artist collaborations, printed in the USA by its sister company Signs by SI in Atlanta. New designs drop every Mahjong Monday."),
       (f"What sizes and materials do {BN} mats come in?", "Natural rubber mats come in 20\" travel, 31.5\" and 33.5\". SI Signature faux leather mats come in 20\" travel, 33\" square, 33\" scalloped and 34\" round. Both use a 3mm construction."),
       (f"Can I get a custom {BN} mat?", "Yes. You can personalize one of their designs with a name, monogram, logo or text, or start from a blank mat in their Custom Mat Builder and upload your own artwork."),
       ("Are the mats made to order?", "Yes. Every mat is printed to order in their U.S. facility, and most orders are final sale because they are made to order."),
       ("Can I combine the code with other offers?", "Most shops allow one discount code per order, so the code usually can't be combined with a sale or another code.")]
esc = lambda s: html.escape(s, quote=False).replace("'", '&rsquo;')
faq_html = '\n'.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in FAQ)
schema = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ[:5]]}, ensure_ascii=False)
hero = img(FLO[0], 1500)
grid = lambda rows, kind: '\n'.join(card(p, kind) for p in rows)
body = f'''<div class="mmbg">
<div class="hero">
<img src="{hero}" style="object-position:50% 50%" alt="{BN} {html.escape(clean(FLO[0]['title']))} mahjong mat">
<div class="hero-txt">
<p class="eyebrow">Brand guide</p>
<h1>{BN}</h1>
<p class="dek">Hundreds of printed mahjong mat designs, from florals and coastal prints to chinoiserie and holiday mats, printed in the USA. Plus, my {BN} discount code for readers.</p>
</div>
</div>
<div class="perk perk-top" style="margin:22px 0 4px">
<p><strong>A thank-you for Mahj Matchmaker readers:</strong> use code <span class="code">MAHJMATCH</span> for 10% off your mat at {BN}.</p>
<p style="font-size:14px;opacity:.75;margin:6px 0 14px">&#10003; {BN} discount code: MAHJMATCH &middot; 10% off mats &middot; verified {VDATE}</p>
<a class="btn" href="{LINK}" target="_blank" rel="noopener">Visit {BN}</a>
</div>
<section>
<h2>About {BN}</h2>
<div class="note">
<p>{BN} is the mahjong mat line from Stacie Ivers Francombe, who grew up hearing her mom&rsquo;s weekly mahjong group shuffle tiles down the hall. Her Atlanta print and fabrication company, Signs by SI, printed custom mahjong mats for about five years before {BN} had a name, and her husband and three kids are part of the business.</p>
<p>The designs come from an in-house designer and collaborations with independent artists, and every mat is printed to order in their U.S. facility. Natural rubber mats come in 20&quot;, 31.5&quot; and 33.5&quot;; the SI Signature faux leather mats come in square, scalloped and round shapes. They also offer personalized and fully custom mats, and new designs drop every Mahjong Monday.</p>
</div>
</section>
<p>With hundreds of designs, here&rsquo;s where I&rsquo;d start.</p>
<section>
<h2>New {BN} mats</h2>
<div class="grid">
{grid(NEW, 'mat')}
</div>
</section>
<section>
<h2>Floral mats</h2>
<div class="grid">
{grid(FLO, 'mat')}
</div>
</section>
<section>
<h2>Coastal mats</h2>
<div class="grid">
{grid(COA, 'mat')}
</div>
</section>
<section>
<h2>Chinoiserie mats</h2>
<div class="grid">
{grid(CHI, 'mat')}
</div>
</section>
<section>
<h2>For the holidays</h2>
<div class="grid">
{grid(HOL, 'holiday mat')}
</div>
</section>
<section>
<h2>Round and scalloped mats</h2>
<div class="grid">
{grid(SHP, 'mat')}
</div>
</section>
<section>
<h2>{BN} Discount Code</h2>
<div class="perk">
<p><strong>A thank-you for Mahj Matchmaker readers:</strong> use code <span class="code">MAHJMATCH</span> for 10% off your mat at {BN}.</p>
<a class="btn" href="{LINK}" target="_blank" rel="noopener">Visit {BN}</a>
</div>
</section>
<section>
<h2>Questions about {BN}</h2>
{faq_html}
</section>
<section>
<h2>More brands I love</h2>
<div class="more">
<a href="/oh-my-mahjong-discount-code">Oh My Mahjong</a>
<a href="/miss-mahjong-discount-code">Miss Mahjong</a>
<a href="/my-fair-mahjong-discount-code">My Fair Mahjong</a>
<a href="/mahj-mood-discount-code">Mahj Mood</a>
<a href="/noli-june-discount-code">Noli June</a>
<a href="/mahj-pit-discount-code">Mahj Pit</a>
<a href="/mah-jongg-maven-discount-code">Mah Jongg Maven</a>
<a href="/soiree-all-day-discount-code">Soir&eacute;e All Day</a>
<a href="/mahjong-discount-codes">All brands &rarr;</a>
</div>
</section>
<p class="small">Mahj Matchmaker may earn a commission when you use my code, at no extra cost to you. Thank you for supporting the tile match mock-ups and inspiration I share with the community.</p>
</div>
<script type="application/ld+json">{schema}</script>'''
open(OUT, 'w').write(css + '\n' + body)
print('ok', OUT, len(css + body))
