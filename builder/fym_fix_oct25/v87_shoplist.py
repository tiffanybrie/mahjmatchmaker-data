"""FYM v87 (Tiffany Oct 25 15:29, approved): 'Shop your match' checklist on the card page, instead of a 'Buy all' button
(browsers allow one new window per tap; Safari silently blocks the rest).
- Heading 'Shop your match' + one line: each Shop button opens that store in a new tab; come back to tick off the rest.
- Tapping a piece's Shop button marks that row 'Shopped ✓' and updates 'N of M shopped' (kept for this match in sessionStorage).
- 'Text or email me this list' sends every piece + link in one message (share sheet on phones; email fallback).
Usage: python3 v87_shoplist.py <build_dir>  (in place)"""
import sys
P = sys.argv[1] + '/index.html'; h = open(P).read()
def rep(a, b):
    global h
    assert h.count(a) == 1, (a[:70], h.count(a)); h = h.replace(a, b)
rep('<div class="shop"><h3>Take them home</h3>${pieces().map(id=>{',
    '<div class="shop"><h3>Shop your match</h3><p class="shp">Each <b>Shop</b> button opens that store in a new tab. Come back here to tick off the rest.</p>'
    '<p class="shc" id="shc"></p>${pieces().map(id=>{')
rep('return `<div class="si"><img src="${im}"', 'return `<div class="si" data-sid="${esc(id)}"><img src="${im}"')
rep('}).join(\'\')}</div>\n <button type="button" class="lnk" data-restart>',
    '}).join(\'\')}<button type="button" class="big gh shl" data-shoplist>Text or email me this list</button></div>\n <button type="button" class="lnk" data-restart>')
rep('drawCard();}\nconst lk=src=>',
    'drawCard();shopSync();}\n'
    "function shopKey(){return 'fym_shop_'+(set()?set().slug:'')+'|'+S.fav+'|'+S.rpick.join(',');}"
    "function shopDone(){try{return JSON.parse(sessionStorage.getItem(shopKey())||'[]');}catch(e){return [];}}"
    "function shopSync(){const d=shopDone(),rows=[...document.querySelectorAll('.shop .si[data-sid]')];let n=0;rows.forEach(r=>{const on=d.includes(r.dataset.sid);r.classList.toggle('done',on);"
    "const a=r.querySelector('a.go');if(a&&!a.dataset.t0)a.dataset.t0=a.textContent;if(a)a.textContent=on?'Shopped \\u2713':a.dataset.t0;if(on)n++;});"
    "const c=$('shc');if(c){const m=rows.filter(r=>r.querySelector('a.go')).length;c.textContent=n?`${n} of ${m} shopped`:'';}}"
    "document.addEventListener('click',e=>{const a=e.target.closest&&e.target.closest('.shop .si a.go');if(!a)return;const r=a.closest('.si');const d=shopDone();"
    "if(!d.includes(r.dataset.sid)){d.push(r.dataset.sid);try{sessionStorage.setItem(shopKey(),JSON.stringify(d));}catch(x){}}setTimeout(shopSync,50);});"
    "function shopText(){const s=set();const L=pieces().map(id=>{const o=M[id]||R[id]||T[id];if(!o||!o.u)return '';const nm=T[id]?s.name+' tiles':R[id]?o.n:o.n+' mat';"
    "return `${nm} (${o.bn}): ${o.u}`;}).filter(Boolean);const pb=[...new Set(pieces().map(id=>M[id]||R[id]||T[id]).filter(o=>o&&o.pa&&!o.nc).map(o=>o.bn))];const code=pb.length?'Use code MAHJMATCH at '+pb.join(', ')+' to save':'';"
    "return `My mahjong match: ${s.name} + ${M[S.fav].n}\\n\\n${L.join('\\n')}${code?'\\n\\n'+code:''}\\n\\nMatched with Find Your Mat-ch \\u00b7 mahjmatchmaker.com`;}"
    "document.addEventListener('click',async e=>{if(!(e.target.closest&&e.target.closest('[data-shoplist]')))return;const t=shopText();trk('shoplist',{mat:S.fav});"
    "if(navigator.share){try{await navigator.share({title:'My mahjong match',text:t});return;}catch(x){if(x&&x.name==='AbortError')return;}}"
    "const u='mailto:?subject='+encodeURIComponent('My mahjong match')+'&body='+encodeURIComponent(t);try{window.open(u,'_blank')||(location.href=u);}catch(x){location.href=u;}});\n"
    'const lk=src=>')
css = '.rfil{padding:8px 0 10px}'
rep(css, css + ' .shop .shp{margin:-4px 0 6px;font:500 13.5px/1.4 var(--body);color:var(--mute)} .shop .shc{margin:0 0 6px;font:700 13px var(--body);color:var(--pink);min-height:1em}'
    ' .shop .si.done{opacity:.72} .shop .si.done a.go{background:#e9f4ec;color:#2f7a45} .shop .shl{width:100%;margin-top:10px}')
open(P, 'w').write(h); print('ok')
