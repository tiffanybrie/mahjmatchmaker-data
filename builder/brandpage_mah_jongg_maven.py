"""Mah Jongg Maven V1 brand page (Nov 9, 2026). Template: brand-pages/lets-be-besties.html CSS (same as the Mahj Pit builder).
Usage: python3 brandpage_mah_jongg_maven.py <woo products.json (list from /wp-json/wc/store/v1/products)> <verified date text> <out.html>
- Direct partner (no network): Debbie set up code MAHJMATCH on Jan 23, 2026 (mahjmatchmaker@ thread "Affiliate program").
  5% off everything except NMJL cards and Custom Jokers; 5% payout. No affiliate link: the code tracks, so links go to the plain shop.
- Debbie's asks (Jan 2026): never call them "affordable"; don't put them in a "$100 or less" feature. Best sellers: 3 layer Sparkle + Jewel tone ink sets.
- About: facts from mahjonggmaven.com/about and product pages only, read Nov 9, 2026."""
import json, sys, html, re, os
PROD, VDATE, OUT = sys.argv[1:4]
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
HOST = 'https://mahjonggmaven.com'
HOME = 'https://mahjonggmaven.com/'
A = json.load(open(PROD))
def find(prefix):
    m = [p for p in A if p['slug'].startswith(prefix)]
    assert m, prefix
    return m[0]
BN = 'Mah Jongg Maven'
TILES = [('3-layer-amythyst-sparkle', 'Amethyst Sparkle, 3 layer', 'Sparkle tiles with jewel-tone pink, turquoise and light blue ink'),
         ('dark-blue-sparkle-engraved', 'Dark Blue Sparkle, 3 layer', 'Sparkle tiles; choose jewel-tone or primary ink'),
         ('3-layer-deep-lake-blue', 'Midnight Blue with jewel-tone ink, 3 layer', 'Deep blue tiles with turquoise, pink and royal blue ink'),
         ('3-layer-teal-green-engraved', 'Teal Green Jelly, 3 layer', 'Jelly-style tiles with turquoise, pink and royal blue ink'),
         ('3-layer-royal-purple-engraved-hand', 'Royal Purple Jelly, 3 layer', 'Jelly-style tiles with turquoise, pink and blue ink'),
         ('3-layer-pink-leopard', 'Pink Leopard, 3 layer', 'Engraved and hand painted'),
         ('mahj-in-bloom-artist', 'Mahj in Bloom (artist collaboration)', 'Made with artist Lorra Kurtz; each tile draws on her paintings'),
         ('royal-garden-series-artist-inspired-3-layer-orange', 'Royal Garden, Orange Red (artist-inspired)', 'A fresh take on the traditional suits; standard size, fits 18" racks')]
MATS = [('mahj-in-bloom-floral-mat-with-pink-center', 'Colorful Floral, Pink Center', '34" x 34"'),
        ('mahj-in-bloom-floral-mat-with-green-center', 'Colorful Floral, Olive Green Center', '34" x 34"'),
        ('pink-flower-mat-with-navy-center', 'Pink Flower, Navy Center', '34" x 34"'),
        ('leopard-design-mah-jongg-mat', 'Leopard', '34" x 34"'),
        ('peace-love-mah-jongg-game-mat', 'Peace, Love', '34" x 34"'),
        ('colorful-tye-dye-mah-jongg-game-mat', 'Colorful Tie Dye', '34" x 34"')]
HOL = [('menorah-hanukkah-mah-jongg-mat', 'Menorah Hanukkah Mat', 'Blue, gold and green menorah; 34" x 34" neoprene'),
       ('dreidel-hanukkah-mah-jongg-mat', 'Dreidel Hanukkah Mat', '34" x 34"'),
       ('sparkle-santa-christmas', 'Sparkle Santa Christmas tiles', 'Engraved and hand painted holiday set')]
RACKS = [('pink-transparent-racks-with-attached-pushers', 'Pink Transparent Racks (set of 4)', 'Attached straight pusher with adjustable tension'),
         ('turquoise-racks-with-attached-helping-hands', 'Turquoise Racks (set of 4)', 'Attached pushers'),
         ('lavender-mahjong-racks-with-attached-pushers', 'Purple Transparent Racks (set of 4)', 'Attached pushers'),
         ('hand-made-oak-wooden-racks', 'Handcrafted Oak Racks', 'Three wood stains')]
def img(p, w=700):
    s = p['images'][0]['src']
    if 'i0.wp.com' in s: return s.split('?')[0] + f'?w={w}&ssl=1'
    return s
