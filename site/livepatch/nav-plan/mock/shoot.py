import os,sys
from playwright.sync_api import sync_playwright
D=os.path.dirname(os.path.abspath(__file__)); O=os.path.join(D,'..','shots')
jobs=[('home-launch',1280,True),('home-launch',390,True),('home-prelaunch',1280,True),('home-prelaunch',390,True),
('shop',1280,True),('shop',390,True),('header-matches',1280,True),('header-community',1280,True),
('menu-top',390,False),('menu-matches',390,False),('menu-community',390,False),('footer',1280,True),('footer',390,True)]
only=sys.argv[1:]
with sync_playwright() as p:
    b=p.chromium.launch()
    for n,w,full in jobs:
        if only and n not in only: continue
        pg=b.new_page(viewport={'width':w,'height':844 if w==390 else 900},device_scale_factor=2 if w==390 else 1)
        pg.goto('file://'+os.path.join(D,n+'.html')); pg.wait_for_load_state('networkidle'); pg.wait_for_timeout(600)
        sw=pg.evaluate('document.documentElement.scrollWidth')
        if sw>w: print('OVERFLOW',n,w,sw)
        pg.screenshot(path=os.path.join(O,f'{n}-{w}.png'),full_page=full)
        pg.close()
    b.close()
print('shot')
