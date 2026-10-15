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
def build(img,tgt):
    # tgt(url) -> target attrs; preview opens everything in a new tab
    COLORS=[('Holiday','#a3192e','/holiday-mahjong-matches'),('Red','#c8343c','/red-mahjong-tile-matches'),('Pink','#d6568a','/pink-mahjong-tile-matches'),('Yellow & Orange','#e08a2e','/yellow-orange-mahjong-tile-matches'),('Green','#3f8f55','/green-mahjong-tile-matches'),('Blue','#3f6fb5','/blue-mahjong-tile-matches'),('Purple','#7d55b0','/purple-mahjong-tile-matches'),('Brown','#7a4a2a','/brown-mahjong-tile-matches'),('Ivory','#b9a57a','/ivory-mahjong-tile-matches'),('Natural Patterns','#8a6a3a','/neutral-mahjong-tile-matches')]
    chips=''.join(f'<a class="chip" href="{S}{u}"{tgt(S+u)} style="--c:{c}">{n}</a>' for n,c,u in COLORS)
    strip=''.join(f'<a class="alb" href="{S}/{k}-mahjong-tile-matches"{tgt(S)}><img src="{img("v2/album-"+k+".jpg")}" width="140" height="175" alt="{t} mahjong tile matches" loading="lazy"><span>{t}</span></a>' for k,t,_ in pop)
    hol=''.join(f'<img src="{img("v2/holiday-"+k+".jpg")}" width="150" height="188" alt="{t} mahjong tiles holiday matches">' for k,t in HOLIDAY)
    btn=lambda ico,t,s,u: f'<a class="btn" href="{u}"{tgt(u)}><span class="ico">{ico}</span><span class="tx"><b>{t}</b><small>{s}</small></span><span class="ar">›</span></a>'
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
.mml .ft{{text-align:center;margin-top:22px;font-size:12px;opacity:.75}}.mml .ft img{{width:26px;vertical-align:middle}}
</style>
<div class="mml">
<div class="hd"><img class="hs" src="{img('headshot.png')}" alt="Tiffany of Mahj Matchmaker"><img class="lg" src="{img('logo.png')}" alt="Mahj Matchmaker"><div class="tag">Hooking up tiles, mats &amp; racks 💕</div><img class="omm" src="{img('omm.png')}" alt="Oh My Mahjong certified instructor"></div>
<div class="code"><div><small>Partner brand discount</small><b>MAHJMATCH</b></div><button type="button" onclick="(navigator.clipboard?navigator.clipboard.writeText('MAHJMATCH'):Promise.reject()).then(()=>{{this.textContent='Copied ✓'}}).catch(()=>{{this.textContent='MAHJMATCH'}})">Copy code</button></div>
<a class="where" href="{S}/mahjong-discount-codes"{tgt(S)}>See all our partner brands ›</a>
<a class="feat" href="{S}/holiday-mahjong-matches"{tgt(S)}><div class="hol">{hol}</div><div><b>Holiday Matches 🎄<small>Christmas tiles, mats &amp; racks, matched</small></b><span style="font-size:26px">›</span></div></a>
<h2>Find your tiles&rsquo; match</h2>
<!-- newest live albums first (see pop.json / build script comment) -->
<div class="row">{strip}</div>
<a class="all" href="{S}/mahjong-tile-matches"{tgt(S)}>See all tile albums ›</a>
<h2>Shop by tile color</h2>
<div class="chips">{chips}</div>
<h2>More from Mahj Matchmaker</h2>
{btn('💬','Join our Facebook group','Matches, new drops &amp; table photos','https://www.facebook.com/groups/mahjmatchmaker')}
{btn('🀄','Book a private mahjong lesson','Learn with an OMM certified instructor',S+'/private-mahjong-lessons')}
{btn('💌','Request an album','Tell me which tiles to match next',S+'/request-an-album')}
{btn('📸','Share your table','Send me your tiles + mat combo',S+'/share-your-table')}
{btn('🎁','Christmas mahjong sets guide','Holiday tiles, mats &amp; racks for 2026',S+'/blog/christmas-mahjong-sets')}
{btn('📖','Mahjong buying guide','What to buy first, and why',S+'/blog/mahjong-buying-guide')}
{btn('📅','Events &amp; rentals','Mahjong parties, events and table rentals',S+'/events')}
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
