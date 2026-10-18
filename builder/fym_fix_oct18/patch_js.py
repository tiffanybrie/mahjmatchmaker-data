import sys
src,dst=sys.argv[1],sys.argv[2]
h=open(src).read()
def R(old,new,cnt=1):
    global h
    n=h.count(old)
    assert n==cnt,(n,old[:90])
    h=h.replace(old,new)
# ---- CSS
R(".matv .chip{position:absolute;right:8px;top:8px}",
""".matv .chip{position:absolute;right:8px;top:8px}
.matv img{cursor:zoom-in}
.xz{position:absolute;right:10px;bottom:10px;z-index:3;width:36px;height:36px;border-radius:50%;border:0;background:rgba(36,52,143,.88);color:#fff;font:700 18px/36px var(--body);cursor:pointer;padding:0}
.lbx{position:fixed;inset:0;z-index:999;background:rgba(20,16,30,.94);display:flex;flex-direction:column}
.lbx .lbh{display:flex;align-items:center;gap:8px;padding:10px 12px;color:#fff;font:700 14px var(--body)}
.lbx .lbh b{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.lbx .lbh button{border:0;border-radius:999px;background:#fff;color:var(--navy);font:700 14px var(--body);padding:8px 14px;cursor:pointer}
.lbx .lbb{position:relative;flex:1;overflow:hidden;touch-action:none}
.lbx .lbb img{position:absolute;left:0;top:0;max-width:100%;max-height:100%;transform-origin:0 0;-webkit-user-drag:none}
.lbx .zb{position:absolute;right:12px;bottom:14px;display:flex;gap:8px;z-index:2}
.lbx .zb button{width:44px;height:44px;border-radius:50%;border:0;background:#fff;color:var(--navy);font:700 22px var(--body)}
.herbar{display:flex;align-items:center;justify-content:space-between;gap:8px;margin:8px 0 2px}
.herbar small{color:var(--mute);font-size:12px}
.chip.her{white-space:nowrap}
.scard .aw{position:absolute;left:10px;top:40px;z-index:2;background:#1f3a6b;color:#fff;border-radius:999px;padding:4px 10px;font:700 11px var(--body);pointer-events:none}
.r3p{border:2px dashed #f2c2d4;border-radius:18px;padding:18px 16px;text-align:center;background:#fff8fb;margin-top:8px}
.r3p p{margin:0 0 12px;font-size:15px;color:var(--ink,#2a2036)}
.r3p img{width:120px;height:120px;object-fit:contain;display:block;margin:0 auto 10px}
.dnote{background:#fdf1f6;border-radius:14px;padding:10px 12px;margin:6px 0;font-size:13.5px;line-height:1.35}
.dnote b{color:var(--pink)}
@media (min-width:561px){.tilev{aspect-ratio:16/7}.matv{height:min(80vw,460px)}}""")
# ---- helpers & pools
R("function matPool(){return set().rank.map(i=>D.order[i]).filter(id=>M[id]&&(!M[id].rt||herMat(id)));}",
"""function matPool(){const h=set().m.map(x=>x[0]).filter(id=>M[id]);const hs=new Set(h);return [...h,...set().rank.map(i=>D.order[i]).filter(id=>M[id]&&!hs.has(id)&&!M[id].rt&&!M[id].hid)];}
const smallSet=()=>/Oh My Mahjong|Mahjong Row/.test(set().maker||'');
const rackOK=r=>R[r]&&!R[r].hid&&!R[r].rt&&(!R[r].sm||smallSet())&&(!/Oh My Mahjong/.test(R[r].bn||'')||/Oh My Mahjong/.test(set().maker||''));
const uni=()=>UNI.filter(rackOK);""")
R("""function rackPool(){const hr=herRacks();""","""function rackPool(){const hr=herRacks().filter(r=>R[r]);""")
R(""" const rest=Object.keys(R).filter(r=>!hr.includes(r)&&!UNI.includes(r)&&!R[r].rt).map(r=>[sc(r),r]).sort((a,b)=>a[0]-b[0]).map(x=>x[1]);
 return [...new Set([...hr,...UNI,...rest])];}""",""" const U=uni();const rest=Object.keys(R).filter(r=>!hr.includes(r)&&!U.includes(r)&&rackOK(r)).map(r=>[sc(r),r]).sort((a,b)=>a[0]-b[0]).map(x=>x[1]);
 return [...new Set([...hr,...U,...rest])];}""")
