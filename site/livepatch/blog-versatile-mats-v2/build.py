"""Draft v2 of /blog/most-versatile-mahjong-mats (Tiffany, Oct 25 7:38pm: lead with leather, then lots-of-colour mats,
then earthy neutrals + greens; real mat photos, match card only when the mat is no longer sold; not OMM-forward).
Builds preview.html (images embedded) for her review. Nothing here is live."""
import base64, io, json, os, urllib.request
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__))
P = {r['name']: r for r in json.load(open(D + '/picks_data.json'))}

# chosen product photo per mat (index into the brand's product images); Cognac = her live match card (mat no longer sold)
PHOTO = {'Brown Vegan Leather': 3, 'Vegan Leather – Caramel': 0, 'Chinoiserie Songbird': 0, 'Larkspur': 0, 'Darjeeling': 0,
         'Lorelei': 0, 'Jardín de Los Jefes': 1, 'Rattan': 0, 'The Hunt Club': 0, 'Autumn Saffron': 0, 'Ivy Reverie': 0,
         'Osmanthus Grove': 0, 'Jade': 0, 'Nantucket Basket': 1}
COGNAC_CARD = 'https://images.squarespace-cdn.com/content/69b1d01289d0f8016ee3d508/fcacc536-e38f-4a29-8508-9c6057dbcafd/10-heritage-2-0-mahjong-tiles-oh-my-mahjong-cognac-mat.jpg?format=1000w'


def img(url):
    b = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=40).read()
    im = Image.open(io.BytesIO(b)).convert('RGB'); im.thumbnail((900, 900))
    o = io.BytesIO(); im.save(o, 'JPEG', quality=82)
    return 'data:image/jpeg;base64,' + base64.b64encode(o.getvalue()).decode()


def photo(name):
    if name == 'Cognac':
        return img(COGNAC_CARD)
    r = P[name]
    return img(r['img'][PHOTO[name]].split('?')[0] + '?width=1000')


def sets(name, n=8):
    s = P[name]['sets']
    return ', '.join(s[:n - 1]) + (' and ' + s[n - 1] if len(s) >= n else '') if len(s) > 1 else s[0]


MATS = {
 'leather': [
  ('Brown Vegan Leather', 'Charleston Mahjong Club', 'Brown Vegan Leather by Charleston Mahjong Club',
   "A warm, saddle-brown vegan leather with a soft, worn-in look. It's the mat I'd hand to anyone who owns wood-look or tortoise tiles, and it makes cream tile faces look rich instead of plain."),
  ('Vegan Leather – Caramel', 'Bam Bird Boutique', 'Vegan Leather by Bam Bird Boutique',
   "Bam Bird makes their vegan leather mat in Caramel, Navy, Gold, Hunter Green and Cream. Caramel is my favorite all-rounder, and Navy is the one I'd pick for jewel-tone tiles."),
  ('Cognac', 'Oh My Mahjong', 'Cognac by Oh My Mahjong',
   "A rich caramel vegan leather that behaves like a true neutral. It isn't in Oh My Mahjong's shop right now, so if you spot one in a buy/sell group, it's a keeper."),
 ],
 'color': [
  ('Chinoiserie Songbird', 'Mahj & Vine', 'Chinoiserie Songbird by Mahj & Vine',
   "Tropical leaves and blooms in hot pink, greens and blues, with little songbirds tucked in. Bright and pastel tile sets all find something to grab onto."),
  ('Larkspur', 'Oh My Mahjong', 'Larkspur by Oh My Mahjong',
   "A coral center, a lime border and blue florals. It's the mat I've matched with more tile sets than any other, from soft pastels to tortoise."),
  ('Jardín de Los Jefes', 'Tigre de Tartan', 'Jardín de Los Jefes by Tigre de Tartan',
   "Bold garden florals in nearly every color on a crisp white ground, framed in rattan. Bright tile sets look right at home here."),
  ('Lorelei', 'Oh My Mahjong', 'Lorelei by Oh My Mahjong',
   "Pagodas and florals in pink, turquoise and soft green. Playful without being loud, and those three color families give almost any tile back something to pick up."),
  ('Darjeeling', 'Oh My Mahjong', 'Darjeeling by Oh My Mahjong',
   "Layered pagodas, trees and florals in blues, greens, honey and brown. It works with everything from wood-look tiles to bright sets."),
 ],
 'earthy': [
  ('Rattan', 'Sunday Mahjong', 'Rattan by Sunday Mahjong',
   "A woven rattan border around an olive center. It's natural texture plus green, which is exactly why it goes with so much. Sunday restocks in drops, so keep an eye on their release schedule."),
  ('Autumn Saffron', 'Mahjong Row & Co.', 'Autumn Saffron by Mahjong Row & Co.',
   "A deep brown frame around a golden floral and lattice center. Warm, rich and grown-up, and gorgeous with wood-look tiles."),
  ('Ivy Reverie', 'Mahjong Row & Co.', 'Ivy Reverie by Mahjong Row & Co.',
   "A soft ivy-print border around a calm taupe center. It's a quiet mat that lets busy tile faces be the star."),
  ('Osmanthus Grove', 'Mahjong Row & Co.', 'Osmanthus Grove by Mahjong Row & Co.',
   "Deep green with a warm golden lattice border. If you want green on the table without going bright, this is the one."),
  ('The Hunt Club', 'Charleston Mahjong Club', 'The Hunt Club by Charleston Mahjong Club',
   "Green toile framed in terracotta around a cream gingham center. Preppy, earthy and easy to match."),
  ('Nantucket Basket', 'Tigre de Tartan', 'Nantucket Basket by Tigre de Tartan',
   "A woven basketweave with a white rope border. Basketweave reads as a neutral, so it pairs with natural-texture tiles and colorful sets alike."),
  ('Jade', 'Oh My Mahjong', 'Jade by Oh My Mahjong',
   "Deep teal and ocean blues with soft green waves. It reads almost like a neutral, so bright tile backs pop without fighting it."),
 ],
}
SECT = {
 'leather': ('Leather and leatherette',
   "If you only buy one mat, I'd start here. A solid leather-look mat acts like a neutral, and warm browns flatter wood-look, tortoise and jewel-tone tiles alike."),
 'color': ('Mats with lots of colors',
   "My other secret: a mat with three or more colors in it. Different tile backs can each pull a different color, so one mat ends up matching a surprising number of sets."),
 'earthy': ('Earthy neutrals and greens',
   "Green is always on the table in mahjong. Every set has a whole suit of green bams, plus the green dragons. That's why mats with earthy neutrals and soft greens are so easy to love: they pick up colors your tiles already have."),
}


