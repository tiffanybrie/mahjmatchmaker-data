"""Side-by-side: C (color wheel ring seal) vs 2 (full pastel wheel, navy flame), both with the real flame-heart."""
import sys; sys.path.insert(0,'/home/claude/mahjmatchmaker-data/scripts/brand')
from seal_full import *
def ring(S=900,kind='pastel',inner=(251,246,239,255)):
    w=wheel(S,kind); m=Image.new('L',(S*4,S*4),0); d=ImageDraw.Draw(m); pad=int(S*4*0.075)
    d.ellipse((pad,pad,S*4-1-pad,S*4-1-pad),fill=255); m=m.resize((S,S),Image.LANCZOS)
    w.paste(Image.new('RGBA',(S,S),inner),(0,0),m)
    lg=logo(int(S*0.46),(5,70,137,255),(245,108,140,255)); w.alpha_composite(lg,((S-lg.width)//2,(S-lg.height)//2+int(S*0.01))); return w
c=ring(); c.save(R+'assets/brand/seal/seal-C-ring-pastel.png')
two=seal('pastel','navy')
T=520; sheet=Image.new('RGB',(2*T+3*60,T+170),(246,233,223)); d=ImageDraw.Draw(sheet)
ft=ImageFont.truetype(R+'scripts/social/tileprofile/fonts/Caprasimo.ttf',34)
for i,(s,n) in enumerate([(c,'C - Color wheel ring'),(two,'2 - Full pastel wheel')]):
    x=60+i*(T+60); t=s.resize((T,T),Image.LANCZOS); sheet.paste(t,(x,50),t); d.text((x+T/2,T+100),n,font=ft,fill=(5,70,137),anchor='mm')
# small-size check row (how they read tiny, like a highlight or avatar)
sm=Image.new('RGB',(sheet.width,140),(255,255,255)); sd=ImageDraw.Draw(sm)
for i,s in enumerate([c,two]):
    for j,z in enumerate([110,64,36]):
        t=s.resize((z,z),Image.LANCZOS); x=60+i*(T+60)+j*150+60; sm.paste(t,(x,(140-z)//2),t)
out=Image.new('RGB',(sheet.width,sheet.height+140),(255,255,255)); out.paste(sheet,(0,0)); out.paste(sm,(0,sheet.height))
out.save(R+'assets/brand/seal/seal-C-vs-2.png'); print('ok')
