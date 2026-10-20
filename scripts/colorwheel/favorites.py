"""'Her best features' favorite-tiles graphic (1080x1350), Coquette layout (Tiffany, Oct 19 11pm):
clean tile cutouts (no white frames), grouped sections with spaced caps headings + one italic caption each:
row of 4 / hero single + 2x2. Cutouts: assets/tiles/faces/<set>/clean/ (cut from the brand's flat lay).
Usage: python3 scripts/colorwheel/favorites.py"""
import asyncio
R='/home/claude/mahjmatchmaker-data'; u=lambda p:f'file://{R}/{p}'
F=f'file://{R}/scripts/social/tileprofile/fonts'; G='file:///usr/share/fonts/truetype/google-fonts'
T='assets/tiles/faces/papaya-spritz/clean/'
SET=dict(title='Her best features', shop='Shop Papaya at Oh My Mahjong',
  row=('The parasols & peonies', ['dot3','dot7','peony-coral2','peony-purple1'], 'Little umbrellas and lantern peonies. Obsessed.'),
  hero=('The crane', 'crane', 'A gray-crowned crane bird bam'),
  quad=('The dragons & jokers', ['dragon-coral','lola-ginger','dragon-green','lola-lavender'], 'Dancing dragons and the Lola sisters'))
tile=lambda k,w: f'<img src="{u(T+k+".png")}" style="width:{w}px;display:block;filter:drop-shadow(0 10px 14px rgba(120,60,30,.20)) drop-shadow(0 2px 3px rgba(120,60,30,.12))">'
h=lambda t: f'<div style="font:700 27px Pop;letter-spacing:.24em;text-transform:uppercase;color:#1f3a6b;text-align:center">{t}</div>'
cap=lambda t: f'<div style="font:italic 400 29px PF;color:#2c3e63;text-align:center;white-space:nowrap">{t}</div>'
r,hr,q=SET['row'],SET['hero'],SET['quad']
html=f"""<!doctype html><html><head><meta charset=utf8><style>
@font-face{{font-family:Capra;src:url('{F}/Caprasimo.ttf')}}
@font-face{{font-family:Pop;font-weight:700;src:url('{G}/Poppins-Bold.ttf')}}
@font-face{{font-family:PF;font-style:italic;src:url('{F}/playfair-display-latin-400-italic.woff2')}}
*{{margin:0;padding:0;box-sizing:border-box}} body{{width:1080px;height:1350px;overflow:hidden}}
.big{{font-family:Capra;text-transform:uppercase;text-align:center;-webkit-text-stroke:14px #fff;paint-order:stroke fill;letter-spacing:.01em;line-height:1}}
</style></head><body>
<div style="position:relative;width:1080px;height:1350px;background:#f6e3d3;overflow:hidden">
<div class="big" style="position:absolute;top:44px;left:0;right:0;font-size:82px;color:#e06a8e">{SET['title']}</div>
<div style="position:absolute;top:168px;left:0;right:0">{h(r[0])}
 <div style="display:flex;justify-content:center;gap:26px;margin-top:22px">{''.join(tile(k,200) for k in r[2] and r[1])}</div>
 <div style="margin-top:22px">{cap(r[2])}</div></div>
<div style="position:absolute;top:612px;left:60px;width:440px;display:flex;flex-direction:column;align-items:center">{h(hr[0])}
 <div style="margin-top:24px">{tile(hr[1],282)}</div><div style="margin-top:22px">{cap(hr[2])}</div></div>
<div style="position:absolute;top:612px;right:60px;width:460px;display:flex;flex-direction:column;align-items:center">{h(q[0])}
 <div style="display:grid;grid-template-columns:auto auto;gap:22px 24px;margin-top:24px">{''.join(tile(k,140) for k in q[1])}</div>
 <div style="margin-top:22px">{cap(q[2])}</div></div>
<div class="big" style="position:absolute;bottom:46px;left:0;right:0;font-size:48px;color:#1f3a6b;-webkit-text-stroke:10px #fff">{SET['shop']}</div>
</div></body></html>"""
open(R+'/scripts/colorwheel/favorites.html','w').write(html)
async def go():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1080,'height':1350},device_scale_factor=2)
        await pg.goto('file://'+R+'/scripts/colorwheel/favorites.html'); await pg.wait_for_timeout(1500)
        await pg.screenshot(path='/tmp/fav2x.png'); await b.close()
    from PIL import Image
    Image.open('/tmp/fav2x.png').convert('RGB').resize((1080,1350),Image.LANCZOS).save(R+'/assets/social/papaya-spritz-launch/papaya-spritz-favorite-tiles.jpg',quality=93)
asyncio.run(go())
