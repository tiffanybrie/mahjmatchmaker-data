import cv2,numpy as np,json
from PIL import Image, ImageDraw
def rect_crop(f,c,sz,ang,inset=0.03):
    im=cv2.imread(f);box=cv2.boxPoints((tuple(c),tuple(sz),ang)).astype(np.float32)
    # order points tl,tr,br,bl
    s=box.sum(1);d=np.diff(box,axis=1).ravel()
    tl=box[np.argmin(s)];br=box[np.argmax(s)];tr=box[np.argmin(d)];bl=box[np.argmax(d)]
    W=int(max(np.linalg.norm(tr-tl),np.linalg.norm(br-bl)));H=int(max(np.linalg.norm(bl-tl),np.linalg.norm(br-tr)))
    M=cv2.getPerspectiveTransform(np.array([tl,tr,br,bl]),np.float32([[0,0],[W,0],[W,H],[0,H]]))
    o=cv2.warpPerspective(im,M,(W,H))
    if H>W:o=cv2.rotate(o,cv2.ROTATE_90_CLOCKWISE)
    h,w=o.shape[:2];o=o[int(h*inset):int(h*(1-inset)),int(w*inset):int(w*(1-inset))]
    return Image.fromarray(cv2.cvtColor(o,cv2.COLOR_BGR2RGB))
def faces_crop(f,box,pad=0.0):
    im=Image.open(f).convert('RGB').crop(box);a=np.asarray(im).astype(int)
    hsv=cv2.cvtColor(np.asarray(im),cv2.COLOR_RGB2HSV)
    ink=(hsv[...,1]>60)|(a.min(2)<140)
    ink=cv2.morphologyEx(ink.astype(np.uint8),cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    ys,xs=np.where(ink);
    # robust bbox: 0.3/99.7 percentiles
    x0,x1=np.percentile(xs,[0.2,99.8]);y0,y1=np.percentile(ys,[0.2,99.8])
    return im.crop((int(x0),int(y0),int(x1),int(y1)))
def half(im,align):
    s=700/im.height;im=im.resize((max(800,round(im.width*s)),700),Image.LANCZOS)
    return im.crop((im.width-800,0,im.width,700)) if align=='right' else im.crop((0,0,800,700))
def split(F,B,out):
    c=Image.new('RGB',(1600,700),'white');c.paste(half(F,'right'),(0,0));c.paste(half(B,'left'),(800,0))
    ImageDraw.Draw(c).rectangle((796,0,803,700),fill='white');c.save(out,quality=90);return c
def box_crop(f,b,inset=0.04):
    x,y,w,h=b
    if isinstance(inset,tuple):
        l,t,r,bt=inset;return Image.open(f).convert('RGB').crop((int(x+w*l),int(y+h*t),int(x+w*(1-r)),int(y+h*(1-bt))))
    return Image.open(f).convert('RGB').crop((int(x+w*inset),int(y+h*inset),int(x+w*(1-inset)),int(y+h*(1-inset))))
P='F_%s.jpg'
S={}
fb=faces_crop(P%'boots-bubbles-mahjong-tile-set_00',(720,1584,1776,2184))
S['boots-blue']=(fb,box_crop(P%'boots-bubbles-mahjong-tile-set_00',(310,2397,1101,631)))
S['boots-pink']=(fb,box_crop(P%'boots-bubbles-mahjong-tile-set_00',(1113,736,1068,615)))
fm=faces_crop(P%'mcm-mahjong-tile-set_16',(168,912,1656,1752))
S['mcm-navy-olive']=(fm,box_crop(P%'mcm-mahjong-tile-set_16',(674,2006,1532,901)))
S['mcm-olive-pink']=(fm,box_crop(P%'mcm-mahjong-tile-set_14',(723,2010,1540,895),(0.04,0.11,0.04,0.04)))
fc=faces_crop(P%'tiles-box-die_00',(672,1138,1776,1752))
S['classic-rose']=(fc,box_crop(P%'tiles-box-die_00',(313,373,1162,621)))
S['classic-lavender']=(fc,box_crop(P%'tiles-box-die_00',(934,1856,1194,692),(0.05,0.08,0.05,0.05)))
S['classic-teal']=(fc,box_crop(P%'tiles-box-die_00',(363,2567,1189,777),(0.07,0.13,0.07,0.13)))
fe=faces_crop(P%'east-meets-west-tile-set_03',(864,960,2160,1656))
S['emw-emerald']=(fe,box_crop(P%'east-meets-west-tile-set_01',(191,940,1434,867),(0.06,0.1,0.06,0.06)))
S['emw-periwinkle']=(fe,box_crop(P%'east-meets-west-tile-set_03',(214,1943,1395,842),(0.05,0.09,0.05,0.06)))
fo=faces_crop(P%'origami-tile-set_01',(336,1256,2160,2256))
S['origami-azure']=(fo,rect_crop(P%'origami-tile-set_02',(1519,1071),(1435,834),-22.3,0.065))
S['origami-timber']=(fo,rect_crop(P%'origami-tile-set_03',(1031,1060),(1517,894),-43.5))
rows=[]
for k,(F,B) in S.items():
    F.save(f'faces_{k}.jpg');B.save(f'backs_{k}.jpg')
    c=split(F,B,f'bam-bird-{k}-split.jpg');sq=c.crop((450,0,1150,700)).resize((280,280))
    r=Image.new('RGB',(940,300),'white');r.paste(c.resize((640,280)),(0,0));r.paste(sq,(660,0));ImageDraw.Draw(r).text((5,285),k,fill='black');rows.append(r)
sh=Image.new('RGB',(1880,((len(rows)+1)//2)*300),'white')
for i,r in enumerate(rows):sh.paste(r,((i%2)*940,(i//2)*300))
sh.save('contact.jpg',quality=85)
