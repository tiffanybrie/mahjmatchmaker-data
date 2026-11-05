"""Juniper picks page, round 2 (Tiffany Nov 5 12:42am notes). Usage: python3 build_r2.py <out.html>"""
import json,base64,io,html,sys,os,re
from PIL import Image
R='/home/claude/mahjmatchmaker-data/'; S='/tmp/claude-0/-home-claude/05549d34-8fe3-5ca9-a6a5-308991cb9a78/scratchpad/'
os.chdir(R)
snap=json.load(open('config/fym-mats-snapshot.json'))['mats']
RK=json.load(open(S+'junpage/racks.json'))
for k,v in RK.items():
  if (v.get('img') or '').startswith('"'): v['img']=v['img'][1:]
def b64(path,maxw=900,q=80,png=False):
  im=Image.open(path).convert('RGBA' if png else 'RGB'); im.thumbnail((maxw,maxw)); bio=io.BytesIO()
  im.save(bio,'PNG') if png else im.save(bio,'JPEG',quality=q)
  return ('data:image/png;base64,' if png else 'data:image/jpeg;base64,')+base64.b64encode(bio.getvalue()).decode()
card='assets/racks/card/'
RK['owa']={'n':'White Acrylic','bn':'Oh My Mahjong','img':b64(card+'oh-my-mahjong-white-acrylic.png',500,png=True)}
RK['plmp']['img']=b64(card+'peace-love-mahjong-pink.png',500,png=True)
RK['plmc']['img']=b64(card+'peace-love-mahjong-chartreuse.png',500,png=True)
H=S+'junhd/'; G='assets/mats/gallery/'; J='assets/colorcards/juniper/mats/'
r2=json.load(open(S+'jun_r2_img.json'))
def gal(name,bn=None):
  for k,v in r2.items():
    if re.sub(r'\s*\(retired\)','',snap[k]['n'])==name and (bn is None or snap[k]['bn']==bn): return v[5:] if v.startswith('FILE:') else G+v+'.webp'
  raise SystemExit('no img '+name)
