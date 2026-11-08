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
# Nov 6 (Tiffany, Juniper round 3: "Forest Green Jade sits where the colour isn't shown"): a hue/saturation wheel only shows
# bright colours, so a DARK colour lands on a bright patch. VALUE wheel: hue around, LIGHTNESS outward (center = near white,
# middle ring = full clear colour, outer ring = dark), so every pin sits on a patch of its own colour, light or dark.
# Used automatically when a set has a dark colour (needs_value); sets without one (Papaya Spritz) keep the classic wheel.
VL0, VL1, VS = 0.97, 0.12, 0.85   # lightness at the center / at the rim, saturation of the painted wheel
def _hsl(hh, ss, ll):
    c = (1 - abs(2 * ll - 1)) * ss; hp = hh * 6; x = c * (1 - abs(hp % 2 - 1)); m = ll - c / 2
    i = np.floor(hp).astype(int) % 6; z = 0 * hh
    r = np.choose(i, [c, x, z, z, x, c]); g = np.choose(i, [x, c, c, x, z, z]); b = np.choose(i, [z, z, x, c, c, x])
    return r + m, g + m, b + m
def wheel_value(size=1200):
    y, x = np.mgrid[0:size, 0:size]; c = size / 2; dx = x - c; dy = y - c
    r = np.sqrt(dx * dx + dy * dy) / c; h = (np.degrees(np.arctan2(dy, dx)) + 90) % 360 / 360
    ll = VL0 - np.clip(r, 0, 1) * (VL0 - VL1)
    R_, G_, B_ = _hsl(h, VS + 0 * h, ll); img = (np.stack([R_, G_, B_], 2).clip(0, 1) * 255).astype(np.uint8)
    im = Image.fromarray(img).convert('RGBA'); im.putalpha(Image.fromarray(((r <= 1) * 255).astype(np.uint8))); return im
def light(hexc):
    hexc = hexc.lstrip('#'); v = [int(hexc[k:k + 2], 16) / 255 for k in (0, 2, 4)]; return (max(v) + min(v)) / 2
def needs_value(pins): return any(light(p['hex']) < 0.35 for p in pins)
def pin_r(hexc, sat, value):
    """distance from the center as a share of the radius: saturation (classic) or 1 - lightness (value wheel)"""
    return min(1.0, max(0.0, (VL0 - light(hexc)) / (VL0 - VL1))) if value else sat
