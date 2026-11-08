"""'Her best features' favorite-tiles graphic (1080x1350), Coquette layout (Tiffany, Oct 19 11pm):
clean tile cutouts (no white frames), grouped sections with spaced caps headings + one italic caption each:
row of 4 / hero single + 2x2. Cutouts: assets/tiles/faces/<set>/clean/ (cut from the brand's flat lay).
Usage: python3 scripts/colorwheel/favorites.py"""
import asyncio
R='/home/claude/mahjmatchmaker-data'; u=lambda p:f'file://{R}/{p}'
F=f'file://{R}/scripts/social/tileprofile/fonts'; G='file:///usr/share/fonts/truetype/google-fonts'
T='assets/tiles/faces/papaya-spritz/clean/'
SET=dict(title='Her best features', shop='Shop Papaya at Oh My Mahjong',
  top=('The dancing dragons', ['dragon-coral','dragon-green'], 'My favorite dragons, and they come as a pair'),
  singles=[('The crane','crane','Her gray-crowned<br>crane bird bam'), ('Ginger Lola','lola-ginger','The redheaded<br>matriarch'), ('The parasols','dot3','Little umbrellas')])
# Nov 6: python3 favorites.py <key> -> reads config/profiles/<key>.json best_features (+ 'shop'); papaya (no arg) unchanged.
# A best_features block with a _status containing 'PROPOSAL' renders a visible DRAFT ribbon and writes ...-favorite-tiles-DRAFT.jpg.
import sys, json
KEY = sys.argv[1] if len(sys.argv) > 1 else 'papaya-spritz'
DRAFT = ''
OUTF = R+'/assets/social/papaya-spritz-launch/papaya-spritz-favorite-tiles.jpg'; HTMLF = R+'/scripts/colorwheel/favorites.html'
if KEY != 'papaya-spritz':
    _p = json.load(open(f'{R}/config/profiles/{KEY}.json')); _b = _p['best_features']
    T = _p.get('faces_dir', f'assets/tiles/faces/{KEY}/clean/')  # Nov 7: Deco colourways share one face set
    SET = dict(title='Her best features', shop=_b.get('shop', f"Shop {_p['name']} at {_p['brand']}"), top=tuple(_b['top']), singles=[tuple(x) for x in _b['singles']])
    isdraft = 'PROPOSAL' in _b.get('_status', '')
    DRAFT = ('<div style="position:absolute;bottom:128px;left:50%;transform:translateX(-50%);white-space:nowrap;background:#1f3a6b;color:#fff;font:700 20px Pop;letter-spacing:.14em;'
             'padding:10px 18px;border-radius:999px">DRAFT · CLAUDE\'S PICKS</div>') if isdraft else ''
    import os as _os; _os.makedirs(f'{R}/assets/social/{KEY}-launch', exist_ok=True)
    OUTF = f'{R}/assets/social/{KEY}-launch/{KEY}-favorite-tiles' + ('-DRAFT' if isdraft else '') + '.jpg'; HTMLF = f'{R}/scripts/colorwheel/favorites-{KEY}.html'
# Tiffany Oct 19 11:20pm: keep HER picks; clean edges, no white boxes, NO shadows; dragons big at the top
tile=lambda k,w: f'<img src="{u(T+k+".png")}" style="width:{w}px;display:block">'
h=lambda t: f'<div style="font:700 27px Pop;letter-spacing:.24em;text-transform:uppercase;color:#1f3a6b;text-align:center;white-space:nowrap">{t}</div>'
cap=lambda t: f'<div style="font:italic 400 29px/1.25 PF;color:#2c3e63;text-align:center;white-space:nowrap">{t}</div>'
tp=SET['top']
singles=''.join(f'<div style="display:flex;flex-direction:column;align-items:center;width:300px">{h(n)}<div style="margin-top:20px">{tile(k,232)}</div><div style="margin-top:18px">{cap(c)}</div></div>' for n,k,c in SET['singles'])
html=f"""<!doctype html><html><head><meta charset=utf8><style>
@font-face{{font-family:Capra;src:url('{F}/Caprasimo.ttf')}}
@font-face{{font-family:Pop;font-weight:700;src:url('{G}/Poppins-Bold.ttf')}}
@font-face{{font-family:PF;font-style:italic;src:url('{F}/playfair-display-latin-400-italic.woff2')}}
*{{margin:0;padding:0;box-sizing:border-box}} body{{width:1080px;height:1350px;overflow:hidden}}
.big{{font-family:Capra;text-transform:uppercase;text-align:center;-webkit-text-stroke:14px #fff;paint-order:stroke fill;letter-spacing:.01em;line-height:1}}
</style></head><body>
<div style="position:relative;width:1080px;height:1350px;background:#f6e3d3;overflow:hidden">
{DRAFT}<div class="big" style="position:absolute;top:44px;left:0;right:0;font-size:82px;color:#e06a8e">{SET['title']}</div>
<div style="position:absolute;top:166px;left:0;right:0">{h(tp[0])}
 <div style="display:flex;justify-content:center;gap:44px;margin-top:22px">{''.join(tile(k,244) for k in tp[1])}</div>
 <div style="margin-top:20px">{cap(tp[2])}</div></div>
<div style="position:absolute;top:688px;left:30px;right:30px;display:flex;justify-content:space-between">{singles}</div>
<div class="big" style="position:absolute;bottom:46px;left:0;right:0;font-size:48px;color:#1f3a6b;-webkit-text-stroke:10px #fff">{SET['shop']}</div>
</div></body></html>"""
open(HTMLF,'w').write(html)
async def go():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1080,'height':1350},device_scale_factor=2)
        await pg.goto('file://'+HTMLF); await pg.wait_for_timeout(1500)
        await pg.screenshot(path=f'/tmp/fav2x-{KEY}.png'); await b.close()
    from PIL import Image
    Image.open(f'/tmp/fav2x-{KEY}.png').convert('RGB').resize((1080,1350),Image.LANCZOS).save(OUTF,quality=93); print(OUTF)
asyncio.run(go())
