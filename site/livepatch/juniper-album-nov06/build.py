"""Juniper full album set review page (Nov 6, Tiffany 1:11am: cover, colour card, colour wheel + colour theory,
favourite faces run-through, dating profile + intro carousel, all the match cards).
One phone-first page (390px). Faces: tap the heart on up to 4, then 'Copy my picks' (text for the chat). Claude's 4
proposals are marked. Images = jsDelivr pinned to a pushed commit (pass the SHA).
Usage: python3 build.py <commit sha> <out.html>"""
import json, sys, html, os
R = '/home/claude/mahjmatchmaker-data/'
SHA, OUT = sys.argv[1], sys.argv[2]
CDN = f'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@{SHA}/'
e = html.escape
P = json.load(open(R + 'config/profiles/juniper.json'))
MAN = json.load(open(R + 'assets/cards/juniper/manifest.json'))['cards']
F = 'assets/tiles/faces/juniper/clean/'
CLAUDE = {  # Claude's 4 proposals (= config/profiles/juniper.json best_features)
 'dragon-green': "Pair them: OMM's emerald dragon is the star of the set, and her pink twin is the reverse colorway.",
 'dragon-red': "Pair them: the pink twin of the emerald dragon; together they show off both halves of her palette.",
 'bam-1-peacock': "The signature tile: pink tail, mint body, and the only bird on the set.",
 'flower-2a': "The best of the 8 flowers: hot pink lotus + green pagoda, the whole garden in one tile.",
 'joker-1': "The jester joker with the pink bird: playful, and the pink pops most on the white face.",
}
G = [
 ('Dragons', 'Emerald dragon, her pink twin and the pagoda soap', [
   ('dragon-green', 'Green Dragon: the emerald dragon'), ('dragon-red', 'Red Dragon: the pink dragon'),
   ('dragon-white-pagoda', 'White Dragon (soap): the teal pagoda frame')]),
 ('Bird bam', 'The peacock', [('bam-1-peacock', 'Bird bam: the peacock')]),
 ('Flowers', 'Eight garden scenes: a pagoda and a lotus on each', [
   ('flower-1a', 'Flower 1: navy pagoda tower + pink lotus'), ('flower-1b', 'Flower 1: pink pavilion + teal lotus'),
   ('flower-2a', 'Flower 2: green pagoda + hot pink lotus'), ('flower-2b', 'Flower 2: coral pagoda + teal lotus'),
   ('flower-3a', 'Flower 3: teal pavilion + pink lotus'), ('flower-3b', 'Flower 3: pink gate + teal lotuses'),
   ('flower-4a', 'Flower 4: green pagoda + hot pink lotus'), ('flower-4b', 'Flower 4: coral lantern pavilion + teal lotus')]),
 ('Jokers', 'Two jester designs (the set has 3 + 2 of them)', [
   ('joker-1', 'Joker: pink bird, green jester hat'), ('joker-2', 'Joker: coral bird, mint + pink jester hat')]),
 ('Winds', 'Each with its own arrow colour', [
   ('wind-north', 'North wind: teal N, coral arrow'), ('wind-east', 'East wind: blush E, green arrow'),
   ('wind-west', 'West wind: green W, teal arrow'), ('wind-south', 'South wind: pink S, gold arrow')]),
 ('Dots', 'Floral medallions in pink, teal, navy and gold', [(f'dot-{i}', f'{i} Dot') for i in range(1, 10)]),
 ('Bams', 'Bamboo over a pink bridge', [(f'bam-{i}', f'{i} Bam') for i in range(2, 10)]),
 ('Craks', 'Coral brushstroke characters', [(f'crak-{i}', f'{i} Crak') for i in range(1, 10)]),
]
def img(p, alt, cls='', lazy=True):
    return f'<img src="{CDN}{p}" alt="{e(alt)}"{" loading=lazy" if lazy else ""} class="{cls}" data-zoom>'
