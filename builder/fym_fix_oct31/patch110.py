"""FYM v110 = public "Version 1.10" (Oct 31 night): STARS (save favourites per device, no account yet; Tiffany Oct 27 6:01pm +
Oct 31 9:33pm) + Mahj & Moon ShopMy links (config/mahj-moon-shopmy-links.json, Etsy 6%).
Code-only patch + one data edit; applies identically to the app index, the artifact index and the website copy.
Usage: python3 patch110.py <in index.html> <out index.html>"""
import sys, json, os
SRC, OUT = sys.argv[1:3]
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
h = open(SRC).read()

def rep(a, b, n=1):
    global h
    c = h.count(a)
    assert c == n, (c, a[:90])
    h = h.replace(a, b)

# version
assert h.count('Version 1.9.4') == 2
h = h.replace('Version 1.9.4', 'Version 1.10')

CSS = '''.stb{display:inline-flex;align-items:center;justify-content:center;flex:none;width:34px;height:34px;margin-left:auto;border-radius:50%;background:#fff;border:2px solid #f3d3df;color:#c8325f;font:400 19px/1 Arial,sans-serif;cursor:pointer;padding:0;-webkit-tap-highlight-color:transparent}
.stb[aria-pressed="true"]{background:#c8325f;border-color:#c8325f;color:#fff}
.scard .meta span.stb{display:inline-flex;font:400 19px/1 Arial,sans-serif;color:#c8325f;overflow:visible;white-space:normal}
.scard .meta span.stb[aria-pressed="true"]{color:#fff}
.scard:not(.rk):not(.tk) .meta .stb{margin-right:44px}
.tgrid button{position:relative}
.tgrid .stb{position:absolute;top:4px;right:4px;width:26px;height:26px;font-size:15px;margin:0;z-index:2}
.si .stb{width:30px;height:30px;font-size:16px;margin:0 2px 0 0}
.mystars{display:inline-flex;align-items:center;gap:6px;margin:8px 2px 2px;border:2px solid #c8325f;background:#fff;color:#c8325f;border-radius:999px;padding:6px 14px;font:700 14px var(--body);cursor:pointer}
.mystars b{background:#c8325f;color:#fff;border-radius:999px;padding:0 7px;font-size:12px;line-height:18px}
#starsov{position:fixed;inset:0;z-index:9999;background:rgba(40,52,69,.55);display:flex;align-items:flex-start;justify-content:center;overflow:auto;padding:16px}
#starsov .sbox{background:#fff;border-radius:20px;max-width:720px;width:100%;padding:16px 16px 20px;box-shadow:0 12px 40px rgba(0,0,0,.3)}
#starsov h2{margin:0 0 4px;font:400 26px var(--head,inherit);color:#283445}
#starsov .shint{margin:0 0 10px;color:#6b6070;font:400 14px var(--body)}
#starsov h3{margin:14px 0 6px;font:700 12px var(--body);letter-spacing:.12em;text-transform:uppercase;color:#c8325f}
#starsov .sgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
@media (min-width:600px){#starsov .sgrid{grid-template-columns:repeat(5,1fr)}}
#starsov .sit{position:relative;border:2px solid #f3e1e8;background:#fff;border-radius:14px;padding:6px 5px;display:flex;flex-direction:column;align-items:center;gap:4px;font:700 12.5px/1.15 var(--body);cursor:pointer;min-width:0;text-align:center;color:#283445;text-decoration:none}
#starsov .sit img{width:100%;aspect-ratio:1;object-fit:cover;border-radius:10px}
#starsov .sit small{font-weight:400;color:#6b6070}
#starsov .sit .stb{position:absolute;top:4px;right:4px;width:26px;height:26px;font-size:15px;margin:0}
#starsov .sclose{float:right;border:0;background:#f6e8ee;color:#283445;border-radius:999px;width:36px;height:36px;font:700 18px var(--body);cursor:pointer}
#starsov .sempty{color:#6b6070;font:400 14px var(--body);margin:6px 0}
'''
i = h.rindex('</style></head>'); h = h[:i] + CSS + h[i:]

