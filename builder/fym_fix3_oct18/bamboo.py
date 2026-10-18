# cut a mat out of a bamboo/rattan/wood surface: classify tan "surface" pixels by colour, crop to the mat, whiten leftover corners
import numpy as np
from PIL import Image, ImageFilter
def surf_mask(im):
    hsv=np.asarray(im.convert('HSV'),dtype=float)
    h=hsv[...,0]*360/255; s=hsv[...,1]/255; v=hsv[...,2]/255
    return (h>15)&(h<48)&(s>0.22)&(s<0.75)&(v>0.30)&(v<0.92)
def surface_fraction(im):
    sm=im.convert('RGB').resize((300,300)); m=surf_mask(sm); e=10
    strip=np.concatenate([m[:e].ravel(),m[-e:].ravel(),m[:,:e].ravel(),m[:,-e:].ravel()])
    return float(strip.mean())
def run(v,th):
    best=(0,0,0); s=None
    for i,x in enumerate(list(v)+[0]):
        if x>th and s is None: s=i
        if x<=th and s is not None:
            if i-s>best[0]: best=(i-s,s,i)
            s=None
    return best[1],best[2]
def cut(im):
    im=im.convert('RGB'); sm=im.filter(ImageFilter.MedianFilter(5))
    mat=~surf_mask(sm); H,W=mat.shape
    pr,pc=mat.mean(1),mat.mean(0)
    r0,r1=run(pr,0.6); c0,c1=run(pc,0.6)
    if r1-r0<H*0.45 or c1-c0<W*0.45: return None
    # tighten: inside the box, edge rows/cols still mostly surface -> step in
    def tighten(a0,a1,prof):
        while a1-a0>10 and prof[a0]<0.75: a0+=1
        while a1-a0>10 and prof[a1-1]<0.75: a1-=1
        return a0,a1
    sub=mat[r0:r1,c0:c1]; r0b,r1b=tighten(0,sub.shape[0],sub.mean(1)); c0b,c1b=tighten(0,sub.shape[1],sub.mean(0))
    r0,r1,c0,c1=r0+r0b,r0+r1b,c0+c0b,c0+c1b
    out=np.asarray(im.crop((c0,r0,c1,r1))).copy(); mm=mat[r0:r1,c0:c1]
    h,w=mm.shape; k=int(min(h,w)*0.08)
    for ys,xs in ((slice(0,k),slice(0,k)),(slice(0,k),slice(w-k,w)),(slice(h-k,h),slice(0,k)),(slice(h-k,h),slice(w-k,w))):
        sub=out[ys,xs]; sub[~mm[ys,xs]]=255; out[ys,xs]=sub
    return Image.fromarray(out)