faces = ''
for title, sub, items in G:
    small = title in ('Dots', 'Bams', 'Craks')
    cards = ''
    for k, name in items:
        why = CLAUDE.get(k)
        cards += (f'<figure class="face{" cp" if why else ""}" data-key="{k}" data-name="{e(name)}">'
                  f'<div class="fimg">{img(F + k + ".png", name)}</div>'
                  f'<figcaption><b>{e(name)}</b>{f"<span class=badge>Claude&rsquo;s pick</span><em>{e(why)}</em>" if why else ""}</figcaption>'
                  f'<button class="heart" aria-pressed="false" aria-label="Pick {e(name)}">&#9829;</button></figure>')
    faces += f'<h3 class="fg">{e(title)} <small>{e(sub)}</small></h3><div class="fgrid{" sm" if small else ""}">{cards}</div>'
carousel = ''.join(f'<div class="slide">{img(f"assets/social/juniper-launch/intro/{i}.jpg", f"Intro carousel slide {i}")}<span>{i}</span></div>' for i in range(1, 8))
GROUPS = {'top': 'Top three', 'deep': 'Forest green + pink', 'bright': 'Pink &amp; green brights', 'chino': 'Chinoiserie gardens', 'soft': 'Soft', 'stone': 'Stone &amp; solid'}
mc, cur = '', None
for c in MAN:
    if c['group'] != cur:
        cur = c['group']; mc += f'<h3 class="fg">{GROUPS[cur]}</h3>'
    racks = ' · '.join(c['racks']) ; mr = ' · '.join(c['mat_racks'])
    mc += (f'<article class="mcard">{img("assets/cards/juniper/" + c["file"], "Juniper + " + c["mat"] + " match card")}'
           f'<div class="mt"><p class="num">#{c["order"]}{" · <span class=ret>Retired</span>" if c["retired_mat"] else ""}{" · <span class=ret>Pair mat</span>" if c["caption_note"] else ""}</p>'
           f'<h4>{e(c["mat"])}</h4><p class="bn">{e(c["brand"])}</p><p class="why">{e(c["why"])}</p>'
           f'<p class="rk"><b>Match the tiles:</b> {e(racks)}<br><b>Match the mat:</b> {e(mr)}</p></div></article>')
