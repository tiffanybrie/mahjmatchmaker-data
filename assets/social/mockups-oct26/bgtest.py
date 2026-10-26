import os
exec(open('mk.py').read().split('with sync_playwright')[0])
from playwright.sync_api import sync_playwright
WHITE=('#f7f7f5','#d6d6d3','#e2e2df')
SH='0 28px 60px rgba(6,42,85,.16), 0 4px 12px rgba(6,42,85,.08)'; NO='0 0 0 rgba(0,0,0,0)'
cases=[('navy-shadow','#062a55',SH),('navy-no-shadow','#062a55',NO),('pink-shadow','#e0547f',SH),('pink-no-shadow','#e0547f',NO)]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1000},device_scale_factor=1)
    for n,bg,sh in cases:
        ph=phone('s_home.png',340,*WHITE,30,110,0,1,sh)+phone('s_card3.png',340,*WHITE,710,110,0,1,sh)+phone('s_swipe2.png',400,*WHITE,340,40,0,3,sh)
        h=f'<html><head><meta charset=utf8><style>{CSS}</style></head><body style="background:{bg};height:1000px">'+ph+f'<div style="position:absolute;left:24px;top:14px;font:700 30px Bit;color:#fff">{n}</div></body></html>'
        open('bg.html','w').write(h); pg.goto('file://'+os.path.abspath('bg.html')); pg.wait_for_timeout(700); pg.screenshot(path=f'bg_{n}.png')
    b.close()
from PIL import Image
s=Image.new('RGB',(1080,1000),'white')
for i,(n,_,_) in enumerate(cases):
    im=Image.open(f'bg_{n}.png').convert('RGB').resize((540,500)); s.paste(im,((i%2)*540,(i//2)*500))
s.save('bg_compare.jpg',quality=88)
