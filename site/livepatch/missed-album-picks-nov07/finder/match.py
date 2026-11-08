import re,html,unicodedata
def nz(x):
    x=''.join(c for c in unicodedata.normalize('NFD',html.unescape(str(x or ''))) if not unicodedata.combining(c)).lower()
    return re.sub(r'[^a-z0-9]','',x.replace('&','and').replace('+','and'))
STOP={'mat','mahjong','mahj','neoprene','leatherette','vegan','leather','premium','the','a','and','of','in','with','x','side','double','sided','game','surface','table','full','size','mats'}
def toks(s):
    s=''.join(c for c in unicodedata.normalize('NFD',html.unescape(str(s or ''))) if not unicodedata.combining(c)).lower().replace('&',' and ')
    return {t for t in re.findall(r'[a-z0-9]+',s) if t not in STOP}
def cards(h):
    out=[]
    for f in re.findall(r'<figure class="mm3-c[ "][\s\S]*?</figure>',h):
        t=html.unescape((re.search(r'<h3>(.*?)</h3>',f,re.S) or [None,''])[1]); t=re.sub(r'<[^>]+>','',t)
        name=t.split(' + ',1)[1] if ' + ' in t else t
        by=re.search(r'<span class="mm3-by">Mat by (?:<a[^>]*>)?([^<]+)',f); by=html.unescape(by.group(1)).strip() if by else ''
        alt=html.unescape((re.search(r'alt="([^"]*)"',f) or [None,''])[1]); src=(re.search(r'src="([^"]+)"',f) or [None,''])[1]
        out.append({'name':name,'by':by,'alt':alt,'src':src,'title':t,'hc':'mm3-hc' in f[:40]})
    return out
def brand_eq(a,b):
    a,b=nz(a),nz(b)
    if not a or not b: return False
    return a==b or a in b or b in a or a[:8]==b[:8]
def on_page(mat,brand,cs):
    mt=toks(re.sub(r'^.*?:\s*','',mat) if ':' in mat else mat)|toks(mat)
    mn=nz(mat)
    for c in cs:
        ct=toks(c['name'])
        if not ct: continue
        bok=brand_eq(c['by'],brand) or (nz(brand) and nz(brand) in nz(c['alt']+c['src']))
        sub=lambda A,B: all((t in B) if len(t)>1 else any(b.startswith(t) for b in B-A) for t in A)
        nameok=sub(ct,mt) or (toks(mat) and sub(toks(mat),ct)) or nz(c['name'])==mn
        if nameok and bok: return c['title']
        if nameok and not c['by'] and not brand: return c['title']
    return None
