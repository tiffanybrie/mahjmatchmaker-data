import json,re,collections
D=json.load(open('D.json')); M=D['mats']
A=json.load(open('/home/claude/mahjmatchmaker-data/work/albums.json')); L=A if isinstance(A,list) else list(A.values())
def nn(s): s=re.sub(r'\(.*?\)','',s.lower()); s=s.replace('&','and'); return re.sub(r'[^a-z0-9]','',s)
def nb(s): s=nn(s); return s.replace('mahjong','').replace('mahjongg','').replace('co','')
idx=collections.defaultdict(list)
for i,m in M.items(): idx[(nn(m['n']),nb(m['bn']))].append(i); idx[(nn(m['n']),'*')].append(i)
sets={s['slug']:s for s in D['sets']}
def setslug(a): return a['slug'].replace('-mahjong-tile-matches','')
unmapped=collections.Counter(); truth={}
for a in L:
    sl=setslug(a); ids=[]
    for c in a['cards']:
        k=(nn(c['mat']),nb(c['brand'])); cand=idx.get(k) or idx.get((nn(c['mat']),'*'))
        if not cand: unmapped[(c['mat'],c['brand'])]+=1; ids.append(None); continue
        ids.append(cand[0] if len(cand)==1 else sorted(cand,key=lambda i:(i.startswith('alb:'),i))[0])
    truth[sl]=ids
res=[]
miss_tot=extra_tot=0; off=0
for sl,ids in truth.items():
    s=sets.get(sl)
    if not s: res.append((sl,'NO SET IN FYM')); continue
    have=[x[0] for x in s['m']]; want=[i for i in ids if i]
    miss=[i for i in want if i not in have]; extra=[i for i in have if i not in want]
    if miss or extra: off+=1
    miss_tot+=len(miss); extra_tot+=len(extra)
    res.append((sl,len(want),len(have),len(miss),len(extra)))
for r in res: print(r)
print('sets off',off,'missing',miss_tot,'extra',extra_tot)
print('unmapped album mats',len(unmapped)); print(unmapped.most_common(60))
json.dump({k:v for k,v in truth.items()},open('truth.json','w'))
