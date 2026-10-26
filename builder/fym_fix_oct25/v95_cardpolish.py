"""FYM v95 match-card polish (card sweep Oct 26, docs/FYM-CARD-SWEEP-oct26.md; Tiffany 10:48-10:51am):
1. Title colour: darkened in the same hue until it reaches >= 3:1 contrast on the cream card (yellow/teal/mint/lime titles).
2. Subtitle "tiles on the <mat> mat": fits the mat column (W*.74): shrink, then two balanced lines; never '…'.
   Very long mat names get a short display name (M.dn, config/fym-mat-display-names-oct26.json); real name stays for links.
3. 'Photo coming soon' tile image: set name, label and maker sized to fit inside the match-card circle (no clipping).
4. Rack label fallback: never the generic 'Racks'; brand + colour instead (Bam Bird / Amahj 'Mahjong Rack & Pusher Set').
5. Truncated mat names fixed: Spring Awakening – Porcelain Blue, Mocha Bloom – Light (names from mahjongrowandco.com;
   locks updated to the corrected names).
Idempotent. Gate [72]. Usage: v95_cardpolish.py <build>"""
import sys, os, json
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i

# --- data: display names + truncated names
DN = json.load(open(REPO + 'config/fym-mat-display-names-oct26.json'))
n_dn = 0
for k, v in DN['dn'].items():
    if k in D['mats'] and D['mats'][k].get('dn') != v: D['mats'][k]['dn'] = v; n_dn += 1
n_fix = 0
for k, v in DN['fix_names'].items():
    if k in D['mats'] and D['mats'][k]['n'] != v: D['mats'][k]['n'] = v; n_fix += 1
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]

def rep(old, new, tag):
    global h
    if new in h: return
    assert h.count(old) == 1, (tag, h.count(old)); h = h.replace(old, new); print('patched', tag)

# 1. title contrast
rep("return `hsl(${Math.round(H2*360)},${Math.round(Math.min(1,Math.max(S2,.38))*100)}%,${Math.round(Math.min(L,.5)*100)}%)`;})();",
    "/* v95 contrast */const Hh=H2*360,Ss=Math.min(1,Math.max(S2,.38));let Ll=Math.min(L,.5);const lum=(hh,ss,ll)=>{const a=ss*Math.min(ll,1-ll),f=n=>{const k=(n+hh/30)%12;const c=ll-a*Math.max(-1,Math.min(k-3,9-k,1));return c<=.03928?c/12.92:Math.pow((c+.055)/1.055,2.4);};return .2126*f(0)+.7152*f(8)+.0722*f(4);};const LC=.8534;while((LC+.05)/(lum(Hh,Ss,Ll)+.05)<3.5&&Ll>.12)Ll-=.02;return `hsl(${Math.round(Hh)},${Math.round(Ss*100)}%,${Math.round(Ll*100)}%)`;})();",
    'title contrast')

# 2. subtitle fit (and display name)
rep("const mName=M[S.fav].n.replace(/\\s*(Neoprene|Leatherette)?\\s*Mahjong Mat$/i,'').trim();",
    "const mName=(M[S.fav].dn||M[S.fav].n).replace(/\\s*(Neoprene|Leatherette)?\\s*(Mahjong )?Mat$/i,'').trim();",
    'mName dn')
rep("y+=44;g.fillStyle='#4a3d58';g.font='italic 500 32px \"Playfair Display\", Georgia, serif';g.fillText(clip(`tiles on the ${mName} mat`,W-120),W/2,y);}",
    "y+=44;g.fillStyle='#4a3d58';{/* v95 subtitle fits the mat column */const SWd=W*.74,st=`tiles on the ${mName} mat`;let sf=32;const SF=n=>{g.font=`italic 500 ${n}px \"Playfair Display\", Georgia, serif`;};SF(sf);while(g.measureText(st).width>SWd&&sf>26){sf-=2;SF(sf);}if(g.measureText(st).width<=SWd){g.fillText(st,W/2,y);}else{const ws=st.split(' ');let bi=1,bs=1e9;for(let k=1;k<ws.length;k++){const a=ws.slice(0,k).join(' '),b=ws.slice(k).join(' ');const sc=Math.max(g.measureText(a).width,g.measureText(b).width);if(sc<bs){bs=sc;bi=k;}}const L2=[ws.slice(0,bi).join(' '),ws.slice(bi).join(' ')];sf=30;SF(sf);while(Math.max(...L2.map(l=>g.measureText(l).width))>SWd&&sf>18){sf-=2;SF(sf);}y-=sf*.45;g.fillText(L2[0],W/2,y);y+=sf*1.15;g.fillText(L2[1],W/2,y);}}}",
    'subtitle fit')

# 3. Photo coming soon: fit inside the circle (the card circle = centre square of the wide image, diameter = height)
old3 = "const ln=L.slice(0,3),fs=wide?58:(ln.some(l=>l.length>10)?48:60),y0=hh/2-(ln.length-1)*fs*.55-14;"
new3 = ("const ln=L.slice(0,wide?4:3),R0=Math.min(w,hh)/2,mxl=Math.max(...ln.map(l=>l.length)),fs=Math.min(wide?58:60,(R0*1.5)/(.62*mxl),(R0*1.1)/(ln.length*1.1+1)),"
        "y0=hh/2-(ln.length-1)*fs*.55-14;/* v95 fit circle */const chord=yy=>2*Math.sqrt(Math.max(0,R0*R0-(yy-hh/2)*(yy-hh/2)))-36;"
        "const lfs=Math.min(wide?24:22,chord(y0+(ln.length-1)*fs*1.1+fs*.95)/(17*.72)),my=Math.min(hh-34,y0+(ln.length-1)*fs*1.1+fs*.95+lfs*1.9),"
        "mfs=Math.min(22,chord(my-8)/(.56*Math.max(4,String(s.maker||'').length)));")
rep(old3, new3, 'soon fit')
rep('font-size="${wide?26:24}" letter-spacing="2" fill="#7a6a85">PHOTO COMING SOON</text><text x="${w/2}" y="${hh-34}" text-anchor="middle" font-family="Bitter, Georgia, serif" font-size="${wide?22:22}" fill="#054689">',
    'font-size="${lfs.toFixed(1)}" letter-spacing="1" fill="#7a6a85">PHOTO COMING SOON</text><text x="${w/2}" y="${my.toFixed(1)}" text-anchor="middle" font-family="Bitter, Georgia, serif" font-size="${mfs.toFixed(1)}" fill="#054689">',
    'soon labels')
# wrap: shorter lines in the circle
rep("if((L[L.length-1]+' '+q).trim().length>(wide?22:13)&&L[L.length-1])L.push(q);",
    "if((L[L.length-1]+' '+q).trim().length>(wide?12:13)&&L[L.length-1])L.push(q);", 'soon wrap')

# 4. rack label fallback
rep("if(!pick)pick=/luxe/i.test(r.n)?'Luxe':/acrylic|lucite/i.test(r.n)?'Acrylic':/wood/i.test(r.n)?'Wood':'Racks';",
    "if(!pick)pick=/luxe/i.test(r.n)?'Luxe':/acrylic|lucite/i.test(r.n)?'Acrylic':/wood/i.test(r.n)?'Wood':(()=>{/* v95 no generic Racks */const c=(r.rf||[]).find(x=>RL_COL.test(x));return ((core||r.bn||'')+(c?' '+c[0].toUpperCase()+c.slice(1):'')).trim()||'Racks';})();",
    'rack fallback')
open(P, 'w').write(h); print('dn', n_dn, 'name fixes', n_fix)
