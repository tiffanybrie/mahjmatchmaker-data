import json,re
A=json.load(open('albums.json'))
P='https://images.squarespace-cdn.com/content/69b1d01289d0f8016ee3d508/'
colors={'pink':'amara coquette dandy glitterville glow-wild la-fete','blue':'birdie gatsby lagoon lola moonlight osler seabreeze nantucket','green':'cypress-forest drake emerald jade jasmine malachite palm-royale willow','yellow':'heritage-2-0 heritage limoncello pippa sierra solara sorbet sunset tortoise','purple':'gemma luminaire taylor','neutral':'cypress-forest heritage-2-0 heritage jade malachite palm-royale pearlescent smith talulah tortoise'}
uni=['heritage','smith','cypress-forest','pearlescent','tortoise','talulah','jade','malachite','palm-royale','coquette']
R=[];Ri={};M=[];Mi={};T=[];X=[]
def rk(n,u):
    k=n
    if k not in Ri: Ri[k]=len(R); R.append([n,u])
    return Ri[k]
for a in A:
    slug=a['slug'].replace('-mahjong-tile-matches','')
    cs=[c for c,v in colors.items() if slug in v.split()]
    ti=len(T)
    name=a['tile']
    T.append([slug,name,a['maker'],a['cover'].replace(P,''),a['tileShop'],cs,(uni.index(slug)+1) if slug in uni else 0])
    for c in a['cards']:
        k=(c['mat'].lower().strip(),c['brand'].lower().strip())
        if k not in Mi:
            Mi[k]=len(M); M.append([c['mat'],c['brand'],c['shop'] if 'Mat' in c['shopLabel'] or 'mat' in c['shopLabel'] else '',1 if c['retired'] else 0])
        mi=Mi[k]
        if not M[mi][2] and ('Mat' in c['shopLabel']): M[mi][2]=c['shop']
        X.append([ti,mi,c['img'].replace(P,''),c['take'],[rk(n,u) for u,n in c['racks']],int(c['n'] or 0)])
D=dict(P=P,T=T,M=M,R=R,X=X)
s=json.dumps(D,separators=(',',':'),ensure_ascii=False)
open('data.json','w').write(s)
print(len(T),len(M),len(R),len(X),len(s))
import gzip;print('gz',len(gzip.compress(s.encode())))
print([t[1] for t in T if not t[5]])
print(sum(1 for m in M if not m[2]),'mats without shop link')
