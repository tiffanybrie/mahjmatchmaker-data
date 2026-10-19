import asyncio
R='/home/claude/mahjmatchmaker-data'; u=lambda p:p if p.startswith('file:') else f'file://{R}/{p}'
S='file:///tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/'
M=lambda n:f'assets/social/titlecards/counseling-ep1-papaya/frames/{n}'
items=[
 ('TUE 10/20','10:00 AM ET','GRID #1','Planoly posts it','assets/social/papaya-spritz-launch/grid/papaya-grid-1-its-a-match-heiress.jpg','&ldquo;It&rsquo;s a match!&rdquo; Papaya &hearts; Heiress','Single image. Caption teases: she launches Wed 10am CT, code MAHJMATCH.'),
 ('TUE 10/20','6:00 PM ET','GRID #2','Planoly posts it',S+'profC34.jpg','Her dating profile (carousel)','Swipe-through of 7 slides: her profile, colors, racks, made for each other (Vivienne), OMM sisters, blind dates, see all + code. Grid shows the profile card.'),
 ('TUE 10/20','anytime','STORY','You · 30 sec','assets/social/papaya-spritz-launch/papaya-spritz-introducing-carousel-1.jpg','Reshare OMM&rsquo;s countdown','Tap OMM&rsquo;s countdown sticker &rarr; add to your story, type &ldquo;Code MAHJMATCH &#x1F9E1;&rdquo;.'),
 ('WED 10/21','10:00 AM CT','GRID #3','You post it (song)','assets/covers/albums/w800/00-papaya-spritz-mahjong-tiles-cover.jpg','The hotline reel','Your Edits version with &ldquo;This Will Be.&rdquo; Pick the Papaya album cover as the reel cover, so the grid shows the album cover.'),
 ('WED 10/21','10:00 AM CT','FB GROUP','On your yes','assets/brand/fb-page/mahj-matchmaker-albums-post-1640x856.jpg','Papaya launch post','Already drafted in Ready to Ship, date filled in.'),
 ('WED 10/21','after launch','STORY','You · 30 sec','assets/social/papaya-spritz-launch/papaya-spritz-introducing-carousel-7.jpg','&ldquo;She&rsquo;s live!&rdquo;','A frame I send you + link sticker to her album.'),
]
cards=''.join(f'''<div class="it"><div class="th" style="background-image:url({u(img)})"></div><div class="tx">
<div class="when">{d} &middot; {t}</div><div class="tags"><span class="w {'g' if 'GRID' in w else ('s' if w=='STORY' else 'f')}">{w}</span><span class="who {'me' if 'You' in who else ''}">{who}</span></div>
<div class="tt">{tt}</div><div class="ds">{ds}</div></div></div>''' for d,t,w,who,img,tt,ds in items)
row=''.join(f'<div class="c" style="background-image:url({u(p)})"><i>{n}</i></div>' for n,p in [('#3 Wed',items[3][4]),('#2 Tue',items[1][4]),('#1 Tue',items[0][4])])
old=''.join(f'<div class="c" style="background-image:url({u("assets/covers/albums/w800/"+t+"-mahjong-tiles-cover.jpg")})"></div>' for t in ['24-lagoon','22-drake','14-tortoise'])
html=f"""<!doctype html><html><head><meta charset=utf8><style>
body{{margin:0;background:#f6e9df;font-family:Helvetica,Arial;color:#062a55;padding:40px;width:1500px}}
h1{{font:700 46px Georgia;margin:0}} .sub{{font-size:20px;color:#5a6b85;margin:8px 0 30px}}
.wrap{{display:flex;gap:40px}} .list{{flex:1;display:flex;flex-direction:column;gap:16px}}
.it{{display:flex;gap:20px;background:#fff;border-radius:22px;padding:16px;box-shadow:0 6px 16px rgba(6,42,85,.07)}}
.th{{width:120px;height:160px;border-radius:12px;background-size:cover;background-position:center;flex:none}}
.when{{font:700 16px Helvetica;letter-spacing:.08em;color:#5a6b85}} .tags{{margin:8px 0}}
.w,.who{{display:inline-block;font:700 13px Helvetica;letter-spacing:.08em;padding:4px 10px;border-radius:999px;margin-right:8px}}
.w.g{{background:#062a55;color:#fff}} .w.s{{background:#f7b6c8;color:#72243e}} .w.f{{background:#dbe7f7;color:#0c447c}}
.who{{background:#e9f4e0;color:#27500a}} .who.me{{background:#fde3c8;color:#854f0b}}
.tt{{font:700 24px Georgia}} .ds{{font-size:16px;color:#44506a;margin-top:6px;line-height:1.4}}
.side{{width:420px}} .ph{{background:#fff;border-radius:30px;padding:20px 14px}} .g3{{display:grid;grid-template-columns:repeat(3,1fr);gap:3px}}
.c{{aspect-ratio:3/4;background-size:cover;background-position:center;position:relative}} .c i{{position:absolute;top:6px;left:6px;font:700 11px Helvetica;font-style:normal;background:#f56c8c;color:#fff;padding:2px 6px;border-radius:8px}}
.note{{background:#fff;border-radius:22px;padding:18px 20px;margin-top:20px;font-size:16px;line-height:1.5}}
</style></head><body>
<h1>Papaya Spritz launch plan</h1><div class="sub">Launches Wed Oct 21, 10am CT (11am ET). Three grid posts = one row. Everything else is Stories or the Facebook group.</div>
<div class="wrap"><div class="list">{cards}</div>
<div class="side"><div class="ph"><div style="font:700 18px Helvetica;margin:0 4px 10px">Your grid after Wednesday</div><div class="g3">{row}{old}</div></div>
<div class="note"><b>Your part:</b> Tue, one story reshare (optional). Wed 10am, post the reel with your song + one story. That&rsquo;s it.<br><br><b>Off the grid this week</b> (Reels tab only, so rows stay lined up): the Season 2 trailer and the Pippa/Smith episodes.</div></div></div>
</body></html>"""
open(R+'/scripts/social/feedmock/papaya_plan.html','w').write(html)
async def go():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1580,'height':1000})
        await pg.goto('file://'+R+'/scripts/social/feedmock/papaya_plan.html'); await pg.wait_for_timeout(2000)
        await pg.screenshot(path=R+'/assets/social/papaya-spritz-launch/papaya-launch-plan.png',full_page=True); await b.close()
asyncio.run(go())
