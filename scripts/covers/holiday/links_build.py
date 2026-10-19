import json,sys
# ALBUM ORDER (Oct 15, Tiffany: newest/most popular first, not by color):
# pop.json = the 12 newest LIVE album pages, newest first. "Live date" = the creation
# time embedded in each Squarespace page's collection id (first 8 hex chars of the
# ObjectId, from <album-url>?format=json), checked Oct 15 2026 for all 37 albums in
# work/album-urls.txt. We have no traffic numbers per album, so recency decides.
# Images: 2x the CSS display size (album 140px -> 280x350, holiday ~150px -> 300x375),
# resized with Lanczos from the 1080x1350 originals.
pop=json.load(open('pop.json'))
HOLIDAY=[('dear-santa','Dear Santa'),('rackin-rudolph',"Rackin' Rudolph"),('tinselle-emerald','Tinselle Emerald')]  # Tiffany's top 3 (Oct 15)
S='https://www.mahjmatchmaker.com'
FYM=S+'/find-your-match'  # planned page: goes live on launch day (Nov 3 proposed, doc 54)
FAN=['talulah','gatsby','emerald']
FYM_LIVE=False  # flip to True on 10/27 when /find-your-match goes live (then the card links)
NEWSET=('papaya-spritz','Papaya Spritz','Oh My Mahjong','Launches Wed 10/21 · see all 50 of her matches')  # launch-week feature card (doc 86 step 11)  # album covers fanned on the Find Your Match card (left, right, center)
def build(img,tgt):
    # tgt(url) -> target attrs; preview opens everything in a new tab
    COLORS=[('Holiday','#a3192e','/holiday-mahjong-matches'),('Red','#c8343c','/red-mahjong-tile-matches'),('Pink','#d6568a','/pink-mahjong-tile-matches'),('Yellow & Orange','#e08a2e','/yellow-orange-mahjong-tile-matches'),('Green','#3f8f55','/green-mahjong-tile-matches'),('Blue','#3f6fb5','/blue-mahjong-tile-matches'),('Purple','#7d55b0','/purple-mahjong-tile-matches'),('Brown','#7a4a2a','/brown-mahjong-tile-matches'),('Ivory','#b9a57a','/ivory-mahjong-tile-matches'),('Natural Patterns','#8a6a3a','/neutral-mahjong-tile-matches')]
    chips=''.join(f'<a class="chip" href="{S}{u}"{tgt(S+u)} style="--c:{c}">{n}</a>' for n,c,u in COLORS)
    strip=''.join(f'<a class="alb" href="{S}/{k}-mahjong-tile-matches"{tgt(S)}><img src="{img("v2/album-"+k+".jpg")}" width="140" height="175" alt="{t} mahjong tile matches" loading="lazy"><span>{t}</span></a>' for k,t,_ in pop)
    fan=''.join(f'<img class="f{n}" src="{img("v2/album-"+k+".jpg")}" width="118" height="148" alt="">' for n,k in zip((1,2,3),FAN))
    hol=''.join(f'<img src="{img("v2/holiday-"+k+".jpg")}" width="150" height="188" alt="{t} mahjong tiles holiday matches">' for k,t in HOLIDAY)
    btn=lambda ico,t,s,u,c='btn': f'<a class="{c}" href="{u}"{tgt(u)}><span class="ico">{ico}</span><span class="tx"><b>{t}</b><small>{s}</small></span><span class="ar">›</span></a>'
    return f'''<style>
.mml{{--cream:#fdf0e6;--navy:#1f3a6b;--pink:#e36a8f;--red:#a3192e;--card:#fff;max-width:480px;margin:0 auto;padding:22px 16px 40px;color:var(--navy);font-family:Montserrat,system-ui,sans-serif;background:var(--cream)}}
.mml *{{box-sizing:border-box}}.mml a{{text-decoration:none!important;color:inherit}}
.mml .hd{{text-align:center}}.mml .hs{{width:104px;height:104px;border-radius:50%;border:4px solid #fff;box-shadow:0 6px 18px rgba(31,58,107,.18)}}
.mml .lg{{display:block;width:250px;max-width:70%;margin:10px auto 2px}}.mml .tag{{font-weight:700;font-size:15px;margin:4px 0 8px}}
.mml .omm{{height:44px;margin:0 auto 6px;display:block}}
.mml .code{{display:flex;align-items:center;gap:10px;background:var(--navy);color:#fff;border-radius:18px;padding:12px 12px 12px 18px;margin:14px 0 6px}}
.mml .code div{{flex:1;line-height:1.25}}.mml .code small{{display:block;opacity:.85;font-size:12px;letter-spacing:.08em;text-transform:uppercase}}.mml .code b{{font-size:22px;letter-spacing:.06em}}
.mml .code button{{font:700 14px Montserrat,system-ui,sans-serif;border:0;border-radius:999px;padding:10px 16px;background:var(--pink);color:#fff;cursor:pointer}}
.mml .where{{display:block;text-align:center;font-size:13px;font-weight:600;margin-bottom:18px;text-decoration:underline!important}}
.mml .feat{{display:block;border-radius:20px;overflow:hidden;background:var(--red);color:#fff;box-shadow:0 8px 22px rgba(163,25,46,.25);margin-bottom:18px}}
.mml .feat .hol{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px;padding:8px 8px 0}}.mml .feat .hol img{{width:100%;height:auto;aspect-ratio:4/5;display:block;border-radius:12px}}.mml .feat div{{padding:12px 16px 14px;display:flex;align-items:center;gap:10px}}
.mml .feat b{{font-family:Caprasimo,Georgia,serif;font-weight:400;font-size:24px;flex:1;line-height:1.1}}.mml .feat small{{display:block;font-family:Montserrat,system-ui,sans-serif;font-size:13px;opacity:.9;margin-top:3px}}
.mml h2{{font-family:Caprasimo,Georgia,serif;font-weight:400;font-size:22px;margin:22px 0 10px;text-align:center;color:var(--red)}}
.mml .row{{display:flex;gap:10px;overflow-x:auto;scroll-snap-type:x mandatory;padding:2px 2px 10px;margin:0 -16px;padding-left:16px;padding-right:16px;-webkit-overflow-scrolling:touch}}
.mml .alb{{flex:0 0 140px;scroll-snap-align:start;text-align:center;font-size:13px;font-weight:700}}.mml .alb img{{width:140px;height:auto;aspect-ratio:4/5;object-fit:cover;border-radius:12px;display:block;margin-bottom:5px;box-shadow:0 3px 10px rgba(0,0,0,.12)}}
.mml .all{{display:block;text-align:center;font-weight:700;font-size:14px;margin:2px 0 6px;text-decoration:underline!important}}
.mml .chips{{display:flex;flex-wrap:wrap;gap:8px;justify-content:center}}.mml .chip{{padding:8px 14px;border-radius:999px;background:var(--c);color:#fff!important;font-weight:700;font-size:14px}}
.mml .btn{{display:flex;align-items:center;gap:12px;background:var(--card);border-radius:16px;padding:13px 14px;margin:10px 0;box-shadow:0 3px 12px rgba(31,58,107,.08);border:2px solid transparent;transition:transform .15s,border-color .15s}}
.mml .btn:hover{{transform:translateY(-2px);border-color:var(--pink)}}.mml .ico{{font-size:24px;width:40px;height:40px;border-radius:12px;background:var(--cream);display:flex;align-items:center;justify-content:center;flex:none}}
.mml .tx{{flex:1;line-height:1.25}}.mml .tx b{{display:block;font-size:16px}}.mml .tx small{{font-size:13px;opacity:.8}}.mml .ar{{font-size:24px;opacity:.5}}
.mml .nw{{display:block;border-radius:22px;overflow:hidden;background:#df772f;color:#fff;box-shadow:0 10px 24px rgba(223,119,47,.32);margin:16px 0 4px}}.mml .nw img{{width:100%;height:auto;display:block}}
.mml .nw div{{padding:12px 16px 14px;display:flex;align-items:center;gap:10px}}.mml .nw .new{{font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;background:#fff;color:#df772f;border-radius:999px;padding:4px 10px;flex:none}}
.mml .nw b{{font-family:Caprasimo,Georgia,serif;font-weight:400;font-size:26px;flex:1;line-height:1.05}}.mml .nw small{{display:block;font-family:Montserrat,system-ui,sans-serif;font-size:13px;opacity:.95;margin-top:4px}}
/* Find Your Match: top, biggest card */
.mml .fym{{display:block;border-radius:24px;overflow:hidden;background:var(--navy);color:#fff;box-shadow:0 10px 26px rgba(31,58,107,.3);margin:16px 0 14px;text-align:center;padding:20px 16px 18px}}
.mml .fym .new{{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;background:var(--pink);border-radius:999px;padding:4px 12px}}
.mml .fan{{position:relative;height:178px;margin:14px auto 6px;max-width:300px}}
.mml .fan img{{position:absolute;top:8px;left:50%;width:118px;height:auto;aspect-ratio:4/5;object-fit:cover;border-radius:14px;border:3px solid #fff;box-shadow:0 6px 16px rgba(0,0,0,.3)}}
.mml .fan .f1{{transform:translateX(-118%) rotate(-10deg)}}.mml .fan .f2{{transform:translateX(18%) rotate(10deg)}}.mml .fan .f3{{transform:translateX(-50%) translateY(-6px);z-index:2}}
.mml .fan .no,.mml .fan .yes{{position:absolute;bottom:2px;z-index:3;width:40px;height:40px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;font-size:19px;font-weight:700;box-shadow:0 4px 10px rgba(0,0,0,.25)}}
.mml .fan .no{{left:calc(50% - 74px);color:#9aa3b5}}.mml .fan .yes{{right:calc(50% - 74px);color:var(--pink)}}
.mml .fym b{{display:block;font-family:Caprasimo,Georgia,serif;font-weight:400;font-size:34px;line-height:1.05;margin-top:6px}}
.mml .fym p{{margin:8px auto 14px;font-size:15px;line-height:1.35;max-width:300px;opacity:.95}}
.mml .fym .go{{display:inline-block;background:var(--pink);color:#fff;font-weight:700;font-size:16px;border-radius:999px;padding:12px 26px}}
/* small "More" links at the bottom */
.mml .more{{margin-top:6px}}.mml .more .btn{{padding:9px 12px;margin:7px 0;border-radius:14px;box-shadow:none;background:rgba(255,255,255,.6)}}
.mml .more .ico{{font-size:18px;width:32px;height:32px;border-radius:10px}}.mml .more .tx b{{font-size:14px}}.mml .more .tx small{{font-size:12px}}.mml .more .ar{{font-size:20px}}
.mml .more .btn.sm{{padding:6px 12px;opacity:.85}}.mml .more .btn.sm .ico{{font-size:15px;width:26px;height:26px}}.mml .more .btn.sm .tx b{{font-size:13px}}
.mml h2.h3{{font-size:17px;margin:26px 0 4px;opacity:.85}}
.mml .ft{{text-align:center;margin-top:22px;font-size:12px;opacity:.75}}.mml .ft img{{width:26px;vertical-align:middle}}
</style>
<div class="mml">
<div class="hd"><img class="hs" src="{img('headshot.png')}" alt="Tiffany of Mahj Matchmaker"><img class="lg" src="{img('logo.png')}" alt="Mahj Matchmaker"><div class="tag">Hooking up tiles, mats &amp; racks 💕</div><img class="omm" src="{img('omm.png')}" alt="Oh My Mahjong certified instructor"></div>
<!-- FIND YOUR MATCH: first and biggest link (Tiffany, Oct 15 6:58pm).
     NOTE: /find-your-match is the PLANNED page. It goes live on launch day (Mahj Matchmaker 2.0, doc 54);
     until then this link would 404, so the page and this link launch together. -->
<a class="nw" href="{S}/{NEWSET[0]}-mahjong-tile-matches"{tgt(S)}><img src="{img('v2/feature-'+NEWSET[0]+'.jpg')}" alt="{NEWSET[1]} mahjong tiles" width="448" height="246"><div><span class="new">New</span><b>{NEWSET[1]}<small>{NEWSET[2]} · {NEWSET[3]}</small></b><span style="font-size:26px">›</span></div></a>
{(f'<a class="fym" href="{FYM}"{tgt(FYM)}>' if FYM_LIVE else '<div class="fym">')}<span class="new">{'New' if FYM_LIVE else 'Coming 10.27'}</span>
<div class="fan">{fan}<span class="no">✕</span><span class="yes">♥</span></div>
<b>Find Your Match</b><p>Pick your tiles, then swipe through mats and racks that match them.</p>{('<span class="go">Start matching ›</span></a>' if FYM_LIVE else '<span class="go" style="opacity:.75">Coming October 27</span></div>')}
<div class="code"><div><small>Partner brand discount</small><b>MAHJMATCH</b></div><button type="button" onclick="(navigator.clipboard?navigator.clipboard.writeText('MAHJMATCH'):Promise.reject()).then(()=>{{this.textContent='Copied ✓'}}).catch(()=>{{this.textContent='MAHJMATCH'}})">Copy code</button></div>
<a class="where" href="{S}/mahjong-discount-codes"{tgt(S)}>See all our partner brands ›</a>
<a class="feat" href="{S}/holiday-mahjong-matches"{tgt(S)}><div class="hol">{hol}</div><div><b>Holiday Matches 🎄<small>Christmas tiles, mats &amp; racks, matched</small></b><span style="font-size:26px">›</span></div></a>
<h2>Tile album matches</h2>
<!-- newest live albums first (see pop.json / build script comment) -->
<div class="row">{strip}</div>
<a class="all" href="{S}/mahjong-tile-matches"{tgt(S)}>See all tile albums ›</a>
<h2>Shop by tile color</h2>
<div class="chips">{chips}</div>
<h2>My most helpful guides</h2>
<!-- picked from the live blog Oct 15: the most helpful, non-overlapping guides (no color round-ups) -->
{btn('🎄','Christmas mahjong guide','Holiday tiles, mats &amp; racks for 2026',S+'/blog/christmas-mahjong-sets')}
{btn('📖','Mahjong buying guide','Tiles, mat, racks: what to buy first',S+'/blog/mahjong-buying-guide')}
{btn('🀄','My most versatile tile sets','Wood, pearl, tortoise &amp; stone looks',S+'/blog/most-versatile-mahjong-tiles')}
{btn('🟫','The most versatile mats','Mats that go with almost any tiles',S+'/blog/most-versatile-mahjong-mats')}
{btn('✨','My favorite racks','The racks I recommend first',S+'/blog/my-favorite-mahjong-racks')}
<h2>Help me match</h2>
{btn('💌','Request an album','Tell me which tiles to match next',S+'/request-an-album')}
{btn('📸','Share your table','Send me your tiles + mat combo',S+'/share-your-table')}
<h2 class="h3">More</h2>
<div class="more">
{btn('💬','Facebook group','Matches, new drops &amp; table photos','https://www.facebook.com/groups/mahjmatchmaker')}
{btn('🎓','Book a lesson','With an OMM certified instructor',S+'/private-mahjong-lessons')}
{btn('📅','Events &amp; rentals','Parties and table rentals',S+'/events','btn sm')}
</div>
<div class="ft"><img src="{img('flame.png')}" alt=""> mahjmatchmaker.com</div>
</div>'''
# preview artifact
prev=build(lambda f:'img/'+f, lambda u:' target="_blank" rel="noopener"')
open('index.html','w').write('<title>Mahj Matchmaker Links</title><link href="https://fonts.googleapis.com/css2?family=Caprasimo&family=Montserrat:wght@500;600;700&display=swap" rel="stylesheet"><style>:root{color-scheme:light}body{margin:0;background:#fdf0e6}</style>'+prev)
# live squarespace code block (images via repo CDN)
CDN='https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@partner-catalogs-sqsp/assets/links/'
# on the live site, own pages open in the same tab; outside sites (Facebook) open a new tab
open('squarespace_code_block.html','w').write('<link href="https://fonts.googleapis.com/css2?family=Caprasimo&family=Montserrat:wght@500;600;700&display=swap" rel="stylesheet">'+build(lambda f:CDN+f, lambda u:'' if u.startswith(S) else ' target="_blank" rel="noopener"'))
print('ok')
