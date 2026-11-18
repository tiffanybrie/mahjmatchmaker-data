# Dear Santa reel v4: same reel as v3, end card filled with a wall of the matched mats (Tiffany Nov 17 noon: "fill up that last frame a little better").
import json, subprocess, os
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageFilter
R='/home/claude/tiffanybrie/mahjmatchmaker-data/'
D=R+'assets/social/dear-santa-push/'
FD=R+'scripts/social/tileprofile/fonts/'
CAP=FD+'Caprasimo.ttf'; BIT=R+'scripts/albumcard/woodfix/Bitter-Bold.ttf'; PF=FD+'playfair-display-latin-600-italic.woff2'; PF4=FD+'playfair-display-latin-400-italic.woff2'
CREAM=(246,234,224); GREEN=(15,72,42); RED=(179,32,42); INK=(70,52,40)
W,H=1080,1920
cfg=json.load(open(D+'reel-config.json'))
def trim(im):
    rgb=im.convert('RGB'); bg=Image.new('RGB',rgb.size,(255,255,255))
    diff=ImageChops.difference(rgb,bg).convert('L').point(lambda v:255 if v>40 else 0)
    bb=diff.getbbox(); im=rgb.crop(bb) if bb else rgb
    w,h=im.size; k=int(min(w,h)*0.02); im=im.crop((k,k,w-k,h-k)); w,h=im.size; s=min(w,h); return im.crop(((w-s)//2,(h-s)//2,(w-s)//2+s,(h-s)//2+s))
def rmask(size,r):
    m=Image.new('L',size,0); ImageDraw.Draw(m).rounded_rectangle((0,0,size[0]-1,size[1]-1),r,fill=255); return m
# wall, oversized for the push-in
Z=1.08; WW,WH=int(W*Z),int(H*Z)
cell=262; gap=14; cols=5; rows=8
wall=Image.new('RGB',(WW,WH),CREAM)
mats=[trim(Image.open(R+p)).resize((cell,cell),Image.LANCZOS) for p in cfg['mats']]
tw=cols*cell+(cols-1)*gap; th=rows*cell+(rows-1)*gap
x0=(WW-tw)//2; y0=(WH-th)//2; k=0
for r in range(rows):
    off=(cell+gap)//2 if r%2 else 0
    for c in range(-1,cols+1):
        x=x0+c*(cell+gap)+off-(cell+gap)//4; y=y0+r*(cell+gap)
        if x+cell<0 or x>WW: continue
        m=mats[k%len(mats)]; k+=1
        wall.paste(m,(x,y),rmask(m.size,18))
# plate
plate=Image.new('RGBA',(W,H),(0,0,0,0))
px0,py0,px1,py1=90,610,990,1310
sh=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle((px0,py0+18,px1,py1+18),44,fill=(40,30,20,120)); plate.alpha_composite(sh.filter(ImageFilter.GaussianBlur(26)))
d=ImageDraw.Draw(plate); d.rounded_rectangle((px0,py0,px1,py1),44,fill=CREAM+(255,))
def ct(y,t,f,fill):
    d.text((W/2-d.textlength(t,font=f)/2,y),t,font=f,fill=fill)
ct(py0+56,"Your Christmas table, matched",ImageFont.truetype(PF4,46),INK)
fT=ImageFont.truetype(CAP,108); fY=ImageFont.truetype(PF4,116)
a="Find "; b="Your"; wa=d.textlength(a,font=fT); wb=d.textlength(b,font=fY); x=W/2-(wa+wb)/2; y=py0+140
d.text((x,y),a,font=fT,fill=GREEN); d.text((x+wa,y-6),b,font=fY,fill=GREEN)
c="Mat-ch"; wc=d.textlength(c,font=fT); d.text((W/2-wc/2,y+118),c,font=fT,fill=GREEN); d.text((W/2+wc/2+4,y+128),"™",font=ImageFont.truetype(BIT,34),fill=GREEN)
ct(py0+420,"Start with your tiles. Swipe the mats that match.",ImageFont.truetype(PF4,40),INK)
fP=ImageFont.truetype(BIT,44); t="Link in bio"; pw=d.textlength(t,font=fP)+80; ph=82; pxl=(W-pw)/2; py=py0+500
d.rounded_rectangle((pxl,py,pxl+pw,py+ph),ph/2,fill=RED); bb=fP.getbbox(t); d.text((pxl+40,py+(ph-(bb[3]-bb[1]))/2-bb[1]),t,font=fP,fill=(255,255,255))
ct(py0+612,cfg['code_line'],ImageFont.truetype(BIT,40),GREEN)
# frames
OUTF='/tmp/claude-0/-home-user/480229dd-9afd-5a5d-8d97-f8a0f68e2764/scratchpad/ds/frames/'; os.makedirs(OUTF,exist_ok=True)
for f in os.listdir(OUTF): os.remove(OUTF+f)
src=D+'dear-santa-reel-v3.mp4'
subprocess.run(['ffmpeg','-v','error','-y','-i',src,'-vf','select=eq(n\\,498)','-vframes','1',OUTF+'last_old.png'],check=True)
old=Image.open(OUTF+'last_old.png').convert('RGB')
N=62
for i in range(N):
    t=i/(N-1)
    scale=1.0+0.06*t  # push in
    cw=int(W/scale*Z/Z); ch=int(H/scale)
    cx=(WW-cw)//2; cy=(WH-ch)//2
    fr=wall.crop((cx,cy,cx+cw,cy+ch)).resize((W,H),Image.LANCZOS).convert('RGBA')
    fr.alpha_composite(plate); fr=fr.convert('RGB')
    if i<6: fr=Image.blend(old,fr,(i+1)/6)
    fr.save(OUTF+f'e{i:03d}.png')
fr.save(D+'v4/dear-santa-reel-v4-endcard.jpg',quality=90)
print('ok')
