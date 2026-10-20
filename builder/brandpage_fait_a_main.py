"""Fait à Main V1 brand page (Oct 20, 2026). Template: brand-pages/lets-be-besties.html (CSS reused as-is).
Usage: python3 brandpage_fait_a_main.py <products.json> <affiliate link or ''> <verified date text, e.g. 'October 21, 2026'> <out.html>
- Product links get the affiliate ref query (everything after '?' in the link) once the link is known.
- Until the link exists, links go to the shop homepage / plain product URLs (HQ brands/fait-a-main.next says 'link missing').
- About section: facts from faitamainstudio.com only (home page, product pages, shipping banner), read Oct 20, 2026."""
import json, sys, html, re
PROD, LINK, VDATE, OUT = sys.argv[1:5]
R = '/home/claude/mahjmatchmaker-data/'
HOST = 'https://faitamainstudio.com'
REF = ('?' + LINK.split('?', 1)[1]) if '?' in LINK else ''
HOME = LINK or HOST
P = {p['handle']: p for p in json.load(open(PROD))['products']}
BN = 'Fait &agrave; Main'; BNp = 'Fait à Main'
# (handle, image index picked by eye: flat lay of the mat / rack, no promo graphics)
MATS = [('le-ete-indien-studio-print-no-1', 0), ('saint-remy-mat', 0), ('automne-provencal', 0), ('le-madeline', 0),
        ('le-bandana-edition-limitee', 0), ('le-bandana-rose-bonbon', 0), ('le-bandana-purple-peach', 0),
        ('texas-mon-amour-mat', 0), ('texas-mon-amour-mat-peach', 0), ('le-drip-mat-summer-colors', 0),
        ('round-top-mon-amour-mahjong-mat', 0), ('l-ete-indien-voyage', 4)]
RACKS = [('the-scallop-rack-set', 0), ('the-scalloped-rack-pink-tortoise', 0)]
NAMES = {'le-ete-indien-studio-print-no-1': "L&rsquo;&Eacute;t&eacute; Indien, Studio Print No. 1", 'saint-remy-mat': 'Saint-R&eacute;my', 'automne-provencal': 'Automne Proven&ccedil;al',
         'le-madeline': 'Le Madeline', 'le-bandana-edition-limitee': 'Le Bandana, Crimson &amp; Cream', 'le-bandana-rose-bonbon': 'Le Bandana, Rose Bonbon',
         'le-bandana-purple-peach': 'Le Bandana, Purple &amp; Peach', 'texas-mon-amour-mat': 'Texas Mon Amour, Cream', 'texas-mon-amour-mat-peach': 'Texas Mon Amour, Peach',
         'le-drip-mat-summer-colors': 'Le Drip, Summer Colors', 'round-top-mon-amour-mahjong-mat': 'Round Top Mon Amour (limited edition)',
         'l-ete-indien-voyage': "L&rsquo;&Eacute;t&eacute; Indien, Voyage (travel mat)", 'the-scallop-rack-set': 'The Scalloped Rack, Clear Acrylic (set of 4)',
         'the-scalloped-rack-pink-tortoise': 'The Scalloped Rack, Pink Tortoise'}
def nice_old(t):
    t = re.sub(r'\s*[—-]\s*(PINK TORTOISE PERFECTION!|ACRYLIC MAHJONG RACKS)', lambda m: ' — ' + m.group(1).title().replace('!', ''), t)
    t = t.replace('LE BANDANA - ', 'Le Bandana, ').replace(' MAHJONG MAT', '').replace(' Mahjong Mat', '')
    if t.isupper() or sum(c.isupper() for c in t) > len(t) * .6: t = t.title()
    return t.replace("'S ", "'s ").replace('Mat Cream', 'Mat, Cream').replace('Mat Peach', 'Mat, Peach').replace(' & ', ' &amp; ')
def price(p):
    v = sorted({float(x['price']) for x in p['variants']}); f = lambda x: f'${x:,.0f}'
    return f(v[0]) if len(v) == 1 else f'{f(v[0])}&ndash;{f(v[-1])}'
def detail(p, h=''):
    b = html.unescape(re.sub(r'<[^>]+>', ' ', p['body_html'] or ''))
    m = re.search(r'(\d+(?:\.\d+)?)"\s*x\s*(\d+(?:\.\d+)?)"', b)
    size = f'{m.group(1)}" square' if m else ''
    bits = [x for x in ['Leatherette' if ('eatherette' in b or 'bandana' in h) else '', size or ('31.5" square' if 'bandana' in h else '')] if x]
    if 'Monogram' in json.dumps(p['options']) or 'MONOGRAM' in json.dumps(p['options']): bits.append('optional hand-painted monogram')
    if 'acrylic' in b.lower(): bits = ['Acrylic with magnetic scalloped pusher' if 'pusher' in b.lower() else 'Acrylic, magnetic']
    if 'RULES PRINTED' in json.dumps(p['options']): bits.append('rules printed on the mat or design only')
    return ', '.join(bits)
