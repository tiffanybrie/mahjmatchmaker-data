import numpy as np, cv2, sys, glob, os
from PIL import Image, ImageDraw, ImageFont
F='/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf'
PINK=(245,108,140)
TXT='MATCHING MAHJONG TILES, MATS & RACKS'
def clean(img, box=(380,1008,725,1044)):
    a=np.asarray(img.convert('RGB')).copy()
    x0,y0,x1,y1=box
    g=cv2.cvtColor(a,cv2.COLOR_RGB2GRAY).astype(int)
    bg=cv2.medianBlur(g.astype(np.uint8),21).astype(int)
    m=np.zeros(g.shape,np.uint8)
    m[y0:y1,x0:x1]=((g-bg)[y0:y1,x0:x1]>14).astype(np.uint8)*255
    m=cv2.dilate(m,np.ones((5,5),np.uint8))
    out=cv2.inpaint(a,m,7,cv2.INPAINT_TELEA)
    return Image.fromarray(out)
def text_img(style, width=420):
    # render text with tracking to fit width
    for size in range(30,8,-1):
        f=ImageFont.truetype(F,size); tr=size*0.18
        w=sum(f.getlength(c) for c in TXT)+tr*(len(TXT)-1)
        if w<=width-(24 if style=='ribbon' else 0): break
    H=int(size*1.9); W=int(w+(28 if style=='ribbon' else 4))
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    if style=='ribbon': d.rectangle((0,0,W,H),fill=PINK+(255,))
    x=(W-w)/2; y=(H-size*1.25)/2
    for c in TXT:
        d.text((x,y),c,font=f,fill=(255,255,255,255)); x+=f.getlength(c)+tr
    return im,size
def apply(path,style,out,cx=540,cy=1026,width=400):
    img=clean(Image.open(path)).convert('RGBA')
    t,s=text_img(style,width); img.alpha_composite(t,(int(cx-t.width/2),int(cy-t.height/2)))
    img.convert('RGB').save(out,quality=94)
if __name__=='__main__':
    apply(sys.argv[1],sys.argv[2],sys.argv[3])
