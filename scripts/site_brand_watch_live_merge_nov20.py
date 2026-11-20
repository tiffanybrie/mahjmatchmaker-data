import re,html,sys,datetime
blk=open('bw/live_block.html').read()
repo=open('/home/claude/mahjmatchmaker-data/site/livepatch/brand-watch/brand-watch.html').read()
ART=re.compile(r'<article class="bw-card">.*?</article>',re.S)
txt=lambda h:re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',h))).strip()
brand=lambda a:html.unescape(re.search(r'<div class="bw-brand">(.*?)<span',a,re.S).group(1)).strip()
MON={'Sun':0}
def newest(a):
    best=(0,0,0,0)
    for d,mo,da,t in re.findall(r'(?:Added|Earlier ·)?\s*(Mon|Tue|Wed|Thu|Fri|Sat|Sun) (\d+)/(\d+)(?: · (\d+:\d+[ap]m))?',' '.join(re.findall(r'<div class="bw-stamp">(.*?)</div>',a))):
        hh=0
        if t:
            h,m=t[:-2].split(':');h=int(h)%12+(12 if t.endswith('pm') else 0);hh=h*60+int(m)
        best=max(best,(int(mo),int(da),hh,0))
    return best
def parts(h):
    m=h.find('<section class="bw-bpage"'); e=h.find('<script',m); return h[:m],h[m:e],h[e:]
Lmain,Lbp,Ltail=parts(blk); Rmain,Rbp,_=parts(repo)
SECS=[('black-friday','Black Friday deals'),('coming-soon','Coming soon'),('just-dropped','Just dropped')]
def repo_sec(title):
    m=re.search(r'<section class="bw-sec"[^>]*><h2>'+re.escape(title)+r'</h2><div class="bw-grid">(.*?)</div>\s*(?:<a class="bw-top"[^>]*>.*?</a>)?</section>',Rmain,re.S); return ART.findall(m.group(1))
log=[]
def live_sec_span(h,sid):
    i=h.find('id="%s"'%sid); g=h.find('<div class="bw-grid">',i)+len('<div class="bw-grid">'); e=h.find('<a class="bw-top"',g); e2=h.rfind('</div>',g,e); return g,e2
def mk(b,stamp,what,when,href,btn,save):
    return ('<article class="bw-card"><div class="bw-body"><div class="bw-brand">%s<span class="bw-tag bw-t-black-friday-deals">Black Friday deals</span></div><div class="bw-item"><div class="bw-stamp">%s</div><div class="bw-what">%s</div><div class="bw-when">When: %s</div><a class="bw-btn" href="%s" target="_blank" rel="noopener">%s</a><div class="bw-save">%s</div></div></div></article>')%(html.escape(b,quote=False).replace("'","&#x27;"),stamp,html.escape(what,quote=False).replace("'","&#x27;"),when,href,btn,save)
sqh='https://mahjsquadshop.com/discount/MAHJMATCH?redirect=/'
blh='https://bamletsmahjong.com/discount/MAHJMATCH?redirect=/'
NOSTACK='Whether <b>MAHJMATCH</b> works on top of this sale is not confirmed yet. Shop through our link.'
ST='Added Fri 11/20 · 8:20am ET'
NEWBF=[mk('My Fair Mahjong',ST,"My Fair Holiday: 20% off sitewide for Black Friday. Seen on their Instagram, Thu 11/19.",'Fri 11/27 · through Mon 11/30','https://myfairmahjong.com/discount/MAHJMATCH?redirect=/','Shop',NOSTACK),
 mk('Mahj Squad',ST,"15% off and free shipping on the new Mint Nutcracker tiles during Thanksgiving week. The tiles drop Sun 11/22 at 3pm ET. Seen on their Instagram, Thu 11/19.",'Thanksgiving week',sqh,'Shop',NOSTACK),
 mk('Peace Love Mahjong',ST,"Black Friday sale: up to 25% off tile sets, mats and accessories, plus free shipping. Seen on their site, Thu 11/19.",'Through Sun 11/29','https://peacelovemahjong.com/?ref=Mahjmatch','Shop',NOSTACK),
 mk('Amanda Toppe',ST,"Black Friday sale with their own code BLACKFRIDAY20. It can't be combined with MAHJMATCH.",'Black Friday week','https://www.amandatoppeart.com/?ref=mahjmatchmaker','Shop','<b>MAHJMATCH</b> does not stack with BLACKFRIDAY20. Shop through our link.')]