JS = r'''/*v110 STARS: per-device favourites, no account (localStorage via LS, safe when storage is blocked)*/
const STAR={k:'fym_stars_v1',mem:null,get(){if(this.mem)return this.mem;let v=null;try{v=JSON.parse(LS.get(this.k)||'null');}catch(e){}this.mem=Array.isArray(v)?v:[];return this.mem;},has(x){return this.get().includes(x);},tog(x){const a=this.get(),i=a.indexOf(x);if(i>=0)a.splice(i,1);else a.unshift(x);LS.set(this.k,JSON.stringify(a));return i<0;}};
function STB(t,id){const x=t+':'+id,on=STAR.has(x);return `<span class="stb" role="button" tabindex="0" data-star="${esc(x)}" aria-pressed="${on}" aria-label="${on?'Remove from':'Add to'} My stars">${on?'★':'☆'}</span>`;}
function STG(t,id){return STB(t,id);}
function starsLink(){const n=STAR.get().length;return `<button type="button" class="mystars" data-mystars>★ My stars${n?` <b>${n}</b>`:''}</button>`;}
function starSync(x,on){document.querySelectorAll('[data-star]').forEach(el=>{if(el.dataset.star!==x)return;el.setAttribute('aria-pressed',on);el.textContent=on?'★':'☆';el.setAttribute('aria-label',(on?'Remove from':'Add to')+' My stars');});const n=STAR.get().length;document.querySelectorAll('[data-mystars]').forEach(el=>{el.innerHTML='★ My stars'+(n?` <b>${n}</b>`:'');});}
function starItems(){const out={t:[],m:[],r:[]};STAR.get().forEach(x=>{const j=x.indexOf(':'),t=x.slice(0,j),id=x.slice(j+1);if(t==='t'){const i=D.sets.findIndex(s=>s.slug===id);if(i>=0&&VIS(D.sets[i]))out.t.push({i,s:D.sets[i]});}else if(t==='m'){if(M[id]&&!M[id].hid)out.m.push(id);}else if(t==='r'){if(R[id])out.r.push(id);}});return out;}
function openStars(){const g=starItems(),n=g.t.length+g.m.length+g.r.length;const sec=(lab,arr,f)=>`<h3>${lab}</h3>`+(arr.length?`<div class="sgrid">${arr.map(f).join('')}</div>`:`<p class="sempty">No ${lab.toLowerCase()} starred yet.</p>`);
 const html=`<div class="sbox" role="dialog" aria-label="My stars"><button type="button" class="sclose" data-starsclose aria-label="Close">✕</button><h2>★ My stars</h2><p class="shint">${n?'Saved on this device. Tap one to match it.':'Tap ☆ on any tile set, mat or rack to save it here.'}</p>`+
 sec('Tile sets',g.t,r=>`<button type="button" class="sit" data-starst="${r.i}"><img src="${pile(r.s)}" alt="" loading="lazy"><span>${esc(r.s.name)}</span><small>${esc(r.s.maker)}</small>${STB('t',r.s.slug)}</button>`)+
 sec('Mats',g.m,id=>`<button type="button" class="sit" data-starsm="${esc(id)}"><img src="${matTh(id)}" alt="" loading="lazy"><span>${esc(MN(id))}</span><small>${esc(M[id].bn||'')}</small>${STB('m',id)}</button>`)+
 sec('Racks',g.r,id=>{const o=R[id];return `<a class="sit" ${o.u?`href="${esc(o.u)}" target="_blank" rel="noopener"`:''}><img src="${rackSrc(id)}" alt="" loading="lazy" style="object-fit:contain"><span>${esc(shortR(id))}</span><small>${esc(o.bn||'')}${o.u?' · Shop ›':''}</small>${STB('r',id)}</a>`;})+`</div>`;
 let ov=document.getElementById('starsov');if(!ov){ov=document.createElement('div');ov.id='starsov';document.body.appendChild(ov);}ov.innerHTML=html;trk('stars',{x:String(n)});}
function closeStars(){const ov=document.getElementById('starsov');if(ov)ov.remove();}
function starFake(attr,val){const b=document.createElement('button');b.type='button';b.setAttribute(attr,val);b.style.display='none';document.body.appendChild(b);b.click();b.remove();}
['pointerdown','mousedown','touchstart'].forEach(ev=>document.addEventListener(ev,e=>{if(e.target.closest&&e.target.closest('[data-star]'))e.stopPropagation();},{capture:true,passive:true}));
document.addEventListener('click',e=>{const q=s=>e.target.closest&&e.target.closest(s);let b;
 if(b=q('[data-star]')){e.preventDefault();e.stopImmediatePropagation();const x=b.dataset.star,on=STAR.tog(x);starSync(x,on);const j=x.indexOf(':');trk('star',{x:x.slice(0,j)+(on?':on':':off'),mat:x.slice(0,j)==='m'?x.slice(j+1):'',rack:x.slice(0,j)==='r'?x.slice(j+1):'',set:x.slice(0,j)==='t'?x.slice(j+1):''});return;}
 if(q('[data-mystars]')){e.preventDefault();e.stopImmediatePropagation();openStars();return;}
 if(q('[data-starsclose]')||(e.target&&e.target.id==='starsov')){e.preventDefault();e.stopImmediatePropagation();closeStars();return;}
 if(b=q('[data-starst]')){e.preventDefault();e.stopImmediatePropagation();const i=b.dataset.starst;closeStars();if(S.door!=='tiles'){S.door='tiles';S.ddeck=false;S.dkeep=null;}starFake('data-tile',i);return;}
 if(b=q('[data-starsm]')){e.preventDefault();e.stopImmediatePropagation();const id=b.dataset.starsm;closeStars();S.door='mat';S.ddeck=false;S.dkeep=null;S.tilesOpen=true;starFake('data-dmat',id);window.scrollTo({top:0,behavior:'smooth'});return;}
},true);
document.addEventListener('keydown',e=>{if((e.key==='Enter'||e.key===' ')&&e.target.closest&&e.target.closest('[data-star]')){e.preventDefault();e.target.click();}if(e.key==='Escape')closeStars();});
'''
rep('function tileBtn(', JS + 'function tileBtn(')

