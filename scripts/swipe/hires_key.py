"""Find sharp versions of LOWRES mats: key the mat out of the brand's full-size listing graphic
(solid background, text above/below), match it to the vetted catalog image, save up to 1600px."""
import json, sys, io, urllib.request
from PIL import Image, ImageChops, ImageStat, ImageFilter
UA={"User-Agent":"Mozilla/5.0"}
def get(u): return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30).read()
def sized(s,w): s=s.split("?")[0]; return s+f"?width={w}"
def bgcol(im):
    w,h=im.size; c=[im.getpixel(p) for p in [(2,2),(w-3,2),(2,h-3),(w-3,h-3)]]
    return tuple(sorted(x[i] for x in c)[1] for i in range(3))
def keybox(im, tol=30, frac=0.3, cfrac=0.5):
    rgb=im.convert("RGB"); w,h=rgb.size; bg=bgcol(rgb)
    m=ImageChops.difference(rgb,Image.new("RGB",rgb.size,bg)).convert("L").point(lambda v:255 if v>tol else 0)
    m=m.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3))
    px=m.load()
    rows=[sum(1 for x in range(0,w,2) if px[x,y])*2/w for y in range(h)]
    ys=[y for y in range(h) if rows[y]>frac]
    if not ys: return None
    # longest contiguous run of mat rows
    runs=[];s=ys[0];p=ys[0]
    for y in ys[1:]:
        if y>p+12: runs.append((s,p)); s=y
        p=y
    runs.append((s,p)); y0,y1=max(runs,key=lambda r:r[1]-r[0])
    cols=[sum(1 for y in range(y0,y1,2) if px[x,y])*2/(y1-y0+1) for x in range(w)]
    xs=[x for x in range(w) if cols[x]>cfrac]
    if not xs: return None
    runs=[];s=xs[0];p=xs[0]
    for x in xs[1:]:
        if x>p+12: runs.append((s,p)); s=x
        p=x
    runs.append((s,p)); x0,x1=max(runs,key=lambda r:r[1]-r[0])
    if (x1-x0)*(y1-y0)<0.15*w*h: return None
    return (x0,y0,x1+1,y1+1)
def sig(im): return im.convert("RGB").resize((24,24))
def dist(a,b): return sum(ImageStat.Stat(ImageChops.difference(a,b)).mean)
def feed(url):
    base=url.split("?")[0].rstrip("/")
    try: return [i["src"] for i in json.loads(get(base+".json"))["product"]["images"]]
    except Exception as e: return []
def fix(url, ref_path, out_path, minside=1100):
    ref=sig(Image.open(ref_path)); best=None
    for s in feed(url)[:8]:
        try: im=Image.open(io.BytesIO(get(sized(s,800)))).convert("RGB")
        except Exception: continue
        for mode in ("key","full"):
            b=keybox(im) if mode=="key" else (0,0)+im.size
            if not b: continue
            d=dist(sig(im.crop(b)),ref)
            if best is None or d<best[0]: best=(d,s,b,im.size)
    if not best: return "no feed"
    d,s,b,(w,h)=best
    if d>45: return f"no match ({d:.0f})"
    big=Image.open(io.BytesIO(get(sized(s,3000)))).convert("RGB"); W,H=big.size; k=W/w
    bb=(int(b[0]*k),int(b[1]*k),int(b[2]*k),int(b[3]*k)); im=big.crop(bb)
    # shave 0.4% to drop any background halo on the edge
    e=int(min(im.size)*0.004); im=im.crop((e,e,im.width-e,im.height-e))
    im.thumbnail((1600,1600),Image.LANCZOS)
    if min(im.size)<minside: return f"still small {im.size} (d {d:.0f})"
    im.save(out_path,"JPEG",quality=88); return f"OK {im.size[0]}x{im.size[1]} d{d:.0f}"
if __name__=="__main__":
    jobs=json.load(open(sys.argv[1]))
    res={}
    for j in jobs:
        try: r=fix(j["url"],j["ref"],j["out"])
        except Exception as e: r="ERR "+str(e)[:80]
        res[j["id"]]=r; print(j["id"],r,flush=True)
    json.dump(res,open(sys.argv[2],"w"),indent=1)
