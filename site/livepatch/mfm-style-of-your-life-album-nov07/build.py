"""My Fair Mahjong The Style of Your Life Series (Pearl Green) album review page (Nov 7, built like Juniper:
site/livepatch/juniper-album-nov06/build.py). Faces picker (4 hearts -> Copy my picks), cover, color card + wheel + theory,
Juniper overlap + timing, all match cards (Claude's round-1 order). Images = jsDelivr pinned SHA, or 'local' = relative paths.
Usage: python3 build.py <commit sha|local> <out.html>"""
import json, sys, html
CSS = '<style>\n:root{--bg:#f6ece2;--card:#fffaf5;--ink:#0b3f78;--muted:#5a6b85;--pink:#c8325f;--line:#e6d6c8;--acc:#0b6b3a;--chip:#fdf0f3}\n@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#13202e;--card:#1b2b3c;--ink:#e9eef6;--muted:#a8b4c6;--pink:#ff8fb0;--line:#2c3e52;--acc:#7fd19c;--chip:#2a2030}}\n:root[data-theme="dark"]{--bg:#13202e;--card:#1b2b3c;--ink:#e9eef6;--muted:#a8b4c6;--pink:#ff8fb0;--line:#2c3e52;--acc:#7fd19c;--chip:#2a2030}\n*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 Bitter,Georgia,serif}\n.wrap{max-width:760px;margin:0 auto;padding:18px 16px 120px}\n.kick{font:700 12px Bitter;letter-spacing:.18em;text-transform:uppercase;color:var(--pink);margin:0}\nh1{font:400 40px/1.05 Caprasimo;margin:6px 0 8px;color:var(--acc)}h2{font:400 28px/1.1 Caprasimo;margin:38px 0 6px;scroll-margin-top:12px}\n.lede{margin:0 0 12px;color:var(--muted)}\nnav{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0 4px}nav a{background:var(--card);border:1px solid var(--line);border-radius:999px;padding:6px 12px;color:var(--ink);text-decoration:none;font-weight:600;font-size:14px}\n.note{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px;margin:12px 0}\n.note p{margin:0 0 8px}.note p:last-child{margin:0}\nh3.fg{font:700 13px Bitter;letter-spacing:.16em;text-transform:uppercase;color:var(--pink);margin:26px 0 10px}h3.fg small{display:block;letter-spacing:0;text-transform:none;font:italic 15px \'Playfair Display\';color:var(--muted);margin-top:2px}\n.fgrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.fgrid.sm{grid-template-columns:repeat(3,minmax(0,1fr))}\n@media(min-width:640px){.fgrid{grid-template-columns:repeat(3,minmax(0,1fr))}.fgrid.sm{grid-template-columns:repeat(5,minmax(0,1fr))}}\n.face{position:relative;margin:0;display:flex;flex-direction:column;justify-content:space-between;background:var(--card);border:2px solid var(--line);border-radius:16px;padding:10px 10px 12px}\n.face.cp{border-color:var(--acc)}.face.on{border-color:var(--pink);box-shadow:0 0 0 3px var(--pink)}\n.fimg{background:#1d3a5c;border-radius:12px;padding:8px;display:flex;justify-content:center}.fimg img{width:100%;max-width:220px;height:auto;display:block;cursor:zoom-in}\n.face figcaption{margin-top:8px;font-size:14px;line-height:1.35}.face figcaption b{display:block}\n.face em{display:block;font:italic 14px/1.35 \'Playfair Display\';color:var(--muted);margin-top:4px}\n.badge{display:inline-block;margin-top:6px;background:var(--acc);color:#fff;border-radius:999px;padding:2px 9px;font:700 11px Bitter;letter-spacing:.08em;text-transform:uppercase}\n.heart{display:block;width:100%;margin-top:10px;min-height:44px;border-radius:999px;border:2px solid var(--pink);background:transparent;color:var(--pink);font:700 15px Bitter;cursor:pointer}\n.heart[aria-pressed="true"]{background:#f56c8c;border-color:#f56c8c;color:#fff}\n.heart:after{content:\' Pick\'}.heart[aria-pressed="true"]:after{content:\' Picked\'}\n.bar{position:fixed;left:0;right:0;bottom:0;background:var(--card);border-top:1px solid var(--line);padding:10px 16px calc(10px + env(safe-area-inset-bottom));display:flex;gap:10px;align-items:center;justify-content:space-between;z-index:5}\n.bar span{font-weight:700;font-size:14px;min-width:0;overflow-wrap:anywhere}.bar button{flex:0 0 auto;background:var(--pink);color:#fff;border:0;border-radius:999px;padding:10px 16px;font:700 14px Bitter}\n.big{width:100%;height:auto;display:block;border-radius:14px;cursor:zoom-in;margin:8px 0}\n.two{display:grid;grid-template-columns:1fr;gap:12px}@media(min-width:640px){.two{grid-template-columns:1fr 1fr}}\n.car{display:flex;gap:10px;overflow-x:auto;scroll-snap-type:x mandatory;padding-bottom:8px}.slide{flex:0 0 78%;scroll-snap-align:start;position:relative}.slide img{width:100%;border-radius:12px;display:block;cursor:zoom-in}\n.slide span{position:absolute;top:8px;left:8px;background:var(--ink);color:var(--bg);border-radius:999px;padding:2px 9px;font-weight:700;font-size:13px}\n.mcard{background:var(--card);border:1px solid var(--line);border-radius:16px;overflow:hidden;margin:0 0 16px}.mcard img{width:100%;height:auto;display:block;cursor:zoom-in}\n.mt{padding:12px 14px 14px}.mt h4{font:400 24px/1.1 Caprasimo;margin:0}.num{margin:0 0 4px;font:700 12px Bitter;letter-spacing:.12em;color:var(--muted)}\n.ret{background:var(--muted);color:var(--card);border-radius:999px;padding:1px 8px;font-size:11px}.bn{margin:2px 0 6px;color:var(--muted);font-weight:600}.why{margin:0 0 8px}.rk{margin:0;font-size:14px;color:var(--muted)}\n.draft{display:inline-block;background:var(--ink);color:var(--bg);border-radius:999px;padding:2px 10px;font:700 11px Bitter;letter-spacing:.1em;vertical-align:middle}\n.lb{position:fixed;inset:0;background:rgba(0,0,0,.9);display:none;align-items:center;justify-content:center;z-index:9;padding:12px}.lb.on{display:flex}.lb img{max-width:100%;max-height:100%;object-fit:contain}\nul{padding-left:20px;margin:6px 0}li{margin:3px 0}\n</style>\n<style>.ov{width:100%;border-collapse:collapse;font-size:14px;margin:8px 0}.ov th,.ov td{border-bottom:1px solid var(--line);padding:6px 4px;text-align:left;vertical-align:top}.ov th{font:700 12px Bitter;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}.tw{overflow-x:auto}.racks{background:#1d3a5c;border-radius:12px;padding:12px;display:grid;gap:10px}.racks img{width:100%;height:auto;display:block}</style>'
R = '/home/claude/mahjmatchmaker-data/'
SHA, OUT = sys.argv[1], sys.argv[2]
CDN = '' if SHA == 'local' else f'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@{SHA}/'
e = html.escape
MAN = json.load(open(R + 'assets/cards/style-of-your-life/manifest.json'))['cards']
F = 'assets/tiles/faces/style-of-your-life/clean/'
CLAUDE = {
 'dragon-green': "Pair them: the dragon sitting on a stack of cash, asking if you can pay for it. The funniest tile in the set.",
 'dragon-red': "Pair them: the wine dragon on a credit card, the other half of the joke.",
 'bam-1': "The signature tile: a hummingbird mistaking the shoe's pink puff for a flower.",
 'joker-7': "Makeup counter joker: one red lipstick. The cleanest pop of her wine on a white face.",
 'crak-9': "The bubblegum pink hobo bag: her pink at its biggest.",
}
G = [
 ('Dragons', 'The retail dragons: can you pay for it?', [('dragon-green', 'Green Dragon: on a stack of cash'), ('dragon-red', 'Red Dragon: on a credit card'), ('dragon-white', 'White Dragon (soap): a powder blue pearl strand')]),
 ('Bird bam', 'The shoe department', [('bam-1', '1 Bam: hummingbird + shoe')]),
 ('Jokers', 'The departments (10 designs)', [('joker-1', 'Joker: Accessories (sunglasses)'), ('joker-2', "Joker: Men's (shirt + tie)"), ('joker-3', 'Joker: Wedding Registry (champagne)'), ('joker-4', 'Joker: Gift Wrap'), ('joker-5', 'Joker: Pajamas (robe)'), ('joker-6', 'Joker: Bedding'), ('joker-7', 'Joker: Makeup (lipstick)'), ('joker-8', 'Joker: Luggage'), ('joker-9', 'Joker: Perfume'), ('joker-10', 'Joker: Table Top')]),
 ('Flowers', 'Floral-dressed mannequins', [(f'flower-{i}', f'Flower {i}') for i in range(1, 9)]),
 ('Winds', 'Escalators', [('wind-north', 'North: mother + daughter'), ('wind-east', 'East: a woman perusing'), ('wind-west', 'West: the waving man'), ('wind-south', 'South: a successful day')]),
 ('Craks', 'Handbags', [(f'crak-{i}', f'{i} Crak') for i in range(1, 10)]),
 ('Dots', 'Jewelry', [(f'dot-{i}', f'{i} Dot') for i in range(1, 10)]),
 ('Bams', 'Shoe racks', [(f'bam-{i}', f'{i} Bam') for i in range(2, 10)]),
]
def img(p, alt, cls='', lazy=True):
    return f'<img src="{CDN}{p}" alt="{e(alt)}"{" loading=lazy" if lazy else ""} class="{cls}" data-zoom>'
