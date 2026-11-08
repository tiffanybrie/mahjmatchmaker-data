import json,re,html,os,shutil,collections
OUTD='/home/claude/mahjmatchmaker-data/site/livepatch/missed-album-picks-nov07/'
SITE='https://www.mahjmatchmaker.com'
A=json.load(open('missing_final.json'))
D7=json.load(open('D117.json')); D8=json.load(open('D118.json')); M8=D8['mats']; M7=D7['mats']
MI=json.load(open('matimg.json'))
SETS={s['name']:s for s in D7['sets']}
def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower().replace('&','and').replace("'",'').replace('é','e').replace('á','a').replace('ó','o').replace('ú','u')).strip('-')
def page_key(u):
    p=u.replace(SITE,'').strip('/').split('#')
    return ('holiday#'+p[1]) if len(p)>1 else p[0].replace('-mahjong-tile-matches','')
heads={}
def tile_name(u):
    p=u.replace(SITE,'').split('#')[0].strip('/'); h=open(f'live/{p}.html').read()
    if '#' in u:
        sid=u.split('#')[1]; i=h.find(f'id="{sid}"'); m=re.search(r'<h2>(.*?) holiday matches</h2>',h[i:i+600])
        return re.sub(r'\s*\(.*?\)','',html.unescape(m.group(1))).strip() if m else sid
    m=re.search(r'<h2>(?:Every (.*?) match|My (.*?) matches)</h2>',h)
    return html.unescape(m.group(1) or m.group(2))
TB={'holiday#december-1994':'Sunday Mahjong','sunday-tile-set':'Sunday Mahjong','brownstone-bloom':'Anders Ruff','tortoise':'Bam Bird Boutique'}
def disp(n):
    n=re.sub(r'\s*\((retired)\)\s*','',n).strip()
    n=re.sub(r'\s+(Mat|Premium)$','',n).strip()
    n=re.sub(r'^Tigre de Tartán x Miss Mahjong:\s*','',n).strip().strip('“”"')
    return n
out=[]
seen=collections.Counter()
for p in A['pairs']:
    pk=page_key(p['album'])
    k=p['key']; m=M8.get(k) or M7.get(k) or {}
    s=SETS.get(p['set'])
    tbrand=TB.get(pk) or (s['maker'] if s else 'Oh My Mahjong')
    tn=tile_name(p['album'])
    sec='holiday' if (p['hol'] or pk.startswith('holiday#')) else 'main'
    mname=m.get('n',p['mat']); brand=m.get('bn') or p['brand']
    d=disp(mname)
    fn=f"{slug(pk.replace('holiday#',''))}-mahjong-tiles-{slug(brand)}-{slug(d)}-mat.jpg"
    ph=os.path.basename(MI[k]['file'])
    out.append({'page':pk,'album':p['album'],'section':sec,'tile_name':tn,'tile_brand':tbrand,'tc':(s or {}).get('tc'),
      'key':k,'mat':d,'mat_name':mname,'brand':brand,'url':m.get('u'),'dc':m.get('dc'),'code':bool(m.get('pa')) and not m.get('nc'),
      'retired':bool(m.get('rt')),'file':fn,'photo':ph,'src':p['src'],'flags':p.get('flags',[])})
    seen[fn]+=1
assert max(seen.values())==1,[k for k,v in seen.items() if v>1]
os.makedirs(OUTD+'matphotos',exist_ok=True)
from PIL import Image
for ph in {x['photo'] for x in out}:
    im=Image.open('matimg/'+ph); im.thumbnail((1300,1300)); im.save(OUTD+"matphotos/"+ph,quality=86)
json.dump(out,open(OUTD+'pairs.json','w'),indent=1,ensure_ascii=False)
json.dump({'not_mappable':A['not_mappable'],'dropped':A['dropped']},open(OUTD+'not_mappable.json','w'),indent=1,ensure_ascii=False)
print(len(out)); print(collections.Counter((x['page'],x['tile_name']) for x in out).most_common(80))