NEWBF.append(mk("Bam! Let's Mahjong",ST,"Early Black Friday: 15% off. Seen on their Instagram, Thu 11/19.",'Early Black Friday · no end date given',blh,'Shop',NOSTACK))
# MAIN
for sid,title in SECS:
    g,e=live_sec_span(Lmain,sid); grid=Lmain[g:e]; lc=ART.findall(grid); out=list(lc)
    if sid=='black-friday':
        out=NEWBF+out; log.append(f'BF: +{len(NEWBF)} new cards')
    else:
        lb={brand(a):i for i,a in enumerate(out)}
        add=[]
        for ra in repo_sec(title):
            b=brand(ra)
            if b in lb:
                la=out[lb[b]]
                if txt(la)!=txt(ra) and newest(ra)>newest(la): out[lb[b]]=ra; log.append(f'{title}: replaced {b}')
            elif newest(ra)>=(11,17,0,0): add.append(ra); log.append(f'{title}: added {b}')
        out=add+out
    # Miss Darling Lilac no longer coming soon
    if sid=='coming-soon':
        for i,a in enumerate(out):
            if brand(a)=='Miss Mahjong' and 'opens Wed 11/18' in txt(a): log.append('coming soon: Miss Mahjong card still has opens 11/18!!')
    Lmain=Lmain[:g]+'\n'+''.join(out)+Lmain[e:]
    n=len(out); Lmain=re.sub(r'(<a class="bw-chip" href="#%s">[^<]*<span>)\d+(</span>)'%sid,lambda m:m.group(1)+str(n)+m.group(2),Lmain)
# BPAGES
def bpages(h): return re.findall(r'<section class="bw-bpage" id="p-([^"]+)" hidden>(.*?)</section>',h,re.S)
def bsecs(body):
    head=body[:body.find('<h3')]; out=[]
    for t,g in re.findall(r'<h3 class="bw-bsec">(.*?)</h3><div class="bw-grid">(.*?)</div>(?=<h3|$)',body[len(head):],re.S): out.append((t,ART.findall(g)))
    return head,out
L=dict(bpages(Lbp)); R=dict(bpages(Rbp)); order=[k for k,_ in bpages(Lbp)]
slug=lambda b:re.sub(r'[^a-z0-9]+','-',b.lower()).strip('-')
for k,rb in R.items():
    if k not in L:
        if k=='mahj-squad': L[k]=rb; order.append(k); log.append('bpage added '+k)
        continue
    lh,ls=bsecs(L[k]); rh,rs=bsecs(rb); ld=dict(ls); rd=dict(rs)
    lmax=max([newest(a) for _,c in ls for a in c] or [(0,)]); rmax=max([newest(a) for _,c in rs for a in c] or [(0,)])
    if rmax<=lmax: continue
    new=[]
    for t in ['Black Friday deals','Coming soon','Just dropped']:
        if t=='Black Friday deals': c=ld.get(t) or rd.get(t)
        else: c=rd.get(t) or None
        if c: new.append((t,c))
    for t,c in ls:
        if t not in dict(new) and t=='Black Friday deals': new.append((t,c))
    L[k]=lh+''.join(f'<h3 class="bw-bsec">{t}</h3><div class="bw-grid">{"".join(c)}</div>' for t,c in new); log.append('bpage rebuilt '+k)
# new BF cards into bpages
for a in NEWBF:
    k=slug(brand(a)); k={'bam-let-s-mahjong':'bam-let-s-mahjong'}.get(k,k)
    if k not in L: log.append('NO BPAGE for '+k); continue
    lh,ls=bsecs(L[k]); d=dict(ls); d['Black Friday deals']=[a]+d.get('Black Friday deals',[])
    L[k]=lh+''.join(f'<h3 class="bw-bsec">{t}</h3><div class="bw-grid">{"".join(d[t])}</div>' for t in ['Black Friday deals','Coming soon','Just dropped'] if t in d); log.append('bpage BF card '+k)
last=[k for k,_ in bpages(Lbp)][-1]; order=[k for k in order if k!=last]+[last]
Lbp=''.join(('</div>\n' if k==last else '')+f'<section class="bw-bpage" id="p-{k}" hidden>{L[k]}</section>' for k in order)
out=Lmain+Lbp+Ltail
if 'value="mahj-squad"' not in out: out=out.replace('<option value="mahj-vine">','<option value="mahj-squad">Mahj Squad</option><option value="mahj-vine">')
out,n=re.subn(r'<p class="bw-updated">[^<]*</p>','<p class="bw-updated">Last updated Fri 11/20 · 8:20am ET</p>',out); assert n==1
open('bwmerge/merged_block.html','w').write(out)
print('\n'.join(log)); print(len(blk),'->',len(out)); print('arts',len(ART.findall(out)), 'div balance',out.count('<div')-out.count('</div>'),'vs live',blk.count('<div')-blk.count('</div>'),'sections',out.count('<section')-out.count('</section>'))
