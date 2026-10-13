import sys,json,numpy as np
from PIL import Image
def crop_mat(p,out,size=1100):
    im=Image.open(p).convert('RGB'); a=np.asarray(im).astype(int); nb=~(a.min(2)>235); ys,xs=np.where(nb)
    c=im.crop((xs.min(),ys.min(),xs.max(),ys.max())); w,h=c.size; s=min(w,h); c=c.crop(((w-s)//2,(h-s)//2,(w-s)//2+s,(h-s)//2+s)).resize((size,size)); c.save(out,quality=90); return out
def lab(rgb):
    c=rgb/255.0;c=np.where(c>0.04045,((c+0.055)/1.055)**2.4,c/12.92)
    M=np.array([[0.4124,0.3576,0.1805],[0.2126,0.7152,0.0722],[0.0193,0.1192,0.9505]])
    xyz=c@M.T/np.array([0.9505,1.0,1.089]);f=np.where(xyz>0.008856,np.cbrt(xyz),7.787*xyz+16/116)
    return np.stack([116*f[...,1]-16,500*(f[...,0]-f[...,1]),200*(f[...,1]-f[...,2])],-1)
def palette(p,k=6,seed=1):
    a=np.asarray(Image.open(p).convert('RGB').resize((160,160)),float).reshape(-1,3)
    L=lab(a); rng=np.random.default_rng(seed); C=L[rng.choice(len(L),k,replace=False)]
    for _ in range(25):
        d=((L[:,None]-C[None])**2).sum(-1); lb=d.argmin(1)
        C=np.array([L[lb==j].mean(0) if (lb==j).any() else C[j] for j in range(k)])
    out=[]
    for j in range(k):
        m=lb==j; rgb=a[m].mean(0); out.append(('#%02x%02x%02x'%tuple(int(v) for v in rgb), float(m.mean()), C[j].tolist()))
    # merge near-duplicates
    out.sort(key=lambda x:-x[1]); res=[]
    for h,s,l in out:
        if all(np.linalg.norm(np.array(l)-np.array(r[2]))>12 for r in res): res.append((h,s,l))
    return res
if __name__=='__main__':
    crop_mat(sys.argv[1],sys.argv[2]); print(json.dumps([(h,round(s,3)) for h,s,_ in palette(sys.argv[2],int(sys.argv[3]) if len(sys.argv)>3 else 7)]))
