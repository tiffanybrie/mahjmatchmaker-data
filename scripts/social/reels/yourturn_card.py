"""'It's your turn to be the matchmaker' reel card: 3x3 grid of FYM table mats + stats + Comment MATCH.
usage: yourturn_card.py out.png raw1.png ... raw9.png  (FYM table raws, 1170 wide)"""
import sys
from PIL import Image,ImageDraw,ImageFont,ImageFilter
R='/home/claude/mahjmatchmaker-data/'
out=sys.argv[1]; raws=sys.argv[2:11]
im=Image.new('RGB',(1080,1920),(250,240,235)); d=ImageDraw.Draw(im)
cap=lambda s:ImageFont.truetype(R+'assets/fonts/CaprasimoMM.ttf',s)
def mont(w,s):
    f=ImageFont.truetype('/usr/share/fonts/truetype/google-fonts/ofl/montserrat/Montserrat[wght].ttf',s); f.set_variation_by_name(w); return f
NAVY=(5,70,137); PINK=(214,47,104)
def ctr(t,f,y,c):
    w=d.textlength(t,font=f); d.text(((1080-w)/2,y),t,font=f,fill=c)
ctr("It's your turn to be",cap(72),236,NAVY); ctr("the matchmaker",cap(100),326,PINK)
S=304; g=22; x0=(1080-(3*S+2*g))//2; y0=520
for i,p in enumerate(raws):
    r=Image.open(p).convert('RGB').crop((60,262,1110,1312)).resize((S,S),Image.LANCZOS)
    m=Image.new('L',(S,S),0); ImageDraw.Draw(m).rounded_rectangle((0,0,S,S),28,fill=255)
    x=x0+(i%3)*(S+g); y=y0+(i//3)*(S+g)
    sh=Image.new('L',(S+40,S+40),0); ImageDraw.Draw(sh).rounded_rectangle((20,24,S+20,S+24),28,fill=70); sh=sh.filter(ImageFilter.GaussianBlur(10))
    im.paste((180,150,150),(x-20,y-20),sh); im.paste(r,(x,y),m)
yb=y0+3*S+2*g
ctr("1,500+ mats  ·  250+ racks",mont('Bold',52),yb+44,NAVY)
f2=mont('Bold',46); t="Comment MATCH for the link"; w=d.textlength(t,font=f2); x=(1080-w)/2; y=yb+150
d.rounded_rectangle((x-44,y-24,x+w+44,y+76),radius=50,fill=PINK); d.text((x,y),t,font=f2,fill='white')
im.save(out)
