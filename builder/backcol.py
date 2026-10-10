import json,numpy as np,colorsys
from PIL import Image,ImageDraw
from scipy.cluster.vq import kmeans2
PILE=json.load(open('/tmp/mb/pile.json'))
def back(f):
    im=Image.open(f).convert('RGB');im.thumbnail((200,200));a=np.asarray(im).astype(float)/255
    h,w,_=a.shape;yy,xx=np.mgrid[:h,:w];c=((yy-h/2)**2+(xx-w/2)**2)<(min(h,w)*.42)**2
    mx=a.max(2);mn=a.min(2);s=(mx-mn)/(mx+1e-6);v=mx
    m=c&(v>.12)&(v<.97)&(s>.28)
    p=a[m]
    if len(p)<200: m=c&(v<.97)&(s>.15);p=a[m]
    if len(p)<50: return None
    np.random.seed(1);cen,lab=kmeans2(p,4,minit='++',seed=1)
    cnt=np.bincount(lab,minlength=4);q=p[lab==cnt.argmax()];sc=q.max(1)*(q.max(1)-q.min(1));q=q[sc>=np.percentile(sc,55)];col=np.median(q,axis=0)
    return tuple(int(x*255) for x in col)
out={}
for k,f in PILE.items():
    try:
        c=back(f)
        if c: out[k]=c
    except Exception as e: print(k,e)
json.dump(out,open('backcol.json','w'))
ks=list(out);W=240;sheet=Image.new('RGB',(W*4,200*((len(ks)+3)//4)),'white');d=ImageDraw.Draw(sheet)
for i,k in enumerate(ks):
    x,y=(i%4)*W,(i//4)*200
    im=Image.open(PILE[k]).convert('RGB');im.thumbnail((140,140));sheet.paste(im,(x,y))
    d.rectangle([x+145,y,x+235,y+90],fill=out[k]);d.text((x+2,y+150),k.split('/')[-1][:34],fill='black')
sheet.save('backsheet.png');print(len(ks))
