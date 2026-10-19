"""Instagram grid mockups (Oct 19): A covers only, B covers + rhythm, C mixed."""
import asyncio
R='/home/claude/mahjmatchmaker-data'; u=lambda p:f'file://{R}/{p}'
C=lambda n:f'assets/covers/albums/w800/{n}-mahjong-tiles-cover.jpg'
F='assets/social/titlecards/counseling-ep1-papaya/frames/'
today=[C('24-lagoon'),C('22-drake'),C('14-tortoise'),C('10-amara'),C('06-emerald'),C('11-heritage')]
A=[C('00-coquette'),C('00-smith'),C('00-pippa'),
   C('00-papaya-spritz'),C('00-petalee'),C('00-osler'),
   C('00-seabreeze'),C('00-talulah'),C('00-cypress-forest')]+today
prof='assets/colorcards/papaya-spritz/00-papaya-spritz-mahjong-tiles-profile-c-story.jpg'
mood='assets/moodboards/rackin-rudolph/rackin-rudolph-amazon-1080x1350.jpg'
B=[C('00-coquette'),F+'f01.png',C('00-smith'),
   C('00-pippa'),prof,C('00-papaya-spritz'),
   C('00-osler'),F+'f11.png',C('00-seabreeze')]+today
Cm=[F+'f01.png',C('00-coquette'),F+'f03.png',
    prof,F+'f07.png',mood,
    C('00-smith'),F+'f13.png' if False else F+'f11.png','assets/colorcards/papaya-spritz/00-papaya-spritz-mahjong-tiles-tile-edit-moodboard.jpg']+today
import os
if not os.path.exists(R+'/'+mood):
    import glob; m=glob.glob(R+'/assets/moodboards/rackin-rudolph/*.jpg'); mood=m[0].replace(R+'/','')
    Cm[5]=mood
def grid(title,sub,items,new=9):
    cells=''.join(f'<div class="c" style="background-image:url({u(p)})">{"<i>new</i>" if i<new else ""}</div>' for i,p in enumerate(items))
    return f'<div class="ph"><div class="t">{title}</div><div class="s">{sub}</div><div class="hd"><img src="{u("assets/brand/fb-page/mahj-matchmaker-page-profile-1080.jpg")}"><b>mahjmatchmaker</b></div><div class="g">{cells}</div></div>'
html=f"""<!doctype html><html><head><meta charset=utf8><style>
body{{margin:0;background:#f6e9df;font-family:Helvetica,Arial;display:flex;gap:40px;padding:40px}}
.ph{{width:520px;background:#fff;border-radius:40px;padding:26px 18px;box-shadow:0 20px 50px rgba(0,0,0,.15)}}
.t{{font:700 30px Georgia;color:#062a55;text-align:center}} .s{{font-size:17px;color:#5a6b85;text-align:center;margin:8px 10px 16px;min-height:44px}}
.hd{{display:flex;align-items:center;gap:12px;margin:0 6px 12px}} .hd img{{width:54px;height:54px;border-radius:50%}} .hd b{{font-size:18px}}
.g{{display:grid;grid-template-columns:repeat(3,1fr);gap:3px}}
.c{{aspect-ratio:3/4;background-size:cover;background-position:center;position:relative}}
.c i{{position:absolute;top:6px;left:6px;font:700 11px Helvetica;font-style:normal;background:#f56c8c;color:#fff;padding:2px 6px;border-radius:8px}}
</style></head><body>
{grid('A · Album covers only','Every grid post is a set&rsquo;s album cover. Skits &amp; promos post to Reels/Stories, hidden from the grid.',A)}
{grid('B · Covers + rhythm','Each row: cover · reel cover · cover. Skit covers in the set&rsquo;s colors break it up.',B)}
{grid('C · Everything on the grid','Every piece we make lands on the grid as-is.',Cm)}
</body></html>"""
open(R+'/scripts/social/feedmock/mock.html','w').write(html)
async def go():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1720,'height':1300})
        await pg.goto('file://'+R+'/scripts/social/feedmock/mock.html'); await pg.wait_for_timeout(2500)
        await pg.screenshot(path=R+'/assets/social/feed-mockups-A-B-C.png',full_page=True); await b.close()
asyncio.run(go())
