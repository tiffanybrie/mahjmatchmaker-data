"""YOLO Mahjong V1 brand page (Oct 28, 2026). Template: brand-pages/lets-be-besties.html CSS (same as Fait à Main builder).
Usage: python3 brandpage_yolo_mahjong.py <products.json> <affiliate link or ''> <verified date text> <out.html>
- Until the UpPromote link is known, links go to the shop homepage / plain product URLs (HQ brands/yolo-mahjong.next says 'link missing').
- Code MAHJMATCH: YOLO coupon email Oct 23 + cart test Oct 28 (10% off, applicable=true).
- About: facts from yolomahjong.com only (About Us, FAQ, shipping policy, product pages), read Oct 28, 2026."""
import json, sys, html, re, os
PROD, LINK, VDATE, OUT = sys.argv[1:5]
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
HOST = 'https://www.yolomahjong.com'
REF = ('?' + LINK.split('?', 1)[1]) if '?' in LINK else ''
HOME = LINK or HOST
P = {p['handle']: p for p in json.load(open(PROD))['products']}
BN = 'YOLO Mahjong'
JTTW = [('journey-to-the-west-collection-mahjong-tiles', 0, 'Journey to the West Mahjong Tiles (pre-order)', '160 tiles + 2 dice, engraved and UV printed, ivory marble-look backs, ships mid-December', 'tiles'),
        ('journey-to-the-west-collection-mat-31-5-shipped-rolled', 0, 'Journey to the West Mat (pre-order)', 'Neoprene, 31.5" square, burgundy, ivory, green and gold', 'mat'),
        ('journey-to-the-west-tortoiseshell-acrylic-rack-20', 1, 'Tortoiseshell Acrylic Racks, 20" (set of 4)', 'Amber-brown tortoiseshell acrylic, in stock', 'racks'),
        ('journey-to-the-west-golden-wooden-rack-20', 1, 'Metallic Gold Wooden Racks, 20" (set of 4)', 'Metallic gold finish', 'racks')]
MATS = [('pink-tiger-mahjong-mat-floral-chinese-mahjong-table-mat-for-mahjong-set-31-5-x-31-5-inch', 'Pink Tiger Floral'),
        ('blue-chinoiserie-peacock-mahjong-mat', 'Blue Chinoiserie Peacock'),
        ('pink-hydrangea-mahjong-mat', 'Pink Hydrangea'),
        ('crane-moon-mahjong-mat-floral-chinese-mahjong-table-mat-for-mahjong-set-31-5-x-31-5-inch', 'Crane &amp; Moon'),
        ('mahjong-mat-martini-mahjong-mat-pink-orange', 'Martini'),
        ('tropical-palm-beach-mahjong-mat', 'Tropical Palm Beach'),
        ('scalloped-pink-purple-mahjong-mat', 'Scalloped Pink &amp; Purple'),
        ('sage-ripple-mahjong-mat', 'Sage Ripple'),
        ('lavender-scroll-mahjong-mat', 'Lavender Scroll'),
        ('mahjong-mat-31-5x31-5-ship-folded-3', 'Leopard Print'),
        ('pastel-rainbow-round-mahjong-mat', 'Pastel Rainbow Round')]
HOL = [('pre-order-neoprene-heritage-christmas-tartan-mahjong-mat-ship-rolled-up', 'Heritage Christmas Tartan (pre-order)', 'Neoprene, 33" square, ships mid-November'),
       ('preorder-neoprene-winter-ski-resort-square-mahjong-mat-ship-rolled-up', 'Winter Ski Resort (pre-order)', 'Neoprene'),
       ('classic-christmas-plaid-mahjong-mat', 'Classic Christmas Plaid', 'Shipped rolled'),
       ('christmas-botanical-bow-mahjong-mat', 'Christmas Botanical Bow', 'Shipped rolled')]
def price(p):
    v = sorted({float(x['price']) for x in p['variants']}); f = lambda x: f'${x:,.0f}'
    return f(v[0]) if len(v) == 1 else f'{f(v[0])}&ndash;{f(v[-1])}'
def size(p):
    b = html.unescape(re.sub(r'<[^>]+>', ' ', p['body_html'] or '')) + ' ' + p['title']
    m = re.search(r'(\d+(?:\.\d+)?)\s*(?:x|in)\s*(\d+(?:\.\d+)?)\s*in', b) or re.search(r'(\d+(?:\.\d+)?)"\s*[xX×]\s*(\d+(?:\.\d+)?)"', b)
    if not m: return ''
    return f'{m.group(1)}" round' if 'round' in p['handle'] else f'{m.group(1)}" square'
