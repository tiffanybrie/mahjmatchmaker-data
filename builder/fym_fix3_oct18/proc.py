# full-quality pass for FYM mat + catalog tile images.
# For each item: find the store photo that IS the current picture (optionally cropped out of a listing graphic),
# fetch it full size, crop/trim to the mat, re-encode (long side <=1400). Current images are only trimmed, never panel-cropped.
import json,sys,os,io,hashlib,subprocess,concurrent.futures as cf
import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
sys.path.insert(0,'f3'); from matimg import *
FX='/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/fymfix2/'
D=loadD(); M=D['mats']; T=D['tiles']
pj=json.load(open('f3/pj_imgs.json'))
albumtiles={s['tile'] for s in D['sets'] if s.get('album')}
FC=set(json.load(open('f3/forcecur.json'))) if os.path.exists('f3/forcecur.json') else set()
OV=json.load(open('f3/overrides.json')) if os.path.exists('f3/overrides.json') else {}
for d in ('f3/full','f3/out','f3/prev'): os.makedirs(d,exist_ok=True)
TH=0.035
def flat(im):
    if im.mode in ('RGBA','LA','P'):
        im=im.convert('RGBA'); bg=Image.new('RGB',im.size,(255,255,255)); bg.paste(im,mask=im.split()[3]); return bg
    return im.convert('RGB')
def longest_run(v,th):
    best=(0,0,0); s=None
    for i,x in enumerate(list(v)+[0]):
        if x>th and s is None: s=i
        if x<=th and s is not None:
            if i-s>best[0]: best=(i-s,s,i)
            s=None
    return best[1],best[2]
