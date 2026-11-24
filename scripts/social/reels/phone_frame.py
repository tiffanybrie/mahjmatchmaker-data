"""Put an FYM phone raw (1170x2532) into the reel phone template with a ONE-colour headline.
Phone is scaled up 1.2x and pushed up (top ~360) under a headline that starts at the 180px safe line.
usage: phone_frame.py template.png raw.png out.png "line 1" "line 2"   ("Your" is set in Playfair italic)"""
import sys
from PIL import Image,ImageDraw,ImageFont
R='/home/claude/mahjmatchmaker-data/'
tpl,raw,out,l1,l2=sys.argv[1:6]
K=1.2; TOP=356
t=Image.open(tpl).convert('RGB')
r=Image.open(raw).convert('RGB'); w=758; r=r.resize((w,int(r.height*w/r.width)),Image.LANCZOS)
t.paste(r.crop((0,0,w,1310)),(161,610))
ph=t.crop((0,452,1080,1920)); ph=ph.resize((int(1080*K),int(ph.height*K)),Image.LANCZOS)
x0=(ph.width-1080)//2; ph=ph.crop((x0,0,x0+1080,min(ph.height,1920-TOP)))
bgrow=t.crop((0,262,1080,263))
im=bgrow.resize((1080,1920))
# vertical gradient like template
top=t.crop((0,0,1080,452)).resize((1080,TOP)); im.paste(top,(0,0))
im.paste(ph,(0,TOP))
# sharp screen: paste the raw again at full scale (not upscaled from 758)
W2=int(round(758*K)); r2=Image.open(raw).convert('RGB'); r2=r2.resize((W2,int(r2.height*W2/r2.width)),Image.LANCZOS)
sx=int(round(161*K))-x0; sy=TOP+int(round((610-452)*K)); im.paste(r2.crop((0,0,W2,min(r2.height,1920-sy))),(sx,sy))
d=ImageDraw.Draw(im)
NAVY=(5,70,137); cap=ImageFont.truetype(R+'assets/fonts/CaprasimoMM.ttf',74); it=ImageFont.truetype('/tmp/PlayfairBI.ttf',82)
def line(tx,y):
    parts=tx.split('Your'); segs=[]
    for i,pt in enumerate(parts):
        if pt: segs.append((pt,cap,0))
        if i<len(parts)-1: segs.append(('Your',it,-6))
    W=sum(d.textlength(s,font=f) for s,f,_ in segs)+8*(len(segs)-1); x=(1080-W)/2
    for s,f,dy in segs:
        d.text((x,y+dy),s,font=f,fill=NAVY); x+=d.textlength(s,font=f)+8
# clean headline area
d.rectangle((0,170,1080,TOP-8),fill=t.getpixel((20,300)))
line(l1,186); line(l2,266)
im.save(out)