faces = ''
for title, sub, items in G:
    small = title in ('Dots', 'Bams', 'Craks', 'Flowers', 'Jokers')
    cards = ''
    for k, name in items:
        why = CLAUDE.get(k)
        cards += (f'<figure class="face{" cp" if why else ""}" data-key="{k}" data-name="{e(name)}">'
                  f'<div class="fimg">{img(F + k + ".png", name)}</div>'
                  f'<figcaption><b>{e(name)}</b>{f"<span class=badge>Claude&rsquo;s pick</span><em>{e(why)}</em>" if why else ""}</figcaption>'
                  f'<button class="heart" aria-pressed="false" aria-label="Pick {e(name)}">&#9829;</button></figure>')
    faces += f'<h3 class="fg">{e(title)} <small>{e(sub)}</small></h3><div class="fgrid{" sm" if small else ""}">{cards}</div>'
GROUPS = {'top': 'Top three', 'best': 'Among the best', 'navy': 'Navy + pink', 'pink': 'Pink &amp; green', 'deep': 'Deep green',
          'shared': 'Also in Juniper: your call'}
N = len(MAN)
mc, cur = '', None
for c in MAN:
    if c['group'] != cur:
        cur = c['group']; mc += f'<h3 class="fg">{GROUPS[cur]}</h3>'
    cn = f' · <span class=ret>{e(c["caption_note"])}</span>' if c['caption_note'] else ''
    mc += (f'<article class="mcard">{img("assets/cards/style-of-your-life/" + c["file"], "Style of Your Life + " + c["mat"] + " match card")}'
           f'<div class="mt"><p class="num">#{c["order"]}{" · <span class=ret>Retired</span>" if c["retired_mat"] else ""}{cn}</p>'
           f'<h4>{e(c["mat"])}</h4><p class="bn">{e(c["brand"])}</p><p class="why">{e(c["why"])}</p>'
           f'<p class="rk"><b>Match the tiles:</b> {e(" · ".join(c["racks"]))}<br><b>Match the mat:</b> {e(" · ".join(c["mat_racks"]))}</p></div></article>')
