"""Mat Color Tagger page (private artifact). Tiffany sets ONE primary color + up to 3 accents per mat; taps save to db
collection `matcolors` (doc id = gallery image name), {primary, secondary:[], holiday, skip, key, by:'tiffany', at}.
Pre-filled with the computer's guess (scripts/colors/families.py); ordered most-likely-wrong first.
Usage: python3 build_tagger.py D.json manifest.json preview_with_EMB.html out.html [guesses.json]"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import families as F
D = json.load(open(sys.argv[1]))['mats']; man = json.load(open(sys.argv[2]))
src = open(sys.argv[3]).read(); i = src.find('window.__EMB='); j = src.find('</script>', i)
EMB = src[i:j].rstrip().rstrip(';')  # window.__EMB={...}
G = json.load(open(sys.argv[5])) if len(sys.argv) > 5 else {}
R0 = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
rows = []
for name, k in man.items():
    v = D[k]
    if name in G: g = G[name]; p, s, tone, amb = g['p'], g['s'], g['t'], g['a']
    else: p, s, tone, amb = F.guess_img(os.path.join(R0, 'assets/mats/gallery', name + '.webp'))
    old = (v.get('mf') or ['neutral'])[0]
    score = (1.0 if old != p else 0) + amb * 0.8 + (0.5 if p == 'multi' else 0) + (0.3 if p in ('brown', 'orange', 'yellow', 'gold') else 0)
    rows.append({'id': name, 'k': k, 'n': v['n'], 'b': v['bn'], 'p': p, 's': s, 't': tone, 'h': 1 if v.get('hol') else 0,
                 'r': 1 if v.get('rt') else 0, 'sc': round(score, 3)})
rows.sort(key=lambda r: -r['sc'])
for i2, r in enumerate(rows): r['o'] = i2
data = json.dumps(rows, separators=(',', ':'), ensure_ascii=False).replace('</', '<\\/')
codes = json.dumps([[c, F.LABEL[c]] for c in F.CODES])
tones = json.dumps([[t, F.TONE_LABEL[t]] for t in F.TONES])
html = r"""<title>Mat Color Tagger</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Caprasimo&family=Bitter:wght@400;600;700&display=swap">
<style>
/* layout: sticky toolbar, then a single column of mat cards (2-up on wide screens) */
:root{--bg:#fffaf7;--card:#ffffff;--ink:#14305f;--soft:#5d6b86;--pink:#e8457f;--pinksoft:#fde6ef;--line:#ecdfe6;--ok:#2f8a5b;--disp:"Caprasimo",Georgia,serif;--body:"Bitter",Georgia,serif}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#141a2b;--card:#1d2540;--ink:#f3eaf0;--soft:#aab3c9;--pink:#ff6a9d;--pinksoft:#3b2238;--line:#2d3654;--ok:#5fd19a;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#141a2b;--card:#1d2540;--ink:#f3eaf0;--soft:#aab3c9;--pink:#ff6a9d;--pinksoft:#3b2238;--line:#2d3654;--ok:#5fd19a;color-scheme:dark}
body{background:var(--bg);color:var(--ink);font-family:var(--body)}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:var(--bg)}
.wrap{max-width:1100px;margin:0 auto;padding-block:12px 60px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
h1{font-family:var(--disp);font-weight:400;color:var(--pink);font-size:clamp(28px,6vw,40px);margin:4px 0 2px;text-wrap:balance}
.lede{color:var(--soft);margin:0 0 10px;line-height:1.5;max-width:62ch}
.bar{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--bg);padding:8px 0;border-bottom:1px solid var(--line);display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.count{font-weight:700;font-variant-numeric:tabular-nums;margin-right:auto}
.count b{color:var(--pink)}
.seg{display:flex;border:1.5px solid var(--ink);border-radius:999px;overflow:hidden}
.seg button{border:0;background:transparent;color:var(--ink);font:600 14px var(--body);padding:8px 14px;min-height:40px;cursor:pointer}
.seg button[aria-pressed="true"]{background:var(--ink);color:var(--bg)}
select,.tg{font:600 14px var(--body);color:var(--ink);background:var(--card);border:1.5px solid var(--line);border-radius:999px;padding:8px 12px;min-height:40px}
.tg[aria-pressed="true"]{border-color:var(--pink);background:var(--pinksoft)}
.filt{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 0}
.filt[hidden]{display:none}
.msg{background:var(--pinksoft);border-radius:12px;padding:10px 14px;margin:10px 0;font-weight:600}
.grid{display:grid;grid-template-columns:1fr;gap:14px;margin-top:14px}
@media (min-width:820px){.grid{grid-template-columns:1fr 1fr}}
.sec h2{font-family:var(--disp);font-weight:400;font-size:24px;margin:22px 0 0;color:var(--ink)}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:12px;display:grid;grid-template-columns:120px 1fr;grid-template-areas:'img hd' 'img body';gap:6px 12px;min-width:0;align-items:start}.card img{grid-area:img}.hd{grid-area:hd;min-width:0}.body{grid-area:body;min-width:0}
.card.done{border-color:var(--ok)}
.card.skip{opacity:.55}
.card img{width:120px;height:120px;object-fit:cover;border-radius:10px;cursor:zoom-in;background:var(--line)}
.meta{min-width:0}
.brand{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--soft)}
.name{font-weight:700;font-size:16px;margin:2px 0 6px;overflow-wrap:anywhere}
.chk{color:var(--ok);font-size:13px;font-weight:700;margin-left:6px}
.lab{font-size:12px;font-weight:700;color:var(--soft);margin:6px 0 4px;letter-spacing:.04em;text-transform:uppercase}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{display:inline-flex;align-items:center;gap:6px;border:1.5px solid var(--line);background:transparent;color:var(--ink);border-radius:999px;padding:6px 10px;min-height:36px;font:600 13px var(--body);cursor:pointer}
.chip i{width:12px;height:12px;border-radius:50%;flex:none;border:1px solid rgba(0,0,0,.15)}
.chip[aria-pressed="true"]{border-color:var(--ink);background:var(--ink);color:var(--bg)}
.chip.multi{border-width:2px;border-color:var(--pink)}.chip.ton[aria-pressed="true"]{background:var(--pink);border-color:var(--pink);color:#fff}.chip.sec[aria-pressed="true"]{background:var(--pinksoft);color:var(--ink);border-color:var(--pink)}
.row2{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px}
.more{display:block;margin:18px auto 0;font:700 15px var(--body);background:var(--ink);color:var(--bg);border:0;border-radius:999px;padding:12px 22px;min-height:44px;cursor:pointer}
.zoom{position:fixed;inset:0;background:rgba(0,0,0,.82);display:flex;align-items:center;justify-content:center;z-index:20;padding:20px}
.zoom img{max-width:100%;max-height:100%;border-radius:12px}
button:focus-visible,select:focus-visible{outline:3px solid var(--pink);outline-offset:2px}
@media (max-width:600px){.card{grid-template-columns:84px 1fr;grid-template-areas:'img hd' 'body body'}.card img{width:84px;height:84px}.chip{padding:5px 9px;min-height:34px;font-size:12.5px}}
</style>
<div class="wrap">
<h1>Mat Color Tagger</h1>
<p class="lede">Pick each mat's main color, the one you'd say at first glance, its tone (clean and bright, muted and earthy, or pastel), then tap any accent colors (up to 3). The computer's guess is filled in, and the mats most likely wrong come first. Every tap saves right away and overrides the computer's colors everywhere: swipe books, Find Your Match and the gallery.</p>
<div class="bar">
<span class="count" id="count"></span>
<div class="seg" role="group" aria-label="View"><button type="button" id="vWrong" aria-pressed="true">Most likely wrong</button><button type="button" id="vColor" aria-pressed="false">By main color</button></div>
<select id="brand" aria-label="Brand"><option value="">All brands</option></select>
<button type="button" class="tg" id="unchk" aria-pressed="false">Unchecked only</button>
</div>
<div class="filt" id="tonef" hidden role="group" aria-label="Filter by tone"></div><div class="filt" id="secf" hidden role="group" aria-label="Filter by accent color"></div>
<div class="msg" id="msg" hidden></div>
<div id="list"></div>
</div>
<script>__EMB__</script>
<script type="application/json" id="rows">__DATA__</script>
<script>
(function(){
var CODES=__CODES__,TONES=__TONES__,SW={pink:'#f39bbd',red:'#c8323c',orange:'#ee7a2f',yellow:'#f5cf3a',gold:'#c39a2c',brown:'#8a5a3b',blue:'#3f6fc4',teal:'#2fb3b0',green:'#4f9a55',purple:'#8a5bbf',neutral:'#efe6d6',bw:'linear-gradient(90deg,#111 50%,#fff 50%)',dark:'#2b2a40',multi:'conic-gradient(#e8457f,#f2b33d,#4f9a55,#3f6fc4,#8a5bbf,#e8457f)'};
var LBL={};CODES.forEach(function(c){LBL[c[0]]=c[1]});
var R=JSON.parse(document.getElementById('rows').textContent),BY={};R.forEach(function(r){BY[r.id]=r});
var S={}; // saved state by id
var view='wrong',brand='',unchk=false,secF='',toneF='',shown=60,db=null,canWrite=true;
var list=document.getElementById('list'),msg=document.getElementById('msg');
var bs={};R.forEach(function(r){bs[r.b]=1});Object.keys(bs).sort(function(a,b){return a.toLowerCase()<b.toLowerCase()?-1:1}).forEach(function(b){var o=document.createElement('option');o.textContent=b;document.getElementById('brand').appendChild(o)});
var secf=document.getElementById('secf');secf.innerHTML='<button type="button" class="chip sec" data-s="" aria-pressed="true">Any accent</button>'+CODES.map(function(c){return '<button type="button" class="chip sec" data-s="'+c[0]+'" aria-pressed="false"><i style="background:'+SW[c[0]]+'"></i>'+c[1]+'</button>'}).join('');
var tonef=document.getElementById('tonef');tonef.innerHTML='<button type="button" class="chip sec" data-t="" aria-pressed="true">Any tone</button>'+TONES.map(function(t){return '<button type="button" class="chip sec" data-t="'+t[0]+'" aria-pressed="false">'+t[1]+'</button>'}).join('');
tonef.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;toneF=b.dataset.t;tonef.querySelectorAll('button').forEach(function(x){x.setAttribute('aria-pressed',x===b)});shown=60;render()});
function cur(r){var s=S[r.id];return s?{p:s.primary||r.p,s:s.secondary||[],t:s.tone||r.t,h:!!s.holiday,k:!!s.skip,done:true}:{p:r.p,s:r.s.slice(),t:r.t,h:!!r.h,k:false,done:false}}
function esc(t){return String(t).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function card(r){var c=cur(r),img=(window.__EMB&&window.__EMB[r.id])||'';
return '<div class="card'+(c.done?' done':'')+(c.k?' skip':'')+'" data-id="'+r.id+'"><img src="'+img+'" alt="'+esc(r.b+' '+r.n)+'" loading="lazy" width="120" height="120"><div class="hd"><div class="brand">'+esc(r.b)+(r.r?' · Retired':'')+'</div><div class="name">'+esc(r.n)+(c.done?'<span class="chk">&#10003; checked</span>':'')+'</div></div><div class="body">'+
'<div class="lab">Main color (what you\'d call it at first glance)</div><div class="chips">'+CODES.map(function(x){return '<button type="button" class="chip pri'+(x[0]==='multi'?' multi':'')+'" data-p="'+x[0]+'" aria-pressed="'+(c.p===x[0])+'"><i style="background:'+SW[x[0]]+'"></i>'+x[1]+'</button>'}).join('')+'</div>'+'<div class="lab">Tone</div><div class="chips">'+TONES.map(function(x){return '<button type="button" class="chip ton" data-t="'+x[0]+'" aria-pressed="'+(c.t===x[0])+'">'+x[1]+'</button>'}).join('')+'</div>'+
'<div class="lab">Accents (up to 3)</div><div class="chips">'+CODES.filter(function(x){return x[0]!=='multi'}).map(function(x){return '<button type="button" class="chip sec" data-s="'+x[0]+'" aria-pressed="'+(c.s.indexOf(x[0])>=0)+'"'+(x[0]===c.p?' hidden':'')+'><i style="background:'+SW[x[0]]+'"></i>'+x[1]+'</button>'}).join('')+'</div>'+
'<div class="row2"><button type="button" class="tg hol" aria-pressed="'+c.h+'">Holiday</button><button type="button" class="tg skp" aria-pressed="'+c.k+'">Skip (never match)</button>'+(c.done?'':'<button type="button" class="tg ok">Looks right</button>')+'</div></div></div>'}
function pass(r){if(brand&&r.b!==brand)return false;if(unchk&&S[r.id])return false;var c=cur(r);if(secF&&c.s.indexOf(secF)<0)return false;if(toneF&&c.t!==toneF)return false;return true}
function render(){var n=Object.keys(S).length;document.getElementById('count').innerHTML='<b>'+n+'</b> of '+R.length+' checked';
var h='';
if(view==='wrong'){var L=R.filter(pass),sl=L.slice(0,shown);h='<div class="grid">'+sl.map(card).join('')+'</div>'+(L.length>shown?'<button type="button" class="more" id="more">Show more ('+(L.length-shown)+' left)</button>':'')}
else{CODES.forEach(function(c){var L=R.filter(function(r){return pass(r)&&cur(r).p===c[0]});if(!L.length)return;h+='<section class="sec"><h2>'+c[1]+' <small style="font:600 14px var(--body);color:var(--soft)">'+L.length+'</small></h2><div class="grid">'+L.slice(0,shown).map(card).join('')+'</div>'+(L.length>shown?'<p class="lede">'+(L.length-shown)+' more in '+c[1]+'. Tap "Show more" below.</p>':'')+'</section>'});h+='<button type="button" class="more" id="more">Show more</button>'}
list.innerHTML=h||'<p class="msg">No mats match these filters.</p>';var m=document.getElementById('more');if(m)m.onclick=function(){shown+=60;render()}}
function rerender(id){var el=list.querySelector('.card[data-id="'+id+'"]');if(!el)return;var t=document.createElement('div');t.innerHTML=card(BY[id]);el.replaceWith(t.firstChild);document.getElementById('count').innerHTML='<b>'+Object.keys(S).length+'</b> of '+R.length+' checked'}
var timers={},busy={},pend={};
function save(id,state){S[id]=state;rerender(id);if(!db){return}clearTimeout(timers[id]);timers[id]=setTimeout(function(){flush(id)},500)}
function flush(id){if(busy[id]){pend[id]=1;return}busy[id]=1;var s=S[id],r=BY[id];
db.doc('matcolors/'+id).set({primary:s.primary,secondary:s.secondary,tone:s.tone,holiday:s.holiday,skip:s.skip,key:r.k,by:'tiffany',at:new Date().toISOString()}).then(function(){busy[id]=0;if(pend[id]){pend[id]=0;flush(id)}},function(e){busy[id]=0;if(e&&e.code==='invalid_argument'){canWrite=false;msg.hidden=false;msg.textContent='This view can\'t save changes. Ask Tiffany for edit access.'}else{msg.hidden=false;msg.textContent='A tap didn\'t save. Check your connection and tap again.'}})}
list.addEventListener('click',function(e){var b=e.target.closest('button'),im=e.target.closest('.card img');
if(im){var z=document.createElement('div');z.className='zoom';z.innerHTML='<img src="'+im.src+'" alt="">';z.onclick=function(){z.remove()};document.body.appendChild(z);return}
if(!b)return;var el=b.closest('.card');if(!el)return;var id=el.dataset.id,r=BY[id],c=cur(r);
var st={primary:c.p,secondary:c.s.slice(),tone:c.t,holiday:c.h,skip:c.k};
if(b.classList.contains('pri')){st.primary=b.dataset.p;st.secondary=st.secondary.filter(function(x){return x!==st.primary})}
else if(b.classList.contains('sec')){var x=b.dataset.s,i=st.secondary.indexOf(x);if(i>=0)st.secondary.splice(i,1);else{if(st.secondary.length>=3)st.secondary.shift();st.secondary.push(x)}}
else if(b.classList.contains('ton'))st.tone=b.dataset.t;
else if(b.classList.contains('hol'))st.holiday=!st.holiday;
else if(b.classList.contains('skp'))st.skip=!st.skip;
else if(!b.classList.contains('ok'))return;
save(id,st)});
function setView(v){view=v;shown=60;document.getElementById('vWrong').setAttribute('aria-pressed',v==='wrong');document.getElementById('vColor').setAttribute('aria-pressed',v==='color');secf.hidden=v!=='color';tonef.hidden=v!=='color';render()}
document.getElementById('vWrong').onclick=function(){setView('wrong')};document.getElementById('vColor').onclick=function(){setView('color')};
document.getElementById('brand').onchange=function(e){brand=e.target.value;shown=60;render()};
document.getElementById('unchk').onclick=function(e){unchk=!unchk;e.currentTarget.setAttribute('aria-pressed',unchk);shown=60;render()};
secf.addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;secF=b.dataset.s;secf.querySelectorAll('button').forEach(function(x){x.setAttribute('aria-pressed',x===b)});shown=60;render()});
render();
if(window.claude&&window.claude.use){window.claude.use('db').then(function(d){if(!d){msg.hidden=false;msg.textContent='Open this page signed in to save your taps.';return}db=d;
d.collection('matcolors').onSnapshot(function(snap){var ch=[];snap.docChanges().forEach(function(x){var v=x.doc.data();if(x.type==='removed'){delete S[x.doc.id]}else if(v&&BY[x.doc.id]&&!busy[x.doc.id]&&!timers[x.doc.id+'_l']){S[x.doc.id]={primary:v.primary,secondary:v.secondary||[],tone:v.tone,holiday:!!v.holiday,skip:!!v.skip}}ch.push(x.doc.id)});if(ch.length>20)render();else ch.forEach(rerender)},function(){msg.hidden=false;msg.textContent='Lost the connection to saved colors. Reload the page.'})})}
else{msg.hidden=false;msg.textContent='Open this page in Claude to save your taps.'}
})();
</script>"""
html = html.replace('__EMB__', EMB).replace('__DATA__', data).replace('__CODES__', codes).replace('__TONES__', tones)
open(sys.argv[4], 'w').write(html)
print(len(rows), 'mats', round(len(html) / 1e6, 2), 'MB')
