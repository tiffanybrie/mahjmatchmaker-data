import json,re,html,unicodedata,collections
R='/home/claude/mahjmatchmaker-data/'
D=json.load(open('D117.json')); M=D['mats']; D8=json.load(open('D118.json')); M8=D8['mats']
def nz(x):
    x=''.join(c for c in unicodedata.normalize('NFD',html.unescape(str(x or ''))) if not unicodedata.combining(c)).lower()
    return re.sub(r'[^a-z0-9]','',x.replace('&','and').replace('+','and'))
def visible(h):
    h=re.sub(r'<!--.*?-->',' ',h,flags=re.S); h=re.sub(r'<(script|style)[^>]*>.*?</\1>',' ',h,flags=re.S|re.I)
    alts=' '.join(re.findall(r'\balt="([^"]*)"',h)); return html.unescape(re.sub(r'<[^>]+>',' ',h)+' '+alts)
def cands(n):
    c={nz(n),nz(re.sub(r'\s*\(.*?\)','',n)),nz(re.sub(r'\b(mahjong|mahj|mat|neoprene|leatherette|vegan leather)\b','',n,flags=re.I))}
    return {x for x in c if len(x)>=4}
SITE='https://www.mahjmatchmaker.com'
EXTRA={'December 1994':SITE+'/holiday-mahjong-matches#december-1994','Sunday':SITE+'/sunday-tile-set-mahjong-tile-matches',
       'Papaya Spritz':SITE+'/papaya-spritz-mahjong-tile-matches'}
NOTLIVE={'Hummingbird':'album drafted (site/livepatch/sunday-albums-nov06), not live yet; holiday section #hummingbird hidden',
         'Spirit of Christmas':'PLM Spirit of Christmas has no holiday-page section or album yet',
         'Cypress':'Mahjong Row is out of the site (Nov 6)'}
pages={}
HSID={'Dear Santa':'dear-santa',"Rackin' Rudolph":'rackin-rudolph','Holly Jolly (Rudolph Red)':'holly-jolly-red','Holly Jolly (Grinch Green)':'holly-jolly-green',
 'Holly Jolly (Sugarplum Pink)':'holly-jolly-pink','Nivalee (Glacier Blue)':'nivalee-blue','Tinselle (Emerald Green)':'tinselle-emerald','Tinselle (Ruby Red)':'tinselle-ruby',
 'Nutcracker Ballet':'nutcracker-ballet','Après Ski Club':'cmc-apres-ski'}
def page(u):
    p=u.replace(SITE,'').split('#')[0].strip('/')
    if p not in pages: pages[p]=open(f'live/{p}.html').read()
    return pages[p]
def section(h,u):
    if '#' in u and 'holiday-mahjong-matches' in u:
        sid=u.split('#')[1]; i=h.find(f'id="{sid}"'); j=h.find('<section class="mm3-hol"',i+10)
        return h[i:j if j>0 else len(h)]
    return h
def blobs(u):
    h=section(page(u),u)
    figs=re.findall(r'<figure class="mm3-c[ "][\s\S]*?</figure>',h)
    return nz(' '.join(visible(f)+' '+' '.join(re.findall(r'src="([^"]+)"',f)) for f in figs)), nz(visible(h))
pairs={}  # (album_url, key) -> rec
unmap=[]
for s in D['sets']:
    if not s['m']: continue
    if s['name'] in NOTLIVE:
        unmap.append({'set':s['name'],'n':len(s['m']),'why':NOTLIVE[s['name']]}); continue
    u=s.get('album') or EXTRA.get(s['name'])
    if u.rstrip('/').endswith('/holiday-mahjong-matches') or ('holiday-mahjong-matches' in u and '#' not in u): u=SITE+'/holiday-mahjong-matches#'+HSID[s['name']]
    cb,pb=blobs(u)
    for k,r in s['m']:
        mt=M.get(k) or M8.get(k) or {}; n=mt.get('n',k)
        if any(x in cb for x in cands(n)): continue
        pairs[(u,k)]={'set':s['name'],'slug':s['slug'],'album':u,'key':k,'mat':n,'brand':mt.get('bn'),'hol':bool(mt.get('hol')),'ayr':bool(mt.get('ayr')),
                      'fym_racks':r,'src':['fym117'],'page_text_mentions':any(x in pb for x in cands(n)),'mat_hidden_fym':bool(mt.get('hid'))}