def main(key, pins, title, sub, note=None, value=False):
    W,H=1080,1350; bg=Image.new('RGB',(W,H),(246,233,223)); d=ImageDraw.Draw(bg)
    many=len(pins)>3; ws=600 if many else 660; wl=wheel_value(ws) if value else wheel(ws, v=0.97); cx,cy=W//2,(530 if many else 575)
    # soften: blend wheel toward cream a touch so it reads designer, not neon
    cream=Image.new('RGBA',(ws,ws),(246,233,223,255)); wl=Image.composite(Image.blend(wl,cream,0.18),wl.copy(),wl.split()[3])
    sh=Image.new('RGBA',(ws+40,ws+40),(0,0,0,0)); ImageDraw.Draw(sh).ellipse([20,28,ws+20,ws+28],fill=(120,60,30,45))
    bg.paste(sh,(cx-ws//2-20,cy-ws//2-20),sh); bg.paste(wl,(cx-ws//2,cy-ws//2),wl)
    d.ellipse([cx-ws//2,cy-ws//2,cx+ws//2,cy+ws//2],outline=(255,255,255),width=8)
    lab=ImageFont.truetype(TF+'Caprasimo.ttf',74); small=ImageFont.truetype(GF+'Lora-Variable.ttf',30)
    mono=ImageFont.truetype(GF+'Lora-Variable.ttf',24); num=ImageFont.truetype(TF+'bitter-latin-700-normal.woff2',30) if False else ImageFont.truetype(GF+'Lora-Variable.ttf',30)
    chipname=ImageFont.truetype(GF+'Lora-Variable.ttf',30); chipsm=ImageFont.truetype(GF+'Lora-Variable.ttf',23)
    d.text((W/2,92),title,font=lab,fill=(5,70,137),anchor='mm'); d.text((W/2,158),sub,font=small,fill=(90,107,133),anchor='mm')
    for deg,name in [(0,'red'),(30,'orange'),(60,'yellow'),(120,'green'),(180,'teal'),(240,'blue'),(275,'lavender'),(320,'pink')]:
        aa=math.radians(deg-90); x=cx+(ws/2+40)*math.cos(aa); y=cy+(ws/2+40)*math.sin(aa)
        d.text((x,y),name,font=mono,fill=(90,107,133),anchor='mm')
    n=len(pins)
    if n>3: return _rest_many(bg,d,key,pins,cx,cy,ws,mono,num,chipname,chipsm,note,value)
    cw=280; gap=40; x0=(W-(n*cw+(n-1)*gap))/2; cyc=975
    for i,p in enumerate(pins):
        hexc=p['hex'].lstrip('#'); r,g,b=[int(hexc[k:k+2],16)/255 for k in (0,2,4)]; h,sat,v=colorsys.rgb_to_hsv(r,g,b)
        col=(int(r*255),int(g*255),int(b*255))
        aa=math.radians(h*360-90); rr=pin_r(hexc,sat,value)*(ws/2-6); px=cx+rr*math.cos(aa); py=cy+rr*math.sin(aa)
        d.ellipse([px-34,py-34,px+34,py+34],fill=col,outline=(255,255,255),width=7)
        d.ellipse([px-40,py-40,px+40,py+40],outline=(5,70,137),width=3)
        d.text((px,py),str(i+1),font=num,fill=(255,255,255),anchor='mm')
        # designer color chip below
        x=x0+i*(cw+gap)
        d.rounded_rectangle([x+6,cyc+10,x+cw+6,cyc+250],18,fill=(220,200,185))
        d.rounded_rectangle([x,cyc,x+cw,cyc+240],18,fill=(255,255,255))
        d.rounded_rectangle([x,cyc,x+cw,cyc+150],18,fill=col); d.rectangle([x,cyc+130,x+cw,cyc+150],fill=col)
        d.ellipse([x+14,cyc+14,x+54,cyc+54],fill=(255,255,255)); d.text((x+34,cyc+34),str(i+1),font=mono,fill=(5,70,137),anchor='mm')
        d.text((x+18,cyc+188),p['name'],font=chipname,fill=(5,70,137),anchor='ls')
        d.text((x+18,cyc+222),f"#{hexc.upper()} · {round(h*360)}°",font=chipsm,fill=(90,107,133),anchor='ls')
    d.text((W/2,H-88),'Sampled from Oh My Mahjong’s tile back photo. Angle = hue · distance from center = how vivid.',font=mono,fill=(90,107,133),anchor='mm')
    logo=Image.open(R+'assets/brand/mahjmatchmaker-wordmark-notag.png').convert('RGBA'); logo.thumbnail((260,80)); bg.paste(logo,(W//2-logo.width//2,H-62),logo)
    out=R+f'assets/colorwheels/{key}-color-wheel.jpg'; bg.save(out,quality=93); print(out)
def _rest_many(bg,d,key,pins,cx,cy,ws,mono,num,chipname,chipsm,note,value=False):
    """Nov 6 (Juniper): more than 3 pins -> two rows of 3 smaller chips (backs row, faces row). Papaya (3 pins) unchanged."""
    W,H=bg.size
    for i,p in enumerate(pins):
        hexc=p['hex'].lstrip('#'); r,g,b=[int(hexc[k:k+2],16)/255 for k in (0,2,4)]; h,sat,v=colorsys.rgb_to_hsv(r,g,b)
        col=(int(r*255),int(g*255),int(b*255))
        aa=math.radians(h*360-90); rr=pin_r(hexc,sat,value)*(ws/2-6); px=cx+rr*math.cos(aa); py=cy+rr*math.sin(aa)
        d.ellipse([px-30,py-30,px+30,py+30],fill=col,outline=(255,255,255),width=6)
        d.ellipse([px-36,py-36,px+36,py+36],outline=(5,70,137),width=3)
        d.text((px,py),str(i+1),font=num,fill=(255,255,255),anchor='mm')
    cw=300; gap=24; ch=108
    rows=[pins[:3],pins[3:6]]; ylab=[922,1088]; labs=['BACKS & LAYERS','FACES']
    k=0
    for ri,row in enumerate(rows):
        n=len(row); x0=(W-(n*cw+(n-1)*gap))/2; y=ylab[ri]+22
        d.text((W/2,ylab[ri]),labs[ri],font=chipsm,fill=(5,70,137),anchor='mm')
        for j,p in enumerate(row):
            k+=1; hexc=p['hex'].lstrip('#'); r,g,b=[int(hexc[q:q+2],16) for q in (0,2,4)]; h=colorsys.rgb_to_hsv(r/255,g/255,b/255)[0]
            x=x0+j*(cw+gap)
            d.rounded_rectangle([x+5,y+8,x+cw+5,y+ch+8],16,fill=(220,200,185))
            d.rounded_rectangle([x,y,x+cw,y+ch],16,fill=(255,255,255))
            d.rounded_rectangle([x,y,x+64,y+ch],16,fill=(r,g,b)); d.rectangle([x+40,y,x+64,y+ch],fill=(r,g,b))
            d.text((x+32,y+ch/2),str(k),font=mono,fill=(255,255,255),anchor='mm')
            nm=p['name']; f=chipname
            while d.textlength(nm,font=f)>cw-88 and f.size>18: f=ImageFont.truetype(GF+'Lora-Variable.ttf',f.size-1)
            d.text((x+80,y+52),nm,font=f,fill=(5,70,137),anchor='ls')
            d.text((x+80,y+88),f"#{hexc.upper()} · {round(h*360)}°",font=chipsm,fill=(90,107,133),anchor='ls')
    d.text((W/2,H-92),note or 'Angle = hue · distance from center = how vivid.',font=mono,fill=(90,107,133),anchor='mm')
    logo=Image.open(R+'assets/brand/mahjmatchmaker-wordmark-notag.png').convert('RGBA'); logo.thumbnail((260,80)); bg.paste(logo,(W//2-logo.width//2,H-62),logo)
    out=R+f'assets/colorwheels/{key}-color-wheel.jpg'; bg.save(out,quality=93); print(out)

# Nov 6: per-set pins. papaya-spritz = the original 3 (unchanged). Others: config/colorcards.json backs + the faces listed here.
WHEEL_FACES={'juniper':['HOT PINK','CORAL','GOLD'],'style-of-your-life':['INDIGO','WINE','BUBBLEGUM PINK'],
            'deco-lagoon':['MULBERRY','ROSE','NAVY'],'deco-mulberry':['TEAL','ROSE','NAVY'],'deco-indigo':['MULBERRY','TEAL','ROSE']}  # Nov 7 Bam Bird Deco
# Nov 7: the legend is 3 + 3, so a set with 2 back colours names its third layer here (MFM: 'a pearl green back, a deep green middle layer, and a white face').
WHEEL_EXTRA_BACKS={'style-of-your-life':[{'name':'White Face','hex':'#f4f1ec'}]}
WHEEL_TITLE={'papaya-spritz':('Papaya Spritz','where her colors sit on the color wheel')}
if __name__=='__main__':
    key=sys.argv[1] if len(sys.argv)>1 else 'papaya-spritz'
    if key=='papaya-spritz':
        pins=[{'name':'Papaya backs','hex':'#de7e30'},
              {'name':'Lavender layer','hex':'#a8a3e1'},
              {'name':'Light lime layer','hex':'#c8d7a5'}]
        main('papaya-spritz',pins,'Papaya Spritz','where her colors sit on the color wheel')
    else:
        cc=json.load(open(R+'config/colorcards.json'))['sets'][key]
        pins=[{'name':n.title(),'hex':h} for n,h,_ in cc['backs']]+WHEEL_EXTRA_BACKS.get(key,[])
        fx=dict((n,h) for n,h in cc['faces'])
        pins+=[{'name':n.title(),'hex':fx[n]} for n in WHEEL_FACES.get(key,[])]
        t,sub=WHEEL_TITLE.get(key,(cc['name'],'where her colors sit on the color wheel'))
        vv=needs_value(pins)
        main(key,pins,t,sub,value=vv,note=(f"From {cc['brand']}'s photos. Angle = hue · center = light, outer ring = dark." if vv else f"From {cc['brand']}'s photos. Angle = hue · farther out = more vivid."))

def mini(key, pins, ws=900, value=False):
    """Small transparent color wheel with numbered pins only (for the merged Her colors slide). value=True: the light/dark wheel."""
    import math, colorsys
    pad=60; S=ws+2*pad; im=Image.new('RGBA',(S,S),(0,0,0,0)); d=ImageDraw.Draw(im)
    wl=wheel_value(ws) if value else wheel(ws, v=0.97); cream=Image.new('RGBA',(ws,ws),(246,233,223,255)); wl=Image.composite(Image.blend(wl,cream,0.18),wl.copy(),wl.split()[3])
    sh=Image.new('RGBA',(S,S),(0,0,0,0)); ImageDraw.Draw(sh).ellipse([pad,pad+10,pad+ws,pad+ws+10],fill=(120,60,30,45))
    from PIL import ImageFilter; im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8))); im.alpha_composite(wl,(pad,pad))
    d.ellipse([pad,pad,pad+ws,pad+ws],outline=(255,255,255),width=12)
    num=ImageFont.truetype(GF+'Lora-Variable.ttf',44); cx=cy=S/2
    for i,p in enumerate(pins):
        hexc=p['hex'].lstrip('#'); r,g,b=[int(hexc[k:k+2],16)/255 for k in (0,2,4)]; h,sat,v=colorsys.rgb_to_hsv(r,g,b)
        aa=math.radians(h*360-90); rr=pin_r(hexc,sat,value)*(ws/2-8); px=cx+rr*math.cos(aa); py=cy+rr*math.sin(aa)
        d.ellipse([px-50,py-50,px+50,py+50],fill=(int(r*255),int(g*255),int(b*255)),outline=(255,255,255),width=10)
        d.ellipse([px-58,py-58,px+58,py+58],outline=(5,70,137),width=4)
        d.text((px,py),str(i+1),font=num,fill=(255,255,255),anchor='mm')
    out=R+f'assets/colorwheels/{key}-color-wheel-mini.png'; im.save(out); return out
