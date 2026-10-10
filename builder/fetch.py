import json,subprocess,io,sys,os,re
import numpy as np
from PIL import Image
plan=json.load(open('/tmp/mb/plan.json'));P=plan['prods']
def get(url,t=25):
    r=subprocess.run(['curl','-s','-m',str(t),'-L',url],capture_output=True);return r.stdout
def score(im):
    a=np.asarray(im.convert('RGB').resize((200,200))).astype(int)
    b=np.concatenate([a[:8].reshape(-1,3),a[-8:].reshape(-1,3),a[:,:8].reshape(-1,3),a[:,-8:].reshape(-1,3)])
    med=np.median(b,axis=0); dist=np.abs(b-med).max(axis=1)
    uni=(dist<28).mean()
    # penalise busy full-frame scenes: fraction of corner-to-centre variance
    return float(uni)
import os
res=json.load(open('/tmp/mb/fetched.json')) if os.path.exists('/tmp/mb/fetched.json') else {}
for pid,p in P.items():
    if pid in res and 'file' in res[pid]: continue
    out=f"/tmp/mb/img/{pid.replace('/','__')}"
    try:
        j=json.loads(get(f"https://{p['domain']}/products/{p['handle']}.json"))['product']
    except Exception as e:
        res[pid]=dict(err='json');print(pid,'ERR json');continue
    best=None;cands=[]
    for k,im in enumerate(j['images'][:8]):
        src=im['src']; src=src+('&' if '?' in src else '?')+'width=700'
        data=get(src)
        try: img=Image.open(io.BytesIO(data)).convert('RGB')
        except: continue
        s=score(img); cands.append((s,k,img))
        if s>0.97 and k<3: break
    if not cands: res[pid]=dict(err='noimg');continue
    # prefer high score, earlier image
    cands.sort(key=lambda c:(-round(c[0],1),c[1]))
    s,k,img=cands[0]
    f=out+'.jpg'; img.save(f,quality=90)
    res[pid]=dict(score=round(s,2),idx=k,file=f,title=j.get('title'),nimg=len(j['images']),price=(j['variants'][0].get('price') if j.get('variants') else None))
    print(pid,round(s,2),k,len(j['images']),flush=True)
json.dump(res,open('/tmp/mb/fetched.json','w'),indent=1)
