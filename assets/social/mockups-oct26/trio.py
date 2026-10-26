import os
exec(open('mk.py').read().split('with sync_playwright')[0])
from playwright.sync_api import sync_playwright
W,H=1080,1000
ph=phone('s_home.png',340,*BLACK,30,110,0,1)+phone('s_card3.png',340,*BLACK,710,110,0,1)+phone('s_swipe2.png',400,*BLACK,340,40,0,3)
h=f'<html><head><meta charset=utf8><style>{CSS}body{{width:{W}px;height:{H}px;background:transparent}}</style></head><body>'+ph+'</body></html>'
open('trio.html','w').write(h)
samp=f'<html><head><meta charset=utf8><style>{CSS}</style></head><body style="background:#fff">'+head('#fff','trio-white')+ph.replace('top:110px','top:410px').replace('top:40px','top:340px')+'</body></html>'
open('trio_s.html','w').write(samp)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':W,'height':H},device_scale_factor=2)
    pg.goto('file://'+os.path.abspath('trio.html')); pg.wait_for_timeout(900); pg.screenshot(path='fym-phones-trio-malachite.png',omit_background=True)
    pg.set_viewport_size({'width':1080,'height':1350}); pg.goto('file://'+os.path.abspath('trio_s.html')); pg.wait_for_timeout(900); pg.screenshot(path='trio_sample.png')
    b.close()