R("""if(f.her)ids=ids.filter(r=>hr.includes(r)||UNI.includes(r));""","""if(f.her){const U=uni();ids=ids.filter(r=>hr.includes(r)||U.includes(r));}""")
# ---- filter chip label + second toggle
R("""<button type="button" class="chip her" data-her="${k}" aria-pressed="${f.her}">${icon()} Tiffany\\u2019s</button>""","""${herBtn(k)}""")
R("""function filters(k){""","""function herBtn(k){const on=S.f[k].her;return `<button type="button" class="chip her" data-her="${k}" aria-pressed="${on}" title="Tap to switch">${icon()} ${on?'Showing: Tiffany\\u2019s picks only':'Showing: all '+(k==='m'?'mats':'racks')}</button>`;}
function herBar(k){const n=k==='m'?set().m.length:herRacks().length;return `<div class="herbar">${herBtn(k)}<small>${S.f[k].her?'Tap to see everything':(n?'Her picks still come first':'')}</small></div>`;}
function filters(k){""")
# ---- card labels + award
R("""function card(id,k,back){const mat=k==='m';const o=mat?M[id]:R[id];const her=mat?herMat(id):(herRacks().includes(id)||UNI.includes(id));""",
"""function card(id,k,back){const mat=k==='m';const o=mat?M[id]:R[id];const her=mat?herMat(id):(herRacks().includes(id)||uni().includes(id));const aw=!mat&&D.badges&&D.badges[id];""")
R("""!mat&&UNI.includes(id)&&!herRacks().includes(id)?'Goes with everything':'Tiffany’s match'}</span>`:''}""","""!mat&&UNI.includes(id)&&!herRacks().includes(id)?'Goes with everything':'Tiffany’s match'}</span>`:''}${aw&&!back?`<span class="aw">🏆 ${esc(aw)}</span>`:''}""")
# mat expand button on the top mat card
R("""${back?'':`${mat&&!aer?'<div class="zb">""","""${back||!mat?'':`<button type="button" class="xz" data-lbx="${esc(id)}" aria-label="See this mat full screen">⤢</button>`}${back?'':`${mat&&!aer?'<div class="zb">""")
# ---- mats section: her bar + door note
R("""+filters('m')+
 (S.mode==='close'?""","""+filters('m')+(S.dmat&&S.dset===S.set&&M[S.dmat]?`<div class="dnote">Your mat: <b>${esc(M[S.dmat].n)}</b>. Want to see other mats for ${esc(s.name)}? Swipe below.</div>`:'')+
 (S.mode==='close'?""")
R("""+acts('m')+tray('m');
 bindCard('m');""","""+herBar('m')+acts('m')+tray('m');
 bindCard('m');""")
# ---- racks section: option-2 prompt
R("""function renderRacks(){const el=$('s-racks');if(!S.fav){el.innerHTML='';return;}const m=M[S.fav];""",
"""function selSuitor(){return S.peek||(S.fav&&S.liked.includes(S.fav)?S.fav:null)||S.liked[S.liked.length-1]||null;}
function renderRacks(){const el=$('s-racks');if(S.set==null){el.innerHTML='';return;}
 const sel=selSuitor();
 if(!S.fav||(S.peek&&S.peek!==S.fav)){el.innerHTML=head(3,'Love triangle','All couples need a wingman.')+`<div class="r3p">${sel?`<img src="${matTh(sel)}" alt=""><p>Pick your favorite suitor and tap <b>Mock your match</b> to swipe racks.</p><button type="button" class="big" style="width:auto;padding:10px 18px" data-mock="${esc(sel)}">Mock your match with ${esc(M[sel].n)} ›</button>`:`<p>Heart a mat in step 2 and it’ll show up here.</p>`}</div>`;return;}
 const m=M[S.fav];""")
