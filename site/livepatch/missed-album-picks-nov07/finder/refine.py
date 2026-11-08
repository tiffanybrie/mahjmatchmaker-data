import json,collections,sys
sys.path.insert(0,'.')
from match import *
SITE='https://www.mahjmatchmaker.com'
A=json.load(open('missing_all.json'))
def sec(u):
    p=u.replace(SITE,'').split('#')[0].strip('/'); h=open(f'live/{p}.html').read()
    if '#' in u:
        sid=u.split('#')[1]; i=h.find(f'id="{sid}"'); j=h.find('<section class="mm3-hol"',i+10); h=h[i:j if j>0 else len(h)]
    return h
keep=[];cache={};drop=[]
for p in A['pairs']:
    u=p['album']
    if u not in cache: cache[u]=cards(sec(u))
    if on_page(p['mat'],p['brand'],cache[u]): continue
    if 'Mahjong Row' in (p['brand'] or ''): drop.append(('Mahjong Row is out of the site (Nov 6)',p)); continue
    p['flags']=[]
    if 'paige spearin' in p['mat'].lower(): p['flags'].append('paige-spearin-tdt (no commission)')
    if p['mat_hidden_fym']: p['flags'].append('mat hidden in FYM')
    keep.append(p)
A['pairs']=keep; A['dropped']=[{'why':w,**p} for w,p in drop]
json.dump(A,open('missing_final.json','w'),indent=1,ensure_ascii=False)
print('remaining',len(keep),'holiday',sum(p['hol'] for p in keep),'dropped',len(drop))
print(collections.Counter(p['album'][32:] for p in keep if 'holiday-mahjong' in p['album']))
