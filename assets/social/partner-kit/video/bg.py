import sys,os
from playwright.sync_api import sync_playwright
R='/home/claude/mahjmatchmaker-data'; F='file://'+R+'/scripts/social/tileprofile/fonts/'
brand,logo,out=sys.argv[1:4]
# phone screen box: x=232..848 (616w), y=372..(372+616*844/390=1333)=1705
H=f'''<!doctype html><html><head><meta charset=utf-8><style>
@font-face{{font-family:Cap;src:url({F}Caprasimo.ttf)}}@font-face{{font-family:Bit;src:url({F}bitter-latin-700-normal.woff2);font-weight:700}}
@font-face{{font-family:PF;src:url({F}playfair-display-latin-400-italic.woff2);font-style:italic}}
*{{margin:0;box-sizing:border-box}}body{{width:1080px;height:1920px;background:#faf3ea;position:relative;overflow:hidden}}
.c{{position:absolute;left:0;right:0;text-align:center}}
.t{{font:400 78px/1 Cap;color:#062a55}}.s{{font:italic 40px/1.25 PF;color:#c8325f}}
.pill{{display:inline-block;background:#062a55;color:#fff;font:700 28px Bit;letter-spacing:6px;padding:11px 30px;border-radius:50px}}
.ph{{position:absolute;left:214px;top:354px;width:652px;height:1369px;border-radius:66px;background:#151a22;box-shadow:0 30px 70px rgba(6,42,85,.3)}}
.foot{{position:absolute;left:0;right:0;top:1790px;text-align:center;font:700 36px Bit;color:#062a55}}
</style></head><body>
<div class="c" style="top:60px"><span class="pill">NOW IN</span></div>
<div class="c t" style="top:128px">Find Your Mat-ch&trade;</div>
<div class="c s" style="top:225px">Swipe {brand}<br>tiles, mats &amp; racks into one look</div>
<div class="ph"></div>
<div class="foot">mahjmatchmaker.com/find-your-match</div></body></html>'''
open('bg.html','w').write(H)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1920}); pg.goto('file://'+os.path.abspath('bg.html')); pg.wait_for_timeout(900); pg.screenshot(path=out); b.close()
