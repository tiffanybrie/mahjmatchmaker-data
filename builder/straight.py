import numpy as np,io,subprocess
from PIL import Image,ImageFilter
from scipy.ndimage import binary_opening,binary_fill_holes,label,binary_erosion
def get(u):return subprocess.run(['curl','-s','-m','25','-L',u],capture_output=True).stdout
def _mask(rgba_or_rgb,bg,thr,only=False):
    a=np.asarray(rgba_or_rgb.convert('RGB')).astype(int);d=np.abs(a-bg).max(2);m=d>thr
    m=binary_opening(m,iterations=2);lab,n=label(m)
    if n>1:
        s=np.bincount(lab.ravel());s[0]=0;m=(s==s.max())[lab] if only else (s>s.max()*0.15)[lab]
    return binary_fill_holes(m)
def straight(url,thr=24,only=False,trim=True):
    im=Image.open(io.BytesIO(get(url+('&' if '?' in url else '?')+'width=1400'))).convert('RGB')
    a=np.asarray(im).astype(int);bg=np.median(np.concatenate([a[:10].reshape(-1,3),a[-10:].reshape(-1,3)]),axis=0)
    m=_mask(im,bg,thr,only)
    ys,xs=np.nonzero(m);pts=np.stack([xs,ys],1).astype(float);pts-=pts.mean(0)
    ev,evec=np.linalg.eigh(np.cov(pts.T));v=evec[:,ev.argmax()];ang=np.degrees(np.arctan2(v[1],v[0]))
    def rot(img,deg):return img.rotate(deg,resample=Image.BICUBIC,expand=True,fillcolor=tuple(int(x) for x in bg))
    # refine: level the top edge of the rack
    for _ in range(3):
        r=rot(im,ang);mm=_mask(r,bg,thr,only);cols=np.nonzero(mm.any(0))[0]
        c0,c1=cols[0],cols[-1];w=c1-c0;xs2=np.arange(int(c0+w*.1),int(c0+w*.75));tops=np.array([np.argmax(mm[:,x]) for x in xs2])
        k=np.polyfit(xs2,tops,1)[0];d=np.degrees(np.arctan(k))
        if abs(d)<0.15:break
        ang+=d
    r=rot(im,ang);mm=_mask(r,bg,thr,only)
    if not trim:
        al=Image.fromarray((binary_erosion(mm,iterations=1)*255).astype('uint8')).filter(ImageFilter.GaussianBlur(1));out=r.convert('RGBA');out.putalpha(al);bb=out.getbbox();return out.crop(bb),ang
    cols=np.nonzero(mm.any(0))[0];c0,c1=cols[0],cols[-1];w=c1-c0
    runs=[]
    for x in range(int(c0+w*.1),int(c0+w*.6)):
        col=mm[:,x];t=np.argmax(col);L=np.argmax(~col[t:]) if (~col[t:]).any() else len(col)-t;runs.append((t,L))
    top=int(np.median([t for t,_ in runs]));band=int(np.median([L for _,L in runs]))
    keep=np.zeros_like(mm);keep[max(0,top-3):top+band+3]=True;mm=mm&keep
    mm=binary_erosion(mm,iterations=1)
    al=Image.fromarray((mm*255).astype('uint8')).filter(ImageFilter.GaussianBlur(1))
    out=r.convert('RGBA');out.putalpha(al);bb=out.getbbox();return out.crop(bb),ang
