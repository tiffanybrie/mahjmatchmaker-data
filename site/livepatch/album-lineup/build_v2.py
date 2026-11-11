import json,re,subprocess,base64,io,html,os,concurrent.futures as cf
from PIL import Image
e=html.escape
S=json.load(open('/tmp/claude-0/plan2/sets2.json'))
ALB={"Oh My Mahjong":("31 albums (every set incl. retired, Coquette, Juniper)",""),
"Miss Mahjong":("2: Jade, Malachite","At your limit of 2 until everyone has one. A brand-new set can still jump the line."),
"Bam Bird Boutique":("2: Classic Tortoise, Deco Lagoon","Deco Indigo + Mulberry review pages are ready for you; MCM after."),
"Anders Ruff":("2: Brownstone Bloom, Dear Santa (holiday)","Green Light Gatsby half done (32 yes)."),
"Sunday Mahjong":("2: Sunday Tile Set, December 1994 (holiday)","Sunday Blues building; Nature Walk, Plum Panda, Hummingbird queued."),
"Charleston Mahjong Club":("1: Après Ski Club (holiday)","Cabana Club swipe book is ready for you."),
"Virora Mahjong":("1: Nivalee Glacier Blue (holiday)","Tinselle Emerald (holiday) kit queued; Petalée banked (61 cards)."),
"Bam! Let's Mahjong":("1: Holly Jolly (holiday only)","Needs a year-round album."),
"Hip Hip Mahjong":("1: Rackin' Rudolph (holiday only)","Needs a year-round album."),
"Mahj Squad":("1: Nutcracker Ballet (holiday only)","Needs a year-round album."),
}
NOTE={"Mahj Pit":"No Christmas album (too late; Christmas is planned Sept-Oct). Year-round set needed.",
"Noli June":"No holiday album (too late). Year-round set needed.",
"Mahj Mood":"You like their Mauve-Blush (one of your favorite pink tiles, popular). Playing For Keeps is new: pick it only if you love it.",
"Mac + Miller Mahjong":"Fire + Fortune = Verdant Fortune + Ember Fire (photos below). Watermarked photos are OK, like Sunday.",
"Middle & Main Mahjong":"Peach & Pine is queued for me to build (it was picked Oct 28 but never actually swiped). Goes with a lot of Britt Mills mats. Not for sale on their site right now.",
"Bespoke Mahjong":"Glitter Glow Red (coming in November) is the red set you mentioned. Showing their full-size sets; custom $4,000+ sets left out.",
"My Fair Mahjong":"Style of Your Life is banked (Dillard's exclusive, you skipped it).",
"Bird & Bamboo":"Lowest priority (your call): known for racks and heavily featured on the rack side. Newest set is The Iconic (July 2026); nothing coming soon on her store.",
"Peace Love Mahjong":"Their store shows only kids' sets and holiday tiles (Spirit of Christmas, Merry Nutcracker); no year-round full-size set found.",
"Splash of Color":"Mats are out of Find Your Mat-ch; they do sell tile sets.",
"Yellow Mountain Imports":"Never featured (your rule).",
"Mahjong Studios":"Budget sets; their mats are out, tiles are fine.",
"Tigre de Tartan":"Code is image-only on the site.",
"Mah Jongg Maven":"Their store isn't readable by our watch; Coca-Cola Classic found by hand.",
"The Mahjong Press":"Store is The Mahjong House (themahjonghouse.com): they DO sell tile sets.",
}
NOTILES={"Britt Mills":"mats + racks","Amanda Toppe":"art mats (store not readable by our watch; please check)","Mini Mahjer":"mats, no tile sets in their store","Wren Mats":"mats (store not readable; please check)","Mahj & Vine":"mats","Mahjong Co.":"1 product (mat)","I Love Mahj":"app / lessons, no store","Soirée All Day":"mats + tablecloths (store not readable; please check)","Mahjong Register":"mats + racks (81 products, no tile set)","Let's Be Besties":"mats","Mahjong by SI":"onboarding; no store link yet","Sweet Jojo Designs":"Amazon mats","Fait à Main":"mats (bandana / Texas mats)"}
PICKS=[("Charleston Cabana Club","your call; swipe book ready"),("Bespoke Glitter Glow Red","new red set, year-round, mid-holiday"),("Let's Mahj On: Let's Golf!","new Nov 9"),("Mahj Mood: Playing For Keeps or Mauve-Blush","your pick from the photos"),("Mac + Miller: Fire + Fortune","watermarked photos OK"),("Middle & Main: Peach & Pine","queued for me to build, not urgent"),("My Fair Mahjong","pick from photos"),("Noli June / Mahj Pit / Royal / The Mahjong Press / Amahj","year-round sets, pick from photos"),("Miss Mahjong: Darling Lilac","only when it gets a date"),("Bird & Bamboo","last: her racks are her strength and well featured")]
def th(u):
  if not u: return ''
  u='https:'+u if u.startswith('//') else u
  if 'cdn.shopify.com' in u and 'width=' not in u: u+=('&' if '?' in u else '?')+'width=360'
  try:
    b=subprocess.run(['curl','-sL','--max-time','25',u],capture_output=True).stdout
    im=Image.open(io.BytesIO(b)).convert('RGB'); im.thumbnail((240,240)); o=io.BytesIO(); im.save(o,'JPEG',quality=72)
    return 'data:image/jpeg;base64,'+base64.b64encode(o.getvalue()).decode()
  except Exception: return ''
