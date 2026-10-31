"""Oct 31 content bank: Find Your Mat-ch pieces that show the app IN USE (real v107 / Version 1.9.2 screens from cap.py, cap_color.py, cap_matdoor.py).
Renders feed slides (1080x1350), story frames (1080x1920, every slide), Pinterest pins (1000x1500). FOR REVIEW ONLY: never post.
Usage: python3 build.py   (raw screens in /dev/shm/w/caps)"""
import os,json
os.environ.setdefault('TMPDIR','/dev/shm/w')
from playwright.sync_api import sync_playwright
OUTD=os.path.dirname(os.path.abspath(__file__)); R=os.path.abspath(OUTD+'/../../..'); CAPS='/dev/shm/w/caps'
exec(open(R+'/assets/social/mockups-oct26/mk.py').read().split('CSS=')[0].replace("D=os.path.abspath('.');","D='"+CAPS+"';"))
F='file://'+R+'/scripts/social/tileprofile/fonts/'
WHITE=('#f7f7f5','#d6d6d3','#e2e2df'); SH='0 30px 60px rgba(6,42,85,.16), 0 6px 14px rgba(6,42,85,.08)'
NAVY,PINK,CREAM,BLUSH,GREEN,RED='#062a55','#e0547f','#faf3ea','#f7b6c8','#1f5a3a','#a61e21'
CSS=f"""@font-face{{font-family:Cap;src:url({F}Caprasimo.ttf)}}@font-face{{font-family:PF;font-style:italic;src:url({F}playfair-display-latin-600-italic.woff2)}}
@font-face{{font-family:Bit;font-weight:700;src:url({F}bitter-latin-700-normal.woff2)}}*{{margin:0}}body{{position:relative;overflow:hidden;font-family:Bit}}
.c{{position:absolute;left:0;right:0;text-align:center}}.pf{{font-family:PF;font-style:italic;font-weight:600}}"""
FYM=lambda s:f'Find <span class="pf" style="font-size:{s*1.04:.0f}px">Your</span> Mat-ch<sup style="font-size:{s*.36:.0f}px">&trade;</sup>'
def pill(t,bg=PINK,fg='#fff',fs=30): return f'<span style="display:inline-block;background:{bg};color:{fg};font:700 {fs}px Bit;letter-spacing:{fs/5:.0f}px;padding:{fs*.45:.0f}px {fs:.0f}px;border-radius:40px">{t}</span>'
# geometry per format: (W,H, top, h1 size, sub size, phone y, single phone w, foot y)
G={'feed':(1080,1350,64,84,38,410,430,None),'story':(1080,1920,150,100,44,600,500,1690),'pin':(1000,1500,70,80,38,440,430,1360)}
def head(fmt,kick,h1,sub,fg,acc,kbg):
    W,H,t,h,s,*_=G[fmt]
    return f'<div class="c" style="top:{t}px;color:{fg}">{pill(kick,kbg,fs=26 if fmt=="feed" else 30)}<div style="font:400 {h}px/1.04 Cap;margin-top:{22 if fmt=="feed" else 30}px;padding:0 40px">{h1}</div><div style="font:600 {s}px/1.25 PF;font-style:italic;color:{acc};margin-top:14px;padding:0 70px">{sub}</div></div>'
def foot(fmt,fg,acc,code=True):
    W,H,*_,fy=G[fmt]
    if fy is None: return ''
    url='mahjmatchmaker.com' + (' &middot; code MAHJMATCH' if code else '')
    return f'<div class="c" style="top:{fy}px;color:{fg}"><div style="font:400 {56 if fmt=="story" else 50}px Cap">{FYM(56 if fmt=="story" else 50)}</div><div style="font:700 32px Bit;letter-spacing:.06em;margin-top:14px;color:{acc}">{url}</div></div>'
def phones(fmt,imgs):
    W,H,t,h,s,py,pw,fy=G[fmt]; cx=W/2
    if len(imgs)==1:
        return phone(imgs[0],pw,*WHITE,cx-pw/2,py,0,1,SH)
    if len(imgs)==2:
        w=pw*0.95 if fmt!='story' else 400
        return phone(imgs[0],w,*WHITE,cx-w-30,py+40,-4,1,SH)+phone(imgs[1],w,*WHITE,cx+30,py,4,2,SH)
    w=pw*0.8 if fmt!='story' else 330; wc=w*1.21
    return phone(imgs[0],w,*WHITE,cx-wc/2-w+40,py+90,-5,1,SH)+phone(imgs[2],w,*WHITE,cx+wc/2-40,py+90,5,1,SH)+phone(imgs[1],wc,*WHITE,cx-wc/2,py,0,3,SH)
