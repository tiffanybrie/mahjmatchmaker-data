import json,re,subprocess,base64,os,io,html
from PIL import Image
T=json.load(open('/tmp/claude-0/tiles_by_brand.json'))
R='/home/claude/mahjmatchmaker-data/'
e=html.escape
def find(brand,q):
  for x in T.get(brand,[]):
    if q.lower() in x['title'].lower(): return x.get('img')
def thumb(src):
  if not src: return ''
  try:
    if src.startswith('http') or src.startswith('//'):
      u='https:'+src if src.startswith('//') else src
      b=subprocess.run(['curl','-sL','--max-time','25',u],capture_output=True).stdout
    else: b=open(R+src,'rb').read()
    im=Image.open(io.BytesIO(b)).convert('RGB'); im.thumbnail((300,300))
    o=io.BytesIO(); im.save(o,'JPEG',quality=78)
    return 'data:image/jpeg;base64,'+base64.b64encode(o.getvalue()).decode()
  except Exception as ex: print('img fail',src,ex); return ''
# (brand, albums_done, in_progress, [(candidate, img_src_or_(brand,q), status, note)], pick_note)
HAVE=[
("Oh My Mahjong","30+ (every set, incl. Juniper)","","Every new OMM set gets an album on launch day. Nothing to decide.",[]),
("Miss Mahjong","2: Jade, Malachite","","At your limit of 2. Exception: a brand-new set.",[("Miss Darling Lilac","Miss Mahjong|Darling: Mahjong Tile Set - Lilac","NEW · coming soon, no date","$425 full-size, party version of Cameo Blue")]),
("Bam Bird Boutique","2: Classic Tortoise, Deco Lagoon","Deco Indigo + Mulberry (you're doing these)","Rounding out their two most popular sets.",[("MCM","Bam Bird Boutique|MCM","Available","Queued after the Deco trio")]),
("Anders Ruff","2: Brownstone Bloom, Dear Santa (holiday)","Green Light Gatsby (round 1 done, 32 yes)","Gatsby is half done; bridal set coming (no date).",[("Green Light Gatsby","Anders Ruff|Green Light Gatsby","Preorder","Finish round 2 (26 mats)")]),
("Sunday Mahjong (non-partner)","2: Sunday Tile Set, December 1994 (holiday)","Sunday Blues","Personal favorite line.",[]),
("Charleston Mahjong Club","1: Après Ski Club (holiday)","Cabana Club (you said it goes before Darling Lilac)","",[("Cabana Club (full size)","assets/launches/cmc-cabana-club-teaser","Email subscribers now; next batch December","Swipe book already exists")]),
("Virora Mahjong","1: Nivalee Glacier Blue (holiday)","Tinselle Emerald (holiday, stalled); Petalée banked (61 cards)","",[]),
("Bam! Let's Mahjong","1: Holly Jolly (3 colours, holiday)","","Only a holiday album. Year-round pick:",[("Art Deco tiles","Bam! Let's Mahjong|Art Deco","Available · $475","Their new pink floral mat (coming) pairs with it")]),
("Hip Hip Mahjong","1: Rackin' Rudolph (holiday)","","Only a holiday album. Year-round pick:",[("So Bam Grateful","Hip Hip Mahjong|So Bam Grateful","Available · $400","Newest set (Sept)")]),
("Mahj Squad","1: Nutcracker Ballet (holiday)","","Only a holiday album. Year-round options:",[("Parisian","Mahj Squad|Parisian","Available · $400",""),("Blue Chinoiserie","Mahj Squad|Blue Chinoiserie","Available · $350","")]),
("Mahjong Row & Co.","1: Cypress","","On hold (code paused).",[]),
]
NONE=[
("Bespoke Mahjong","Red tiles you can play year-round, landing mid-holiday (your idea).",[("Glitter Glow Red (It's a Vibe)","Bespoke Mahjong|GLITTER GLOW RED","NEW · coming in November, no exact date","$495"),("Sunshine Glow","Bespoke Mahjong|SUNSHINE GLOW","NEW · live Nov 4","$495"),("Glitter Glow Green","Bespoke Mahjong|GLITTER GLOW GREEN","NEW · coming in November","$495")]),
("Mahj Pit","Christmas tiles launch today.",[("Christmas tiles","assets/social/mahj-pit-christmas-tiles-nov11/christmas-tiles-launch-1111-DfId2tWPVhq.jpg","NEW · launching Nov 11","Holiday album candidate"),("Confetti tiles","Mahj Pit|Confetti","Restock Nov 11","$395")]),
("Let's Mahj On","Brand-new set out now, five more rolling out.",[("Let's Golf! (Celadon Mist / Magnolia Blush)","Let's Mahj On|Celedon","NEW · out Nov 9","$385; Wild, Sweet, Refined, Merry, Stir Things Up still to come")]),
("Middle & Main Mahjong","Peach & Pine (swiped earlier) is unavailable on their store now.",[("Summit to Sea","","NEW · in their store, online soon, no date",""),("Clearwater Dockside","Middle & Main Mahjong|Clearwater","NEW · Nov 5","$250"),("Peach & Pine","Middle & Main Mahjong|Peach","Not available right now","Swiped in October")]),
("Mahj Mood","All sets are preorder; ships Jan, so an album in Dec/Jan fits.",[("Playing For Keeps","Mahj Mood|Playing For Keeps","NEW · preorder, ships January","$390"),("Radiant Mood White Pearl","Mahj Mood|White Pearl","Preorder, ships end of November","$390"),("The Eloise Collection","Mahj Mood|Eloise","Preorder, ships January","$390")]),
("Mac + Miller Mahjong","Fire + Fortune was swiped; waits on clean, non-watermarked photos.",[("Fire + Fortune: Verdant Fortune","Mac + Miller Mahjong|Verdant","Available · $350",""),("Ember Fire","Mac + Miller Mahjong|Ember","Coming soon",""),("Red, White & Blues","Mac + Miller Mahjong|Red, White","Preorder","")]),
("My Fair Mahjong","Style of Your Life is banked (you skipped it: Dillard's exclusive). The set you struggled to pick.",[("The Jubilee Series (Pearl White / Midnight Blue)","My Fair Mahjong|Pearl White","Available · $395","Newest (Aug)"),("Crystal Confetti Calm Blue","My Fair Mahjong|Calm Blue","Available · $375",""),("Crystal Confetti Sorbet Pink","My Fair Mahjong|Sorbet Pink","Available · $375","")]),
("Noli June","",[("Holiday Soirée","Noli June|Holiday Soir","Available · $385","Holiday album candidate"),("The Chinoiserie Set (3 colours)","Noli June|CHINOISERIE SET -  MAHJONG TILES:  POLISHED","Available · $399",""),("The Riviera Jet Set","Noli June|RIVIERA","Available · $479","")]),
("Bird & Bamboo","",[("The Iconic","Bird & Bamboo|Iconic","Available · $375","Newest (July)"),("The Madeira","Bird & Bamboo|Madeira","Available · $375",""),("The Empress","Bird & Bamboo|Empress","Available · $375","")]),
("Amahj","New Stamped set teased (mint green).",[("On the Water","Amahj|On the Water","NEW · Oct 18, $258",""),("New Stamped set (mint)","","Coming, no name or date","")]),
("Peace Love Mahjong","Holiday tiles item is stalled; their other full-size sets are kids' sets.",[("Spirit of Christmas + Merry Nutcracker","","Holiday","Stalled item on HQ")]),
("Mah Jongg Maven","",[("Coca-Cola Classic","https://mahjonggmaven.com/wp-content/uploads/2026/08/tile-set--scaled.jpg","Preorder, ships early December","$450")]),
("YOLO Mahjong","",[("Journey to the West","YOLO Mahjong|Journey","2nd batch reservations, delivery Jan 2027","$438")]),
("Maison Mahj","",[("House Line No. 1","Maison Mahj|House Line","Preorder, ships Feb 2027","$595")]),
("The Royal Mahjong Society","",[("Crown Jewels","","Studio Series on sale; Heirloom soon","")]),
("Tigre de Tartán","Code is image-only on the site.",[("House Tigers Oyster","","Available","")]),
("Mahjong Studios","Budget sets. Their mats are out, tiles are fine.",[("Ruby / Royal / Lavender Sparkle","Mahjong Studios|Ruby Sparkle","Available · $225","")]),
("Mini Mahjer","Our store watch shows no full-size tile set; I'll check their store.",[]),
]
MATONLY="Britt Mills, Amanda Toppe, Wren Mats, Mahj & Vine, Fait à Main, Let's Be Besties, Soirée All Day, Mahjong Register, I Love Mahj, The Mahjong Press, Mahjong Co., Splash of Color, Sweet Jojo Designs, Mahjong by SI"
PICKS=[("Bespoke Glitter Glow Red","new red set, year-round, mid-holiday"),("Charleston Cabana Club","your call: before Darling Lilac"),("Mahj Pit Christmas tiles","new today, holiday window"),("Let's Mahj On: Let's Golf!","new Nov 9, more sets coming"),("Middle & Main: Summit to Sea","when it goes online (Peach & Pine is unavailable)"),("Mahj Mood: Playing For Keeps","ships January"),("Mac + Miller: Fire + Fortune","once clean photos exist"),("Bird & Bamboo: The Iconic","newest set"),("My Fair Mahjong: Jubilee","newest set"),("Noli June: Holiday Soirée","if a holiday slot opens"),("Miss Mahjong: Darling Lilac","skips the line the week it gets a date")]
def img(spec):
  if not spec: return ''
  if '|' in spec: b,q=spec.split('|',1); spec=find(b,q) or ''
  elif spec.startswith('assets/') and os.path.isdir(R+spec): spec=spec+'/'+sorted(os.listdir(R+spec))[0]
  return thumb(spec)
