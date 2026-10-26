import json,numpy as np
from PIL import Image
from scipy import ndimage
from split import make, M
def objs(p,thr=238):
    im=Image.open(p).convert('RGB');a=np.asarray(im.convert('L'))<thr
    a=ndimage.binary_closing(a,iterations=3);lab,n=ndimage.label(a)
    sl=[s for s in ndimage.find_objects(lab) if (s[0].stop-s[0].start)*(s[1].stop-s[1].start)>im.width*im.height*0.01]
    sl=sorted(sl,key=lambda s:s[1].start)
    return im,[(s[1].start,s[0].start,s[1].stop,s[0].stop) for s in sl]
def tile(im,b,h,pad=6):
    t=im.crop((b[0]-pad,b[1]-pad,b[2]+pad,b[3]+pad));return t.resize((int(t.width*h/t.height),h),Image.LANCZOS)
def canvas(): return Image.new('RGB',(1600,700),'white')
# Canyon Clay: faces tray (img 6) | one whole back tile from YMI's joker/side/back shot (img 5)
def canyon():
    h='fx-am021-a';M[h]=(6,6);c=make(h)  # left half from faces tray
    c.paste(Image.new('RGB',(796,700),'white'),(804,0))
    im,bx=objs(f'img/{h}/05.jpg');t=tile(im,bx[-1],360);c.paste(t,(950-t.width//2,350-t.height//2));return c
# Ivory Stripes: no faces tray on YMI -> Joker from img 5 (left) | backs tray img 6 (right)
def ivory():
    h='fx-am014-a';c=canvas()
    im,bx=objs(f'img/{h}/05.jpg');t=tile(im,bx[0],360);c.paste(t,(650-t.width//2,350-t.height//2))
    b=Image.open(f'img/{h}/06.jpg').convert('RGB')
    a=np.asarray(b.convert('L'))<225;cols=np.where(a.mean(0)>.03)[0];rows=np.where(a.mean(1)>.03)[0]
    L,T=cols[0]+30,rows[0]+30;c.paste(b.crop((L,T,L+915,T+800)).resize((796,700),Image.LANCZOS),(804,0));return c
# Outlaws of the Marsh: only a 500px face/side/back shot -> face tile | back tile
def outlaws():
    h='hb-at002-a';c=canvas();im,bx=objs(f'img/{h}/00.jpg')
    print('outlaws objs',bx)
    f=tile(im,bx[0],360,3);b=tile(im,bx[-1],360,3);c.paste(f,(650-f.width//2,350-f.height//2));c.paste(b,(950-b.width//2,350-b.height//2));return c
if __name__=='__main__':
    for h,fn in [('fx-am021-a',canyon),('fx-am014-a',ivory),('hb-at002-a',outlaws)]:
        fn().save(f'out/{h}.jpg',quality=90)
