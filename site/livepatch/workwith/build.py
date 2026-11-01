"""Build the Work With Mahj Matchmaker page, v3 (Nov 1). Built on her approved Oct 18 v2 design + her Oct 24 l-workwith6
notes + Oct 29 asks (partner / ShopMy / no-affiliation tiers, "Why affiliate programs make sense", Brands form).
Run: python3 site/livepatch/workwith/build.py <commit>
  -> workwith.html (Squarespace code block, images pinned to jsDelivr @commit) + urls.txt
  -> preview.html (self-contained artifact preview: images as data URIs, plus the Brands form + auto-reply drafts)
HARD RULES: never link/point brands to the Discount Codes page; no "Google"/SEO pitch; colour matching is never
gated by partnership; ShopMy brands are never called partners; non-partners can still get albums at her discretion."""
import sys, os, io, base64
from PIL import Image
R = '/home/claude/mahjmatchmaker-data/'
C = sys.argv[1]
J = f'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@{C}/'
SITE = 'https://www.mahjmatchmaker.com'
CARDS = [
 'assets/cards/vivienne/pippa-mahjong-tiles-oh-my-mahjong-vivienne-mat.jpg',
 'assets/cards/papaya-spritz/papaya-spritz-mahjong-tiles-anders-ruff-press-for-mahjong-mat.jpg',
 'assets/cards/papaya-spritz/papaya-spritz-mahjong-tiles-britt-mills-heiress-mat.jpg',
 'assets/cards/papaya-spritz/papaya-spritz-mahjong-tiles-mahj-and-vine-greenly-mat.jpg',
 'assets/cards/vivienne/solara-mahjong-tiles-oh-my-mahjong-vivienne-mat.jpg',
]
PHONES = 'assets/links/v2/fym-phones-trio-white-links.webp'   # real FYM screens (launch build, Oct 27)
LOGOS = 'assets/workwith/partner-logos-2026-10-30.jpg'      # logo grid cropped from assets/hub/partner-brands-2026-10-30.jpg (38 partners)
IMGS = CARDS + [PHONES, LOGOS]


