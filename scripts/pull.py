import json,subprocess,sys,os,time
rows=[l.rstrip('\n').split('\t') for l in open('domains.tsv')]
out={}
for page,dom in rows:
    dom=dom.split('?')[0]
    allp=[];ok=True
    for pg in range(1,20):
        url=f"https://{dom}/products.json?limit=250&page={pg}"
        r=subprocess.run(['curl','-sS','-m','25','-L','-A','Mozilla/5.0',url],capture_output=True,text=True)
        try: d=json.loads(r.stdout)
        except Exception: ok=False;break
        ps=d.get('products',[])
        allp+=ps
        if len(ps)<250: break
        time.sleep(0.5)
    json.dump(allp,open(f'raw/{dom}.json','w'))
    print(f"{dom}\t{len(allp) if ok or allp else 'NOT SHOPIFY/blocked'}",flush=True)
