import numpy as np,cv2,sys
from PIL import Image
from scipy import ndimage
def clean(im):
    a=np.asarray(im.convert('RGB'));hsv=cv2.cvtColor(a,cv2.COLOR_RGB2HSV).astype(int)
    H,S,V=hsv[...,0],hsv[...,1],hsv[...,2]
    br=(S>50)&((H<22)|(H>165))
    dark=(V<125)&br
    lab,n=ndimage.label(dark);keep=np.zeros_like(dark)
    for k in range(1,n+1):
        m=lab==k
        if m.sum()>250 and V[m].mean()<100: keep|=m
    keep=ndimage.binary_closing(keep,iterations=2)
    edge=ndimage.binary_dilation(keep,iterations=3)&(V<150)&br
    m=keep|edge
    for _ in range(3): m=m|(ndimage.binary_dilation(m,iterations=3)&(((V<110)&(S>35))|(V<70)))
    al=cv2.GaussianBlur((m*255).astype(np.uint8),(3,3),0)/255.
    return Image.fromarray((a*(1-al[...,None])+255*al[...,None]).astype(np.uint8))
if __name__=='__main__':
    a=Image.open('hb_cur.jpg').convert('RGB');o=clean(a);o.save('hb_clean.jpg',quality=92)
    S2=Image.new('RGB',(2280,1190),'white');S2.paste(a.resize((1140,1190)),(0,0));S2.paste(o.resize((1140,1190)),(1140,0));S2.save('hb_ba.jpg',quality=88)
