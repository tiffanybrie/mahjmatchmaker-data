"""Charleston Mahjong Club Hunt Club Edition restock story frames (partner watch Oct 30 6:30pm ET; pattern from restock-catrina-oct27). Screens = LIVE /find-your-match (cap_live.py "Hunt Club Edition" hunt "Hunt Club"). Tiffany has no Hunt Club matches yet, so no N count. FOR REVIEW ONLY: never post.
Real app screens in white iPhone frames. Usage: python3 build.py"""
import os
from playwright.sync_api import sync_playwright
D=os.path.dirname(os.path.abspath(__file__)); R='/home/claude/pc'
exec(open(R+'/assets/social/mockups-oct26/mk.py').read().split('CSS=')[0].replace("D=os.path.abspath('.');","D='"+D+"';"))
F='file://'+R+'/scripts/social/tileprofile/fonts/'
WHITE=('#f7f7f5','#d6d6d3','#e2e2df'); SH='0 30px 60px rgba(6,42,85,.16), 0 6px 14px rgba(6,42,85,.08)'
NAVY,PINK,CREAM,BLUSH,GREEN='#062a55','#e0547f','#faf3ea','#f7b6c8','#1f5a3a'
CSS=f"""@font-face{{font-family:Cap;src:url({F}Caprasimo.ttf)}}@font-face{{font-family:PF;font-style:italic;src:url({F}playfair-display-latin-600-italic.woff2)}}
@font-face{{font-family:Bit;font-weight:700;src:url({F}bitter-latin-700-normal.woff2)}}*{{margin:0}}body{{width:1080px;height:1920px;position:relative;overflow:hidden;font-family:Bit}}
.c{{position:absolute;left:0;right:0;text-align:center}}.pf{{font-family:PF;font-style:italic;font-weight:600}}"""
FYM=lambda s:f'Find <span class="pf" style="font-size:{s*1.04:.0f}px">Your</span> Mat-ch<sup style="font-size:{s*.36:.0f}px">&trade;</sup>'
def pill(t,bg=PINK,fg='#fff'): return f'<span style="display:inline-block;background:{bg};color:{fg};font:700 30px Bit;letter-spacing:6px;padding:14px 32px;border-radius:40px">{t}</span>'
def top(kicker,h1,sub,fg,acc,kbg=PINK): return f'<div class="c" style="top:150px;color:{fg}">{pill(kicker,kbg)}<div style="font:400 104px/1.02 Cap;margin-top:30px">{h1}</div><div style="font:400 44px/1.25 PF;font-style:italic;font-weight:600;color:{acc};margin-top:20px;padding:0 70px">{sub}</div></div>'
def foot(fg,acc): return f'<div class="c" style="top:1650px;color:{fg}"><div style="font:400 60px Cap">{FYM(60)}</div><div style="font:700 34px Bit;letter-spacing:.06em;margin-top:16px;color:{acc}">mahjmatchmaker.com &middot; code MAHJMATCH</div></div>'
def trio(l,c,r,y=640): return phone(l,330,*WHITE,95,y+90,-5,1,SH)+phone(r,330,*WHITE,655,y+90,5,1,SH)+phone(c,400,*WHITE,340,y,0,3,SH)
def duo(a,b,y=640): return phone(a,400,*WHITE,110,y+40,-4,1,SH)+phone(b,400,*WHITE,570,y,4,2,SH)
V={}
V['hc-A-cream-trio']=(CREAM, top('BACK IN STOCK','Mock up Hunt Club','Swipe mats for Charleston Mahjong Club&rsquo;s Hunt Club tiles',NAVY,PINK)+trio('hc-swipe0.png','hc-swipe1.png','hc-swipe2.png')+foot(NAVY,PINK))
V['hc-B-green-trio']=(GREEN, top('BACK AT CHARLESTON MAHJONG CLUB','Hunt Club is back.','Just in time for Halloween. Now find her mat.','#fff',BLUSH)+trio('hc-swipe0.png','hc-swipe1.png','hc-swipe2.png')+foot('#fff',BLUSH))
V['hc-C-white-duo']=('#ffffff', top('GOT HUNT CLUB?','Now the mat.','Swipe mats + racks for her in Find Your Mat-ch',NAVY,PINK,NAVY)+duo('hc-swipe1.png','hc-swipe0.png')+foot(NAVY,PINK))
os.makedirs(D+'/out',exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1920})
    for k,(bg,body) in V.items():
        open(D+'/_v.html','w').write(f'<html><head><meta charset=utf8><style>{CSS}</style></head><body style="background:{bg}">{body}</body></html>')
        pg.goto('file://'+D+'/_v.html'); pg.wait_for_timeout(1200); pg.screenshot(path=f'{D}/out/{k}.jpg',type='jpeg',quality=92); print(k)
    b.close()
os.remove(D+'/_v.html')
