import os
from playwright.sync_api import sync_playwright
D=os.path.abspath('.'); F='file:///home/claude/mahjmatchmaker-data/scripts/social/tileprofile/fonts/'
def phone(img,w,frame,ring,btn,x,y,rot=0,z=1,shadow='0 30px 60px rgba(6,42,85,.10), 0 6px 14px rgba(6,42,85,.06)'):
    p=w*0.034; h=w*2.06
    bt=lambda side,top,hh: f'<div style="position:absolute;{side}:-{w*0.012}px;top:{top*h}px;width:{w*0.014}px;height:{hh*h}px;background:{btn};border-radius:3px"></div>'
    return f'''<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);z-index:{z}">
{bt('left',.17,.045)}{bt('left',.25,.08)}{bt('left',.345,.08)}{bt('right',.27,.12)}
<div style="position:absolute;inset:0;border-radius:{w*.17}px;background:{frame};box-shadow:{shadow}, inset 0 0 0 {w*0.006}px {ring};padding:{p}px">
<div style="position:relative;width:100%;height:100%;border-radius:{w*.135}px;overflow:hidden;background:#fff">
<div style="height:{w*.115}px;display:flex;justify-content:space-between;align-items:center;padding:{w*.02}px {w*.085}px 0;font:600 {w*.046}px -apple-system,Helvetica,Arial;color:#111"><span>9:41</span><span style="letter-spacing:2px;font-size:{w*.036}px">▂▄▆ ◔ ▭</span></div>
<div style="position:absolute;left:50%;top:{w*.03}px;transform:translateX(-50%);width:{w*.29}px;height:{w*.085}px;background:#000;border-radius:{w*.05}px"></div>
<img src="file://{D}/{img}" style="width:100%;display:block">
</div></div></div>'''
CSS=f"@font-face{{font-family:Cap;src:url({F}Caprasimo.ttf)}}@font-face{{font-family:PF;src:url({F}playfair-display-latin-400-italic.woff2);font-style:italic}}@font-face{{font-family:Bit;src:url({F}bitter-latin-700-normal.woff2);font-weight:700}}*{{margin:0}}body{{width:1080px;height:1350px;position:relative;overflow:hidden;font-family:Bit}}"
def head(bg,label):
    return f'''<div style="position:absolute;left:0;right:0;top:70px;text-align:center"><div style="display:inline-block;background:#062a55;color:#fff;font:700 26px Bit;letter-spacing:5px;padding:12px 28px;border-radius:40px">LAUNCHING TOMORROW · 10.27</div>
<div style="font:400 92px/1 Cap;color:#062a55;margin-top:30px">Find <span style="font:italic 400 96px PF">Your</span> Mat-ch<sup style="font-size:34px">™</sup></div></div>
<div style="position:absolute;left:24px;bottom:18px;font:700 22px Bit;color:#999">{label}</div>'''
BLACK=('#1c1c1e','#3a3a3c','#2c2c2e'); PINK=('#f3c9d3','#e7a9b8','#e7a9b8'); NAVY=('#0b2f5c','#24497a','#24497a'); CREAMF=('#efe6dc','#d9cbbd','#d9cbbd')
V={
'A-clean-black-duo':('#faf3ea',[('s_home.png',400,*BLACK,105,370,0,1),('s_swipe.png',450,*BLACK,525,300,0,2)]),
'B-trio-like-mahj-closet':('#ffffff',[('s_home.png',360,*BLACK,40,390,0,1),('s_card.png',360,*BLACK,680,390,0,1),('s_swipe.png',420,*BLACK,330,310,0,3)]),
'C-blush-pink-duo':('#fdf3f3',[('s_home.png',400,*PINK,105,370,0,1),('s_swipe.png',450,*PINK,525,300,0,2)]),
'D-navy-duo':('#f9dde6',[('s_home.png',400,*NAVY,105,370,0,1),('s_swipe.png',450,*NAVY,525,300,0,2)]),
}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1350},device_scale_factor=2)
    for k,(bg,ps) in V.items():
        h=f'<html><head><meta charset=utf8><style>{CSS}</style></head><body style="background:{bg}">'+head(bg,k)+''.join(phone(*a) for a in ps)+'</body></html>'
        open(k+'.html','w').write(h); pg.goto('file://'+D+'/'+k+'.html'); pg.wait_for_timeout(700); pg.screenshot(path=k+'.png')
    b.close()
from PIL import Image
ims=[Image.open(k+'.png').resize((540,675)) for k in V]; s=Image.new('RGB',(1080,1350),'white')
for i,im in enumerate(ims): s.paste(im,((i%2)*540,(i//2)*675))
s.save('sheet.jpg',quality=88)
