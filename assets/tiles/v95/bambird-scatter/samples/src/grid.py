import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage
def seams(prof,n,lo,hi):
    # refine n+1 boundaries between lo and hi at local minima
    step=(hi-lo)/n;out=[]
    for k in range(n+1):
        e=lo+k*step;a=int(max(0,e-step*.18));b=int(min(len(prof)-1,e+step*.18))
        out.append(a+int(np.argmin(prof[a:b+1])))
    return out
def rr(w,h,r):
    m=Image.new('L',(w,h),0);ImageDraw.Draw(m).rounded_rectangle((0,0,w-1,h-1),radius=r,fill=255);return m.filter(ImageFilter.GaussianBlur(1.2))
def cells(path,box,rows,cols,ins=.035):
    im=Image.open(path).convert('RGB');g=np.asarray(im.convert('L')).astype(float)
    x0,y0,x1,y1=box
    reg=g[y0:y1,x0:x1]
    vp=ndimage.uniform_filter1d(reg[int((y1-y0)*.1):int((y1-y0)*.9)].mean(0),5)
    hp=ndimage.uniform_filter1d(reg[:,int((x1-x0)*.1):int((x1-x0)*.9)].mean(1),5)
    xs=[x0+v for v in seams(vp,cols,0,x1-x0-1)];ys=[y0+v for v in seams(hp,rows,0,y1-y0-1)]
    out={}
    for r in range(rows):
        for c in range(cols):
            a,b,c2,d=xs[c],ys[r],xs[c+1],ys[r+1];w=c2-a;h=d-b
            t=im.crop((int(a+w*ins),int(b+h*ins),int(c2-w*ins),int(d-h*ins))).convert('RGBA')
            t.putalpha(rr(t.width,t.height,int(t.width*.09)));out[(r,c)]=t
    return out,xs,ys
