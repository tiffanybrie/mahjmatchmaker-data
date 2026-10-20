"""FB group cover v7 (Oct 19): v6 rainbow album collage + a big stacked-logo badge in the center so the
auto-cropped square group icon reads clearly."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
R='/home/claude/mahjmatchmaker-data/'
cov=Image.open(R+'assets/brand/fb-group-cover-v6-rainbow.jpg').convert('RGBA')   # 1640x856
W,H=cov.size; NAVY=(5,70,137); PINK=(214,96,140); CREAM=(253,248,246)
bw,bh=684,560; x0=(W-bw)//2; y0=(H-bh)//2
sh=Image.new('RGBA',cov.size,(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle((x0+6,y0+14,x0+bw+6,y0+bh+14),48,fill=(10,20,50,110)); cov.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16)))
d=ImageDraw.Draw(cov)
d.rounded_rectangle((x0,y0,x0+bw,y0+bh),48,fill=PINK)
d.rounded_rectangle((x0+10,y0+10,x0+bw-10,y0+bh-10),40,fill=CREAM)
d.rounded_rectangle((x0+22,y0+22,x0+bw-22,y0+bh-22),32,outline=NAVY,width=6)
av=Image.open(R+'assets/brand/fb-page/mahj-matchmaker-page-profile-1080.jpg').convert('RGB').crop((120,215,975,880))
# knock out the near-white background so it sits on the cream card
import numpy as np
a=np.asarray(av).astype(int); m=(a.min(axis=2)<235).astype('uint8')*255
lg=av.convert('RGBA'); lg.putalpha(Image.fromarray(m).filter(ImageFilter.GaussianBlur(0.8)))
lw=430; lg=lg.resize((lw,int(lg.height*lw/lg.width)),Image.LANCZOS)
cov.alpha_composite(lg,((W-lw)//2+10,y0+42))
fb=lambda s,w=700: ImageFont.truetype(R+'scripts/social/tileprofile/fonts/'+('bitter-latin-700-normal.woff2' if w==700 else 'bitter-latin-600-normal.woff2'),s)
try: f1=ImageFont.truetype('/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf',19)
except: f1=ImageFont.load_default()
txt='MATCHING MAHJONG TILES, MATS & RACKS'; sp=3
tw=sum(d.textlength(c,font=f1)+sp for c in txt)-sp; py=y0+bh-140
d.rounded_rectangle(((W-tw)/2-26,py,(W+tw)/2+26,py+46),23,fill=PINK)
x=(W-tw)/2
for c in txt: d.text((x,py+11),c,font=f1,fill=(255,255,255)); x+=d.textlength(c,font=f1)+sp
cap=ImageFont.truetype(R+'scripts/social/tileprofile/fonts/Caprasimo.ttf',30)
d.text((W/2,py+76),'40+ tile set albums  |  mahjmatchmaker.com',font=ImageFont.truetype(R+'scripts/social/tileprofile/fonts/Caprasimo.ttf',25),fill=NAVY,anchor='mm')
out=R+'assets/brand/fb-group-cover-v7-stacked.jpg'; cov.convert('RGB').save(out,quality=92)
# previews: desktop cover, mobile crop, and the square icon (center square, shown small)
ic=cov.crop(((W-H)//2,0,(W+H)//2,H)).convert('RGB')
pv=Image.new('RGB',(1640,856+260),(255,255,255)); pv.paste(cov.convert('RGB'),(0,0))
for i,z in enumerate([200,100,48]):
    t=ic.resize((z,z),Image.LANCZOS); m=Image.new('L',(z,z),0); ImageDraw.Draw(m).rounded_rectangle((0,0,z-1,z-1),z//6,fill=255)
    pv.paste(t,(60+i*260,856+30+(200-z)//2),m)
ImageDraw.Draw(pv).text((820,856+130),'group icon at real sizes (left)',font=cap,fill=NAVY)
dk=cov.convert('RGB').crop((0,(H-607)//2,W,(H+607)//2)).resize((820,303)); pv.paste(dk,(800,856+0)) if False else None
pv.save(R+'assets/brand/fb-group-cover-v7-preview.jpg',quality=88); print(out)