def build(src):
    fan = ''.join(f'<img class="c c{i}" src="{src(c)}" alt="Mahj Matchmaker match card" loading="{"eager" if i==2 else "lazy"}">' for i, c in enumerate(CARDS))
    heart = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7.5-4.6-9.6-9.2C.9 8.4 3 4.5 6.9 4.5c2.1 0 3.6 1.2 5.1 3 1.5-1.8 3-3 5.1-3 3.9 0 6 3.9 4.5 7.3C19.5 16.4 12 21 12 21z"/></svg>'
    ic_tag = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 12V4a1 1 0 0 1 1-1h8l9 9-9 9-9-9zm5-5a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3z"/></svg>'
    ic_star = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.7-6.2 3.7 1.6-7L2 9.2l7.1-.6z"/></svg>'
    ic_book = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 4h7a3 3 0 0 1 3 3v13a2 2 0 0 0-2-2H4zm16 0h-4a3 3 0 0 0-3 3v13a2 2 0 0 1 2-2h5z"/></svg>'
    ic_link = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M10.6 13.4a1 1 0 0 1 0-1.4l3.5-3.5a1 1 0 1 1 1.4 1.4L12 13.4a1 1 0 0 1-1.4 0zM8.5 19.5a4.5 4.5 0 0 1-3.2-7.7l2.1-2.1 1.4 1.4-2.1 2.1a2.5 2.5 0 0 0 3.5 3.5l2.1-2.1 1.4 1.4-2.1 2.1a4.5 4.5 0 0 1-3.1 1.4zm8.1-5.2-1.4-1.4 2.1-2.1a2.5 2.5 0 0 0-3.5-3.5l-2.1 2.1-1.4-1.4 2.1-2.1a4.5 4.5 0 0 1 6.4 6.4z"/></svg>'
    ic_dot = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="7"/></svg>'
    Y = 'Find <em>Your</em> Mat-ch'
    return f"""<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Caprasimo&display=swap" rel="stylesheet">
<style>{CSS}</style>
<div class="mmww">
<section class="hero">
<div>
<span class="ey">For mahjong brands</span>
<h1>Let's make some matches together!</h1>
<p class="dek">Hi, I'm Tiffany! Matching tiles with the mats and racks that make them shine is my favorite thing, and I love helping players fall for brands like yours.</p>
<div class="btns"><a class="btn p" href="#ways">Ways we work together</a><a class="btn s" href="{SITE}/mahjong-tile-matches" target="_blank" rel="noopener">See the matches</a></div>
</div>
<div class="fan">{fan}</div>
</section>

<p class="intro"><span class="h">Here's what partnering with Mahj Matchmaker looks like.</span></p>

<section class="sec">
<div class="ic">{ic_star}</div>
<div class="mn">
<h2><span class="nw">Find Your</span> <span class="nw">Mat-ch™</span> <span class="badge">Live now</span></h2>
<p>{Y} is our swipe-to-match tool. Players start with the tiles they own or the mat they love, swipe through the mats and racks I'd pair with them, and save a match card pre-formatted for sharing across different platforms.</p>
<p>Every shareable match card names each product used by brand name, and many formats include the brand logos of the products used.</p>
<p>There's nothing you need to upload. If your shop runs on Shopify, I pull your catalog in automatically. If it runs on something else, I add your products by hand. With a very large line, I curate my favorites so the matching stays focused and every product gets a fair shot.</p>
<figure class="phones"><img src="{src(PHONES)}" alt="Three Find Your Mat-ch screens: choosing tiles or a mat, swiping mats, and a finished match card" loading="lazy"></figure>
<p class="cta"><a class="btn s" href="{SITE}/find-your-match" target="_blank" rel="noopener">Try {Y}</a></p>
</div>
</section>

<section class="tiers" id="tiers">
<h2>How brands show up in Find Your <span class="nw">Mat-ch</span></h2>
<p class="lead">{Y} is built for players first, so the best color match always shows up, whoever makes it. Partnership never decides whether a great match gets seen. What it changes is where your brand sits, how it's labeled, and how much I can do to send shoppers your way.</p>
<div class="tg">
<div class="tc pt">
<span class="tl">Affiliate program + code MAHJMATCH</span>
<h3>Partner brands <span class="hrt">♥</span></h3>
<ul>
<li>Top of <b>Shop by brand</b>, marked with a ♥: "Code MAHJMATCH works at brands marked ♥"</li>
<li>Shown first in color results and labeled as offering a discount with code MAHJMATCH</li>
<li>At least one match album if you sell tile sets</li>
<li>Your own brand page with my favorites and highlights, plus your logo in our partner brand lineup</li>
<li>Regular editorial consideration on the blog, in match albums and on social media</li>
</ul>
</div>
<div class="tc sm">
<span class="tl">Linked through ShopMy</span>
<h3>ShopMy brands</h3>
<ul>
<li>I link your products through ShopMy and recommend them wherever they're a great match</li>
<li>In {Y}, listed with the non-partner brands below the partners, marked "no discount available"</li>
<li>Add an affiliate program with a code any time and you move up into the partner group</li>
</ul>
</div>
<div class="tc na">
<span class="tl">No affiliation yet</span>
<h3>Every other brand</h3>
<ul>
<li>Your products can still appear when I've matched or picked them, because players deserve the best match</li>
<li>Listed below the partner brands, marked "no discount available"</li>
<li>Albums and features happen at my discretion, often from reader requests</li>
</ul>
</div>
</div>
<div class="sbb">
<div class="mock" aria-label="Illustration of the Shop by brand menu in Find Your Mat-ch">
<div class="mh"><b>Shop by brand</b><span>Code MAHJMATCH works at brands marked ♥</span></div>
<div class="row"><span>Oh My Mahjong</span><i>♥</i></div>
<div class="row"><span>Mahjong Row &amp; Co.</span><i>♥</i></div>
<div class="row"><span>Miss Mahjong</span><i>♥</i></div>
<div class="row you"><span>Your brand</span><i>♥</i></div>
<div class="mg">Non-partner brands · no discount available</div>
<div class="row dim"><span class="bar"></span></div>
<div class="row dim"><span class="bar s"></span></div>
</div>
<p class="note">To shoppers, ShopMy brands and brands with no affiliation look the same: no discount. The ♥ and the code are what set partners apart, and they're the easiest way to turn a match into a sale.</p>
</div>
</section>

<section class="why">
<h2>Why affiliate programs make sense <span>(especially for small brands)</span></h2>
<div class="wg">
<div class="wc"><div class="ic">{heart}</div><div class="mn"><h3>You pay only when you get paid</h3><p>Commission comes out of a sale that already happened. No sale, no cost.</p></div></div>
<div class="wc"><div class="ic">{ic_tag}</div><div class="mn"><h3>Zero wasted ad spend</h3><p>Ads charge for views and clicks whether anyone buys. An affiliate program never does.</p></div></div>
<div class="wc"><div class="ic">{ic_star}</div><div class="mn"><h3>About a 10x return on ad spend</h3><p>At a 10% commission, every $10 you pay out arrived with a $100 order. That's roughly a 10x return, every time.</p></div></div>
<div class="wc"><div class="ic">{ic_link}</div><div class="mn"><h3>Reach shoppers who won't pay full price</h3><p>Some shoppers wait for a code before they buy. A code gives them a reason to buy from you.</p></div></div>
<div class="wc wide"><div class="ic">{ic_dot}</div><div class="mn"><h3>Build it into your margins</h3><p>Like "free shipping," the cost lives in your pricing. There's no such thing as free marketing, and this is the kind that only costs you when it works.</p></div></div>
</div>
</section>

<section class="ways" id="ways">
<h2>Ways we work together</h2>
<div class="grid">
<div class="card"><div class="ic">{ic_tag}</div><h3>Affiliate partnership</h3><p>Discount code MAHJMATCH for our followers, a brand page of my favorites and highlights, product placement in {Y}, and regular editorial consideration for promotion on the blog, inside match albums and on social media. We focus on making your products highly shoppable with links and recommendations.</p></div>
<div class="card"><div class="ic">{ic_star}</div><h3>New Releases &amp; Restocks</h3><p>Let us know what's coming! We love hearing about new products and restocks, and we work them into matches and blog articles as they make sense. <a href="{SITE}/brand-launches">Tell me about a launch</a>.</p></div>
<div class="card"><div class="ic">{ic_book}</div><h3>Match albums</h3><p>If your brand sells tile sets, I commit to producing at least one match album for your brand. Album timing is subject to my content plan. Please share your desired tile set for album creation if you have a preference.</p></div>
</div>
</section>

<section class="logos" aria-label="Partner brands">
<span class="ey">Partner brands</span>
<img src="{src(LOGOS)}" alt="Logos of Mahj Matchmaker partner brands" loading="lazy">
</section>

<section class="faq">
<h2>FAQ</h2>
<details><summary>Do you offer paid placements?</summary><p>No. I don't offer any paid placements on the site.</p></details>
<details><summary>Will my products appear if I don't have an affiliate program?</summary><p>They can. {Y} always shows the best color matches, so products I've matched or picked can appear from any brand. Without a code, they're listed below the partner brands and marked "no discount available." An affiliate program with code MAHJMATCH moves you up into the partner group.</p></details>
<details><summary>Does every partner brand get a match album?</summary><p>If your brand sells tile sets, yes. I commit to producing at least one match album for every partner brand that sells tile sets. Album timing is subject to my content plan, so it often won't be immediate. Please share your desired tile set if you have a preference.</p><p>Beyond that, which sets get albums is my call: I weigh market demand, uniqueness, artistic quality and seasonality, plus my own taste. Our readers send album requests all the time, and I keep track of the most-requested sets and weigh that heavily. And yes, a brand can absolutely get more than one album!</p></details>
<details><summary>My shop doesn't run on Shopify. Can I still be in {Y}?</summary><p>Yes! If your shop runs on Shopify, I pull your catalog in automatically. If it runs on something else, I add your products by hand from your shop. Either way, there's nothing you need to upload.</p></details>
<details><summary>Will you review my products on your blog?</summary><p>A first-hand review means I've held it, used it or played with it, so I only write those for products I have in hand. Products can still be recommended on the site for other reasons, like how well they match. My reviews are always honest, but never harsh. I share what I love about a product, plus the helpful details shoppers need to know (like what size tiles a rack fits), so they can choose what's right for them.</p><p>When I really love something, I give it a badge on the site, like "Tiffany's Favorite," Best Value, Most Unique or Rare Edition. Just as "Tiffany's Matches" gives shoppers a confidence boost in {Y}, badges are a friendly guidepost through the many products on the market. They're reserved for things I've personally used and truly love.</p><p>But badges aren't the final word. The north star of Mahj Matchmaker is helping shoppers find <em>their</em> perfect set and accessories, not copy mine. So I leave plenty of room around my favorites to share what I genuinely like about other products too. Something that isn't on my own table might be exactly right for someone else's.</p></details>
<details><summary>Do you accept product samples or gifting?</summary><p>Yes, we do. Many brands send samples for color matching. Sample sets or swatches are very helpful for getting the best color match, but they aren't required for a partnership. If you have a new product launching soon, or simply want your products considered for personal recommendations and editorial content, feel free to send. I will always give my honest opinion. When I have a product in hand, I'm also happy to photograph it for {Y} if your brand's default product photography style or angle isn't ideal for the app.</p></details>
<details><summary>How do players find my products?</summary><p>Through your partner brand page, my tile set albums, the {Y} tool, blog articles and styled table mock-ups, social media and our Facebook group, where we share matches, real-life tables, and upcoming launches, restocks and release dates.</p></details>
<details><summary>I have an upcoming launch or restock. Can I tell you about it?</summary><p>Yes, please do! Content planning is constant for us, so the earlier you can let us know about your upcoming launches, re-launches and restocks, the better. <a href="{SITE}/brand-launches">This form</a> lands right in my social media calendar and is the best way to tell us what you have coming up.</p><p>We also subscribe to all of our partner brands' newsletters and regularly plan content around them. If you don't do a newsletter, the form is a great way to share your plans so we can help promote them. We understand some brands prefer to announce on social media to their entire audience, affiliates included. We'll do our best to keep up with those posts, but they're the least reliable way to get into our content.</p></details>
</section>

<section class="hello" id="partner">
{heart.replace('<svg ', '<svg class="h1" ')}
{heart.replace('<svg ', '<svg class="h2" ')}
<h2>Ready to partner?</h2>
<p>Affiliate programs are set up on your end. Send your affiliate invite or sign-up link to <b>mahjmatchmaker@gmail.com</b> and I'll take it from there. If your program doesn't let me create my own code, please pre-assign the code <b>MAHJMATCH</b> for my readers.</p>
<p class="sm">No affiliate program yet? Please add me to your list of interested partners, and let me know when you open one.</p>
<a class="btn" href="mailto:mahjmatchmaker@gmail.com?subject=Affiliate%20invite%20for%20Mahj%20Matchmaker">Send your invite</a>
</section>
</div>
"""


