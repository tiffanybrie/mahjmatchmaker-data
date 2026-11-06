import json,sys,os
os.chdir('/dev/shm/sun')
sys.path.insert(0,'/home/claude/mahjmatchmaker-data/scripts/swipe/sunday_rebuild_oct29/wide')
import score as S
R='/home/claude/mahjmatchmaker-data/'
M=S.M; old=json.load(open('mats103.json'))
rk=json.load(open(R+'scripts/swipe/sunday_rebuild_oct29/wide/ranked.json'))
bk=json.load(open('book.json'))
inbook={it.get('key') for it in bk['items'].values()}
res={}
for sid in ['nature-walk','sunday-blues','plum-panda','hummingbird']:
    keys_in=[k for s,k in rk[sid] if k in inbook]
    scores=[s for s,k in rk[sid] if k in inbook]
    cut=min(scores) if scores else 0
    # re-score all current mats to get the same scale
    allL=sorted([(S.score(sid,k,m),k) for k,m in M.items() if S.ok(k,m) and S.score(sid,k,m)],reverse=True)
    new=[(sc[0],k) for sc,k in allL if k not in old]
    print(sid,'book-from-ranked',len(keys_in),'cut',cut,'new visible scored',len(new))
    top=[(s,k,M[k]['n'],M[k]['bn']) for s,k in new if s>=cut]
    print('  new >= cut:',len(top))
    for t in top[:40]: print('   ',t)
    res[sid]=top
json.dump(res,open('new_cands.json','w'))