def cardimg(fmt,img):
    W,H,t,h,s,py,pw,fy=G[fmt]; ch=(fy or H)-py-40; cw=ch*9/16
    return f'<img src="file://{CAPS}/{img}" style="position:absolute;left:{(W-cw)/2:.0f}px;top:{py:.0f}px;height:{ch:.0f}px;border-radius:22px;box-shadow:{SH}">'
def cta(fmt,bg,fg,acc,line,code=True):
    W,H,*_=G[fmt]; y=H*0.30
    c2=f'<div style="font:700 38px Bit;margin-top:26px;color:{acc}">Shop it with code MAHJMATCH</div>' if code else ''
    return f'<div class="c" style="top:{y:.0f}px;color:{fg}"><div style="font:700 30px Bit;letter-spacing:6px;color:{acc}">FREE TO USE</div><div style="font:400 {120 if W>1000 else 110}px/1.05 Cap;margin-top:30px">{FYM(120)}</div><div style="font:600 48px/1.3 PF;font-style:italic;color:{acc};margin:40px 80px 0">{line}</div><div style="font:700 44px Bit;margin-top:70px">mahjmatchmaker.com</div>{c2}<div style="font:700 30px Bit;margin-top:22px;opacity:.8">link in bio</div></div>'
def S(kick,h1,sub,imgs=None,card=None,bg=CREAM,fg=NAVY,acc=PINK,kbg=PINK,ctaline=None,code=True):
    return dict(kick=kick,h1=h1,sub=sub,imgs=imgs or [],card=card,bg=bg,fg=fg,acc=acc,kbg=kbg,ctaline=ctaline,code=code)
def body(fmt,s):
    if s['ctaline']: return cta(fmt,s['bg'],s['fg'],s['acc'],s['ctaline'],s['code'])
    b=head(fmt,s['kick'],s['h1'],s['sub'],s['fg'],s['acc'],s['kbg'])
    b+=cardimg(fmt,s['card']) if s['card'] else phones(fmt,s['imgs'])
    if fmt!='feed': b+=foot(fmt,s['fg'],s['acc'],s['code'] and fmt!='pin')
    return b
