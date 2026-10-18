"""Pack the HD tile / rack / logo images into chunk files for the FYM build: <build>/hd/index.json + hd/{t,r,l}N.json."""
import json,os,base64,sys,glob,io
from PIL import Image
CAP={'t':(1280,80),'r':(1200,84),'m':(1400,82),'l':(900,90)}
SP='/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad'
B=sys.argv[1] if len(sys.argv)>1 else SP+'/fymfix2/build';O=B+'/hd';os.makedirs(O,exist_ok=True)
for f in glob.glob(O+'/*.json'):os.remove(f)
def uri(p,kind=None):
    if kind in CAP:
        im=Image.open(p);cap,q=CAP[kind]
        if max(im.size)>cap:im.thumbnail((cap,cap),Image.LANCZOS)
        b=io.BytesIO();im.save(b,'WEBP',quality=q,method=6);return 'data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode()
    ext=p.rsplit('.',1)[1].lower();mt={'webp':'webp','png':'png','jpg':'jpeg'}[ext]
    return f'data:image/{mt};base64,'+base64.b64encode(open(p,'rb').read()).decode()
idx={'t':{},'r':{},'l':{},'m':{}}
def pack(kind,items,per):
    items=sorted(items);cur={};n=0;size=0
    for k,p in items:
        cur[k]=uri(p,kind);size+=len(cur[k])
        if len(cur)>=per or size>3_000_000:
            fn=f'{kind}{n}.json';json.dump(cur,open(f'{O}/{fn}','w'));[idx[kind].__setitem__(x,fn) for x in cur];cur={};n+=1;size=0
    if cur:fn=f'{kind}{n}.json';json.dump(cur,open(f'{O}/{fn}','w'));[idx[kind].__setitem__(x,fn) for x in cur]
t=json.load(open(SP+'/hd_tiles/report.json'));pack('t',[(k,SP+'/hd_tiles/'+v['hd']) for k,v in t.items() if v.get('hd')],12)
r=json.load(open(SP+'/hd_racks/report.json'));pack('r',[(k,SP+'/hd_racks/'+v['hd']) for k,v in r.items() if v.get('hd')],24)
l=json.load(open(SP+'/hd_logos/final/map.json'));pack('l',[(k,SP+'/hd_logos/final/'+v['f']) for k,v in l.items()],60)
mp=SP+'/hd_mats/report.json'
if os.path.exists(mp):
    m=json.load(open(mp));pack('m',[(k,SP+'/hd_mats/'+v['hd']) for k,v in m.items() if v.get('hd')],10)
json.dump(idx,open(O+'/index.json','w'))
tot=sum(os.path.getsize(f) for f in glob.glob(O+'/*.json'))
print({k:len(v) for k,v in idx.items()},'files',len(glob.glob(O+'/*.json')),'MB',round(tot/1e6,1))
