#!/usr/bin/env python3
"""Brand-box fixes (Oct 21). Input: live page HTML in --src dir (curl of each -discount-code page).
Output: per-page before/after of the Why-I-love box + patched full block (<slug>.after.html is the whole page's code block text region)."""
import re,glob,os,sys,html
SRC=sys.argv[1]; OUT=os.path.dirname(os.path.abspath(__file__))
HS='https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@efde3ef88b70a8797d97bdcdb8409faafe6bd62c/assets/brand/headshot/tiffany-chambray-headshot-square.jpg'
OLDHS='https://images.squarespace-cdn.com/content/69b1d01289d0f8016ee3d508/fa40abe2-2b7e-426d-90d0-c88854212701/Tiffany+Headshot.png?format=300w'
OLDI='Oh My Mahjong Mahji Mentor instructor and the matchmaker behind Mahj Matchmaker.'
NEWI='Mahjong instructor and the matchmaker behind Mahj Matchmaker.'
CSS_OLD='.mmbg .me span{display:block;font-size:.88em;opacity:.8}'
CSS_NEW=CSS_OLD+'\n.mmbg h1,.mmbg h2,.mmbg h3{font-style:normal}'
BB_OLD=("<p>Bird &amp; Bamboo is my go-to for painted wood racks when I want to pull one exact color out of a tile set. With 94 paint colors and stains, it&rsquo;s the brand I recommend most in my album rack matches, from Harbor Blue and Jade to Weathered Oak.</p>"
"<p>Weathered Oak, Clear Stain, French Blue and Hot Pink are my most-used shades. Because there are so many colors, I built a <a href=\"/bird-and-bamboo-rack-colors\">Bird &amp; Bamboo rack color library</a> to make choosing easier. You&rsquo;ll see my picks in the rack matches for albums like <a href=\"/willow-mahjong-tile-matches\">Willow</a>, <a href=\"/heritage-2-0-mahjong-tile-matches\">Heritage 2.0</a> and <a href=\"/solara-mahjong-tile-matches\">Solara</a>.</p>")
BB_NEW=("<p>Bird &amp; Bamboo is my go-to for painted wood racks when I want to pull one exact color out of a tile set. With 94 paint colors and stains, it&rsquo;s the rack brand I use most in my album matches, from Harbor Blue to Jade.</p>"
"<p>My most-used shades are Weathered Oak, Clear Stain, French Blue and Hot Pink. With so many colors, I built a <a href=\"/bird-and-bamboo-rack-colors\">Bird &amp; Bamboo rack color library</a> to make choosing easier. You&rsquo;ll see my picks in the rack matches for albums like <a href=\"/willow-mahjong-tile-matches\">Willow</a>, <a href=\"/heritage-2-0-mahjong-tile-matches\">Heritage 2.0</a> and <a href=\"/solara-mahjong-tile-matches\">Solara</a>.</p>")
report=[]
for f in sorted(glob.glob(SRC+'/*-discount-code*.html')):
    slug=os.path.basename(f)[:-5]; s=open(f).read()
    if 'class="me"' not in s: continue
    m=re.search(r'<section>\s*<h2>[^<]*</h2>\s*<div class="note">\s*<div class="me">.*?</section>',s,re.S)
    if not m: report.append((slug,'NO BOX MATCH')); continue
    before=m.group(0); after=before
    # headshot img tag
    after=re.sub(r'<img src="'+re.escape(OLDHS)+r'" style="object-position:50% 22%"','<img src="'+HS+'" style="object-position:50% 50%"',after)
    isOMM=slug=='oh-my-mahjong-discount-code'
    assert after.count(HS)==1,slug
    assert CSS_OLD in s,slug
    full=s  # not written; page patch is applied in-browser by the same replacements
    d=os.path.join(OUT,'pages'); os.makedirs(d,exist_ok=True)
    open(f'{d}/{slug}.before.html','w').write(before+'\n')
    open(f'{d}/{slug}.after.html','w').write(after+'\n')
    report.append((slug,'ok'))
for r in report: print(*r)
