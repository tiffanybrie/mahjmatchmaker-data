from PIL import Image, ImageFilter, ImageDraw
import numpy as np
im=Image.open('assets/tiles/v92/bam-bird-origami-timber-split.jpg').convert('RGB');g=np.asarray(im).astype(float).mean(2)
def sm(p,k=5): return np.convolve(p,np.ones(k)/k,'same')
def vx(c,y0,y1,r=10):  # x of vertical gutter near c within rows y0..y1
    p=sm(g[y0:y1,c-r:c+r].mean(0),3); return c-r+float(np.argmin(p))
def hy(c,x0,x1,r=10):
    p=sm(g[c-r:c+r,x0:x1].mean(1),3); return c-r+float(np.argmin(p))
def centroid(p,off):
    w=np.clip(p.max()-p-(p.max()-p.min())*.5,0,None)
    return off+float((w*np.arange(len(p))).sum()/w.sum())
def lattice(cols,rows,pitchx,pitchy):
    pts=[]
    rb=[0]+rows+[699]
    for ci,c in enumerate(cols):
        for ri,rw in enumerate(rows):
            # refine x just above and below the row gutter, y left and right of col gutter
            x=centroid(g[rw-16:rw+16,c-14:c+14].mean(0),c-14)
            y=centroid(g[rw-14:rw+14,c-16:c+16].mean(1),rw-14)
            pts.append((ci,ri,x,y))
    return pts
F=lattice([286,418,551],[165,349,533],132,184)
B=lattice([1017,1141,1267],[175,348,521],126,173)
for p in F+B: print(p)
def affine(pts,tx,ty):
    A=[];bx=[];by=[]
    for ci,ri,x,y in pts:
        A.append([tx[ci],ty[ri],1]);bx.append(x);by.append(y)
    A=np.array(A);cx=np.linalg.lstsq(A,np.array(bx),rcond=None)[0];cy=np.linalg.lstsq(A,np.array(by),rcond=None)[0]
    res=np.abs(A@cx-bx).max(),np.abs(A@cy-by).max()
    return (cx[0],cx[1],cx[2],cy[0],cy[1],cy[2]),res
TY=[237,500,763]
cf,rf=affine(F,[0,200,400],TY);cb,rb=affine(B,[0,200,400],TY);print('resid',rf,rb)
f=im.transform((400,1000),Image.AFFINE,cf,Image.BICUBIC)
b=im.transform((400,1000),Image.AFFINE,cb,Image.BICUBIC)
out=Image.new('RGB',(800,1000),'white');out.paste(f,(0,0));out.paste(b,(400,0))
ImageDraw.Draw(out).rectangle([397,0,402,1000],fill='white')
out=out.filter(ImageFilter.UnsharpMask(1.2,60,2))
out.save('assets/tiles/album/inset/origami-timber-winds-2col.jpg',quality=93)
out.save('/tmp/claude-0/-home-claude/f4da3022-6ec8-595a-90aa-668aea191899/scratchpad/origami-inset-B-fixed.jpg',quality=93)
