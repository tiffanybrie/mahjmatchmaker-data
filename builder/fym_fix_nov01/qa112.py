"""v112 QA fixes (independent QA, Nov 1 ~2am), on top of the b112 build:
1. Tigre de Tartán is link-only EVERYWHERE: logo-grid pill 'Save through our link' (not 'Code MAHJMATCH'); no ♥ before link-only
   brands in the brand menus (♥ = code works); partner headings (shop by colour, logo grid, brand menu optgroup) add
   'or through our link' only when a link-only brand is in that section.
2. Flattened photos: the 11 mats moved to config/fym-mat-flat-oct26.json 'skipped' ("QA Nov 1: flatten = close-up/partial")
   get their v111 photo fields back exactly (f, f0, th, th0, w, h, ms, w98) from the v111 build index.
3. Sold-out badge sits after the brand with no dangling ' · '; 'tick off the rest' -> 'check off the rest'; 'Tigre de Tartán'
   with the accent in UI text (display only: data bn stays 'Tigre de Tartan' because the locks hold it); rack colour/finish chips
   only offered when the rack deck would show at least one rack for them (Papaya + red gave an empty deck).
Usage: python3 qa112.py <b112 dir> <b111 dir>"""
import sys, os, json, re
B, B111 = sys.argv[1:3]; R0 = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
def L(p):
    h = open(p).read(); i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:]); return h, i, e, D
h, i, e, D = L(B + '/index.html'); D111 = L(B111 + '/index.html')[3]
# 2
SK = {k: v for k, v in json.load(open(os.path.join(R0, 'config/fym-mat-flat-oct26.json')))['skipped'].items() if 'QA Nov 1' in v.get('why', '')}
FLD = ('f', 'f0', 'th', 'th0', 'w', 'h', 'ms', 'w98'); dead_th = set(); n2 = 0
for k in SK:
    m, o = D['mats'][k], D111['mats'][k]
    if m.get('th') != o.get('th'): dead_th.add(m.get('th'))
    for f in FLD:
        if f in o: m[f] = o[f]
        else: m.pop(f, None)
    n2 += 1
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[i + e:]
def rep(a, b, cnt=1):
    global h
    assert h.count(a) == cnt, (h.count(a), a[:90]); h = h.replace(a, b)
# 1
rep("${BPA(m)?'<em>Code MAHJMATCH</em>':''}", "${BPA(m)?(LINKONLY[m]?'<em>Save through our link</em>':'<em>Code MAHJMATCH</em>'):''}")
rep("${BCODE[b]?'♥ ':''}", "${BCODE[b]&&!LINKONLY[b]?'♥ ':''}")
rep('<h4 class="blh">Partner brands \\u00b7 save 10% or more with code MAHJMATCH</h4>',
    '<h4 class="blh">Partner brands \\u00b7 save 10% or more with code MAHJMATCH${P.some(m=>LINKONLY[m])?\' or through our link\':\'\'}</h4>')
rep('<optgroup label="${CODEL}">', '<optgroup label="${CODEL}${B.filter(b=>BCODE[b]).some(b=>LINKONLY[b])?\' or through our link\':\'\'}">')
rep('P.length?`<h4 class="blh secp" style="grid-column:1/-1">${SECP}</h4>`+P.map(matBtn)',
    'P.length?`<h4 class="blh secp" style="grid-column:1/-1">${SECPH(P.map(id=>M[id].bn))}</h4>`+P.map(matBtn)')
rep('P.length?`<h4 class="blh secp" style="grid-column:1/-1">${SECP}</h4>`+P.map(([s,i])=>tileBtn',
    'P.length?`<h4 class="blh secp" style="grid-column:1/-1">${SECPH(P.map(x=>x[0].maker))}</h4>`+P.map(([s,i])=>tileBtn')
