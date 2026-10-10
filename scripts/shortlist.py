"""Color-tag shortlist: score every partner mat against a tile set's palette.
Usage: python3 scripts/shortlist.py "Name" HEX,HEX,... [--exclude "Splash of Color"] [--top 120]
Writes work/shortlist-<name>.json (ranked). Thumbnails cached in work/th/.
Method (Oct 10, Brownstone Bloom): drop white background, convert to Lab, share of mat pixels within dE<20
of any palette color (cream excluded), +0.08 per palette color hit (>4% of pixels), -1.2 x share of strongly
colored pixels far (dE>35) from the palette. Then Claude picks by eye from the top ~120 and Tiffany says Yes/Maybe/No."""
import json,os,sys,hashlib,urllib.request,concurrent.futures as cf
import numpy as np
from PIL import Image
args=sys.argv[1:];name=args[0];pal=args[1].split(',')
exclude=set();top=120
if '--exclude' in args: exclude.add(args[args.index('--exclude')+1])
if '--top' in args: top=int(args[args.index('--top')+1])
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TH=ROOT+'/work/th';os.makedirs(TH,exist_ok=True)
def lab(rgb):
    c=rgb/255.0;c=np.where(c>0.04045,((c+0.055)/1.055)**2.4,c/12.92)
    M=np.array([[0.4124,0.3576,0.1805],[0.2126,0.7152,0.0722],[0.0193,0.1192,0.9505]])
    xyz=c@M.T/np.array([0.9505,1.0,1.089]);f=np.where(xyz>0.008856,np.cbrt(xyz),7.787*xyz+16/116)
    return np.stack([116*f[...,1]-16,500*(f[...,0]-f[...,1]),200*(f[...,1]-f[...,2])],-1)
TL=[lab(np.array([[int(h[i:i+2],16) for i in (0,2,4)]],float))[0] for h in pal]
it=json.load(open(ROOT+'/work/items-colored.json'))
mats=[x for x in it if x['k']=='mat' and x.get('a') and x.get('i') and x['b'] not in exclude]
def th(x):
    h=hashlib.md5(x['u'].encode()).hexdigest()[:12];p=f'{TH}/{h}.jpg'
    if not os.path.exists(p):
        u=x['i']+('&' if '?' in x['i'] else '?')+'width=240'
        try: open(p,'wb').write(urllib.request.urlopen(u,timeout=20).read())
        except Exception: return None
    return p
with cf.ThreadPoolExecutor(16) as ex: paths=list(ex.map(th,mats))
res=[]
for x,p in zip(mats,paths):
    if not p: continue
    try: a=np.asarray(Image.open(p).convert('RGB').resize((80,80)),float).reshape(-1,3)
    except Exception: continue
    a=a[~(a.min(1)>235)]
    if len(a)<500: continue
    L=lab(a);D=np.stack([np.linalg.norm(L-t,axis=1) for t in TL],1);mn=D.min(1)
    hits=(D<20).mean(0);nh=int((hits>0.04).sum())
    chroma=np.hypot(L[:,1],L[:,2]);far=((mn>35)&(chroma>25)).mean()
    s=(mn<20).mean()+0.08*nh-1.2*far-(0.5 if nh==0 else 0)
    res.append(dict(b=x['b'],t=x['t'],u=x['u'],i=x['i'],p=x.get('p'),s=round(float(s),3)))
res.sort(key=lambda r:-r['s'])
out=ROOT+'/work/shortlist-'+name.lower().replace(' ','-')+'.json'
json.dump(res[:top],open(out,'w'),indent=1);print(out,len(res))
