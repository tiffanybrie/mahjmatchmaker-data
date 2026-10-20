"""One story frame per missing highlight (1080x1920), bg = that highlight's style-C cover color.
Tiffany posts each with 'share to highlights only' and sets the style-C cover."""
import asyncio, glob, shutil
R='/home/claude/mahjmatchmaker-data'; u=lambda p:f'file://{R}/{p}'
F=f'file://{R}/scripts/social/tileprofile/fonts'
S='/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/'
O=R+'/assets/social/highlights/stories/'
head=f"""<!doctype html><html><head><meta charset=utf8><style>
@font-face{{font-family:Capra;src:url('{F}/Caprasimo.ttf')}}
@font-face{{font-family:PF;font-style:italic;src:url('{F}/playfair-display-latin-400-italic.woff2')}}
@font-face{{font-family:Bit;font-weight:600;src:url('{F}/bitter-latin-600-normal.woff2')}}
*{{margin:0;padding:0;box-sizing:border-box}} body{{width:1080px;height:1920px;overflow:hidden}}
.k{{font:600 26px Bit;letter-spacing:.28em;text-transform:uppercase;color:#c8325f;text-align:center}}
.h{{font:400 96px/1 Capra;color:#054689;text-align:center}}
.p{{font:italic 400 40px/1.3 PF;color:#3c4f73;text-align:center}}
.pill{{display:inline-block;background:#054689;color:#fff;font:600 34px Bit;padding:20px 44px;border-radius:60px}}
.img{{border-radius:28px;box-shadow:0 18px 44px rgba(40,30,60,.18)}}
</style></head><body>"""
wm=f"<img src='{u('assets/brand/mahjmatchmaker-wordmark-notag.png')}' style='position:absolute;left:50%;transform:translateX(-50%);bottom:110px;width:330px'>"
def page(bg,inner): return head+f"<div style='position:relative;width:1080px;height:1920px;background:rgb{bg}'>{inner}{wm}</div></body></html>"
covers=sorted(glob.glob(S+'grid-post/[0-9]*.jpg'))
pick=[covers[i] for i in (0,3,8,12,17,21,27,31,36)]
grid=''.join(f"<div style='background:url(file://{c}) center/cover;aspect-ratio:4/5;border-radius:14px'></div>" for c in pick)
P={
'06-codes':((220,220,246),f"""<div style='position:absolute;top:150px;left:0;right:0' class='k'>Save at all 35 partner brands</div>
<div class='h' style='position:absolute;top:210px;left:0;right:0'>Code<br>MAHJMATCH</div>
<img class='img' src="{u('assets/brand/Partner Brands Oct 17 2026.jpg')}" style='position:absolute;left:90px;top:470px;width:900px'>
<div class='p' style='position:absolute;top:1640px;left:60px;right:60px'>Every brand + discount is on the<br>Discount Codes page · link in bio</div>"""),
'01-find-your-match':((249,211,220),f"""<div class='k' style='position:absolute;top:200px;left:0;right:0'>Launching Tuesday, Oct 27</div>
<div class='h' style='position:absolute;top:270px;left:0;right:0;font-size:120px'>Find your<br>Mat-ch</div>
<img class='img' src="{u('assets/social/pinned/find-your-match-3-right.jpg')}" style='position:absolute;left:190px;top:580px;width:700px'>
<div class='p' style='position:absolute;top:1490px;left:70px;right:70px'>Start with your tiles or your mat.<br>Swipe. Heart the ones you love.</div>"""),
'02-new-tiles':((252,220,198),f"""<div class='k' style='position:absolute;top:170px;left:0;right:0'>New tiles · Oh My Mahjong</div>
<div class='h' style='position:absolute;top:230px;left:0;right:0'>Papaya Spritz</div>
<img class='img' src="file://{S}pap/A-in-card-1.jpg" style='position:absolute;left:150px;top:400px;width:780px'>
<div style='position:absolute;top:1430px;left:0;right:0;text-align:center'><span class='pill'>Wed 10/21 · 10am Central</span></div>
<div class='p' style='position:absolute;top:1560px;left:60px;right:60px'>All 50 of her matches are in her album</div>"""),
'03-albums':((251,239,194),f"""<div class='k' style='position:absolute;top:170px;left:0;right:0'>Every tile set has its own album</div>
<div class='h' style='position:absolute;top:230px;left:0;right:0'>The Albums</div>
<div style='position:absolute;left:110px;right:110px;top:400px;display:grid;grid-template-columns:repeat(3,1fr);gap:18px'>{grid}</div>
<div class='p' style='position:absolute;top:1520px;left:60px;right:60px'>The mats and racks I'd pair with each set,<br>across brands · link in bio</div>"""),
}
async def go():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1080,'height':1920})
        for k,(bg,inner) in P.items():
            hp=S+f'hl_{k}.html'; open(hp,'w').write(page(bg,inner))
            await pg.goto('file://'+hp); await pg.wait_for_timeout(1200); await pg.screenshot(path=O+f'{k}-story.png')
        await b.close()
asyncio.run(go())
from PIL import Image
for f in glob.glob(O+'*.png'): Image.open(f).convert('RGB').save(f[:-4]+'.jpg',quality=93)
shutil.copy('/root/.claude/uploads/801d31e6-4a74-59be-8637-eb67bfa0e99e/92b30356-image.png',O+'08-about-2-0-story.png')
Image.open(O+'08-about-2-0-story.png').convert('RGB').save(O+'08-about-2-0-story.jpg',quality=93)
shutil.copy(R+'/assets/social/pinned/meet-your-matchmaker-1.jpg',O+'08-about-meet.jpg')
