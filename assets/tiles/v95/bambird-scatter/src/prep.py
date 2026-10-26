import numpy as np, cv2, glob
from PIL import Image, ImageDraw, ImageFilter
B='/tmp/claude-0/-home-claude/05549d34-8fe3-5ca9-a6a5-308991cb9a78/scratchpad/bbt/'
TR={'classic':('east-meets-west-tortoise-shell-tile-set-copy_01.jpg',1017,2402,192.9,271.0),'emw':('east-meets-west-tortoise-shell-tile-set_00.jpg',1060,2175,227.7,316.7)}
PICK=[(3,4),(3,5),(3,6),(3,7),(3,8),(3,9),(1,9),(2,9),(3,0),(3,1),(3,2),(1,0),(0,4),(0,0),(2,4),(1,4)]
def rr(w,h,r):
    m=Image.new('L',(w,h),0);ImageDraw.Draw(m).rounded_rectangle((0,0,w-1,h-1),radius=r,fill=255);return m.filter(ImageFilter.GaussianBlur(1.2))
for k,(f,x0,y0,pw,ph) in TR.items():
    im=Image.open(B+f).convert('RGB')
    faces=[]
    for r,c in PICK:
        t=im.crop((int(x0+c*pw+5),int(y0+r*ph+5),int(x0+(c+1)*pw-5),int(y0+(r+1)*ph-5))).convert('RGBA')
        t.putalpha(rr(t.width,t.height,int(t.width*.09)));faces.append(t)
    backs=[]
    for p in sorted(glob.glob(f'{k}_back*.png')):
        b=Image.open(p);a=np.asarray(b)[...,3]>128
        cnt,_=cv2.findContours(a.astype(np.uint8),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE);c=max(cnt,key=cv2.contourArea)
        (cx,cy),(w,h),ang=cv2.minAreaRect(c);rect=a.sum()/(w*h)
        if w>h: w,h=h,w;ang+=90
        ratio=h/w
        if rect<0.9 or not(1.15<ratio<1.55): print('skip',p,round(rect,2),round(ratio,2));continue
        rgb=np.asarray(b.convert('RGB'));M=cv2.getRotationMatrix2D((cx,cy),ang,1)
        rot=cv2.warpAffine(rgb,M,(rgb.shape[1],rgb.shape[0]),flags=cv2.INTER_CUBIC,borderValue=(255,255,255))
        ins=0.05;crop=rot[int(cy-h/2+h*ins):int(cy+h/2-h*ins),int(cx-w/2+w*ins):int(cx+w/2-w*ins)]
        t=Image.fromarray(crop).convert('RGBA');t.putalpha(rr(t.width,t.height,int(t.width*.09)));backs.append(t)
    for j,t in enumerate(faces): t.save(f'u_{k}_f{j:02d}.png')
    for j,t in enumerate(backs): t.save(f'u_{k}_b{j:02d}.png')
    S=Image.new('RGB',(16*130,2*190),(230,230,230))
    for j,t in enumerate(faces): u=t.copy();u.thumbnail((120,180));S.paste(u,(j*130,5),u)
    for j,t in enumerate(backs): u=t.copy();u.thumbnail((120,180));S.paste(u,(j*130,195),u)
    S.save(f'u_{k}.jpg');print(k,len(faces),len(backs),faces[0].size,backs[0].size if backs else None)
