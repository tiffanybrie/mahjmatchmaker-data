import json,sys,collections; sys.path.insert(0,'f3'); from matimg import *; from bamboo import *
import numpy as np
from PIL import Image
D=loadD(); M=D['mats']; P=json.load(open('f3/proc.json'))
done={}; boxes=collections.defaultdict(list); fail=[]
for k,v in P.items():
    if k[0]!='m' or 'file' not in v: continue
    im=Image.open(v['file']).convert('RGB')
    if M[k[2:]]['bn'] not in ('Mahj & Moon','Mahj Mood') or surface_fraction(im)<0.5: continue
    c=cut(im); W,H=im.size
    ok=c is not None and c.width*c.height>=0.55*W*H and 0.85<c.width/c.height<1.18
    if ok:
        done[k]=c; bb=im.getbbox()
        # record box as fractions via template match of size/position: approximate with centred crop
        boxes[M[k[2:]]['bn']].append((c.width/W,c.height/H))
    else: fail.append(k)
print('cut',len(done),'fail',len(fail))
for k in fail:
    im=Image.open(P[k]['file']).convert('RGB'); W,H=im.size; bn=M[k[2:]]['bn']
    if boxes[bn]:
        fw=float(np.median([b[0] for b in boxes[bn]])); fh=float(np.median([b[1] for b in boxes[bn]]))
        x0=int(W*(1-fw)/2); y0=int(H*(1-fh)/2); done[k]=im.crop((x0,y0,x0+int(W*fw),y0+int(H*fh))); P[k]['bamboo']='template'
for k,c in done.items():
    c.save(P[k]['file'],'WEBP',quality=85,method=5); P[k]['after']=list(c.size); P[k].setdefault('bamboo','cut')
json.dump(P,open('f3/proc.json','w'))
json.dump(sorted(done),open('f3/bamboo_done.json','w'))
print(collections.Counter(M[k[2:]]['bn'] for k in done).most_common())
