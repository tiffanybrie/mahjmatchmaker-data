# v2 (Nov 2): same as stock.py, against FYM v113 data in /dev/shm/introv2
import json,re,sys,subprocess,concurrent.futures as cf
from urllib.parse import urlparse,unquote
D=json.load(open('/dev/shm/introv2/D.json'))
M=D['mats']
EX={'Etsy','Tigre de Tartan','Splash of Color','Mahjong Studios','Yellow Mountain'}
def prod_url(k,v):
    u=v.get('u0') or v.get('u','')
    if 'redirect=' in u:
        p=urlparse(u); dom=p.netloc; r=unquote(re.search(r'redirect=([^&]+)',u).group(1)); path=r.split('?')[0]
    else:
        p=urlparse(u); dom=p.netloc; path=p.path
    m=re.search(r'/products/([^/?#]+)',path)
    return (dom, m.group(1)) if m else (dom,None)
cands=[k for k,v in M.items() if v['hol'] and not v.get('hid') and v['bn'] not in EX and 'paige' not in v['n'].lower()]
def chk(k):
    dom,h=prod_url(k,M[k])
    if not h: return k,None,'nohandle',dom
    try:
        o=subprocess.run(['curl','-sS','-m','20','-A','Mozilla/5.0','-L',f'https://{dom}/products/{h}.js'],capture_output=True,text=True).stdout
        j=json.loads(o); av=j.get('available'); vs=[(x.get('title'),x.get('available')) for x in j.get('variants',[])]
        return k,av,vs,f'https://{dom}/products/{h}'
    except Exception as e: return k,None,'err '+str(e)[:60],f'https://{dom}/products/{h}'
res={}
with cf.ThreadPoolExecutor(16) as ex:
    for k,av,vs,url in ex.map(chk,cands):
        res[k]={'n':M[k]['n'],'bn':M[k]['bn'],'pa':M[k]['pa'],'avail':av,'variants':vs,'url':url,'f':M[k]['f']}
json.dump(res,open('/dev/shm/introv2/stock.json','w'),indent=1)
import collections
print(len(res), collections.Counter(str(v['avail']) for v in res.values()))
for k,v in res.items():
    if v['avail'] is not True: print(v['avail'],v['bn'],'|',v['n'],'|',str(v['variants'])[:80])