def price(p): return f"${int(p['prices']['price']) / 100:,.0f}"
def card(prefix, name, det, kind):
    p = find(prefix)
    alt = html.escape(f'{BN} {re.sub(r" [(].*", "", name)} mahjong {kind}')
    so = '' if p['is_in_stock'] else ' Sold out for now.'
    return f'''<div class="card">
<img src="{img(p)}" alt="{alt}" loading="lazy">
<div class="in">
<h3>{html.escape(name, quote=False)}</h3>
<p>{html.escape(det, quote=False)}. {price(p)}.{so}</p>
<a class="go" href="{p['permalink']}" target="_blank" rel="noopener">Shop it &rarr;</a>
</div>
</div>'''
tpl = open(R + 'brand-pages/lets-be-besties.html').read()
css = tpl[:tpl.index('</style>') + 8]
FAQ = [("Is there a Mah Jongg Maven discount code?", "Yes. Use code MAHJMATCH at checkout on mahjonggmaven.com for 5% off. It works on everything except NMJL cards and custom Jokers."),
       ("What is Mah Jongg Maven known for?", "Engraved and hand painted American Mah Jongg tile sets that honor the traditional suits with colorful flair, made for more than 28 years. Their best sellers are the 3 layer Sparkle and jewel-tone ink sets."),
       ("Can I customize the Jokers?", "Yes. Mah Jongg Maven offers custom Joker tiles for many of its sets, so you can personalize your set. The discount code does not apply to custom Jokers."),
       ("Does Mah Jongg Maven sell mats and racks too?", "Yes. They carry 34\" x 34\" Mah Jongg mats (including Hanukkah designs), acrylic racks with attached pushers in many colors, handcrafted wooden racks, bags, cases and accessories."),
       ("Does the code work on NMJL cards?", "No. The MAHJMATCH discount does not apply to National Mah Jongg League cards or custom Jokers."),
       ("Can I combine the code with other offers?", "Most shops allow one discount code per order, so the code usually can't be combined with a sale or another code.")]
esc = lambda s: html.escape(s, quote=False).replace("'", '&rsquo;')
faq_html = '\n'.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in FAQ)
schema = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ[:5]]}, ensure_ascii=False)
hero = img(find('mahj-in-bloom-artist'), 1500)
grid = lambda rows, kind: '\n'.join(card(h, n, d, kind) for h, n, d in rows)
body = f'''<div class="mmbg">
<div class="hero">
<img src="{hero}" style="object-position:50% 50%" alt="Mah Jongg Maven Mahj in Bloom engraved and hand painted mahjong tiles">
<div class="hero-txt">
<p class="eyebrow">Brand guide</p>
<h1>{BN}</h1>
<p class="dek">Engraved and hand painted American Mah Jongg tiles with colorful flair, plus mats and racks. Plus, my {BN} discount code for readers.</p>
</div>
</div>
<div class="perk perk-top" style="margin:22px 0 4px">
<p><strong>A thank-you for Mahj Matchmaker readers:</strong> use code <span class="code">MAHJMATCH</span> for 5% off at {BN}.</p>
<p style="font-size:14px;opacity:.75;margin:6px 0 14px">&#10003; {BN} discount code: MAHJMATCH &middot; 5% off (not valid on NMJL cards or custom Jokers) &middot; verified {VDATE}</p>
<a class="btn" href="{HOME}" target="_blank" rel="noopener">Visit {BN}</a>
</div>
<section>
<h2>About {BN}</h2>
<div class="note">
<p>For more than 28 years, {BN} has made engraved and hand painted Mah Jongg sets that keep the traditional suits everyone knows, with color and personality layered on top. They built the business through a printed catalog long before online shopping, and today offer more than 30 tile sets and colorways.</p>
<p>Their best sellers are the 3 layer Sparkle sets and the sets with jewel-tone ink in pink, turquoise and royal blue. They also make custom Joker tiles for many sets, and their newest collections are artist-inspired, like Mahj in Bloom with artist Lorra Kurtz. You&rsquo;ll find mats, racks, cases and accessories there too.</p>
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
<h2>For the holidays</h2>
<div class="grid">
{grid(HOL, 'holiday')}
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
<p><strong>A thank-you for Mahj Matchmaker readers:</strong> use code <span class="code">MAHJMATCH</span> for 5% off at {BN}. It works on everything except NMJL cards and custom Jokers.</p>
<a class="btn" href="{HOME}" target="_blank" rel="noopener">Visit {BN}</a>
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
<a href="/bird-and-bamboo-discount-code">Bird &amp; Bamboo</a>
<a href="/mahj-mood-discount-code">Mahj Mood</a>
<a href="/yolo-mahjong-discount-code">YOLO Mahjong</a>
<a href="/noli-june-discount-code">Noli June</a>
<a href="/mahj-pit-discount-code">Mahj Pit</a>
<a href="/mahjong-discount-codes">All brands &rarr;</a>
</div>
</section>
<p class="small">Mahj Matchmaker may earn a commission when you use my code, at no extra cost to you. Thank you for supporting the tile match mock-ups and inspiration I share with the community.</p>
</div>
<script type="application/ld+json">{schema}</script>'''
open(OUT, 'w').write(css + '\n' + body)
print('ok', OUT, len(css + body))
