"""v112 app-code patches prepared by the MATCH-INBOX sweep (Nov 1). Every patch is anchored on the v110 code (assert = stop if the
v111 accounts build moved it; re-anchor, never skip). Idempotent (each patch checks its own marker). Run after fixes112.py.
Usage: python3 ui112.py <build_dir>

 A  Card titles: NO white offset copy behind the title (Tiffany Oct 27 12:50am: "Why do we need white outlines anywhere?").
    v110 drawCard still draws `rgba(255,255,255,.9)` at +4,+4 under every title line. Title = one plain fill. Gate N1.
 B  Shop by colour, both doors (Tiffany Oct 31 2:28pm, her own wording approved): after a colour chip, partner brands first under
    'Partner brands · save with code MAHJMATCH', then 'More brands · no discount code'. Colour order kept inside each group.
    Tile door: tileGrid colour branch. Mat door: doorMats + mdgrid render. Gate N2.
 C  Brand menu copy (Tiffany Oct 29 3:32pm APPROVED, the latest call; the 1:57pm pink box stays pink): drop "Partner brands come
    first. Save 10% or more at any of them with code MAHJMATCH"; general note = "Code MAHJMATCH works at brands marked ♥"; a ♥
    on every partner brand in the dropdown. Gate N3.
 D  Tigre de Tartán visible-code policy (Oct 29; BRAND-GUIDE changelog Oct 30; docs/research/tdt-code-exposure-oct29.md):
    no visible text pairs TdT with the code. bnote(TdT) = "Save at Tigre de Tartán through our link" (no % in UI text: gate [4] / rule 7); codeLine counts TdT
    pieces as link-only; share text drops TdT from the "Use code MAHJMATCH at ..." list and adds "Tigre de Tartán: save through
    the link above". Links unchanged (auto-apply). Gate N4.
 E  Rack fit by TILE SIZE (Tiffany Oct 26 7:37/7:39pm): rackOK uses R.len + T.tw (data from rackfit112.py) instead of the
    brand-name smallSet()/sm rule: a rack <=18.5" only with tiles <=0.95" wide. OMM-racks-with-OMM-tiles rule unchanged. Gate N5.
 F  Tortoise order (Tiffany Oct 26 7:40pm): Mahjong Row & Co. Scalloped Tortoise (20") always before Middle & Main Hawksbill
    in the rack deck when both are in it. Gate N6.
 G  Tile colour groups: drop the dead "Glitter Glow" entry (no set has that name; the Bespoke tile is hidden) and put Sunday
    December 1994 in Holiday (nutcracker, poinsettia, cardinal tiles = Christmas). Gate N7.
"""
import sys, re, json
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read(); done = []
def rep(a, b, tag, count=1):
    global h
    if tag in h: return
    assert h.count(a) == count, f'{tag}: anchor found {h.count(a)}x, expected {count}: {a[:90]}'
    h = h.replace(a, b); done.append(tag)

# A
rep("g.fillStyle='rgba(255,255,255,.9)';g.fillText(l,W/2+4,y+4);g.fillStyle=tc;g.fillText(l,W/2,y);",
    "/*v112A no white copy*/g.fillStyle=tc;g.fillText(l,W/2,y);", '/*v112A')
# B tile door
rep("return (BACKG[S.tcol]||[]).flatMap(n=>all.filter(x=>x[0].name===n)).sort((a,b)=>!!T[a[0].tile].soon-!!T[b[0].tile].soon||(BPA(a[0].maker)?0:1)-(BPA(b[0].maker)?0:1))/* v104: partners first, non-partners last (Photo coming soon still at the very bottom, gate [61]) */.map(([s,i])=>tileBtn(s,i)).join('');}",
    "{/*v112B*/const L=(BACKG[S.tcol]||[]).flatMap(n=>all.filter(x=>x[0].name===n)).sort((a,b)=>!!T[a[0].tile].soon-!!T[b[0].tile].soon||(BPA(a[0].maker)?0:1)-(BPA(b[0].maker)?0:1));const P=L.filter(x=>BPA(x[0].maker)),N=L.filter(x=>!BPA(x[0].maker));return (P.length?`<h4 class=\"blh secp\" style=\"grid-column:1/-1\">${SECP}</h4>`+P.map(([s,i])=>tileBtn(s,i)).join(''):'')+(N.length?`<h4 class=\"blh np secn\" style=\"grid-column:1/-1\">${SECN}</h4>`+N.map(([s,i])=>tileBtn(s,i)).join(''):'');}}",
    '/*v112B*/')
rep("BPA=m=>!!BCODE[m];", "BPA=m=>!!BCODE[m];const SECP='Partner brands \\u00b7 save with code MAHJMATCH',SECN='More brands \\u00b7 no discount code';/*v112B*/", 'SECP=')
# B mat door: partners first after a colour chip, with the two headers in the grid
rep("return C.length?CSORT(ids,C):ids;}\nconst MN=",
    "if(!C.length)return ids;ids=CSORT(ids,C);/*v112Bm*/return [...ids.filter(id=>BCODE[M[id].bn]),...ids.filter(id=>!BCODE[M[id].bn])];}\nconst MN=", '/*v112Bm*/')
