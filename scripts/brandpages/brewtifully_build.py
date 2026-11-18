# Brewtifully brand page (Tiffany Nov 18 2026 5:17-5:19am direction).
# - No tile sets as favorites: "Brewtifully sells more than 100 tile sets. Here are a few examples." (2 shown: Folk Dragon + Ohio MRAP Veteran).
# - Mats: her 3 picks (Folk Art Autumn Love, Christmas Memories and Traditions, Kaua'i Memories), photos cropped clean.
# - Talk about Tracy as a real artist, the satin-smooth finish, sizes travel to 33", 2mm vs 3mm (2mm = budget, more prone to wrinkling), affordability.
import json, re, html as H, sys, os, base64
REPO=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
commit=sys.argv[1]; preview_out=sys.argv[2] if len(sys.argv)>2 else None
tpl=open(f'{REPO}/brand-pages/mahj-pit.html').read()
style=re.search(r'<style.*?</style>',tpl,re.S).group(0)
REF='sca_ref=12791501.UkLEYdzzWXP'
CDN=f'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@{commit}/assets/brand-pages/brewtifully/'
def link(h): return f'https://shop.brewtifully.com/products/{h}?{REF}'
E=H.escape
tiles=[('folk-dragon-american-mahjong-tiles','folk-dragon-tiles.jpg','Folk Dragon Tiles','Dragons drawn in her folk-art style on a dark green back. Bag or box set, $350.'),
('veteran-american-mahjong-tiles','veteran-tiles.jpg','Ohio MRAP Veteran-Inspired Tiles','A veteran-inspired set in green and black, a good pick for the men at your table. Bag or box set, $350.')]
mats=[('mahjong-mat-made-in-usa-folkarts-autumn-love','folk-art-autumn-love.jpg','Folk Art Autumn Love','Warm folk-art florals in rust, plum and olive. Rubber-backed, made in the USA, in 20.9", 26", 31.5" and 33", 2mm or 3mm. From $45.'),
('mahjong-mat-sleeksurface-made-in-usa-christmas-memories-and-traditions','christmas-memories.jpg','Christmas Memories and Traditions','A navy holiday mat full of Christmas-movie nods: the lit-up house, the RV, the station wagon with the tree. SleekSurface, 31.5" or 33". $95.'),
('mahjong-mat-sleeksurface-made-in-usa-kaua-i-memories','kauai-memories.jpg',"Kauaʻi Memories",'Hand-painted waterfalls, red blooms and roosters on aqua. SleekSurface, 31.5" or 33". $95.')]
def cards(items,kind):
    o=''
    for h,img,n,d in items:
        o+=f'''<div class="card">
<img src="{CDN}{img}" alt="Brewtifully {E(n)} mahjong {kind}" loading="lazy"{' style="aspect-ratio:1/1"' if kind=="mat" else ""}>
<div class="in">
<h3>{E(n)}</h3>
<p>{E(d)}</p>
<a class="go" href="{link(h)}" target="_blank" rel="sponsored noopener">Shop it &rarr;</a>
</div>
</div>
'''
    return o
