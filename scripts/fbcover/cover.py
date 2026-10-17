"""Oct 17: Facebook group cover 1640x856. Center: brand logo + tagline (from the share image).
Sides: fans of real album covers (crop-safe: key content stays in the middle 1000px)."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H=1640,856
share=Image.open('assets/brand/share-wide-1200x630-v2.png').convert('RGB')
bg=share.getpixel((200,520))
im=Image.new('RGB',(W,H),bg)
C='assets/covers/albums/w800/'
L=['00-coquette-mahjong-tiles-cover.jpg','00-pippa-mahjong-tiles-cover.jpg','24-lagoon-mahjong-tiles-cover.jpg']
R=['00-smith-mahjong-tiles-cover.jpg','02-nantucket-mahjong-tiles-cover.jpg','00-talulah-mahjong-tiles-cover.jpg']
def card(f,w=250):
    c=Image.open(C+f).convert('RGB').resize((w,int(w*1.25)))
    m=Image.new('L',c.size,0); ImageDraw.Draw(m).rounded_rectangle([0,0,c.width-1,c.height-1],18,fill=255)
    out=Image.new('RGBA',c.size); out.paste(c,(0,0),m); return out
def place(f,cx,cy,ang):
    c=card(f).rotate(ang,expand=True,resample=Image.BICUBIC)
    sh=Image.new('RGBA',c.size,(0,0,0,0)); a=c.split()[3].point(lambda v:int(v*.28)); sh.putalpha(a)
    sh=Image.composite(Image.new('RGBA',c.size,(60,30,40,255)),sh,Image.new('L',c.size,0)) if False else Image.merge('RGBA',(Image.new('L',c.size,60),Image.new('L',c.size,30),Image.new('L',c.size,40),a)).filter(ImageFilter.GaussianBlur(12))
    x,y=int(cx-c.width/2),int(cy-c.height/2)
    im.paste(c,(x,y),c)
for (f,cx,cy,a) in zip(L,[175,330,215],[250,470,610],[10,-7,5]): place(f,cx,cy,a)
for (f,cx,cy,a) in zip(R,[1465,1310,1425],[250,470,610],[-10,7,-5]): place(f,cx,cy,a)
logo=share.crop((360,80,900,490))
m=Image.new('L',logo.size,0)
import numpy as np
arr=np.asarray(logo).astype(int); d=np.abs(arr-np.array(bg)).sum(2); m=Image.fromarray(((d>24)*255).astype('uint8')).filter(ImageFilter.GaussianBlur(.6))
logo=logo.resize((int(logo.width*.95),int(logo.height*.95)),Image.LANCZOS); m=m.resize(logo.size,Image.LANCZOS)
im.paste(logo,(W//2-logo.width//2+10,150),m)
bar=share.crop((285,506,915,551)).resize((int(630*.92),int(45*.92)),Image.LANCZOS)
im.paste(bar,(W//2-bar.width//2,150+logo.height+18))
dr=ImageDraw.Draw(im); f=ImageFont.truetype('/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf',30)
navy=share.getpixel((470,330))
dr.text((W//2,150+logo.height+18+bar.height+48),'mahjmatchmaker.com',font=f,fill=(24,64,128),anchor='mm')
im.save('assets/brand/fb-group-cover-1640x856.jpg',quality=92); print(navy)