# round 1
AUD=json.load(open(R+'docs/audits/album-missed-mats-2026-11-07.json'))['albums']
BYNAME={nz(v['name']):k for k,v in AUD.items()}
def split_pairs(t):
    out,depth,cur=[],0,''
    for ch in t:
        depth+=ch=='('; depth-=ch==')'
        if ch==',' and depth==0: out.append(cur.strip()); cur=''
        else: cur+=ch
    if cur.strip(): out.append(cur.strip())
    res=[]
    for it in out:
        m=re.match(r'^(.*)\(([^()]*)\)\s*$',it); res.append((m.group(1).strip(),m.group(2).strip()) if m else (it,''))
    return res
NB={}
for k,o in M8.items(): NB.setdefault((nz(o['n']),nz(o.get('bn'))),[]).append(k)
r1=0
for line in open(R+'config/picks/missed-mats-round1-2026-11-07.txt'):
    if ':' not in line or line.startswith('My yeses'): continue
    alb,rest=line.split(':',1); alb=alb.strip(); hl=alb.endswith('(holiday)'); base=re.sub(r'\s*\(holiday\)\s*$','',alb)
    aslug=BYNAME.get(nz(base))
    if not aslug: unmap.append({'set':alb,'why':'album not in audit'}); continue
    u=SITE+f'/{aslug}-mahjong-tile-matches'
    if aslug.replace('-mahjong-tile-matches','') and not __import__('os').path.exists(f'live/{aslug}-mahjong-tile-matches.html'):
        import urllib.request; open(f'live/{aslug}-mahjong-tile-matches.html','w').write(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'})).read().decode())
    cb,pb=blobs(u)
    for mat,brand in split_pairs(rest.strip()):
        r1+=1
        cand=[x['key'] for x in AUD[aslug].get('strong',[])+AUD[aslug].get('holiday',[]) if nz(x['name'])==nz(mat) and nz(x['brand'])==nz(brand)]
        if not cand: cand=NB.get((nz(mat),nz(brand)),[])
        if not cand: cand=[k for (n_,b_),ks in NB.items() if n_==nz(mat) for k in ks]
        cand=list(dict.fromkeys(cand))
        if len(cand)!=1: unmap.append({'set':alb,'mat':mat,'brand':brand,'why':f'mat key not unique: {cand}'}); continue
        k=cand[0]; mt=M8.get(k,{})
        if any(x in cb for x in cands(mat)): continue
        if (u,k) in pairs: pairs[(u,k)]['src'].append('round1'); continue
        sset=next((s for s in D['sets'] if (s.get('album') or EXTRA.get(s['name'],'')).split('#')[0]==u),None)
        pairs[(u,k)]={'set':sset['name'] if sset else base,'slug':sset['slug'] if sset else aslug,'album':u,'key':k,'mat':mat,'brand':brand,
                      'hol':bool(mt.get('hol')) or hl,'ayr':bool(mt.get('ayr')),'fym_racks':[],'src':['round1'],'holiday_line':hl,
                      'page_text_mentions':any(x in pb for x in cands(mat)),'mat_hidden_fym':bool(mt.get('hid'))}
out=sorted(pairs.values(),key=lambda x:(x['album'],x['hol'],x['mat']))
json.dump({'pairs':out,'not_mappable':unmap},open('missing_all.json','w'),indent=1,ensure_ascii=False)
print('round1 pairs read',r1,'| total missing',len(out),'| holiday',sum(o['hol'] for o in out))
c=collections.Counter(o['album'].replace(SITE,'') for o in out); print(c.most_common(50))
c=collections.Counter(o['mat'] for o in out); print(c.most_common(20))
print('hidden-in-fym mats',sum(o['mat_hidden_fym'] for o in out))
for x in unmap: print('UNMAP',x)
