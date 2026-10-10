import json,subprocess,io,sys
import numpy as np
from PIL import Image
plan=json.load(open('/tmp/mb/plan.json'))['prods']
def get(u):return subprocess.run(['curl','-s','-m','25','-L',u],capture_output=True).stdout
def pilescore(img):
    a=np.asarray(img.convert('RGB').resize((120,150))).astype(int)
    white=(a.min(axis=2)>235)
    border=np.concatenate([white[:4].ravel(),white[-4:].ravel(),white[:,:4].ravel(),white[:,-4:].ravel()])
    g=np.asarray(img.convert('L').resize((150,150))).astype(float)
    e=np.abs(np.diff(g,axis=0))[:,:-1]+np.abs(np.diff(g,axis=1))[:-1,:]
    cells=[e[i*49:(i+1)*49,j*49:(j+1)*49].mean() for i in range(3) for j in range(3)]
    pilescore.busy=min(cells)
    return float(white.mean()), float(border.mean())   # pile = almost no white anywhere, incl. border
import os
out=json.load(open('/tmp/mb/pile.json'))
for pid,p in plan.items():
    if p['kind']!='tile' or pid in out: continue
    try: j=json.loads(get(f"https://{p['domain']}/products/{p['handle']}.json"))['product']
    except: continue
    best=None
    for k,im in enumerate(j['images'][:10]):
        s=im['src']+('&' if '?' in im['src'] else '?')+'width=600'
        try: img=Image.open(io.BytesIO(get(s))).convert('RGB')
        except: continue
        w,b=pilescore(img)
        if pilescore.busy>14 and (best is None or w<best[0]): best=(w,k,img)
    print(p['name'],'pile idx',best[1] if best else None,flush=True)
    if best:
        f=f"/tmp/mb/img/{pid.replace('/','__')}.pile.jpg";best[2].save(f,quality=88);out[pid]=f
json.dump(out,open('/tmp/mb/pile.json','w'))
