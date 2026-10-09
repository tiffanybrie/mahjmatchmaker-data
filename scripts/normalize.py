import json,glob,os,re,html
from classify import kind
BRAND={}
for l in open('visit.tsv'):
    p,u=l.rstrip('\n').split('\t'); u=html.unescape(u)
    dom=re.sub(r'^https?://','',u).split('/')[0].split('?')[0]
    m=re.search(r'[?&]((?:sca_ref|ref)=[^&]+)',u)
    BRAND[dom]=dict(page=p,ref=m.group(1) if m else '')
NAMES={l.split('\t')[1].strip().split('?')[0]:l.split('\t')[0] for l in open('domains.tsv')}
pretty={}
for l in open('hub-at-a-glance.html'):
    m=re.search(r'href="(/[^"]+)"><strong>(.*?)</strong>',l)
    if m: pretty[m.group(1)]=html.unescape(m.group(2))
items=[]
for f in sorted(glob.glob('raw/*.json')):
    dom=os.path.basename(f)[:-5]; b=BRAND.get(dom,{}); page=b.get('page') or NAMES.get(dom,'')
    bname=pretty.get(page,dom)
    for p in json.load(open(f)):
        k=kind(p)
        if k=='other': continue
        img=p['images'][0]['src'] if p.get('images') else ''
        vs=p.get('variants',[])
        price=min((float(v['price']) for v in vs),default=0)
        avail=any(v.get('available') for v in vs)
        base=f"https://{dom}/products/{p['handle']}"
        def link(var=None):
            q=[]
            if var: q.append(f"variant={var}")
            if b.get('ref'): q.append(b['ref'])
            return base+('?'+'&'.join(q) if q else '')
        # racks: split color variants into separate items when variants carry images or color option
        opts=[o['name'].lower() for o in p.get('options',[])]
        ci=next((i for i,o in enumerate(opts) if 'color' in o or 'colour' in o),None)
        if k=='rack' and ci is not None and len(vs)>1:
            imgs={im['id']:im['src'] for im in p.get('images',[])}
            seen=set()
            for v in vs:
                col=v.get(f'option{ci+1}');
                if not col or col in seen: continue
                seen.add(col)
                vi=(v.get('featured_image') or {}).get('src') or img
                items.append(dict(b=bname,d=dom,k=k,t=f"{p['title']} – {col}",u=link(v['id']),i=vi,p=float(v['price']),a=bool(v.get('available')),tags=p.get('tags',[]),pt=p.get('product_type','')))
        else:
            items.append(dict(b=bname,d=dom,k=k,t=p['title'],u=link(),i=img,p=price,a=avail,tags=p.get('tags',[]),pt=p.get('product_type','')))
json.dump(items,open('items.json','w'))
from collections import Counter
print(len(items),Counter(i['k'] for i in items)); print(Counter(i['b'] for i in items).most_common(40))