# (group, name, brand, img, why, racks, retired)
M=[
('top','Garden Glow – Emerald Green','Bespoke Mahjong',J+'garden-glow-emerald-bespoke-mahjong.jpg',"Looks made for the set: the deep forest ground is the jade-look back, and the pink wildflowers and greens pick up the craks, bams and dots.",['bbfg','ohp']),
('top','Palm Royale','Mahj Tile Haus',J+'palm-royale-mahj-tile-haus.jpg',"Kelly cane lattice, blush palms and leopards: pink and green at the same brightness as the faces, with enough green to hold the backs.",['bbk','bbhp']),
('top','Lotus Cove','Oh My Mahjong',J+'lotus-cove-oh-my-mahjong.jpg',"Oh My Mahjong's own pair for Juniper (starter kit, Nov 11). Pink pond frame and lily pads echo the lotus flower tiles; it has no forest green, so it sits third.",['opq','owa']),
('deep','Botanical Jewel',"Let's Be Besties",gal('Botanical Jewel'),"Forest green ground full of magenta and pink wildflowers: back, bams and craks in one.",['bbfg','ohp']),
('deep','Esme','Oh My Mahjong',gal('Esme'),"Deep teal-green with pink blossoms, an Oh My Mahjong cousin of the set. Retired, but still a match for anyone who owns it.",['jb','opq'],1),
('deep','Emerald Leopard in Bloom','Mahjong Register',H+'emerald-leopard-in-bloom-premium-padded.jpg',"Emerald lattice frame with pink peonies; the leopard keeps it playful, like the jester jokers.",['mrep','opq']),
('deep','Midori Shadows','Golden Pond Mahjong',gal('Midori Shadows'),"Deep green with cranes and pink blossoms: the garden-at-night mood of the set. Also one of your Malachite picks.",['jb','opq']),
('deep','Reba','Britt Mills',gal('Reba'),"Deep green field inside a pink frame, with a bouquet of pinks and greens.",['mal','ohp']),
('deep','Mahj In Bloom Mat','Mahj Mood',gal('Mahj In Bloom Mat'),"Deep green with pink and orchid roses; the lilac border is the only colour Juniper doesn't carry.",['jb','opq']),
('deep','Savannah','Britt Mills',J+'savannah-britt-mills.jpg',"Forest green with a pink floral medallion. Its olive and orange make it the moodier, Thanksgiving-to-Christmas pick.",['mal','opq']),
('deep','Viola','Britt Mills',gal('Viola'),"Deep green center inside a dark floral border of pinks and lilacs: elegant and dark.",['jb','bblp']),
('deep','YOTD Black','Bespoke Mahjong',gal('YOTD Black'),"Black ground with pink roses and a green dragon, for the emerald dragon tiles. The darkest pick here.",['jb','ohp']),
('deep','Sunday Premium','Sunday Mahjong',gal('Sunday Premium'),"Teal-green with a coral crane, the peacock tile's cousin; the gold trim picks up the gold dots.",['jb','opq']),
('deep','Crane & Moon','YOLO Mahjong',gal('Crane & Moon'),"Deep green-navy night sky with cranes, coral flowers and a gold moon: the lantern-lit garden in OMM's own words.",['mrep','ohp']),
('bright','Enchanted','Oh My Mahjong',gal('Enchanted'),"Hot pink and kelly green chinoiserie from Oh My Mahjong: the same pink and green, at the same brightness as the faces. Retired.",['ohp','bbk'],1),
('bright','Peonies Burst',"Let's Be Besties",gal('Peonies Burst'),"Magenta peonies around a kelly green star: bold, and right on Juniper's pink and green.",['ohp','bbk']),
('bright','Zesty Plume','Mahj & Vine',H+'zesty-plume.jpg',"Hits every Juniper colour: hot pink frame, teal and chartreuse foliage, and a white field like the faces.",['plmp','jb']),
('bright','Chinoiserie Songbird','Mahj & Vine',H+'chinoiserie-songbird.jpg',"A chinoiserie garden in pink, mint and lime: the world of the peacock and pagoda tiles.",['plmp','plmc']),
('bright','Cherry Blossom Jade','Miss Mahjong',H+'cherry-blossom-jade.jpg',"Hot pink, chartreuse and kelly: all three of Juniper's loud colours in one mat.",['jb','bbhp']),
('bright','Day Dreamer (Pink and Green)','Betty June & Jeannette',gal('Day Dreamer (Pink and Green)'),"Hot pink and lime medallion: picks up the chartreuse layer and the pink dots.",['ohp','plmc']),
('bright','Tropical Travels',"Let's Be Besties",gal('Tropical Travels'),"Pink, kelly and teal tropical leaves: preppy and bright.",['ohp','bbj']),
('bright','Palm Beach Tropical Pink Lime','Anders Ruff',H+'palm-beach-tropical-pink-lime.jpg',"The chartreuse layer's best friend: a lime centre inside a hot pink tropical frame.",['ohp','bbk']),
('chino','Cheetah in Chinoiserie','Sophie Clima',gal('Cheetah in Chinoiserie'),"A pagoda garden in pinks and greens under a navy sky, like the pagoda and flower tiles. Etsy, through ShopMy.",['jb','ohp']),
('chino','Whimsical Chinoiserie Meeting in the Pavilion','Sophie Clima',gal('Whimsical Chinoiserie Meeting in the Pavilion'),"Pagodas, pink blossoms and green gardens: the flower tiles as a full scene. Etsy, through ShopMy.",['opq','bbj']),
('chino','Grand Rose Medallion Chinoiserie',"Let's Be Besties",gal('Grand Rose Medallion Chinoiserie'),"Pink roses on big green lily pads around a medallion, close to the lotus flower tiles.",['opq','bbj']),
('chino','YOTD Pink','Bespoke Mahjong',gal('YOTD Pink'),"Blush ground, pink roses and a green dragon: the dragon tiles, softened.",['opq','jb']),
('chino','YOTD White','Bespoke Mahjong',gal('YOTD White'),"White ground like the faces, with roses and a teal dragon: the lightest of the dragon mats.",['owa','jb']),
('soft','The Dahlia','Bird & Bamboo',H+'the-dahlia.jpg',"Soft pink and teal-green toile: the quiet option that lets the faces do the talking.",['bbj','bblp']),
('soft','Green Bamboo Blossoms',"Let's Be Besties",gal('Green Bamboo Blossoms'),"Bamboo lattice with pink blossoms, like the bam tiles. Its sage green is softer and a little earthier than the backs.",['bbfg','bblp']),
('stone','Green Malachite','Mahj Squad',gal('Green Malachite'),"A green stone pattern that echoes the jade-look backs. Tone on tone; the faces bring the pink.",['jb','ohp']),
('stone','Evergreen','That Mahjong Moment',gal('Evergreen'),"Deep green with ferns: tone on tone, like the backs. One of your Malachite picks.",['mal','opq']),
('stone','Emerald Cove','Mahj Mood',H+'emerald-cove-mat.jpg',"A swirled emerald that looks like the tile backs themselves. Sleek and moody.",['mmc','mal']),
('stone','Emerald Teal & Celadon Leatherette','Mahjong Register',H+'emerald-teal-celedon-green-double-sided-leatherette.jpg',"The solid pick: the emerald side matches the teal layer, and the celadon side flips it softer.",['mrep','ohp']),
]
OUT=[('Lorelei','Oh My Mahjong',"Pagodas and pink, but led by bright aqua blue; Juniper has no aqua."),
('Midnight Peacock','Anders Ruff',"The right deep green, but gold and sage instead of pink."),
('Flora','Britt Mills',"Pretty pinks with no green ground to hold the backs."),
('Aria','Britt Mills',"Pink and blue watercolour; the blue pulls away from the set."),
('Pink Winds','Amanda Toppe',"The closest Amanda Toppe: soft lilac and blue, no forest green. Your Malachite Amanda Toppe picks (Petalwood, Serenity) lean lilac too."),
('Pink Orchids','Amanda Toppe',"Pink and lilac, but no green to tie in the backs."),
('Festival Malachite','Miss Mahjong',"Red, purple and blue lanterns; Juniper's greens aren't in it."),
('Cherry Blossom Malachite','Miss Mahjong',"Mostly blue and teal, with only a little green."),
('Hot Tips – Vintage Blooms','Peace Love Mahjong',"Coral flowers like the craks, but the sage-grey ground reads earthy next to the clean faces."),
]
groups={'top':('Top three','The strongest matches'),'deep':('Forest green + pink','The back, the layers and the faces all match'),'bright':('Pink & green brights','Match the faces and the chartreuse layer'),'chino':('Chinoiserie gardens','Pagodas, dragons and blossoms like the art on the tiles'),'soft':('Soft','Quieter ways to wear it'),'stone':('Stone & solid','Tone on tone with the jade-look backs')}
pile=b64('assets/tiles/album/juniper.jpg',420,85)
cc=b64('assets/colorcards/juniper/00-juniper-mahjong-tiles-tile-edit-moodboard.jpg',1800,82)
def rk(rs): return ''.join(f'<figure class="rk"><div class="rkimg"><img src="{RK[r]["img"]}" alt=""></div><figcaption><span>{html.escape(RK[r]["bn"])}</span>{html.escape(RK[r]["n"].replace(RK[r]["bn"],"").strip() or RK[r]["n"])}</figcaption></figure>' for r in rs)
cards=[];cur=None;n=0
for row in M:
  g,name,bn,img,why,racks=row[:6]; ret=len(row)>6
  n+=1
  if g!=cur: cur=g;t,s=groups[g];cards.append(f'<header class="grp"><h2>{t}</h2><p>{s}</p></header>')
  cards.append(f'''<article class="mc"><button class="ph" data-zoom aria-label="Zoom {html.escape(name)} with Juniper tiles"><img class="mat" src="{b64(img)}" alt="{html.escape(name)} mat by {html.escape(bn)}"><img class="pile" src="{pile}" alt="Juniper tiles"></button>
<div class="txt"><p class="rank">#{n}{' · <span class="ret">Retired</span>' if ret else ''}</p><h3>{html.escape(name)}</h3><p class="bn">{html.escape(bn)}</p><p class="why">{html.escape(why)}</p><p class="lab">Racks</p><div class="rks">{rk(racks)}</div></div></article>''')
outc=[]
for name,bn,why in OUT:
  outc.append(f'''<article class="mc out"><button class="ph" data-zoom aria-label="Zoom {html.escape(name)} with Juniper tiles"><img class="mat" src="{b64(gal(name,bn))}" alt="{html.escape(name)} mat by {html.escape(bn)}"><img class="pile" src="{pile}" alt="Juniper tiles"></button>
<div class="txt"><h3>{html.escape(name)}</h3><p class="bn">{html.escape(bn)}</p><p class="why">{html.escape(why)}</p></div></article>''')
tpl=open(R+'site/livepatch/juniper-picks-nov04/juniper-picks.html').read()
head=tpl[:tpl.index('<div class="wrap">')]
head=head.replace('.out{margin-top:40px;padding:16px;border-radius:12px;border:1px dashed var(--line);font-size:15px}','.mc.out{opacity:.96;border-style:dashed}.ret{display:inline-block;background:var(--muted);color:var(--card);border-radius:999px;padding:1px 8px;font-size:10px;letter-spacing:.08em}.note{margin:10px 0 0;font-size:14px;color:var(--muted)}')
script=tpl[tpl.index('<div class="lb"'):]
body=f'''<div class="wrap">
<p class="kick">Oh My Mahjong · launches Nov 11 · round 2</p>
<h1>Juniper, matched by Claude</h1>
<p class="lede">Round 2 with your notes: {n} mats in six groups, each with two racks, plus the ones I left out so you can judge them. Tap any card to zoom.</p>
<button class="cc" data-cc aria-label="Zoom the Juniper colour card"><img src="{cc}" alt="Juniper colour card: forest green jade-look backs, chartreuse and teal layers, hot pink, coral, bamboo green, mint, teal, navy and gold faces"></button>
<div class="how"><b>How I read Juniper:</b> forest green backs with a jade stone look (Oh My Mahjong: "inspired by the rich beauty of jade"), chartreuse and teal layers, and white faces. The faces that fill the table are pink and coral craks, kelly and mint bams, and pink, teal and navy dots. So the top mats need a deep or kelly green <i>and</i> pink.
<p class="note">What changed: the teal layer is called teal (not jade). Lotus Cove moved to #3 and Palm Royale to #2. Esme and Enchanted are back in (retired, still matched). New: Etsy mats (Sophie Clima, Betty June &amp; Jeannette), your Malachite picks Midori Shadows and Evergreen, and a stone-look group.</p></div>
{''.join(cards)}
<header class="grp"><h2>Left out, and why</h2><p>Judge for yourself: tell me any you'd add</p></header>
{''.join(outc)}
</div>
'''
open(sys.argv[1],'w').write(head+body+script)
print(n,'mats', os.path.getsize(sys.argv[1])/1e6,'MB')
