#!/usr/bin/env python3
"""Oct 18 draft site/livepatch/qa/bb-wood-copy.md, applied (Tiffany Oct 21 10:31pm). Input: dir of live curl HTML.
Writes bb/<slug>.replacements.json (exact old->new pairs for the code block + FAQ JSON-LD) and bb/*.after.html previews."""
import sys,os,re,json
SRC=sys.argv[1]; OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'bb'); os.makedirs(OUT,exist_ok=True)
def rep(s,pairs):
    for o,n in pairs:
        assert s.count(o)>=1,o[:60]
        s=s.replace(o,n)
    return s
# ---- discount pages
D=[("<p>Tip: they sell painted wood samples","<p>Every color comes standard or scalloped.</p><p>Tip: they sell painted wood samples"),("from Harbor Blue and Jade to Weathered Oak.","from Harbor Blue and Jade to Hot Pink."),
("Weathered Oak, Clear Stain, French Blue and Hot Pink are my most-used shades.","French Blue, Hot Pink, Dark Navy and Kelly Green are some of my most-used shades."),
("Weathered Oak and Clear Stain are the most versatile. French Blue and Hot Pink are my favorite pops of color.","Neutrals like White, Cream and True Black go with the most sets. French Blue and Hot Pink are my favorite pops of color. Want a wood look? I pair real-wood racks like Peace Love Mahjong Oak or Bam Bird Boutique Walnut.")]
for slug in ['bird-and-bamboo-discount-code','bird-and-bamboo-discount-code-2']:
    s=open(f'{SRC}/{slug}.html').read()
    a=rep(s,D)
    assert 'Weathered' not in a and 'Clear Stain' not in a
    json.dump(D,open(f'{OUT}/{slug}.replacements.json','w'),indent=1)
# ---- rack colors page
s=open(f'{SRC}/rackcolors.html').read()
def sw(name):  # all tile blocks with this name
    return [m for m in re.finditer(r'<div class="sw"><div class="bar[^"]*" style="--c:[^"]*"><span class="ledge"></span></div><p class="nm">'+re.escape(name)+r'</p>.*?</a></div>',s,re.S)]
pairs=[]
for n in ['Weathered Oak','Almond','Tudor','Provincial','Red Mahogany','Dark Walnut','Clear']:
    ms=sw(n); assert ms,n
    for m in ms: pairs.append((m.group(0),''))
# section replace
sec=re.search(r'<section><h2 id="stains">Wood Stains</h2>.*?</section>',s,re.S).group(0)
note='<section><p class="note"><strong>Wood looks:</strong> Bird &amp; Bamboo\'s wood stains aren\'t available right now, so for a wood rack I reach for real wood: Peace Love Mahjong Oak, Bam Bird Boutique Walnut or Middle &amp; Main Scalloped Beechwood.</p></section>'
# neutrals: add White before Blackboard Black
other=[
("All 94 Paint Colors and Stains</h1>","Every Paint Color</h1>"),
("come in 94 paint colors and wood stains, so you can","come in dozens of paint colors, so you can"),
("out of your tiles. Use code <strong>MAHJMATCH</strong>","out of your tiles. Every color comes standard or scalloped. Use code <strong>MAHJMATCH</strong>"),
('<a href="#stains">Wood Stains</a>',''),
("comes in 94 paint colors and wood stains, including metallics.","comes in dozens of paint colors, including metallics."),
("A wood stain like Weathered Oak or Clear is the safest choice","A neutral like White, Cream or True Black is the safest choice"),
]
a=s
# order matters: tiles first (white lives inside sec which is replaced wholesale)
a=a.replace(sec,note)
for o,n in pairs:
    a=a.replace(o,n)
for o,n in other:
    assert o in a,o; a=a.replace(o,n)
# FAQ JSON-LD may repeat the same sentences
tot=len(a)
for w in ['Weathered','Almond','Tudor','Provincial','Mahogany','Walnut','Wood Stains','Clear<']:
    print(w, len(re.findall(w,a)))
i=a.find('<div class="mmrc">'); j=a.find('<script',i)
open(f'{OUT}/bird-and-bamboo-rack-colors.after.html','w').write(a[i:j])
k=s.find('<div class="mmrc">'); l=s.find('<script',k)
open(f'{OUT}/bird-and-bamboo-rack-colors.before.html','w').write(s[k:l])
print('tiles',s.count('class="sw"'),'->',a[i:j].count('class="sw"'))
