"""Bam Bird Boutique Deco (Lagoon) / Deco (Mulberry) full album set review pages (Nov 7; Tiffany 7:03pm: "You take them, just
like you did this one. Just run with it."). Same layout as site/livepatch/juniper-album-nov06/juniper-album.html: faces pick
(hearts + Copy my picks), cover, colors + theory, profile + carousel, the match cards (tiles shown with every mat), and the mats
left out with reasons (mat with her tile pile inset). Phone-first (390px).
Usage: python3 build.py <deco-lagoon|deco-mulberry> <sha|local> <out.html> [files.json]
  sha   = jsDelivr pinned commit (repo copy);  local = relative paths (self-contained copy; pass files.json to list them)"""
import json, sys, html
R = '/home/claude/mahjmatchmaker-data/'
KEY, SHA, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
FILES = sys.argv[4] if len(sys.argv) > 4 else None
CDN = '' if SHA == 'local' else f'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@{SHA}/'
USED = set()
e = html.escape
P = json.load(open(R + f'config/profiles/{KEY}.json')); CC = json.load(open(R + 'config/colorcards.json'))['sets'][KEY]
MANF = json.load(open(R + f'assets/cards/{KEY}/manifest.json')); MAN = MANF['cards']; GROUPS = MANF['groups']
LO = json.load(open(R + 'scripts/albumcard/specs/deco_leftout_nov07.json'))[KEY]
LAG = KEY == 'deco-lagoon'; COL = 'Lagoon' if LAG else 'Mulberry'; OTHER = 'Mulberry' if LAG else 'Lagoon'
F = 'assets/tiles/faces/deco/clean/'
def src(p): USED.add(p); return CDN + p
def img(p, alt, cls='', lazy=True):
    return f'<img src="{src(p)}" alt="{e(alt)}"{" loading=lazy" if lazy else ""} class="{cls}" data-zoom>'
CLAUDE = {  # Claude's 4 proposals (= config/profiles/<key>.json best_features)
 'dragon-green': "Pair them: the teal-framed dragon in gold, and her mulberry-framed twin. The two Deco colors, side by side.",
 'dragon-red': "Pair them: the mulberry twin of the teal dragon.",
 'bam-1-crane': "The signature tile: a gold-winged crane with a teal crest, pure deco.",
}
if LAG:
    CLAUDE.update({'wind-east': "A gold peacock feather: the gold palm on her back, on the face.",
                   'joker-teal-lion': "The deep green lion, framed in mulberry and gold stripes. The boldest tile in the set."})
else:
    CLAUDE.update({'wind-south': "A mulberry heart in a peacock crest: her back color, on a face.",
                   'joker-rose-lion': "The rose lion in teal stripes: her two colors, swapped."})
G = [
 ('Dragons', 'Teal and mulberry twins, plus the soap', [('dragon-green', 'Green Dragon: teal frame, gold dragon'), ('dragon-red', 'Red Dragon: mulberry frame, gold dragon'), ('dragon-white', 'White Dragon (soap): periwinkle frame')]),
 ('Bird bam', 'The crane', [('bam-1-crane', 'Bird bam: the gold-winged crane')]),
 ('Flowers', 'Four art nouveau flowers', [('flower-iris-navy', 'Flower: navy iris'), ('flower-iris-gold', 'Flower: gold iris'), ('flower-poppy', 'Flower: teal poppy'), ('flower-lily', 'Flower: mulberry and gold lilies')]),
 ('Jokers', 'Two lions', [('joker-teal-lion', 'Joker: deep green lion, mulberry stripes'), ('joker-rose-lion', 'Joker: rose lion, teal stripes')]),
 ('Winds', 'Peacock feathers', [('wind-north', 'North wind: periwinkle feather'), ('wind-east', 'East wind: gold feather'), ('wind-west', 'West wind: rose feather'), ('wind-south', 'South wind: mulberry heart')]),
 ('Dots', 'Stars in teal, periwinkle and navy over a gold deco line', [(f'dot-{i}', f'{i} Dot') for i in range(1, 10)]),
 ('Bams', 'Gold and teal bamboo', [(f'bam-{i}', f'{i} Bam') for i in range(2, 10)]),
 ('Craks', 'Gold characters in mulberry and rose deco frames', [(f'crak-{i}', f'{i} Crak') for i in range(1, 10)]),
]
faces = ''
for title, sub, items in G:
    small = title in ('Dots', 'Bams', 'Craks'); cards = ''
    for k, name in items:
        why = CLAUDE.get(k)
        cards += (f'<figure class="face{" cp" if why else ""}" data-key="{k}" data-name="{e(name)}">'
                  f'<div class="fimg">{img(F + k + ".png", name)}</div>'
                  f'<figcaption><b>{e(name)}</b>{f"<span class=badge>Claude&rsquo;s pick</span><em>{e(why)}</em>" if why else ""}</figcaption>'
                  f'<button class="heart" aria-pressed="false" aria-label="Pick {e(name)}">&#9829;</button></figure>')
    faces += f'<h3 class="fg">{e(title)} <small>{e(sub)}</small></h3><div class="fgrid{" sm" if small else ""}">{cards}</div>'
