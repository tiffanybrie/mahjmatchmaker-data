import os,json,sys
M='/tmp/claude-0/-home-claude/f4da3022-6ec8-595a-90aa-668aea191899/scratchpad/mock/'
src=open(M+'mk.py').read().split('with sync_playwright')[0]
os.chdir(M); exec(src); os.chdir(os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
from PIL import Image
import base64,io
def du(fn,s=600):
    im=Image.open(fn).convert('RGB'); im.thumbnail((s,s)); b=io.BytesIO(); im.save(b,'JPEG',quality=88); return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
JOBS2={'lbb':("Let's Be Besties",[20,19,12,17,23,29,33,37,4,3,6,5],[20,19,12,17,23,29,33,37,4]),
 'mr':('Mahjong Register',[25,7,9,15,16,17,23,24,27,8,26,28],[25,7,9,15,16,17,23,24,27]),
 'sad':('Soirée All Day',[0,1,2,3,4,5,6,7,8],[0,1,2,3,4,5,6,7,8]),
 'mv':('Mahj & Vine',[0,2,5,6,7,12,13,14,15],[0,2,5,6,7,12,13,14,15]),
 'fam':('Fait à Main',[2,0,1,3,5,6],[2,0,1,3,5,6])}
JOBS0={'bm':('Britt Mills',[10,0,6,8,9,1,12,33,40,16,19,29],[10,0,6,8,9,1,12,33,40]),
      'at':('Amanda Toppe',list(range(9)),list(range(9)))}
def html(W,H,brand,files,cols,hy,gy,cell,gap,by,line):
    tiles=''.join(f'<img src="{du(f)}" style="width:{cell}px;height:{cell}px;object-fit:cover;border-radius:18px;box-shadow:0 14px 30px rgba(6,42,85,.16),0 3px 8px rgba(6,42,85,.08)">' for f in files)
    gw=cols*cell+(cols-1)*gap
    return f'''<html><head><meta charset=utf8><style>{CSS}body{{margin:0;width:{W}px;height:{H}px;background:#fff;position:relative}}</style></head><body>
<div style="position:absolute;left:0;right:0;top:{hy}px;text-align:center">
<div style="font:400 100px/1 Cap;color:#062a55">Find <span style="font:italic 400 104px PF">Your</span> Mat-ch<sup style="font-size:36px">™</sup></div>
<div style="font:italic 46px PF;color:#c8325f;margin-top:26px">now featuring</div>
<div style="font:400 64px/1.1 Cap;color:#062a55;margin-top:6px">{brand}</div></div>
<div style="position:absolute;top:{gy}px;left:{(W-gw)//2}px;width:{gw}px;display:grid;grid-template-columns:repeat({cols},{cell}px);gap:{gap}px">{tiles}</div>
<div style="position:absolute;left:0;right:0;top:{by}px;text-align:center;font:700 34px Bit;color:#062a55;letter-spacing:1px">{line}</div>
<div style="position:absolute;left:0;right:0;top:{by+56}px;text-align:center;font:700 40px Bit;color:#c8325f">mahjmatchmaker.com</div>
</body></html>'''
JOBS=JOBS2 if len(sys.argv)>1 else JOBS0
if len(sys.argv)>2: JOBS={k:v for k,v in JOBS.items() if k in sys.argv[2].split(',')}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page()
    for tag,(brand,st,po) in JOBS.items():
        L=json.load(open(tag+'.json')); fs=[L[i][0] for i in st]; fp=[L[i][0] for i in po]
        line=(f'{brand} mats, ready to swipe' if tag in ('lbb',) else f'Every {brand} mat, ready to swipe')
        n=len(fs); rows=(n+2)//3
        cell=252 if rows==4 else 300; gap=24
        gh=rows*cell+(rows-1)*gap; gy=590+(1660-590-gh)//2
        pr=(len(fp)+2)//3; pgy=345+(1170-345-(pr*246+(pr-1)*22))//2
        for nm,(W,H,files,cols,cl,gp,gyy,by) in {'story':(1080,1920,fs,3,cell,gap,gy,1700),'post':(1080,1350,fp,3,246,22,pgy,1190)}.items():
            open('e.html','w').write(html(W,H,brand,files,cols,50 if nm=='post' else 230,gyy,cl,gp,by,line))
            pg.set_viewport_size({'width':W,'height':H}); pg.goto('file://'+os.path.abspath('e.html')); pg.wait_for_timeout(900); pg.screenshot(path=f'eye-{tag}-{nm}.png')
    b.close()
