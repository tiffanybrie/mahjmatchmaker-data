import json,re,urllib.request,concurrent.futures as cf,collections
H={'User-Agent':'Mozilla/5.0'}
import os
R0=os.path.dirname(os.path.abspath(__file__))+'/../'
P=set(json.load(open(R0+'catalog/fym_mat_keys.json')))
L=json.load(open(R0+'catalog/locked_decisions.json'))
B=json.load(open(R0+'catalog.json'))['B']
brands=[(b[0],b[1],True) for b in B]
brands+=[('Mahjong Register','mahjongregister.com',True),('Royal Mahjong Society','theroyalmahjongsociety.com',True)]
for b,d,t in json.load(open(R0+'config/fym_extra_brands.json')):
    if d and t=='shopify' and b not in ('Mahjong Register','Mahjong Co.','Mini Mahjer'): brands.append((b,d,False))
MAT=re.compile(r'\bmats?\b|playmat|play mat|game mat|mahjong mat',re.I)
NOT=re.compile(r'rack|pusher|\bbag\b|tote|tube(?! *$)|caddy|storage|tile set|tiles\b|\bkit\b|bundle|solo play|practice|table ?cover|tablecloth|desk mat|coaster|mouse|puzzle|gift card|sticker|card holder|scorecard|\bcards?\b|book|class|lesson|ticket|strap|band\b|sleeve|wrap|ornament|candle|napkin|placemat|bar mat|cocktail|dice|wallet|pouch|case\b|hat\b|shirt|sweatshirt|mug|glass|charm|necklace|earring|bracelet|keychain|pin\b|patch|towel|blanket|pillow|umbrella stand|card table|table\b',re.I)
def isTubeMat(t): return re.search(r'mat (in|w/?|with) tube',t,re.I)
def get(u): return json.loads(urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=40).read())
def harvest(b):
    name,dom,partner=b;out=[];allp=[]
    for pg in range(1,20):
        try: j=get(f'https://{dom}/products.json?limit=250&page={pg}')
        except Exception as e: return name,dom,partner,None,str(e)
        if not j['products']: break
        allp+=j['products']
    for p in allp:
        t=p['title'];ty=p.get('product_type','')
        txt=t+' '+ty
        if not (MAT.search(txt)): continue
        if NOT.search(t) and not isTubeMat(t): continue
        if re.search(r'rack|pusher|bag|tube|storage|kit|bundle|tile',ty,re.I) and not re.search(r'\bmat',ty,re.I): continue
        imgs={i['id']:i['src'] for i in p['images']}
        if not imgs: continue
        base=f"{dom}/{p['handle']}"
        vs=[(v['id'],v['title'],v.get('image_id')) for v in p['variants']]
        vimg={i for _,_,i in vs if i}
        if len(vimg)>1:
            g=collections.OrderedDict()
            for vid,vt,im in vs:
                if 'coming soon' in vt.lower() or 'sold out' in vt.lower(): continue
                col=vt.split(' / ')[0].strip()
                e=g.setdefault(col,[vid,im])
                if not e[1] and im: e[1]=im
            for col,(vid,im) in g.items():
                if not im: continue
                out.append(dict(key=base+'?v='+str(vid),base=base,n=t,var=col,img=imgs.get(im),imgs=list(imgs.values())[:10],url=f"https://{dom}/products/{p['handle']}?variant={vid}",brand=name,partner=partner,avail=any(v.get('available',True) for v in p['variants'])))
        else:
            out.append(dict(key=base,base=base,n=t,var='',img=p['images'][0]['src'],imgs=list(imgs.values())[:10],url=f"https://{dom}/products/{p['handle']}",brand=name,partner=partner,avail=any(v.get('available',True) for v in p['variants'])))
    return name,dom,partner,out,len(allp)
with cf.ThreadPoolExecutor(10) as ex: R=list(ex.map(harvest,brands))
allc=[];
for name,dom,partner,out,n in R:
    if out is None: print('FAIL',name,dom,n);continue
    new=[o for o in out if o['key'] not in P and o['key'] not in L and o['base'] not in L]
    have=[o for o in out if o['key'] in P]
    print(f"{name:28s} {dom:32s} products {n:4d} mats {len(out):4d} in-catalog {len(have):3d} NEW {len(new):4d}")
    allc+=new
json.dump(allc,open(R0+'work/fym_new_items.json','w'),indent=0)
print('TOTAL NEW',len(allc))
