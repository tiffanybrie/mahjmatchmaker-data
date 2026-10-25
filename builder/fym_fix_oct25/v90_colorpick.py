"""FYM v90 colour picker (Tiffany Oct 25, asked earlier in the day and again 17:14: "when I click red, the red ones come up. Then I
click orange, red goes off and orange goes on"; plus a clear separate way to pick more than one colour so it's obvious why matches
run out). Mats: a colour tap = only that colour (another tap switches; same tap = off). '+ Add a colour' turns on combine mode,
where taps add colours, and a line under the chips says 'Mats with pink and green · 14 mats · Clear'. Holiday stays its own toggle.
Racks: single colour only, no combine. The colour wheel clears everything.
Usage: python3 v90_colorpick.py <build_dir>"""
import sys
P = sys.argv[1] + '/index.html'; h = open(P).read()
def rep(a, b):
    global h
    assert h.count(a) == 1, a[:90]; h = h.replace(a, b)
rep("const TOG=(C,c)=>!c?[]:(C.includes(c)?C.filter(x=>x!==c):[...C,c]);",
    "const TOG=(C,c)=>!c?[]:(C.includes(c)?C.filter(x=>x!==c):[...C,c]);"
    "/* v90: one colour at a time unless the shopper turns on '+ Add a colour' (mats only) */"
    "const PICK=(k,f,c)=>{if(!c){f.multi=false;return [];}if(k==='r')return f.fam[0]===c?[]:[c];if(c==='holiday')return TOG(f.fam,c);"
    "const hol=f.fam.includes('holiday')?['holiday']:[],cols=f.fam.filter(x=>x!=='holiday');if(f.multi)return [...hol,...TOG(cols,c)];"
    "return [...hol,...(cols.length===1&&cols[0]===c?[]:[c])];};")
rep("f.fam=TOG(f.fam,b.dataset.fam);rerender(b.dataset.k);tourEv('fam');return;}",
    "f.fam=PICK(b.dataset.k,f,b.dataset.fam);rerender(b.dataset.k);tourEv('fam');return;}"
    "  if(b=q('[data-fmulti]')){const f=S.f[b.dataset.fmulti];f.multi=!f.multi;if(!f.multi){const hol=f.fam.includes('holiday')?['holiday']:[],cols=f.fam.filter(x=>x!=='holiday');f.fam=[...hol,...cols.slice(-1)];}rerender(b.dataset.fmulti);return;}")
rep("if(b=q('[data-fclear]')){S.f[b.dataset.fclear].fam=[];", "if(b=q('[data-fclear]')){S.f[b.dataset.fclear].fam=[];S.f[b.dataset.fclear].multi=false;")
# the + Add a colour chip and the combine line (mats)
old = "`<button type=\"button\" class=\"dot\" data-fam=\"${x}\" data-k=\"${k}\" aria-pressed=\"${f.fam.includes(x)}\" title=\"${FAMN[x]}\" aria-label=\"${FAMN[x]}\"><i style=\"background:${FAMC[x]}\"></i></button>`).join('')}</div>`;}"
new = ("`<button type=\"button\" class=\"dot\" data-fam=\"${x}\" data-k=\"${k}\" aria-pressed=\"${f.fam.includes(x)}\" title=\"${FAMN[x]}\" aria-label=\"${FAMN[x]}\"><i style=\"background:${FAMC[x]}\"></i></button>`).join('')}"
       "</div>"
       "${(()=>{const cols=f.fam.filter(x=>x!=='holiday');if(k!=='m'||cols.length<2)return '';const n=matDeck().length;"
       "return `<p class=\"fcombo\">${f.fam.includes('holiday')?'Holiday mats':'Mats'} with ${cols.map(c=>FAMN[c].toLowerCase()).join(' <b>and</b> ')} \\u00b7 ${n} mat${n===1?'':'s'} \\u00b7 <button type=\"button\" class=\"lnk\" data-fclear=\"m\">Clear</button></p>`;})()}`;}")
rep(old, new)
# the chip sits right after the rainbow 'All colors' dot so it's on screen (QA v90: it was off the end of the scrolling row)
rep("<i style=\"background:${RAINBOW}\"></i></button>", "<i style=\"background:${RAINBOW}\"></i></button>${k==='m'?`<button type=\"button\" class=\"chip addc\" data-fmulti=\"m\" aria-pressed=\"${!!f.multi}\">${f.multi?'\\u2713 Adding':'+ Add colour'}</button>`:''}")
css = ".chip.finc{border:2px solid #8a5a3b;color:#6b4226;background:#fff;flex:none}"
rep(css, css + ".frow{gap:4px}.frow .chip.her{padding-left:10px;padding-right:10px}.chip.addc{flex:none;padding:5px 8px;font-size:12.5px;border:2px dashed var(--line);background:#fff;color:var(--navy);font-weight:700;white-space:nowrap}.chip.addc[aria-pressed=\"true\"]{border-style:solid;border-color:var(--navy);background:var(--navy);color:#fff}"
    ".fcombo{margin:6px 2px 0;font:600 13px/1.35 var(--body);color:var(--navy)}.fcombo b{color:var(--pink)}.fcombo .lnk{white-space:nowrap;border:0;background:none;color:var(--pink);font:700 13px var(--body);text-decoration:underline;cursor:pointer;padding:0}")
open(P, 'w').write(h); print('ok')
