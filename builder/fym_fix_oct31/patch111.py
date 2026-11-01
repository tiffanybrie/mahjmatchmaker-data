"""FYM v111 = public "Version 1.11" (Oct 31 late night): ACCOUNTS (Tiffany Oct 31 9:58pm: option B, email sign-in) on top of v110 stars.
- Supabase (config/fym-supabase.json; public/publishable key only, no tables): a signed-in user's stars + saved match cards live in
  auth user_metadata.fym = {stars:[...], matches:[...], v:1}. supabase-js is loaded LAZILY (only when Account opens or a session /
  sign-in link is present), and every call is guarded so the matching flow never depends on it.
- Sign in = email code (6-digit, works everywhere incl. the claude.ai copy) or the email link (website: the token lands in the parent
  page hash of the same-origin srcdoc iframe; we read it, set the session and clean the URL).
- Top bar: "★" My stars (count) + account icon, reachable from every step (MATCH-INBOX v110 note). My stars sheet gets a
  "My match cards" tab (saved on this device; synced to the account when signed in; tap = reopen the card).
Code-only patch; applies identically to the app index, the artifact index and the website copy.
Usage: python3 patch111.py <in index.html> <out index.html>"""
import sys, json, os
SRC, OUT = sys.argv[1:3]
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
SB = json.load(open(os.path.join(R, 'config', 'fym-supabase.json')))
h = open(SRC).read()

def rep(a, b, n=1):
    global h
    c = h.count(a)
    assert c == n, (c, a[:90])
    h = h.replace(a, b)

assert h.count('Version 1.10') == 2, h.count('Version 1.10')
h = h.replace('Version 1.10', 'Version 1.11')

CSS = '''.tbx{display:flex;gap:6px;flex:none;align-items:center}
.tbb{position:relative;display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:50%;border:2px solid #c8325f;background:#fff;color:#c8325f;font:400 18px/1 Arial,sans-serif;cursor:pointer;padding:0;-webkit-tap-highlight-color:transparent}
.tbb b{position:absolute;top:-6px;right:-7px;background:#c8325f;color:#fff;border-radius:999px;min-width:17px;padding:0 4px;font:700 10.5px/17px var(--body);text-align:center}
.tbb svg{width:19px;height:19px}
.tbb.on{background:#c8325f;color:#fff}
@media (max-width:420px){.top{gap:6px;padding-left:10px;padding-right:10px}.top img{height:26px}.tbb{width:30px;height:30px;font-size:16px}.tbb svg{width:17px;height:17px}}
#starsov .stabs{display:flex;gap:6px;margin:6px 0 2px}
#starsov .stabs button{border:2px solid #c8325f;background:#fff;color:#c8325f;border-radius:999px;padding:6px 14px;font:700 13.5px var(--body);cursor:pointer}
#starsov .stabs button[aria-pressed="true"]{background:#c8325f;color:#fff}
#starsov .mcp{display:flex;gap:4px;width:100%}
#starsov .mcp img{width:50%;aspect-ratio:1;object-fit:cover;border-radius:8px}
#starsov .ac{max-width:440px;margin:0 auto}
#starsov .ac label{display:block;font:700 13px var(--body);color:#283445;margin:12px 0 6px}
#starsov .ac input{width:100%;box-sizing:border-box;border:2px solid #e9cdd8;border-radius:12px;padding:12px 14px;font:400 17px var(--body);color:#283445;background:#fff}
#starsov .ac input:focus{outline:none;border-color:#c8325f}
#starsov .ac .abtn{display:block;width:100%;margin:12px 0 6px;border:0;border-radius:999px;background:#c8325f;color:#fff;padding:13px 16px;font:700 16px var(--body);cursor:pointer}
#starsov .ac .abtn[disabled]{opacity:.55;cursor:default}
#starsov .ac .agh{display:block;width:100%;margin:6px 0;border:2px solid #c8325f;border-radius:999px;background:#fff;color:#c8325f;padding:11px 16px;font:700 15px var(--body);cursor:pointer}
#starsov .ac .alnk{border:0;background:none;color:#283445;text-decoration:underline;font:400 14px var(--body);cursor:pointer;padding:6px 0}
#starsov .ac .afine{color:#6b6070;font:400 12.5px/1.4 var(--body);margin:8px 0 0}
#starsov .ac .aerr{color:#a3285a;background:#fde8ef;border-radius:10px;padding:8px 10px;font:600 13.5px/1.35 var(--body);margin:8px 0 0}
#starsov .ac .aok{color:#1f5d3a;background:#e6f4ec;border-radius:10px;padding:8px 10px;font:600 13.5px/1.35 var(--body);margin:8px 0 0}
'''
i = h.rindex('</style></head>'); h = h[:i] + CSS + h[i:]

ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7"/></svg>'
rep('<nav class="stp" id="stp" aria-label="Steps"></nav></header>',
    '<nav class="stp" id="stp" aria-label="Steps"></nav><div class="tbx"><button type="button" class="tbb" data-mystars aria-label="My stars">★</button>'
    '<button type="button" class="tbb" data-acct aria-label="Your account">' + ICON + '</button></div></header>')