HTML = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Style of Your Life Album</title>
<link href="https://fonts.googleapis.com/css2?family=Caprasimo&family=Bitter:wght@400;600;700&family=Playfair+Display:ital@1&display=swap" rel="stylesheet">
__CSS__
</head><body><div class="wrap">
<p class="kick">My Fair Mahjong · The Style of Your Life Series · Pearl Green</p>
<h1>Style of Your Life, the album set</h1>
<p class="lede">Your next album after Juniper, built the Juniper way. It&rsquo;s the set that looks like Juniper: green backs with a pink-and-green face palette. The one question for you is her <b>best features</b> (pick 4 faces). The match order is Claude&rsquo;s draft until you OK it.</p>
<nav><a href="#juniper">Juniper overlap + timing</a><a href="#faces">1 · Pick her faces</a><a href="#cover">2 · Cover</a><a href="#colors">3 · Colors + theory</a><a href="#cards">4 · {N} match cards</a></nav>

<div class="note" id="juniper">
<p><b>Why this set.</b> On Oct 28 you put My Fair Mahjong&rsquo;s Style of Your Life first in the album order and said it looked like the green-on-green set Oh My Mahjong was teasing, which turned out to be Juniper. None of My Fair Mahjong&rsquo;s other sets is close: the Park Series is mint melamine and Crystal Confetti Citrus Green is clear-backed lime.</p>
<p><b>How close it really is.</b> Both sets have green backs and white faces with pink and green art. The differences:</p>
<div class="tw"><table class="ov"><tr><th></th><th>Juniper (Oh My Mahjong)</th><th>Style of Your Life (My Fair Mahjong)</th></tr>
<tr><td>Back</td><td>Forest Green Jade, darker, jade-look stone</td><td>Pearl green with a malachite-style swirl, brighter and more emerald</td></tr>
<tr><td>Layers</td><td>Chartreuse + teal</td><td>One deep green layer</td></tr>
<tr><td>Faces</td><td>Hot pink, coral, mint, teal</td><td>Indigo (the main ink), wine, bubblegum pink, cornflower, marigold</td></tr>
<tr><td>Theme</td><td>Chinoiserie garden</td><td>A day of shopping: shoes, handbags, jewelry, escalators</td></tr></table></div>
<p><b>Mats that would top both albums:</b> pink-and-green mats (Palm Royale, Cherry Blossom Jade, Peonies Burst, Botanical Jewel) and the deep greens (Garden Glow &ndash; Emerald Green, Green Malachite). To keep the two albums apart, none of Juniper&rsquo;s top 7 is in this album. Only 3 of these 22 mats are also in Juniper, and they sit at the bottom under &ldquo;Also in Juniper&rdquo; for you to keep or cut.</p>
<p><b>How this album leans its own way:</b> navy and indigo (Tennis Club, Peacock Circle, Floral Instincts, the navy group), wine (Crimson Harvest), and cornflower and marigold (MOD Daisies). Juniper leans on chartreuse, teal and coral. Different tile racks too: My Fair Mahjong Indigo Blue + Magenta here, Oh My Mahjong Hot Pink + Agate on Juniper.</p>
<p><b>Timing (Claude&rsquo;s recommendation):</b> build it now, but post it at least a week after Juniper (Wed 11/11), with the Deco albums in between, so the feed and the album wall never show two green albums side by side. Target: <b>Wed 11/18 or later</b>. Two things to check before it posts: (1) Style of Your Life shows <b>sold out on myfairmahjong.com</b> today (Nov 7). It&rsquo;s a Dillard&rsquo;s exclusive, so it may be in Dillard&rsquo;s stores, but we can&rsquo;t link a sold-out set. Post it when My Fair Mahjong has it back, or on their restock day. (2) Its pair mat Parquet Petal is still &ldquo;coming soon&rdquo;. The set is holiday-friendly (Crimson Harvest, The Polo Club), so late November is a good slot.</p>
</div>

