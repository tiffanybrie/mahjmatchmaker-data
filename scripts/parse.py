import re, json, html, glob, os
from html.parser import HTMLParser
def txt(s): return html.unescape(re.sub(r'<[^>]+>','',s)).strip()
albums=[]
for f in sorted(glob.glob('albums/*.html')):
    h=open(f).read()
    slug=os.path.basename(f)[:-5]
    i=h.find('class="mm3"');
    if i<0: print('NO mm3',slug); continue
    body=h[i:]
    kicker=txt(re.search(r'class="mm3-kicker">(.*?)</p>',body).group(1)) if 'mm3-kicker' in body else ''
    h1=txt(re.search(r'<h1>(.*?)</h1>',body).group(1))
    tile=re.sub(r'\s*Mahjong Tile Matches$','',h1)
    cover=re.search(r'mm3-hero-img"><img src="([^"]+)"',body)
    cta=re.search(r'class="mm3-cta"><a class="mm3-btn[^"]*" href="([^"]+)"[^>]*>(.*?)</a>',body)
    cards=[]
    for m in re.finditer(r'<figure class="mm3-c">(.*?)</figure>',body,re.S):
        c=m.group(1)
        g=lambda p: (re.search(p,c,re.S).group(1) if re.search(p,c,re.S) else '')
        img=g(r'<img src="([^"]+)"')
        title=txt(g(r'<h3>(.*?)</h3>'))
        by=txt(g(r'class="mm3-by">(.*?)</span>'))
        by=re.sub(r'Retired$','',by).strip()
        brand=re.sub(r'^Mat by\s*','',by)
        mat=title.split(' + ',1)[1] if ' + ' in title else title
        take=txt(g(r'class="mm3-take">(.*?)</div>'))
        retired='mm3-ret"' in c
        l=g(r'class="mm3-l">(.*?)</div>')
        shop=re.search(r'href="([^"]+)"[^>]*>(.*?)</a>',l)
        code=txt(g(r'class="mm3-code"[^>]*>(.*?)</(?:p|div|span)>'))
        racks=[(html.unescape(a),txt(b)) for a,b in re.findall(r'<a href="([^"]+)"[^>]*>(.*?)</a>',g(r'class="mm3-rk"[^>]*>(.*?)</div>'))]
        cards.append(dict(n=txt(g(r'class="mm3-n">(.*?)</span>')),img=img.split('?')[0],mat=mat,brand=brand,take=take,retired=retired,
            shop=html.unescape(shop.group(1)) if shop else '',shopLabel=txt(shop.group(2)) if shop else '',code=code,racks=racks))
    albums.append(dict(slug=slug,tile=tile,maker=kicker,cover=cover.group(1).split('?')[0] if cover else '',tileShop=html.unescape(cta.group(1)) if cta else '',cards=cards))
json.dump(albums,open('albums.json','w'),indent=0)
print(len(albums), sum(len(a['cards']) for a in albums))
mats={}
for a in albums:
    for c in a['cards']:
        k=(c['mat'].lower(),c['brand'].lower()); mats.setdefault(k,[]).append(a['tile'])
print('unique mats',len(mats)); multi=sorted(mats.items(),key=lambda x:-len(x[1]))[:10]
for k,v in multi: print(k,len(v))
print(albums[0]['tile'],albums[0]['maker'],albums[0]['cards'][0])