faq=[("Is there a Brewtifully discount code?","Yes. Use code MAHJMATCH at checkout on shop.brewtifully.com for 15% off."),
("Who makes Brewtifully mahjong mats?","Tracy Dawn Brewer, a surface pattern designer and painter. Every Brewtifully design starts as her own hand-drawn, hand-painted artwork."),
("What sizes do Brewtifully mahjong mats come in?","From 20.9\" travel mats through 26\" and 31.5\" full size up to 33\", with 32\" round on some designs. Many come in 2mm or 3mm thickness."),
("Should I get a 2mm or 3mm Brewtifully mat?","2mm is the budget-friendly, lighter choice but is more prone to wrinkling. 3mm lies flatter and cushions the tiles more."),
("What is a SleekSurface mat?","Brewtifully's SleekSurface mats have a smooth, satiny finish over a rubber backing, made in the USA. They ship rolled, so unroll and let them lie flat for a few minutes."),
("Does Brewtifully make custom mahjong mats?","Yes. Tracy makes custom mats for players, clubs, organizations and events, and her art is in a 57-mat collection with Mahjong by SI."),
("Can I combine the code with other offers?","Most shops allow one discount code per order, so the code usually can't be combined with a sale or another code.")]
faqh=''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>\n' for q,a in faq)
ld=json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]},ensure_ascii=False)
body=f'''{style}
<div class="mmbg">
<div class="hero">
<img src="{CDN}kauai-memories.jpg" style="object-position:50% 50%" alt="Brewtifully Kauai Memories mahjong mat">
<div class="hero-txt">
<p class="eyebrow">Brand guide</p>
<h1>Brewtifully</h1>
<p class="dek">Hand-painted mahjong mats from artist Tracy Dawn Brewer, from budget-friendly travel mats to satin-smooth 33&quot; mats. Plus, my Brewtifully discount code for readers.</p>
</div>
</div>
<div class="perk perk-top" style="margin:22px 0 4px">
<p><strong>A thank-you for Mahj Matchmaker readers:</strong> use code <span class="code">MAHJMATCH</span> for 15% off at Brewtifully.</p>
<p style="font-size:14px;opacity:.75;margin:6px 0 14px">&#10003; Brewtifully discount code: MAHJMATCH &middot; 15% off &middot; verified November 18, 2026</p>
<a class="btn" href="https://shop.brewtifully.com/?{REF}" target="_blank" rel="sponsored noopener">Visit Brewtifully</a>
</div>
<section>
<h2>About Brewtifully</h2>
<div class="note">
<p>Brewtifully is the work of Tracy Dawn Brewer, a real working artist: a surface pattern designer and painter who has sold her own patterns for more than a decade. Every mat starts as her hand-drawn or hand-painted artwork, from folk-art florals to painted landscapes and holiday scenes. She taught art at the Canton Museum of Art in Ohio, paints murals and now works from her studio in Seattle.</p>
<p>Her mats are made to order, so you choose the design, size and thickness. Her art also shows up beyond her own shop: a 57-mat collection with Mahjong by SI, and Miss Mahjong&rsquo;s Deep Green Garden Party mat, reproduced from one of her paintings.</p>
</div>
</section>
<section>
<h2>Brewtifully mahjong mats</h2>
<div class="note">
<p><strong>A satin-smooth finish.</strong> Her SleekSurface mats have a smooth, satiny fabric surface over a rubber backing, made in the USA, and it&rsquo;s a finish people really like at the table. She also offers satin-smooth neoprene mats with stitched edges.</p>
<p><strong>Every size, and a price for every budget.</strong> Mats run from 20.9&quot; travel mats through 26&quot;, 31.5&quot; full size and 33&quot;, with a 32&quot; round on some designs. Rubber-backed mats start around $45 and SleekSurface mats are $95. Many come in 2mm or 3mm: the 2mm is the budget-conscious choice, but it&rsquo;s thinner and more prone to wrinkling, so choose 3mm if you want it to lie flatter.</p>
</div>
<p>A few of my picks:</p>
<div class="grid">
{cards(mats,"mat")}</div>
</section>
<section>
<h2>Brewtifully tile sets</h2>
<p>Brewtifully sells more than 100 tile set designs. Here are a few examples:</p>
<div class="grid">
{cards(tiles,"tiles")}</div>
</section>
<section>
<h2>Brewtifully Discount Code</h2>
<div class="perk">
<p><strong>A thank-you for Mahj Matchmaker readers:</strong> use code <span class="code">MAHJMATCH</span> for 15% off at Brewtifully. Shop through my link so the code tracks.</p>
<a class="btn" href="https://shop.brewtifully.com/?{REF}" target="_blank" rel="sponsored noopener">Visit Brewtifully</a>
</div>
</section>
<section>
<h2>Questions about Brewtifully</h2>
{faqh}</section>
<section>
<h2>More brands I love</h2>
<div class="more">
<a href="/oh-my-mahjong-discount-code">Oh My Mahjong</a>
<a href="/miss-mahjong-discount-code">Miss Mahjong</a>
<a href="/mahjong-by-si-discount-code">Mahjong by SI</a>
<a href="/my-fair-mahjong-discount-code">My Fair Mahjong</a>
<a href="/bird-and-bamboo-discount-code">Bird &amp; Bamboo</a>
<a href="/mahj-mood-discount-code">Mahj Mood</a>
<a href="/noli-june-discount-code">Noli June</a>
<a href="/mahjong-discount-codes">All brands &rarr;</a>
</div>
</section>
<p class="small">Mahj Matchmaker may earn a commission when you shop through these links, at no extra cost to you. Thank you for supporting the tile match mock-ups and inspiration I share with the community.</p>
</div>
<script type="application/ld+json">{ld}</script>
'''
open(f'{REPO}/brand-pages/brewtifully.html','w').write(body)
if preview_out:
    pv=body
    for f in os.listdir(f'{REPO}/assets/brand-pages/brewtifully'):
        pv=pv.replace(CDN+f,'data:image/jpeg;base64,'+base64.b64encode(open(f'{REPO}/assets/brand-pages/brewtifully/{f}','rb').read()).decode())
    open(preview_out,'w').write('<title>Brewtifully Page Preview</title><meta name="viewport" content="width=device-width,initial-scale=1"><style>:root{--bg:#faf3ea}body{background:var(--bg);margin:0}.bar{background:#054689;color:#fff;font:600 15px Helvetica;padding:12px 16px}.wrap{max-width:980px;margin:0 auto;padding:0 16px}</style><div class="bar">Preview of mahjmatchmaker.com/brewtifully-discount-code (v2, not live yet)</div><div class="wrap">'+pv+'</div>')
print('ok')
