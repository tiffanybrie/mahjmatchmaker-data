import os,sys
M='/tmp/claude-0/-home-claude/f4da3022-6ec8-595a-90aa-668aea191899/scratchpad/mock/'
src=open(M+'mk.py').read().split('with sync_playwright')[0].replace("D=os.path.abspath('.')","D=os.path.abspath('.')")
exec(src)
from playwright.sync_api import sync_playwright
WHITE=('#f7f7f5','#d6d6d3','#e2e2df'); SH='0 28px 60px rgba(6,42,85,.16), 0 4px 12px rgba(6,42,85,.08)'
OUT,BRAND=sys.argv[1],sys.argv[2]
LINE=sys.argv[3] if len(sys.argv)>3 else 'Build your perfect '+BRAND+' set'
def page(W,H,top,pw,cw):
    y=top; ph=phone('s_home.png',pw,*WHITE,(W-2*pw-cw)//2+0,y+70,0,1,SH)+phone(OUT+'_card.png',pw,*WHITE,W-(W-2*pw-cw)//2-pw,y+70,0,1,SH)+phone(OUT+'_swipe.png',cw,*WHITE,(W-cw)//2,y,0,3,SH)
    # overlap: side phones tucked 60px under centre
    return ph
def html(W,H,top,pw,cw,hy,by):
    left=(W-cw)//2-pw+60; right=(W+cw)//2-60
    ph=phone('s_home.png',pw,*WHITE,left,top+70,0,1,SH)+phone(OUT+'_card.png',pw,*WHITE,right,top+70,0,1,SH)+phone(OUT+'_swipe.png',cw,*WHITE,(W-cw)//2,top,0,3,SH)
    return f'''<html><head><meta charset=utf8><style>{CSS}body{{width:{W}px;height:{H}px;background:#fff}}</style></head><body>
<div style="position:absolute;left:0;right:0;top:{hy}px;text-align:center">
<div style="font:400 100px/1 Cap;color:#062a55">Find <span style="font:italic 400 104px PF">Your</span> Mat-ch<sup style="font-size:36px">™</sup></div>
<div style="font:italic 46px PF;color:#c8325f;margin-top:26px">now featuring</div>
<div style="font:400 64px/1.1 Cap;color:#062a55;margin-top:6px">{BRAND}</div></div>
{ph}
<div style="position:absolute;left:0;right:0;top:{by}px;text-align:center;font:700 34px Bit;color:#062a55;letter-spacing:1px">{LINE}</div>
<div style="position:absolute;left:0;right:0;top:{by+56}px;text-align:center;font:700 40px Bit;color:#c8325f">mahjmatchmaker.com</div>
</body></html>'''
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1920},device_scale_factor=1)
    for nm,(W,H,top,pw,cw,hy,by) in {'story':(1080,1920,600,400,480,230,1690),'post':(1080,1350,350,280,330,50,1170)}.items():
        open('c.html','w').write(html(W,H,top,pw,cw,hy,by)); pg.set_viewport_size({'width':W,'height':H}); pg.goto('file://'+os.path.abspath('c.html')); pg.wait_for_timeout(900); pg.screenshot(path=f'{OUT}-{nm}.png')
    b.close()
