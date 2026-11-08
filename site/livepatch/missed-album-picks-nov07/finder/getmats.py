import json,subprocess,struct,re,io,os
from PIL import Image
FS='/home/claude/fym-site'
files=[l for l in open("mcfiles.txt").read().split() if "fym-v" in l]
D7=json.load(open('D117.json'))['mats']; D8=json.load(open('D118.json'))['mats']
def ver(p): return int(re.search(r'fym-v(\d+)',p).group(1))
CACHE={}
def chunks(c):
    for p in sorted([p for p in files if p.endswith(f'/mc/{c}.webp')],key=ver,reverse=True):
        if p not in CACHE:
            CACHE[p]=subprocess.run(['git','-C',FS,'show','HEAD:'+p],capture_output=True).stdout
        yield p,CACHE[p]
def get(f,out,maxver=999):
    n=int(re.search(r'(\d+)',f).group(1))
    for p,ab in chunks(n//12):
        if ver(p)>maxver: continue
        hl=struct.unpack('<I',ab[-4:])[0]; h=json.loads(ab[-4-hl:-4].decode())
        k=next((x for x in (f,str(n),'m/%d.webp'%n) if x in h),None)
        if k is None: continue
        a,l=h[k]; Image.open(io.BytesIO(ab[a:a+l])).convert('RGB').save(out,quality=93); return p
    return None
def slug(k): return re.sub(r'[^a-z0-9]+','-',k.lower()).strip('-')[-90:]
if __name__=='__main__':
    A=json.load(open('missing_final.json'))['pairs']
    res={}
    for k in sorted({p['key'] for p in A}):
        m8=D8.get(k); m7=D7.get(k)
        # same photo index in both versions? prefer the v117 file with v117 chunks (live), else v118
        if m7 and m7.get('f'): src=get(m7['f'],f'matimg/{slug(k)}.jpg',117); v=117
        else: src=None
        if not src and m8 and m8.get('f'): src=get(m8['f'],f'matimg/{slug(k)}.jpg',118); v=118
        res[k]={'file':f'matimg/{slug(k)}.jpg' if src else None,'chunk':src}
        if not src: print('NO PHOTO',k)
    json.dump(res,open('matimg.json','w'),indent=1)
    print(len(res),'mats',sum(1 for v in res.values() if v['file']),'with photo')
