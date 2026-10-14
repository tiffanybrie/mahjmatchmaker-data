import json,base64,io,os,hashlib,shutil
from PIL import Image
SP='/tmp/claude-0/-home-claude-mahjmatchmaker-data/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/sw2'
os.makedirs(SP+'/m',exist_ok=True);os.makedirs(SP+'/t',exist_ok=True)
d=json.load(open('/tmp/mb/data_embed.json'));P=d['prods'];S=json.load(open('/tmp/sw/swipe.json'))
def im(u): return Image.open(io.BytesIO(base64.b64decode(u.split(',',1)[1])))
def uri(img,fmt,q,w):
    img=img.copy();img.thumbnail((w,w));b=io.BytesIO()
    img.convert('RGBA' if fmt in ('WEBP','PNG') else 'RGB').save(b,fmt,quality=q)
    return 'data:image/%s;base64,'%fmt.lower()+base64.b64encode(b.getvalue()).decode()
B={}  # key -> data uri (bundled)
def bund(u,fmt,q,w):
    v=uri(im(u),fmt,q,w);h=hashlib.md5(v.encode()).hexdigest()[:10];B[h]=v;return h
T=lambda v:v is True or v=='True'
mats={};racks={};tiles={}
nfile=0
for i,m in enumerate(S['mats']):
    p=P[m];clean=T(p.get('clean'))
    src=p['cut'] if clean else p['photo']
    img=im(src);f=f'm/{i}.webp'
    out=img.convert('RGBA' if clean else 'RGB');out.thumbnail((640,640))
    out.save(SP+'/'+f,'WEBP',quality=82);nfile+=1
    th=bund(src,'WEBP' if clean else 'JPEG',70,150)
    mats[m]=dict(n=p['n'],bn=p.get('bn') or p['b'],b=p['b'],u=p.get('url',''),dc=p.get('d',''),pa=T(p.get('p')),nc=T(p.get('nc')),rt=bool(p.get('retired')),c=clean,ml=T(p.get('mult')),f=f,th=th,w=out.width,h=out.height,mf=S['mf'][m],ms=S['ms'][m],hol=S['mt'][m]=='holiday')
for r,p in P.items():
    if p['k']!='rack' or T(p.get('hide')):continue
    clean=T(p.get('clean'));src=p['cut'] if clean else p['photo']
    racks[r]=dict(n=p['n'],bn=p.get('bn') or p['b'],b=p['b'],u=p.get('url',''),dc=p.get('d',''),pa=T(p.get('p')),nc=T(p.get('nc')),rt=bool(p.get('retired')),c=clean,ml=T(p.get('mult')),sk=T(p.get('skin')),hx=p.get('hx'),rf=S['rf'].get(r,[]),im=bund(src,'WEBP' if clean else 'JPEG',78,420))
sets=[]
for ti,s in enumerate(d['sets']):
    t=P[s['tile']];_src=t.get('pile') or t['cut']
    _A=json.load(open('/tmp/albtiles/index.json'));_af=(_A.get(s['name']) or {}).get('file')
    if _af:
        _src='data:image/jpeg;base64,'+base64.b64encode(open('/tmp/albtiles/'+_af.split('/')[-1],'rb').read()).decode()
    else: print('NO ALBUM TILE',s['name'])
    t=dict(t,pile=_src);im(_src).convert('RGB').save(f'{SP}/t/{ti}.jpg','JPEG',quality=92);tiles[s['tile']]=dict(full=f't/{ti}.jpg',n={'Jade':'Miss Classic Jade','Malachite':'Miss Classic Malachite','Heritage':'Heritage 1.0'}.get(s['name'],s['name']),bn=t.get('bn') or t['b'],u=t.get('url',''),dc=t.get('d',''),pa=T(t.get('p')),nc=T(t.get('nc')),rt=bool(t.get('retired')),pile=bund(t.get('pile') or t['cut'],'JPEG',80,620))
    sets.append(dict(slug=s['slug'],name={'Jade':'Miss Classic Jade','Malachite':'Miss Classic Malachite','Heritage':'Heritage 1.0'}.get(s['name'],s['name']),maker=s['maker'].replace(' Retired tile set',''),tile=s['tile'],tc=s.get('tc') or '#d6247f',tag=s.get('tag',''),album=s.get('album',''),rank=S['rank'][s['slug']],
      m=[[x['mat'],[r for r in x.get('racks',[]) if r in racks]] for x in s['matches'] if x['mat'] in mats]))
logos={k:bund(v,'PNG',90,360) for k,v in d['logos'].items() if isinstance(v,str) and v.startswith('data:')}
D=dict(mats=mats,racks=racks,tiles=tiles,sets=sets,uni=[u for u in d['uni'] if u in racks],order=S['mats'],logos=logos)
for f in os.listdir(SP):
    if f.startswith('b') and f.endswith('.js'):os.remove(SP+'/'+f)
chunks=[];cur={};sz=0
for h,u in B.items():
    cur[h]=u;sz+=len(u)
    if sz>4_500_000:chunks.append(cur);cur={};sz=0
if cur:chunks.append(cur)
tags=''
for i,c in enumerate(chunks):
    open(f'{SP}/b{i}.js','w').write('window.IMG=Object.assign(window.IMG||{},'+json.dumps(c,separators=(',',':'))+');');tags+=f'<script src="b{i}.js"></script>\n'
t=open('/tmp/sw2/tpl.html').read().replace('<!--BUNDLES-->',tags).replace('__DATA__',json.dumps(D,separators=(',',':')))
open(SP+'/index.html','w').write(t)
print('mats',len(mats),'racks',len(racks),'files',nfile,'bundles',[os.path.getsize(f'{SP}/b{i}.js')//1024 for i in range(len(chunks))],'index KB',os.path.getsize(SP+'/index.html')//1024)