carousel = ''.join(f'<div class="slide">{img(f"assets/social/{KEY}-launch/intro/{i}.jpg", f"Intro carousel slide {i}")}<span>{i}</span></div>' for i in range(1, 8))
N = len(MAN); mc, cur = '', None
for c in MAN:
    if c['group'] != cur:
        cur = c['group']; mc += f'<h3 class="fg">{e(GROUPS[cur])}</h3>'
    racks = ' · '.join(c['racks']); mr = ' · '.join(c['mat_racks'])
    notes = []
    if c['retired_mat']: notes.append('<span class=ret>Retired</span>')
    if c['caption_note'] and c['caption_note'] != 'Retired': notes.append(f'<span class=ret>{e(c["caption_note"])}</span>')
    if c['lowres']: notes.append('<span class=lr>Small brand photo</span>')
    mc += (f'<article class="mcard">{img(f"assets/cards/{KEY}/" + c["file"], CC["name"] + " + " + c["mat"] + " match card")}'
           f'<div class="mt"><p class="num">#{c["order"]}{" · " + " ".join(notes) if notes else ""}</p>'
           f'<h4>{e(c["mat"])}</h4><p class="bn">{e(c["brand"])}</p><p class="why">{e(c["why"])}</p>'
           f'<p class="rk"><b>Match the tiles:</b> {e(racks)}<br><b>Match the mat:</b> {e(mr)}</p></div></article>')
lo = ''
for m in LO:
    lo += (f'<article class="lo"><div class="lop">{img(m["img"], m["name"])}<div class="ins">{img(CC["tile"], CC["name"] + " tiles")}</div></div>'
           f'<div class="mt"><h4>{e(m["name"])}</h4><p class="bn">{e(m["brand"])}{" · <span class=ret>Retired</span>" if m["retired"] else ""}</p><p class="why">{e(m["why"])}</p></div></article>')
