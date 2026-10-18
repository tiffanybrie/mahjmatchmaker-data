import json,re,glob,os,html
R='/home/claude/mahjmatchmaker-data/'
S='/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/'
e=lambda s: html.escape(s,quote=True)
man={}
for c in json.load(open(R+'scripts/albumcard/holiday_manifest.json')):
    man[c['file']]=c; man[c['file'].replace('.jpg','-hd.jpg')]=c
def nm(k):
    if k.startswith('bb:'): return 'Bird & Bamboo '+k[3:]
    if k.startswith('plm:'): return 'Peace Love Mahjong '+k[4:]
    if '/' in k and ' ' not in k:  # handle-style key
        if 'golden-grain' in k: return 'Middle & Main Golden Grain Beechwood'
    return k
# url map
U={}
for n,u in json.load(open(R+'data.json'))['R']: U[n]=u
for n,u in json.load(open(S+'rkcap/fymracks.json')).items(): U.setdefault(n,u)
for f in glob.glob(R+'site/livepatch/codefooter/*.html')+glob.glob(S+'codefooter/html/*.html'):
    for u,n in re.findall(r'<a href="([^"]+)"[^>]*>([^<]+)</a>',open(f).read()):
        n=html.unescape(n).strip()
        if n.startswith(('Bird & Bamboo','Peace Love','Middle & Main','Miss Mahjong','Mahjong Row','Sunday','Bam Bird','Tigre','Oh My','My Fair','Hip Hip')):
            U.setdefault(n,html.unescape(u))
MAN={'Middle & Main Hawksbill Heritage Tortoise':'https://www.middleandmainmahjong.com/products/hawksbill-heritage-mahjong-rack-and-pusher-set-of-4?sca_ref=10574197.BKiJ48vXYfYfD31E',
 'Middle & Main Milk Glass Scalloped Acrylic':'https://www.middleandmainmahjong.com/products/milk-glass-collection-mahjong-rack-and-pusher-set-of-4?sca_ref=10574197.BKiJ48vXYfYfD31E',
 'Middle & Main White Lace Acrylic':U.get('Middle & Main White Lace'),
 'Miss Mahjong Blonde Tortoise & Brass':'https://missmahjong.com/products/blonde-tortoise-and-brass-acrylic-racks?ref=mahjmatch',
 'Miss Mahjong Brass & Tortoise':'https://missmahjong.com/products/dark-tortoise-and-brass-acrylic-racks?ref=mahjmatch',
 'Sunday Mahjong Cola':'https://sundaymahjong.com/products/sunday-cola-mahjong-rack-set',
 'Middle & Main Golden Grain Beechwood':'https://www.middleandmainmahjong.com/products/golden-grain-beechwood-mahjong-rack-and-pusher-set-of-4?sca_ref=10574197.BKiJ48vXYfYfD31E'}
U.update({k:v for k,v in MAN.items() if v})
BB=next(u for n,u in U.items() if n.startswith('Bird & Bamboo'))
BBBASE=re.sub(r'variant=\d+&?','',BB).replace('?&','?')
missing=set(); skipped=[]
def link(k):
    n=nm(k); u=U.get(n)
    if not u and n.startswith('Bird & Bamboo'): u=BBBASE
    if not u: missing.add(n); return e(n)
    return f'<a href="{e(u)}" target="_blank" rel="sponsored noopener">{e(n)}</a>'
def newdiv(c):
    NOPHOTO={'Tigre de Tartán Oxblood Scallop'}  # not printed on cards (no product photo)
    t=' · '.join(link(k) for k in c['racks'] if k not in NOPHOTO); m=' · '.join(link(k) for k in c.get('mat_picks',[]))
    s='Match the tiles: '+t
    if m: s+='<br>Match the mat: '+m
    return f'<div class="mm3-rk" style="margin-top:8px;font-size:.82em;line-height:1.55">{s}</div>'
FIG=re.compile(r'<figure class="mm3-c[^"]*">.*?</figure>',re.S)
RK=re.compile(r'<div class="mm3-rk"[^>]*>Rack matches:.*?</div>',re.S)
def process(h):
    swaps=[]; 
    def fx(m):
        F=m.group(0); r=RK.search(F)
        if not r: return F
        src=re.search(r'<img src="([^"]+)"',F).group(1)
        b=os.path.basename(src).split('?')[0]
        if not re.search(r'/assets/cards/(codefooter-v1/cards/)?(holiday-v4|polofix-v1)/',src): skipped.append(src); return F
        c=man.get(b)
        if not c: return F
        nd=newdiv(c)
        if r.group(0)==nd: return F
        i=F.index('<img src='); j=r.end()
        seg=F[i:j]; nseg=seg[:-len(r.group(0))]+nd
        swaps.append({'img':src,'title':c['title'],'old':seg,'new':nseg})
        return F.replace(r.group(0),nd)
    return FIG.sub(fx,h),swaps
if __name__=='__main__':
    out={}
    os.makedirs(R+'site/livepatch/rackcaptions',exist_ok=True)
    # 1) the 14 codefooter blocks: fix in place
    for f in sorted(glob.glob(R+'site/livepatch/codefooter/*.html')):
        slug=os.path.basename(f)[:-5]; h=open(f).read(); h2,sw=process(h)
        if sw:
            open(f,'w').write(h2)
            j=json.load(open(f[:-5]+'.json')); j['caption_swaps']=[{'img':s['img'],'title':s['title'],'old':s['old'],'new':s['new']} for s in sw]; json.dump(j,open(f[:-5]+'.json','w'),indent=1)
        out[slug]={'n':len(sw),'in':'codefooter'}
    # 2) every other live page from the Oct 18 cache: caption-only swap lists
    for f in sorted(glob.glob(S+'codefooter/html/*.html')):
        slug=os.path.basename(f)[:-5]
        if slug in out: continue
        h2,sw=process(open(f).read())
        if sw:
            json.dump({'page':'/'+slug.replace('blog_','blog/'),'caption_swaps':[{'img':s['img'],'title':s['title'],'old':s['old'],'new':s['new']} for s in sw]},open(R+f'site/livepatch/rackcaptions/{slug}.json','w'),indent=1)
            out[slug]={'n':len(sw),'in':'rackcaptions'}
    json.dump(out,open(S+'rkcap/summary.json','w'),indent=1)
    for k,v in out.items():
        if v['n']: print(k,v)
    print('skipped non-v4',len(skipped),[os.path.basename(x)[:60] for x in skipped if man.get(os.path.basename(x).split('?')[0])]); print('total',sum(v['n'] for v in out.values()),'missing links',missing)
