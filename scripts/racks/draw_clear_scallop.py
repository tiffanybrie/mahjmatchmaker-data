"""Our own drawn illustration of a clear acrylic rack with a scalloped pusher (Oct 20). Not traced from any
brand photo: built from shapes in the same front-on 1400x255 format as assets/racks/card/*.png.
Used for 'Mahj Mood Scalloped Clear Acrylic' on match cards (Tiffany: link the $100 Mahj Mood set)."""
from PIL import Image, ImageDraw, ImageFilter
W,H=1400,255; S=2
w,h=W*S,H*S
def layer(): return Image.new('RGBA',(w,h),(0,0,0,0))
out=layer()
# scalloped pusher (back): 13 half-discs on a strip
p=layer(); d=ImageDraw.Draw(p)
n=13; x0,x1=30*S,(W-30)*S; step=(x1-x0)/n; r=step/2
for i in range(n):
    cx=x0+r+i*step; d.pieslice((cx-r+2*S,10*S,cx+r-2*S,10*S+2*r),180,360,fill=(236,244,250,140)); d.arc((cx-r+2*S,10*S,cx+r-2*S,10*S+2*r),180,360,fill=(255,255,255,240),width=3*S)
d.rectangle((x0,10*S+r,x1,75*S),fill=(236,244,250,140))
out.alpha_composite(p)
# rack front face
f=layer(); d=ImageDraw.Draw(f)
d.rounded_rectangle((14*S,60*S,(W-14)*S,215*S),radius=6*S,fill=(228,238,246,150),outline=(255,255,255,240),width=4*S)
# inner face edge + top bevel highlight
d.line((20*S,74*S,(W-20)*S,74*S),fill=(255,255,255,230),width=5*S)
d.line((20*S,200*S,(W-20)*S,200*S),fill=(190,210,225,170),width=3*S)
out.alpha_composite(f)
# base lip
b=layer(); d=ImageDraw.Draw(b)
d.rounded_rectangle((0,212*S,W*S,250*S),radius=5*S,fill=(222,234,244,160),outline=(255,255,255,230),width=3*S)
out.alpha_composite(b)
# soft glints
g=layer(); d=ImageDraw.Draw(g)
for gx in (160,520,880,1220):
    d.polygon([(gx*S,80*S),((gx+60)*S,80*S),((gx+10)*S,195*S),((gx-50)*S,195*S)],fill=(255,255,255,70))
out.alpha_composite(g.filter(ImageFilter.GaussianBlur(6*S)))
# subtle edge shadow so it reads on light mats
sh=out.split()[3].filter(ImageFilter.GaussianBlur(3*S)).point(lambda v:int(v*0.35))
base=Image.new('RGBA',(w,h),(60,80,100,0)); base.putalpha(sh)
final=layer(); final.alpha_composite(base,(0,2*S)); final.alpha_composite(out)
final=final.resize((W,H),Image.LANCZOS)
final.save('assets/racks/card/mahj-mood-scalloped-clear-acrylic-drawn.png'); print('ok')