def panelbox(im):
    """box (fractions) of the mat inside a solid-colour panel (listing graphic), or None"""
    a=np.asarray(im,dtype=int); H,W,_=a.shape; e=max(2,H//40)
    cs=np.concatenate([a[:e].reshape(-1,3),a[-e:].reshape(-1,3),a[:,:e].reshape(-1,3),a[:,-e:].reshape(-1,3)])
    bg=np.median(cs,axis=0)
    if (np.abs(cs-bg).sum(1)<36).mean()<0.85: return None
    m=np.abs(a-bg).sum(2)>45
    pr,pc=m.mean(1),m.mean(0)
    r0,r1=longest_run(pr,0.15); c0,c1=longest_run(pc,0.15)
    if r1-r0<H*0.3 or c1-c0<W*0.3: return None
    while r0>0 and pr[r0-1]>0.08: r0-=1
    while r1<H and pr[r1]>0.08: r1+=1
    while c0>0 and pc[c0-1]>0.08: c0-=1
    while c1<W and pc[c1]>0.08: c1+=1
    if (r1-r0)*(c1-c0)>0.9*H*W: return None
    return (c0/W,r0/H,c1/W,r1/H)
def area(b): return (b[2]-b[0])*(b[3]-b[1])
def trimbox(im,thr=238):
    a=np.asarray(im.convert('L')); m=a<thr
    rows=np.where(m.mean(1)>0.02)[0]; cols=np.where(m.mean(0)>0.02)[0]
    if len(rows)<5 or len(cols)<5: return (0,0,1,1)
    W,H=im.size; return (cols[0]/W,rows[0]/H,(cols[-1]+1)/W,(rows[-1]+1)/H)
def crop(im,b,pad=0.0):
    W,H=im.size; return im.crop((max(0,int(b[0]*W)-int(pad*W)),max(0,int(b[1]*H)-int(pad*H)),min(W,int(b[2]*W)+int(pad*W)),min(H,int(b[3]*H)+int(pad*H))))
def vec(im): return np.asarray(im.convert('RGB').resize((40,40)),dtype=float)/255
def prev(src):
    base=src.split('?')[0]
    fn='f3/prev/'+hashlib.md5(base.encode()).hexdigest()[:14]+'.jpg'
    if not os.path.exists(fn) or os.path.getsize(fn)<500:
        u=base+('?width=240' if ('cdn.shopify' in base or '/cdn/shop/' in base) else '')
        subprocess.run(['curl','-s','-L','-m','20','-o',fn,u])
    try: return flat(Image.open(fn))
    except Exception: return None
def getfull(src):
    base=src.split('?')[0]
    fn='f3/full/'+hashlib.md5(base.encode()).hexdigest()[:14]+os.path.splitext(base)[1][:5]
    if not os.path.exists(fn) or os.path.getsize(fn)<2000:
        u=base+('?width=2400' if ('cdn.shopify' in base or '/cdn/shop/' in base) else '')
        subprocess.run(['curl','-s','-L','-m','90','-o',fn,u])
    return flat(Image.open(fn))
def cur(kind,k):
    if kind=='m': return matimg(M[k]['f'])
    f=T[k]['full']
    for d in ('build/','site/','site2/'):
        if os.path.exists(FX+d+f): return Image.open(FX+d+f).convert('RGB')
def fin(kind,key,im,before,src,graphic,d=None):
    im.thumbnail((1400,1400),Image.LANCZOS)
    fn='f3/out/'+hashlib.md5(key.encode()).hexdigest()[:14]+('.webp' if kind=='m' else '.jpg')
    if kind=='m': im.save(fn,'WEBP',quality=85,method=5)
    else: im.save(fn,'JPEG',quality=88)
    return {'file':fn,'before':before,'after':im.size,'src':src,'graphic':graphic,'d':d}
def job(key):
    kind,k=key.split('|',1)
    if kind=='t' and (k in albumtiles or not T[k].get('cat')): return key,None
    try:
        c=cur(kind,k)
        if c is None: return key,None
        before=c.size
        if key in OV:
            p=OV[key]; im=flat(Image.open(p if os.path.isabs(p) else '/home/claude/mahjmatchmaker-data/'+p))
            pb=panelbox(im) if kind=='m' else None
            if pb: im=crop(im,pb)
            return key,fin(kind,key,crop(im,trimbox(im)),before,p,bool(pb))
        cpb=panelbox(c) if kind=='m' else None
        cg=bool(cpb and area(cpb)<0.75) and key not in FC
        if cg: c=crop(c,cpb)
        ct=crop(c,trimbox(c)); cv=vec(ct); best=(9,None,None)
        for src,w,h in ([] if key in FC else (pj.get(key) or []))[:8]:
            if not w or max(w,h or 0)<max(before)*1.1: continue
            p=prev(src)
            if p is None: continue
            opts=[(None,crop(p,trimbox(p)))]
            pb=panelbox(p) if kind=='m' else None
            if pb:
                pc=crop(p,pb); opts.append((pb,crop(pc,trimbox(pc))))
            if pb and area(pb)<0.75: opts=opts[1:]
            for b,im in opts:
                d=float(((vec(im)-cv)**2).mean())
                if d<best[0]: best=(d,src,b)
        if key not in FC and kind=='m' and 'brittmillsdesign.com' in k and (best[0]>=TH or not best[1]):
            for src,w,h in (pj.get(key) or [])[:3]:
                if w and w>=3000 and not src.split('?')[0].lower().endswith('.heic'):
                    p=prev(src); pb=panelbox(p) if p is not None else None
                    if pb and area(pb)<0.75: best=(0.0,src,pb); break
        if best[1] and best[0]<TH:
            im=getfull(best[1])
            if best[2]: im=crop(im,best[2])
            im=crop(im,trimbox(im))
            ar=im.width/im.height
            if 0.6<ar<1.67 and max(im.size)>max(before):
                return key,fin(kind,key,im,before,best[1].split('?')[0],bool(best[2]),round(best[0],4))
        return key,fin(kind,key,ct,before,'current',cg)
    except Exception as e:
        return key,{'err':str(e)[:120]}
keys=[('m|'+m) for m in M if not M[m].get('hid')]+[('t|'+t) for t in T]
if len(sys.argv)>1: keys=[k for k in keys if any(s in k for s in sys.argv[1:])]
with cf.ThreadPoolExecutor(8) as ex: out=dict(ex.map(job,keys))
out={k:v for k,v in out.items() if v}
old=json.load(open('f3/proc.json')) if os.path.exists('f3/proc.json') else {}
old.update(out); json.dump(old,open('f3/proc.json','w'))
print(len(out),'errors',sum(1 for v in out.values() if 'err' in v),'upgraded',sum(1 for v in out.values() if v.get('src')!='current' and 'err' not in v),'graphic-cropped',sum(1 for v in out.values() if v.get('graphic')))
