import numpy as np,glob,json,sys
from PIL import Image
sys.path.insert(0,sys.argv[1]); from box import navybox
def strip(f,bx):
    x0,y0,x1,y1=bx; y1=min(y1,y0+136)
    im=Image.open(f).convert('L').crop((x0,y0,x1,y1)).resize((420,136))
    a=np.asarray(im).astype(float)[95:130,30:390]; return (a>128).astype(float)
old=strip('assets/cards/logofix-v2/sierra-mahjong-tiles-tigre-de-tartan-caned-trompe-mat.jpg',(658,1104,1079,1240))
new=strip('assets/cards/sunday-tile-set-v3/sunday-mahjong-tiles-anders-ruff-brownstone-bloom-mat-v3.jpg',(659,1107,1079,1241))
res={}
for f in sorted(glob.glob('assets/cards/**/*.jpg',recursive=True)):
    im=Image.open(f)
    if im.size!=(1080,1350): continue
    bx=navybox(f)
    if not bx: res[f]=('nobox',None); continue
    s=strip(f,bx); do=abs(s-old).mean(); dn=abs(s-new).mean()
    res[f]=('old' if do<dn else 'new',[int(v) for v in bx],round(do,3),round(dn,3))
json.dump(res,open(sys.argv[1]+'/classify.json','w'),indent=0)
from collections import Counter
c=Counter((f.split('/')[2],v[0]) for f,v in res.items())
for k in sorted(c): print(k,c[k])
