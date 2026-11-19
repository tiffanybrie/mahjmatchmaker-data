import json,re,urllib.request,urllib.parse,concurrent.futures,os,ssl,hashlib
S='/tmp/claude-0/-home-claude/05549d34-8fe3-5ca9-a6a5-308991cb9a78/scratchpad/deco/'
D=json.load(open(S+'D117.json'));M=D['mats'];p=json.load(open(S+'picks.json'))
ctx=ssl.create_default_context(cafile='/root/.ccr/ca-bundle.crt')
def get(u): return urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=40,context=ctx).read()
keys=sorted({c['key'] for c in p['deco-indigo']});old=json.load(open(S+'hd.json'));keys=[k for k in keys if not old.get(k,'').startswith('/')]
def one(k):
    m=M[k];u=m.get('u0') or ''
    if not u or '/products/' not in u:
        uu=m.get('u') or ''
        mm0=re.search(r'redirect=([^&]+)',uu)
        if mm0: u=f"{urllib.parse.urlparse(uu).scheme}://{urllib.parse.urlparse(uu).netloc}"+urllib.parse.unquote(mm0.group(1))
        elif '/products/' in uu: u=uu
    out=S+'hd/'+hashlib.md5(k.encode()).hexdigest()[:10]+'.jpg'
    try:
        pu=urllib.parse.urlparse(u);mm=re.search(r'/products/([^/?#]+)',pu.path)
        if not mm: return k,'nohandle'
        js=json.loads(get(f'{pu.scheme}://{pu.netloc}/products/{mm.group(1)}.json'))['product']
        q=urllib.parse.parse_qs(pu.query);vid=(q.get('variant') or [None])[0]
        if not vid and '?v=' in k: vid=k.split('?v=')[1]
        img=js['images'][0]
        if vid:
            for v in js['variants']:
                if str(v['id'])==str(vid) and v.get('image_id'):
                    img=next((i for i in js['images'] if i['id']==v['image_id']),img)
        src=img['src'];src+=('&' if '?' in src else '?')+'width=1600'
        open(out,'wb').write(get(src));return k,out
    except Exception as e: return k,'ERR '+str(e)[:60]
r={}
with concurrent.futures.ThreadPoolExecutor(10) as ex:
    for k,o in ex.map(one,keys): r[k]=o
old.update(r);json.dump(old,open(S+'hd.json','w'),indent=0)
for k,o in r.items():
    if not o.startswith('/'): print(M[k]['n'],o)