CSS = """
.mmww{--ink:#1f2f5c;--pink:#e05f86;--rose:#c8456f;--blush:#fdeef3;--cream:#fbf6ee;--line:#f0d9e1;--mute:#6f6a80;--white:#fff;color:var(--ink);font-family:inherit;line-height:1.65;font-size:17px;max-width:1100px;margin:0 auto;overflow-wrap:break-word}
.mmww *{box-sizing:border-box}
.mmww img{max-width:100%}
.mmww h1,.mmww h2,.mmww h3{font-family:'Caprasimo',Georgia,serif;font-weight:400;color:var(--pink);letter-spacing:-.01em;margin:0;text-wrap:balance}
.mmww p{margin:0 0 12px;color:var(--ink)}
.mmww a{color:var(--rose)}
.mmww .mn{min-width:0}
.mmww .nw{white-space:nowrap}
.mmww .ey{display:inline-block;text-transform:uppercase;letter-spacing:.18em;font-size:.72em;font-weight:700;color:var(--white);background:var(--ink);border-radius:999px;padding:6px 14px 5px;margin:0 0 16px}
.mmww .hero{position:relative;display:grid;grid-template-columns:1fr 1fr;gap:36px;align-items:center;background:var(--blush);border-radius:28px;padding:48px 44px;overflow:hidden}
.mmww .hero:before,.mmww .hero:after{content:"";position:absolute;border-radius:50%;background:var(--white);opacity:.55}
.mmww .hero:before{width:260px;height:260px;right:-80px;top:-90px}
.mmww .hero:after{width:160px;height:160px;left:-50px;bottom:-60px}
.mmww .hero>*{position:relative;z-index:1;min-width:0}
.mmww h1{font-size:clamp(2.1rem,4vw,3rem);line-height:1.05;margin:0 0 16px}
.mmww .dek{font-size:1.06em}
.mmww .btns{display:flex;flex-wrap:wrap;gap:12px;margin-top:20px}
.mmww .btn{display:inline-block;text-decoration:none;font-weight:700;border-radius:999px;padding:13px 26px;font-size:.95em;transition:transform .15s}
.mmww .btn:hover{transform:translateY(-2px)}
.mmww .btn:focus-visible{outline:3px solid var(--ink);outline-offset:3px}
.mmww .btn.p{background:var(--pink);color:var(--white);box-shadow:0 6px 16px rgba(224,95,134,.35)}
.mmww .btn.s{background:var(--white);color:var(--ink);border:2px solid var(--ink)}
.mmww .fan{position:relative;height:430px}
.mmww .fan .c{position:absolute;width:44%;left:28%;top:34px;border-radius:12px;box-shadow:0 14px 30px rgba(31,47,92,.25);border:5px solid var(--white);background:var(--white)}
.mmww .fan .c0{transform:rotate(-16deg) translate(-56%,24px)}
.mmww .fan .c1{transform:rotate(-8deg) translate(-28%,6px)}
.mmww .fan .c2{transform:rotate(0);z-index:3}
.mmww .fan .c3{transform:rotate(8deg) translate(28%,6px)}
.mmww .fan .c4{transform:rotate(16deg) translate(56%,24px)}
.mmww .fan .c1,.mmww .fan .c3{z-index:2}
.mmww .intro{text-align:center;max-width:720px;margin:44px auto 8px;font-size:1.08em}
.mmww .intro .h{color:var(--pink);font-family:'Caprasimo',Georgia,serif;font-size:1.3em}
.mmww .sec{display:grid;grid-template-columns:72px minmax(0,1fr);gap:22px;align-items:start;background:var(--white);border:2px solid var(--line);border-radius:24px;padding:32px 34px;margin:26px 0}
.mmww .sec .ic{width:72px;height:72px;border-radius:50%;background:var(--blush);display:flex;align-items:center;justify-content:center}
.mmww .sec .ic svg{width:34px;height:34px;fill:var(--pink)}
.mmww h2{font-size:clamp(1.55rem,2.6vw,2rem);line-height:1.15;margin:0 0 12px}
.mmww .badge{display:inline-block;background:var(--pink);color:var(--white);font-weight:700;font-size:.42em;letter-spacing:.12em;text-transform:uppercase;border-radius:999px;padding:5px 12px 4px;vertical-align:middle;margin-left:6px;font-family:inherit}
.mmww .phones{margin:14px auto 4px;max-width:640px}
.mmww .phones img{display:block;width:100%;height:auto}
.mmww .cta{text-align:center;margin:8px 0 0}
.mmww .tiers{margin:44px 0}
.mmww .tiers>h2{text-align:center}
.mmww .lead{max-width:760px;margin:0 auto 22px;text-align:center;font-size:1.04em}
.mmww .tg{display:grid;grid-template-columns:1.25fr 1fr 1fr;gap:18px;align-items:start}
.mmww .tc{border-radius:22px;padding:24px 22px 10px;background:var(--cream);border:2px solid var(--line);min-width:0}
.mmww .tc.pt{background:var(--blush);border-color:var(--pink)}
.mmww .tl{display:inline-block;font-size:.68em;font-weight:800;letter-spacing:.14em;text-transform:uppercase;border-radius:999px;padding:4px 11px 3px;margin-bottom:10px;background:var(--white);color:var(--mute)}
.mmww .tc.pt .tl{background:var(--pink);color:var(--white)}
.mmww .tc h3{font-size:1.35rem;margin-bottom:8px}
.mmww .tc.sm h3,.mmww .tc.na h3{color:var(--ink)}
.mmww .hrt{color:var(--pink)}
.mmww .tc ul{margin:0;padding:0 0 0 1.1em;font-size:.95em}
.mmww .tc li{margin:0 0 9px}
.mmww .tc.pt li::marker{color:var(--pink)}
.mmww .sbb{display:grid;grid-template-columns:minmax(0,320px) minmax(0,1fr);gap:26px;align-items:center;max-width:860px;margin:26px auto 0}
.mmww .mock{background:var(--white);border:2px solid var(--line);border-radius:18px;padding:14px 14px 10px;box-shadow:0 10px 24px rgba(31,47,92,.10);font-size:.9em}
.mmww .mh{display:flex;flex-direction:column;padding:2px 4px 10px;border-bottom:1px solid var(--line);margin-bottom:6px}
.mmww .mh b{font-family:'Caprasimo',Georgia,serif;font-weight:400;color:var(--ink);font-size:1.15em}
.mmww .mh span{font-size:.85em;color:var(--mute)}
.mmww .row{display:flex;justify-content:space-between;align-items:center;padding:7px 8px;border-radius:10px}
.mmww .row i{font-style:normal;color:var(--pink);font-weight:700}
.mmww .row.you{background:var(--blush);border:2px dashed var(--pink);font-weight:700}
.mmww .mg{font-size:.72em;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--mute);padding:10px 8px 4px;border-top:1px solid var(--line);margin-top:6px}
.mmww .row.dim .bar{display:block;height:10px;width:62%;border-radius:6px;background:var(--line)}
.mmww .row.dim .bar.s{width:44%}
.mmww .note{font-size:1.02em;margin:0}
.mmww .why{background:var(--ink);border-radius:28px;padding:38px 34px;margin:44px 0}
.mmww .why h2{color:var(--white);text-align:center;margin-bottom:22px}
.mmww .why h2 span{display:block;font-family:inherit;font-size:.5em;letter-spacing:.06em;color:#f7b6c8;margin-top:6px}
.mmww .wg{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}
.mmww .wc{display:grid;grid-template-columns:44px minmax(0,1fr);gap:14px;align-items:start;background:var(--white);border-radius:18px;padding:18px 20px}
.mmww .wc.wide{grid-column:1/-1}
.mmww .wc .ic{width:44px;height:44px;border-radius:50%;background:var(--blush);display:flex;align-items:center;justify-content:center}
.mmww .wc .ic svg{width:22px;height:22px;fill:var(--pink)}
.mmww .wc h3{font-size:1.18rem;line-height:1.2;margin:0 0 4px}
.mmww .wc p{margin:0;font-size:.96em}
.mmww .ways{margin:44px 0}
.mmww .ways>h2{text-align:center;margin-bottom:22px}
.mmww .grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}
.mmww .card{background:var(--cream);border-radius:22px;padding:26px 24px;position:relative;border-top:6px solid var(--pink);min-width:0}
.mmww .card:nth-child(2){border-top-color:var(--ink)}
.mmww .card .ic{width:48px;height:48px;border-radius:50%;background:var(--white);display:flex;align-items:center;justify-content:center;margin-bottom:12px}
.mmww .card .ic svg{width:24px;height:24px;fill:var(--pink)}
.mmww .card:nth-child(2) .ic svg{fill:var(--ink)}
.mmww h3{font-size:1.3rem;line-height:1.2;margin:0 0 8px}
.mmww .card p{font-size:.96em;margin:0}
.mmww .logos{background:var(--ink);border-radius:24px;padding:26px 24px 24px;margin:44px 0;text-align:center}
.mmww .logos .ey{background:var(--pink)}
.mmww .logos img{display:block;width:100%;max-width:720px;height:auto;margin:0 auto;border-radius:16px}
.mmww .faq{margin:44px 0}
.mmww .faq>h2{text-align:center;margin-bottom:18px}
.mmww details{background:var(--white);border:2px solid var(--line);border-radius:18px;margin:0 0 12px;overflow:hidden}
.mmww summary{list-style:none;cursor:pointer;font-weight:700;font-size:1.04em;padding:18px 58px 18px 22px;position:relative;color:var(--ink)}
.mmww summary:focus-visible{outline:3px solid var(--pink);outline-offset:-3px}
.mmww summary::-webkit-details-marker{display:none}
.mmww summary:after{content:"+";position:absolute;right:20px;top:50%;transform:translateY(-50%);width:28px;height:28px;border-radius:50%;background:var(--blush);color:var(--pink);font-size:22px;line-height:28px;text-align:center;font-weight:700}
.mmww details[open] summary:after{content:"\\2013"}
.mmww details[open]{border-color:var(--pink)}
.mmww details p{padding:0 22px 14px;margin:0}
.mmww .hello{background:var(--pink);border-radius:28px;padding:40px 30px;text-align:center;margin:44px 0 10px;position:relative;overflow:hidden}
.mmww .hello h2{color:var(--white);font-size:clamp(2rem,4vw,2.8rem);margin-bottom:10px}
.mmww .hello p{color:var(--white);font-size:1.08em;margin:0 auto 14px;max-width:760px;position:relative}
.mmww .hello p.sm{font-size:.98em;opacity:.95;margin-bottom:20px}
.mmww .hello .btn{background:var(--white);color:var(--pink);position:relative}
.mmww .hello svg{position:absolute;width:120px;height:120px;fill:rgba(255,255,255,.14)}
.mmww .hello .h1{left:-20px;top:-20px;transform:rotate(-18deg)}
.mmww .hello .h2{right:-16px;bottom:-24px;transform:rotate(16deg)}
@media (prefers-reduced-motion:reduce){.mmww .btn{transition:none}.mmww .btn:hover{transform:none}}
@media (max-width:900px){.mmww .tg{grid-template-columns:1fr}.mmww .sbb{grid-template-columns:1fr}.mmww .mock{max-width:340px;margin:0 auto;width:100%}}
@media (max-width:820px){
 .mmww{font-size:16px}
 .mmww .hero{grid-template-columns:1fr;padding:34px 22px 18px;text-align:center}
 .mmww .btns{justify-content:center}
 .mmww .fan{height:270px;max-width:400px;margin:0 auto;width:100%}
 .mmww .fan .c{width:50%;left:25%;top:20px}
 .mmww .sec{grid-template-columns:1fr;padding:26px 20px;gap:12px}
 .mmww .sec .ic{width:58px;height:58px}
 .mmww .grid{grid-template-columns:1fr}
 .mmww .why{padding:30px 18px}
 .mmww .wg{grid-template-columns:1fr}
 .mmww .logos{padding:22px 14px}
}
"""

