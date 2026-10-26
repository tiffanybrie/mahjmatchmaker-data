import numpy as np, sys, json
from PIL import Image
from scipy import ndimage
B='/tmp/claude-0/-home-claude/05549d34-8fe3-5ca9-a6a5-308991cb9a78/scratchpad/bbt/'
for f in ['east-meets-west-tortoise-shell-tile-set-copy_01.jpg','east-meets-west-tortoise-shell-tile-set_00.jpg']:
    im=Image.open(B+f).convert('RGB');a=np.asarray(im).astype(int)
    mx=a.max(2);mn=a.min(2);sat=mx-mn
    dark=(mx<170)|(sat>60)   # tortoise / colored stuff
    dark=ndimage.binary_opening(dark,iterations=3);dark=ndimage.binary_closing(dark,iterations=6);dark=ndimage.binary_fill_holes(dark)
    lab,n=ndimage.label(dark);objs=ndimage.find_objects(lab);sz=ndimage.sum(dark,lab,range(1,n+1))
    out=[]
    for i,(sl,s) in enumerate(zip(objs,sz)):
        if s<20000: continue
        y0,y1=sl[0].start,sl[0].stop;x0,x1=sl[1].start,sl[1].stop
        out.append(dict(i=i+1,box=[x0,y0,x1,y1],area=int(s)))
    print(f,len(out));[print(o) for o in sorted(out,key=lambda o:-o['area'])[:30]]
