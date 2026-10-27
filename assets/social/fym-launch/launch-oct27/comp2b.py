import os
from PIL import Image
exec(open('comp.py').read().split('mode=sys.argv[1]')[0])
for o in []:
    Image.open(o+'_cardonly.png').convert('RGB').resize((1080,1350),Image.LANCZOS).save(f'card-{o}.jpg',quality=92)
def story_card(o,top_html):
    return f'<div class="c" style="top:230px">{top_html}</div><img src="file://{D}/card-{o}.jpg" style="position:absolute;left:40px;top:480px;width:1000px;border-radius:24px;box-shadow:0 20px 50px rgba(6,42,85,.14)">'
P={}
P['bb-2-phone']=(1350,f'<div class="c" style="top:80px">{pill("FALL FAVORITE")}<div style="font:400 78px/1.05 Cap;margin-top:24px">Start with<br>Brownstone Bloom</div><div style="font:italic 400 36px PF;color:#4a3d58;margin-top:16px">Pick the tiles, swipe your mat, add racks.</div></div>'+phone('bb_swipe.png',400,340,560))
S={}
S['bb-1']=story_card('bb',f'<div style="font:400 72px/1.05 Cap">Start with<br>Brownstone Bloom</div><div style="font:italic 400 34px PF;color:#4a3d58;margin-top:14px">in {FYM(34)}</div>')
S['bb-2']=f'<div class="c" style="top:230px"><div style="font:400 72px/1.05 Cap">Swipe your mat</div><div style="font:italic 400 34px PF;color:#4a3d58;margin-top:14px">Anders Ruff Brownstone Bloom tiles</div></div>'+phone('bb_swipe.png',520,280,450)
for o,t in [('mal1','Miss Classic Malachite'),('jad1','Miss Classic Jade')]:
    S[o]=story_card(o,f'<div style="font:700 26px Bit;letter-spacing:5px;color:#d6247f">BACK IN STOCK</div><div style="font:400 66px/1.05 Cap;margin-top:16px">{t}</div><div style="font:italic 400 34px PF;color:#4a3d58;margin-top:12px">Find her mat in {FYM(34)}</div>')
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1350})
    for k,(H,body) in []:
        pg.set_viewport_size({'width':1080,'height':H})
        open('_p.html','w').write(f'<html><head><meta charset=utf8><style>{CSS}body{{width:1080px;height:{H}px}}</style></head><body>{body}</body></html>'); pg.goto('file://'+D+'/_p.html'); pg.wait_for_timeout(900); pg.screenshot(path=f'post-{k}.jpg',type='jpeg',quality=92)
    pg.set_viewport_size({'width':1080,'height':1920})
    for k,body in [(k,v) for k,v in S.items() if k in ('mal1','jad1')]:
        open('_s.html','w').write(f'<html><head><meta charset=utf8><style>{CSS}body{{width:1080px;height:1920px}}</style></head><body>{body}</body></html>'); pg.goto('file://'+D+'/_s.html'); pg.wait_for_timeout(900); pg.screenshot(path=f'story-instock-{k}.jpg',type='jpeg',quality=92)
    b.close()
