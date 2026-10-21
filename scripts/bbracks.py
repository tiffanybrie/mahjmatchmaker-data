# Bird & Bamboo rack colors from Tiffany's own color guide page (real swatch colors, grouped by family)
import re,json,html,subprocess
h=subprocess.run(['curl','-sS','-m','30','https://www.mahjmatchmaker.com/bird-and-bamboo-rack-colors'],capture_output=True,text=True).stdout
FAMMAP={'pinks':'pink','purples':'purple','reds':'red','yellows':'yellow','greens':'green','blues':'blue','neutrals':'neutral','stains':'neutral','metallics':'neutral'}
out=[];seen=set();sec=None
for m in re.finditer(r'<h2 id="([^"]+)"|<div class="sw">(.*?)</a></div>',h,re.S):
    if m.group(1): sec=m.group(1); continue
    b=m.group(2)
    hx=re.search(r'--c:(#[0-9A-Fa-f]{6})',b); nm=re.search(r'class="nm">(.*?)</p>',b); sh=re.search(r'class="shop" href="([^"]+)"',b)
    if not(hx and nm and sh) or sec=='most-used': continue
    name=html.unescape(re.sub('<[^>]+>','',nm.group(1))).strip()
    if name in seen: continue
    seen.add(name)
    fam=FAMMAP.get(sec,'neutral')
    if sec=='yellows':
        r,g,bb=(int(hx.group(1)[i:i+2],16) for i in (1,3,5))
        import colorsys; hh=colorsys.rgb_to_hsv(r/255,g/255,bb/255)[0]*360
        fam='orange' if hh<40 or hh>340 else 'yellow'
    if sec=='pinks':
        r,g,bb=(int(hx.group(1)[i:i+2],16) for i in (1,3,5))
        import colorsys; hh,ss,vv=colorsys.rgb_to_hsv(r/255,g/255,bb/255); hh*=360
        if 255<=hh<300: fam='purple'
    if sec=='greens':
        r,g,bb=(int(hx.group(1)[i:i+2],16) for i in (1,3,5))
        import colorsys; hh=colorsys.rgb_to_hsv(r/255,g/255,bb/255)[0]*360
        if 160<=hh<200: fam='teal'
    seen_in=re.sub('<[^>]+>','',(re.search(r'class="seen">(.*?)</p>',b) or [None,''])[1]) if re.search(r'class="seen">(.*?)</p>',b) else ''
    out.append(dict(name=name,hex=hx.group(1).upper(),fam=fam,url=html.unescape(sh.group(1)),seen=html.unescape(seen_in).strip()))
json.dump(out,open('bbracks.json','w'),indent=0)
print(len(out),'Bird & Bamboo rack colors')
