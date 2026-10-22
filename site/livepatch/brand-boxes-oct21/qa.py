import glob,re,os
bad=0
for a in sorted(glob.glob('pages/*.after.html')):
    slug=os.path.basename(a)[:-11]; A=open(a).read(); B=open(f'pages/{slug}.before.html').read()
    errs=[]
    if 'tiffany-chambray-headshot-square.jpg' not in A or 'Tiffany+Headshot' in A: errs.append('headshot')
    if 'Mahji Mentor instructor and the matchmaker' in A and 'oh-my-mahjong' not in slug: errs.append('intro')
    if re.search(r'<h2[^>]*>.*<em',A): errs.append('em headline')
    if sorted(re.findall(r'href="([^"]+)"',A))!=sorted(re.findall(r'href="([^"]+)"',B)): errs.append('links changed')
    if 'MAHJMATCH' in B and 'MAHJMATCH' not in A: errs.append('code')
    if slug.startswith('bird-and-bamboo'):
        t=re.sub(r'<[^>]+>','',A)
        if t.count('Weathered Oak')!=1 or '94 paint colors' not in t or 'samples' not in t: errs.append('bb copy')
    print(slug,errs or 'ok'); bad+=bool(errs)
print('FAIL' if bad else 'ALL OK')
