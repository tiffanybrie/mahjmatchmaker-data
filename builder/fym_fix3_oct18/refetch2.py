# match each current FYM image to the same photo on the brand's store (small previews), record best source
import json,sys,os,io,hashlib,subprocess,concurrent.futures as cf
import numpy as np
from PIL import Image
sys.path.insert(0,'f3'); from matimg import *
D=loadD(); M=D['mats']; T=D['tiles']
FX='/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/fymfix2/'
pj=json.load(open('f3/pj_imgs.json'))
os.makedirs('f3/prev',exist_ok=True)
def trim(im,thr=242):
    g=np.asarray(im.convert('L'))<thr
    ys,xs=np.where(g)
    if len(xs)<50: return im
    return im.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
def vec(im):
    a=np.asarray(trim(im).convert('RGB').resize((40,40)),dtype=float)/255
    return a
def prev(src):
    base=src.split('?')[0]
    fn='f3/prev/'+hashlib.md5(base.encode()).hexdigest()[:14]+'.jpg'
    if not os.path.exists(fn) or os.path.getsize(fn)<500:
        u=base+('?width=240' if 'cdn.shopify' in base or '/cdn/shop/' in base else '')
        subprocess.run(['curl','-s','-L','-m','20','-o',fn,u])
    try: return Image.open(fn).convert('RGB')
    except Exception: return None
def cur(kind,k):
    if kind=='m': return matimg(M[k]['f'])
    f=T[k]['full']
    for d in ('build/','site/','site2/'):
        if os.path.exists(FX+d+f): return Image.open(FX+d+f).convert('RGB')
def job(key):
    kind,k=key.split('|',1); imgs=pj.get(key)
    if not imgs: return key,None
    c=cur(kind,k)
    if c is None: return key,None
    cv=vec(c); best=(9,None,None)
    for src,w,h in imgs[:8]:
        p=prev(src)
        if p is None: continue
        d=float(((vec(p)-cv)**2).mean())
        if d<best[0]: best=(d,src,(w,h))
    return key,{'d':round(best[0],4),'src':best[1],'wh':best[2],'cur':c.size}
keys=[k for k,v in pj.items() if v]
with cf.ThreadPoolExecutor(12) as ex: res=dict(ex.map(job,keys))
json.dump(res,open('f3/match.json','w'))
import collections
ok=[k for k,v in res.items() if v and v['d']<0.02]
print(len(keys),'good',len(ok))
up=[k for k in ok if res[k]['wh'] and res[k]['wh'][0] and max(res[k]['wh'])>max(res[k]['cur'])*1.15]
print('upgradable',len(up))
bad=sorted([(v['d'],k) for k,v in res.items() if v and v['d']>=0.02])
print('nomatch',len(bad)); print(bad[:10])