<h2 id="faces">Pick her 4 best features</h2>
<p class="lede">Tap the heart on up to 4 faces (the two dragons can count as one pick, as a pair). Green border = Claude&rsquo;s pick. Tap a tile to zoom. Then tap <b>Copy my picks</b> and paste it in the chat. Your picks are final.</p>
{faces}

<h2 id="cover">Album cover <span class="draft">DRAFT</span></h2>
<p class="lede">Same look as Juniper: her tile pile, a deep green panel, a white My Fair Mahjong logo and the frame with the double white lines.</p>
{img('assets/covers/albums/00-style-of-your-life-mahjong-tiles-cover.jpg', 'Style of Your Life album cover', 'big', False)}

<h2 id="colors">Her colors + color theory</h2>
<div class="two">{img('assets/colorcards/style-of-your-life/00-style-of-your-life-mahjong-tiles-color-guide-mobile.jpg', 'Style of Your Life color card', 'big')}{img('assets/colorwheels/style-of-your-life-color-wheel.jpg', 'Style of Your Life color wheel', 'big')}</div>
<div class="note">
<p><b>Clean and bright.</b> My Fair Mahjong calls it a pearl green back with a deep green middle layer and a white face. The back swirls from near-black green to a pale pearly mint, so it reads brighter and more emerald than Juniper.</p>
<p><b>Indigo is her main ink.</b> More of her face art is indigo than any other color (numbers, jewelry stands, joker arches). Navy mats pick it up, which no other green album does.</p>
<p><b>Complementary.</b> Her pink and wine sit across the wheel from her greens, so pink and red mats make her pop. Marigold and cornflower are her small accents (earrings, chains, escalators).</p>
<p><b>Mat colors that should work, strongest first:</b></p>
<ul>
<li>Navy + pink + green together: all of her at once (Tennis Club, Floral Instincts, Peach Petals).</li>
<li>Her faces as a print: cornflower, pink, red and marigold on green (MOD Daisies).</li>
<li>Wine + pink on deep green: moody, and good through the holidays (Crimson Harvest).</li>
<li>Cobalt or navy grounds: her indigo, with the backs as the contrast (Peacock Circle, Color Wave &ndash; Cobalt Center, Grandmillennial Peony).</li>
</ul>
<p><b>Use with care:</b> chartreuse, lime, teal and coral mats (those are Juniper&rsquo;s colors and she has none), and earthy olive or tan greens.</p>
<p><b>Tile racks:</b> My Fair Mahjong Indigo Blue + Magenta, the same solid acrylic rack in two colors, both 20&Prime;. My Fair Mahjong&rsquo;s own favorites with this set are tortoiseshell, magenta, teal, macaron blue, pearl white and clear. Malachite Dapple was the obvious choice, but it&rsquo;s black with a neon green dapple (not her pearly green), and the only photo is a stack, not a single rack.</p>
<div class="racks">{img('assets/racks/card/my-fair-mahjong-indigo-blue.png', 'My Fair Mahjong Indigo Blue rack')}{img('assets/racks/card/my-fair-mahjong-magenta.png', 'My Fair Mahjong Magenta rack')}</div>
</div>

