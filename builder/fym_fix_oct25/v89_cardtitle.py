"""FYM v89 (Tiffany Oct 25 16:51): Mac + Miller 'Heirloom Collection: Fire + Fortune Verdant Fortune' ran off the match card.
The title shrank to a 48px floor and then just overflowed. Now: one line down to 66px; if it still doesn't fit, it wraps to two
balanced lines (break at a space, preferring before '(' or after ':'), each line fitted (floor 44px), and the rest of the card moves
down. Also the two scraped Mac + Miller names are cleaned (one even ended in a stray '(').
Usage: python3 v89_cardtitle.py <build_dir>"""
import sys, json
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
REN = {'www.macandmillermahjong.com/heirloom-collection-fire-fortune-ember-fire-coming-soon': 'Fire + Fortune (Ember)',
       'www.macandmillermahjong.com/heirloom-collection-fire-fortune-verdant-fortune-coming-soon': 'Fire + Fortune (Verdant)'}
for s in D['sets']:
    if s['tile'] in REN: s['name'] = REN[s['tile']]; D['tiles'][s['tile']]['n'] = REN[s['tile']]
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
old = ("{const nm=s.name.toUpperCase(),SW=CT==='B'?150:0;let fs=W>1040?104:98;g.textAlign='center';g.font=`${fs}px Caprasimo, Georgia, serif`;while(g.measureText(nm).width>W-120-2*SW&&fs>48){fs-=4;g.font=`${fs}px Caprasimo, Georgia, serif`;}\n"
       "  y+=fs*.82;g.fillStyle='rgba(255,255,255,.9)';g.fillText(nm,W/2+4,y+4);g.fillStyle=tc;g.fillText(nm,W/2,y);")
new = ("{const nm=s.name.toUpperCase(),SW=CT==='B'?150:0,TW=W-120-2*SW;let fs=W>1040?104:98;g.textAlign='center';const F=n=>{g.font=`${n}px Caprasimo, Georgia, serif`;};F(fs);"
       "while(g.measureText(nm).width>TW&&fs>66){fs-=4;F(fs);}"
       "let lines=[nm];if(g.measureText(nm).width>TW){/* v89: too long for one line -> two balanced lines */const ws=nm.split(' ');let bi=1,bs=1e9;"
       "for(let k=1;k<ws.length;k++){const a=ws.slice(0,k).join(' '),b=ws.slice(k).join(' ');F(fs);let sc=Math.max(g.measureText(a).width,g.measureText(b).width);if(/^\\(/.test(ws[k])||/:$/.test(ws[k-1]))sc-=60;if(sc<bs){bs=sc;bi=k;}}"
       "lines=[ws.slice(0,bi).join(' '),ws.slice(bi).join(' ')];fs=W>1040?96:90;F(fs);while(Math.max(...lines.map(l=>g.measureText(l).width))>TW&&fs>44){fs-=4;F(fs);}}"
       "lines.forEach((l,li)=>{y+=li?fs*.98:fs*.82;g.fillStyle='rgba(255,255,255,.9)';g.fillText(l,W/2+4,y+4);g.fillStyle=tc;g.fillText(l,W/2,y);});")
assert h.count(old) == 1; h = h.replace(old, new)
open(P, 'w').write(h); print('ok')