# ---------- Brands form + auto-reply + launch form (shown in the preview so she approves the words; staged in README/emails.md)
FORM_HTML = """
<section class="pvx" id="form">
<h2>Not on the page: the footer link, the Brands form and the reply email</h2>
<p>How brands reach the page: <b>footer "Brands" link → /brands form → automatic reply email → /work-with-us</b> (hidden from menus and Google). Nothing here is live. These are the words for your OK.</p>
<div class="pvg">
<div class="pvc">
<h3>Brands form (/brands)</h3>
<p class="k">Title</p><p>Work with Mahj Matchmaker</p>
<p class="k">Intro</p><p>Love what you see? Tell me a little about your brand and I'll send over everything you need to know about partnering with Mahj Matchmaker.</p>
<p class="k">Fields</p>
<ol>
<li>Brand name (required)</li>
<li>Your name (required)</li>
<li>Email (required, so the reply can send)</li>
<li>Website or shop link (required)</li>
<li>What do you make? Tiles · Mats · Racks · Accessories · Other</li>
<li>Do you have an affiliate program? Yes, with a discount code · Yes, without a code · We're on ShopMy · Not yet</li>
<li>Anything else you'd like me to know? (optional)</li>
</ol>
<p class="k">Button</p><p>Send</p>
<p class="k">After they send</p><p>Thank you! Check your inbox. I've just sent over how partnering with Mahj Matchmaker works.</p>
</div>
<div class="pvc">
<h3>Automatic reply email</h3>
<p class="k">Subject</p><p>Thanks for reaching out to Mahj Matchmaker!</p>
<div class="mail">
<p>Hi [first name],</p>
<p>Thank you so much for reaching out! Everything you need to know about partnering with Mahj Matchmaker is here, including how brands show up in Find Your Mat-ch™ and why an affiliate program can make sense for a small brand:<br>www.mahjmatchmaker.com/work-with-us</p>
<p>Ready to partner? Affiliate programs are set up on your end, so just send your affiliate invite or sign-up link to mahjmatchmaker@gmail.com and I'll take it from there. If you don't have a program yet, please add me to your list of interested partners.</p>
<p>Talk soon,<br>Tiffany<br>Mahj Matchmaker</p>
</div>
<p class="k">Sends from</p><p>A Squarespace Email Campaigns automation on the Brands form, built as a draft for your final read. Nothing sends until you OK it there.</p>
</div>
<div class="pvc">
<h3>Launch &amp; restock form (/brand-launches)</h3>
<p>The page's "Tell me about a launch" links go here. Partners and brands use it to put a launch on our content calendar.</p>
<ol>
<li>Brand name (required)</li>
<li>Your name (required)</li>
<li>Email (required)</li>
<li>What's coming? New release · Restock · Re-launch · Sale · Other</li>
<li>Product name(s) (required)</li>
<li>Date it goes live (required)</li>
<li>Product or preview link</li>
<li>Link to photos (optional)</li>
<li>Anything else? (optional)</li>
</ol>
<p class="k">After they send</p><p>Got it, thank you! I'll work it into my content plan.</p>
<p class="k">Where answers go</p><p>Filed away from your inbox; Claude reads them every morning and puts each launch on the social calendar and HQ.</p>
</div>
</div>
</section>
"""

