import sys,numpy as np
from PIL import Image
from scipy import ndimage
def one(src,dst):
    im=Image.open(src).convert('RGBA'); a=np.array(im)
    m=a[:,:,3]>40; lab,n=ndimage.label(ndimage.binary_closing(m,iterations=2))
    if n<2: im.save(dst); return n
    sizes=ndimage.sum(m,lab,range(1,n+1)); big=[i+1 for i,s in enumerate(sizes) if s>0.5*sizes.max()]
    # topmost big component
    k=min(big,key=lambda i:np.argwhere(lab==i)[:,0].mean())
    keep=(lab==k); b=a.copy(); b[~keep,3]=0
    ys,xs=np.nonzero(keep); pts=np.c_[xs,ys]-[xs.mean(),ys.mean()]
    ev,evec=np.linalg.eigh(np.cov(pts.T)); v=evec[:,1]; ang=np.degrees(np.arctan2(v[1],v[0]))
    if ang>90: ang-=180
    if ang<-90: ang+=180
    out=Image.fromarray(b).rotate(ang,expand=True,resample=Image.BICUBIC)
    out=out.crop(out.getbbox()); out.save(dst); return n
for s,d in zip(sys.argv[1::2],sys.argv[2::2]): print(d,one(s,d))
