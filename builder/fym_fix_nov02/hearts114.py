"""v114 STARS BECOME HEARTS (Tiffany Nov 3 2:58pm, reversible):
 - every visible star becomes a heart: 'My stars' -> 'My hearts', the star/empty-star glyphs -> filled/empty hearts
   (top bar, item toggles, sheet, account sheet copy, shop-list toggles, tour);
 - every mat and rack a person hearts while swiping is saved to My hearts automatically (deduped; syncs to the account
   when signed in through the existing STAR.tog wrapper);
 - each item in the My hearts sheet shows an x that removes it (the sheet re-renders);
 - account prompt under the match card: signed out = button that opens the existing sign-in sheet,
   signed in = 'Saved to your account (check)'. Not a gate on making the card.
Storage keys stay the same (fym_stars_v1, user_metadata.fym.stars) so nobody loses what they saved. Gate [153]. Idempotent."""
import sys, os, json
P = sys.argv[1]; P = P if P.endswith('.html') else os.path.join(P, 'index.html'); h = open(P).read()
if '/*v114 hearts*/' in h: print('hearts114 already'); sys.exit()
i = h.index('const D=') + 8; _, e = json.JSONDecoder().raw_decode(h, i)
head, app = h[:e], h[e:]
def rep(a, b, n=1):
    global app
    c = app.count(a); assert (c == n if n else c >= 1), (c, a[:90]); app = app.replace(a, b)
rep("on?'★':'☆'", "on?'♥':'♡'", 0)
rep("'★'+(n?", "'♥'+(n?")
rep("'★ My stars'", "'♥ My hearts'")
rep('data-mystars>★ My stars', 'data-mystars>♥ My hearts')
_tb='data-mystars aria-label="My stars">★</button>'; assert head.count(_tb) == 1; head = head.replace(_tb, 'data-mystars aria-label="My hearts">♥</button>')
rep('<h2>★ My stars</h2>', '<h2>♥ My hearts</h2>', 0)
rep('My stars', 'My hearts', 0)
rep('starred yet', 'hearted yet', 0)
rep('★ Stars${', '♥ Hearts${')
rep("★ ${n} star${n===1?'':'s'}", "♥ ${n} heart${n===1?'':'s'}")
rep('Save your stars everywhere', 'Save your hearts everywhere', 0)
rep('keep your ★ stars', 'keep your ♥ hearts')
rep('Your stars ', 'Your hearts ', 0)
rep('save your stars', 'save your hearts', 0)
rep("Tap ☆ on any tile set, mat or rack to save it here.", "Every mat and rack you ♥ while swiping is saved here. Tap ♡ on a tile set to add it.", 0)
rep('under ★ at the top', 'under ♥ at the top')
# auto-save hearted swipes
rep("if(yes&&!S.liked.includes(id))S.liked.push(id);", "if(yes&&!S.liked.includes(id))S.liked.push(id);if(yes)HSAVE('m:'+id);")
rep("if(yes&&!S.rliked.includes(id))S.rliked.push(id);", "if(yes&&!S.rliked.includes(id))S.rliked.push(id);if(yes)HSAVE('r:'+id);")
# account prompt under the card
rep('<button type="button" class="big gh shl" data-shoplist>Text or email me this list</button></div>',
    '<button type="button" class="big gh shl" data-shoplist>Text or email me this list</button><div class="acp">${ACPH()}</div></div>')
assert app.count('★') == 0 and app.count('☆') == 0, [app[k-60:k+20] for k in [app.find('★'), app.find('☆')] if k >= 0]
js = r"""<script>/*v114 hearts*/
function HSAVE(x){try{if(!STAR.has(x)){STAR.tog(x);starSync(x,true);}}catch(e){}}
function ACPH(){return (typeof ACCT!=='undefined'&&ACCT.user)?'<p class="acok">Saved to your account ✓</p>':'<button type="button" class="acbtn" data-acct>Save your match cards and hearts to every device: sign in with your email</button>';}
(function(){const _t=acctTop;acctTop=function(){_t.apply(this,arguments);document.querySelectorAll('.acp').forEach(el=>{el.innerHTML=ACPH();});};
 const _o=openStars;openStars=function(){_o.apply(this,arguments);const ov=document.getElementById('starsov');if(!ov||ov.dataset.k!=='stars')return;
  ov.querySelectorAll('.stb[data-star]').forEach(el=>{el.classList.add('hrm');el.textContent='✕';el.setAttribute('aria-label','Remove from My hearts');});};
 window.addEventListener('click',e=>{const b=e.target.closest&&e.target.closest('#starsov .stb.hrm[data-star]');if(!b)return;setTimeout(()=>{try{openStars();}catch(_){}},0);},true);
 window.addEventListener('keydown',e=>{if((e.key==='Enter'||e.key===' ')&&e.target.closest&&e.target.closest('#starsov .stb.hrm[data-star]'))setTimeout(()=>{try{openStars();}catch(_){}},0);},true);})();
</script>"""
css = """.stb.hrm{font:700 13px/1 var(--body);color:#76687f}.acp{margin:10px 0 0;text-align:center}.acbtn{border:0;background:none;color:#c8325f;font:600 14px/1.4 var(--body);text-decoration:underline;cursor:pointer;padding:6px 4px}.acok{margin:0;color:#3d7a52;font:600 14px/1.4 var(--body)}"""
h = head + app
h = h.replace('</style>', css + '</style>', 1)
j = h.rindex('</body>') if '</body>' in h else len(h); h = h[:j] + js + h[j:]
open(P, 'w').write(h); print('hearts114 ok')
