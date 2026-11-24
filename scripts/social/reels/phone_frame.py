"""Put an FYM phone raw (1170x2532) into the reel phone template with a ONE-colour headline.
usage: phone_frame.py template.png raw.png out.png "line 1" "line 2"   ("Your" in line text is set in Playfair italic)"""
import sys
from PIL import Image,ImageDraw,ImageFont
R='/home/claude/mahjmatchmaker-data/'
tpl,raw,out,l1,l2=sys.argv[1:6]
im=Image.open(tpl).convert('RGB'); bg=im.crop((0,262,1080,263)).resize((1080,440-262))
im.paste(bg,(0,262)); d=ImageDraw.Draw(im)
NAVY=(5,70,137); cap=ImageFont.truetype(R+'assets/fonts/CaprasimoMM.ttf',72); it=ImageFont.truetype('/tmp/PlayfairBI.ttf',80)
def line(t,y):
    parts=t.split('Your'); segs=[]
    for i,pt in enumerate(parts):
        if pt: segs.append((pt,cap,0))
        if i<len(parts)-1: segs.append(('Your',it,-6))
    W=sum(d.textlength(s,font=f) for s,f,_ in segs)+ (8*(len(segs)-1))
    x=(1080-W)/2
    for s,f,dy in segs:
        d.text((x,y+dy),s,font=f,fill=NAVY); x+=d.textlength(s,font=f)+8
line(l1,282); line(l2,362)
r=Image.open(raw).convert('RGB'); w=758; r=r.resize((w,int(r.height*w/r.width)),Image.LANCZOS)
im.paste(r.crop((0,0,w,1310)),(161,610)); im.save(out)
