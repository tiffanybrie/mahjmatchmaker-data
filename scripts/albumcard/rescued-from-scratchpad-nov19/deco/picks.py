import json
S='/tmp/claude-0/-home-claude/05549d34-8fe3-5ca9-a6a5-308991cb9a78/scratchpad/deco/'
D=json.load(open(S+'D117.json'));M=D['mats'];keys=json.load(open(S+'sheetkeys.json'))
def K(n): return keys[n]
LAG=[('top',113),('top',122),('top',23),
('best',226),('best',84),('best',252),('best',344),
('teal',119),('teal',236),('teal',366),('teal',172),('teal',342),('teal',182),('teal',100),
('deco',312),('deco',158),('deco',333),
('peacock',11),('peacock',191),('peacock',88),('peacock',87),('peacock',89),('peacock',372),('peacock',198),
('contrast',270),('contrast',292),('contrast',253),('contrast',21),
('bright',145),('bright',16)]
MUL=[('top',119),('top',226),('top',22),
('best',122),('best',344),('best',330),('best',252),
('teal',24),('teal',322),('teal',295),('teal',234),('teal',348),('teal',366),('teal',236),('teal',199),
('berry',253),('berry',235),('berry',105),('berry',114),('berry',365),('berry',270),('berry',59),('berry',7),
('jewel',84),('jewel',292),('jewel',333),('jewel',177),('jewel',16),
('quiet',376),('quiet',182)]
out={}
for nm,L in (('deco-lagoon',LAG),('deco-mulberry',MUL)):
    out[nm]=[dict(group=g,key=K(n),name=M[K(n)]['n'],brand=M[K(n)]['bn'],rt=M[K(n)].get('rt')) for g,n in L]
    print(nm,len(L),len(set(n for g,n in L)))
json.dump(out,open(S+'picks.json','w'),indent=1,ensure_ascii=False)
