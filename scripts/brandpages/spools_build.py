# Spools brand page V1 (Nov 19 2026; Tiffany Nov 18: "Spools is a new brand", code MAHJMATCH).
# Facts only from spools.com (homepage, /pages/about-spools, product .json), read Nov 19 2026.
# NOT LIVE until MAHJMATCH is confirmed for Spools (GoAffPro). At publish: replace __LINK__ with the
# GoAffPro affiliate link and __PCT__ with the confirmed % (code-truth.json), then send her the page
# for her personal note + favorites (config/brand-page-reviews.json).
import json, re, html as H, os
REPO=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
tpl=open(f'{REPO}/brand-pages/mahj-pit.html').read()
style=re.search(r'<style.*?</style>',tpl,re.S).group(0)
E=H.escape
CDN='https://cdn.shopify.com/s/files/1/0635/1323/1443/files/'
def link(h): return f'https://spools.com/products/{h}?__LINK__'
tiles=[('travel-mahjong-tiles-3d','3D_Tiles_-_Layout.jpg?v=1785888196','3D Tiles','Raised, tactile designs that read in any light. 160 full-size tiles in 8 back colors. $320.'),
('travel-mahjong-tiles-travel-theme','Travel_Mahjong_Tiles_Compass_Tile_Layout.jpg?v=1790140180','Compass Tiles','The classic Spools set, bold and easy to read, the one they built for beginners. 6 colors. $275.'),
('floating-mahjong-tiles-pool-theme','Pool_mahjong_set_layout.jpg?v=1784497929','Pool Tiles','Sunny jokers and ocean-inspired flowers, made for poolside play. 5 colors. $275.'),
('travel-mahjong-tiles-traditional','photo-04-preview.webp?v=1795056504','Traditional Tiles','Lightweight full-size tiles that work for both American and Hong Kong style mahjong. Navy or Alpine Green. $295.'),
('travel-mahjong-tiles-christmas','christmas-mat.webp?v=1791516055','Christmas Tiles','A full Christmas theme in raised 3D designs that catch the light. $299.')]
racks=[('mahjong-travel-racks-for-full-size-tiles','Travel_Mahjong_Rack.jpg?v=1784494187','Travel Racks (Set of 4)','Each rack is 20 inches at the table and comes apart into two pieces that fit in a purse. 16 colors. $99.')]
def cards(items,kind):
    o=''
    for h,img,n,d in items:
        o+=f'''<div class="card">
<img src="{CDN}{img}" alt="Spools {E(n)}" loading="lazy">
<div class="in">
<h3>{E(n)}</h3>
<p>{E(d)}</p>
<a class="go" href="{link(h)}" target="_blank" rel="sponsored noopener">Shop it &rarr;</a>
</div>
</div>
'''
    return o
faq=[("Is there a Spools discount code?","Yes. Use code MAHJMATCH at checkout on spools.com for __PCT__ off."),
("Are Spools mahjong tiles full size?","Yes. Spools makes 160 full-size American mahjong tiles that weigh about 1.6 pounds for the whole set."),
("Do Spools tiles really float?","Spools says its tiles float and hold up to 122°F, so they can go to the pool, the hot tub or the beach."),
("Where are Spools tiles made?","Spools designs and 3D prints its tiles, racks and pushers in the USA, made to order."),
("Can Spools make custom jokers?","Yes. Spools makes custom jokers and blank tiles."),
("Can I combine the code with other offers?","Most shops allow one discount code per order, so the code usually can't be combined with a sale or another code.")]
faqh=''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>\n' for q,a in faq)
ld=json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]},ensure_ascii=False)
body=f'''{style}
<div class="mmbg">
<div class="hero">
<img src="{CDN}Travel_Mahjong_Tiles_Compass_Tile_Layout.jpg?v=1790140180" style="object-position:50% 50%" alt="Spools Compass travel mahjong tiles">
<div class="hero-txt">
<p class="eyebrow">Brand guide</p>
<h1>Spools</h1>
<p class="dek">Full-size travel mahjong tiles at about 1.6 pounds a set, designed and 3D printed in the USA. Plus, my Spools discount code for readers.</p>
</div>
</div>
<div class="perk perk-top" style="margin:22px 0 4px">
<p><strong>A thank-you for Mahj Matchmaker readers:</strong> use code <span class="code">MAHJMATCH</span> for __PCT__ off at Spools.</p>
<a class="btn" href="https://spools.com/?__LINK__" target="_blank" rel="sponsored noopener">Visit Spools</a>
</div>
<section>
<h2>About Spools</h2>
<div class="note">
<p>Spools started with Keen, its maker, and a grandmother who couldn&rsquo;t carry her 14-pound mahjong set anymore. Keen is a mechanical engineer who designed hardware for rockets, aircraft and iPads, and set out to make a set that stays full size on the table but is light in your bag.</p>
<p>Every tile, rack and pusher is designed and 3D printed in the USA and made to order. Tiles, racks and pushers weigh about 3 pounds together and pack into one tote, and the tiles float, so a set can go to the pool or the beach.</p>
</div>
</section>
<section>
<h2>Spools tile sets</h2>
<div class="grid">
{cards(tiles,"tiles")}</div>
</section>
<section>
<h2>Spools racks</h2>
<div class="grid">
{cards(racks,"racks")}</div>
</section>
<section>
<h2>Spools Discount Code</h2>
<div class="perk">
<p><strong>A thank-you for Mahj Matchmaker readers:</strong> use code <span class="code">MAHJMATCH</span> for __PCT__ off at Spools. Shop through my link so the code tracks.</p>
<a class="btn" href="https://spools.com/?__LINK__" target="_blank" rel="sponsored noopener">Visit Spools</a>
</div>
</section>
<section>
<h2>Questions about Spools</h2>
{faqh}</section>
<section>
<h2>More brands I love</h2>
<div class="more">
<a href="/oh-my-mahjong-discount-code">Oh My Mahjong</a>
<a href="/miss-mahjong-discount-code">Miss Mahjong</a>
<a href="/my-fair-mahjong-discount-code">My Fair Mahjong</a>
<a href="/bam-bird-boutique-discount-code">Bam Bird Boutique</a>
<a href="/peace-love-mahjong-discount-code">Peace Love Mahjong</a>
<a href="/mahj-mood-discount-code">Mahj Mood</a>
<a href="/mahjong-discount-codes">All brands &rarr;</a>
</div>
</section>
<p class="small">Mahj Matchmaker may earn a commission when you shop through these links, at no extra cost to you. Thank you for supporting the tile match mock-ups and inspiration I share with the community.</p>
</div>
<script type="application/ld+json">{ld}</script>
'''
open(f'{REPO}/brand-pages/spools.html','w').write(body)
json.dump({"title":"Spools Discount Code: MAHJMATCH | Mahj Matchmaker","url":"/spools-discount-code",
 "description":"Spools discount code MAHJMATCH for full-size travel mahjong tiles that weigh about 1.6 lbs and float. Made in the USA.",
 "status":"V1 built Nov 19 2026; NOT LIVE: waits on MAHJMATCH confirmation (GoAffPro). Fill __LINK__ and __PCT__ at publish."},
 open(f'{REPO}/brand-pages/spools-seo.json','w'),indent=1,ensure_ascii=False)
print('ok', len(body))
