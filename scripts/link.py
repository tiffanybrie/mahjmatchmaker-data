import json,re
D=json.load(open('data.json')); C=json.load(open('catalog.json'))
norm=lambda s:re.sub(r'[^a-z0-9]','',s.lower().replace('&','and').replace('mahjong','').replace('mahj',''))
bn=[norm(b[0]) for b in C['B']]
def find(name,brand,kind):
    nb=norm(brand); n=name.lower().strip()
    cands=[i for i,c in enumerate(C['C']) if c[1]==kind and (bn[c[0]]==nb or nb in bn[c[0]] or bn[c[0]] in nb) and nb]
    best=None
    for i in cands:
        t=C['C'][i][2].lower()
        if re.search(r'(^|[^a-z])'+re.escape(n)+r'([^a-z]|$)',t):
            if best is None or len(t)<len(C['C'][best][2]): best=i
    return best
for m in D['M']: del m[4:]
for t in D['T']: del t[7:]
hit=0
for m in D['M']:
    j=find(m[0],m[1],1); m.append(j if j is not None else -1); hit+= j is not None
print('mats linked',hit,'/',len(D['M']))
th=0
for t in D['T']:
    j=find(t[1],t[2],0); t.append(j if j is not None else -1); th+= j is not None
print('tiles linked',th,'/',len(D['T']))
print([t[1] for t in D['T'] if t[-1]==-1])
json.dump(D,open('data.json','w'),separators=(',',':'),ensure_ascii=False)
# a curated-brand mat that appears in one of Tiffany's albums counts as approved
for m in D['M']:
    if m[4]>=0 and len(C['C'][m[4]])>13: C['C'][m[4]][13]=0
json.dump(C,open('catalog.json','w'),separators=(',',':'),ensure_ascii=False)