rep("ids.length?ids.slice(0,DOOR.lim).map(matBtn).join(''):", "ids.length?DGRID(ids):", 'DGRID(ids)')
rep("g.innerHTML=L.length?L.slice(0,DOOR.lim).map(matBtn).join(''):", "g.innerHTML=L.length?DGRID(L):", 'DGRID(L)')
rep("function matBtn(id){", "function DGRID(L){const s=L.slice(0,DOOR.lim);if(!(S.dfams||[]).filter(x=>x!=='holiday').length)return s.map(matBtn).join('');const P=s.filter(id=>BCODE[M[id].bn]),N=s.filter(id=>!BCODE[M[id].bn]);return (P.length?`<h4 class=\"blh secp\" style=\"grid-column:1/-1\">${SECP}</h4>`+P.map(matBtn).join(''):'')+(N.length?`<h4 class=\"blh np secn\" style=\"grid-column:1/-1\">${SECN}</h4>`+N.map(matBtn).join(''):'');}/*v112DG*/\nfunction matBtn(id){", '/*v112DG*/')
# C + D brand note
TDT = 'Tigre de Tartan'
rep("function bnote(b){if(!b)return `<p class=\"bnote gen\"><span>✦ Partner brands come first. Save 10% or more at any of them with code <b>MAHJMATCH</b></span></p>`;",
    "const LINKONLY={'Tigre de Tartan':1,'Tigre de Tart\\u00e1n':1};/*v112D TdT: no code next to their name*/function bnote(b){if(!b)return `<p class=\"bnote gen\"><span>✦ Code <b>MAHJMATCH</b> works at brands marked ♥</span></p>`;/*v112C*/if(LINKONLY[b])return `<p class=\"bnote ok\"><span>✦ Save at ${esc(b)} through our link</span></p>`;",
    '/*v112C*/')
rep("o=b=>`<option value=\"${esc(b)}\"${cur===b?' selected':''}>${esc(b)} (${n[b]})</option>`;",
    "o=b=>`<option value=\"${esc(b)}\"${cur===b?' selected':''}>${BCODE[b]?'♥ ':''}${esc(b)} (${n[b]})</option>`;/*v112C2*/", '/*v112C2*/')
# D codeLine + share text
rep("function codeLine(){const ps=[T[set().tile],M[S.fav],...S.rpick.map(r=>R[r])].filter(o=>o&&o.pa&&!o.nc);",
    "function codeLine(){const ps0=[T[set().tile],M[S.fav],...S.rpick.map(r=>R[r])].filter(o=>o&&o.pa&&!o.nc),ps=ps0.filter(o=>!LINKONLY[o.bn]);if(!ps.length&&ps0.length)return 'Save through our links';/*v112D2*/",
    '/*v112D2*/')
rep(".filter(o=>o&&o.pa&&!o.nc).map(o=>o.bn))];const code=pb.length?'Use code MAHJMATCH at '+pb.join(', ')+' to save':'';",
    ".filter(o=>o&&o.pa&&!o.nc).map(o=>o.bn))];const pbL=pb.filter(b=>LINKONLY[b]),pbC=pb.filter(b=>!LINKONLY[b]);const code=[pbC.length?'Use code MAHJMATCH at '+pbC.join(', ')+' to save':'',...pbL.map(b=>b+': save through the link above')].filter(Boolean).join('\\n');/*v112D3*/",
    '/*v112D3*/')
# E rack fit by tile size
rep("const rackOK=r=>R[r]&&!R[r].hid&&!R[r].rt&&(!R[r].sm||smallSet())&&",
    "const RFIT=r=>!(R[r].len&&R[r].len<=18.5)||((T[set().tile]||{}).tw||9)<=0.95;/*v112E tile-size rack fit*/const rackOK=r=>R[r]&&!R[r].hid&&!R[r].rt&&RFIT(r)&&",
    '/*v112E')
# F tortoise order (end of rackDeck)
rep("ids=[...ids.filter(r=>!poor(r)&&ids.indexOf(r)<=ids.indexOf(G[G.length-1])),...ids.filter(r=>!(!poor(r)&&ids.indexOf(r)<=ids.indexOf(G[G.length-1])))];}return ids;}",
    "ids=[...ids.filter(r=>!poor(r)&&ids.indexOf(r)<=ids.indexOf(G[G.length-1])),...ids.filter(r=>!(!poor(r)&&ids.indexOf(r)<=ids.indexOf(G[G.length-1])))];}{/*v112F tortoise order*/const A='mahjongrowandco.com/scalloped-deluxe-tortoise-rack',HB=ids.findIndex(r=>/hawksbill/i.test(r)),ia=ids.indexOf(A);if(ia>HB&&HB>=0){ids.splice(ia,1);ids.splice(HB,0,A);}}return ids;}",
    '/*v112F')
# G BACKG
m = re.search(r'const BACKG=(\{.*?\});\n', h)
assert m, 'BACKG not found'
BG = json.loads(m.group(1)); ch = False
for g in BG:
    if 'Glitter Glow' in BG[g]: BG[g] = [n for n in BG[g] if n != 'Glitter Glow']; ch = True
if 'December 1994' not in BG['Holiday']: BG['Holiday'].append('December 1994'); ch = True
if ch:
    h = h[:m.start(1)] + json.dumps(BG, ensure_ascii=False) + h[m.end(1):]; done.append('G BACKG')
open(P, 'w').write(h); print('ui112 applied:', done)
