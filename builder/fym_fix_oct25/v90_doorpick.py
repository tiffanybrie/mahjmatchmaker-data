"""FYM v90 (QA v90: the mat-first door's 'Mats by color' chips still combined colours, with the hint "Tap two or more colors to find
mats with all of them"). Same rule as the in-deck chips (Tiffany Oct 25 17:14): a colour tap = only that colour (another tap switches,
same tap = off); '+ Add a colour' turns on combine mode with a 'Mats with pink and green · N mats · Clear' line. Holiday stays its own toggle.
Usage: python3 v90_doorpick.py <build_dir>  (after v90_colorpick)"""
import sys
P = sys.argv[1] + '/index.html'; h = open(P).read()
def rep(a, b):
    global h
    assert h.count(a) == 1, a[:90]; h = h.replace(a, b)
rep("if(b=q('[data-dfam]')){S.dfams=TOG(S.dfams||[],b.dataset.dfam);DOOR.lim=36;renderTiles();return;}",
    "if(b=q('[data-dfam]')){const f={fam:S.dfams||[],multi:!!S.dmulti};S.dfams=PICK('m',f,b.dataset.dfam);S.dmulti=f.multi;DOOR.lim=36;renderTiles();return;}"
    "\n if(b=q('[data-dmulti]')){S.dmulti=!S.dmulti;if(!S.dmulti){const F=S.dfams||[],hol=F.includes('holiday')?['holiday']:[],cols=F.filter(x=>x!=='holiday');S.dfams=[...hol,...cols.slice(-1)];}renderTiles();return;}")
rep("<small class=\"thint\">Tap two or more colors to find mats with all of them</small>",
    "<small class=\"thint\">Tap a color to see those mats. Want two colors together? Tap + Add a colour first.</small>")
rep("+`<button type=\"button\" data-dfam=\"holiday\" aria-pressed=\"${(S.dfams||[]).includes('holiday')}\" style=\"--c:#a3192e\">Holiday</button>`",
    "+`<button type=\"button\" data-dmulti aria-pressed=\"${!!S.dmulti}\" style=\"--c:#1f3a6b;border-style:${S.dmulti?'solid':'dashed'}\">${S.dmulti?'\\u2713 Adding colours':'+ Add a colour'}</button>`"
    "+`<button type=\"button\" data-dfam=\"holiday\" aria-pressed=\"${(S.dfams||[]).includes('holiday')}\" style=\"--c:#a3192e\">Holiday</button>`")
old = "style=\"--c:${FAMC[f]}\">${FAMN[f]}</button>`).join('')+`</div>`;}"
new = ("style=\"--c:${FAMC[f]}\">${FAMN[f]}</button>`).join('')+(()=>{const F=S.dfams||[],cols=F.filter(x=>x!=='holiday');if(cols.length<2)return '';const n=doorMats().length;"
       "return `<p class=\"fcombo\">${F.includes('holiday')?'Holiday mats':'Mats'} with ${cols.map(c=>FAMN[c].toLowerCase()).join(' <b>and</b> ')} \\u00b7 ${n} mat${n===1?'':'s'} \\u00b7 <button type=\"button\" class=\"lnk\" data-dfam=\"\">Clear</button></p>`;})()+`</div>`;}")
rep(old, new)
open(P, 'w').write(h); print('ok')
