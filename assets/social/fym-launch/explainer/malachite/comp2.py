import json,subprocess,math
from PIL import Image,ImageDraw,ImageFont,ImageFilter
W,H,FPS=1080,1920,30
CAP='/home/claude/mahjmatchmaker-data/scripts/social/tileprofile/fonts/Caprasimo.ttf'
NAVY=(6,42,85);PINK=(224,84,127);SOFT=(249,221,230);CREAM=(253,243,243)
meta=json.load(open('meta.json'))
def mat(name): return [m for m in meta['mats'] if m['n']==name][0]
SH=['Darjeeling','Jungle Turquoise','The Hunt Club','Dancing Poppies','Legacy','Domino Oxblood','Deep Green Garden Party','YOTD Black','Palomino','Dapper 2','Liberty','Hawthorne']
FINAL='Petalwood'
durs=[0.42,0.36,0.3,0.24,0.2,0.18,0.18,0.2,0.24,0.32,0.42,0.55]
tile=Image.open('tile.jpg').convert('RGB')
def circ(img,d):
    s=min(img.size); img=img.crop(((img.width-s)//2,(img.height-s)//2,(img.width+s)//2,(img.height+s)//2)).resize((d,d),Image.LANCZOS)
    m=Image.new('L',(d,d),0); ImageDraw.Draw(m).ellipse((0,0,d-1,d-1),fill=255)
    o=Image.new('RGBA',(d+24,d+24),(0,0,0,0)); ImageDraw.Draw(o).ellipse((0,0,d+23,d+23),fill=(255,255,255,255)); o.paste(img,(12,12),m); return o
TILEC=circ(tile,360)
f1=ImageFont.truetype(CAP,64); f2=ImageFont.truetype(CAP,40); f3=ImageFont.truetype(CAP,84)
def text_c(d,y,t,f,fill):
    w=d.textlength(t,font=f); d.text(((W-w)/2,y),t,font=f,fill=fill)
def mat_frame(m,heart=0.0,racks=None,head='Let’s see…'):
    fr=Image.new('RGB',(W,H),SOFT); d=ImageDraw.Draw(fr)
    text_c(d,250,head,f3,NAVY)
    im=Image.open(m['file']).convert('RGB'); sc=880/max(im.size); im=im.resize((int(im.width*sc),int(im.height*sc)),Image.LANCZOS)
    x=(W-im.width)//2; y=430+(880-im.height)//2
    sh=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle((x,y+20,x+im.width,y+im.height+20),18,fill=(6,42,85,60)); sh=sh.filter(ImageFilter.GaussianBlur(24))
    fr=fr.convert('RGBA'); fr.alpha_composite(sh); fr.paste(im,(x,y)); d=ImageDraw.Draw(fr)
    if racks:
        rx=x-10; ry=y+im.height-60
        for i,rf in enumerate(racks):
            r=Image.open(rf).convert('RGBA'); sc2=620/r.width; r=r.resize((620,int(r.height*sc2)),Image.LANCZOS); fr.alpha_composite(r,(rx+i*20,ry-int(racks_off*(1))+i*110 if False else ry+i*110))
    fr.alpha_composite(TILEC,(W-TILEC.width-50,y+im.height-TILEC.height+120))
    ly=1430
    text_c(d,ly,m['n'],f1,NAVY); text_c(d,ly+86,m['bn'],f2,PINK)
    if heart>0:
        s=int(200*min(1,heart)*(1.15 if heart<0.6 else 1)); hc=Image.new('RGBA',(s,s),(0,0,0,0)); hd=ImageDraw.Draw(hc); hd.ellipse((0,0,s-1,s-1),fill=PINK+(255,))
        r=s*0.16; cx=s/2; cy=s*0.43; hd.ellipse((cx-2*r,cy-r,cx,cy+r),fill=(255,255,255,255)); hd.ellipse((cx,cy-r,cx+2*r,cy+r),fill=(255,255,255,255)); hd.polygon([(cx-2*r+1,cy+r*0.25),(cx+2*r-1,cy+r*0.25),(cx,cy+2.4*r)],fill=(255,255,255,255))
        fr.alpha_composite(hc,(x+im.width-s//2-20,y-s//2+20))
    return fr.convert('RGB')
racks_off=0
def card(k,u,zoom=0.035):
    im=Image.open(f'card_{k}.png').convert('RGB'); s=1+zoom*u; w,h=int(W*s),int(H*s)
    return im.resize((w,h),Image.LANCZOS).crop(((w-W)//2,(h-H)//2,(w-W)//2+W,(h-H)//2+H))
p=subprocess.Popen(['ffmpeg','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-movflags','+faststart','body.mp4'],stdin=subprocess.PIPE)
def emit(img,n):
    b=img.tobytes()
    for _ in range(n): p.stdin.write(b)
def seg_card(k,dur,zoom=0.035):
    n=int(dur*FPS)
    for i in range(n): p.stdin.write(card(k,i/n,zoom).tobytes())
seg_card('q1',1.8); seg_card('q2',1.8); seg_card('q3',1.6); seg_card('q4',2.0)
for nm,dd in zip(SH,durs): emit(mat_frame(mat(nm)),max(2,int(dd*FPS)))
fm=mat(FINAL); RK=[meta['racks'][r]['file'] for r in ['peacelovemahjong.com/mahjong-racks-racks-pushers-set-of-4','bb:French Blue'] if r in meta['racks']][:2]
emit(mat_frame(fm,head='Let’s see…'),int(0.5*FPS))
for i in range(10): p.stdin.write(mat_frame(fm,heart=(i+1)/10,head='It’s a mat-ch!').tobytes())
emit(mat_frame(fm,heart=1,racks=RK,head='It’s a mat-ch!'),int(2.3*FPS))
seg_card('end',3.2,0.02)
p.stdin.close(); p.wait(); print('ok', fm['racks'], RK)
