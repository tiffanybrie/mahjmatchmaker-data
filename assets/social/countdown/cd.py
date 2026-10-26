import os
from playwright.sync_api import sync_playwright
F='file:///home/claude/mahjmatchmaker-data/scripts/social/tileprofile/fonts/'
PH='file:///home/claude/mahjmatchmaker-data/assets/links/v2/fym-phones-oct26.webp'
H=f'''<html><head><meta charset=utf-8><style>@font-face{{font-family:Cap;src:url({F}Caprasimo.ttf)}}@font-face{{font-family:Bit;src:url({F}bitter-latin-700-normal.woff2);font-weight:700}}@font-face{{font-family:PF;src:url({F}playfair-display-latin-400-italic.woff2);font-style:italic}}@font-face{{font-family:Cav;src:url({F}Caveat-Bold.ttf)}}
*{{margin:0;box-sizing:border-box}}body{{width:1080px;height:1920px;background:linear-gradient(#fbe3ea,#fdf3f3 60%,#fbe3ea);position:relative;overflow:hidden;font-family:Bit}}
.c{{position:absolute;left:0;right:0;text-align:center}}
</style></head><body>
<div class="c" style="top:235px"><span style="background:#062a55;color:#fff;font:700 30px Bit;letter-spacing:7px;padding:13px 34px;border-radius:50px">FIND YOUR MAT-CH&trade; · 10.27</span></div>
<div class="c" style="top:322px;font:italic 64px PF;color:#062a55">Tomorrow,</div>
<div class="c" style="top:405px;font:400 96px/1 Cap;color:#062a55;white-space:nowrap">you become</div><div class="c" style="top:500px;font:400 104px/1 Cap;color:#e0547f;white-space:nowrap">the matchmaker.</div>
<img src="{PH}" style="position:absolute;left:150px;top:630px;width:720px;left:180px">
<div class="c" style="top:1330px;font:400 58px Cav;color:#062a55">get a reminder when it&rsquo;s live &darr;</div>
<div class="c" style="top:1745px;font:700 34px Bit;color:#062a55">mahjmatchmaker.com</div>
</body></html>'''
open('cd.html','w').write(H)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1920}); pg.goto('file://'+os.path.abspath('cd.html')); pg.wait_for_timeout(900); pg.screenshot(path='cd.png'); b.close()
from PIL import Image; Image.open('cd.png').convert('RGB').save('countdown-tomorrow-sticker.jpg',quality=93)
Image.open('cd.png').resize((360,640)).save('cdp.png')
