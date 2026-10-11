"""Pull partner stores that run on Squarespace (not Shopify) into raw/<domain>.json
in the same shape pull.py writes for Shopify stores, so classify/compact treat them alike.
Config: config/sqsp-stores.tsv  -> page<TAB>domain<TAB>collection path(s, comma-separated)"""
import json,subprocess,os,time
rows=[l.rstrip('\n').split('\t') for l in open('config/sqsp-stores.tsv') if l.strip() and not l.startswith('#')]
def get(url):
    r=subprocess.run(['curl','-sS','-L','-m','30','-A','Mozilla/5.0 (Macintosh)',url],capture_output=True,text=True)
    return json.loads(r.stdout)
os.makedirs('raw',exist_ok=True)
for page,dom,paths in rows:
    out=[]
    for path in paths.split(','):
        url=f"https://{dom}{path}?format=json";n=0
        while url and n<20:
            try: d=get(url)
            except Exception as e: print(dom,path,'not json');break
            for it in d.get('items',[]):
                sc=it.get('structuredContent') or {}
                vs=it.get('variants') or sc.get('variants') or []
                price=None
                if vs:
                    pm=(vs[0].get('priceMoney') or {}).get('value')
                    price=pm if pm else (vs[0].get('price',0)/100 if vs[0].get('price') else None)
                imgs=[{'src':x.get('assetUrl')} for x in (it.get('items') or []) if x.get('assetUrl')] or ([{'src':it['assetUrl']}] if it.get('assetUrl') else [])
                out.append({'title':it.get('title',''),'handle':it.get('fullUrl','').strip('/'),'url':f"https://{dom}{it.get('fullUrl','')}",
                    'product_type':', '.join(it.get('categories') or []),'tags':it.get('tags') or [],'images':imgs,
                    'variants':[{'price':str(price) if price is not None else '','available':(v.get('qtyInStock',1)!=0 or v.get('unlimited',False))} for v in vs] or [{'price':'','available':True}],
                    'body_html':it.get('excerpt',''),'source':'squarespace'})
            p=d.get('pagination') or {}
            url=f"https://{dom}{p['nextPageUrl']}&format=json" if p.get('nextPage') and p.get('nextPageUrl') else None
            n+=1;time.sleep(0.5)
    json.dump(out,open(f'raw/{dom}.json','w'))
    print(f'{dom}\t{len(out)}')
