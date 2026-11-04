"""Mahj Pit V1 brand page (Nov 4, 2026). Template: brand-pages/lets-be-besties.html CSS (same as the YOLO / Fait a Main builders).
Usage: python3 brandpage_mahj_pit.py <products.json> <verified date text> <out.html>
- Tiffany Nov 4 3:27pm: direct link https://mahjpit.co/tiffany11, code MAHJMATCH (UpPromote, auto-applied via the link), PayPal.
- Code MAHJMATCH: cart test Nov 4 (10% off, applicable=true; a fake code = applicable false).
- About: facts from mahjpit.co only (About page, product pages, return policy), read Nov 4, 2026."""
import json, sys, html, re, os
PROD, VDATE, OUT = sys.argv[1:4]
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
HOST = 'https://mahjpit.co'
REF = '?sca_ref=12703261.srer4OxWkeRwwDVs'
HOME = 'https://mahjpit.co/tiffany11'
P = {p['handle']: p for p in json.load(open(PROD))['products']}
BN = 'Mahj Pit'
TILES = [('large-confetti-tiles', 'The Original Confetti Tiles (Large)', 'Translucent acrylic with an iridescent confetti finish and a high-contrast blue face; 160 tiles, tile bag and dice'),
         ('the-original-confetti-tiles-small', 'The Original Confetti Tiles (Small)', 'The confetti tiles in a smaller size'),
         ('the-martha-tiles', 'The Martha Tiles', 'Pearl backs with a wave pattern and solid white faces; 160 tiles incl. jokers and blanks, tile bag and dice'),
         ('merry-merry-holiday-tiles-limited-edition', 'Merry Merry Holiday Tiles (limited edition)', 'Vintage holiday colours: champagne, citrus, cinnamon and eggnog')]
MATS = [('mahjong-mat-domino-oxblood', 'Domino Oxblood', 'Oxblood botanical ribbons with hidden tigers'),
        ('mahjong-mat-french-mural', 'French Mural', 'From their tabletop collection'),
        ('savannah', 'Savannah', 'Low-pile chenille, 31" square, machine washable'),
        ('inky-mat', 'The Blue Hole', 'Low-pile chenille'),
        ('the-butterfly-dolly-mat', 'Butterfly Dolly', 'Low-pile chenille, 31.5" square, comes with a storage tube'),
        ('pixel-pusher-mat', 'Pixel Pusher', 'Low-pile chenille'),
        ('paint-party-mat', 'Paint Party', 'Low-pile chenille')]
HOL = [('mahjong-mat-ditsy-christmas-maraschino-w-rules', 'Ditsy Christmas, Maraschino', 'Holiday mat with the rules printed on it')]
RACKS = [('blonde-tortoise-pusher-house-racks-set-of-4-copy', 'Retro Racks (set of 4)', '20", thick acrylic, magnets underneath hold the pusher, dual-pocket carry bag'),
         ('blonde-tortoise-pusher-tag-a-long-racks-set-of-4', 'Blonde Tortoise Pusher House Racks (set of 4)', '20", thick acrylic, magnetic pusher storage'),
         ('double-trouble-tortoise-siamese-racks', 'Double Trouble Tortoise Siamese Racks', '20", made for two-player games, with a Mahj Pit carry bag')]
def price(p):
    v = sorted({float(x['price']) for x in p['variants']}); f = lambda x: f'${x:,.0f}'
    return f(v[0]) if len(v) == 1 else f'{f(v[0])}&ndash;{f(v[-1])}'
