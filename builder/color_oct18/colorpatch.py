import json,sys,re
SP='/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/'
REPO='/home/claude/mahjmatchmaker-data/'
sys.path.insert(0,SP+'fymcolor'); from props import P,H
OLD=json.load(open(REPO+'config/tile-back-colors.json'))
Dc=json.load(open(SP+'fymaudit/D_cur.json'));S0=Dc['sets']
TGT=sys.argv[1] if len(sys.argv)>1 else SP+'fymaudit/index.html'
html=open(TGT).read()
i=html.find('const D=')+8;D,j=json.JSONDecoder().raw_decode(html,i);S=D['sets']
key=lambda s:(s['name'],s['maker'])
cur={key(s):s for s in S}
WEB=['Holiday','Pink','Red','Blue','Green','Purple','Yellow & Orange','Brown','Ivory','Natural Patterns']
BG={g:list(OLD[g]) for g in WEB}
assert set(OLD)==set(WEB)
prop={}
allp={**H,**P}
order=sorted(allp,key=lambda k:(0 if allp[k][1] in('her','album') else 1, S0[k]['name']))
for k in order:
    groups,conf,note=allp[k];s=S0[k]
    assert key(s) in cur,(k,s['name'])
    for g in groups:
        if s['name'] not in BG[g]: BG[g].append(s['name'])
    prop[s['name']]={'maker':s['maker'],'groups':groups,'confidence':{'her':'Tiffany','album':'proposed-album','h':'proposed-clear','m':'proposed-likely','l':'proposed-back-not-shown','dark':'needs-decision-black','notset':'not-a-tile-set'}[conf],'note':note}
# write html: D tiles swaps
sw=json.load(open(SP+'fymcolor/swap.json'))
for s in S:
    if s['name'] in sw and (s['maker']!='Oh My Mahjong' or s['name']=='Papaya Spritz'):
        D['tiles'][s['tile']]['pile']=sw[s['name']]['pile'];D['tiles'][s['tile']]['full']=sw[s['name']]['full']
html=html[:i]+json.dumps(D,ensure_ascii=False,separators=(',',':'))+html[j:]
a=html.find('const BACKG=');b=html.find(';',a)
html=html[:a]+'const BACKG='+json.dumps(BG,ensure_ascii=False,separators=(',',':'))+html[b:]
old='(BACKG[S.tcol]||[]).map(n=>all.find(x=>x[0].name===n)).filter(Boolean)'
if old in html: html=html.replace(old,'(BACKG[S.tcol]||[]).flatMap(n=>all.filter(x=>x[0].name===n))')
if 'b10v1.js' not in html: html=html.replace('<script src="b9v1.js"></script>','<script src="b9v1.js"></script><script src="b10v1.js"></script>')
assert 'b10v1.js' in html
open(TGT,'w').write(html)
json.dump(BG,open(REPO+'config/tile-back-colors.json','w'),ensure_ascii=False,indent=1)
json.dump(prop,open(REPO+'config/tile-back-colors-proposed.json','w'),ensure_ascii=False,indent=1)
tagged=set(n for v in BG.values() for n in v)
un=[(s['name'],s['maker']) for s in S if s['name'] not in tagged]
json.dump(un,open(SP+'fymcolor/untagged_after.json','w'),ensure_ascii=False,indent=1)
print('untagged after',len(un));[print(' ',x) for x in un]
