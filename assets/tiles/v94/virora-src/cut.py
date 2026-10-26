import json,numpy as np
from PIL import Image,ImageDraw,ImageFilter
from scipy import ndimage
from skimage.morphology import convex_hull_image
def back_cut(im):
    a=np.asarray(im.convert('RGB')).astype(float);H,W=a.shape[:2]
    sat=a.max(2)-a.min(2)
    x0,y0=int(W*.80),int(H*.62);sub=sat[y0:,x0:]
    best=None
    for th in (40,28,18,12):
        m=ndimage.binary_opening(sub>th,iterations=2);m=ndimage.binary_closing(m,iterations=3)
        lab,n=ndimage.label(m)
        if n==0: continue
        s=ndimage.sum(m,lab,range(1,n+1));j=np.argmax(s)
        comp=lab==(j+1)
        ys,xs=np.where(comp)
        # the back tile is the big blob touching the lower-right; engraving blobs are small
        if s[j]>sub.size*0.04: best=comp;break
    hull=convex_hull_image(best)
    # grow to catch pale top/white layer: include low-sat pixels inside a dilated hull that differ from white bg
    big=ndimage.binary_dilation(hull,iterations=14)
    nonwhite=(a[y0:,x0:].min(2)<232)|(sub>10)
    grow=convex_hull_image(hull|(big&nonwhite&ndimage.binary_dilation(hull,iterations=14)))
    full=np.zeros((H,W),bool);full[y0:,x0:]=hull
    full2=np.zeros((H,W),bool);full2[y0:,x0:]=grow
    return full,full2
if __name__=='__main__':
    P=json.load(open('products.json'));rows=[]
    for k,v in P.items():
        im=Image.open(f"src/{v['handle']}_00.jpg").convert('RGB');h1,h2=back_cut(im)
        ys,xs=np.where(h2);bb=(xs.min()-10,ys.min()-10,xs.max()+10,ys.max()+10)
        al=Image.fromarray((h2*255).astype('uint8')).filter(ImageFilter.GaussianBlur(1.5))
        o=im.convert('RGBA');o.putalpha(al);o=o.crop(bb)
        bgc=Image.new('RGBA',o.size,(30,40,90,255));bgc.alpha_composite(o)
        t=bgc.convert('RGB');t.thumbnail((210,210));t2=im.crop(bb);t2.thumbnail((210,210))
        r=Image.new('RGB',(440,230),'white');r.paste(t2,(0,18));r.paste(t,(220,18));ImageDraw.Draw(r).text((2,2),v['handle'],fill='red');rows.append(r)
    S=Image.new('RGB',(880,230*8),'white')
    for j,r in enumerate(rows):S.paste(r,((j//8)*440,(j%8)*230))
    S.save('cuts.jpg',quality=85)
