import numpy as np,sys
from PIL import Image
def navybox(f):
    a=np.asarray(Image.open(f).convert('RGB')).astype(int)
    r,g,b=a[...,0],a[...,1],a[...,2]
    m=(b>100)&(b<175)&(r<45)&(g>35)&(g<100)
    sub=m[1000:1330,500:1080]
    cols=np.where(sub.sum(0)>90)[0]; rows=np.where(sub.sum(1)>200)[0]
    if len(cols)<50 or len(rows)<50: return None
    return (cols.min()+500,rows.min()+1000,cols.max()+500,rows.max()+1000)
if __name__=='__main__':
    for f in sys.argv[1:]: print(navybox(f),f.split('/')[-1][:60])
