import sys
from PIL import Image,ImageDraw,ImageFont,ImageFilter
R='/home/claude/mahjmatchmaker-data/'
def crop(f,kind):
    im=Image.open(f).convert('RGB')
    return im.crop((36,330,1134,1590)) if kind!='up' else im.crop((36,530,1134,2370))
def rounded(im,r):
    m=Image.new('L',im.size,0); ImageDraw.Draw(m).rounded_rectangle((0,0,im.width-1,im.height-1),r,fill=255); o=Image.new('RGBA',im.size); o.paste(im,(0,0),m); return o
def build(table,aerial,up,out,labels=('Table view','Aerial','Up close')):
    W,H=1080,1350; bg=Image.new('RGB',(W,H),'#fbe3ea'); d=ImageDraw.Draw(bg)
    cap=ImageFont.truetype(R+'assets/fonts/Caprasimo.ttf',78); pf=ImageFont.truetype(R+'assets/fonts/playfair-display-latin-700-italic.woff2',84)
    parts=[('Find ',cap),('Your ',pf),('Mat-ch',cap)]; x=(W-sum(d.textlength(t,font=f) for t,f in parts))/2-12; y=92
    for t,f in parts: d.text((x,y),t,font=f,fill='#062a55',anchor='lm'); x+=d.textlength(t,font=f)
    d.text((x+2,y-28),'™',font=ImageFont.truetype(R+'assets/fonts/Caprasimo.ttf',28),fill='#062a55',anchor='lm')
    d.text((W//2,162),'Your tiles on every mat, every way you want to see them',font=ImageFont.truetype(R+'assets/fonts/playfair-display-latin-400-italic.woff2',34),fill='#d6336c',anchor='mm')
    lab=ImageFont.truetype(R+'assets/fonts/poppins-latin-600-normal.woff2',24); small=ImageFont.truetype(R+'assets/fonts/poppins-latin-500-normal.woff2',22)
    def panel(img,x,y,w,label):
        t=img.resize((w,int(img.height*w/img.width)),Image.LANCZOS); t=rounded(t,26)
        sh=Image.new('RGBA',(t.width+40,t.height+40),(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle((20,24,t.width+20,t.height+22),26,fill=(60,20,60,60)); sh=sh.filter(ImageFilter.GaussianBlur(10))
        bg.paste(sh,(x-20,y-20),sh); bg.paste(t,(x,y),t)
        tw=d.textlength(label,font=lab); d.rounded_rectangle((x+14,y-22,x+14+tw+36,y+22),22,fill='#062a55'); d.text((x+32+tw/2,y),label,font=lab,fill='white',anchor='mm')
        return t.height
    h1=panel(crop(table[0],"t"),40,215,440,labels[0]); panel(crop(aerial[0],"t"),40,215+h1+48,440,labels[1])
    h3=panel(crop(up[0],"up"),520,215,520,labels[2])
    ty=215+h3+70
    for i,line in enumerate(['Pick your tiles. Swipe through mats','from 40+ brands. Save your match','card. Free, at mahjmatchmaker.com']):
        d.text((780,ty+i*36),line,font=small,fill='#062a55',anchor='mm')
    bg.save(out,quality=92)
O={'A':(('amara/raw/1-1-table-songbird.png',),('sunday/raw/1-2-aerial-whitelotus.png',),('malachite/raw/2-3-upclose-darjeeling.png',)),
   'B':(('papaya/raw/1-1-table-greenly.png',),('amara/raw/3-2-aerial-lorelei.png',),('sunday/raw/1-3-upclose-whitelotus.png',)),
   'C':(('sunday/raw/2-1-table-poloclub.png',),('papaya/raw/2-2-aerial-heiress.png',),('amara/raw/1-3-upclose-songbird.png',))}
for k,(a,b,c) in O.items(): build(a,b,c,f'option-{k}.jpg')
