import json,re,io,sys
exec(open('/tmp/rs/patch.py').read().split('done=[]')[0])
from PIL import Image
C=json.load(open('/tmp/ab/cand.json'))
acc=list(range(36,62))+[69,70,71,72,74,75,76,80,81,82,84]+list(range(86,96))+[101,102,103,104]+list(range(114,211))+[211,214,215,216,240,241,242,243,248,249,250,251,252,253,254,255,256,263,264,266,277]
alt={29:2,30:3,31:3,32:1,33:1,34:1,35:1,232:4,233:4,234:4,235:3,244:4,245:2,247:2,259:1}
crops=[0,1,2,5,6,7,8,9,10]+list(range(217,231))
excl=list(range(3,5))+list(range(11,29))
excl=[i for i in excl if i not in (5,6,7,8,9,10)]
flag=[62,63,64,65,66,67,68,73,77,78,79,83,85,96,97,98,99,100]+list(range(105,114))+[212,213,231,236,237,238,239,246,257,258,260,261,262,265]+list(range(267,277))
dom={}
for line in open('/home/claude/mahjmatchmaker-data/config/domains.tsv'):
    p,dm=line.strip().split('\t');dom[dm.split('?')[0].replace('www.','')]='https://mahjmatchmaker.com'+p
dom['mahjongregister.com']='https://www.mahjmatchmaker.com/mahjong-register-discount-code';dom['theroyalmahjongsociety.com']='https://www.mahjmatchmaker.com/royal-mahjong-society-discount-code'
def clean(n):
    n=re.sub(r'^NEW/COMING SOON:\s*','',n);n=re.sub(r'\s*(Mahjong|Mahj)?\s*(Game\s*)?(Play(ing)?\s*)?Mat(s)?\b.*$','',n,flags=re.I).strip(' -|')
    return n or 'Mahjong Mat'
def sqcrop(f):
    im=Image.open(f).convert('RGB');a=np.asarray(im).astype(int);bg=a[3,3];d=np.abs(a-bg).sum(2)>40
    rows=np.where(d.mean(1)>.45)[0];cols=np.where(d.mean(0)>.45)[0];x0,x1,y0=cols.min(),cols.max()+1,rows.min()
    return im.crop((x0,y0,x1,min(im.height,y0+(x1-x0))))
L=json.load(open('/home/claude/mahjmatchmaker-data/catalog/locked_decisions.json'))
n=0
def add(x,im):
    global n
    d0=x['key'].split('/')[0].replace('www.','')
    nm=clean(x['n'])+((' – '+x['var']) if x['var'] else '')
    v=dict(k='mat',n=nm,b=x['key'].split('/')[0],bn=x['brand'],url=x['url'],d=dom.get(d0,''),p=bool(x['partner']),nc=False,clean=False,hide=False,photo=uri(im),src='harvest-oct14')
    P[x['key']]=v;pr=prof(fg(im),nm)
    if pr: pr.update(clean=False,n=nm,b=x['brand'],albums=[],ar=[]);PR[x['key']]=pr
    L[x['key']]={'status':'photo-locked','reason':'added Oct 14 all-brands harvest, photo hand-checked'};n+=1
for i in acc: add(C[i],Image.open(C[i]['f']))
for i,c in alt.items(): add(C[i],Image.open(f'/tmp/ab/alt/{i}_{c}.jpg'))
for i in crops: add(C[i],sqcrop(C[i]['f']))
for i in excl: L[C[i]['key']]={'status':'rejected','reason':'not a mat (art print / pet or bath mat)'}
for i in flag: L[C[i]['key']]={'status':'needs-photo','reason':'no isolated mat photo (lifestyle, tiles/racks on mat, stacks or text overlay)','name':C[i]['n'],'brand':C[i]['brand']}
json.dump(d,open('/tmp/mb/data_embed.json','w'));json.dump(PR,open('/tmp/cc/profiles.json','w'))
json.dump(L,open('/home/claude/mahjmatchmaker-data/catalog/locked_decisions.json','w'),indent=1)
print('added',n,'excl',len(excl),'flag',len(flag),'covered',len(set(acc)|set(alt)|set(crops)|set(excl)|set(flag)),'of',len(C))
print(sorted(set(range(len(C)))-(set(acc)|set(alt)|set(crops)|set(excl)|set(flag))))
