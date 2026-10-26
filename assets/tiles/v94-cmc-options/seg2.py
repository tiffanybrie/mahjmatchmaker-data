import numpy as np, cv2
from PIL import Image, ImageFilter
from scipy import ndimage
def cutout(path, maxdim=1100):
    im=Image.open(path).convert('RGB');W,H=im.size;s=maxdim/max(W,H)
    sm=np.asarray(im.resize((int(W*s),int(H*s)),Image.LANCZOS));h,w=sm.shape[:2]
    lab=cv2.cvtColor(sm,cv2.COLOR_RGB2LAB).astype(float)
    bw=max(3,int(min(h,w)*.015))
    border=np.concatenate([lab[:bw].reshape(-1,3),lab[-bw:].reshape(-1,3),lab[:,:bw].reshape(-1,3),lab[:,-bw:].reshape(-1,3)])
    # border pixels that look like background (most common cluster): use median
    bg=np.median(border,0)
    d=np.sqrt((((lab-bg)*np.array([.6,1.5,1.5]))**2).sum(2))
    m=np.full((h,w),cv2.GC_PR_FGD,np.uint8)
    near=d<18
    lab_,n=ndimage.label(near);edge=np.unique(np.concatenate([lab_[0],lab_[-1],lab_[:,0],lab_[:,-1]]));edge=edge[edge>0]
    bgc=np.isin(lab_,edge)
    m[bgc]=cv2.GC_PR_BGD;m[ndimage.binary_erosion(bgc,iterations=6)]=cv2.GC_BGD
    m[d>60]=cv2.GC_PR_FGD
    bgd=np.zeros((1,65));fgd=np.zeros((1,65))
    cv2.grabCut(cv2.cvtColor(sm,cv2.COLOR_RGB2BGR),m,None,bgd,fgd,6,cv2.GC_INIT_WITH_MASK)
    fg=(m==cv2.GC_FGD)|(m==cv2.GC_PR_FGD)
    fg=ndimage.binary_opening(fg,iterations=2);fg=ndimage.binary_fill_holes(fg)
    L,n=ndimage.label(fg);sz=ndimage.sum(fg,L,range(1,n+1))
    fg=np.isin(L,[i+1 for i,v in enumerate(sz) if v>.003*fg.size])
    al=Image.fromarray((fg*255).astype(np.uint8)).resize((W,H),Image.BILINEAR).filter(ImageFilter.GaussianBlur(max(1,W/900)))
    o=im.convert('RGBA');o.putalpha(al);return o
