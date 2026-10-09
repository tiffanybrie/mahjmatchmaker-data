import json,glob,re,os
from collections import Counter
def kind(p):
    t=(p['title']+' '+p.get('product_type','')+' '+' '.join(p.get('tags',[]) if isinstance(p.get('tags'),list) else [p.get('tags','')])).lower()
    ti=p['title'].lower()
    if re.search(r'gift card|sample|swatch|bag|tote|pouch|case|card holder|scorecard|score card|shirt|tee|hat|sweatshirt|candle|napkin|coaster|sticker|pin\b|earring|necklace|bracelet|book|lesson|class|cup|tumbler|dice|charm|ornament|print\b|poster|towel|apron|socks|keychain|mug|glass|playing cards|card\b.*2026|2026.*card|tablecloth|runner|bundle|subscription|insurance|shipping',ti):
        if not re.search(r'\bmat\b|tiles?\b|rack',ti): return 'other'
        if re.search(r'rack bag|tile bag|mat bag|bag for|carrying|storage|case|tote|pouch|sample|swatch|scorecard|insurance',ti): return 'other'
    pt0=p.get('product_type','').lower()
    if re.search(r'lamp|placemat|place mat|coaster|charger|table runner|napkin|table\b.*set of|coffee table|side table|cabinet|chest|t-shirt|mug|home decor|pillow|blanket|wall art|stool|chair|puzzle|jewelry',ti+' '+pt0): return 'other'
    if re.search(r'\bmat\b',ti) and not re.search(r'rack (set|and|&)|racks? (with|&|and) pushers',ti): return 'mat'
    if re.search(r'\brack|pusher',ti): return 'rack'
    if re.search(r'\bmat\b|\bmats\b|table cover|playmat|play mat|tablecloth topper',ti): return 'mat'
    if re.search(r'tile set|tiles|mahjong set|mah jongg set|mahjong tile|travel set|\bset\b.*mahj',ti): return 'tiles'
    pt=p.get('product_type','').lower()
    if 'mat' in pt: return 'mat'
    if 'rack' in pt: return 'rack'
    if 'tile' in pt: return 'tiles'
    return 'other'
tot=Counter();per={}
for f in sorted(glob.glob('raw/*.json')):
    ps=json.load(open(f)); c=Counter(kind(p) for p in ps); per[os.path.basename(f)[:-5]]=c; tot+=c
    print(os.path.basename(f)[:-5], dict(c))
print(tot)
