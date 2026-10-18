import numpy as np,json,sys
from PIL import Image
R='/home/claude/mahjmatchmaker-data/'
T=Image.open(R+'assets/cards/sunday-tile-set-v3/sunday-mahjong-tiles-anders-ruff-brownstone-bloom-mat-v3.jpg').convert('RGB').crop((660,1107,1080,1241))
def top(a):
    nav=(abs(a[...,0]-7)<14)&(abs(a[...,1]-70)<14)&(abs(a[...,2]-137)<16)
    rows=np.where(nav[1000:1300,1075])[0]+1000
    cols=np.where(nav[1170,600:])[0]+600
    return int(rows.min()),int(rows.max()),int(cols.min())
def stamp(src,dst):
    im=Image.open(src).convert('RGB'); a=np.asarray(im).astype(int)
    y0,y1,x0=top(a)
    if not(1100<=y0<=1112 and 1234<=y1<=1246 and 655<=x0<=665): return (y0,y1,x0)
    im.paste(T,(660,y0)); im.save(dst,quality=93); return None
if __name__=='__main__':
    print(stamp(sys.argv[1],sys.argv[2]))
