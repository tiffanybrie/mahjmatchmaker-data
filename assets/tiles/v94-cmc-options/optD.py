import json,sys
sys.path.insert(0,'.')
from PIL import Image, ImageDraw
from seg2 import cutout
from build import box, SETS, crops, W, H
def optD(h,j):
    im,b=box(h,j);o=cutout(f'hi/{h}_{j:02d}.jpg')
    c=Image.new('RGBA',(W,H),(255,255,255,255))
    bb=o.getbbox();fx1=min(bb[2],int(b[0])-4);faces=o.crop((bb[0],bb[1],fx1,bb[3]))
    s=700/faces.height;faces=faces.resize((int(faces.width*s),700),Image.LANCZOS)
    left=faces.crop((faces.width-800,0,faces.width,700)) if faces.width>=800 else faces
    c.alpha_composite(left,(800-left.width,0))
    bw=b[2]-b[0];bh=b[3]-b[1];pad=.03
    back=o.crop((int(b[0]-bw*pad),int(b[1]-bh*pad),int(b[2]+bw*pad),int(b[3]+bh*pad)))
    s=175/back.height;back=back.resize((int(back.width*s),175),Image.LANCZOS)
    # 3 whole tiles inside the match-card circle (centre 800,350 r 350), 3 more to fill the swipe strip
    for cx,cy,a in [(905,165,-14),(1010,350,10),(905,540,-6),(1210,230,12),(1370,470,-9),(1500,200,5)]:
        t=back.rotate(a,expand=True,resample=Image.BICUBIC);c.alpha_composite(t,(int(cx-t.width/2),int(cy-t.height/2)))
    d=ImageDraw.Draw(c);d.rectangle((796,0,803,700),fill=(255,255,255,255));return c.convert('RGB')
rows=[]
for h,name,ja,jb in SETS:
    c=optD(h,jb);c.save(f'opt/D_{h}.jpg',quality=90);s,cc,band=crops(c)
    r=Image.new('RGB',(900,290),'white');r.paste(s,(0,14));r.paste(cc,(620,14));ImageDraw.Draw(r).text((4,0),name,fill='black');rows.append(r)
S=Image.new('RGB',(900,290*len(rows)),'white')
for i,r in enumerate(rows):S.paste(r,(0,i*290))
S.save('option_D.jpg',quality=88)
