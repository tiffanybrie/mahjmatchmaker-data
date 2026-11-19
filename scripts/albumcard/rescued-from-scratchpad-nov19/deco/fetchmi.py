import json,re,urllib.request,urllib.parse,concurrent.futures,os,hashlib,ssl
S='/tmp/claude-0/-home-claude/05549d34-8fe3-5ca9-a6a5-308991cb9a78/scratchpad/deco/'
D=json.load(open(S+'D117.json'));M=D['mats'];P=json.load(open(S+'pool.json'));gm=json.load(open(S+'galmap.json'))
need=[k for k in set(P['lag'])|set(P['mul']) if k not in gm]
ctx=ssl.create_default_context(cafile='/root/.ccr/ca-bundle.crt')
def get(u):
    r=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'});return urllib.request.urlopen(r,timeout=30,context=ctx).read()
def one(k):
    m=M[k];u=m.get('u0') or ''
    out=S+'mi/'+hashlib.md5(k.encode()).hexdigest()[:12]+'.jpg'
    if os.path.exists(out): return k,out
    try:
        pu=urllib.parse.urlparse(u)
        mm=re.search(r'/products/([^/?#]+)',pu.path)
        if not mm: return k,'nohandle '+u
        js=json.loads(get(f'{pu.scheme}://{pu.netloc}/products/{mm.group(1)}.json'))['product']
        q=urllib.parse.parse_qs(pu.query);vid=(q.get('variant') or [None])[0]
        if not vid and '?v=' in k: vid=k.split('?v=')[1]
        img=js['images'][0]
        if vid:
            for v in js['variants']:
                if str(v['id'])==str(vid) and v.get('image_id'):
                    img=next((i for i in js['images'] if i['id']==v['image_id']),img)
        src=img['src']; src+=('&' if '?' in src else '?')+'width=900'
        open(out,'wb').write(get(src));return k,out
    except Exception as e: return k,'ERR '+str(e)[:80]
res={}
with concurrent.futures.ThreadPoolExecutor(12) as ex:
    for k,o in ex.map(one,need): res[k]=o
json.dump(res,open(S+'mi.json','w'),indent=0)
bad={k:v for k,v in res.items() if not v.startswith('/')}
print(len(res),'bad',len(bad))
for k,v in bad.items(): print(M[k]['bn'],M[k]['n'],v[:100])
