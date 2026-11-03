"""v114 My match cards (Tiffany Nov 3 2:43pm, Claude's default, she's fine either way): keep auto-save, but
 (1) ONE card per tile set: a new mat (or racks) for the same tiles REPLACES that set's card (also on read and on sign-in merge,
     so old duplicates collapse to the newest);
 (2) every card gets a small x remove button with an Undo toast (removals sync to the account when signed in);
 (3) newest first;
 (4) the card's save button says 'Save image / Share' (it downloads / shares the picture; separate from My match cards).
Same signed in (user_metadata.fym via acctSave) and signed out (this device). Gate [150]. Idempotent."""
import sys, os
P = sys.argv[1]; P = P if P.endswith('.html') else os.path.join(P, 'index.html'); h = open(P).read()
if '/*v114 cards*/' in h: print('cards114 already'); sys.exit()
def rep(a, b):
    global h
    assert h.count(a) == 1, (h.count(a), a[:90]); h = h.replace(a, b)
rep("const MCH={k:'fym_matches_v1',mem:null,get(){if(this.mem)return this.mem;let v=null;try{v=JSON.parse(LS.get(this.k)||'null');}catch(e){}this.mem=Array.isArray(v)?v.filter(x=>x&&x.t&&x.m):[];return this.mem;},put(a){this.mem=a.slice(0,50);",
    "/*v114 cards*/function MCH1(a){const o=[],seen=new Set();a.slice().sort((x,y)=>(y.at||0)-(x.at||0)).forEach(x=>{if(x&&x.t&&x.m&&!seen.has(x.t)){seen.add(x.t);o.push(x);}});return o;}/* one card per tile set, newest first */\n"
    "const MCH={k:'fym_matches_v1',mem:null,get(){if(this.mem)return this.mem;let v=null;try{v=JSON.parse(LS.get(this.k)||'null');}catch(e){}this.mem=MCH1(Array.isArray(v)?v.filter(x=>x&&x.t&&x.m):[]);return this.mem;},put(a){this.mem=MCH1(a).slice(0,50);")
rep("const a=MCH.get().filter(x=>mkey(x)!==mkey(m));a.unshift(m);MCH.put(a);", "const a=MCH.get().filter(x=>x.t!==m.t);a.unshift(m);MCH.put(a);")
rep("lm.sort((a,b)=>(b.at||0)-(a.at||0));MCH.put(lm);", "MCH.put(lm);")
rep("""return `<button type="button" class="sit" data-mopen="${esc(mkey(m))}"><span class="mcp"><img src="${pile(s)}" alt="" loading="lazy"><img src="${matTh(m.m)}" alt="" loading="lazy"></span><span>${esc(s.name)}</span><small>on ${esc(MN(m.m))}</small></button>`;""",
    """return `<div class="mcw"><button type="button" class="sit" data-mopen="${esc(mkey(m))}"><span class="mcp"><img src="${pile(s)}" alt="" loading="lazy"><img src="${matTh(m.m)}" alt="" loading="lazy"></span><span>${esc(s.name)}</span><small>on ${esc(MN(m.m))}</small></button><button type="button" class="mrm" data-mrm="${esc(mkey(m))}" aria-label="Remove ${esc(s.name)} on ${esc(MN(m.m))} from My match cards">✕</button></div>`;""")
rep('<button type="button" class="big" data-share>Save / Share my match card</button>', '<button type="button" class="big" data-share>Save image / Share</button>')
js = r"""<script>/*v114 cards: remove + undo*/(function(){let undo=null;
function mtoast(msg,withUndo){let el=document.getElementById('mctoast');if(!el){el=document.createElement('div');el.id='mctoast';el.setAttribute('role','status');el.setAttribute('aria-live','polite');document.body.appendChild(el);}
 el.innerHTML=`<span>${msg}</span>`+(withUndo?'<button type="button" data-mundo>Undo</button>':'');el.hidden=false;clearTimeout(mtoast.t);mtoast.t=setTimeout(()=>{el.hidden=true;undo=null;},6000);}
document.addEventListener('click',e=>{const q=s=>e.target.closest&&e.target.closest(s);let b;
 if(b=q('[data-mrm]')){e.preventDefault();e.stopImmediatePropagation();const k=b.dataset.mrm,a=MCH.get(),m=a.find(x=>mkey(x)===k);if(!m)return;undo=m;MCH.put(a.filter(x=>mkey(x)!==k));
  try{if(ACCT.user)acctSave(true);}catch(_){}ACCT.tab='matches';openStars();mtoast('Match card removed.',true);try{trk('matchrm',{mat:m.m,set:m.t});}catch(_){}return;}
 if(q('[data-mundo]')){e.preventDefault();e.stopImmediatePropagation();if(undo){MCH.put([undo,...MCH.get().filter(x=>x.t!==undo.t)]);try{if(ACCT.user)acctSave(true);}catch(_){}undo=null;if(document.getElementById('starsov')){ACCT.tab='matches';openStars();}}
  const el=document.getElementById('mctoast');if(el)el.hidden=true;return;}},true);})();</script>"""
css = """.mcw{position:relative;min-width:0}.mcw .sit{width:100%}.mrm{position:absolute;top:4px;right:4px;z-index:2;width:26px;height:26px;border-radius:50%;border:0;background:rgba(255,255,255,.95);box-shadow:0 1px 4px rgba(0,0,0,.25);color:#76687f;font:700 13px/26px var(--body);padding:0;cursor:pointer}
#mctoast{position:fixed;left:50%;bottom:calc(24px + env(safe-area-inset-bottom,0px));transform:translateX(-50%);z-index:460;background:#2a2036;color:#fff;border-radius:16px;padding:8px 10px 8px 16px;font:600 14px/1.35 var(--body);display:flex;align-items:center;gap:12px;box-shadow:0 8px 24px rgba(0,0,0,.25)}#mctoast[hidden]{display:none}#mctoast button{border:0;background:#fff;color:#c8325f;border-radius:999px;padding:6px 12px;font:700 13px/1 var(--body);cursor:pointer}"""
h = h.replace('</style>', css + '</style>', 1)
j = h.rindex('</body>') if '</body>' in h else len(h); h = h[:j] + js + h[j:]
open(P, 'w').write(h); print('cards114 ok')
