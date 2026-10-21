import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as ndi
def bgcut(src, tol=3, mode='flood'):
    """Flood the background in from the photo edges; anything not reachable stays (so white inside a tile/mat is safe)."""
    a=np.asarray(src.convert('RGB')).astype(float)
    h,w,_=a.shape
    b=np.concatenate([a[:3].reshape(-1,3),a[-3:].reshape(-1,3),a[:,:3].reshape(-1,3),a[:,-3:].reshape(-1,3)])
    bg=np.median(b,axis=0); spread=np.abs(b-bg).max(axis=1)
    uniform=float((spread<10).mean())
    d=np.abs(a-bg).max(axis=2)
    if mode=='thresh':
        m=ndi.binary_closing(d>max(tol,14),iterations=2)
        lab,n=ndi.label(m)
        if n==0: return None,uniform
        sizes=ndi.sum(m,lab,range(1,n+1)); keep=ndi.binary_fill_holes(lab==(1+int(np.argmax(sizes))))
        keep=ndi.binary_erosion(ndi.binary_opening(keep,iterations=1),iterations=4)
        al=Image.fromarray((keep*255).astype('uint8')).filter(ImageFilter.GaussianBlur(0.8))
        out=Image.fromarray(np.dstack([a.astype('uint8'),np.asarray(al)]),'RGBA');bb=out.getbbox()
        return (out.crop(bb) if bb else out),uniform
    near=d<=tol
    lab,n=ndi.label(near)
    edge=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
    bgm=np.isin(lab,list(edge)) if edge else np.zeros_like(near)
    keep=~bgm
    keep=ndi.binary_opening(keep,iterations=1)
    lab2,n2=ndi.label(keep)
    if n2==0: return None,uniform
    sizes=ndi.sum(keep,lab2,range(1,n2+1))
    big=[i+1 for i,s in enumerate(sizes) if s>=0.02*max(sizes)]   # keep all substantial pieces (tile grids, racks)
    keep=np.isin(lab2,big)
    keep=ndi.binary_fill_holes(keep)
    al=Image.fromarray((keep*255).astype('uint8')).filter(ImageFilter.GaussianBlur(0.8))
    out=Image.fromarray(np.dstack([a.astype('uint8'),np.asarray(al)]),'RGBA')
    bb=out.getbbox(); out=out.crop(bb) if bb else out
    return out,uniform

def unroll(cut):
    """If a mat photo has a rolled-up tube attached on one side (low-saturation strip) and/or a dark shadow strip below, trim them."""
    import colorsys
    a=np.asarray(cut).copy(); al=a[...,3]>128; rgb=a[...,:3].astype(float)
    h,w=al.shape
    mx=rgb.max(axis=2); mn=rgb.min(axis=2); sat=(mx-mn)/np.maximum(mx,1)
    # shadow rows at bottom
    lum=rgb.mean(axis=2)
    bot=h
    while bot>h*0.8 and ((lum[bot-1][al[bot-1]]<60).mean()>0.5 if al[bot-1].any() else True): bot-=1
    if bot==h or lum[al].mean()<70: return cut   # no roll shadow signature: leave the mat alone
    a=a[:bot]; al=al[:bot]; sat=sat[:bot]
    # roll on right (or left): columns that are mostly low-saturation
    lowsat=((sat<0.18)&al).sum(axis=0)/np.maximum(al.sum(axis=0),1)
    right=w
    cc=al.sum(axis=0)/max(al.shape[0],1)
    while right>w*0.6 and (cc[right-1]<0.3 or lowsat[right-1]>0.35): right-=1
    left=0
    while left<w*0.4 and (cc[left]<0.3 or lowsat[left]>0.35): left+=1
    if left+(w-right)>0.25*w: return cut
    a=a[:,left:right]
    out=Image.fromarray(a,'RGBA'); bb=out.getbbox()
    return out.crop(bb) if bb else out
