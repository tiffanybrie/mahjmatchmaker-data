import os,sys
sys.argv=['x']; exec(open('mk.py').read().split('with sync_playwright')[0])
from playwright.sync_api import sync_playwright
W,H=1000,1020
h=f'<html><head><meta charset=utf8><style>{CSS}body{{width:{W}px;height:{H}px;background:transparent}}</style></head><body>'+phone('s_home.png',400,*PINK,60,90,0,1)+phone('s_swipe.png',450,*PINK,480,20,0,2)+'</body></html>'
open('duo.html','w').write(h)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':W,'height':H},device_scale_factor=2)
    pg.goto('file://'+os.path.abspath('duo.html')); pg.wait_for_timeout(800); pg.screenshot(path='fym-phones-blush-duo.png',omit_background=True); b.close()
