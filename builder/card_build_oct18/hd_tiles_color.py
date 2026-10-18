"""Match each HD tile crop's colour to the approved bundled pile (some piles were colour-corrected, e.g. Sunday's warmer mustard).
Per-channel mean/std transfer in LAB, measured on same-size versions. Rewrites hd_tiles/*.webp once (marks report 'cfix')."""
import json,sys,os
import numpy as np,cv2
from PIL import Image
sys.argv=['x','__none__']
import hd_tiles as H
S=H.SP+'/hd_tiles';r=json.load(open(S+'/report.json'));n=0
for k,v in r.items():
    if not v.get('hd') or v.get('cfix'):continue
    q=np.asarray(H.dec(H.IMG[H.D['tiles'][k]['pile']]));p=S+'/'+v['hd'];hd=np.asarray(Image.open(p).convert('RGB'))
    small=cv2.resize(hd,(q.shape[1],q.shape[0]),interpolation=cv2.INTER_AREA)
    lq=cv2.cvtColor(q,cv2.COLOR_RGB2LAB).astype(np.float32);ls=cv2.cvtColor(small,cv2.COLOR_RGB2LAB).astype(np.float32);lh=cv2.cvtColor(hd,cv2.COLOR_RGB2LAB).astype(np.float32)
    for c in range(3):
        ms,ss=ls[...,c].mean(),ls[...,c].std()+1e-6;mq,sq=lq[...,c].mean(),lq[...,c].std()
        lh[...,c]=(lh[...,c]-ms)*(sq/ss)+mq
    out=cv2.cvtColor(np.clip(lh,0,255).astype(np.uint8),cv2.COLOR_LAB2RGB)
    Image.fromarray(out).save(p,'WEBP',quality=88);v['cfix']=1;n+=1
json.dump(r,open(S+'/report.json','w'),indent=1);print('colour-matched',n)
