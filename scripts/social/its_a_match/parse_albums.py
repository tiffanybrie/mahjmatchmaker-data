import re, json, html, glob, os, sys
D=sys.argv[1]
def txt(s): return html.unescape(re.sub(r'<[^>]+>','',s)).strip()
out=[]
for f in sorted(glob.glob(D+'/albums/*.html')):
    h=open(f).read(); slug=os.path.basename(f)[:-5].replace('-mahjong-tile-matches','')
    kick=re.search(r'class="mm3-kicker">(.*?)</p>',h)
    h1=re.search(r'<h1>(.*?)</h1>',h)
    cards=[]
    for m in re.finditer(r'<figure class="mm3-c">(.*?)</figure>',h,re.S):
        c=m.group(1); g=lambda p:(re.search(p,c,re.S).group(1) if re.search(p,c,re.S) else '')
        title=txt(g(r'<h3>(.*?)</h3>')); by=re.sub(r'Retired$','',txt(g(r'class="mm3-by">(.*?)</span>'))).strip()
        cards.append(dict(n=txt(g(r'class="mm3-n">(.*?)</span>')),img=g(r'<img src="([^"]+)"').split('?')[0],
          mat=title.split(' + ',1)[1] if ' + ' in title else title,brand=re.sub(r'^Mat by\s*','',by),
          retired=('mm3-ret"' in c), take=txt(g(r'class="mm3-take">(.*?)</div>')), alt=g(r'alt="([^"]*)"')))
    text=txt(re.sub(r'<(script|style).*?</\1>','',h,flags=re.S))
    out.append(dict(slug=slug,tile=re.sub(r'\s*Mahjong Tile Matches$','',txt(h1.group(1))) if h1 else slug,maker=txt(kick.group(1)) if kick else '',
       n=len(cards),cards=cards,he=len(re.findall(r'\b(he|him|his|himself)\b',text,re.I)),she=len(re.findall(r'\b(she|her|hers|herself)\b',text,re.I))))
json.dump(out,open(D+'/albums_live.json','w'),indent=1)
for a in out: print(a['slug'],'|',a['tile'],'|',a['maker'],'|',a['n'],'he',a['he'],'she',a['she'])
