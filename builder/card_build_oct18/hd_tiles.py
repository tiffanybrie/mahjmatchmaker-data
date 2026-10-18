"""HD tile-pile images for the FYM match card (Oct 18).
For each FYM tile set, locate its bundled pile photo (360-620px) inside higher-res candidates
(T.full, repo tile photos, the brand's Shopify product images at 2000px) with SIFT + homography,
then warp-crop the best candidate to the same framing at the highest available resolution (cap 1600).
Writes hd_tiles/<tilekey-hash>.webp + hd_tiles/report.json. Usage: python3 hd_tiles.py [name filter]"""
import json,re,os,sys,io,base64,glob,unicodedata,urllib.request,hashlib
import numpy as np,cv2
from PIL import Image
SP='/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad'
BUILD=SP+'/fymfix2/build';REPO='/home/claude/mahjmatchmaker-data/'
OUT=SP+'/hd_tiles';os.makedirs(OUT,exist_ok=True);CACHE=SP+'/hd_cache';os.makedirs(CACHE,exist_ok=True)
s=open(BUILD+'/index.html').read();i=s.index('const D=')+8;j=s.index('\n',i);D=json.loads(s[i:j].rstrip()[:-1])
# bundled images live in the b*.js bundles as window.IMG entries
IMG={}
for f in glob.glob(REPO+'builder/card_redesign_oct18/serve/b*.js'):
    t=open(f).read()
    for m in re.finditer(r'"([A-Za-z0-9_:.-]{6,60})"\s*:\s*"(data:image/[^"]+)"',t):IMG[m.group(1)]=m.group(2)
def dec(u):return Image.open(io.BytesIO(base64.b64decode(u.split(',',1)[1]))).convert('RGB')
def fullpath(rel):
    for base in [BUILD,SP+'/fym_independent_audit/site_pub',REPO+'builder/card_redesign_oct18/serve']:
        p=os.path.join(base,rel)
        if os.path.exists(p):return p
norm=lambda t:re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',t).encode('ascii','ignore').decode().lower())
REPOTILES=[f for f in glob.glob(REPO+'assets/tiles/**/*.*',recursive=True) if f.lower().endswith(('.jpg','.jpeg','.png','.webp'))]
UA={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124 Safari/537.36'}
def get(url,timeout=25):
    h=hashlib.md5(url.encode()).hexdigest();p=os.path.join(CACHE,h)
    if os.path.exists(p):return open(p,'rb').read()
    r=urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=timeout).read();open(p,'wb').write(r);return r
def shopify(u):
    m=re.match(r'(https?://[^/]+)/(?:collections/[^/]+/)?products/([^/?#]+)',u or '')
    if not m:return []
    try:d=json.loads(get(f'{m.group(1)}/products/{m.group(2)}.json'))['product']
    except Exception:return []
    out=[]
    for im in d.get('images',[])[:10]:
        src=im['src'];src=src+('&' if '?' in src else '?')+'width=2000'
        try:out.append(('shop:'+src,Image.open(io.BytesIO(get(src))).convert('RGB')))
        except Exception:pass
    return out
sift=cv2.SIFT_create(nfeatures=4000)
def feats(pil,maxs=1600):
    a=np.asarray(pil);k=min(1,maxs/max(a.shape[:2]));
    if k<1:a=cv2.resize(a,None,fx=k,fy=k,interpolation=cv2.INTER_AREA)
    g=cv2.cvtColor(a,cv2.COLOR_RGB2GRAY);kp,de=sift.detectAndCompute(g,None);return kp,de,k
