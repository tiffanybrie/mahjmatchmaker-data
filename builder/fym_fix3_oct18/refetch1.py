# fetch product json (image lists) for every visible mat and tile set
import json,sys,os,re,subprocess,hashlib,collections,concurrent.futures as cf
sys.path.insert(0,'f3'); from matimg import *
D=loadD(); M=D['mats']; T=D['tiles']
vis=[('m',m,M[m].get('u','')) for m in M if not M[m].get('hid')]
vis+=[('t',t,T[t].get('u','')) for t in T]
def pj(x):
    kind,k,u=x
    mm=re.match(r'https?://([^/]+)/(?:collections/[^/]+/)?products/([^/?#]+)',u)
    if not mm: return kind+'|'+k,None
    url=f'https://{mm.group(1)}/products/{mm.group(2)}.json'
    fn='f3/pj/'+hashlib.md5(url.encode()).hexdigest()[:12]+'.json'
    if not os.path.exists(fn) or os.path.getsize(fn)<50:
        subprocess.run(['curl','-s','-L','-m','25','-A','Mozilla/5.0','-o',fn,url])
    try:
        d=json.load(open(fn))['product']; return kind+'|'+k,[(i['src'],i.get('width'),i.get('height')) for i in d['images']]
    except Exception: return kind+'|'+k,None
with cf.ThreadPoolExecutor(12) as ex: out=dict(ex.map(pj,vis))
json.dump(out,open('f3/pj_imgs.json','w'))
print(len(vis),sum(1 for v in out.values() if v))
c=collections.Counter((k.split('|')[0],(M if k[0]=='m' else T)[k.split('|',1)[1]]['bn']) for k,v in out.items() if not v)
print(c.most_common(40))
