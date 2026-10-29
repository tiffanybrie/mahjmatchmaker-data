import json,shutil,os
P=json.load(open('plan2.json')); KF=json.load(open('kf.json')); M=json.load(open('mats.json'))
cur=json.load(open('cur.json')); D=cur['D']; V=cur['V']
DROP={'nature-walk':[5,7,8,9,11,14,15,17,19,20,21,22,24,28,32,33,35,38,39,40,41,45,47,50,53,55,56,
 60,61,62,64,66,67,69,70,71,72,74,75,76,77,78,79,80,82,84,85,88,90,92,94,96,97,98,99,104,105,106,108,110],
'sunday-blues':[8,11,15,22,25,26,32,36,48,49,50,54,56,58,59,62,67,69,79,86,89,90,92,93,95,97,99,100,101,102,103,105,111,113],
'plum-panda':[8,10,13,14,15,17,19,23,24,29,32,36,38,41,42,44,45,46,50,52,54,56,58,61,62,64,67,68,69,70,72,73,75,77,78,83,85,86,87,88,96,99,101,102,103,104],
'hummingbird':[2,4,5,6,8,18,20,21,22,25,28,29,30,32,33,35,38,40,42,44,45,46,48,49,53,57,59,
 60,61,62,64,67,70,72,75,76,78,79,80,82,83,85,89,91,93,94,95,96,97,98,99,100,101,102,104,105,107,108,110]}
items={x['id']:x for x in D['items']}
newitems={}; order={}; rep={}
os.makedirs('../sunday/pub/mz',exist_ok=True)
for g,p in P.items():
    ks=p['tnt']+p['cand']; dr=set(DROP[g]); keep=[k for i,k in enumerate(ks) if i not in dr]
    seq=[]
    for k in keep:
        m=M[k]; tnt=k in p['tnt']
        iid=p['k2old'].get(k) or KF[k]
        lab=('TNT rec · ' if tnt else '')+m['n']+' · '+m['bn']
        if iid in items and not tnt: it=dict(items[iid])
        else:
            if iid in items: it=dict(items[iid]); it['label']=lab
            else:
                shutil.copy('mx/'+KF[k]+'.jpg','../sunday/pub/mz/'+KF[k]+'.jpg'); it={'id':iid,'label':lab,'img':'mz/'+KF[k]+'.jpg'}
        newitems[iid]=it; seq.append(iid)
    voted=p['voted']
    for v in voted: newitems[v]=items[v]
    order[g]=seq+[v for v in voted if v not in seq]
    rep[g]=dict(tnt=len(p['tnt']),new=len(seq)-len(p['tnt']),voted=len(voted),total=len(order[g]))
D2=dict(D); D2['items']=list(newitems.values()); D2['order']=order
json.dump(D2,open('D2.json','w')); print(rep, len(D2['items']))