<h2 id="cards">{N} match cards <span class="draft">DRAFT ORDER</span></h2>
<p class="lede">Claude&rsquo;s order: Tennis Club #1, MOD Daisies #2, Crimson Harvest #3. Parquet Petal is the pair mat, so it&rsquo;s in the group, not #1. Retired mats are marked. The 3 mats Juniper also has are at the bottom.</p>
{mc}
</div>
<div class="bar"><span id="cnt">Your picks: 0 of 4</span><button id="copy">Copy my picks</button></div>
<div class="lb" id="lb"><img alt=""></div>
<script>
(function(){{
 var K='soyl-faces-picks', picks=[];
 try{{picks=JSON.parse(localStorage.getItem(K)||'[]')||[]}}catch(e){{picks=[]}}
 function count(a){{return a.length-((a.indexOf('dragon-green')>-1&&a.indexOf('dragon-red')>-1)?1:0)}}
 var figs=[].slice.call(document.querySelectorAll('.face'));
 function nm(k){{var el=document.querySelector('[data-key="'+k+'"]');return el?el.dataset.name:k}}
 function render(){{figs.forEach(function(f){{var on=picks.indexOf(f.dataset.key)>-1;f.classList.toggle('on',on);f.querySelector('.heart').setAttribute('aria-pressed',on)}});
  document.getElementById('cnt').textContent='Your picks: '+count(picks)+' of 4'+(picks.length?' · '+picks.map(nm).join(', '):'');
  try{{localStorage.setItem(K,JSON.stringify(picks))}}catch(e){{}} }}
 figs.forEach(function(f){{f.querySelector('.heart').addEventListener('click',function(){{var k=f.dataset.key,i=picks.indexOf(k);
  if(i>-1)picks.splice(i,1);else{{var nx=picks.concat([k]);if(count(nx)>4){{alert('That\\'s 4 already. Un-heart one first.');return}} picks.push(k)}} render()}})}});
 document.getElementById('copy').addEventListener('click',function(){{var t='Style of Your Life best features: '+picks.map(nm).join(' | ');
  var done=function(){{document.getElementById('copy').textContent='Copied!';setTimeout(function(){{document.getElementById('copy').textContent='Copy my picks'}},1500)}};
  if(navigator.clipboard)navigator.clipboard.writeText(t).then(done,function(){{prompt('Copy this:',t)}});else prompt('Copy this:',t)}});
 var lb=document.getElementById('lb'),li=lb.querySelector('img');
 document.addEventListener('click',function(ev){{var t=ev.target;if(t.matches&&t.matches('img[data-zoom]')){{li.src=t.src;li.alt=t.alt;lb.classList.add('on')}}}});
 lb.addEventListener('click',function(){{lb.classList.remove('on')}});
 render();
}})();
</script></body></html>"""
HTML = HTML.replace('__CSS__', CSS)
open(OUT, 'w').write(HTML); print(OUT, len(HTML) // 1024, 'KB')
