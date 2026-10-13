import subprocess,json,math
from PIL import Image,ImageFilter
W,H,FPS=1080,1920,30
CREAM=(246,233,223)
R='/home/claude/mahjmatchmaker-data/'
mat=Image.open(R+'config/matcard/larkspur_mat.jpg').convert('RGB')
IDX=json.load(open(R+'assets/tiles/album/index.json'))
def pile(n): 
    im=Image.open(R+IDX[n]['file']).convert('RGB');s=min(im.size);l=(im.width-s)//2;t=(im.height-s)//2;return im.crop((l,t,l+s,t+s))
ov={k:Image.open(f'ov-{k}.png').convert('RGBA') for k in ['title','matches']}
labs=[('Moonlight','Moonlight'),('Limoncello','Limoncello'),('La Fete','La Fete'),('Luminaire','Luminaire'),('Palm Royale','Palm Royale'),('Spring Love (retired)','Spring Love')]
labimg={l:Image.open(f'ov-lab-{l}.png').convert('RGBA') for _,l in labs}
sec=Image.open('/tmp/cc/seq/larkspur-3-secret.png').convert('RGB')
card=Image.open('/tmp/cc/seq/larkspur-6-card-option2-bigger-tiles.png').convert('RGB')
ease=lambda x:1-(1-x)**3
def shadowed(img,r=24,border=10):
    b=Image.new('RGB',(img.width+2*border,img.height+2*border),(255,255,255));b.paste(img,(border,border));return b
MATW=960;MATY=420
matS=mat.resize((MATW,MATW),Image.LANCZOS)
def base():
    f=Image.new('RGB',(W,H),CREAM);f.paste(matS,((W-MATW)//2,MATY));return f
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-preset','medium','-movflags','+faststart','larkspur-reel-preview.mp4'],stdin=subprocess.PIPE)
def emit(f): p.stdin.write(f.tobytes())
# 1 hook: zoom out from bird detail to full mat (2.6s)
n=int(2.6*FPS)
for i in range(n):
    t=ease(min(1,i/(n*0.8)))
    sc=2.4-(2.4-1)*t
    sz=int(MATW*sc);m=mat.resize((sz,sz),Image.BILINEAR)
    # focus point top-right bird at (0.78,0.25) -> center moves to mat center
    fx=0.78+(0.5-0.78)*t;fy=0.25+(0.5-0.25)*t
    cx=W//2;cy=MATY+MATW//2
    f=Image.new('RGB',(W,H),CREAM);f.paste(m,(int(cx-fx*sz),int(cy-fy*sz)))
    if i>n*0.35:
        a=min(1,(i-n*0.35)/(n*0.25));o=ov['title'].copy();o.putalpha(o.getchannel('A').point(lambda v:int(v*a)));f.paste(o,(0,0),o)
    emit(f)
# 2 beats: pile drops on corner (1.3s each)
for key,lab in labs:
    pl=shadowed(pile(key).resize((440,440),Image.LANCZOS))
    n=int(1.3*FPS)
    for i in range(n):
        f=base();f.paste(ov['matches'],(0,0),ov['matches'])
        t=ease(min(1,i/9))
        s=1.35-0.35*t;sz=int(pl.width*s);pp=pl.resize((sz,sz),Image.BILINEAR)
        tx=W-80-pl.width+ (pl.width-sz)//2; ty=MATY+MATW-pl.width+40+(pl.width-sz)//2 - int(60*(1-t))
        f.paste(pp,(tx,ty))
        l=labimg[lab];f.paste(l,(0,0),l)
        emit(f)
# 3 secret (3.2s) gentle zoom
n=int(3.2*FPS)
for i in range(n):
    s=1+0.04*i/n;sz=(int(W*s),int(H*s));im=sec.resize(sz,Image.BILINEAR);l=(sz[0]-W)//2;t=(sz[1]-H)//2;emit(im.crop((l,t,l+W,t+H)))
# 4 end card (3.8s) slide-up then hold
n=int(3.8*FPS)
for i in range(n):
    t=ease(min(1,i/12));f=Image.new('RGB',(W,H),CREAM);f.paste(card,(0,int(200*(1-t))));emit(f)
p.stdin.close();p.wait()
