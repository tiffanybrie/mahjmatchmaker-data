"""FYM v90 rack colours (Tiffany Oct 25 17:08): rack colour chips were wrong because the old tags were measured off the photo
background (pink -> white Bam Bird racks, blue -> TdT Rich Raisin (brown), purple -> Hip Hip Trust Fund (metallic), black ->
Hip Hip Santa Baby (seasonal), orange -> Virora white hinged). Every visible rack was re-tagged BY EYE (config/rack-colours-oct25.json:
main, also, finish, strength). Her calls:
 - rack colour chips are SINGLE-select (tap = only that colour; another tap switches; tap again = off); no combining on racks
 - new chips: Brown (painted brown, no wood grain), Black (split from 'Brown & black'), Metallic, Clear, next to Wood + Tortoise;
   a rack can sit in more than one (a metallic green: Green + Metallic)
 - seasonal / mostly-metallic racks (Santa Baby, Trust Fund) sit in Metallic only, not a colour
 - Tortoise always leads with Middle & Main Hawksbill Heritage (her Best Value tortoise award); Mahjong Studios never leads a chip
 - Mahj Mood chocolate brown wooden racks are PAINTED brown (Brown, not Wood)
Each rack gets rf (chip families) + rs (score per chip, used to order the chip). hx is replaced by the family colour when the old
measured hx disagrees with the by-eye main colour (it drives the 'goes with this mat' rack order).
Usage: python3 v90_rackcolors.py <build_dir>"""
import sys, os, json, colorsys
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i; R = D['racks']
RC = json.load(open(REPO + 'config/rack-colours-oct25.json'))
FAM = {'white': 'neutral', 'black': 'black', 'brown': 'brown', 'clear': 'clear'}
HEX = {'pink': '#e88fb4', 'red': '#c42a3a', 'orange': '#e8742a', 'yellow': '#e8c43c', 'green': '#4f9a5a', 'blue': '#3a6fc0',
       'purple': '#8a5fc0', 'neutral': '#efe9dc', 'black': '#2a2a2e', 'brown': '#6b4428', 'clear': '#e6e8ea'}
def hue_fam(hx):
    r, g, b = (int(hx[k:k + 2], 16) / 255 for k in (1, 3, 5)); hh, l, s = colorsys.rgb_to_hls(r, g, b); d = hh * 360
    if l > .82 or s < .15: return 'neutral' if l > .45 else 'black'
    if l < .18: return 'black'
    if d < 15 or d >= 345: return 'red' if s > .45 and l < .6 else 'pink'
    if d < 40: return 'brown' if l < .45 else 'orange'
    if d < 70: return 'yellow' if l > .4 else 'brown'
    if d < 165: return 'green'
    if d < 255: return 'blue'
    if d < 300: return 'purple'
    return 'pink'
n = changed_hx = 0
for k, r in R.items():
    c = RC.get(k)
    if not c: continue
    main, also, fin, st = c['main'], c.get('also') or [], c.get('finish') or [], float(c.get('strength') or .5)
    metal_only = ('seasonal' in fin) or ('metallic' in fin and st < .5) or main == 'multi'
    rs = {}
    if not metal_only:
        f = FAM.get(main, main)
        if main == 'brown' and ('wood' in fin or 'tortoise' in fin): pass        # natural wood / tortoise live in their finish chip
        else: rs[f] = 1 + st
        for a in also:
            fa = FAM.get(a, a)
            if fa not in rs and fa != 'brown': rs[fa] = .4 * st
    for x in fin:
        if x in ('wood', 'tortoise', 'metallic', 'clear'): rs[x] = max(rs.get(x, 0), 1 + st)
    if main == 'clear': rs['clear'] = 1 + max(st, .6)
    if k == 'mm:Hawksbill': rs['tortoise'] = 9                                   # her Best Value tortoise award
    if 'Mahjong Studios' in (r.get('bn') or ''): rs = {x: v - .9 for x, v in rs.items()}   # never leads a chip
    r['rf'] = sorted(rs, key=lambda x: -rs[x]); r['rs'] = {x: round(v, 2) for x, v in rs.items()}; n += 1
    want = 'neutral' if main == 'clear' else FAM.get(main, main)
    if main != 'multi' and r.get('hx') and hue_fam(r['hx']) != want and not (want == 'brown' and hue_fam(r['hx']) in ('orange', 'yellow')):
        r['hx'] = HEX.get(want, r['hx']); changed_hx += 1
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
def rep(a, b):
    global h
    assert h.count(a) == 1, a[:90]; h = h.replace(a, b)
# chips: racks get their own colour list + finish chips
rep("${k==='r'?['wood','tortoise'].filter(x=>pool.some(id=>fk(id).includes(x))).map(x=>`<button type=\"button\" class=\"chip finc\" data-fam=\"${x}\" data-k=\"r\" aria-pressed=\"${f.fam.includes(x)}\">${x==='wood'?'Wood':'Tortoise'}</button>`).join(''):''}",
    "${k==='r'?['wood','tortoise','metallic','clear'].filter(x=>pool.some(id=>fk(id).includes(x))).map(x=>`<button type=\"button\" class=\"chip finc\" data-fam=\"${x}\" data-k=\"r\" aria-pressed=\"${f.fam.includes(x)}\">${RFINN[x]}</button>`).join(''):''}")
rep("const fams=FAMS.filter(x=>pool.some(id=>fk(id).includes(x)));", "const fams=(k==='r'?RFAMS:FAMS).filter(x=>pool.some(id=>fk(id).includes(x)));")
rep("FAMC={", "RFAMS=['pink','red','orange','yellow','green','blue','purple','neutral','brown','black'],RFINN={wood:'Wood',tortoise:'Tortoise',metallic:'Metallic',clear:'Clear'};FAMC={brown:'#7a4a2a',black:'#1f1f22',")
rep("FAMN={", "FAMN={brown:'Brown (painted)',black:'Black',")
# rack chip: keep the rack's score order inside the chip
rep("if(f.fam.length)ids=ids.filter(r=>f.fam.every(c=>(R[r].rf||[]).includes(c)));if(f.brand)ids=ids.filter(r=>R[r].bn===f.brand);return ids;}",
    "if(f.fam.length){const c=f.fam[0];ids=ids.filter(r=>(R[r].rf||[]).includes(c));const hr2=f.her?[]:[];const rk=r=>-((R[r].rs||{})[c]||0);ids=ids.map((r,j)=>[r,j]).sort((a,b)=>(rk(a[0])-rk(b[0]))||(a[1]-b[1])).map(x=>x[0]);if(f.her)ids=[...ids.filter(r=>hr.includes(r)),...ids.filter(r=>!hr.includes(r))];}if(f.brand)ids=ids.filter(r=>R[r].bn===f.brand);return ids;}")
open(P, 'w').write(h); print('racks re-tagged', n, '| hx replaced', changed_hx)
