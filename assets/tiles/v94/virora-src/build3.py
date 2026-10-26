import json,numpy as np,os,sys
from PIL import Image,ImageDraw
from scipy import ndimage
# Virora's own 3x3 studio grids. key -> (handle, back-centre grid img, faces grid L, faces grid R). Picked by eye Oct 26.
PICK={'hol:nivalee-blue':('nivalee-glacier-blue',10,7,8),'hol:tinselle-emerald':('tinselle-emerald-green',9,5,6),'hol:tinselle-ruby':('ruby-christmas',9,5,6),
'www.viroramahjong.com/christmas-collection-ii-nivalee':('christmas-collection-ii-nivalee',7,6,8),'www.viroramahjong.com/sylvaria':('sylvaria',8,5,6),
'www.viroramahjong.com/aveline':('aveline',11,8,9),'www.viroramahjong.com/yellow-lilacee':('yellow-lilacee',10,7,8),
'www.viroramahjong.com/marivelle':('marivelle',9,6,7),'www.viroramahjong.com/petalee':('petalee',8,5,6)}
def gridbox(im):
    s=4;sm=im.resize((im.width//s,im.height//s));a=np.asarray(sm).astype(float)
    g=a.mean(2);sat=a.max(2)-a.min(2);gm=np.hypot(ndimage.sobel(g,0),ndimage.sobel(g,1))
    m=(gm>50)|(sat>40);b=6;m[:b]=0;m[-b:]=0;m[:,:b]=0;m[:,-b:]=0;m=ndimage.binary_dilation(m,iterations=2)
    r=np.where(m.sum(1)>m.shape[1]*.06)[0];c=np.where(m.sum(0)>m.shape[0]*.06)[0]
    return c.min()*s,r.min()*s,c.max()*s,r.max()*s
def panel(path,w,h=700,pad=.05):
    im=Image.open(path).convert('RGB');x0,y0,x1,y1=gridbox(im);cx,cy=(x0+x1)/2,(y0+y1)/2
    gw,gh=(x1-x0)*(1+2*pad),(y1-y0)*(1+2*pad)
    if gw/gh>w/h: gh=gw*h/w
    else: gw=gh*w/h
    return im.crop((int(cx-gw/2),int(cy-gh/2),int(cx+gw/2),int(cy+gh/2))).resize((w,h),Image.LANCZOS)
if __name__=='__main__':
    src=sys.argv[1] if len(sys.argv)>1 else 'src';out=sys.argv[2] if len(sys.argv)>2 else 'out3'
    os.makedirs(out,exist_ok=True);rows=[]
    for k,(hd,b,f1,f2) in PICK.items():
        c=Image.new('RGB',(1600,700),'white')
        c.paste(panel(f'{src}/{hd}_{f1:02d}.jpg',536),(0,0));c.paste(panel(f'{src}/{hd}_{b:02d}.jpg',512),(544,0));c.paste(panel(f'{src}/{hd}_{f2:02d}.jpg',536),(1064,0))
        c.save(f'{out}/virora-{hd}-grid3.jpg',quality=90)
        cc=c.crop((450,0,1150,700));mask=Image.new('L',(700,700),0);ImageDraw.Draw(mask).ellipse((0,0,699,699),fill=255);w=Image.new('RGB',(700,700),'white');w.paste(cc,(0,0),mask)
        r=Image.new('RGB',(900,280),'white');r.paste(c.resize((600,262)),(0,16));r.paste(w.resize((262,262)),(620,16));ImageDraw.Draw(r).text((4,2),f'{hd}  (listing imgs {f1:02d} | {b:02d} back | {f2:02d})',fill='black');rows.append(r)
    S=Image.new('RGB',(900,280*len(rows)),'white')
    for j,r in enumerate(rows):S.paste(r,(0,j*280))
    S.save(f'{out}/preview_grid3.jpg',quality=86)