# compact count on the top-bar star button (v110 starSync rewrote every [data-mystars] as "★ My stars N")
rep("document.querySelectorAll('[data-mystars]').forEach(el=>{el.innerHTML='★ My stars'+(n?` <b>${n}</b>`:'');});",
    "document.querySelectorAll('[data-mystars]').forEach(el=>{el.innerHTML=el.classList.contains('tbb')?'★'+(n?`<b>${n}</b>`:''):'★ My stars'+(n?` <b>${n}</b>`:'');});")
# every made card is remembered (this device; + account when signed in)
rep("S.made=true;renderCard();steps();jump('s-card');return;}", "S.made=true;acctSaveMatch();renderCard();steps();jump('s-card');return;}")

JS = r'''/*v111 ACCOUNTS: Supabase email sign-in (public key only); stars + match cards in user_metadata.fym. Lazy + fully guarded.*/
const SB_URL=__SBURL__,SB_KEY=__SBKEY__,SB_JS='https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.45.4/dist/umd/supabase.min.js';
const ACCT={sb:null,user:null,loading:null,dead:false,step:'email',email:'',busy:false,msg:'',err:'',saveT:0,tab:'stars'};
const MCH={k:'fym_matches_v1',mem:null,get(){if(this.mem)return this.mem;let v=null;try{v=JSON.parse(LS.get(this.k)||'null');}catch(e){}this.mem=Array.isArray(v)?v.filter(x=>x&&x.t&&x.m):[];return this.mem;},put(a){this.mem=a.slice(0,50);LS.set(this.k,JSON.stringify(this.mem));}};
function sbStore(){const mem={};return {getItem:k=>{try{return localStorage.getItem(k);}catch(e){return k in mem?mem[k]:null;}},setItem:(k,v)=>{try{localStorage.setItem(k,v);}catch(e){mem[k]=v;}},removeItem:k=>{try{localStorage.removeItem(k);}catch(e){delete mem[k];}}};}
function sbLoad(){if(ACCT.sb)return Promise.resolve(ACCT.sb);if(ACCT.loading)return ACCT.loading;
 ACCT.loading=new Promise((res,rej)=>{try{if(window.supabase&&window.supabase.createClient)return res();const s=document.createElement('script');s.src=SB_JS;s.async=true;s.crossOrigin='anonymous';s.onload=()=>res();s.onerror=()=>rej(new Error('load'));document.head.appendChild(s);setTimeout(()=>rej(new Error('timeout')),15000);}catch(e){rej(e);}})
 .then(()=>{if(!(window.supabase&&window.supabase.createClient))throw new Error('noclient');ACCT.sb=window.supabase.createClient(SB_URL,SB_KEY,{auth:{storage:sbStore(),persistSession:true,autoRefreshToken:true,detectSessionInUrl:false,flowType:'implicit'}});
  try{ACCT.sb.auth.onAuthStateChange((ev,sess)=>{const u=(sess&&sess.user)||null,was=ACCT.user;ACCT.user=u;if(u&&(!was||was.id!==u.id))acctMerge();if(!u&&was){acctTop();}acctRefresh();});}catch(e){}
  return ACCT.sb;}).catch(e=>{ACCT.loading=null;ACCT.dead=true;throw e;});
 return ACCT.loading;}
function acctMeta(){try{return (ACCT.user&&ACCT.user.user_metadata&&ACCT.user.user_metadata.fym)||{};}catch(e){return {};}}
function starRefresh(){document.querySelectorAll('[data-star]').forEach(el=>{const on=STAR.has(el.dataset.star);el.setAttribute('aria-pressed',on);el.textContent=on?'★':'☆';});starSync('',false);}
function acctTop(){const b=document.querySelector('.tbb[data-acct]');if(b){b.classList.toggle('on',!!ACCT.user);b.setAttribute('aria-label',ACCT.user?'Your account (signed in)':'Sign in to save your stars');}}
function acctMerge(){const c=acctMeta(),cs=Array.isArray(c.stars)?c.stars:[],loc=STAR.get();let ch=false;cs.forEach(x=>{if(typeof x==='string'&&!loc.includes(x)){loc.push(x);ch=true;}});if(ch){LS.set(STAR.k,JSON.stringify(loc));starRefresh();}
 const cm=Array.isArray(c.matches)?c.matches:[],lm=MCH.get().slice();cm.forEach(m=>{if(m&&m.t&&m.m&&!lm.some(x=>mkey(x)===mkey(m)))lm.push(m);});lm.sort((a,b)=>(b.at||0)-(a.at||0));MCH.put(lm);acctTop();acctSave(true);trk('account',{x:'signedin'});}
function acctSave(now){if(!ACCT.user||!ACCT.sb)return;clearTimeout(ACCT.saveT);ACCT.saveT=setTimeout(()=>{try{ACCT.sb.auth.updateUser({data:{fym:{stars:STAR.get().slice(0,600),matches:MCH.get().slice(0,50),v:1}}}).then(r=>{if(r&&r.data&&r.data.user)ACCT.user=r.data.user;}).catch(()=>{});}catch(e){}},now?50:1200);}
{const _tog=STAR.tog.bind(STAR);STAR.tog=function(x){const r=_tog(x);if(ACCT.user)acctSave();return r;};}
const mkey=m=>m.t+'|'+m.m+'|'+(m.r||[]).join(',');
function acctSaveMatch(){try{const s=set();if(!s||!S.fav||!S.rpick.length)return;const m={t:s.slug,m:S.fav,r:S.rpick.slice(0,2),at:Date.now()};const a=MCH.get().filter(x=>mkey(x)!==mkey(m));a.unshift(m);MCH.put(a);if(ACCT.user)acctSave();}catch(e){}}
function openMatch(k){const m=MCH.get().find(x=>mkey(x)===k);if(!m)return;const i=D.sets.findIndex(s=>s.slug===m.t);const rk=(m.r||[]).filter(r=>R[r]);if(i<0||!M[m.m]||!rk.length)return;closeStars();
 Object.assign(S,{dmat:null,dkeep:null,ddeck:false,dset:null,door:'tiles',tilesOpen:false});resetFrom(1);S.set=i;S.fav=m.m;if(!S.liked.includes(m.m))S.liked.push(m.m);S.rpick=rk.slice(0,2);rk.forEach(r=>{if(!S.rliked.includes(r))S.rliked.push(r);});S.made=true;renderAll();jump('s-card');trk('account',{x:'reopen'});}
function acctUrl(){let w=window;try{if(window.parent&&window.parent!==window&&window.parent.location.href)w=window.parent;}catch(e){w=window;}let hs='';try{hs=w.location.hash||'';}catch(e){}
 if(!/access_token=|error_code=/.test(hs))return null;const p=new URLSearchParams(hs.replace(/^#/,''));try{w.history.replaceState(null,'',w.location.pathname+w.location.search);}catch(e){}
 if(p.get('error_code')||p.get('error'))return {err:p.get('error_code')==='otp_expired'?'That sign-in link has expired. Send yourself a new one below.':'That sign-in link didn’t work. Send yourself a new one below.'};
 const t={access_token:p.get('access_token'),refresh_token:p.get('refresh_token')};return t.access_token&&t.refresh_token?t:null;}
function acctBoot(){let t=null;try{t=acctUrl();}catch(e){}let has=false;try{for(let i=0;i<localStorage.length;i++){if(/^sb-.*-auth-token$/.test(localStorage.key(i)||''))has=true;}}catch(e){}
 if(t&&t.err){ACCT.err=t.err;openAcct();return;}if(!t&&!has)return;
 sbLoad().then(sb=>t?sb.auth.setSession(t):sb.auth.getSession()).then(r=>{const d=(r&&r.data)||{},u=(d.session&&d.session.user)||d.user||null;if(u&&!ACCT.user){ACCT.user=u;acctMerge();}acctTop();if(t){ACCT.msg='You’re signed in. Your stars are saved to your account.';openAcct();}}).catch(()=>{});}
const emailOk=e=>/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(e);
function acctHTML(){const fine='<p class="afine">We only use your email to sign you in. No spam, and we never share it. Your stars and match cards are saved with your account.</p>';
 const note=(ACCT.err?`<p class="aerr">${esc(ACCT.err)}</p>`:'')+(ACCT.msg?`<p class="aok">${esc(ACCT.msg)}</p>`:'');
 let b;
 if(ACCT.user){const n=STAR.get().length,mc=MCH.get().length;b=`<h2>Your account</h2><p class="shint">Signed in as <b>${esc(ACCT.user.email||'')}</b></p>${note}<p class="shint">★ ${n} star${n===1?'':'s'} and ${mc} match card${mc===1?'':'s'} saved to your account, on every device you sign in on.</p><button type="button" class="abtn" data-mystars>Open My stars</button><button type="button" class="agh" data-acct-out>Sign out</button>`;}
 else if(ACCT.dead){b=`<h2>Save your stars everywhere</h2><p class="aerr">Sign-in isn’t available here right now. Open Find Your Mat-ch on <b>mahjmatchmaker.com</b> to sign in.</p><p class="shint">Your stars still save on this device.</p><button type="button" class="agh" data-acct-retry>Try again</button>`;}
 else if(ACCT.step==='code'){b=`<h2>Check your email</h2><p class="shint">We sent a sign-in email to <b>${esc(ACCT.email)}</b>. Tap the link in it on this device, or enter the 6-digit code from the email:</p>${note}<label for="acode">6-digit code</label><input id="acode" inputmode="numeric" autocomplete="one-time-code" maxlength="10" placeholder="123456"><button type="button" class="abtn" data-acct-verify ${ACCT.busy?'disabled':''}>${ACCT.busy?'Signing you in…':'Sign in'}</button><button type="button" class="alnk" data-acct-resend>Send a new email</button> · <button type="button" class="alnk" data-acct-back>Use a different email</button>${fine}`;}
 else{b=`<h2>Save your stars everywhere</h2><p class="shint">Sign in with your email to keep your ★ stars and match cards on every device. No password needed.</p>${note}<label for="aemail">Your email</label><input id="aemail" type="email" inputmode="email" autocomplete="email" placeholder="you@example.com" value="${esc(ACCT.email)}"><button type="button" class="abtn" data-acct-send ${ACCT.busy?'disabled':''}>${ACCT.busy?'Sending…':'Email me a sign-in code'}</button>${fine}`;}
 return `<div class="sbox" role="dialog" aria-label="Your account"><button type="button" class="sclose" data-starsclose aria-label="Close">✕</button><div class="ac">${b}</div></div>`;}
function acctRefresh(){const ov=document.getElementById('starsov');if(ov&&ov.dataset.k==='acct'){const f=document.activeElement&&document.activeElement.id;ov.innerHTML=acctHTML();if(f){const e=document.getElementById(f);if(e)e.focus();}}}
function openAcct(){let ov=document.getElementById('starsov');if(!ov){ov=document.createElement('div');ov.id='starsov';document.body.appendChild(ov);}ov.dataset.k='acct';ov.innerHTML=acctHTML();trk('account',{x:ACCT.user?'open-in':'open'});
 if(!ACCT.sb&&!ACCT.dead)sbLoad().then(sb=>sb.auth.getSession()).then(r=>{const u=r&&r.data&&r.data.session&&r.data.session.user;if(u&&!ACCT.user){ACCT.user=u;acctMerge();}acctRefresh();}).catch(()=>acctRefresh());
 setTimeout(()=>{const e=document.getElementById(ACCT.step==='code'?'acode':'aemail');if(e&&!ACCT.user)e.focus();},60);}
const sbErr=e=>{const m=String((e&&(e.message||e.error_description))||e||'');if((e&&e.status===429)||/rate|too many|seconds/i.test(m))return 'Too many sign-in emails just now. Please wait a few minutes and try again.';if(/expired|invalid/i.test(m))return 'That code didn’t work or has expired. Check the newest email, or send a new one.';return 'Something went wrong. Please try again.';};
function acctSend(){const e=(document.getElementById('aemail')||{}).value;const em=String(e||ACCT.email||'').trim();ACCT.err='';ACCT.msg='';if(!emailOk(em)){ACCT.err='Please enter a valid email address.';acctRefresh();return;}ACCT.email=em;ACCT.busy=true;acctRefresh();trk('account',{x:'send'});
 sbLoad().then(sb=>sb.auth.signInWithOtp({email:em,options:{emailRedirectTo:'https://www.mahjmatchmaker.com/find-your-match',shouldCreateUser:true}})).then(r=>{ACCT.busy=false;if(r&&r.error){ACCT.err=sbErr(r.error);}else{ACCT.step='code';ACCT.msg='';}acctRefresh();}).catch(()=>{ACCT.busy=false;acctRefresh();});}
function acctVerify(){const c=String((document.getElementById('acode')||{}).value||'').replace(/\D/g,'');ACCT.err='';ACCT.msg='';if(c.length<6){ACCT.err='Enter the 6-digit code from the email.';acctRefresh();return;}ACCT.busy=true;acctRefresh();trk('account',{x:'verify'});
 sbLoad().then(sb=>sb.auth.verifyOtp({email:ACCT.email,token:c,type:'email'})).then(r=>{ACCT.busy=false;if(r&&r.error){ACCT.err=sbErr(r.error);}else{const u=r&&r.data&&(r.data.user||(r.data.session&&r.data.session.user));if(u){ACCT.user=u;acctMerge();}ACCT.step='email';ACCT.msg='You’re signed in. Your stars are saved to your account.';}acctRefresh();}).catch(()=>{ACCT.busy=false;acctRefresh();});}
function acctOut(){trk('account',{x:'signout'});const done=()=>{ACCT.user=null;ACCT.step='email';ACCT.msg='Signed out. Your stars stay on this device.';ACCT.err='';acctTop();acctRefresh();};try{sbLoad().then(sb=>sb.auth.signOut()).then(done,done);}catch(e){done();}}
document.addEventListener('click',e=>{const q=s=>e.target.closest&&e.target.closest(s);let b;
 if(q('[data-acct]')){e.preventDefault();e.stopImmediatePropagation();ACCT.err='';if(!ACCT.user)ACCT.msg='';openAcct();return;}
 if(q('[data-acct-send]')||q('[data-acct-resend]')){e.preventDefault();e.stopImmediatePropagation();if(!ACCT.busy)acctSend();return;}
 if(q('[data-acct-verify]')){e.preventDefault();e.stopImmediatePropagation();if(!ACCT.busy)acctVerify();return;}
 if(q('[data-acct-back]')){e.preventDefault();e.stopImmediatePropagation();ACCT.step='email';ACCT.err='';ACCT.msg='';acctRefresh();return;}
 if(q('[data-acct-out]')){e.preventDefault();e.stopImmediatePropagation();acctOut();return;}
 if(q('[data-acct-retry]')){e.preventDefault();e.stopImmediatePropagation();ACCT.dead=false;openAcct();return;}
 if(b=q('[data-stab]')){e.preventDefault();e.stopImmediatePropagation();ACCT.tab=b.dataset.stab;openStars();return;}
 if(b=q('[data-mopen]')){e.preventDefault();e.stopImmediatePropagation();openMatch(b.dataset.mopen);return;}
},true);
document.addEventListener('keydown',e=>{if(e.key!=='Enter')return;const id=e.target&&e.target.id;if(id==='aemail'){e.preventDefault();if(!ACCT.busy)acctSend();}else if(id==='acode'){e.preventDefault();if(!ACCT.busy)acctVerify();}});
/* v111: My stars sheet gains a "My match cards" tab; the sheet is reachable from the top bar on every step */
function openStars(){const g=starItems(),n=g.t.length+g.m.length+g.r.length,ms=MCH.get().filter(m=>D.sets.some(s=>s.slug===m.t)&&M[m.m]),tab=ACCT.tab==='matches'?'matches':'stars';
 const sec=(lab,arr,f)=>`<h3>${lab}</h3>`+(arr.length?`<div class="sgrid">${arr.map(f).join('')}</div>`:`<p class="sempty">No ${lab.toLowerCase()} starred yet.</p>`);
 const tabs=`<div class="stabs" role="tablist"><button type="button" data-stab="stars" aria-pressed="${tab==='stars'}">★ Stars${n?` (${n})`:''}</button><button type="button" data-stab="matches" aria-pressed="${tab==='matches'}">My match cards${ms.length?` (${ms.length})`:''}</button></div>`;
 const who=ACCT.user?`<p class="shint">Saved to your account (${esc(ACCT.user.email||'')}).</p>`:`<p class="shint">Saved on this device. <button type="button" class="alnk" data-acct style="padding:0;color:#c8325f;font-weight:700">Sign in</button> to keep them on every device.</p>`;
 let body;
 if(tab==='matches'){body=ms.length?`<div class="sgrid">${ms.map(m=>{const i=D.sets.findIndex(s=>s.slug===m.t),s=D.sets[i];return `<button type="button" class="sit" data-mopen="${esc(mkey(m))}"><span class="mcp"><img src="${pile(s)}" alt="" loading="lazy"><img src="${matTh(m.m)}" alt="" loading="lazy"></span><span>${esc(s.name)}</span><small>on ${esc(MN(m.m))}</small></button>`;}).join('')}</div>`:`<p class="sempty">No match cards yet. Make one and it will be saved here.</p>`;}
 else{body=(n?'':'<p class="shint">Tap ☆ on any tile set, mat or rack to save it here.</p>')+
 sec('Tile sets',g.t,r=>`<button type="button" class="sit" data-starst="${r.i}"><img src="${pile(r.s)}" alt="" loading="lazy"><span>${esc(r.s.name)}</span><small>${esc(r.s.maker)}</small>${STB('t',r.s.slug)}</button>`)+
 sec('Mats',g.m,id=>`<button type="button" class="sit" data-starsm="${esc(id)}"><img src="${matTh(id)}" alt="" loading="lazy"><span>${esc(MN(id))}</span><small>${esc(M[id].bn||'')}</small>${STB('m',id)}</button>`)+
 sec('Racks',g.r,id=>{const o=R[id];return `<a class="sit" ${o.u?`href="${esc(o.u)}" target="_blank" rel="noopener"`:''}><img src="${rackSrc(id)}" alt="" loading="lazy" style="object-fit:contain"><span>${esc(shortR(id))}</span><small>${esc(o.bn||'')}${o.u?' · Shop ›':''}</small>${STB('r',id)}</a>`;});}
 const html=`<div class="sbox" role="dialog" aria-label="My stars"><button type="button" class="sclose" data-starsclose aria-label="Close">✕</button><h2>★ My stars</h2>${who}${tabs}${body}</div>`;
 let ov=document.getElementById('starsov');if(!ov){ov=document.createElement('div');ov.id='starsov';document.body.appendChild(ov);}ov.dataset.k='stars';ov.innerHTML=html;trk('stars',{x:tab+':'+String(tab==='matches'?ms.length:n)});}
'''
JS = JS.replace('__SBURL__', json.dumps(SB['url'])).replace('__SBKEY__', json.dumps(SB['anon_key']))
assert SB['anon_key'].startswith('sb_publishable_') or SB['anon_key'].startswith('eyJ'), 'only the public key may ship'
rep('function tileBtn(', JS + 'function tileBtn(')
# boot: restore a session / read a sign-in link after the first render; the top-bar star count on load
rep('</script>\n</body>', 'try{setTimeout(()=>{try{starSync(\'\',false);acctTop();acctBoot();}catch(e){}},400);}catch(e){}\n</script>\n</body>') if h.count('</script>\n</body>') == 1 else None
if 'acctBoot();}catch' not in h:
    j = h.rindex('</script>')
    h = h[:j] + "\ntry{setTimeout(()=>{try{starSync('',false);acctTop();acctBoot();}catch(e){}},400);}catch(e){}\n" + h[j:]
open(OUT, 'w').write(h)
print('patch111 ok', OUT)
