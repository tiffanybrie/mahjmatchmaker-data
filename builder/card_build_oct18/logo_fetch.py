"""Try to fetch a larger header logo from each brand's own site (Shopify themes expose it as an <img> in the header)."""
import re,urllib.request,io,json,os,sys
from PIL import Image
UA={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124 Safari/537.36'}
SITES={'Bam Bird Boutique':'https://www.bambirdboutique.com','Hip Hip Mahjong':'https://www.hiphipmahjong.com','Amahj':'https://amahjline.com',
'Mahj & Vine':'https://mahjandvine.com','Mac + Miller Mahjong':'https://www.macandmillermahjong.com','My Fair Mahjong':'https://myfairmahjong.com',
'Splash of Color':'https://splashofcolormahjong.com','Yellow Mountain Imports':'https://www.ymimports.com','Tigre de Tartan':'https://tigredetartan.com',
'Oh My Mahjong':'https://www.ohmymahjong.com','Peace Love Mahjong':'https://peacelovemahjong.com','Miss Mahjong':'https://missmahjong.com',
'Ozark Mah Jongg':'https://ozarkmahjongg.com','Mahjong Register':'https://mahjongregister.com','Mahj & Moon':'https://mahjandmoon.com','Wren Mats':'https://www.wrenmats.com',
'Royal Mahjong Society':'https://theroyalmahjongsociety.com','Mahjong by SI':'https://mahjongbysi.com','Rebecca Illustrated':'https://rebeccaillustrated.com','Maison Mahj':'https://maisonmahj.com'}
OUT='/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/hd_logos/fetched';os.makedirs(OUT,exist_ok=True)
res={}
for b,u in SITES.items():
    try:h=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=20).read().decode('utf8','ignore')
    except Exception as e:res[b]='ERR '+str(e)[:60];continue
    hd=h[:h.find('</header>')] if '</header>' in h else h[:80000]
    c=re.findall(r'<img[^>]+>',hd)
    pick=None
    for t in c:
        if re.search(r'logo',t,re.I):
            m=re.search(r'(?:srcset|src)="([^"]+)"',t)
            if m:pick=m.group(1).split(',')[-1].strip().split(' ')[0];break
    if not pick:res[b]='no logo img';continue
    if pick.startswith('//'):pick='https:'+pick
    if pick.startswith('/'):pick=u+pick
    pick=re.sub(r'([?&])width=\d+','\\1width=1200',pick)
    if 'cdn.shopify' in pick and 'width=' not in pick:pick+=('&' if '?' in pick else '?')+'width=1200'
    try:
        d=urllib.request.urlopen(urllib.request.Request(pick,headers=UA),timeout=20).read()
        if pick.split('?')[0].endswith('.svg'):fn=re.sub(r'\W','',b)+'.svg';open(os.path.join(OUT,fn),'wb').write(d);res[b]=('svg',fn,pick);continue
        im=Image.open(io.BytesIO(d));fn=re.sub(r'\W','',b)+'.png';im.convert('RGBA').save(os.path.join(OUT,fn));res[b]=(im.size,fn,pick[:120])
    except Exception as e:res[b]='ERR img '+str(e)[:60]
json.dump(res,open(OUT+'/report.json','w'),indent=1)
for k,v in res.items():print(k,v)