R("""<div class="matv"><img src="${matSrc(S.fav)}" alt="${esc(m.n)}" class="${m.c?'':'photo'}"><button type="button" class="chip mini" data-back-mats>Change mat</button></div>${deck('r')}</div>`+acts('r')+tray('r');""",
"""<div class="matv"><img src="${matSrc(S.fav)}" alt="${esc(m.n)}" class="${m.c?'':'photo'}" data-lbx="${esc(S.fav)}"><button type="button" class="chip mini" data-back-mats>Change mat</button><button type="button" class="xz" data-lbx="${esc(S.fav)}" aria-label="See this mat full screen">⤢</button></div>${deck('r')}</div>`+herBar('r')+acts('r')+tray('r');""")
R("""['s-racks','Racks',!!S.fav]""","""['s-racks','Racks',S.set!=null&&(!!S.fav||S.liked.length>0)]""")
# peek / unpeek re-render racks; mock keeps rack state when same mat
R("""if(b=q('[data-peek]')){const id=b.dataset.peek;S.peek=S.peek===id?null:id;renderMats();return;}
 if(q('[data-unpeek]')){S.peek=null;renderMats();return;}""","""if(b=q('[data-peek]')){const id=b.dataset.peek;S.peek=S.peek===id?null:id;renderMats();renderRacks();steps();return;}
 if(q('[data-unpeek]')){S.peek=null;renderMats();renderRacks();steps();return;}""")
R("""if(b=q('[data-mock]')){const id=b.dataset.mock;if(S.fav!==id){resetFrom(2);S.fav=id;}S.peek=null;renderAll();jump('s-racks');return;}""",
"""if(b=q('[data-mock]')){const id=b.dataset.mock;if(!S.liked.includes(id))S.liked.push(id);if(S.fav!==id){const keep=S.rpick.slice(),rl=S.rliked.slice();resetFrom(2);S.rliked=rl;S.rpick=keep;S.fav=id;}S.peek=null;renderAll();jump('s-racks');const r=$('s-racks');if(r){r.classList.add('flash');setTimeout(()=>r.classList.remove('flash'),900);}return;}
 if(b=q('[data-lbx]')){openLbx(b.dataset.lbx);return;}
 if(q('[data-lbxclose]')){closeLbx();return;}""")
