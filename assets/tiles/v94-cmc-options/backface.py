import sys;sys.path.insert(0,'.')
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter
from build import box
from seg2 import cutout
def face(h,j):
    im,b=box(h,j);o=cutout(f'hi/{h}_{j:02d}.jpg');bw=b[2]-b[0];bh=b[3]-b[1]
    c=o.crop((int(b[0]-bw*.1),int(b[1]-bh*.1),int(b[2]+bw*.1),int(b[3]+bh*.1)))
    a=np.asarray(c.convert('RGB')).astype(np.uint8);hsv=cv2.cvtColor(a,cv2.COLOR_RGB2HSV)
    al=np.asarray(c)[...,3]
    m=((hsv[...,1]>110)&(hsv[...,2]>60)&(al>128)).astype(np.uint8)
    m=cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
    n,lab,st,_=cv2.connectedComponentsWithStats(m);k=1+np.argmax(st[1:,4]);m=(lab==k).astype(np.uint8)
    cnt,_=cv2.findContours(m,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE);(cx,cy),(w,hh),ang=cv2.minAreaRect(cnt[0])
    if w>hh: w,hh=hh,w;ang+=90
    M=cv2.getRotationMatrix2D((cx,cy),ang,1);r=cv2.warpAffine(a,M,(a.shape[1],a.shape[0]),flags=cv2.INTER_CUBIC,borderValue=(255,255,255))
    x0=int(cx-w/2+w*.05);x1=int(cx+w/2+w*.005);y0=int(cy-hh/2+hh*.02);y1=int(cy+hh/2+hh*.005)
    f=Image.fromarray(r[y0:y1,x0:x1]).convert('RGBA')
    mk=Image.new('L',f.size,0);ImageDraw.Draw(mk).rounded_rectangle((0,0,f.width-1,f.height-1),radius=int(f.width*.1),fill=255);f.putalpha(mk.filter(ImageFilter.GaussianBlur(1.2)))
    return f
if __name__=='__main__':
    out=Image.new('RGB',(1200,500),'white');x=0
    for h,j in [('the-country-club-edition',3),('cocktail-club-2-0',13),('the-yacht-club-edition',16)]:
        f=face(h,j);f.save(f'face_{h}.png');g=f.resize((int(f.width*450/f.height),450));out.paste(g,(x,20),g);x+=g.width+40;print(h,f.size)
    out.save('faces.jpg')
    # compose the three sets with straight-up backs (same layout as approved Apres Ski)
    from build import W, H, crops
    for h,j in [('the-country-club-edition',3),('cocktail-club-2-0',13),('the-yacht-club-edition',16)]:
        base=Image.open(f'opt/D_{h}.jpg').convert('RGBA');c=Image.new('RGBA',(W,H),(255,255,255,255));c.alpha_composite(base.crop((0,0,800,700)))
        f=Image.open(f'face_{h}.png');bk=f.resize((int(f.width*175/f.height),175),Image.LANCZOS)
        for cx,cy,a in [(905,165,-14),(1010,350,10),(905,540,-6),(1210,230,12),(1370,470,-9),(1500,200,5)]:
            t=bk.rotate(a,expand=True,resample=Image.BICUBIC);c.alpha_composite(t,(int(cx-t.width/2),int(cy-t.height/2)))
        ImageDraw.Draw(c).rectangle((796,0,803,700),fill=(255,255,255,255));c.convert('RGB').save(f'opt/E_{h}.jpg',quality=90)
    rows=[]
    for h in ['the-country-club-edition','cocktail-club-2-0','the-yacht-club-edition','the-hunt-club-edition','apres-ski-edition-tile-set']:
        p=f'opt/E_{h}.jpg' if h in ('the-country-club-edition','cocktail-club-2-0','the-yacht-club-edition') else f'opt/D_{h}.jpg'
        c=Image.open(p);s,cc,band=crops(c);r=Image.new('RGB',(900,290),'white');r.paste(s,(0,14));r.paste(cc,(620,14));rows.append(r)
    S=Image.new('RGB',(900,290*5),'white')
    for i,r in enumerate(rows):S.paste(r,(0,i*290))
    S.save('cmc_all5.jpg',quality=88)