def cand(c):
  n,s,st,note=c; src=img(s)
  return f'<div class="cand">'+(f'<img src="{src}" alt="">' if src else '<div class="noimg">no photo yet</div>')+f'<div class="cn"><b>{e(n)}</b><span class="st{" new" if st.startswith("NEW") else ""}">{e(st)}</span>'+(f'<small>{e(note)}</small>' if note else '')+'</div></div>'
rows_none=''.join(f'<section class="brand"><h3>{e(b)}<span class="pill zero">0 albums</span></h3>'+(f'<p>{e(n)}</p>' if n else '')+f'<div class="cands">{"".join(cand(c) for c in C)}</div></section>' for b,n,C in NONE)
rows_have=''.join(f'<section class="brand"><h3>{e(b)}<span class="pill">{e(a.split(":")[0])} album{"s" if not a.startswith("1") else ""}</span></h3><p><b>Done:</b> {e(a)}'+(f'<br><b>In progress:</b> {e(ip)}' if ip else '')+(f'<br>{e(n)}' if n else '')+'</p>'+(f'<div class="cands">{"".join(cand(c) for c in C)}</div>' if C else '')+'</section>' for b,a,ip,n,C in HAVE)
picks=''.join(f'<li><b>{e(a)}</b> <span>{e(b)}</span></li>' for a,b in PICKS)
page=open('/tmp/claude-0/plan/tpl.html').read().replace('{{PICKS}}',picks).replace('{{NONE}}',rows_none).replace('{{HAVE}}',rows_have).replace('{{MATONLY}}',e(MATONLY))
open('/tmp/claude-0/plan/album-plan.html','w').write(page); print('ok',len(page))