def avail(p): return any(v['available'] for v in p['variants'])
def card(h, name, det, kind):
    p = P[h]; im = p['images'][0]['src'].split('?')[0] + '?width=700'
    alt = html.escape(f'{BN} {html.unescape(re.sub(r" [(].*", "", name))} mahjong {kind}')
    so = '' if avail(p) else ' Sold out for now.'
    return f'''<div class="card">
<img src="{im}" alt="{alt}" loading="lazy">
<div class="in">
<h3>{name}</h3>
<p>{det}. {price(p)}.{so}</p>
<a class="go" href="{HOST}/products/{h}{REF}" target="_blank" rel="sponsored noopener">Shop it &rarr;</a>
</div>
</div>'''
tpl = open(R + 'brand-pages/lets-be-besties.html').read()
css = tpl[:tpl.index('</style>') + 8]
FAQ = [("Is there a Mahj Pit discount code?", "Yes. Use code MAHJMATCH at checkout on mahjpit.co for 10% off."),
       ("What is Mahj Pit known for?", "Design-forward mahjong tiles in translucent acrylic, like their Original Confetti tiles with an iridescent finish and high-contrast blue faces, plus chenille and neoprene mats and 20\" acrylic racks with magnetic pusher storage."),
       ("What size are Mahj Pit tiles?", "Their standard sets measure 0.91 x 1.38 x 0.43 in and come with 160 tiles, a tile bag and dice."),
       ("Are Mahj Pit mats washable?", "Their low-pile chenille mats have a non-slip rubber back and are machine washable; they ship rolled in a tube."),
       ("What is Mahj Pit's return policy?", "Unused items in original packaging can be returned within 14 days of delivery; tiles must be unopened with seals intact."),
       ("Can I combine the code with other offers?", "Most shops allow one discount code per order, so the code usually can't be combined with a sale or another code.")]
esc = lambda s: html.escape(s, quote=False).replace("'", '&rsquo;')
faq_html = '\n'.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in FAQ)
schema = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ[:5]]}, ensure_ascii=False)
hero = P['large-confetti-tiles']['images'][0]['src'].split('?')[0] + '?width=1500'
grid = lambda rows, kind: '\n'.join(card(h, n, d, kind) for h, n, d in rows)
body = f'''<div class="mmbg">
<div class="hero">
<img src="{hero}" style="object-position:50% 50%" alt="Mahj Pit Original Confetti mahjong tiles">
<div class="hero-txt">
<p class="eyebrow">Brand guide</p>
<h1>{BN}</h1>
<p class="dek">Translucent acrylic tiles, chenille mats and 20&quot; acrylic racks for design-minded players. Plus, my {BN} discount code for readers.</p>
</div>
</div>
<div class="perk perk-top" style="margin:22px 0 4px">
<p><strong>A thank-you for Mahj Matchmaker readers:</strong> use code <span class="code">MAHJMATCH</span> for 10% off at {BN}.</p>
<p style="font-size:14px;opacity:.75;margin:6px 0 14px">&#10003; {BN} discount code: MAHJMATCH &middot; 10% off &middot; verified {VDATE}</p>
<a class="btn" href="{HOME}" target="_blank" rel="sponsored noopener">Visit {BN}</a>
</div>
<section>
<h2>About {BN}</h2>
<div class="note">
<p>{BN} started because its founders couldn&rsquo;t find tiles that matched how they wanted to play: not disposable plastic, and not another set covered in palm trees and preppy patterns. So they made design-conscious tiles in translucent acrylic that catches the light, built to be played hard and passed down.</p>
<p>Their best-known set is the Original Confetti tiles, with an iridescent confetti finish and a high-contrast blue face that&rsquo;s easy to read across the table. They also make low-pile chenille and neoprene mats, travel mats, 20&quot; acrylic racks with magnetic pusher storage, dice holders and vintage finds for the table.</p>
</div>
</section>
<p>Here are the {BN} tiles, mats and racks I&rsquo;d look at first.</p>
<section>
<h2>{BN} tiles</h2>
<div class="grid">
{grid(TILES, 'tiles')}
</div>
</section>
<section>
<h2>{BN} mats</h2>
<div class="grid">
{grid(MATS, 'mat')}
</div>
</section>
<section>
<h2>Holiday mat</h2>
<div class="grid">
{grid(HOL, 'mat')}
</div>
</section>
<section>
<h2>{BN} racks</h2>
<div class="grid">
{grid(RACKS, 'racks')}
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
<a href="/bird-and-bamboo-discount-code">Bird &amp; Bamboo</a>
<a href="/mahj-mood-discount-code">Mahj Mood</a>
<a href="/yolo-mahjong-discount-code">YOLO Mahjong</a>
<a href="/noli-june-discount-code">Noli June</a>
<a href="/mahjong-discount-codes">All brands &rarr;</a>
</div>
</section>
<p class="small">Mahj Matchmaker may earn a commission when you shop through these links, at no extra cost to you. Thank you for supporting the tile match mock-ups and inspiration I share with the community.</p>
</div>
<script type="application/ld+json">{schema}</script>'''
open(OUT, 'w').write(css + '\n' + body)
print('ok', OUT, len(css + body))
