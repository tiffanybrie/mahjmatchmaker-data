import json,re,html
L=json.load(open('config/brand-candidates-oct31.json'))['brands']
def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
def n(b):
    m=re.match(r'(\d+)',b.get('catalog_size_est') or ''); return int(m.group(1)) if m else -1
data=[]
for b in L:
    if 'whole line' in (b.get('in_app_now') or ''): continue  # already fully in the app (Sunday, Ozark, House of Hearts)
    data.append(dict(id=slug(b['name']),name=b['name'],site=b.get('site'),sells=b.get('sells'),size=b.get('catalog_size_est'),
      tnt=b.get('tnt_rec_count') or 0,bucket=b['status_bucket'],applied=b.get('applied'),program=b.get('program'),
      calls=b.get('past_tiffany_calls') or [],rec=b.get('recommendation'),why=b.get('why'),img=b.get('image'),inapp=b.get('in_app_now'),n=n(b)))
data.sort(key=lambda d:(-d['tnt'],-d['n'],d['name']))
tpl=open('site/livepatch/brand-candidates-oct31/page.tpl.html').read()
open('site/livepatch/brand-candidates-oct31/index.html','w').write(tpl.replace('__DATA__',json.dumps(data,ensure_ascii=False).replace('</','<\\/')))
print(len(data))
