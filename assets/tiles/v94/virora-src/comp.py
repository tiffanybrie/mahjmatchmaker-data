import json,numpy as np,os
from PIL import Image,ImageDraw,ImageFilter
from scipy import ndimage
from cut import back_cut
W,H=1600,700
POS=[(915,175,-12,1),(1035,360,9,1),(905,545,-4,1),(1240,215,14,0),(1400,480,-10,0),(1505,170,6,0)]
def grid_box(im,hull):
    a=np.asarray(im).astype(float);sat=a.max(2)-a.min(2)
    g=a.mean(2);gm=np.hypot(ndimage.sobel(g,0),ndimage.sobel(g,1))
    m=(gm>60)|(sat>40);m&=~ndimage.binary_dilation(hull,iterations=60);b=12;m[:b]=0;m[-b:]=0;m[:,:b]=0;m[:,-b:]=0
    m=ndimage.binary_dilation(m,iterations=3)
    rows=np.where(m.sum(1)>m.shape[1]*.08)[0];cols=np.where(m.sum(0)>m.shape[0]*.08)[0]
    return cols.min(),rows.min(),cols.max(),rows.max()
def make(handle,size=205):
    im=Image.open(f"src/{handle}_00.jpg").convert('RGB');_,hull=back_cut(im)
    gx0,gy0,gx1,gy1=grid_box(im,hull)
    faces=im.crop((gx0,gy0,gx1,gy1));s=H/faces.height;faces=faces.resize((int(faces.width*s),H),Image.LANCZOS)
    c=Image.new('RGB',(W,H),'white');c.paste(faces.crop((0,0,796,H)),(0,0))
    ys,xs=np.where(hull);bb=(xs.min()-6,ys.min()-6,xs.max()+7,ys.max()+7)
    al=Image.fromarray((hull*255).astype('uint8')).filter(ImageFilter.GaussianBlur(1.2))
    o=im.convert('RGBA');o.putalpha(al);o=o.crop(bb);sc=size/max(o.size);o=o.resize((int(o.width*sc),int(o.height*sc)),Image.LANCZOS)
    cc=c.convert('RGBA');bad=0
    for cx,cy,ang,inc in POS:
        t=o.rotate(ang,expand=True,resample=Image.BICUBIC);x,y=int(cx-t.width/2),int(cy-t.height/2)
        if inc:
            A=np.asarray(t)[...,3]>40;yy,xx=np.nonzero(A);d=np.hypot(xx+x-800,yy+y-350);bad+=int((d>346).sum())
        cc.alpha_composite(t,(x,y))
    c=cc.convert('RGB');ImageDraw.Draw(c).rectangle((796,0,803,H),fill='white')
    return c,bad,(gx0,gy0,gx1,gy1)
if __name__=='__main__':
    P=json.load(open('products.json'));os.makedirs('out',exist_ok=True);info={}
    for k,v in P.items():
        c,bad,gb=make(v['handle']);c.save(f"out/virora-{v['handle']}-split.jpg",quality=90);info[k]=dict(handle=v['handle'],bad=bad,grid=[int(x) for x in gb]);print(v['handle'],'outside-circle px',bad,gb)
    json.dump(info,open('out/info.json','w'),indent=1)