# decide on mat swipe: also re-render racks prompt
R("""if(yes&&!S.liked.includes(id))S.liked.push(id);renderMats();}""","""if(yes&&!S.liked.includes(id))S.liked.push(id);renderMats();if(!S.fav)renderRacks();steps();}""")
# ---- mat door: her tile sets ranked by strength, dset flow
R("""const her=rows.filter(r=>r.her),alb=""","""const her=rows.filter(r=>r.her).map(r=>Object.assign(r,{hp:r.s.m.findIndex(x=>x[0]===id)})).sort((a,b)=>a.hp-b.hp),alb=""")
R("""if(b=q('[data-dset]')){const i=+b.dataset.dset;resetFrom(1);S.set=i;S.f.m.her=set().m.length>0;resetFrom(2);S.fav=S.dmat;S.tilesOpen=false;renderAll();jump('s-racks');return;}""",
"""if(b=q('[data-dset]')){const i=+b.dataset.dset;resetFrom(1);S.set=i;S.f.m.her=set().m.length>0;resetFrom(2);const dm=S.dmat;S.dset=i;S.liked=[dm];S.seen[dm]=1;S.peek=dm;S.fav=dm;S.tilesOpen=false;renderAll();jump('s-mats');return;}""")
R("""function doorMats(){const c=matCounts();let ids=Object.keys(M).filter(id=>!M[id].rt||c[id]);""","""function doorMats(){const c=matCounts();let ids=Object.keys(M).filter(id=>!M[id].hid&&(!M[id].rt||c[id]));""")
R("function resetFrom(level){if(level<=1){Object.assign(S,{seen:{},liked:[],hist:[],peek:null});","function resetFrom(level){if(level<=1){Object.assign(S,{seen:{},liked:[],hist:[],peek:null,dset:null});")
R(".lbx{position:fixed;",'#s-racks.flash{box-shadow:0 0 0 3px var(--pink);border-radius:18px}\n.lbx{position:fixed;')
# ---- email copy
R("""<p>We’ll send both sizes: one for your Facebook group and one to pin.</p>""","""<p>We’ll email you the view you picked in both sizes: a post size and a tall pin size.</p>""")
R("""In the live version this emails '+v+' both sizes of the card plus the shop links.""","""In the live version this emails '+v+' the view you picked in both sizes (post and tall pin) plus the shop links.""")
# ---- lightbox
R("""function bindTile(id){""","""function openLbx(id){closeLbx();const m=M[id];if(!m)return;const d=document.createElement('div');d.className='lbx';d.id='lbx';d.innerHTML=`<div class="lbh"><b>${esc(m.n)} · ${esc(m.bn||'')}</b><button type="button" data-lbxclose>Close ✕</button></div><div class="lbb" id="lbb"><img src="${matSrc(id)}" alt="${esc(m.n)}" draggable="false"><div class="zb"><button type="button" data-z="-1" aria-label="Zoom out">−</button><button type="button" data-z="1" aria-label="Zoom in">+</button></div></div>`;document.body.appendChild(d);document.body.style.overflow='hidden';
 const bx=$('lbb'),im=bx.querySelector('img');const go=()=>{const r=bx.getBoundingClientRect();const k=Math.min(r.width/im.naturalWidth,r.height/im.naturalHeight);im.style.width=im.naturalWidth*k+'px';im.style.height=im.naturalHeight*k+'px';im.style.maxWidth='none';im.style.maxHeight='none';im.style.left=(r.width-im.naturalWidth*k)/2+'px';im.style.top=(r.height-im.naturalHeight*k)/2+'px';zoomer(bx,im,bx,{});};if(im.complete&&im.naturalWidth)go();else im.addEventListener('load',go,{once:true});
 bx.addEventListener('wheel',e=>{e.preventDefault();const b=bx.querySelector(e.deltaY<0?'[data-z="1"]':'[data-z="-1"]');if(b)b.click();},{passive:false});
 loadMC(m.f).then(()=>{if(MC[m.f]&&im.src!==MC[m.f])im.src=MC[m.f];});}
function closeLbx(){const d=$('lbx');if(d){d.remove();document.body.style.overflow='';}}
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeLbx();});
function bindTile(id){""")
# ---- match card 'tri' view: album-card layout
old_tri_start=h.index(" if(S.view==='tri'){")
old_tri_end=h.index(" }else if(S.view==='stack'){")
h=h[:old_tri_start]+""" if(S.view==='tri'){
  g.restore();const lab=96,ax=px+22,ay=py+22,aw=pw-44,ah=ph-44-lab;
  g.save();g.shadowColor='rgba(60,30,40,.22)';g.shadowBlur=18;g.shadowOffsetY=10;matBox=fit(mat,ax,ay,aw,ah);g.restore();
  const mb=matBox||{x:ax,y:ay,w:aw,h:ah};
  const cr=Math.min(mb.w,mb.h)*0.30,cx=Math.min(mb.x+mb.w-cr*0.72,px+pw-cr-16),cy=Math.min(mb.y+mb.h-cr*0.72,py+ph-lab-cr+18);
  if(tile){g.save();g.shadowColor='rgba(40,20,30,.35)';g.shadowBlur=22;g.shadowOffsetY=8;g.fillStyle=CREAM;g.beginPath();g.arc(cx,cy,cr+9,0,Math.PI*2);g.fill();g.restore();
   g.save();g.beginPath();g.arc(cx,cy,cr,0,Math.PI*2);g.clip();const k=Math.max(2*cr/tile.width,2*cr/tile.height);g.drawImage(tile,cx-tile.width*k/2,cy-tile.height*k/2,tile.width*k,tile.height*k);g.restore();}
  if(rks.length){const rw=Math.min(mb.w*0.5,(cx-cr-24)-(mb.x+14)),n=rks.length,rh=Math.min(96,rw*0.2+30),gap=14,tot=n*rh+(n-1)*gap,rx=mb.x+14,ry=Math.min(mb.y+mb.h-tot-14,py+ph-lab-tot-6);
   g.save();g.fillStyle='rgba(255,255,255,.9)';g.beginPath();g.roundRect(rx-10,ry-10,rw+20,tot+20,18);g.fill();g.restore();
   g.save();g.shadowColor='rgba(60,30,40,.2)';g.shadowBlur=10;g.shadowOffsetY=5;rks.forEach((r,i)=>fit(r,rx,ry+i*(rh+gap),rw,rh));g.restore();}
  const lyb=py+ph-lab+30;label('RACKS',rName||'—',px+pw*.18,lyb,pw*.32);label('MAT',mName,px+pw*.5,lyb,pw*.32);label('TILE SET',tName,px+pw*.82,lyb,pw*.32);
"""+h[old_tri_end:]
open(dst,'w').write(h)
print('ok')
