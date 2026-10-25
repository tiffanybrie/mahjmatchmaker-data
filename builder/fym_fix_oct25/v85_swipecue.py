"""FYM v85 (Tiffany Oct 25 14:35): her husband looked at the middle of the mat and never saw the swipe line under it. Put the cue
FRONT AND CENTER: the tour's moving-finger swipe overlay (.swh, ✕ left, ♥ right, a dot sliding left and right) now also shows on the
first card of every deck (mats, racks, and the mat-door tile swiper) for anyone not in the tour, with a navy label on the card:
"Swipe right ♥ if you love it" / "Swipe left ✕ if it’s not the one". It goes away for good after the first swipe or ✕/♥ tap
(localStorage fym_swiped). Also: the mat-door tile swiper gets the same hint line + 'Not the one' / 'Love it' labels (QA v84 note).
Usage: python3 v85_swipecue.py <build_dir>  (in place, after v84)"""
import sys
P = sys.argv[1] + '/index.html'; h = open(P).read()
def rep(a, b, n=1):
    global h
    assert h.count(a) == n, (a[:80], h.count(a)); h = h.replace(a, b)
# 1. first swipe marks the cue as learned
rep("function decide(k,yes){const q=queue(k);if(!q.length)return;",
    "function decide(k,yes){const q=queue(k);if(!q.length)return;swLearned();")
rep("function tdecide(yes){const q=tq();if(!q.length)return;",
    "function tdecide(yes){const q=tq();if(!q.length)return;swLearned();")
# 2. the cue itself (reuses the tour's .swh overlay) + an observer so every render path gets it
JS = ("/* v85: swipe cue on the first card for people who skip the tour (Tiffany Oct 25) */"
      "function swLearned(){LS.set('fym_swiped','1');document.querySelectorAll('.swh.cue').forEach(e=>e.remove());}"
      "function swCue(){if(TOUR.on||TOUR.prompt||$('tourq')||LS.get('fym_swiped'))return;['top-m','top-r','top-t'].forEach(id=>{const c=$(id);"
      "if(!c||!c.parentElement||c.parentElement.querySelector('.swh'))return;const w=document.createElement('div');w.className='swh cue';"
      "w.setAttribute('aria-hidden','true');w.innerHTML='<b class=\"swl\">Swipe right \\u2665 if you love it<br>Swipe left \\u2715 if it\\u2019s not the one</b>"
      "<span class=\"swx\">\\u2715</span><i></i><span class=\"swy\">\\u2665</span>';c.parentElement.appendChild(w);});}"
      "if(typeof MutationObserver!=='undefined'){let swq=0;new MutationObserver(()=>{if(swq)return;swq=requestAnimationFrame(()=>{swq=0;swCue();});}).observe(document.getElementById('app'),{childList:true,subtree:true});}")
rep("function tourNext(){", JS + "function tourNext(){")
# 3. CSS: label pill on the card, a bit above the finger row
css = ".swh .swx{color:#7a6a85}.swh .swy{color:var(--pink)}"
rep(css, css + " .swh.cue{top:46%} .swh .swl{position:absolute;left:50%;bottom:34px;transform:translateX(-50%);background:var(--navy);color:#fff;"
    "font:700 13px/1.35 var(--body);padding:8px 14px;border-radius:14px;white-space:nowrap;text-align:center;box-shadow:0 6px 16px rgba(5,40,90,.28)}")
# 4. mat-door tile swiper: same hint line + labels as the mat/rack decks (v84)
rep("`<div class=\"acts\"><button type=\"button\" class=\"no\" data-tno aria-label=\"No thanks\" ${q.length?'':'disabled'}>✕</button>"
    "<button type=\"button\" class=\"yes\" data-tyes aria-label=\"Love\" ${q.length?'':'disabled'}>♥</button></div>`",
    "`${q.length?'<p class=\"swhint\">Swipe right ♥ if you love it · swipe left ✕ if it’s not the one</p>':''}<div class=\"acts\">"
    "<span class=\"ab\"><button type=\"button\" class=\"no\" data-tno aria-label=\"No thanks\" ${q.length?'':'disabled'}>✕</button><small>Not the one</small></span>"
    "<span class=\"ab\"><button type=\"button\" class=\"yes\" data-tyes aria-label=\"Love\" ${q.length?'':'disabled'}>♥</button><small>Love it</small></span></div>`")
open(P, 'w').write(h); print('ok')