rep("const BPA=m=>!!BCODE[m];", "const BPA=m=>!!BCODE[m];function SECPH(bs){return bs.some(b=>LINKONLY[b])?'Partner brands \\u00b7 save with code MAHJMATCH or through our link':SECP;}/*v112q*/"
    "function BDN(x){return x==='Tigre de Tartan'?'Tigre de Tart\\u00e1n':x;}/*v112q display name with the accent (data bn stays plain: locks)*/")
# 3a sold-out badge
rep("' · <b class=\"sob\">Sold out</b>'", "' <b class=\"sob\">Sold out</b>'", 2)
rep(".sob{color:#c8325f;font-weight:700}", ".sob{display:inline-block;margin-left:6px;padding:0 7px;border-radius:999px;background:#fde7ee;color:#c8325f;font-weight:700;font-size:.85em;line-height:1.5;white-space:nowrap}")
# 3b
rep("tick off the rest", "check off the rest")
# 3c accent in UI text
for a in ("esc(M[id].bn||'')", "esc(s.maker)", "esc(m.bn||'')", "esc(r.s.maker)", "esc(o.bn)", "esc(o.bn||'')", "esc(R[id].bn)", "esc(s.maker||'')", "esc(R[id].bn||'')"):
    inner = a[4:-1]; h = h.replace(a, f"esc(BDN({inner}))")
rep("at ${esc(b)} through our link", "at ${esc(BDN(b))} through our link")
rep("at ${esc(b)} with code", "at ${esc(BDN(b))} with code", 2)
rep("No discount available for ${esc(b)}", "No discount available for ${esc(BDN(b))}")
rep("${esc(b)} (${n[b]})</option>", "${esc(BDN(b))} (${n[b]})</option>")
rep("<span>${esc(b)}</span></button>", "<span>${esc(BDN(b))}</span></button>")
rep("BNM[m]||esc(m)", "BNM[m]||esc(BDN(m))", 2)
rep("by ${o.bn}", "by ${BDN(o.bn)}")
rep("pbC.join(', ')", "pbC.map(BDN).join(', ')")
rep("...pbL.map(b=>b+':", "...pbL.map(b=>BDN(b)+':")
# 3d rack chips that would give an empty deck
rep("const fams=(k==='r'?RFAMS:FAMS).filter(x=>pool.some(id=>fk(id).includes(x)));",
    "const fams=(k==='r'?RFAMS:FAMS).filter(x=>pool.some(id=>fk(id).includes(x))).filter(x=>k!=='r'||f.fam.includes(x)||RDOTN(x)>0);")
rep("['wood','tortoise','metallic','clear'].filter(x=>pool.some(id=>fk(id).includes(x)))",
    "['wood','tortoise','metallic','clear'].filter(x=>pool.some(id=>fk(id).includes(x))&&(f.fam.includes(x)||RDOTN(x)>0))")
rep("function rackDeck(){return INSF('r',rackDeck0());}",
    "function rackDeck(){return INSF('r',rackDeck0());}function RDOTN(x){const f=S.f.r,s=f.fam,e0=S.insE;f.fam=[x];let n=0;try{n=rackDeck().length;}catch(z){n=1;}finally{f.fam=s;S.insE=e0;}return n;}/*v112q: no colour chip that empties the rack deck*/")
p = B + '/index.html'; os.remove(p); open(p, 'w').write(h)
# drop the now-unused v112 flattened thumbnails from b24v1.js (copy-on-write)
b = open(B + '/b24v1.js').read(); nd = 0
for t in dead_th:
    if t and ('"' + t + '"') not in h:
        b, c = re.subn(r'"' + re.escape(t) + r'":"data:image/[a-z]+;base64,[^"]+",?', '', b); nd += c
b = b.replace(',})', '})')
os.remove(B + '/b24v1.js'); open(B + '/b24v1.js', 'w').write(b)
print('qa112: restored', n2, 'mats to v111 photos; dropped', nd, 'unused thumbs; b24v1.js', len(b))
