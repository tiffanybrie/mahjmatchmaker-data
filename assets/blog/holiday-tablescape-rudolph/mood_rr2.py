exec(open('../hall/pin.py').read())
W,Hh=1000,1500
BG=(250,247,243,255); INK=(34,26,30); NAVY=(6,69,135); PINK=(214,96,140)
c=Image.new('RGBA',(W,Hh),BG); d=ImageDraw.Draw(c)
def lab(t,x,y,s=22,anchor='la'): ImageDraw.Draw(c).text((x,y),t,font=font('HomemadeApple.ttf',s),fill=INK,anchor=anchor)
def arr(p0,p1,p2): arrow(ImageDraw.Draw(c),p0,p1,p2,col=INK,w=3)
logo=fit(load(BR+'mahjmatchmaker-wordmark.png'),w=340); c.alpha_composite(logo,((W-340)//2,24))
_pf=font('Caprasimo.ttf',44); _pt="How I’m Styling"; _pw=d.textlength(_pt,font=_pf)+90
d.rounded_rectangle((W//2-_pw/2,120,W//2+_pw/2,196),38,fill=NAVY)
d.text((W//2,160),_pt,font=_pf,fill=(255,255,255),anchor='mm')
d.text((W//2,250),"The Rackin’ Rudolph Mat",font=font('Caprasimo.ttf',58),fill=PINK,anchor='mm')
d.text((W//2,322),'holiday edition',font=font('HomemadeApple.ttf',38),fill=INK,anchor='mm')
# mat up top, label above with arrow down
lab("rackin' rudolph mat",420,362,s=22); arr((540,398),(546,410),(538,424))
MS=470; MX,MY=300,432
m=load('cut/mat_rr.jpg').resize((MS,int(MS*1692/1670)),Image.LANCZOS)
mk=Image.new('L',m.size,0); ImageDraw.Draw(mk).rounded_rectangle((0,0,m.width-1,m.height-1),20,fill=255); m.putalpha(mk)
place(c,m,MX,MY)
mb=MY+m.height
# milk glass rack set laid over the bottom tartan border
r=fit(load('cut/rack_milkglass.png'),w=320); place(c,r,MX+75,mb-62,rot=0)
lab('middle & main milk glass racks',360,mb+78,s=21); arr((470,mb+74),(466,mb+62),(476,mb+50))
# left: cloth ; right: tiles
lab('cherry red cloth',42,452,s=21); arr((150,488),(154,500),(146,512))
cl=card(load('raw/t_31a3RZHWCgL.jpg'),170,170,r=22,border=8); place(c,cl,36,514,rot=-4)
lab("rackin' rudolph tiles",28,752,s=19); arr((110,786),(114,798),(106,810))
tf=fit(load('cut/tiles_fan.png'),w=245); place(c,tf,18,818,rot=-4)
# bottom row
Y=1090
lab('the bow lamp',70,Y,s=22)
lp=fit(load('cut/lamp_bow.png'),h=270); place(c,lp,100,Y+44)
lab('its bow echoes the',225,Y+112,s=17); lab("bows on the mat",231,Y+136,s=17)
lab('reindeer dice box',420,Y+28,s=21)
db=fit(load('cut/deer_box.png'),h=205); place(c,db,450,Y+82)
lab('white marble coasters',680,Y+100,s=20)
co=fit(load('cut/coaster_marble.png'),w=125); place(c,co,730,Y+150)
d=ImageDraw.Draw(c)
d.rounded_rectangle((90,1428,910,1488),30,fill=NAVY)
d.text((W//2,1458),'shop the look  ·  mahjmatchmaker.com',font=font('DMSerif.ttf',30),fill=(255,255,255),anchor='mm')
c.convert('RGB').save('out/holiday-mahjong-table-rackin-rudolph-shop-the-look.jpg',quality=92)
print('mat bottom',mb)