# star buttons: swipe cards (mat + rack), tile swipe card, grids, shop rows; My stars entry under Shop by brand
rep("${mat&&o.alt?`<em class=\"alt\">${esc(o.alt)}</em>`:''}</div></div>",
    "${mat&&o.alt?`<em class=\"alt\">${esc(o.alt)}</em>`:''}</div>${back?'':STB(mat?'m':'r',id)}</div>")
rep("<span>${esc(s.maker)}</span></div></div></div>`;}", "<span>${esc(s.maker)}</span></div>${peek?'':STB('t',s.slug)}</div></div>`;}")
rep('<button type="button" data-tile="${i}" aria-pressed="${S.set===i}">', '<button type="button" data-tile="${i}" aria-pressed="${S.set===i}">${STG(\'t\',s.slug)}')
rep('<button type="button" data-dmat="${esc(id)}">', '<button type="button" data-dmat="${esc(id)}">${STG(\'m\',id)}')
rep('<button type="button" data-dset="${r.i}" aria-pressed="${S.set===r.i}">', '<button type="button" data-dset="${r.i}" aria-pressed="${S.set===r.i}">${STG(\'t\',r.s.slug)}')
rep("${o.ncn&&!o.dc?'<em class=\"ncn\">No code available at this time</em>':''}</div>",
    "${o.ncn&&!o.dc?'<em class=\"ncn\">No code available at this time</em>':''}</div>${T[id]?STB('t',set().slug):STB(M[id]?'m':'r',id)}")
rep("${bnote(cur)}</div>`;}", "${bnote(cur)}${starsLink()}</div>`;}")

# data: Mahj & Moon shop links -> ShopMy (Etsy 6%); unsure ones keep their link
L = json.load(open(os.path.join(R, 'config', 'mahj-moon-shopmy-links.json')))
i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:]); e += i
n = 0
for k, v in L.items():
    if k.startswith('_') or not isinstance(v, dict) or not v.get('shopmy_url'): continue
    m = D['mats'].get(k)
    if not m or m.get('bn') != 'Mahj & Moon': continue
    m['u'] = v['shopmy_url']; n += 1
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[e:]
open(OUT, 'w').write(h)
print('patch110 ok', OUT, 'mahj&moon shopmy links:', n)