HTML = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Juniper Album Set</title>
<link href="https://fonts.googleapis.com/css2?family=Caprasimo&family=Bitter:wght@400;600;700&family=Playfair+Display:ital@1&display=swap" rel="stylesheet">
<style>
:root{{--bg:#f6ece2;--card:#fffaf5;--ink:#0b3f78;--muted:#5a6b85;--pink:#c8325f;--line:#e6d6c8;--acc:#225d36;--chip:#fdf0f3}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#13202e;--card:#1b2b3c;--ink:#e9eef6;--muted:#a8b4c6;--pink:#ff8fb0;--line:#2c3e52;--acc:#7fd19c;--chip:#2a2030}}}}
:root[data-theme="dark"]{{--bg:#13202e;--card:#1b2b3c;--ink:#e9eef6;--muted:#a8b4c6;--pink:#ff8fb0;--line:#2c3e52;--acc:#7fd19c;--chip:#2a2030}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 Bitter,Georgia,serif}}
.wrap{{max-width:760px;margin:0 auto;padding:18px 16px 120px}}
.kick{{font:700 12px Bitter;letter-spacing:.18em;text-transform:uppercase;color:var(--pink);margin:0}}
h1{{font:400 40px/1.05 Caprasimo;margin:6px 0 8px;color:var(--acc)}}h2{{font:400 28px/1.1 Caprasimo;margin:38px 0 6px;scroll-margin-top:12px}}
.lede{{margin:0 0 12px;color:var(--muted)}}
nav{{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0 4px}}nav a{{background:var(--card);border:1px solid var(--line);border-radius:999px;padding:6px 12px;color:var(--ink);text-decoration:none;font-weight:600;font-size:14px}}
.note{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px;margin:12px 0}}
.note p{{margin:0 0 8px}}.note p:last-child{{margin:0}}
h3.fg{{font:700 13px Bitter;letter-spacing:.16em;text-transform:uppercase;color:var(--pink);margin:26px 0 10px}}h3.fg small{{display:block;letter-spacing:0;text-transform:none;font:italic 15px 'Playfair Display';color:var(--muted);margin-top:2px}}
.fgrid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}}.fgrid.sm{{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media(min-width:640px){{.fgrid{{grid-template-columns:repeat(3,minmax(0,1fr))}}.fgrid.sm{{grid-template-columns:repeat(5,minmax(0,1fr))}}}}
.face{{position:relative;margin:0;display:flex;flex-direction:column;justify-content:space-between;background:var(--card);border:2px solid var(--line);border-radius:16px;padding:10px 10px 12px}}
.face.cp{{border-color:var(--acc)}}.face.on{{border-color:var(--pink);box-shadow:0 0 0 3px var(--pink)}}
.fimg{{background:#1d3a5c;border-radius:12px;padding:8px;display:flex;justify-content:center}}.fimg img{{width:100%;max-width:220px;height:auto;display:block;cursor:zoom-in}}
.face figcaption{{margin-top:8px;font-size:14px;line-height:1.35}}.face figcaption b{{display:block}}
.face em{{display:block;font:italic 14px/1.35 'Playfair Display';color:var(--muted);margin-top:4px}}
.badge{{display:inline-block;margin-top:6px;background:var(--acc);color:#fff;border-radius:999px;padding:2px 9px;font:700 11px Bitter;letter-spacing:.08em;text-transform:uppercase}}
.heart{{display:block;width:100%;margin-top:10px;min-height:44px;border-radius:999px;border:2px solid var(--pink);background:transparent;color:var(--pink);font:700 15px Bitter;cursor:pointer}}
.heart[aria-pressed="true"]{{background:#f56c8c;border-color:#f56c8c;color:#fff}}
.heart:after{{content:' Pick'}}.heart[aria-pressed="true"]:after{{content:' Picked'}}
.bar{{position:fixed;left:0;right:0;bottom:0;background:var(--card);border-top:1px solid var(--line);padding:10px 16px calc(10px + env(safe-area-inset-bottom));display:flex;gap:10px;align-items:center;justify-content:space-between;z-index:5}}
.bar span{{font-weight:700;font-size:14px;min-width:0;overflow-wrap:anywhere}}.bar button{{flex:0 0 auto;background:var(--pink);color:#fff;border:0;border-radius:999px;padding:10px 16px;font:700 14px Bitter}}
.big{{width:100%;height:auto;display:block;border-radius:14px;cursor:zoom-in;margin:8px 0}}
.two{{display:grid;grid-template-columns:1fr;gap:12px}}@media(min-width:640px){{.two{{grid-template-columns:1fr 1fr}}}}
.car{{display:flex;gap:10px;overflow-x:auto;scroll-snap-type:x mandatory;padding-bottom:8px}}.slide{{flex:0 0 78%;scroll-snap-align:start;position:relative}}.slide img{{width:100%;border-radius:12px;display:block;cursor:zoom-in}}
.slide span{{position:absolute;top:8px;left:8px;background:var(--ink);color:var(--bg);border-radius:999px;padding:2px 9px;font-weight:700;font-size:13px}}
.mcard{{background:var(--card);border:1px solid var(--line);border-radius:16px;overflow:hidden;margin:0 0 16px}}.mcard img{{width:100%;height:auto;display:block;cursor:zoom-in}}
.mt{{padding:12px 14px 14px}}.mt h4{{font:400 24px/1.1 Caprasimo;margin:0}}.num{{margin:0 0 4px;font:700 12px Bitter;letter-spacing:.12em;color:var(--muted)}}
.ret{{background:var(--muted);color:var(--card);border-radius:999px;padding:1px 8px;font-size:11px}}.bn{{margin:2px 0 6px;color:var(--muted);font-weight:600}}.why{{margin:0 0 8px}}.rk{{margin:0;font-size:14px;color:var(--muted)}}
.draft{{display:inline-block;background:var(--ink);color:var(--bg);border-radius:999px;padding:2px 10px;font:700 11px Bitter;letter-spacing:.1em;vertical-align:middle}}
.lb{{position:fixed;inset:0;background:rgba(0,0,0,.9);display:none;align-items:center;justify-content:center;z-index:9;padding:12px}}.lb.on{{display:flex}}.lb img{{max-width:100%;max-height:100%;object-fit:contain}}
ul{{padding-left:20px;margin:6px 0}}li{{margin:3px 0}}
</style></head><body><div class="wrap">
<p class="kick">Oh My Mahjong · launches Wed 11/11 · 10am CT</p>
<h1>Juniper, the full album set</h1>
<p class="lede">Everything for her album in one place. The one question for you is her <b>best features</b>: pick 4 faces below. Everything else is a draft until you OK the match order.</p>
<nav><a href="#faces">1 · Pick her faces</a><a href="#cover">2 · Cover</a><a href="#colors">3 · Colors + theory</a><a href="#profile">4 · Profile + carousel</a><a href="#cards">5 · 33 match cards</a></nav>

<h2 id="faces">Pick her 4 best features</h2>
<p class="lede">Tap the heart on up to 4 faces (the two dragons can count as one pick, as a pair). Green border = Claude&rsquo;s pick. Tap a tile to zoom. When you&rsquo;re done, tap <b>Copy my picks</b> and paste it in the chat. Your picks are final: they never get swapped later.</p>
{faces}

<h2 id="cover">Album cover</h2>
<p class="lede">Same style as Papaya Spritz, Coquette and the other Oh My Mahjong covers: her tile pile, forest green panel, white Oh My Mahjong logo.</p>
{img('assets/covers/albums/00-juniper-mahjong-tiles-cover.jpg', 'Juniper Tiles album cover', 'big', False)}

<h2 id="colors">Her colors + color theory</h2>
<div class="two">{img('assets/colorcards/juniper/00-juniper-mahjong-tiles-color-guide-mobile.jpg', 'Juniper color card', 'big')}{img('assets/colorwheels/juniper-color-wheel.jpg', 'Juniper color wheel', 'big')}</div>
<div class="note">
<p><b>Clean, not earthy.</b> The back is dark, but it&rsquo;s a deep jewel green with a jade-look swirl, not a muddy or dusty one. The layers (chartreuse, teal) and faces (hot pink, coral, mint, gold) are all clear, saturated colors. Deep isn&rsquo;t earthy: she sits with Emerald and Jasmine, not with the earthy sets.</p>
<p><b>A cool base, warm accents.</b> Forest green (140&deg;) and teal (172&deg;) are cool; chartreuse (74&deg;) leans warm. The warmth comes from the faces: coral (5&deg;) and gold (44&deg;). Her hot pink (330&deg;) is a cool, blue-leaning pink.</p>
<p><b>Complementary.</b> Pink sits straight across the wheel from her greens. That&rsquo;s why a pink-and-green mat makes her pop, and why a mat that&rsquo;s all green reads tone on tone (moody, but the faces do the work).</p>
<p><b>Mat colors that should work, strongest first:</b></p>
<ul>
<li>Deep forest or emerald ground + pink florals: back and faces in one (Garden Glow, Botanical Jewel).</li>
<li>Kelly green + hot pink brights: her faces and chartreuse layer (Palm Royale, Enchanted, Peonies Burst).</li>
<li>Lime or chartreuse centers: the layer, turned up (Palm Beach Tropical Pink Lime).</li>
<li>Pink lotus and chinoiserie gardens: the art on her flowers (Lotus Cove, the Sophie Clima pagodas).</li>
<li>Tone-on-tone emerald and stone: moody, the faces bring the pink (Emerald Cove, Green Malachite).</li>
</ul>
<p><b>Use with care:</b> aqua- or blue-led mats (she has no aqua), lilac and purple borders, and earthy sage, olive or tan greens (they read muddy next to her clean jewel tones).</p>
<p><b>Odd in the photos:</b> Oh My Mahjong&rsquo;s single-tile shot runs brighter than the pile shot (teal reads aqua, chartreuse reads lime), so we use the pile values. The jade-look back isn&rsquo;t one flat color: the swirl runs from near-black to mid green, so match mats to its deep end. The &ldquo;red&rdquo; dragon is pink on this set.</p>
</div>

<h2 id="profile">Dating profile + intro carousel <span class="draft">DRAFT</span></h2>
<p class="lede">Doc 81 format. Launch line &ldquo;Launching Wed 11/11 · Oh My Mahjong&rdquo;. Top 3: Garden Glow, Palm Royale, Lotus Cove; slide 6 &ldquo;Made for each other&rdquo; = Lotus Cove, the official pair. Slide 4 shows Claude&rsquo;s 4 faces until you pick. The match count (33) is this draft&rsquo;s count; it updates to your final album.</p>
<div class="two">{img('assets/colorcards/juniper/00-juniper-mahjong-tiles-profile-d-story.jpg', 'Juniper dating profile story', 'big')}{img('assets/social/juniper-launch/juniper-favorite-tiles-DRAFT.jpg', 'Her best features draft graphic', 'big')}</div>
<p class="lede">Intro carousel, 7 slides (swipe):</p>
<div class="car">{carousel}</div>

<h2 id="cards">33 match cards <span class="draft">DRAFT ORDER</span></h2>
<p class="lede">Round-2 order with your Nov 5 notes (Garden Glow #1, Palm Royale #2, Lotus Cove #3; Esme + Enchanted in as Retired). Tile racks on every card (your Nov 6 call): Oh My Mahjong Hot Pink + Oh My Mahjong Agate, both the same OMM shape. Tell me the order and any cuts; the album page gets built from your order.</p>
{mc}
</div>
<div class="bar"><span id="cnt">Your picks: 0 of 4</span><button id="copy">Copy my picks</button></div>
<div class="lb" id="lb"><img alt=""></div>
<script>
(function(){{
 var K='juniper-faces-picks', picks=[];
 try{{picks=JSON.parse(localStorage.getItem(K)||'[]')||[]}}catch(e){{picks=[]}}
 function count(a){{return a.length-((a.indexOf('dragon-green')>-1&&a.indexOf('dragon-red')>-1)?1:0)}}
 var figs=[].slice.call(document.querySelectorAll('.face'));
 function render(){{figs.forEach(function(f){{var on=picks.indexOf(f.dataset.key)>-1;f.classList.toggle('on',on);f.querySelector('.heart').setAttribute('aria-pressed',on)}});
  document.getElementById('cnt').textContent='Your picks: '+count(picks)+' of 4'+(picks.length?' · '+picks.map(function(k){{return document.querySelector('[data-key="'+k+'"]').dataset.name}}).join(', '):'');
  try{{localStorage.setItem(K,JSON.stringify(picks))}}catch(e){{}} }}
 figs.forEach(function(f){{f.querySelector('.heart').addEventListener('click',function(){{var k=f.dataset.key,i=picks.indexOf(k);
  if(i>-1)picks.splice(i,1);else{{var nx=picks.concat([k]);if(count(nx)>4){{alert('That\\'s 4 already. Un-heart one first.');return}} picks.push(k)}} render()}})}});
 document.getElementById('copy').addEventListener('click',function(){{var t='Juniper best features: '+picks.map(function(k){{return document.querySelector('[data-key="'+k+'"]').dataset.name}}).join(' | ');
  var done=function(){{document.getElementById('copy').textContent='Copied!';setTimeout(function(){{document.getElementById('copy').textContent='Copy my picks'}},1500)}};
  if(navigator.clipboard)navigator.clipboard.writeText(t).then(done,function(){{prompt('Copy this:',t)}});else prompt('Copy this:',t)}});
 var lb=document.getElementById('lb'),li=lb.querySelector('img');
 document.addEventListener('click',function(ev){{var t=ev.target;if(t.matches&&t.matches('img[data-zoom]')){{li.src=t.src;li.alt=t.alt;lb.classList.add('on')}}}});
 lb.addEventListener('click',function(){{lb.classList.remove('on')}});
 render();
}})();
</script></body></html>"""
HTML = HTML.replace('colour', 'color')  # site spelling is US
open(OUT, 'w').write(HTML); print(OUT, len(HTML) // 1024, 'KB')