bf=cv2.BFMatcher()
def locate(q,cand):
    """Return (scale, H) mapping query pixel coords -> candidate full-res coords, or None."""
    qk,qd,_=feats(q,2000);ck,cd,k=feats(cand)
    if qd is None or cd is None or len(ck)<20:return None
    ms=bf.knnMatch(qd,cd,k=2);good=[m for m,n in (x for x in ms if len(x)==2) if m.distance<0.72*n.distance]
    if len(good)<20:return None
    src=np.float32([qk[m.queryIdx].pt for m in good]);dst=np.float32([ck[m.trainIdx].pt for m in good])/k
    H,mask=cv2.findHomography(src,dst,cv2.RANSAC,4.0*(1/k))
    if H is None or mask.sum()<20:return None
    w,h=q.size;c=cv2.perspectiveTransform(np.float32([[[0,0]],[[w,0]],[[w,h]],[[0,h]]]),H).reshape(4,2)
    area=cv2.contourArea(c);scale=(area/(w*h))**.5
    W,Hh=cand.size;inside=(c[:,0].min()>-0.02*W and c[:,1].min()>-0.02*Hh and c[:,0].max()<1.02*W and c[:,1].max()<1.02*Hh)
    # reject degenerate/skewed fits
    sides=[np.linalg.norm(c[i]-c[(i+1)%4]) for i in range(4)]
    if not inside or min(sides)<0.5*max(sides)*min(w,h)/max(w,h):return None
    return scale,H,int(mask.sum())
def warp(cand,H,q,scale,cap=1600):
    w,h=q.size;f=min(scale,cap/max(w,h));ow,oh=int(w*f),int(h*f)
    S=np.array([[1/f,0,0],[0,1/f,0],[0,0,1]]);M=H@S
    out=cv2.warpPerspective(np.asarray(cand),M,(ow,oh),flags=cv2.WARP_INVERSE_MAP|cv2.INTER_LANCZOS4) if False else cv2.warpPerspective(np.asarray(cand),np.linalg.inv(M),(ow,oh),flags=cv2.INTER_LANCZOS4)
    return Image.fromarray(out)
def sim(a,b):
    a=np.asarray(a.resize((96,96))).astype(float);b=np.asarray(b.resize((96,96))).astype(float)
    a-=a.mean();b-=b.mean();return float((a*b).sum()/np.sqrt((a*a).sum()*(b*b).sum()+1e-9))
flt=sys.argv[1].lower() if len(sys.argv)>1 else ''
rep={} if flt=='__none__' else (json.load(open(OUT+'/report.json')) if os.path.exists(OUT+'/report.json') else {})
names={}
for st in D['sets']:names.setdefault(st['tile'],st['name'])
for key,t in D['tiles'].items():
    nm=names.get(key,t['n'])
    if flt and flt not in nm.lower():continue
    if key in rep and not flt:continue
    q=dec(IMG[t['pile']]) if t['pile'] in IMG else None
    if q is None:rep[key]={'n':nm,'err':'no pile'};continue
    cands=[]
    fp=fullpath(t['full']) if t.get('full') else None
    if fp:cands.append(('full:'+t['full'],Image.open(fp).convert('RGB')))
    nn=norm(nm)
    for f in REPOTILES:
        if nn and nn in norm(os.path.basename(f)):
            try:cands.append(('repo:'+f[len(REPO):],Image.open(f).convert('RGB')))
            except Exception:pass
    cands+=shopify(t.get('u',''))
    best=None
    for src,c in cands:
        if max(c.size)<=max(q.size)*1.15:continue
        r=locate(q,c)
        if not r:continue
        sc,H,inl=r
        if not best or sc>best[0]:best=(sc,H,inl,src,c)
    if not best or best[0]<1.25:
        rep[key]={'n':nm,'pile':list(q.size),'best':(round(best[0],2),best[3]) if best else None,'cands':len(cands),'hd':None};print(nm,'no upgrade',rep[key]['best'],len(cands));continue
    sc,H,inl,src,c=best;out=warp(c,H,q,sc);s2=sim(out,q)
    if s2<0.8:rep[key]={'n':nm,'pile':list(q.size),'best':(round(sc,2),src),'sim':round(s2,3),'hd':None};print(nm,'low sim',s2);continue
    fn=hashlib.md5(key.encode()).hexdigest()[:12]+'.webp';out.save(os.path.join(OUT,fn),'WEBP',quality=88)
    rep[key]={'n':nm,'pile':list(q.size),'hd':fn,'size':list(out.size),'src':src,'scale':round(sc,2),'inl':inl,'sim':round(s2,3)};print(nm,out.size,src[:70],round(s2,3))
    json.dump(rep,open(OUT+'/report.json','w'),indent=1)
if flt!='__none__':json.dump(rep,open(OUT+'/report.json','w'),indent=1)
