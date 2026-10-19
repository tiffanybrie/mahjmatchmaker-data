"""Tile set color wheel (Oct 19): a filled color wheel (hue around, saturation outward) with pins showing where
each measured tile color sits. Usage: python3 wheel.py <set-key>  (reads config/colorcards.json backs; measures from photos if given)."""
import sys, json, math, colorsys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
R='/home/claude/mahjmatchmaker-data/'
GF='/usr/share/fonts/truetype/google-fonts/'; TF=R+'scripts/social/tileprofile/fonts/'
def wheel(size=1200, v=0.96):
    y,x=np.mgrid[0:size,0:size]; c=size/2; dx=x-c; dy=y-c
    r=np.sqrt(dx*dx+dy*dy)/c; h=(np.degrees(np.arctan2(dy,dx))+90)%360/360
    s=np.clip(r,0,1); rgb=np.zeros((size,size,3))
    import colorsys as cs
    hh=h.ravel(); ss=s.ravel()
    # vectorized hsv->rgb
    i=np.floor(hh*6).astype(int)%6; f=hh*6-np.floor(hh*6); p=v*(1-ss); q=v*(1-f*ss); t=v*(1-(1-f)*ss)
    out=np.stack([np.choose(i,[v+0*ss,q,p,p,t,v+0*ss]),np.choose(i,[t,v+0*ss,v+0*ss,q,p,p]),np.choose(i,[p,p,t,v+0*ss,v+0*ss,q])],1)
    img=(out.reshape(size,size,3)*255).astype(np.uint8)
    a=(r<=1).astype(np.uint8)*255
    im=Image.fromarray(img).convert('RGBA'); im.putalpha(Image.fromarray(a)); return im
def main(key, pins, title, sub):
    W,H=1080,1350; bg=Image.new('RGB',(W,H),(246,233,223)); d=ImageDraw.Draw(bg)
    ws=660; wl=wheel(ws, v=0.97); cx,cy=W//2,575
    # soften: blend wheel toward cream a touch so it reads designer, not neon
    cream=Image.new('RGBA',(ws,ws),(246,233,223,255)); wl=Image.composite(Image.blend(wl,cream,0.18),wl.copy(),wl.split()[3])
    sh=Image.new('RGBA',(ws+40,ws+40),(0,0,0,0)); ImageDraw.Draw(sh).ellipse([20,28,ws+20,ws+28],fill=(120,60,30,45))
    bg.paste(sh,(cx-ws//2-20,cy-ws//2-20),sh); bg.paste(wl,(cx-ws//2,cy-ws//2),wl)
    d.ellipse([cx-ws//2,cy-ws//2,cx+ws//2,cy+ws//2],outline=(255,255,255),width=8)
    lab=ImageFont.truetype(TF+'Caprasimo.ttf',74); small=ImageFont.truetype(GF+'Lora-Variable.ttf',30)
    mono=ImageFont.truetype(GF+'Lora-Variable.ttf',24); num=ImageFont.truetype(TF+'bitter-latin-700-normal.woff2',30) if False else ImageFont.truetype(GF+'Lora-Variable.ttf',30)
    chipname=ImageFont.truetype(GF+'Lora-Variable.ttf',30); chipsm=ImageFont.truetype(GF+'Lora-Variable.ttf',23)
    d.text((W/2,92),title,font=lab,fill=(6,42,85),anchor='mm'); d.text((W/2,158),sub,font=small,fill=(90,107,133),anchor='mm')
    for deg,name in [(0,'red'),(30,'orange'),(60,'yellow'),(120,'green'),(180,'teal'),(240,'blue'),(275,'lavender'),(320,'pink')]:
        aa=math.radians(deg-90); x=cx+(ws/2+40)*math.cos(aa); y=cy+(ws/2+40)*math.sin(aa)
        d.text((x,y),name,font=mono,fill=(90,107,133),anchor='mm')
    n=len(pins); cw=280; gap=40; x0=(W-(n*cw+(n-1)*gap))/2; cyc=975
    for i,p in enumerate(pins):
        hexc=p['hex'].lstrip('#'); r,g,b=[int(hexc[k:k+2],16)/255 for k in (0,2,4)]; h,sat,v=colorsys.rgb_to_hsv(r,g,b)
        col=(int(r*255),int(g*255),int(b*255))
        aa=math.radians(h*360-90); rr=sat*(ws/2-6); px=cx+rr*math.cos(aa); py=cy+rr*math.sin(aa)
        d.ellipse([px-34,py-34,px+34,py+34],fill=col,outline=(255,255,255),width=7)
        d.ellipse([px-40,py-40,px+40,py+40],outline=(6,42,85),width=3)
        d.text((px,py),str(i+1),font=num,fill=(255,255,255),anchor='mm')
        # designer color chip below
        x=x0+i*(cw+gap)
        d.rounded_rectangle([x+6,cyc+10,x+cw+6,cyc+250],18,fill=(220,200,185))
        d.rounded_rectangle([x,cyc,x+cw,cyc+240],18,fill=(255,255,255))
        d.rounded_rectangle([x,cyc,x+cw,cyc+150],18,fill=col); d.rectangle([x,cyc+130,x+cw,cyc+150],fill=col)
        d.ellipse([x+14,cyc+14,x+54,cyc+54],fill=(255,255,255)); d.text((x+34,cyc+34),str(i+1),font=mono,fill=(6,42,85),anchor='mm')
        d.text((x+18,cyc+188),p['name'],font=chipname,fill=(6,42,85),anchor='ls')
        d.text((x+18,cyc+222),f"#{hexc.upper()} · {round(h*360)}°",font=chipsm,fill=(90,107,133),anchor='ls')
    d.text((W/2,H-88),'Sampled from Oh My Mahjong’s tile back photo. Angle = hue · distance from center = how vivid.',font=mono,fill=(90,107,133),anchor='mm')
    logo=Image.open(R+'assets/brand/mahjmatchmaker-wordmark-notag.png').convert('RGBA'); logo.thumbnail((260,80)); bg.paste(logo,(W//2-logo.width//2,H-62),logo)
    out=R+f'assets/colorwheels/{key}-color-wheel.jpg'; bg.save(out,quality=93); print(out)
if __name__=='__main__':
    pins=[{'name':'Papaya backs','hex':'#de7e30'},
          {'name':'Lavender layer','hex':'#a8a3e1'},
          {'name':'Light lime layer','hex':'#c8d7a5'}]
    main('papaya-spritz',pins,'Papaya Spritz','where her colors sit on the color wheel')