def card(name, brand, title, text):
    return f'''<section class="mat"><h3>{title}</h3><figure><img alt="{title}" src="{photo(name)}">{"<figcaption>Heritage 2.0 tiles on the Cognac mat (my match card, since the mat isn't sold right now)</figcaption>" if name=="Cognac" else ""}</figure>
<p>{text}</p><p class="see"><b>See it with</b> {sets(name)}.</p></section>'''


body = []
for k in ('leather', 'color', 'earthy'):
    h, intro = SECT[k]
    body.append(f'<h2>{h}</h2><p>{intro}</p>' + ''.join(card(*m) for m in MATS[k]))

HTML = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Versatile Mats Draft</title>
<link href="https://fonts.googleapis.com/css2?family=Caprasimo&family=Bitter:wght@400;700&family=Playfair+Display:ital@1&display=swap" rel="stylesheet">
<style>
:root{--bg:#faf3ea;--card:#fff;--ink:#2a2036;--mute:#6b5a77;--navy:#054689;--pink:#c8325f;--line:#ecd5df;--note:#fff6d6}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#1d1820;--card:#2a2330;--ink:#f3e9ec;--mute:#bfaec4;--navy:#8fb4ea;--pink:#f07aa0;--line:#3d3240;--note:#3a3320}}
:root[data-theme="dark"]{--bg:#1d1820;--card:#2a2330;--ink:#f3e9ec;--mute:#bfaec4;--navy:#8fb4ea;--pink:#f07aa0;--line:#3d3240;--note:#3a3320}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.6 Bitter,Georgia,serif;padding:24px 16px}
.wrap{max-width:720px;margin:0 auto}h1{font:400 40px/1.1 Caprasimo,serif;color:var(--navy);margin:8px 0;text-wrap:balance}
h2{font:400 30px/1.15 Caprasimo,serif;color:var(--navy);margin:44px 0 8px;text-wrap:balance}h3{font:700 21px/1.3 Bitter,serif;margin:0 0 10px}
.lede{font:italic 20px/1.5 "Playfair Display",serif;color:var(--pink)}
.mat{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px;margin:18px 0}
figure{margin:0 0 10px}img{width:100%;border-radius:10px;display:block}figcaption{font-size:13px;color:var(--mute);margin-top:6px}
.see{font-size:15px;color:var(--mute)}.note{background:var(--note);border-radius:12px;padding:12px 14px;font-size:14px;margin:0 0 20px}
</style></head><body><div class="wrap">
<div class="note"><b>Draft v2 for Tiffany, not live.</b> Order: leather → lots of colors → earthy neutrals and greens. Real mat photos, except Cognac (not sold right now, so it keeps your match card). Every "See it with" list comes from your real album picks. Want any mats swapped, added or cut?</div>
<h1>The Most Versatile Mahjong Mats</h1>
<p class="lede">The mats I reach for again and again, because they work with so many tile sets.</p>
<p>If you're only buying one or two mats, marry the versatile one, then date the rest. You want a mat that plays nicely with the tiles you have now and the tiles you'll fall for next year. These are the ones that keep showing up in my match albums, from lots of different brands.</p>
''' + ''.join(body) + '''
<h2>Retired favorites worth hunting for</h2>
<p>Spring Fling, Citrus Songbird and Enchanted by Oh My Mahjong were some of the most versatile mats I've ever matched. They're retired, so if you see one in a mahjong buy/sell group, grab it.</p>
<h2>How to pick a mat that works with everything</h2>
<p><b>Start with leather or a leather look.</b> Solid, warm neutrals go with almost every tile set.</p>
<p><b>Look for three or more colors.</b> Different tile backs can each pull a different one.</p>
<p><b>Don't fear green.</b> Your bams are green, so earthy greens and natural textures like rattan and basketweave are always in play.</p>
<p><b>Start with your tiles.</b> Pull up your set in Find <i>Your</i> Mat-ch™ or its match album and see which of these mats show up.</p>
</div></body></html>'''
open(D + '/preview.html', 'w').write(HTML)
print('ok', len(HTML))
