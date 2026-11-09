import re, html, json
def figs(t, sid=None):
    out=[]
    for m in re.finditer(r'<figure class="(mm3-c[^"]*)">(.*?)</figure>', t, re.S):
        f=m.group(2)
        img=re.search(r'<img src="([^"]+)"',f).group(1)
        h3=html.unescape(re.sub('<[^>]+>','',re.search(r'<h3>(.*?)</h3>',f,re.S).group(1)))
        by=re.search(r'class="mm3-by">Mat by (.*?)</span>',f,re.S)
        brand=html.unescape(re.sub('<[^>]+>','',by.group(1))).replace('Retired','').strip() if by else ''
        shop=re.search(r'class="mm3-btn" href="([^"]+)"',f)
        rk=re.search(r'Match the tiles:(.*?)<br>\s*Match the mat:(.*?)</div>',f,re.S)
        sp=lambda s:[html.unescape(re.sub('<[^>]+>','',x)).strip() for x in s.split('·') if re.sub('<[^>]+>','',x).strip()]
        out.append({'cls':m.group(1),'hol':'mm3-hc' in m.group(1),'img':img,'h3':h3,'brand':brand,'shop':html.unescape(shop.group(1)) if shop else None,
                    'tile_racks':sp(rk.group(1)) if rk else [],'mat_racks':sp(rk.group(2)) if rk else [],'retired':'mm3-ret' in f,'html':m.group(0)})
    return out
def holiday_sections(t):
    ids=[(m.start(),m.group(1)) for m in re.finditer(r'<section class="mm3-hol" id="([a-z0-9-]+)"',t)]
    return {sid:figs(t[pos:t.find('</section>',pos)]) for pos,sid in ids}
