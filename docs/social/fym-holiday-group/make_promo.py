import os,sys
sys.path.insert(0,'/home/claude/mahjmatchmaker-data/assets/social/mockups-oct26')
from playwright.sync_api import sync_playwright
D=os.path.abspath('.'); F='file:///home/claude/mahjmatchmaker-data/scripts/social/tileprofile/fonts/'
def phone(img,w,x,y,rot=0,z=1):
    frame,ring,btn='#ffffff','#e3e3e8','#e8e8ec'; p=w*0.034; h=w*2.06
    bt=lambda side,top,hh: f'<div style="position:absolute;{side}:-{w*0.012}px;top:{top*h}px;width:{w*0.014}px;height:{hh*h}px;background:{btn};border-radius:3px"></div>'
    return f'''<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);z-index:{z}">
{bt('left',.17,.045)}{bt('left',.25,.08)}{bt('left',.345,.08)}{bt('right',.27,.12)}
<div style="position:absolute;inset:0;border-radius:{w*.17}px;background:{frame};box-shadow:0 30px 60px rgba(30,70,120,.22),0 6px 14px rgba(30,70,120,.12), inset 0 0 0 {w*0.006}px {ring};padding:{p}px">
<div style="position:relative;width:100%;height:100%;border-radius:{w*.135}px;overflow:hidden;background:#fff">
<div style="height:{w*.115}px;display:flex;justify-content:space-between;align-items:center;padding:{w*.02}px {w*.085}px 0;font:600 {w*.046}px -apple-system,Helvetica,Arial;color:#111"><span>9:41</span><span style="letter-spacing:2px;font-size:{w*.036}px">▂▄▆ ◔ ▭</span></div>
<div style="position:absolute;left:50%;top:{w*.03}px;transform:translateX(-50%);width:{w*.29}px;height:{w*.085}px;background:#000;border-radius:{w*.05}px"></div>
<img src="file://{D}/{img}" style="width:100%;display:block">
</div></div></div>'''
CSS=f"@font-face{{font-family:Cap;src:url({F}Caprasimo.ttf)}}@font-face{{font-family:PF;src:url({F}playfair-display-latin-600-italic.woff2);font-style:italic}}@font-face{{font-family:Bit;src:url({F}bitter-latin-700-normal.woff2);font-weight:700}}*{{margin:0}}body{{width:1080px;height:1350px;position:relative;overflow:hidden;font-family:Bit;background:radial-gradient(ellipse at 50% 40%,#ffffff 0%,#eef6fc 40%,#d9eaf6 78%,#c6ddef 100%)}}"
import random; random.seed(4)
snow=''.join(f'<i style="position:absolute;left:{random.randint(0,1080)}px;top:{random.randint(0,1350)}px;width:{s}px;height:{s}px;border-radius:50%;background:#fff;box-shadow:0 0 0 1.5px rgba(120,165,205,.5)"></i>' for s in [random.randint(5,13) for _ in range(70)])
head='''<div style="position:absolute;left:0;right:0;top:58px;text-align:center;z-index:5">
<div style="display:inline-block;background:#b3202a;color:#fff;font:700 26px Bit;letter-spacing:5px;padding:12px 28px;border-radius:40px">HOLIDAY EDITION</div>
<div style="font:400 62px/1.05 Cap;color:#062a55;margin-top:22px">Holiday mats &amp; tiles are in</div>
<div style="font:400 92px/1.05 Cap;color:#062a55;margin-top:6px">Find <span style="font:italic 600 96px PF;color:#b3202a">Your</span> Mat-ch<sup style="font-size:34px">™</sup></div></div>
<div style="position:absolute;left:0;right:0;bottom:46px;text-align:center;z-index:5"><span style="display:inline-block;background:#062a55;color:#fff;font:700 34px Bit;padding:18px 36px;border-radius:50px">Pick your tiles · tap Holiday · swipe 140+ holiday mats</span></div>'''
ph=phone('cmm.jpg',330,60,440,-5,1)+phone('fp.jpg',330,690,440,5,1)+phone('card.png',370,355,400,0,3)
h=f'<html><head><meta charset=utf8><style>{CSS}</style></head><body><div style="position:absolute;inset:0">{snow}</div>{head}{ph}</body></html>'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1350},device_scale_factor=2)
    open(D+'/p.html','w').write(h); pg.goto('file://'+D+'/p.html'); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(1200); pg.screenshot(path='/home/claude/mahjmatchmaker-data/docs/social/holiday-albums-group/16-fym-holiday-promo.png'); b.close()
