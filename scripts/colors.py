import json,hashlib,re,colorsys
from PIL import Image
import numpy as np
FAM=['pink','red','orange','yellow','green','teal','blue','purple','neutral','black']
WORDS={'pink':r'pink|blush|rose\b|rosé|coral|fuchsia|magenta|peony','red':r'\bred\b|cherry|crimson|scarlet|burgundy|oxblood','orange':r'orange|tangerine|terracotta|rust|apricot|peach','yellow':r'yellow|lemon|sunshine|butter|gold\b|mustard|limoncello','green':r'green|jade|emerald|sage|olive|malachite|mint|kelly|forest|palm|fern','teal':r'teal|aqua|turquoise|seafoam|lagoon','blue':r'blue|navy|cobalt|denim|periwinkle|indigo|chambray','purple':r'purple|lilac|lavender|violet|plum|orchid|amethyst','neutral':r'tortoise|ivory|cream|white|pearl|natural|wood|walnut|rattan|cane|tan\b|beige|taupe|brown|cognac|grey|gray|clear|neutral|oat','black':r'\bblack\b|onyx|noir|ebony'}
def fam(h,s,v):
    if v<0.16: return 'black'
    if s<0.16 or (v>0.9 and s<0.22): return 'neutral'
    d=h*360
    if (15<=d<50) and (s<0.5 and v<0.75): return 'neutral'
    if d<12 or d>=345: return 'red' if s>0.55 and v<0.85 else 'pink'
    if d<40: return 'orange'
    if d<68: return 'yellow'
    if d<160: return 'green'
    if d<195: return 'teal'
    if d<255: return 'blue'
    if d<290: return 'purple'
    return 'pink'
def analyze(path):
    im=Image.open(path).convert('RGB').resize((48,48))
    a=np.asarray(im).reshape(-1,3)/255.0
    cnt={f:0 for f in FAM}; white=0
    for r,g,b in a:
        h,s,v=colorsys.rgb_to_hsv(r,g,b)
        if v>0.93 and s<0.08: white+=1; continue
        cnt[fam(h,s,v)]+=1
    tot=sum(cnt.values())
    if tot<0.12*len(a): return {'neutral':1.0}
    return {k:v/tot for k,v in cnt.items() if v}
it=json.load(open('items.json'))
for i in it:
    sh={}
    if i['i']:
        p='thumbs/'+hashlib.md5(i['i'].encode()).hexdigest()[:16]+'.jpg'
        try: sh=analyze(p)
        except Exception: sh={}
    t=i['t'].lower()
    named=[f for f,w in WORDS.items() if re.search(w,t)]
    if named:
        prim=named[0] if len(named)==1 else max(named,key=lambda f:sh.get(f,0))
    else:
        cand=sorted(sh.items(),key=lambda x:-x[1])
        # neutral background often dominates mats/tiles photos; prefer a chromatic family if it has >=22%
        chrom=[c for c in cand if c[0] not in('neutral','black') and c[1]>=0.22]
        prim=chrom[0][0] if chrom else (cand[0][0] if cand else 'neutral')
    cols=sorted({prim,*[f for f in named],*[f for f,v in sh.items() if v>=0.2]})
    multi=len([f for f,v in sh.items() if v>=0.15 and f not in('neutral',)])>=3
    i['c']=prim; i['cs']=cols; i['multi']=multi
json.dump(it,open('items-colored.json','w'))
from collections import Counter
print(Counter(i['c'] for i in it)); print(sum(i['multi'] for i in it),'multi')
for i in it[:0]: pass