top3 = ', '.join(f'{m}' for m in P['first_dates'])
if LAG:
    THEORY = f"""
<p><b>Rich, not earthy.</b> Her back, Lagoon, is a deep jewel teal under a glassy acrylic, with a gold-foil art deco palm on every tile. The faces are ivory with clear inks: mulberry, rose, gold, teal, navy and periwinkle. Dark, but clean. She sits with the jewel-tone sets, not the earthy ones.</p>
<p><b>A cool base, warm accents.</b> Lagoon (190&deg;) and navy (224&deg;) are cool. The warmth comes from the gold foil (42&deg;) and the rose crak frames (14&deg;). Her mulberry (329&deg;) is a cool, blue-leaning berry.</p>
<p><b>Split complementary.</b> Her teal sits across the wheel from rose and coral, and mulberry sits just beside that. That&rsquo;s why a teal mat with a pink or berry frame lights her up (Reba, Wren), and why an all-teal mat reads tone on tone.</p>
<p><b>Light and dark.</b> The wheel shows light colors toward the center and dark toward the rim. Lagoon sits out at the dark edge of teal, so it needs a mat that is also deep, or one with a strong second color. Pale, pastel mats wash her out.</p>
<p><b>Mat colors that should work, strongest first:</b></p>
<ul><li>Deep teal inside a pink or mulberry frame: her back plus her faces (Reba, Wren, Caroline in Peacock).</li>
<li>Her sister color, Mulberry: the Deco Dragon (Mulberry) and other berry mats, where the tiles bring the teal.</li>
<li>Art deco gold lines and fans: the same era as the tiles (Gilded Peacock, SoHo, Gatsby Glow).</li>
<li>Peacocks and night gardens on dark teal or navy: her wind tiles and crane (Royal Peacock, Crane &amp; Moon).</li></ul>
<p><b>Use with care:</b> sage, olive and tan (they look dusty next to her), neon brights, and other mats in the same Lagoon teal (blue on blue, your Oct 26 rule).</p>
<p><b>Odd in the photos:</b> Bam Bird Boutique&rsquo;s tray shot reads a little greener than the pile shot. The backs are glassy, so they look lighter where the light hits; we matched to the deep middle of the tile.</p>"""
else:
    THEORY = f"""
<p><b>Rich, not earthy.</b> Her back, Mulberry, is a deep cool berry under a glassy acrylic, with a gold-foil art deco palm on every tile. The faces are ivory with clear inks: teal, mulberry, rose, gold, navy and periwinkle. Dark, but clean.</p>
<p><b>A cool base, warm accents.</b> Mulberry (332&deg;) leans blue, not orange, so she is a cool berry. Her teal bams and green dragon (184&deg;) are cool too. The gold foil (42&deg;) and rose crak frames (14&deg;) bring the warmth.</p>
<p><b>Complementary.</b> Teal sits almost straight across the wheel from her berry. That&rsquo;s why a deep teal mat makes her pop (Viola, Caroline in Peacock, the Lagoon Deco Dragon), and why an all-berry mat is berry on berry.</p>
<p><b>Light and dark.</b> The wheel shows light colors toward the center and dark toward the rim. Mulberry sits out at the dark edge, so she wants a mat that is deep too, or a clean ivory that lets her shine.</p>
<p><b>Mat colors that should work, strongest first:</b></p>
<ul><li>Deep teal with berry or pink flowers: her back plus her bams (Viola, Caroline in Peacock, Wren).</li>
<li>Her sister color, Lagoon: the Deco Dragon (Lagoon) and solid deep teals.</li>
<li>Plum and berry florals with a teal or ivory accent (Pretty in Plum, Mulberry and Sage).</li>
<li>Art deco fans and gold lines (Tiger Fans, Gilded Peacock).</li></ul>
<p><b>Use with care:</b> orange-reds, rust and brick (they clash with a cool berry), neon pinks, and mats in the same Mulberry (berry on berry).</p>
<p><b>Odd in the photos:</b> Mulberry photographs brighter and pinker on loose tiles in the light, and darker and more wine in the box; we matched to the middle, a deep berry.</p>"""
HTML = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(CC['name'])} Album Set</title>
<link href="https://fonts.googleapis.com/css2?family=Caprasimo&family=Bitter:wght@400;600;700&family=Playfair+Display:ital@1&display=swap" rel="stylesheet">
<style>
:root{{--bg:#f6ece2;--card:#fffaf5;--ink:#0b3f78;--muted:#5a6b85;--pink:#c8325f;--line:#e6d6c8;--acc:{CC['col']};--chip:#fdf0f3}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#13202e;--card:#1b2b3c;--ink:#e9eef6;--muted:#a8b4c6;--pink:#ff8fb0;--line:#2c3e52;--acc:{'#7fd1d9' if LAG else '#e59ac0'};--chip:#2a2030}}}}
:root[data-theme="dark"]{{--bg:#13202e;--card:#1b2b3c;--ink:#e9eef6;--muted:#a8b4c6;--pink:#ff8fb0;--line:#2c3e52;--acc:{'#7fd1d9' if LAG else '#e59ac0'};--chip:#2a2030}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 Bitter,Georgia,serif}}
.wrap{{max-width:760px;margin:0 auto;padding:18px 16px 120px}}
.kick{{font:700 12px Bitter;letter-spacing:.18em;text-transform:uppercase;color:var(--pink);margin:0}}
h1{{font:400 40px/1.05 Caprasimo;margin:6px 0 8px;color:var(--acc)}}h2{{font:400 28px/1.1 Caprasimo;margin:38px 0 6px;scroll-margin-top:12px}}
.lede{{margin:0 0 12px;color:var(--muted)}}
nav{{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0 4px}}nav a{{background:var(--card);border:1px solid var(--line);border-radius:999px;padding:6px 12px;color:var(--ink);text-decoration:none;font-weight:600;font-size:14px}}
.note{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px;margin:12px 0}}.note p{{margin:0 0 8px}}.note p:last-child{{margin:0}}
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
.heart[aria-pressed="true"]{{background:#f56c8c;border-color:#f56c8c;color:#fff}}.heart:after{{content:' Pick'}}.heart[aria-pressed="true"]:after{{content:' Picked'}}
.bar{{position:fixed;left:0;right:0;bottom:0;background:var(--card);border-top:1px solid var(--line);padding:10px 16px calc(10px + env(safe-area-inset-bottom));display:flex;gap:10px;align-items:center;justify-content:space-between;z-index:5}}
.bar span{{font-weight:700;font-size:14px;min-width:0;overflow-wrap:anywhere}}.bar button{{flex:0 0 auto;background:var(--pink);color:#fff;border:0;border-radius:999px;padding:10px 16px;font:700 14px Bitter}}
.big{{width:100%;height:auto;display:block;border-radius:14px;cursor:zoom-in;margin:8px 0}}
.two{{display:grid;grid-template-columns:1fr;gap:12px}}@media(min-width:640px){{.two{{grid-template-columns:1fr 1fr}}}}
.car{{display:flex;gap:10px;overflow-x:auto;scroll-snap-type:x mandatory;padding-bottom:8px}}.slide{{flex:0 0 78%;scroll-snap-align:start;position:relative}}.slide img{{width:100%;border-radius:12px;display:block;cursor:zoom-in}}
.slide span{{position:absolute;top:8px;left:8px;background:var(--ink);color:var(--bg);border-radius:999px;padding:2px 9px;font-weight:700;font-size:13px}}
.mcard,.lo{{background:var(--card);border:1px solid var(--line);border-radius:16px;overflow:hidden;margin:0 0 16px}}.mcard>img{{width:100%;height:auto;display:block;cursor:zoom-in}}
.mt{{padding:12px 14px 14px}}.mt h4{{font:400 24px/1.1 Caprasimo;margin:0;overflow-wrap:anywhere}}.num{{margin:0 0 4px;font:700 12px Bitter;letter-spacing:.12em;color:var(--muted)}}
.ret,.lr{{background:var(--muted);color:var(--card);border-radius:999px;padding:1px 8px;font-size:11px;letter-spacing:.06em}}.lr{{background:#b07a1f}}
.bn{{margin:2px 0 6px;color:var(--muted);font-weight:600}}.why{{margin:0 0 8px}}.rk{{margin:0;font-size:14px;color:var(--muted)}}
.lop{{position:relative}}.lop>img{{width:100%;aspect-ratio:1;object-fit:cover;display:block;cursor:zoom-in}}
.ins{{position:absolute;right:8px;bottom:8px;width:38%;border:4px solid #fff;border-radius:12px;overflow:hidden;box-shadow:0 4px 14px rgba(0,0,0,.25)}}.ins img{{width:100%;display:block;cursor:zoom-in}}
.logrid{{display:grid;grid-template-columns:1fr;gap:0 14px}}@media(min-width:640px){{.logrid{{grid-template-columns:1fr 1fr}}}}
.draft{{display:inline-block;background:var(--ink);color:var(--bg);border-radius:999px;padding:2px 10px;font:700 11px Bitter;letter-spacing:.1em;vertical-align:middle}}
.lb{{position:fixed;inset:0;background:rgba(0,0,0,.9);display:none;align-items:center;justify-content:center;z-index:9;padding:12px}}.lb.on{{display:flex}}.lb img{{max-width:100%;max-height:100%;object-fit:contain}}
ul{{padding-left:20px;margin:6px 0}}li{{margin:3px 0}}
</style></head><body><div class="wrap">
<p class="kick">Bam Bird Boutique · in stock now</p>
<h1>{e(CC['name'])}, the full album set</h1>
<p class="lede">Everything for her album in one place, built the way we did Juniper. The one question for you is her <b>best features</b>: pick 4 faces below. Everything else is a draft until you OK the match order.</p>
<nav><a href="#faces">1 · Pick her faces</a><a href="#cover">2 · Cover</a><a href="#colors">3 · Colors + theory</a><a href="#profile">4 · Profile + carousel</a><a href="#cards">5 · {N} match cards</a><a href="#left">6 · Left out</a></nav>
<div class="note"><p><b>How I matched her.</b> Two-color matches first: a mat that carries her {COL} backs <i>and</i> a second color from her faces. Her top 3: {e(top3)}. {('Reba is your favorite Deco pairing from October.' if LAG else 'Viola is the Mulberry pairing you liked in October.')} Bam Bird Boutique&rsquo;s own Deco Dragon mat is in the top 3, not #1, and only in her sister color ({OTHER}), never {COL} on {COL}.</p>
<p>Racks on every card: Bam Bird Boutique&rsquo;s own 19&Prime; wood racks in {COL} and {OTHER}, same shape so they lie the same, drawn at their real length. I looked at all {N} mats next to her tiles; the ones I passed on are at the bottom with the reason.</p></div>

<h2 id="faces">Pick her 4 best features</h2>
<p class="lede">Every Deco colorway has the same faces, so your picks can carry over to both albums if you like. Tap the heart on up to 4 (the two dragons can count as one pick, as a pair). Green border = Claude&rsquo;s pick. Tap a tile to zoom. Then tap <b>Copy my picks</b> and paste it in the chat. Your picks are final: they never get swapped later.</p>
{faces}

<h2 id="cover">Album cover</h2>
<p class="lede">Same style as Juniper and the other covers: her tile pile from Bam Bird Boutique&rsquo;s photo, a {COL.lower()} panel, the white Bam Bird Boutique logo, and the frame with the double white lines. Bam Bird has no loose pile shot, so the pile is the tiles in their velvet bag (a little lining shows at the edges).</p>
{img(f'assets/covers/albums/00-{KEY}-mahjong-tiles-cover.jpg', CC['name'] + ' album cover', 'big', False)}

<h2 id="colors">Her colors + color theory</h2>
<div class="two">{img(f'assets/colorcards/{KEY}/00-{KEY}-mahjong-tiles-color-guide-mobile.jpg', CC['name'] + ' color card', 'big')}{img(f'assets/colorwheels/{KEY}-color-wheel.jpg', CC['name'] + ' color wheel', 'big')}</div>
<div class="note">{THEORY}<p><b>In Bam Bird Boutique&rsquo;s words:</b> &ldquo;two jewel-toned colorways: Lagoon and Mulberry&rdquo;, &ldquo;inspired by the bold elegance of the Art Deco era.&rdquo;</p></div>

<h2 id="profile">Dating profile + intro carousel <span class="draft">DRAFT</span></h2>
<p class="lede">Doc 81 format. Line: &ldquo;{e(P['launch_line'])}&rdquo;. Top 3: {e(top3)}. New prompt: &ldquo;{e(P['swipe']['prompt_q'])}: {e(P['swipe']['prompt_a'])}&rdquo; (not used on any earlier album). Slide 4 shows Claude&rsquo;s 4 faces until your picks go in. Slide 6 uses Bam Bird Boutique&rsquo;s own photo of {('Lagoon tiles on the Indigo Deco Dragon (they have no photo of Lagoon on the Mulberry Dragon)' if LAG else 'Mulberry tiles on the Lagoon Deco Dragon')}.</p>
<div class="two">{img(f'assets/colorcards/{KEY}/00-{KEY}-mahjong-tiles-profile-d-story.jpg', CC['name'] + ' dating profile story', 'big')}{img(f'assets/social/{KEY}-launch/{KEY}-favorite-tiles-DRAFT.jpg', 'Her best features draft graphic', 'big')}</div>
<p class="lede">Intro carousel, 7 slides (swipe):</p>
<div class="car">{carousel}</div>

<h2 id="cards">{N} match cards <span class="draft">DRAFT ORDER</span></h2>
<p class="lede">Claude&rsquo;s order, best first. Every card shows the mat with her tile pile. Full mat and brand names under each card. &ldquo;Small brand photo&rdquo; = the brand&rsquo;s best photo is small, so that card is a bit soft.</p>
{mc}
<h2 id="left">Left out ({len(LO)}), and why</h2>
<p class="lede">Mats I looked at next to her tiles and passed on. Tap one to zoom; if you want any back in, say so in the chat.</p>
<div class="logrid">{lo}</div>
</div>
<div class="bar"><span id="cnt">Your picks: 0 of 4</span><button id="copy">Copy my picks</button></div>
<div class="lb" id="lb"><img alt=""></div>
<script>
(function(){{
 var K='{KEY}-faces-picks', picks=[];
 try{{picks=JSON.parse(localStorage.getItem(K)||'[]')||[]}}catch(e){{picks=[]}}
 function count(a){{return a.length-((a.indexOf('dragon-green')>-1&&a.indexOf('dragon-red')>-1)?1:0)}}
 var figs=[].slice.call(document.querySelectorAll('.face'));
 function nm(k){{var f=document.querySelector('[data-key="'+k+'"]');return f?f.dataset.name:k}}
 function render(){{figs.forEach(function(f){{var on=picks.indexOf(f.dataset.key)>-1;f.classList.toggle('on',on);f.querySelector('.heart').setAttribute('aria-pressed',on)}});
  document.getElementById('cnt').textContent='Your picks: '+count(picks)+' of 4'+(picks.length?' · '+picks.map(nm).join(', '):'');
  try{{localStorage.setItem(K,JSON.stringify(picks))}}catch(e){{}} }}
 figs.forEach(function(f){{f.querySelector('.heart').addEventListener('click',function(){{var k=f.dataset.key,i=picks.indexOf(k);
  if(i>-1)picks.splice(i,1);else{{var nx=picks.concat([k]);if(count(nx)>4){{alert('That\\'s 4 already. Un-heart one first.');return}} picks.push(k)}} render()}})}});
 document.getElementById('copy').addEventListener('click',function(){{var t='{e(CC['name'])} best features: '+picks.map(nm).join(' | ');
  var done=function(){{document.getElementById('copy').textContent='Copied!';setTimeout(function(){{document.getElementById('copy').textContent='Copy my picks'}},1500)}};
  if(navigator.clipboard)navigator.clipboard.writeText(t).then(done,function(){{prompt('Copy this:',t)}});else prompt('Copy this:',t)}});
 var lb=document.getElementById('lb'),li=lb.querySelector('img');
 document.addEventListener('click',function(ev){{var t=ev.target;if(t.matches&&t.matches('img[data-zoom]')){{li.src=t.src;li.alt=t.alt;lb.classList.add('on')}}}});
 lb.addEventListener('click',function(){{lb.classList.remove('on')}});
 render();
}})();
</script></body></html>"""
HTML = HTML.replace('colour', 'color')
open(OUT, 'w').write(HTML); print(OUT, len(HTML) // 1024, 'KB', len(USED), 'images')
if FILES: json.dump([{'path': p} for p in sorted(USED)], open(FILES, 'w'))  # Artifact 'files' list, paths relative to the repo root (Juniper junalb format)