def card(h, ix, kind):
    p = P[h]; im = p['images'][ix]['src'].split('?')[0] + '?width=700'; n = NAMES[h]
    alt = html.escape(f'{BNp} {html.unescape(n)} mahjong {kind}')
    return f'''<div class="card">
<img src="{im}" alt="{alt}" loading="lazy">
<div class="in">
<h3>{n}</h3>
<p>{detail(p, h)}. {price(p)}.</p>
<a class="go" href="{HOST}/products/{h}{REF}" target="_blank" rel="sponsored noopener">Shop it &rarr;</a>
</div>
</div>'''
tpl = open(R + 'brand-pages/lets-be-besties.html').read()
css = tpl[:tpl.index('</style>') + 8]
FAQ = [("Is there a Fait à Main discount code?", "Yes. Use code MAHJMATCH at checkout on faitamainstudio.com."),
       ("Where is Fait à Main based?", "Fait à Main is a hand-painting and design studio in Houston, Texas, founded by Luisa Rangel de Alba."),
       ("What are Fait à Main mahjong mats made of?", "Most Fait à Main mats are 31.5\" square, printed with the studio's original art on leatherette with a soft slip-resistant backing. The Voyage edition is a 19.5\" travel mat."),
       ("Can I add a monogram to a Fait à Main mat?", "Yes. Most mats offer a hand-painted monogram, painted in the studio. Monogrammed items are final sale."),
       ("Does Fait à Main offer free shipping?", "Fait à Main offers free standard shipping on US orders over $250, and ships worldwide."),
       ("Can I combine the code with other offers?", "Most shops allow one discount code per order, so the code usually can't be combined with a sale or another code.")]
esc = lambda s: html.escape(s, quote=False).replace("'", '&rsquo;').replace('à', '&agrave;')
faq_html = '\n'.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in FAQ)
schema = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ[:5]]}, ensure_ascii=False)
hero = P['saint-remy-mat']['images'][0]['src'].split('?')[0] + '?width=1500'
body = f'''<div class="mmbg">
<div class="hero">
<img src="{hero}" style="object-position:50% 50%" alt="Fait &agrave; Main Saint-R&eacute;my mahjong mat">
<div class="hero-txt">
<p class="eyebrow">Brand guide</p>
<h1>{BN}</h1>
<p class="dek">Hand-painted mahjong mats, scalloped acrylic racks and monogrammed accessories from a Houston design atelier. Plus, my {BN} discount code for readers.</p>
</div>
</div>
<div class="perk perk-top" style="margin:22px 0 4px">
<p><strong>A thank-you for Mahj Matchmaker readers:</strong> use code <span class="code">MAHJMATCH</span> at {BN}.</p>
<p style="font-size:14px;opacity:.75;margin:6px 0 14px">&#10003; Code verified {VDATE}</p>
<a class="btn" href="{HOME}" target="_blank" rel="sponsored noopener">Visit {BN}</a>
</div>
<section>
<h2>About {BN}</h2>
<div class="note">
<p>{BN} is a creative design atelier in Houston, Texas. Founder Luisa Rangel de Alba studied textile design in Mexico City, Florence, Milan and San Francisco, and learned the hand-painting technique of marquage during years in luxury retail with the French maison Goyard. That hand-painting is the studio&rsquo;s signature.</p>
<p>Their mahjong mats are printed with Luisa&rsquo;s original art on leatherette with a soft slip-resistant backing, most at 31.5&quot; square, and nearly every mat can carry a monogram hand painted in the studio. Prints include the Texas Mon Amour bandana collection, Provençal stripes and florals, the Studio Print line and Le Drip. They also make scalloped acrylic racks, painted leather pouches, totes and needlepoint. Free standard shipping on US orders over $250; monogrammed pieces are final sale.</p>
</div>
</section>
<p>Here are the {BN} mats and racks you&rsquo;ll find in Find Your Match, paired with tile sets.</p>
<section>
<h2>{BN} mahjong mats</h2>
<div class="grid">
{chr(10).join(card(h, i, 'mat') for h, i in MATS)}
</div>
</section>
<section>
<h2>Scalloped acrylic racks</h2>
<div class="grid">
{chr(10).join(card(h, i, 'racks') for h, i in RACKS)}
</div>
</section>
<section>
<h2>{BN} Discount Code</h2>
<div class="perk">
<p><strong>A thank-you for Mahj Matchmaker readers:</strong> use code <span class="code">MAHJMATCH</span> at {BN}. Shop through my link so the code tracks.</p>
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
