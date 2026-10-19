import os
from playwright.sync_api import sync_playwright
D=os.path.dirname(os.path.abspath(__file__))
with sync_playwright() as p:
    b=p.chromium.launch()
    for n,out in [('home-launch','hero-fan-launch.png'),('home-prelaunch','hero-fan-prelaunch.png')]:
        pg=b.new_page(viewport={'width':1280,'height':900},device_scale_factor=2)
        pg.goto('file://'+os.path.join(D,n+'.html')); pg.wait_for_load_state('networkidle')
        pg.add_style_tag(content='.hero{background:none!important}.hero::before{display:none}.hero .in>div:first-child{visibility:hidden}.hd{display:none}body{background:transparent}')
        pg.wait_for_timeout(300)
        el=pg.query_selector('.fan')
        bb=el.bounding_box()
        pg.screenshot(path=os.path.join(D,'..','assets',out),omit_background=True,clip={'x':bb['x']-60,'y':max(0,bb['y']-40),'width':bb['width']+120,'height':bb['height']+70})
    b.close()
