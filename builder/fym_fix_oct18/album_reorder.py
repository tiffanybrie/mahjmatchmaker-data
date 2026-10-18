import json,re,os,sys,html
S='/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/'
pairs={'c5-brownstone':'brownstone-bloom','c5-v-lilac-soiree':'lilac-soiree','c5-v-preppy-soiree':'preppy-soiree','c5-v-shangri-la':'shangri-la','c5-sunday':'sunday-tile-set'}
REMOVE={'brownstone-bloom':['tigre-de-tartan-el-tigre-mat']}
norm=lambda f: re.sub(r'-v\d+(?=\.jpg)','',os.path.basename(f))
dry='--dry' in sys.argv
for doc,cb in pairs.items():
    j=json.load(open(S+'shipdb/ship/'+doc+'.json'))
    order=[norm(x) for x in j.get('order',[]) if 'cover' not in x]
    p=S+'sunday_live/'+cb+'_codeblock.html'; s=open(p).read()
    # main grid = first mm3-grid
    gm=re.search(r'(<section><h2>My [^<]* matches</h2>.*?<div class="mm3-grid">)(.*?)(</div></section>)',s,re.S)
    head,grid,tail=gm.group(1),gm.group(2),gm.group(3)
    figs=re.findall(r'<figure class="mm3-c">.*?</figure>',grid,re.S)
    assert ''.join(figs)==grid, (cb,'grid has extra content')
    key=lambda f: norm(re.search(r'<img src="([^"]+)"',f).group(1))
    rm=REMOVE.get(cb,[])
    kept=[f for f in figs if not any(r in key(f) for r in rm)]
    removed=len(figs)-len(kept)
    pos={k:i for i,k in enumerate(order)}
    new=sorted(kept,key=lambda f:(pos.get(key(f),10_000), figs.index(f)))
    changed=[key(f) for f in new]!=[key(f) for f in figs]
    # renumber
    out=[]
    for i,f in enumerate(new,1):
        f=re.sub(r'<span class="mm3-n">\d+</span>',f'<span class="mm3-n">{i}</span>',f,1); out.append(f)
    s2=s[:gm.start()]+head+''.join(out)+tail+s[gm.end():]
    # FAQ top3 + count
    def t3(f):
        h=html.unescape(re.search(r'<h3>(.*?)</h3>',f).group(1)); mat=h.split(' + ',1)[1] if ' + ' in h else h
        by=re.search(r'class="mm3-by">Mat by (?:<a[^>]*>)?([^<]+)',f); return f'{mat} by {html.unescape(by.group(1)) if by else ""}'.strip()
    top=[t3(f) for f in new[:3]]
    s2,n1=re.subn(r'My top mat picks for ([^<]*?) are .*? and .*?\. Below are (\d+) ',lambda m:f'My top mat picks for {m.group(1)} are {html.escape(", ".join(top[:-1]))} and {html.escape(top[-1])}. Below are {len(new)} ',s2,count=1)
    s2,n2=re.subn(r'("text": ?"My top mat picks for [^"]*? are )[^"]*(")',lambda m:m.group(1)+json.dumps(', '.join(top[:-1])+' and '+top[-1]+'.')[1:-1]+m.group(2),s2,count=1)
    print(cb, 'figs',len(figs),'removed',removed,'reordered' if changed else 'order unchanged','faq',n1,n2,'| top3:',top)
    missing=[k for k in order if k not in [key(f) for f in figs]]
    if missing: print('   saved but not in main grid:',missing)
    if not dry and (changed or removed): open(p,'w').write(s2)
