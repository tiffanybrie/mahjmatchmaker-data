"""FYM v87 (Tiffany Oct 25 15:12-15:13): tiles door gets a BRAND dropdown next to the search: partner brands A-Z first, then
non-partner brands under 'Non-partner brands' at the bottom. Picking a brand shows every visible tile set from that brand (A-Z);
tapping a colour chip clears the brand and vice versa.
Usage: python3 v87_brandmenu.py <build_dir>  (in place)"""
import sys
P = sys.argv[1] + '/index.html'; h = open(P).read()
def rep(a, b):
    global h
    assert h.count(a) == 1, (a[:70], h.count(a)); h = h.replace(a, b)
rep('<div class="msearch"><input id="tsq" type="search"',
    '${brandMenu()}<div class="msearch"><input id="tsq" type="search"')
rep("function tileGrid(){const all=D.sets.map((s,i)=>[s,i]).filter(x=>VIS(x[0]));",
    "function brandMenu(){const all=D.sets.filter(VIS),pa={},n={};all.forEach(s=>{const t=T[s.tile]||{};n[s.maker]=(n[s.maker]||0)+1;pa[s.maker]=pa[s.maker]||!!t.pa;});"
    "const B=Object.keys(n).sort((a,b)=>a.localeCompare(b)),o=b=>`<option value=\"${esc(b)}\"${S.tbrand===b?' selected':''}>${esc(b)} (${n[b]})</option>`;"
    "return `<div class=\"tbrw\"><label for=\"tbr\">Shop by brand</label><select id=\"tbr\" aria-label=\"Shop tile sets by brand\"><option value=\"\">All brands</option>"
    "<optgroup label=\"Partner brands\">${B.filter(b=>pa[b]).map(o).join('')}</optgroup>${B.some(b=>!pa[b])?`<optgroup label=\"Non-partner brands\">${B.filter(b=>!pa[b]).map(o).join('')}</optgroup>`:''}</select></div>`;}"
    "function tileGrid(){const all=D.sets.map((s,i)=>[s,i]).filter(x=>VIS(x[0]));if(S.tbrand)return all.filter(x=>x[0].maker===S.tbrand).sort((a,b)=>a[0].name.localeCompare(b[0].name)).map(([s,i])=>tileBtn(s,i)).join('');")
rep("if(b=q('[data-tcol]')){const v=b.dataset.tcol;S.tcol=S.tcol===v?'':v;renderTiles();return;}",
    "if(b=q('[data-tcol]')){const v=b.dataset.tcol;S.tcol=S.tcol===v?'':v;S.tbrand='';renderTiles();return;}")
rep("document.addEventListener('input',e=>{if(e.target.id!=='tsq')return;",
    "document.addEventListener('change',e=>{if(e.target.id!=='tbr')return;S.tbrand=e.target.value;if(S.tbrand)S.tcol='';renderTiles();const g=$('tgrid');if(g&&S.tbrand)g.scrollIntoView({block:'nearest'});trk('brand',{x:S.tbrand});});"
    "document.addEventListener('input',e=>{if(e.target.id!=='tsq')return;")
css = '.rfil{padding:8px 0 10px}'
rep(css, css + ' .tbrw{display:flex;align-items:center;gap:10px;margin:10px 2px 8px} .tbrw label{font:700 12px var(--body);letter-spacing:.12em;text-transform:uppercase;color:var(--ink,#2a2036);white-space:nowrap}'
    ' .tbrw select{flex:1;min-width:0;font:600 15px var(--body);color:var(--navy);background:#fff;border:2px solid #ead7e0;border-radius:999px;padding:9px 14px;appearance:auto}')
open(P, 'w').write(h); print('ok')
