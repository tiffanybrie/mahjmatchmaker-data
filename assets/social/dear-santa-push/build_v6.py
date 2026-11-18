# Dear Santa reel v6 (Nov 17 pm, Tiffany's notes): no more pile of mats with white space. The mats now fill the
# whole frame in a slow two-column scroll; the unverified "Ships end of November" pill is gone; no Planoly song
# (she adds her own music in Instagram). Keeps the hook, the live Find Your Mat-ch phone scene (real lockup),
# the Dear Santa cover card and the mat-wall end card she liked.
import json, os, shutil, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageFilter
R='/home/claude/tiffanybrie/mahjmatchmaker-data/'
SCR='/tmp/claude-0/-home-user/480229dd-9afd-5a5d-8d97-f8a0f68e2764/scratchpad/'
SRC=SCR+'fix_ds/'; END=SCR+'endcards/dear-santa/'; OUTF=SCR+'rb/ds6/'
FD=R+'scripts/social/tileprofile/fonts/'; CAP=FD+'Caprasimo.ttf'; BIT=R+'scripts/albumcard/woodfix/Bitter-Bold.ttf'
W,H,FPS=1080,1920,24; GREEN=(15,72,42); RED=(179,32,42)
cfg=json.load(open(R+'assets/social/dear-santa-push/reel-config.json'))
shutil.rmtree(OUTF,ignore_errors=True); os.makedirs(OUTF)
frames=[]
def add(im): p=OUTF+f'{len(frames):04d}.png'; im.convert('RGB').save(p); frames.append(p)
def src(i): return Image.open(SRC+f'f{i+1:04d}.png').convert('RGB')
def xfade(a,b,n):
    for k in range(1,n+1): add(Image.blend(a,b,k/(n+1)))
# A hook (source frames 5..59, already faded in)
for i in range(5,60): add(src(i))
# B tiles: the Anders Ruff photo, slow push-in, title only
ph=Image.open(R+cfg['tiles']).convert('RGB'); s=H/ph.height; ph=ph.resize((round(ph.width*s),H),Image.LANCZOS)
ph=ph.crop(((ph.width-W)//2,0,(ph.width-W)//2+W,H))
title=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(title); f=ImageFont.truetype(CAP,86)
for k,t in enumerate(['Dear Santa tiles','by Anders Ruff']):
    tw=d.textlength(t,font=f); assert tw<W-120,(t,tw); d.text(((W-tw)/2,300+k*104),t,font=f,fill=(255,255,255))
sh=Image.new('RGBA',(W,H),(0,0,0,0)); sh.putalpha(title.split()[3].filter(ImageFilter.GaussianBlur(10)).point(lambda v:int(v*.75)))
sh=Image.composite(Image.new('RGBA',(W,H),(20,10,10,255)),Image.new('RGBA',(W,H),(0,0,0,0)),sh.split()[3])
def tiles(i,n=54):
    z=1+0.07*i/(n-1); cw,ch=int(W/z),int(H/z); im=ph.crop(((W-cw)//2,(H-ch)//2,(W-cw)//2+cw,(H-ch)//2+ch)).resize((W,H),Image.LANCZOS).convert('RGBA')
    im.alpha_composite(sh); im.alpha_composite(title); return im.convert('RGB')
xfade(src(59),tiles(0),6)
for i in range(54): add(tiles(i))
# C every mat, filling the frame: two-column scroll on deep green
def trim(im):
    rgb=im.convert('RGB'); bg=Image.new('RGB',rgb.size,(255,255,255))
    bb=ImageChops.difference(rgb,bg).convert('L').point(lambda v:255 if v>40 else 0).getbbox(); im=rgb.crop(bb) if bb else rgb
    w,h=im.size; k=int(min(w,h)*0.02); im=im.crop((k,k,w-k,h-k)); w,h=im.size; s=min(w,h)
    return im.crop(((w-s)//2,(h-s)//2,(w-s)//2+s,(h-s)//2+s))
# order: Anders Ruff first, brands mixed, look-alikes (two Santas, two Holly Jollys) far apart
ORDER=[0,4, 2,23, 1,15, 22,7, 10,9, 18,5, 8,19, 11,14, 21,16, 6,13, 24,3, 17,20, 12,25]
assert sorted(ORDER)==list(range(26))
mats=[cfg['mats'][i] for i in ORDER]; assert len(mats)==len(set(mats))==26
M=18; cell=(W-3*M)//2; rows=(len(mats)+1)//2; TH=M+rows*(cell+M)
strip=Image.new('RGB',(W,TH),GREEN)
mk=Image.new('L',(cell,cell),0); ImageDraw.Draw(mk).rounded_rectangle((0,0,cell-1,cell-1),20,fill=255)
for j,p in enumerate(mats):
    m=trim(Image.open(R+p)).resize((cell,cell),Image.LANCZOS); strip.paste(m,(M+(j%2)*(cell+M),M+(j//2)*(cell+M)),mk)
fP=ImageFont.truetype(BIT,46); t='26 Christmas mats that match'
pill=Image.new('RGBA',(W,H),(0,0,0,0)); dp=ImageDraw.Draw(pill); pw=dp.textlength(t,font=fP)+96; phh=96; px=(W-pw)/2; py=250
shp=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(shp).rounded_rectangle((px,py+10,px+pw,py+phh+10),phh/2,fill=(0,0,0,110))
pill.alpha_composite(shp.filter(ImageFilter.GaussianBlur(14))); dp=ImageDraw.Draw(pill)
dp.rounded_rectangle((px,py,px+pw,py+phh),phh/2,fill=RED); bb=fP.getbbox(t); dp.text((px+48,py+(phh-(bb[3]-bb[1]))/2-bb[1]),t,font=fP,fill=(255,255,255))
N=168; travel=TH-H
def scroll(i):
    u=i/(N-1); e=u*u*(3-2*u); y=round(travel*(0.15*u+0.85*e))
    im=strip.crop((0,y,W,y+H)).convert('RGBA'); im.alpha_composite(pill); return im.convert('RGB')
xfade(tiles(53),scroll(0),5)
for i in range(N): add(scroll(i))
# D live Find Your Mat-ch phone scene (steady from source frame 262) and E cover (source 456..498)
xfade(scroll(N-1),src(262),6)
for i in range(262,499): add(src(i))
# F mat-wall end card (its first 6 frames already blend from source frame 499)
for k in range(72): add(Image.open(END+f'e{k:03d}.png'))
out=R+'assets/social/dear-santa-push/v6/dear-santa-reel-v6.mp4'
subprocess.run(['ffmpeg','-v','error','-y','-framerate',str(FPS),'-i',OUTF+'%04d.png','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',out],check=True)
strip.resize((W//4,TH//4)).save(SCR+'rb/ds6_strip.jpg',quality=85)
print('frames',len(frames),'sec',round(len(frames)/FPS,1),'strip',TH,'travel',travel)
