import os,sys
from playwright.sync_api import sync_playwright
D=os.path.abspath('.'); F='file:///home/claude/mahjmatchmaker-data/scripts/social/tileprofile/fonts/'
WHITE=('#f7f7f5','#d6d6d3','#e2e2df')
SH='0 28px 60px rgba(6,42,85,.16), 0 4px 12px rgba(6,42,85,.08)'
def phone(img,w,x,y,frame='#f7f7f5',ring='#d6d6d3',btn='#e2e2df',shadow=SH):
    p=w*0.034; h=w*2.06
    bt=lambda side,top,hh: f'<div style="position:absolute;{side}:-{w*0.012}px;top:{top*h}px;width:{w*0.014}px;height:{hh*h}px;background:{btn};border-radius:3px"></div>'
    return f'''<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px">{bt('left',.17,.045)}{bt('left',.25,.08)}{bt('left',.345,.08)}{bt('right',.27,.12)}
<div style="position:absolute;inset:0;border-radius:{w*.17}px;background:{frame};box-shadow:{shadow}, inset 0 0 0 {w*0.006}px {ring};padding:{p}px">
<div style="position:relative;width:100%;height:100%;border-radius:{w*.135}px;overflow:hidden;background:#fff">
<div style="height:{w*.115}px;display:flex;justify-content:space-between;align-items:center;padding:{w*.02}px {w*.085}px 0;font:600 {w*.046}px -apple-system,Helvetica,Arial;color:#111"><span>9:41</span><span style="letter-spacing:2px;font-size:{w*.036}px">▂▄▆ ◔ ▭</span></div>
<div style="position:absolute;left:50%;top:{w*.03}px;transform:translateX(-50%);width:{w*.29}px;height:{w*.085}px;background:#000;border-radius:{w*.05}px"></div>
<img src="file://{D}/{img}" style="width:100%;display:block"></div></div></div>'''
CSS=f"@font-face{{font-family:Cap;src:url({F}Caprasimo.ttf)}}@font-face{{font-family:PF;src:url({F}playfair-display-latin-400-italic.woff2);font-style:italic}}@font-face{{font-family:Bit;src:url({F}bitter-latin-700-normal.woff2);font-weight:700}}*{{margin:0;box-sizing:border-box}}body{{position:relative;overflow:hidden;font-family:Bit;background:#fff;color:#062a55}}.c{{position:absolute;left:0;right:0;text-align:center}}"
NAVY='#062a55';PINK='#d6247f'
FYM=lambda s: f'Find <span style="font:italic 400 {s*1.04:.0f}px PF">Your</span> Mat-ch'
def pill(t): return f'<div style="display:inline-block;background:{NAVY};color:#fff;font:700 26px Bit;letter-spacing:5px;padding:12px 28px;border-radius:40px">{t}</div>'
def step(n,t,sub):
    return f'<div style="display:inline-flex;align-items:center;gap:22px"><span style="display:inline-grid;place-items:center;width:78px;height:78px;border-radius:50%;background:{PINK};color:#fff;font:400 44px Cap">{n}</span><span style="font:400 74px/1 Cap;color:{NAVY}">{t}</span></div><div style="font:italic 400 38px/1.3 PF;color:#4a3d58;margin:18px auto 0;max-width:900px">{sub}</div>'
def slides(H):
    st=H>1500; T=230 if st else 80   # story: keep top 230px + bottom 300px clear
    out={}
    # 1 hero
    out['1-hero']=f'''<div class="c" style="top:{T}px">{pill('NOW LIVE')}<div style="font:400 104px/1.02 Cap;margin-top:28px">{FYM(104)}<sup style="font-size:38px">™</sup><br>is here</div>
<div style="font:italic 400 38px PF;color:#4a3d58;margin-top:20px">Match mahjong tiles, mats &amp; racks across brands</div></div>
<div style="position:absolute;left:0;right:0;top:{T+600 if st else 545}px;height:760px">
<img src="file://{D}/fan-l.jpg" style="position:absolute;left:70px;top:70px;width:470px;border-radius:22px;transform:rotate(-9deg);box-shadow:0 24px 50px rgba(6,42,85,.22)">
<img src="file://{D}/fan-r.jpg" style="position:absolute;right:70px;top:70px;width:470px;border-radius:22px;transform:rotate(9deg);box-shadow:0 24px 50px rgba(6,42,85,.22)">
<img src="file://{D}/fan-c.jpg" style="position:absolute;left:285px;top:0;width:510px;border-radius:22px;box-shadow:0 30px 60px rgba(6,42,85,.28)"></div>'''
    pw=520 if st else 470; py=(T+250) if st else 280; px=(1080-pw)//2
    out['2-swipe']=f'<div class="c" style="top:{T}px">{step(1,"Swipe mats","Pick your tiles, then ♥ the mats you love and ✕ the rest.<br>Already own a mat? Start with your mat instead.")}</div>'+phone('cyk_swipe.png',pw,px,py+60)
    out['3-racks']=f'<div class="c" style="top:{T}px">{step(2,"Add racks","Racks that go with your tiles and your mat, from brands across the table.")}</div>'+phone('cyk_racks.png',pw,px,py+20)
    out['4-card']=f'<div class="c" style="top:{T}px">{step(3,"Get your match card","Save it, share it, shop it. Code MAHJMATCH saves you money at partner brands.")}</div>'+phone('cyk_card.png',pw,px,py+60)
    out['5-cta']=f'''<div class="c" style="top:{T+(80 if st else 40)}px"><div style="font:400 96px/1.05 Cap">Your turn to be<br>the matchmaker</div>
<div style="font:italic 400 40px PF;color:#4a3d58;margin-top:22px">Try {FYM(40)}. It's free.</div>
<div style="font:700 56px Bit;color:{PINK};margin-top:34px">mahjmatchmaker.com</div><div style="font:700 30px Bit;letter-spacing:4px;color:{NAVY};margin-top:14px">LINK IN BIO · #mahjmatch</div></div>'''+phone('home.png',420 if st else 330,(1080-(420 if st else 330))//2,(T+640) if st else 650)
    if st:
        out['6-link']=f'''<div class="c" style="top:{T}px">{pill('IT\'S LIVE')}<div style="font:400 92px/1.05 Cap;margin-top:28px">{FYM(92)}</div>
<div style="font:italic 400 40px PF;color:#4a3d58;margin-top:18px">Swipe your perfect mahjong set</div>
<div style="font:700 30px Bit;letter-spacing:5px;color:{PINK};margin-top:40px">TAP THE LINK ↓</div>
<div style="margin:22px auto 0;width:640px;height:150px;border:3px dashed #e8c3d3;border-radius:28px"></div></div>'''+phone('cyk_card.png',440,320,T+560)
    return out
mode=sys.argv[1]  # post|story
H=1350 if mode=='post' else 1920
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':H},device_scale_factor=1)
    for k,body in slides(H).items():
        h=f'<html><head><meta charset=utf8><style>{CSS}body{{width:1080px;height:{H}px}}</style></head><body>{body}</body></html>'
        open(f'_{mode}.html','w').write(h); pg.goto('file://'+D+f'/_{mode}.html'); pg.wait_for_timeout(900); pg.screenshot(path=f'launch-{mode}-{k}.jpg',type='jpeg',quality=92)
    b.close()
