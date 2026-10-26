from PIL import Image
from grid import rr
def ucells(path,x0,y0,x1,y1,rows,cols,picks,ins=.03):
    im=Image.open(path).convert('RGB');pw=(x1-x0)/cols;ph=(y1-y0)/rows;out=[]
    for r,c in picks:
        a,b=x0+c*pw,y0+r*ph
        t=im.crop((int(a+pw*ins),int(b+ph*ins),int(a+pw*(1-ins)),int(b+ph*(1-ins)))).convert('RGBA')
        t.putalpha(rr(t.width,t.height,int(t.width*.09)));out.append(t)
    return out
