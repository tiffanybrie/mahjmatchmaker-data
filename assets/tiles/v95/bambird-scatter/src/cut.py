import numpy as np, json
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage
B='/tmp/claude-0/-home-claude/05549d34-8fe3-5ca9-a6a5-308991cb9a78/scratchpad/bbt/'
G={'classic':('east-meets-west-tortoise-shell-tile-set-copy_01.jpg',(1012,2392,2940,3488)),'emw':('east-meets-west-tortoise-shell-tile-set_00.jpg',(1048,2172,3328,3464))}
PICK=[(3,4),(3,5),(3,6),(3,7),(3,8),(3,9),(1,9),(2,9),(3,0),(3,2),(1,0),(0,4)]  # N E W S J J dragon dragon flower1 flower3 bam1 dot5
def rr(w,h,r):
    m=Image.new('L',(w,h),0);ImageDraw.Draw(m).rounded_rectangle((0,0,w-1,h-1),radius=r,fill=255);return m.filter(ImageFilter.GaussianBlur(1))
def edge(prof,lo,hi):
    return lo+int(np.argmax(prof[lo:hi]))
out={}
for k,(f,(x0,y0,x1,y1)) in G.items():
    im=Image.open(B+f).convert('RGB');g=np.asarray(im.convert('L')).astype(float);cw=(x1-x0)/10;ch=(y1-y0)/4
    tiles=[]
    for r,c in PICK:
        ex,ey=cw*.25,ch*.2
        wx0,wy0=int(x0+c*cw-ex),int(y0+r*ch-ey);wx1,wy1=int(x0+(c+1)*cw+ex),int(y0+(r+1)*ch+ey)
        w=g[wy0:wy1,wx0:wx1];d=(w<205).astype(float)
        # restrict to central band to find vertical seams, central columns for horizontal
        H,W=w.shape
        vc=d[int(H*.3):int(H*.7),:].mean(0);hc=d[:,int(W*.3):int(W*.7)].mean(1)
        vc=ndimage.uniform_filter1d(vc,3);hc=ndimage.uniform_filter1d(hc,3)
        L=edge(vc,0,int(W*.35));R=edge(vc,int(W*.65),W);T=edge(hc,0,int(H*.3));Bt=edge(hc,int(H*.7),H)
        t=im.crop((wx0+L+3,wy0+T+3,wx0+R-2,wy0+Bt-2)).convert('RGBA');t.putalpha(rr(t.width,t.height,int(t.width*.08)))
        tiles.append(t)
    # backs
    a=np.asarray(im).astype(int);mx=a.max(2);sat=mx-a.min(2)
    dark=(mx<170)|(sat>60);dark=ndimage.binary_opening(dark,iterations=3);dark=ndimage.binary_closing(dark,iterations=6);dark=ndimage.binary_fill_holes(dark)
    lab,n=ndimage.label(dark);sz=ndimage.sum(dark,lab,range(1,n+1));objs=ndimage.find_objects(lab)
    backs=[]
    for i,(sl,s) in enumerate(zip(objs,sz)):
        if not (42000<s<70000): continue
        y0b,y1b,x0b,x1b=sl[0].start,sl[0].stop,sl[1].start,sl[1].stop
        if k=='emw' and x0b>1100: continue
        if k=='classic' and x0b<1600: continue
        m=(lab[y0b:y1b,x0b:x1b]==i+1);m=ndimage.binary_erosion(m,iterations=4)
        al=Image.fromarray((m*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.5))
        t=im.crop((x0b,y0b,x1b,y1b)).convert('RGBA');t.putalpha(al);backs.append(t)
    out[k]=(tiles,backs)
    S=Image.new('RGB',(13*170,2*240),'white')
    for j,t in enumerate(tiles): u=t.copy();u.thumbnail((160,220));S.paste(u,(j*170,5),u)
    for j,t in enumerate(backs): u=t.copy();u.thumbnail((160,220));S.paste(u,(j*170,245),u)
    S.save(f'cut_{k}.jpg')
    for j,t in enumerate(tiles): t.save(f'{k}_face{j}.png')
    for j,t in enumerate(backs): t.save(f'{k}_back{j}.png')
    print(k,len(tiles),len(backs),[t.size for t in tiles][:3],[t.size for t in backs][:3])
