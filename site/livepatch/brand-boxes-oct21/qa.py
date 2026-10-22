import glob,re,os,json
bad=0
for a in sorted(glob.glob('pages/*.after.html')):
    slug=os.path.basename(a)[:-11]; A=open(a).read(); B=open(f'pages/{slug}.before.html').read()
    errs=[]
    if 'tiffany-chambray-headshot-square.jpg' not in A or 'Tiffany+Headshot' in A: errs.append('headshot')
    # everything except the <img> tag must be byte-identical (intro + prose untouched)
    strip=lambda x: re.sub(r'<img [^>]*>','<img>',x)
    if strip(A)!=strip(B): errs.append('copy changed')
    if 'Mahji Mentor instructor and the matchmaker' not in A: errs.append('intro reverted?')
    if re.search(r'<h2[^>]*>.*<em',A): errs.append('em headline')
    print(slug,errs or 'ok'); bad+=bool(errs)
# B&B discount pages (replacements applied to full live HTML)
for slug in ['bird-and-bamboo-discount-code','bird-and-bamboo-discount-code-2']:
    P=json.load(open(f'bb/{slug}.replacements.json'))
    s=open(f'/tmp/claude-0/bp/{slug}.html').read()
    for o,n in P: s=s.replace(o,n)
    t=re.sub(r'<[^>]+>','',s)
    errs=[k for k in ['Weathered','Clear Stain'] if k in s]
    for k in ['/bird-and-bamboo-rack-colors','/willow-mahjong-tile-matches','/heritage-2-0-mahjong-tile-matches','/solara-mahjong-tile-matches','painted wood samples','MAHJMATCH']:
        if k not in s: errs.append('missing '+k)
    if t.count('standard or scalloped')<1 or '19' in re.sub(r'\d{4,}','',t.split('Brand guide')[-1][:0]): errs.append('scalloped')
    if 'Hot Pink.' not in t or 'Dark Navy and Kelly Green' not in t: errs.append('copy')
    print(slug,errs or 'ok'); bad+=bool(errs)
r=open('bb/bird-and-bamboo-rack-colors.after.html').read()
e=[w for w in ['Weathered','Almond','Tudor','Provincial','Mahogany','Dark Walnut','Wood Stains','Clear<','94 paint'] if w in r]
if 'Wood looks:' not in r or 'Peace Love Mahjong Oak' not in r: e.append('note')
if 'Every color comes standard or scalloped' not in r: e.append('scalloped')
print('rack-colors',e or 'ok'); bad+=bool(e)
print('FAIL' if bad else 'ALL OK')
