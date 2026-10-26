import sys;sys.path.insert(0,'.')
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage
from build import crops, W, H
f=Image.open('hunt/full12.jpg').convert('RGB');s=f.width/1200
back=f.crop((int(468*s),int(500*s),int(678*s),int(797*s)))
m=Image.new('L',back.size,0);ImageDraw.Draw(m).rounded_rectangle((0,0,back.width-1,back.height-1),radius=int(back.width*.09),fill=255)
back.putalpha(m.filter(ImageFilter.GaussianBlur(1.5)));back.save('hunt/back.png')
# faces: image 2, key out the red-brown leather (tiles are mint, back tile at bottom right is excluded)
g=Image.open('hunt/full2.jpg').convert('RGB');a=np.asarray(g).astype(int)
r,gg,b=a[...,0],a[...,1],a[...,2]
tile=(gg>r-10)|((r+gg+b)>600)
tile=ndimage.binary_opening(tile,iterations=2);tile=ndimage.binary_closing(tile,iterations=8);tile=ndimage.binary_fill_holes(tile)
lab,n=ndimage.label(tile);keep=lab==(np.argmax(ndimage.sum(tile,lab,range(1,n+1)))+1)
al=Image.fromarray((keep*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
fc=g.copy();fc.putalpha(al);fc=fc.crop(fc.getbbox());fc.save('hunt/faces.png');print(fc.size,back.size)
c=Image.new('RGBA',(W,H),(255,255,255,255))
sc=700/fc.height;fz=fc.resize((int(fc.width*sc),700),Image.LANCZOS)
left=fz.crop((fz.width-800,0,fz.width,700)) if fz.width>800 else fz
c.alpha_composite(left,(800-left.width,0))
bk=back.resize((int(back.width*175/back.height),175),Image.LANCZOS)
for cx,cy,ang in [(905,165,-14),(1010,350,10),(905,540,-6),(1210,230,12),(1370,470,-9),(1500,200,5)]:
    t=bk.rotate(ang,expand=True,resample=Image.BICUBIC);c.alpha_composite(t,(int(cx-t.width/2),int(cy-t.height/2)))
ImageDraw.Draw(c).rectangle((796,0,803,700),fill=(255,255,255,255));c=c.convert('RGB');c.save('opt/D_the-hunt-club-edition.jpg',quality=90)
sw,cc,band=crops(c);r=Image.new('RGB',(1600,1200),'white');r.paste(c,(0,0));r.paste(cc.resize((440,440)),(40,740));r.paste(band.resize((1000,257)),(540,740));r.save('hunt_D_preview.jpg',quality=88)
