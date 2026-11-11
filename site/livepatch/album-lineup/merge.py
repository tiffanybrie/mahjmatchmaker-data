import json,re
R='/home/claude/mahjmatchmaker-data/'
live=json.load(open('/tmp/claude-0/plan2/sets.json'))
snap=json.load(open(R+'config/partner-products-snapshot.json'))
BAD=re.compile(r'travel|\bmini\b|flower tiles|joker|\bbag\b|case|clutch|dice|pusher|rack|sticker|keychain|replacement|bonus|blank|tote|pouch|coaster|gift card|\bmat\b|tray|kids|little mahj|wall art|odd lots|scratch|skinny|tablecloth|rummi|rummy|numbered',re.I)
def hostset(h): return {h, 'www.'+h, h.replace('www.','')}
out={}
for b,v in live.items():
  sets=[]
  seen=set()
  for h in v['hosts']:
    for hk,P in snap.items():
      if hk.replace('www.','')!=h.replace('www.',''): continue
      for hd,pr in P.items():
        if pr.get('kind')!='tiles' or BAD.search(pr['title']) or not (150<=(pr.get('min') or 0)<=1000): continue
        sets.append({'title':pr['title'],'price':pr.get('min'),'pub':(pr.get('published') or '')[:10],'avail':pr.get('avail'),'pre':pr.get('pre'),'pretags':pr.get('pretags',[]),'img':pr.get('img') or '','url':f'https://{hk}/products/{hd}'}); seen.add(hd)
  if not sets: sets=[s for s in v['sets'] if not BAD.search(s['title'])]
  sets.sort(key=lambda s:s['pub'] or '',reverse=True)
  v=dict(v,sets=sets); out[b]=v
  print(len(sets),b)
out['Mah Jongg Maven']['sets']=[{'title':'Coca-Cola Classic American Mah Jongg Tile Set','price':450,'pub':'2026-08','avail':True,'pre':True,'pretags':['preorder'],'img':'https://mahjonggmaven.com/wp-content/uploads/2026/08/tile-set--scaled.jpg','url':'https://mahjonggmaven.com/product/coca-cola-classic-mah-jongg-set-tile-set/'}]
json.dump(out,open('/tmp/claude-0/plan2/sets2.json','w'))
