import json,subprocess,time,urllib.parse,re,sys
recs=json.load(open('../fym_tiles.json')); alb=json.load(open('albums_shop.json'))
items={}
for r in recs:
    u=r['u']
    if 'mahjmatchmaker.com' in u: continue
    items.setdefault(u.split('?')[0],[]).append(('fym',r['key'],r['n'],r['bn']))
for a,v in alb.items():
    if v['shop'] and '/products/' in v['shop']:
        items.setdefault(v['shop'].split('?')[0],[]).append(('album',a,v['label'],v['brand']))
res={}
def get(url):
    p=subprocess.run(['curl','-s','-L','-m','25','-A','Mozilla/5.0','-w','\n%{http_code}',url],capture_output=True,text=True)
    body,_,code=p.stdout.rpartition('\n'); return code,body
for n,(u,who) in enumerate(items.items()):
    pu=urllib.parse.urlparse(u)
    st='unclear'; ev=u; det=''
    if '/products/' in pu.path:
        code,body=get(u+'.js')
        if code=='200':
            try:
                j=json.loads(body); av=j.get('available'); st='available' if av else 'sold out (still listed)'; det=j.get('title','')
            except Exception:
                code2,b2=get(u); st='unclear'; det='non-shopify http '+code2+(' soldout-text' if re.search(r'sold out',b2,re.I) else '')
        elif code=='404':
            code2,b2=get(u); st='retired/vault' if code2=='404' else 'unclear'; det='js 404, page '+code2
        else: det='http '+code
    else:
        code,b=get(u); det='non-product url http '+code
    res[u]={'status':st,'detail':det,'who':who}
    print(n,st,u,det,flush=True); time.sleep(1.2)
json.dump(res,open('check_result.json','w'),indent=1)