PV_CSS = """
:root{--pv-bg:#f6f1f4;--pv-fg:#2c2a3a;--pv-mute:#6f6670;--pv-card:#ffffff;--pv-line:#e7cbd6;--pv-accent:#c8456f;--site:#ffffff}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--pv-bg:#17161f;--pv-fg:#ece8f0;--pv-mute:#b6adbb;--pv-card:#221f2c;--pv-line:#4a3a46;--pv-accent:#f08fb0;color-scheme:dark}}
:root[data-theme="dark"]{--pv-bg:#17161f;--pv-fg:#ece8f0;--pv-mute:#b6adbb;--pv-card:#221f2c;--pv-line:#4a3a46;--pv-accent:#f08fb0;color-scheme:dark}
body{margin:0;background:var(--pv-bg);color:var(--pv-fg);font-family:Poppins,system-ui,-apple-system,sans-serif;padding-block:20px 40px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));overflow-x:hidden}
.pv{max-width:1100px;margin:0 auto 16px;font-size:14px;line-height:1.55;color:var(--pv-fg)}
.pv h1{font-family:Caprasimo,Georgia,serif;font-weight:400;color:var(--pv-accent);font-size:1.6rem;margin:0 0 6px}
.pv ul{margin:6px 0 0;padding-left:1.2em}
.pv li{margin:0 0 4px}
.pv .tag{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--pv-mute);margin-bottom:6px}
.site{background:var(--site);border-radius:20px;padding-block:24px;padding-left:max(12px,2vw);padding-right:max(12px,2vw);max-width:1160px;margin:0 auto}
.pvx{max-width:1100px;margin:22px auto 0;color:var(--pv-fg);font-size:14px;line-height:1.55}
.pvx h2{font-family:Caprasimo,Georgia,serif;font-weight:400;color:var(--pv-accent);font-size:1.35rem;margin:0 0 6px}
.pvg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-top:12px}
.pvc{background:var(--pv-card);border:2px dashed var(--pv-line);border-radius:18px;padding:18px;min-width:0}
.pvc h3{margin:0 0 8px;font-size:1.02rem}
.pvc p{margin:0 0 8px}
.pvc ol{margin:0 0 10px;padding-left:1.2em}
.pvc .k{font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--pv-mute);margin:10px 0 2px}
.mail{border-left:3px solid var(--pv-line);padding-left:12px;margin:8px 0}
@media (max-width:900px){.pvg{grid-template-columns:1fr}}
"""

