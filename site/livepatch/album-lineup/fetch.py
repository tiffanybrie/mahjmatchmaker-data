import json,re,subprocess,sys
R='/home/claude/mahjmatchmaker-data/'
P=json.load(open('/tmp/claude-0/partners.json'))
routes=json.load(open(R+'config/link-routes.json'))['brands']
def norm(t): return re.sub(r'[^a-z0-9]','',t.lower().replace('&','and'))
EXTRA={'The Royal Mahjong Society':['theroyalmahjongsociety.com'],'Mah Jongg Maven':['mahjonggmaven.com'],'The Mahjong Press':['themahjonghouse.com'],'Amanda Toppe':['amandatoppeart.com'],'Soirée All Day':['soireeallday.co'],'Sunday Mahjong':['sundaymahjong.com'],'Mahjong by SI':[],'Sweet Jojo Designs':[]}
BAD=re.compile(r'travel|\bmini\b|flower|joker|\bbag\b|case|clutch|dice|pusher|rack|sticker|\bcard|charm|keychain|replacement|single|extra|bonus|blank|tote|pouch|coaster|gift card|\bmat\b|tray|kids|little mahj|wall art|odd lots|scratch|sample|skinny|tablecloth|table cloth|book|rummi|rummy|tile bag|cover',re.I)
GOOD=re.compile(r'\btiles?\b|tile set|mahjong set',re.I)
out={}
brands=[(p['brand'],p['stage']) for p in P]+[('Sunday Mahjong','non-partner (allowed)')]
for b,stage in brands:
  rk=next((k for k in routes if norm(k)==norm(b) or norm(k).startswith(norm(b)[:8])),None)
  hosts=EXTRA.get(b) if b in EXTRA else [h for h in (routes.get(rk,{}).get('store_hosts') or []) if 'amazon' not in h and 'etsy' not in h and 'pxf' not in h]
  if b=='The Mahjong Press': hosts=['themahjonghouse.com']
  sets=[];ok=None
  for h in hosts:
    for page in (1,2,3):
      r=subprocess.run(['curl','-sL','--max-time','25',f'https://{h}/products.json?limit=250&page={page}'],capture_output=True,text=True).stdout
      try: d=json.loads(r)
      except Exception: ok=False if ok is None else ok; break
      ok=True; L=d.get('products',[])
      for x in L:
        t=x['title']
        try: pr=float(x['variants'][0]['price'] or 0)
        except: pr=0
        if GOOD.search(t) and not BAD.search(t) and 150<=pr<=1000:
          sets.append({'title':t,'price':pr,'pub':(x.get('published_at') or '')[:10],'avail':any(v.get('available') for v in x['variants']),'img':(x['images'][0]['src'] if x['images'] else ''),'url':f'https://{h}/products/{x["handle"]}','tags':x.get('tags',[])})
      if len(L)<250: break
  sets.sort(key=lambda s:s['pub'],reverse=True)
  out[b]={'stage':stage,'hosts':hosts,'readable':ok,'sets':sets}
  print(f"{len(sets):3d} {'?' if ok is False else ' '} {b} {hosts}",flush=True)
json.dump(out,open('/tmp/claude-0/plan2/sets.json','w'))
