"""Bespoke tile flat-lays shot/cut on pure black -> same real photo on white (Tiffany Oct 26 8:50am).
Only the edge band (3px out / 2px in) is un-premultiplied off black; tile pixels are untouched."""
import sys, numpy as np
from PIL import Image
from scipy import ndimage
def towhite(im):
    a=np.asarray(im.convert('RGB')).astype(float)/255
    core=ndimage.binary_fill_holes(a.max(2)>0.25)
    lab,n=ndimage.label(core);core=lab==(np.argmax(ndimage.sum(core,lab,range(1,n+1)))+1)
    inner=ndimage.binary_erosion(core,iterations=2);band=ndimage.binary_dilation(core,iterations=3)&~inner
    ref=ndimage.grey_dilation(a.max(2),size=9);e=np.clip(a.max(2)/np.maximum(ref,1e-3),0,1)
    al=np.where(inner,1.0,np.where(band,e,0.0))
    col=np.where(band[...,None],np.clip(a/np.maximum(al[...,None],1e-3),0,1),a)
    out=col*al[...,None]+(1-al[...,None]);o=Image.fromarray((out*255).round().astype(np.uint8))
    return o.crop(Image.fromarray(((al>0.02)*255).astype(np.uint8)).getbbox())
def strip(o):
    s=660/o.height;o=o.resize((round(o.width*s),660),Image.LANCZOS)
    if o.width>1560: o=o.resize((1560,round(o.height*1560/o.width)),Image.LANCZOS)
    c=Image.new('RGB',(1600,700),'white');c.paste(o,((1600-o.width)//2,(700-o.height)//2));return c
if __name__=='__main__':
    strip(towhite(Image.open(sys.argv[1]))).save(sys.argv[2],quality=90)
