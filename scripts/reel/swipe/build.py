import json,sys,subprocess,os
here=os.path.dirname(os.path.abspath(__file__))
spec=json.load(open(sys.argv[1]));out=sys.argv[2]
t=open(os.path.join(here,'swipe.html')).read()
for k in ['SMITH','MAT1','FLAME','WORDMARK']:t=t.replace(k,spec['assets'][k])
cards=spec['cards'];T=[];x=spec.get('start',1.6)
for c in cards:
    hold=c.get('hold',2.4 if c['yes'] else 1.3)
    T.append([x,x+hold,x+hold+0.55]);x+=hold+0.55+0.35
t=t.replace('CARDS',json.dumps(cards)).replace('TIMING',json.dumps(T)).replace('ENDAT',str(x+0.2))
dur=x+0.2+spec.get('endhold',3.6)
open(out+'.html','w').write(t)
json.dump({'dur':dur,'T':T},open(out+'.json','w'))
print('dur',round(dur,2),T)
