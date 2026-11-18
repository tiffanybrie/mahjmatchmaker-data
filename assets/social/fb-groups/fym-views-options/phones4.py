from PIL import Image,ImageDraw,ImageFont,ImageFilter
R='/home/claude/mahjmatchmaker-data/'
W,H=1080,1240; bg=Image.new('RGB',(W,H),'#f7f2e8'); d=ImageDraw.Draw(bg)
cap=ImageFont.truetype(R+'assets/fonts/Caprasimo.ttf',80); pf=ImageFont.truetype(R+'assets/fonts/playfair-display-latin-700-italic.woff2',86)
parts=[('Find ',cap),('Your ',pf),('Mat-ch',cap)]; x=(W-sum(d.textlength(t,font=f) for t,f in parts))/2-12; y=96
for t,f in parts: d.text((x,y),t,font=f,fill='#062a55',anchor='lm'); x+=d.textlength(t,font=f)
d.text((x+2,y-28),'™',font=ImageFont.truetype(R+'assets/fonts/Caprasimo.ttf',28),fill='#062a55',anchor='lm')
d.text((W//2,170),'Match your tiles, then mock them up, right on your phone',font=ImageFont.truetype(R+'assets/fonts/playfair-display-latin-400-italic.woff2',35),fill='#8a5a2b',anchor='mm')
lab=ImageFont.truetype(R+'assets/fonts/poppins-latin-600-normal.woff2',26)
pw=340; gap=(W-3*pw)//4; top=262
for i,(f,l) in enumerate([('p1.png','Table view'),('p2.png','Aerial'),('p3.png','Up close')]):
    p=Image.open(f); p=p.resize((pw,int(p.height*pw/p.width)),Image.LANCZOS)
    xx=gap+i*(pw+gap)
    a=p.split()[-1].point(lambda v:80 if v>128 else 0); sh=Image.new('RGBA',p.size,(60,20,60,0)); sh.putalpha(a); sh=sh.filter(ImageFilter.GaussianBlur(12))
    bg.paste(p,(xx,top+40),p)
    tw=d.textlength(l,font=lab); cx=xx+pw//2
    d.rounded_rectangle((cx-tw/2-20,top-22,cx+tw/2+20,top+22),22,fill='#062a55'); d.text((cx,top),l,font=lab,fill='white',anchor='mm')
ph=int(2672*pw/1328)
ty=top+40+ph+50
d.text((W//2,ty),'Sunday tiles · White Lotus mat by Mahj Tile Haus · tortoise racks',font=ImageFont.truetype(R+'assets/fonts/poppins-latin-500-normal.woff2',24),fill='#062a55',anchor='mm')
d.text((W//2,ty+46),'1,300+ mats · 280+ tile sets · 290+ racks · 67 brands',font=ImageFont.truetype(R+'assets/fonts/poppins-latin-600-normal.woff2',28),fill='#8a5a2b',anchor='mm')
d.text((W//2,ty+96),'Free at mahjmatchmaker.com/find-your-match',font=ImageFont.truetype(R+'assets/fonts/poppins-latin-500-normal.woff2',26),fill='#062a55',anchor='mm')
bg.save('phones-sunday-whitelotus.jpg',quality=92); print(ty+46)
