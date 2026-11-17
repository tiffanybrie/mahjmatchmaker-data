# Holiday reel end cards (Nov 17 pm): mat wall behind a cream plate (Tiffany loved this on Dear Santa),
# REAL Find Your Mat-ch lockup image (assets/brand/fym-lockup/find-your-mat-ch-lockup.png, cut from the approved
# Juniper end card) instead of typed text, and a comment keyword instead of "Link in bio".
import json, subprocess, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageFilter
R='/home/claude/tiffanybrie/mahjmatchmaker-data/'
FD=R+'scripts/social/tileprofile/fonts/'
BIT=R+'scripts/albumcard/woodfix/Bitter-Bold.ttf'; PF4=FD+'playfair-display-latin-400-italic.woff2'
LOCK=R+'assets/brand/fym-lockup/find-your-mat-ch-lockup.png'
CREAM=(246,234,224); GREEN=(15,72,42); RED=(179,32,42); INK=(70,52,40)
W,H=1080,1920; FPS=24
SCR='/tmp/claude-0/-home-user/480229dd-9afd-5a5d-8d97-f8a0f68e2764/scratchpad/endcards/'
POOL=json.load(open(R+'assets/social/holiday-endcards-nov17/holiday-wall-pool.json'))
FAR={'santa','holiday-love','apres','bb-plaid','nutcracker','frost'}  # only one of each look-alike family on a wall
REELS={
 'dear-santa':dict(src=R+'assets/social/dear-santa-push/dear-santa-reel-v3.mp4', cut=499,
   frames=SCR+'../fix_ds', first=POOL['ar9']+json.load(open(R+'assets/social/dear-santa-push/reel-config.json'))['mats'],
   kicker='Your Christmas table, matched', sub='Start with your tiles. Swipe the mats that match.',
   pill='Comment SANTA for the link', code='Code MAHJMATCH at Anders Ruff',
   out=R+'assets/social/dear-santa-push/v5/dear-santa-reel-v5'),
 'tinselle':dict(src=R+'assets/social/holiday-reels-nov17/tinselle-emerald-reel.mp4', cut=302,
   frames=SCR+'../fix_tin', first=json.load(open(R+'assets/social/holiday-endcards-nov17/tinselle-wall-mats.json')),
   kicker='Your Christmas table, matched', sub='Start with your tiles. Swipe the mats that match.',
   pill='Comment TINSEL for the link', code='Code MAHJMATCH at Virora Mahjong',
   out=R+'assets/social/holiday-reels-nov17/v2/tinselle-emerald-reel-v2'),
}
def trim(im):
    rgb=im.convert('RGB'); bg=Image.new('RGB',rgb.size,(255,255,255))
    bb=ImageChops.difference(rgb,bg).convert('L').point(lambda v:255 if v>40 else 0).getbbox(); im=rgb.crop(bb) if bb else rgb
    w,h=im.size; k=int(min(w,h)*0.02); im=im.crop((k,k,w-k,h-k)); w,h=im.size; s=min(w,h)
    return im.crop(((w-s)//2,(h-s)//2,(w-s)//2+s,(h-s)//2+s))
def rmask(size,r):
    m=Image.new('L',size,0); ImageDraw.Draw(m).rounded_rectangle((0,0,size[0]-1,size[1]-1),r,fill=255); return m
def wall(first):
    # every cell gets a DIFFERENT mat (Tiffany Nov 17: she spotted the Santa mat twice). The cells people can see
    # best (in frame, outside the plate) get the reel's own mats first, then the rest of the holiday pool.
    Z=1.08; WW,WH=int(W*Z),int(H*Z); cell=262; gap=14; cols=5; rows=8
    tw=cols*cell+(cols-1)*gap; th=rows*cell+(rows-1)*gap; x0=(WW-tw)//2; y0=(WH-th)//2
    ox,oy=(WW-W)//2,(WH-H)//2; PL=(90+ox,660+oy,990+ox,1260+oy)
    cells=[]
    for r in range(rows):
        off=(cell+gap)//2 if r%2 else 0
        for c in range(-1,cols+1):
            x=x0+c*(cell+gap)+off-(cell+gap)//4; y=y0+r*(cell+gap)
            if x+cell<0 or x>WW: continue
            vx0,vy0,vx1,vy1=max(x,ox),max(y,oy),min(x+cell,ox+W),min(y+cell,oy+H)
            vis=max(0,vx1-vx0)*max(0,vy1-vy0)
            px0,py0,px1,py1=max(vx0,PL[0]),max(vy0,PL[1]),min(vx1,PL[2]),min(vy1,PL[3])
            vis-=max(0,px1-px0)*max(0,py1-py0)
            cells.append((vis,r,c,x,y))
    pool=[p for p in POOL['pool'] if p not in POOL['drop']]
    order=[p for i,p in enumerate(first+pool) if p not in (first+pool)[:i] and p not in POOL['drop']]
    assert len(order)>=len(cells),(len(order),len(cells))
    def grp(p): return next((g for g,keys in POOL['groups'].items() if any(k in p for k in keys)),None)
    ranked=sorted(cells,key=lambda t:-t[0])
    wl=Image.new('RGB',(WW,WH),CREAM); used=[]; placed=[]
    for vis,r,c,x,y in ranked:
        # look-alike mats (two Santas, two colorways of one design) sit at least 3 cells apart
        pth=next(p for p in order if p not in used and not any(grp(p) and grp(p)==g and max(abs(r-r2),abs(c-c2))<(99 if g in FAR else 4) for g,r2,c2 in placed))
        used.append(pth); placed.append((grp(pth),r,c))
        m=trim(Image.open(R+pth)).resize((cell,cell),Image.LANCZOS); wl.paste(m,(x,y),rmask(m.size,18))
    assert len(set(used))==len(used)
    print('wall cells',len(cells),'distinct mats',len(set(used)))
    return wl
def plate(cfg):
    pl=Image.new('RGBA',(W,H),(0,0,0,0)); PH=600; px0,px1=90,990; py0=(H-PH)//2; py1=py0+PH
    sh=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle((px0,py0+18,px1,py1+18),44,fill=(40,30,20,120))
    pl.alpha_composite(sh.filter(ImageFilter.GaussianBlur(26))); d=ImageDraw.Draw(pl); d.rounded_rectangle((px0,py0,px1,py1),44,fill=CREAM+(255,))
    def ct(y,t,f,fill):
        tw=d.textlength(t,font=f); assert tw<=px1-px0-100,(t,tw); d.text((W/2-tw/2,y),t,font=f,fill=fill)
    ct(py0+52,cfg['kicker'],ImageFont.truetype(PF4,46),INK)
    lk=Image.open(LOCK); lw=780; lk=lk.resize((lw,round(lk.height*lw/lk.width)),Image.LANCZOS)
    pl.alpha_composite(lk,((W-lw)//2,py0+150))
    ct(py0+286,cfg['sub'],ImageFont.truetype(PF4,36),INK)
    fP=ImageFont.truetype(BIT,44); t=cfg['pill']; pw=d.textlength(t,font=fP)+84; ph=84; pxl=(W-pw)/2; py=py0+372
    d.rounded_rectangle((pxl,py,pxl+pw,py+ph),ph/2,fill=RED); bb=fP.getbbox(t); d.text((pxl+42,py+(ph-(bb[3]-bb[1]))/2-bb[1]),t,font=fP,fill=(255,255,255))
    ct(py0+498,cfg['code'],ImageFont.truetype(BIT,40),GREEN)
    return pl
for name in (sys.argv[1:] or REELS):
    cfg=REELS[name]; F=SCR+name+'/'; os.makedirs(F,exist_ok=True); [os.remove(F+f) for f in os.listdir(F)]
    os.makedirs(os.path.dirname(cfg['out']),exist_ok=True)
    wl=wall(cfg['first']); pl=plate(cfg); WW,WH=wl.size
    old=Image.open(cfg['frames']+f"/f{cfg['cut']:04d}.png").convert('RGB').resize((W,H)); N=72
    for i in range(N):
        s=1.0+0.06*i/(N-1); cw=int(W/s); ch=int(H/s); cx=(WW-cw)//2; cy=(WH-ch)//2
        fr=wl.crop((cx,cy,cx+cw,cy+ch)).resize((W,H),Image.LANCZOS).convert('RGBA'); fr.alpha_composite(pl); fr=fr.convert('RGB')
        if i<6: fr=Image.blend(old,fr,(i+1)/6)
        fr.save(F+f'e{i:03d}.png')
    fr.save(cfg['out']+'-endcard.jpg',quality=92)
    subprocess.run(['ffmpeg','-v','error','-y','-framerate',str(FPS),'-i',cfg['frames']+'/f%04d.png','-framerate',str(FPS),'-i',F+'e%03d.png','-filter_complex',
      f"[0:v]trim=end_frame={cfg['cut']},setpts=PTS-STARTPTS,scale={W}:{H},format=yuv420p,setsar=1[a];[1:v]format=yuv420p,setsar=1[b];[a][b]concat=n=2:v=1:a=0[v]",
      '-map','[v]','-r',str(FPS),'-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',cfg['out']+'.mp4'],check=True)
    print(name,'ok')
