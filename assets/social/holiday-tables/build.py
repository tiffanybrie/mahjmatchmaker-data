# Holiday table story sets + reels (draft). Raven story format (hall/story2.py).
import os, sys, subprocess, shutil, math
S='/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/'
exec(open(S+'hall/pin.py').read())
OUT=S+'holiday_social/'
REPO='/home/claude/mahjmatchmaker-data/'
W,Hh=1080,1920
BG=(250,247,243,255); INK=(34,26,30)
logo=fit(load(BR+'mahjmatchmaker-wordmark.png'),w=440)

def lab(d,t,x,y,s=40,anchor='la',col=INK): d.text((x,y),t,font=font('HomemadeApple.ttf',s),fill=col,anchor=anchor)
def note(d,t,x,y,s=34,anchor='la',col=INK): d.text((x,y),t,font=font('Caveat-Bold.ttf',s),fill=col,anchor=anchor)
def base():
    c=Image.new('RGBA',(W,Hh),BG); c.alpha_composite(logo,((W-440)//2,60)); return c
def matimg(p,w,rad=0.045):
    m=load(p); m=m.resize((w,int(w*m.height/m.width)),Image.LANCZOS)
    mk=Image.new('L',m.size,0); ImageDraw.Draw(mk).rounded_rectangle((0,0,m.width-1,m.height-1),int(w*rad),fill=255); m.putalpha(mk); return m
def pill(c,d,txt,y,col,tcol,size=64,padx=70,h=124):
    f=font('Caprasimo.ttf',size); tw=d.textlength(txt,font=f)
    d.rounded_rectangle((W//2-tw/2-padx,y,W//2+tw/2+padx,y+h),h//2,fill=col)
    d.text((W//2,y+h//2),txt,font=f,fill=tcol,anchor='mm')
def center_place(c,im,cx,cy,rot=0):
    if rot: im=im.rotate(rot,expand=True,resample=Image.BICUBIC)
    place(c,im,cx-im.width//2,cy-im.height//2)

TS=S+'tablescape/'; T2=S+'tablescape2/'; T3=S+'tablescape3/'
HER=REPO+'assets/tiles/album/heritage.jpg'
LOOKS={
 'polo':dict(
   pillc=(6,69,135),pillt=(255,255,255),titlec=(214,96,140),
   title='The Polo Club Mat',sub='holiday edition',
   mat=TS+'cut/mat_clean.jpg',matrad=0.045,matlab='polo club mat',
   rack=TS+'raw/rack_walnut.png',racklab='bam bird walnut racks',rack_on_mat=False,
   tiles=('card',HER),tileslab='heritage tiles',
   board=REPO+'assets/blog/holiday-tablescape/holiday-mahjong-table-polo-club-shop-the-look.jpg',
   brandlogo=None),
 'rattan':dict(
   pillc=(0x5e,0x65,0x43),pillt=(0xfb,0xf3,0xe6),titlec=(0x5e,0x65,0x43),
   title='The Rattan Mat',sub='retro holiday edition',
   mat=T2+'cut/rattan_clean.png',matrad=0,matlab='rattan mat',
   rack=T2+'raw/rack_walnut.png',racklab='walnut racks',rack_on_mat=False,
   tiles=('card',HER),tileslab='heritage tiles',
   board=REPO+'assets/blog/holiday-tablescape-rattan/holiday-mahjong-table-rattan-shop-the-look.jpg',
   brandlogo=None),
 'rudolph':dict(
   pillc=(222,34,54),pillt=(255,255,255),titlec=(222,34,54),
   title="The Rackin’ Rudolph Mat",sub=None,
   mat=T3+'cut/mat_rr.jpg',matrad=0.0425,matlab="rackin' rudolph mat",
   rack=T3+'cut/rack_milkglass.png',racklab='middle & main scalloped milk glass racks',rack_on_mat=True,
   tiles=('cut',T3+'cut/tiles_fan2.png'),tileslab="rackin' rudolph tiles",
   board=REPO+'assets/blog/holiday-tablescape-rudolph/holiday-mahjong-table-rackin-rudolph-shop-the-look.jpg',
   brandlogo=REPO+'builder/logos/hiphipmahjong_0.png'),
}

# ---------- frame builders ----------
def f_cover(L):
    c=base(); d=ImageDraw.Draw(c)
    m=matimg(L['mat'],800,L['matrad']); place(c,m,(W-800)//2,230,rot=-2)
    y=230+m.height+70
    pill(c,d,"How I’m Styling",y,L['pillc'],L['pillt'])
    ts=84
    while d.textlength(L['title'],font=font('Caprasimo.ttf',ts))>960: ts-=2
    d.text((W//2,y+235),L['title'],font=font('Caprasimo.ttf',ts),fill=L['titlec'],anchor='mm')
    if L['sub']: d.text((W//2,y+370),L['sub'],font=font('HomemadeApple.ttf',58),fill=INK,anchor='mm')
    return c

def f_setup(L):
    c=base(); d=ImageDraw.Draw(c)
    lab(d,L['matlab'],W//2,240,s=42,anchor='ma')
    arrow(d,(W//2+170,290),(W//2+190,320),(W//2+160,350))
    MW=780; m=matimg(L['mat'],MW,L['matrad']); mx,my=(W-MW)//2,370; place(c,m,mx,my)
    mb=my+m.height
    r=load(L['rack'])
    if L['rack_on_mat']:
        r=fit(r,w=600); place(c,r,mx+90,mb-100); ry=mb-100+r.height+10
    else:
        r=fit(r,w=640); place(c,r,(W-640)//2,mb+40,rot=2); ry=mb+40+r.height+20
    lab(d,L['racklab'],W//2,ry+20,s=34,anchor='ma')
    ty=ry+120
    if L['tiles'][0]=='card':
        t=card(load(L['tiles'][1]),360,300); place(c,t,110,ty,rot=-3)
        lab(d,L['tileslab'],560,ty+110,s=42); arrow(d,(600,ty+190),(560,ty+230),(500,ty+220))
    else:
        t=fit(load(L['tiles'][1]),w=500); place(c,t,50,ty+20,rot=-2)
        lab(d,L['tileslab'],590,ty+40,s=36); note(d,'those cherry red backs!',600,ty+130,s=44)
    return c

def f_accent(L,items):
    """items: list of (img_path, kind, size, label, note), stacked and centered"""
    c=base(); d=ImageDraw.Draw(c)
    th=matimg(L['mat'],200,L['matrad']); place(c,th,W-200-50,200,rot=4,shad=True)
    n=len(items); top=360; bottom=1840; slot=(bottom-top)//n
    for i,(p,kind,sz,label,nt) in enumerate(items):
        y0=top+slot*i
        txt_h=70+(60 if nt else 0)
        maxh=slot-txt_h-60
        if kind=='card':
            s_=min(sz,maxh); im=card(load(p),s_,s_)
        else:
            im=load(p); im=fit(im,h=sz) if im.height>=im.width else fit(im,w=sz)
            if im.height>maxh: im=fit(im,h=maxh)
            if im.width>900: im=fit(im,w=900)
        blk=im.height+txt_h+30
        iy=y0+(slot-blk)//2
        place(c,im,(W-im.width)//2,iy)
        ly=iy+im.height+50
        lab(d,label,W//2,ly,s=44,anchor='ma')
        if nt: note(d,nt,W//2,ly+80,s=48,anchor='ma')
    return c

def f_poll(L,opts):
    c=base(); d=ImageDraw.Draw(c)
    d.rounded_rectangle((70,240,1010,370),65,fill=(246,211,224))
    d.text((W//2,305),'pick one for the center of the table',font=font('Caprasimo.ttf',46),fill=L['pillc'],anchor='mm')
    xs=[185,540,880]; base_y=1060
    for (p,label,h),x in zip(opts,xs):
        im=fit(load(p),h=h)
        if im.width>300: im=fit(im,w=300)
        place(c,im,x-im.width//2,base_y-im.height)
        lab(d,label,x,base_y+50,s=32,anchor='ma')
    note(d,'tie a velvet ribbon on it',880,base_y+120,s=36,anchor='ma')
    fo=ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Medium.otf',38)
    for x in (365,715): d.text((x,820),'or',font=fo,fill=L['pillc'],anchor='mm')
    # clear zone for the Instagram poll sticker: y ~1300-1700
    lab(d,'which would you pick?',W//2,1230,s=40,anchor='ma',col=L['pillc'])
    arrow(d,(W//2+250,1280),(W//2+270,1320),(W//2+220,1360),col=L['pillc'],w=5)
    return c

def f_board(L):
    c=Image.new('RGBA',(W,Hh),BG)
    b=load(L['board']); b=fit(b,w=1040); place(c,b,20,(Hh-b.height)//2,shad=True)
    return c

def f_end(L,strip_items):
    c=base(); d=ImageDraw.Draw(c)
    d.text((W//2,230),'Shop the',font=font('DMSerif.ttf',80),fill=INK,anchor='ma')
    d.text((W//2,330),'whole table',font=font('Caprasimo.ttf',120),fill=L['titlec'],anchor='ma')
    d.text((W//2,500),'all the links + codes in one place',font=font('HomemadeApple.ttf',40),fill=INK,anchor='ma')
    strip=[]
    for p,kind,h in strip_items:
        if kind=='mat': strip.append(matimg(p,int(h*1.0),L['matrad']))
        elif kind=='card': strip.append(card(load(p),int(h*0.9),h,r=14,border=5))
        else: strip.append(fit(load(p),h=h))
    gap=22; tw=sum(i.width for i in strip)+gap*(len(strip)-1); sc=min(1,940/tw)
    if sc<1: strip=[i.resize((int(i.width*sc),int(i.height*sc))) for i in strip]
    tw=sum(i.width for i in strip)+gap*(len(strip)-1); x=(W-tw)//2
    mh=max(i.height for i in strip)
    for i in strip: place(c,i,x,650+(mh-i.height)//2); x+=i.width+gap
    arrow(d,(W//2-120,900),(W//2-150,950),(W//2-60,990),col=L['titlec'],w=5)
    d.text((W//2+30,925),'tap the link',font=font('HomemadeApple.ttf',38),fill=L['titlec'],anchor='la')
    # clear zone y 1000-1280 for the link sticker
    d.rounded_rectangle((190,1330,890,1460),65,fill=L['pillc'])
    d.text((W//2,1395),'code MAHJMATCH',font=font('Caprasimo.ttf',62),fill=L['pillt'],anchor='mm')
    d.text((W//2,1530),'at our partner brands',font=font('HomemadeApple.ttf',36),fill=INK,anchor='mm')
    if L.get('brandlogo'):
        bl=recolor(fit(load(L['brandlogo']),w=220),(40,30,34)); c.alpha_composite(bl,((W-bl.width)//2,1630))
    return c

FRAMES={
 'polo':lambda L:[f_cover(L),f_setup(L),
    f_accent(L,[(TS+'raw/cloth60.jpg','card',420,'hunter green cloth','60x60 for a little more drape'),
                (TS+'cut/coaster1.png','cut',300,'cognac coasters',None)]),
    f_accent(L,[(TS+'cut/ringdish.png','cut',720,'christmas tree ring dish','a home for the dice')]),
    f_poll(L,[(TS+'cut/tree.png','a little tree',520),(TS+'cut/wreath.png','a candle wreath',300),(TS+'cut/lamp_green.png','a ribboned lamp',580)]),
    f_board(L),
    f_end(L,[(TS+'cut/mat_clean.jpg','mat',150),(HER,'card',120),(TS+'raw/rack_walnut.png','cut',40),(TS+'raw/cloth60.jpg','card',110),(TS+'cut/wreath.png','cut',90),(TS+'cut/lamp_green.png','cut',170),(TS+'cut/ringdish.png','cut',90)])],
 'rattan':lambda L:[f_cover(L),f_setup(L),
    f_accent(L,[(T2+'cut/clothE.png','cut',640,'red tartan cloth','60x60 for a little more drape')]),
    f_accent(L,[(T2+'cut/lamp_tree.png','cut',760,'ceramic tree lamp','the retro centerpiece')]),
    f_accent(L,[(T2+'cut/dice_holly.png','cut',420,'holly dice dish',None),(T2+'cut/coaster_amber.png','cut',360,'amber glass coasters',None)]),
    f_board(L),
    f_end(L,[(T2+'cut/rattan_clean.png','mat',150),(HER,'card',120),(T2+'raw/rack_walnut.png','cut',40),(T2+'cut/clothE.png','cut',100),(T2+'cut/lamp_tree.png','cut',170),(T2+'cut/dice_holly.png','cut',95),(T2+'cut/coaster_amber.png','cut',85)])],
 'rudolph':lambda L:[f_cover(L),f_setup(L),
    f_accent(L,[(T3+'raw/t_31a3RZHWCgL.jpg','card',460,'cherry red cloth','matches the bows')]),
    f_accent(L,[(T3+'cut/lamp_bow.png','cut',780,'the bow lamp','its bow echoes the bows on the mat')]),
    f_accent(L,[(T3+'cut/deer_box.png','cut',520,'reindeer dice box','a little box for the dice'),(T3+'cut/coaster_marble.png','cut',300,'white marble coasters',None)]),
    f_board(L),
    f_end(L,[(T3+'cut/mat_rr.jpg','mat',150),(T3+'cut/tiles_fan2.png','cut',90),(T3+'cut/rack_milkglass.png','cut',60),(T3+'raw/t_31a3RZHWCgL.jpg','card',110),(T3+'cut/lamp_bow.png','cut',170),(T3+'cut/deer_box.png','cut',120)])],
}

if __name__=='__main__':
    which=sys.argv[1:] or list(LOOKS)
    for k in which:
        L=LOOKS[k]; od=OUT+k+'/stories/'; os.makedirs(od,exist_ok=True)
        for f in os.listdir(od): os.remove(od+f)
        fr=FRAMES[k](L)
        for i,c in enumerate(fr,1): c.convert('RGB').save(od+f'{k}-story-{i:02d}.jpg',quality=92)
        # contact sheet
        th=[c.convert('RGB').resize((270,480)) for c in fr]
        sh=Image.new('RGB',(270*len(th)+10*(len(th)-1),480),(80,80,90))
        for i,t in enumerate(th): sh.paste(t,(i*280,0))
        sh.save(OUT+k+'/stories_sheet.jpg',quality=88)
        print(k,len(fr),'frames')
