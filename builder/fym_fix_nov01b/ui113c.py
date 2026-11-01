"""v113 QA round 2 (Nov 1):
 1. Links on a swipe card (Dapper 'See the difference', 'Also available …') open with a MOUSE click too: the card's swipe / zoom
    handlers never see pointerdown / mousedown / touchstart / click that start on a link, so no drag starts and the click is not swallowed.
 4. WebKit iPhone: the top step nav (.stp, ~289px) never shrank and made the page slide sideways (live 1.12 too): min-width:0.
 3. 'Also available …' with a variant URL (o.altu) is a link to that product (Funny Lady -> the bordered version), card + shop list.
Idempotent. Usage: python3 ui113c.py <build_dir>"""
import sys
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
if '/*v113c*/' in h: print('ui113c already'); sys.exit()
def rep(a, b, n=1):
    global h
    assert h.count(a) == n, (h.count(a), a[:100]); h = h.replace(a, b)
rep("c.querySelectorAll('button.hb').forEach(b=>b.addEventListener('pointerdown',e=>e.stopPropagation()));",
    "c.querySelectorAll('button.hb').forEach(b=>b.addEventListener('pointerdown',e=>e.stopPropagation()));/*v113c*/c.querySelectorAll('a[href]').forEach(a=>['pointerdown','mousedown','touchstart','click'].forEach(ev=>a.addEventListener(ev,e=>e.stopPropagation(),{passive:true})));")
rep("${mat&&o.alt?`<em class=\"alt\">${esc(o.alt)}</em>`:''}", "${mat&&o.alt?(o.altu?`<a class=\"alt altl\" href=\"${esc(o.altu)}\" target=\"_blank\" rel=\"noopener\">${esc(o.alt)} ›</a>`:`<em class=\"alt\">${esc(o.alt)}</em>`):''}")
rep("${M[id]&&o.alt?`<em class=\"alt\">${esc(o.alt)}</em>`:''}", "${M[id]&&o.alt?(o.altu?`<a class=\"alt altl\" href=\"${esc(o.altu)}\" target=\"_blank\" rel=\"noopener\">${esc(o.alt)} ›</a>`:`<em class=\"alt\">${esc(o.alt)}</em>`):''}")
i = h.index('</style>'); h = h[:i] + 'a.altl{display:block;font-style:normal;text-decoration:underline;color:#1f3a6b}' + '.top .stp{min-width:0;flex:1 1 auto;overflow-x:auto;scrollbar-width:none}.top .stp::-webkit-scrollbar{display:none}/*v113c: WebKit iPhone step nav (289px) would not shrink and pushed the page sideways*/' + h[i:]
open(P, 'w').write(h); print('ui113c ok')