def card(h, ix, name, det, kind):
    p = P[h]; im = p['images'][ix]['src'].split('?')[0] + '?width=700'
    alt = html.escape(f'{BN} {html.unescape(re.sub(r" [(].*", "", name))} mahjong {kind}')
    return f'''<div class="card">
<img src="{im}" alt="{alt}" loading="lazy">
<div class="in">
<h3>{name}</h3>
<p>{det}. {price(p)}.</p>
<a class="go" href="{HOST}/products/{h}{REF}" target="_blank" rel="sponsored noopener">Shop it &rarr;</a>
</div>
</div>'''
tpl = open(R + 'brand-pages/lets-be-besties.html').read()
css = tpl[:tpl.index('</style>') + 8]
FAQ = [("Is there a YOLO Mahjong discount code?", "Yes. Use code MAHJMATCH at checkout on yolomahjong.com for 10% off."),
       ("Who is behind YOLO Mahjong?", "YOLO Mahjong was founded by a Singaporean couple who love Chinese culture, storytelling and mahjong. Each collection is built around a story, starting with Chinese literature."),
       ("What is the Journey to the West collection?", "It's YOLO Mahjong's storytelling set: 160 engraved, UV-printed tiles plus 2 dice, inspired by the classic novel Journey to the West, with a matching neoprene mat, dice tray and 20\" racks. The tiles and mat are on pre-order, shipping mid-December 2026."),
       ("Does YOLO Mahjong offer free shipping?", "Yes. Shipping is free on US orders over $50."),
       ("Can I personalize a YOLO Mahjong set?", "Yes. They customize tile backs with initials, names, dates, monograms or simple artwork for individual orders."),
       ("Can I combine the code with other offers?", "Most shops allow one discount code per order, so the code usually can't be combined with a sale or another code.")]
esc = lambda s: html.escape(s, quote=False).replace("'", '&rsquo;')
faq_html = '\n'.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in FAQ)
schema = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ[:5]]}, ensure_ascii=False)
hero = P['journey-to-the-west-collection-mat-31-5-shipped-rolled']['images'][1]['src'].split('?')[0] + '?width=1500'
mats = '\n'.join(card(h, 0, n, ', '.join(x for x in ['Polyester, non-slip rubber backing', size(P[h])] if x), 'mat') for h, n in MATS)
hol = '\n'.join(card(h, 0, n, d, 'mat') for h, n, d in HOL)
body = f'''<div class="mmbg">
<div class="hero">
<img src="{hero}" style="object-position:50% 50%" alt="YOLO Mahjong Journey to the West tiles and racks on the matching mat">
<div class="hero-txt">
<p class="eyebrow">Brand guide</p>
<h1>{BN}</h1>
<p class="dek">Story-driven mahjong tiles, illustrated mats and 20&quot; racks, starting with the Journey to the West collection. Plus, my {BN} discount code for readers.</p>
</div>
</div>
<div class="perk perk-top" style="margin:22px 0 4px">
<p><strong>A thank-you for Mahj Matchmaker readers:</strong> use code <span class="code">MAHJMATCH</span> for 10% off at {BN}.</p>
<p style="font-size:14px;opacity:.75;margin:6px 0 14px">&#10003; Code verified {VDATE}</p>
<a class="btn" href="{HOME}" target="_blank" rel="sponsored noopener">Visit {BN}</a>
</div>
<section>
<h2>About {BN}</h2>
<div class="note">
<p>{BN} was founded by a Singaporean couple with a shared love of Chinese culture, storytelling and mahjong, a game their grandmothers played. Each collection is built around a story, starting with Chinese literature, and their logo is four interlocking hearts, one for each player at the table.</p>
<p>Their first storytelling set is Journey to the West: 160 larger-format tiles (about 1.5&quot; &times; 1&quot;), engraved and UV printed on ivory fronts with ivory marble-look backs, with a matching neoprene mat, dice tray and 20&quot; tortoiseshell or gold racks sized for American mahjong. They also make a big range of printed 31.5&quot; mats (florals, chinoiserie, tropical, ripple and scallop borders, holiday plaids) and personalize tile backs for individual orders. Shipping is free on US orders over $50.</p>
</div>
</section>
<p>Here are the {BN} tiles, mats and racks I&rsquo;d look at first.</p>
<section>
<h2>Journey to the West collection</h2>
<div class="grid">
{chr(10).join(card(h, i, n, d, k) for h, i, n, d, k in JTTW)}
</div>
</section>
<section>
<h2>{BN} mats</h2>
<div class="grid">
{mats}
</div>
</section>
<section>
<h2>Holiday mats</h2>
<div class="grid">
{hol}
</div>
</section>
<section>
<h2>{BN} Discount Code</h2>
<div class="perk">
<p><strong>A thank-you for Mahj Matchmaker readers:</strong> use code <span class="code">MAHJMATCH</span> for 10% off at {BN}. Shop through my link so the code tracks.</p>
<a class="btn" href="{HOME}" target="_blank" rel="sponsored noopener">Visit {BN}</a>
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
<a href="/mahjong-row-and-co-discount-code">Mahjong Row &amp; Co.</a>
<a href="/royal-mahjong-society-discount-code">The Royal Mahjong Society</a>
<a href="/lets-be-besties-discount-code">Let&rsquo;s Be Besties</a>
<a href="/soiree-all-day-discount-code">Soir&eacute;e All Day</a>
<a href="/mahjong-register-discount-code">Mahjong Register</a>
<a href="/mahjong-discount-codes">All brands &rarr;</a>
</div>
</section>
<p class="small">Mahj Matchmaker may earn a commission when you shop through these links, at no extra cost to you. Thank you for supporting the tile match mock-ups and inspiration I share with the community.</p>
</div>
<script type="application/ld+json">{schema}</script>'''
open(OUT, 'w').write(css + '\n' + body)
print('ok', OUT, len(css + body), 'ref' if REF else 'NO LINK (homepage)')
