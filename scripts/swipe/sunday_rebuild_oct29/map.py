import json,re,unicodedata
def slug(x):
    x=unicodedata.normalize('NFKD',x).encode('ascii','ignore').decode().lower().replace('&',' ')
    return re.sub(r'[^a-z0-9]+','-',x).strip('-')
F=json.load(open('F.json')); M=F['mats']; KEYS=list(M)
D=json.load(open('D.json'))
def bnorm(b): return slug(b).replace('mahjongg','mahjong').replace('-co','')
idx_handle={}; idx_nb={}; idx_n={}
for k,m in M.items():
    h=slug(k.split('/',1)[-1].split('?')[0].split(':')[-1])
    idx_handle.setdefault(h,[]).append(k)
    idx_nb.setdefault((slug(m.get('n','')),bnorm(m.get('bn',''))),[]).append(k)
    idx_n.setdefault(slug(m.get('n','')),[]).append(k)
def match(it):
    iid=it['id']; lab=it['label']; parts=[p.strip() for p in lab.split('·')]
    name=parts[0]; brand=parts[1] if len(parts)>1 else ''
    # handle suffix
    best=None
    for h,ks in idx_handle.items():
        if len(h)>=5 and (iid==h or iid.endswith('-'+h) or iid.endswith(h)):
            if best is None or len(h)>len(best[0]): best=(h,ks)
    if best and len(best[1])==1: return best[1][0],'handle'
    ks=idx_nb.get((slug(name),bnorm(brand)))
    if ks and len(ks)==1: return ks[0],'namebrand'
    # strip mat words
    n2=re.sub(r'\b(mahjong|mat|mats|neoprene|leatherette|premium|in tube|w tube|travel)\b','',name,flags=re.I)
    for (nn,bb),ks in idx_nb.items():
        if bb==bnorm(brand) and slug(n2) and slug(n2)==re.sub(r'-?(mahjong|mat|mats|neoprene|leatherette|premium)-?','-',nn).strip('-') and len(ks)==1: return ks[0],'fuzzy'
    if best: return best[1][0],'handle-multi'
    return None,None
if __name__=='__main__':
    import collections
    res={}; c=collections.Counter(); miss=[]
    for it in D['items']:
        k,how=match(it); c[how]+=1; res[it['id']]=k
        if not k: miss.append(it['label'])
    print(c); print(len(miss)); print(miss)
    json.dump(res,open('map.json','w'),indent=0)
