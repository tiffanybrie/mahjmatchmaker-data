import sys,json,os
from playwright.sync_api import sync_playwright
F='file:///home/claude/mahjmatchmaker-data/scripts/social/tileprofile/fonts/'
brand=sys.argv[1]; labels=json.loads(sys.argv[2])
CSS=f'''@font-face{{font-family:Cap;src:url({F}Caprasimo.ttf)}}@font-face{{font-family:Bit;src:url({F}bitter-latin-700-normal.woff2);font-weight:700}}
@font-face{{font-family:PF;src:url({F}playfair-display-latin-400-italic.woff2);font-style:italic}}*{{margin:0;box-sizing:border-box}}html,body{{background:transparent}}'''
def shot(pg,html,out,w=1080,h=1920,transparent=True):
    open('_o.html','w').write('<!doctype html><html><head><meta charset=utf-8><style>'+CSS+'</style></head><body style="width:%dpx;height:%dpx;position:relative;overflow:hidden">'%(w,h)+html+'</body></html>')
    pg.set_viewport_size({'width':w,'height':h}); pg.goto('file://'+os.path.abspath('_o.html')); pg.wait_for_timeout(700); pg.screenshot(path=out,omit_background=transparent)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page()
    for i,l in enumerate(labels):
        n,t=l.split(' · ',1)
        shot(pg,f'<div style="position:absolute;left:0;right:0;top:70px;text-align:center"><span style="display:inline-flex;align-items:center;gap:18px;background:rgba(255,255,255,.96);border-radius:60px;padding:14px 34px 14px 16px;box-shadow:0 10px 30px rgba(6,42,85,.22)"><span style="width:62px;height:62px;border-radius:50%;background:#c8325f;color:#fff;font:400 38px/62px Cap;text-align:center">{n}</span><span style="font:400 46px Cap;color:#062a55">{t}</span></span></div>',f'lab{i}.png',1080,260)
    shot(pg,f'''<div style="position:absolute;inset:0;background:#faf3ea"></div>
<div style="position:absolute;left:0;right:0;top:700px;text-align:center"><span style="display:inline-block;background:#062a55;color:#fff;font:700 32px Bit;letter-spacing:7px;padding:13px 34px;border-radius:50px">HOW IT WORKS</span></div>
<div style="position:absolute;left:0;right:0;top:790px;text-align:center;font:400 104px/1.05 Cap;color:#062a55">Find Your<br>Mat-ch&trade;</div>
<div style="position:absolute;left:0;right:0;top:1030px;text-align:center;font:italic 50px/1.3 PF;color:#c8325f">with {brand}</div>''','intro.png',transparent=False)
    shot(pg,'''<div style="position:absolute;left:0;right:0;top:1700px;text-align:center"><div style="font:400 56px Cap;color:#062a55">Swipe your own match</div><div style="font:700 36px Bit;color:#c8325f;margin-top:14px">mahjmatchmaker.com/find-your-match</div></div>''','outro.png')
    b.close()
os.remove('_o.html')
