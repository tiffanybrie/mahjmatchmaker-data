import numpy as np, colorsys
from PIL import Image
from scipy import ndimage as ndi
def make_blank():
    im=Image.open('/tmp/mb/p6.png').convert('RGBA')
    c=im.crop((380,1730,1790,1945));a=np.asarray(c).astype(float)
    mx=a[...,:3].max(2);mn=a[...,:3].min(2);sat=(mx-mn)/np.maximum(mx,1)
    m=(a[...,3]>200)&(sat>0.35)
    lab,n=ndi.label(ndi.binary_closing(m,iterations=3));sz=ndi.sum(m,lab,range(1,n+1));k=1+int(np.argmax(sz))
    keep=ndi.binary_fill_holes(lab==k)
    out=np.asarray(c).copy();out[...,3]=(keep*255).astype('uint8')
    r=Image.fromarray(out,'RGBA');r=r.crop(r.getbbox());r.save('/tmp/mb/bb_blank.png');return r
def recolor(blank,hexc):
    a=np.asarray(blank).astype(float);rgb=a[...,:3]/255;al=a[...,3]
    lum=0.299*rgb[...,0]+0.587*rgb[...,1]+0.114*rgb[...,2]
    m=lum[al>128];ref=np.median(m)
    ratio=lum/ref                                   # shading relative to the rack's base tone
    t=np.array([int(hexc[i:i+2],16) for i in (1,3,5)])/255.
    shade=np.clip(0.55+0.45*ratio,0.35,1.5)         # soften contrast so the colour stays true
    out=np.clip(t[None,None,:]*shade[...,None],0,1)
    # lift highlights toward white a little on bright pixels
    hi=np.clip(ratio-1.0,0,1)[...,None]*0.5
    out=np.clip(out+(1-out)*hi,0,1)
    res=np.dstack([out*255,al]).astype('uint8')
    return Image.fromarray(res,'RGBA')
if __name__=='__main__':
    import json
    b=make_blank();print(b.size)
    B={x['name']:x['hex'] for x in json.load(open('/home/claude/mahjmatchmaker-data/work/bbracks.json'))}
    names=['Light Blue','French Blue','Hot Pink','Light Pink','Sunshine','Teal','Kelly Green','Dark Blue','Ballet Pink','Magenta','Forest Green','Almond']
    W=Image.new('RGB',(1000,60*len(names)//2+60),(255,255,255))
    for i,n in enumerate(names):
        if n not in B: print('missing',n);continue
        r=recolor(b,B[n]);r.thumbnail((470,52));W.paste(r,((i%2)*500,(i//2)*60+4),r)
    W.save('/tmp/mb/bb_tests.png')
