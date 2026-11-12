"""FB group photo: everything holiday in one view (Tiffany Nov 12 10:43am: title case, show ALL of it:
11 holiday albums + holiday mats for 33 sets you own + the holiday mats in Find Your Mat-ch; moody holiday vibe)."""
from PIL import Image, ImageDraw, ImageFont
R='/home/claude/mahjmatchmaker-data/'; F=R+'scripts/social/tileprofile/fonts/'
CAP=lambda s: ImageFont.truetype(F+'Caprasimo.ttf', s); SANS=lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', s)
NAVY=(6,42,85); BLUSH=(247,182,200); WHITE=(255,255,255); PINK=(214,51,108)
W,H=1080,1350; im=Image.new('RGB',(W,H),NAVY); d=ImageDraw.Draw(im)
d.text((W/2,70),'Holiday Mahj,',font=CAP(96),fill=WHITE,anchor='ma'); d.text((W/2,172),'All Matched',font=CAP(96),fill=BLUSH,anchor='ma')
covers=['cmc-apres-ski','dear-santa','december-1994','holly-jolly-green','holly-jolly-pink','holly-jolly-red','nivalee-blue','nutcracker-ballet','rackin-rudolph','tinselle-emerald','tinselle-ruby']
cw,ch,g=242,236,12; x0=(W-4*cw-3*g)//2; y0=300
for i,c in enumerate(covers):
    t=Image.open(R+f'assets/covers/holiday/{c}.jpg').convert('RGB'); s=max(cw/t.width,ch/t.height); t=t.resize((int(t.width*s)+1,int(t.height*s)+1))
    t=t.crop(((t.width-cw)//2,(t.height-ch)//2,(t.width-cw)//2+cw,(t.height-ch)//2+ch))
    m=Image.new('L',(cw,ch),0); ImageDraw.Draw(m).rounded_rectangle([0,0,cw-1,ch-1],radius=16,fill=255)
    im.paste(t,(x0+(i%4)*(cw+g),y0+(i//4)*(ch+g)),m)
x=x0+3*(cw+g); y=y0+2*(ch+g); d.rounded_rectangle([x,y,x+cw,y+ch],radius=16,fill=WHITE)
d.text((x+cw/2,y+46),'11',font=CAP(84),fill=NAVY,anchor='ma'); d.text((x+cw/2,y+142),'Holiday Tile Set',font=CAP(25),fill=NAVY,anchor='ma'); d.text((x+cw/2,y+176),'Albums',font=CAP(25),fill=NAVY,anchor='ma')
y=y0+3*(ch+g)+20
def stat(cx,n,l1,l2):
    d.text((cx,y),n,font=CAP(76),fill=BLUSH,anchor='ma'); d.text((cx,y+92),l1,font=SANS(30),fill=WHITE,anchor='ma'); d.text((cx,y+132),l2,font=SANS(30),fill=WHITE,anchor='ma')
stat(W*0.27,'189','Holiday Mats in','Find Your Mat-ch'); stat(W*0.73,'33','Everyday Tile Sets,','Matched for the Holidays')
d.line([(W/2,y+10),(W/2,y+160)],fill=(60,90,130),width=3)
d.text((W/2,H-58),'mahjmatchmaker.com',font=SANS(36),fill=WHITE,anchor='ma')
im.save(R+'assets/social/fb-groups/holiday-all-matched.jpg',quality=90); print('ok')
