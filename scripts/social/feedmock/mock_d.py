"""Option D (Oct 19): 3 grid posts per tile set, one row each: album cover | dating profile | best match."""
import asyncio, json
R='/home/claude/mahjmatchmaker-data'; u=lambda p:f'file://{R}/{p}'
CC=json.load(open(R+'/config/colorcards.json'))['sets']
F=f'file://{R}/scripts/social/tileprofile/fonts'; G='file:///usr/share/fonts/truetype/google-fonts'
sets=[('papaya-spritz','assets/covers/albums/w800/00-papaya-spritz-mahjong-tiles-cover.jpg','assets/colorcards/papaya-spritz/00-papaya-spritz-mahjong-tiles-profile-c-story.jpg','assets/colorcards/papaya-spritz/mats/heiress-britt-mills.jpg','Heiress'),
      ('shangri-la','assets/covers/albums/w800/00-shangri-la-mahjong-tiles-cover.jpg','assets/colorcards/shangri-la/00-shangri-la-mahjong-tiles-color-guide-mobile.jpg','assets/colorcards/shangri-la/mats/camellia-oh-my-mahjong.jpg','Camellia'),
      ('lilac-soiree','assets/covers/albums/w800/00-lilac-soiree-mahjong-tiles-cover.jpg','assets/colorcards/lilac-soiree/00-lilac-soiree-mahjong-tiles-color-guide-mobile.jpg','assets/colorcards/lilac-soiree/mats/chantilly-oh-my-mahjong.jpg','Chantilly')]
today=['24-lagoon','22-drake','14-tortoise','10-amara','06-emerald','11-heritage']
HEART='<svg viewBox="0 0 48 48" width="40" height="40"><path d="M24 40 C10 30 6 23 6 17 C6 11 11 7 16 7 C20 7 22 9 24 12 C26 9 28 7 32 7 C37 7 42 11 42 17 C42 23 38 30 24 40 Z" fill="#f56c8c"/></svg>'
def match(key,mat,mname):
    c=CC[key]; col=c['col']; name=c['name']
    return f'''<div class="c" style="background:{col}22;display:flex;flex-direction:column;align-items:center;justify-content:center;background-image:none">
      <div style="font-family:Hand;font-size:30px;color:#d6336c">It&rsquo;s a match!</div>
      <div style="display:flex;align-items:center;margin:10px 0">
        <div style="width:66px;height:66px;border-radius:50%;background:url({u('assets/tiles/album/'+key+'.jpg')}) center/cover;box-shadow:0 0 0 4px #fff"></div>
        <div style="margin:0 -8px;z-index:2;background:#fff;border-radius:50%;width:34px;height:34px;display:flex;align-items:center;justify-content:center">{HEART.replace('40','24')}</div>
        <div style="width:66px;height:66px;border-radius:12px;background:url({u(mat)}) center/cover;box-shadow:0 0 0 4px #fff"></div></div>
      <div style="font:700 13px Lo;color:#062a55;text-align:center;line-height:1.2">{name}<br><span style="color:{col}">&hearts;</span> {mname}</div>
      <img src="{u('assets/brand/mahjmatchmaker-wordmark-notag.png')}" style="width:70px;margin-top:8px"></div>'''
cells=''
for key,cov,prof,mat,mn in sets:
    cells+=f'<div class="c" style="background-image:url({u(cov)})"><i>cover</i></div>'
    cells+=f'<div class="c" style="background-image:url({u(prof)});background-position:center 30%"><i>profile</i></div>'
    cells+=match(key,mat,mn).replace('<div class="c"','<div class="c"',1)
for t in today: cells+=f'<div class="c" style="background-image:url({u("assets/covers/albums/w800/"+t+"-mahjong-tiles-cover.jpg")})"></div>'
html=f"""<!doctype html><html><head><meta charset=utf8><style>
@font-face{{font-family:Hand;src:url('{F}/Caveat-Bold.ttf')}}
@font-face{{font-family:Lo;src:url('{G}/Lora-Variable.ttf')}}
body{{margin:0;background:#f6e9df;font-family:Helvetica,Arial;padding:40px;display:flex;gap:40px;align-items:flex-start}}
.ph{{width:520px;background:#fff;border-radius:40px;padding:26px 18px;box-shadow:0 20px 50px rgba(0,0,0,.15)}}
.t{{font:700 30px Georgia;color:#062a55;text-align:center}} .s{{font-size:17px;color:#5a6b85;text-align:center;margin:8px 10px 16px}}
.hd{{display:flex;align-items:center;gap:12px;margin:0 6px 12px}} .hd img{{width:54px;height:54px;border-radius:50%}} .hd b{{font-size:18px}}
.g{{display:grid;grid-template-columns:repeat(3,1fr);gap:3px}}
.c{{aspect-ratio:3/4;background-size:cover;background-position:center;position:relative}}
.c i{{position:absolute;top:6px;left:6px;font:700 11px Helvetica;font-style:normal;background:#062a55;color:#fff;padding:2px 6px;border-radius:8px}}
.k{{width:420px;font-size:19px;color:#062a55;line-height:1.5}} .k b{{color:#d6336c}}
</style></head><body>
<div class="ph"><div class="t">D &middot; One row per tile set</div><div class="s">Every launch = 3 grid posts: album cover &middot; her profile &middot; her best match. Rows stay lined up because each set always adds exactly 3.</div>
<div class="hd"><img src="{u('assets/brand/fb-page/mahj-matchmaker-page-profile-1080.jpg')}"><b>mahjmatchmaker</b></div><div class="g">{cells}</div></div>
<div class="k"><p><b>Posting order per set</b> (Instagram shows newest first, top-left):<br>1. Best match &rarr; 2. Profile &rarr; 3. Album cover (posted last, so it lands left).</p>
<p><b>What&rsquo;s underneath can be anything.</b> The hotline reel, a carousel or a mood board, with these three as their grid covers.</p>
<p><b>Your existing 6</b> (bottom two rows) stay as they are. New rows sit on top in sets of 3, so the old covers just become the &ldquo;archive&rdquo; rows.</p>
<p><b>Extra posts</b> beyond 3 per set (teasers, second promos) go to Reels/Stories, hidden from the grid, so rows never shift.</p></div>
</body></html>"""
open(R+'/scripts/social/feedmock/mock_d.html','w').write(html)
async def go():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1100,'height':1200})
        await pg.goto('file://'+R+'/scripts/social/feedmock/mock_d.html'); await pg.wait_for_timeout(2500)
        await pg.screenshot(path=R+'/assets/social/feed-mockup-D-row-per-set.png',full_page=True); await b.close()
asyncio.run(go())