CTA_N=lambda line,code=True: S('','','',bg=NAVY,fg='#fff',acc=BLUSH,ctaline=line,code=code)
PIECES={
 'p1-how-it-works':[
  S('HOW IT WORKS','Your tiles, your mat,<br>in 3 taps',FYM(40)+' shows you real mats with your tiles',['p-search.png','p-deck.png','p-card.png']),
  S('STEP 1','Pick your tiles','Search any set. Here: Papaya Spritz by Oh My Mahjong',['p-search.png']),
  S('STEP 2','Swipe real mats','&#9829; the ones you love, &#10005; the rest. Heiress by Britt Mills',['p-deck.png']),
  S('STEP 3','Add racks','Swipe racks with your mat right above them',['p-rack0.png']),
  S('IT&rsquo;S A MATCH!','Save it. Share it.','Your match card, ready for your group chat',['p-card.png']),
  CTA_N('Bring your tiles.<br>We&rsquo;ll bring the mats.')],
 'p2-holiday-30s':[
  S('HOLIDAY TABLE','Christmas table<br>in 30 seconds','Tinselle tiles + Evergreen &amp; Tartan, matched in the app',['h-deck.png','h-heart.png','h-card.png'],bg='#ffffff',kbg=RED),
  S('0:05','Start with your tiles','Tinselle (Emerald Green) by Virora Mahjong',['h-deck.png'],bg='#ffffff',kbg=RED),
  S('0:10','Tap Holiday + Green','The deck narrows to Christmas mats in your colors',['h-filt1.png'],bg='#ffffff',kbg=RED),
  S('0:15','&#9829; Evergreen &amp; Tartan','by Anders Ruff',['h-heart.png'],bg='#ffffff',kbg=RED),
  S('0:25','Swipe the racks','Bird &amp; Bamboo Brick Red + Evergreen',['h-rack2.png'],bg='#ffffff',kbg=RED),
  S('0:30','It&rsquo;s a match!','Your match card, made in the app','',card='h-storycard.jpg',bg='#ffffff',kbg=RED),
  CTA_N('Your tiles. Christmas mats<br>that love them.')],
 'p3-color-filter':[
  S('CAN&rsquo;T DECIDE ON A MAT?','Tap a color','One tap and the mats change. Papaya Spritz tiles, three ways',['c-orange.png','c-blue.png','c-green.png']),
  S('THE COLOR CHIPS','Pick a color','Tap it again to clear it',['c-orange-chips.png']),
  S('ORANGE &amp; CORAL','Pull out the papaya','Press for by Anders Ruff',['c-orange.png']),
  S('BLUE &amp; TEAL','Go cool','Larkspur by Oh My Mahjong',['c-blue.png']),
  S('GREEN','Go garden','Greenly by Mahj &amp; Vine',['c-green.png']),
  CTA_N('Same tiles. A whole new table<br>with one tap.')],
 'p4-two-doors':[
  S('TWO WAYS IN','Tiles first<br>or mat first?','Papaya Spritz &#8596; Heiress, from both sides',['p-deck.png','m-tiles.png']),
  S('ALREADY OWN YOUR TILES?','Start there','Pick your set, swipe mats under it',['p-deck.png']),
  S('LOVE A MAT?','Start with the mat','Pick the mat, swipe tile sets on it',['m-tiles.png']),
  CTA_N('Tiles first or mat first.<br>Either way, it&rsquo;s a match.')],
 'p6-tartan-tidings-matdoor':[
  S('OWN TARTAN TIDINGS?','Which tiles go on it?','Start with the mat: Tartan Tidings by Anders Ruff',['td2.png','td3.png','td4.png'],bg='#ffffff',kbg=RED),
  S('&#9829; OR &#10005;','Tinselle (Emerald Green)','by Virora Mahjong',['td2.png'],bg='#ffffff',kbg=RED),
  S('&#9829; OR &#10005;','Dear Santa','by Anders Ruff',['td3.png'],bg='#ffffff',kbg=RED),
  S('&#9829; OR &#10005;','Rackin&rsquo; Rudolph','by Hip Hip Mahjong',['td4.png'],bg='#ffffff',kbg=RED),
  CTA_N('Start with your mat.<br>Swipe the tiles that love it.')],
}
PINS=[ # id, head, sub, imgs/card, board
 ('fym-pin-mat-matching-tool','Mahjong mat matching tool','Pick your tiles. Swipe real mats. Free.',['p-search.png','p-deck.png','p-card.png'],None),
 ('fym-pin-mat-for-your-tiles','Find a mahjong mat for your tiles','Swipe mats under your own tile set',['p-deck.png'],None),
 ('fym-pin-christmas-mat-ideas','Christmas mahjong mat ideas','Tap Holiday and swipe mats with your tiles',['h-heart.png'],None),
 ('fym-pin-table-setup','Mahjong table setup: tiles, mat + racks','Mock up the whole table on your phone',['h-rack2.png','h-card.png'],None),
 ('fym-pin-mats-by-color','Mahjong mats by color','Tap a color, the mats change',['c-orange.png','c-blue.png','c-green.png'],None),
 ('fym-pin-tiles-for-my-mat','Which mahjong tiles go with my mat?','Start with the mat, swipe tile sets on it',['m-tiles.png'],None),
 ('fym-pin-holiday-table-card','Christmas mahjong table idea','Tiles + mat + racks, matched in 30 seconds',None,'h-storycard.jpg'),
 ('fym-pin-match-card','Mahjong match card maker','Save and share your tiles + mat + racks',['p-card.png'],None),
]
if __name__=='__main__':
    out=lambda *a: os.path.join(OUTD,*a)
    for k in PIECES: os.makedirs(out(k),exist_ok=True)
    os.makedirs(out('pins'),exist_ok=True)
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page()
        def render(fmt,s,fn,bgover=None):
            W,H,*_=G[fmt]; pg.set_viewport_size({'width':W,'height':H})
            open('/dev/shm/w/_v.html','w').write(f'<html><head><meta charset=utf8><style>{CSS}body{{width:{W}px;height:{H}px}}</style></head><body style="background:{bgover or s["bg"]}">{body(fmt,s)}</body></html>')
            pg.goto('file:///dev/shm/w/_v.html'); pg.wait_for_timeout(700); pg.screenshot(path=fn,type='jpeg',quality=88)
        for k,sl in PIECES.items():
            for i,s in enumerate(sl,1):
                render('feed',s,out(k,f'feed-{i:02d}.jpg')); render('story',s,out(k,f'story-{i:02d}.jpg'))
            print(k,len(sl))
        for pid,h1,sub,imgs,card in PINS:
            s=S('FREE MAHJONG TOOL',h1,sub,imgs,card,code=False)
            render('pin',s,out('pins',pid+'.jpg'))
        print('pins',len(PINS))
        b.close()