CAP=24
jobs={}
for b,v in S.items():
  for s in v['sets'][:CAP]: jobs[s['img']]=None
with cf.ThreadPoolExecutor(12) as ex:
  for u,r in zip(list(jobs),ex.map(th,list(jobs))): jobs[u]=r
def st(s):
  t=[]
  if s.get('pre') or s.get('pretags'): t.append('preorder / coming' if s.get('pretags') else 'preorder')
  t.append('in stock' if s.get('avail') else 'sold out')
  return ' · '.join(t)
def chip(s):
  src=jobs.get(s['img']) or ''
  new=(s.get('pub') or '')>='2026-10-01'
  return f'<a class="cand" href="{e(s["url"])}" target="_blank" rel="noopener">'+(f'<img src="{src}" alt="">' if src else '<div class="noimg">no photo</div>')+f'<div class="cn"><b>{e(re.sub(r"\s+"," ",s["title"])[:70])}</b><span class="st{" new" if new else ""}">{"NEW · " if new else ""}${int(s["price"] or 0)} · {e(st(s))}</span></div></a>'
order=sorted(S, key=lambda b:(0 if b not in ALB and S[b]['sets'] and b not in ('Yellow Mountain Imports',) else 1 if b in ALB else 2, b))
secs=''
for b in order:
  v=S[b]; sets=v['sets']
  if not sets: continue
  a=ALB.get(b,("0 albums",""))
  more=f'<p class="more">+{len(sets)-CAP} more sets on their store.</p>' if len(sets)>CAP else ''
  secs+=f'<section class="brand" id="{re.sub(r"[^a-z0-9]+","-",b.lower())}"><h3>{e(b)}<span class="pill{" zero" if a[0].startswith("0") else ""}">{e(a[0].split(":")[0] if ":" in a[0] else a[0])}</span></h3>'+(f'<p><b>Albums:</b> {e(a[0])}</p>' if b in ALB else '')+''.join(f'<p>{e(x)}</p>' for x in (a[1],NOTE.get(b,'')) if x)+f'<div class="cands">{"".join(chip(s) for s in sets[:CAP])}</div>{more}</section>'
def row(b,v):
  a=ALB.get(b,("0",""))[0]; n=len(v['sets'])
  tiles = f'{n} tile set{"s" if n!=1 else ""}' if n else NOTILES.get(b,'none found in their store')
  link=f' <a href="#{re.sub(r"[^a-z0-9]+","-",b.lower())}">see sets</a>' if n else ''
  return f'<tr><td><b>{e(b)}</b><br><small>{e(v["stage"])}</small></td><td>{e(a)}</td><td>{e(tiles)}{link}</td></tr>'
srt=sorted(S.items(), key=lambda kv:kv[0].lower())
rows_t=''.join(row(b,v) for b,v in srt if v['sets'])
rows_n=''.join(row(b,v) for b,v in srt if not v['sets'])
rows=rows_t
picks=''.join(f'<li><b>{e(x)}</b> <span>{e(y)}</span></li>' for x,y in PICKS)
tpl=open('/tmp/claude-0/plan/tpl.html').read()
tpl=tpl.replace('<h2>No album yet (tile makers)</h2>\n{{NONE}}\n<h2>Have albums</h2>\n{{HAVE}}','<h2>Every partner ({N})</h2><h3 style="margin-top:6px">Make tile sets ({NT})</h3><div class="tw"><table><thead><tr><th>Brand</th><th>Match albums</th><th>Tile sets on their store</th></tr></thead><tbody>{{ROWS}}</tbody></table></div><h3 style="margin-top:14px">No tile sets: mats, racks or other ({NN})</h3><div class="tw"><table><thead><tr><th>Brand</th><th>Match albums</th><th>What they sell</th></tr></thead><tbody>{{ROWSN}}</tbody></table></div>\n<h2>Every tile set, by brand</h2><p class="lede">Brands with no album first. Tap a set to open it on the brand\'s site. NEW = listed since Oct 1.</p>\n{{SECS}}')
tpl=tpl.replace('<div class="box"><h2 style="margin:0">Mat and rack partners (no tile album needed)</h2><p class="lede">{{MATONLY}}. Their mats show up inside other brands\' albums.</p></div>','')
tpl=tpl.replace('a.cand','a.cand').replace('.cand{','a.cand{color:inherit;text-decoration:none}.more{color:var(--muted);margin:0}.tw{overflow-x:auto}table{border-collapse:collapse;width:100%;background:var(--card);border:1px solid var(--line);border-radius:12px}th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top;font-size:14px}td small{color:var(--muted)}td a{color:var(--pink)}\n.cand{')
page=tpl.replace('{{PICKS}}',picks).replace('{{ROWS}}',rows_t).replace('{{ROWSN}}',rows_n).replace('{NT}',str(sum(1 for b,v in srt if v['sets']))).replace('{NN}',str(sum(1 for b,v in srt if not v['sets']))).replace('{{SECS}}',secs).replace('{N}',str(len(S)))
page=page.replace('Every partner that makes tile sets, how many match albums they have, and the sets we could do next.','Every partner (including the newest affiliates and the two still onboarding), how many match albums they have, and a photo + link for every full-size tile set on their store.').replace('Built Wed 11/11 from the partner store watch and HQ albums.','Updated Wed 11/11 12:45pm from each brand\'s live store and HQ albums. Holiday albums only for brands that already have one.')
open('/tmp/claude-0/plan/album-plan.html','w').write(page); print(len(page))
