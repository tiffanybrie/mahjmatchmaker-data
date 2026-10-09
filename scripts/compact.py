import json,re
it=json.load(open('items-colored.json'))
FAM=['pink','red','orange','yellow','green','teal','blue','purple','neutral','black']
K={'tiles':0,'mat':1,'rack':2}
brands=[];bi={}
refs={}
import html
for l in open('visit.tsv'):
    p,u=l.rstrip('\n').split('\t');u=html.unescape(u)
    dom=re.sub(r'^https?://','',u).split('/')[0].split('?')[0]
    m=re.search(r'[?&]((?:sca_ref|ref)=[^&]+)',u); refs[dom]=(m.group(1) if m else '',p)
C=[]
import os
EXCLUDE=set(json.load(open('exclude-brands.json'))) if os.path.exists('exclude-brands.json') else set()
FIX=json.load(open('color-fixes.json')) if os.path.exists('color-fixes.json') else {}
def key(i):
    m=re.match(r'https://([^/]+)/products/([^?]+)(?:\?.*?variant=(\d+))?',i['u']); return f"{m.group(1)}/{m.group(2)}"+(f"#{m.group(3)}" if m.group(3) else '')
out=[]
for i in it:
    if i['b'] in EXCLUDE: continue
    f=FIX.get(key(i))
    if f=='remove': continue
    if f=='multi': i['multi']=True
    elif f: i['c']=f; i['cs']=sorted(set(i['cs'])|{f})
    out.append(i)
it=out
for i in it:
    if i['b'] not in bi:
        bi[i['b']]=len(brands); r=refs.get(i['d'],('',''))
        brands.append([i['b'],i['d'],r[0],r[1]])
    m=re.match(r'https://[^/]+/products/([^?]+)(?:\?(.*))?',i['u']); handle=m.group(1); q=m.group(2) or ''
    var=re.search(r'variant=(\d+)',q); var=var.group(1) if var else ''
    img=i['i'].replace('https://cdn.shopify.com/s/files/','')
    mask=sum(1<<FAM.index(c) for c in i['cs'] if c in FAM)
    C.append([bi[i['b']],K[i['k']],i['t'],handle,var,img,round(i['p']),1 if i['a'] else 0,FAM.index(i['c']),mask,1 if i['multi'] else 0,'',1 if (i.get('mismatch') and not FIX.get(key(i))) else 0])
# Bird & Bamboo rack colors: one item per color, shown as the real swatch from Tiffany's color guide
if os.path.exists('bbracks.json'):
    bb=json.load(open('bbracks.json'))
    if 'Bird & Bamboo' not in bi:
        bi['Bird & Bamboo']=len(brands); r=refs.get('birdandbamboo.com',('','')); brands.append(['Bird & Bamboo','birdandbamboo.com',r[0],r[1]])
    price=0
    try:
        for p in json.load(open('raw/birdandbamboo.com.json')):
            if p['handle']=='20-inch-wooden-mahjong-rack-pusher-set-w-rack-bag': price=round(min(float(v['price']) for v in p['variants']))
    except Exception: pass
    for x in bb:
        m=re.match(r'https://[^/]+/products/([^?]+)\?.*?variant=(\d+)',x['url'])
        if not m: continue
        C.append([bi['Bird & Bamboo'],2,f"20\" Wooden Rack & Pusher Set – {x['name']}",m.group(1),m.group(2),'',price,1,FAM.index(x['fam']),1<<FAM.index(x['fam']),0,x['hex'],0])
D=dict(F=FAM,B=brands,C=C)
s=json.dumps(D,separators=(',',':'),ensure_ascii=False)
open('catalog.json','w').write(s); print(len(C),len(s))
