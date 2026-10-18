import numpy as np,json,sys
from PIL import Image
S=sys.argv[1]
cl=json.load(open(S+'/classify.json'))
out={}
for f,v in cl.items():
    if v[0]=='nobox': out[f]=['nobox']; continue
    x0,y0,x1,y1=v[1]; y1=y0+136
    a=np.asarray(Image.open(f).convert('L').crop((x0,y0,x1,y1))).astype(int)
    band=a[80:125]>170
    cols=np.where(band.sum(0)>0)[0]
    ext=int(cols.max()-cols.min()) if len(cols) else 0
    out[f]=['new' if ext>290 else 'old',[x0,y0,x1,y0+136],ext]
json.dump(out,open(S+'/classify2.json','w'))
from collections import Counter
c=Counter((f.split('/')[2],v[0]) for f,v in out.items())
for k in sorted(c): print(k,c[k])
import statistics
print(sorted(Counter(v[2]//10*10 for v in out.values() if len(v)>2).items()))