PV_HEAD = """<title>Work With Preview</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>""" + PV_CSS + """</style>
<div class="pv">
<span class="tag">Preview v3 · for your approval · not live</span>
<h1>Work With Mahj Matchmaker</h1>
<p>The hidden page brands get from the footer "Brands" form (and that you can paste into affiliate applications). What's new since the Oct 18 version:</p>
<ul>
<li><b>How brands show up in Find Your Mat-ch:</b> partner brands (code MAHJMATCH, ♥, shown first), ShopMy brands, and brands with no affiliation (only when you matched or picked them, below partners). Framed as a reason to affiliate, never a threat.</li>
<li><b>New section:</b> "Why affiliate programs make sense (especially for small brands)", from your Oct 29 points.</li>
<li><b>Your Oct 24 notes applied:</b> "shoppable", New Releases &amp; Restocks, the album promise, gifting, non-Shopify shops, match cards name every brand, launch/restock form, FAQ without the Discount Codes page.</li>
<li><b>Fixed:</b> the partner logo strip had empty boxes; it's now one logo image (38 partners). "Coming 10.27" is gone (the tool is live) and the screens are the real launch app.</li>
<li>The Brands form, reply email and launch form text are below the page.</li>
</ul>
</div>
<div class="site">
"""


def data_uri(path):
    p = R + path
    if path.endswith('.webp'):
        return 'data:image/webp;base64,' + base64.b64encode(open(p, 'rb').read()).decode()
    im = Image.open(p).convert('RGB')
    w = 520 if '/cards/' in path else 900
    if im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'JPEG', quality=82, optimize=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()


D = os.path.dirname(os.path.abspath(__file__))
HTML = build(lambda p: J + p)
open(os.path.join(D, 'workwith.html'), 'w').write(HTML)
open(os.path.join(D, 'urls.txt'), 'w').write('\n'.join(J + p for p in IMGS) + '\n')
cache = {}
PV = PV_HEAD + build(lambda p: cache.setdefault(p, data_uri(p))) + '</div>\n' + FORM_HTML
open(os.path.join(D, 'preview.html'), 'w').write(PV)
print('ok', len(HTML), 'preview', len(PV))
