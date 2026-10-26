"""FYM v95: 'Add racks ›' right under the chosen (suitor) mat + tapping the chosen mat goes to racks.
Tiffany Oct 26 10:25am: testers pick a suitor, it shows below, they tap that mat expecting the next step.
1) acts('m') while S.peek: a big 'Add racks ›' (data-mock = same action as the tray button) above the back/remove pills.
2) bindCard('m') while S.peek: a single tap on the chosen mat (not a double-tap zoom, not while zoomed, not on a
   button) clicks that button. Idempotent. Gate [69]. Usage: v95_addracks.py <build>"""
import sys
P = sys.argv[1] + '/index.html'; h = open(P).read(); n = 0
o1 = "function acts(k){if(k==='m'&&S.peek)return `<div class=\"acts pk\"><button type=\"button\" class=\"pill\" data-unpeek>"
n1 = ("function acts(k){if(k==='m'&&S.peek)return `<div class=\"acts pk\"><button type=\"button\" class=\"go pkgo\" data-mock=\"${esc(S.peek)}\">Add racks ›</button>"
      "<button type=\"button\" class=\"pill\" data-unpeek>")
if 'class="go pkgo"' not in h:
    assert h.count(o1) == 1, h.count(o1); h = h.replace(o1, n1); n += 1
o2 = "function bindCard(k){const c=$('top-'+k);if(!c)return;"
n2 = (o2 + "if(k==='m'&&S.peek&&!c.dataset.pk){c.dataset.pk=1;/* v95: tap the chosen mat = Add racks */"
      "c.addEventListener('click',e=>{if(e.target.closest&&e.target.closest('button'))return;"
      "setTimeout(()=>{const zz=S.zs&&S.zs.mz;if(zz&&zz.s>1)return;if(!S.peek)return;"
      "const g=document.querySelector('.acts.pk [data-mock]');if(g)g.click();},330);});}")
if 'v95: tap the chosen mat' not in h:
    assert h.count(o2) == 1, h.count(o2); h = h.replace(o2, n2); n += 1
css = ".acts.pk .pkgo{flex:1 1 100%;width:100%;height:52px;border:0;border-radius:999px;background:var(--pink);color:#fff;font:700 16px var(--body);cursor:pointer;box-shadow:0 6px 16px rgba(200,50,95,.25)}"
anchor = ".acts.pk{padding-left:0;flex-wrap:wrap;gap:8px}"
if css not in h:
    assert h.count(anchor) == 1; h = h.replace(anchor, anchor + " " + css, 1); n += 1
o3 = "b:'.tray .go[data-mock],.dacts [data-mock],.tray .th button'"
n3 = "b:'.acts.pk [data-mock],.tray .go[data-mock],.dacts [data-mock],.tray .th button'"
if n3 not in h and o3 in h: h = h.replace(o3, n3, 1); n += 1  # tour step 4 highlights the new button first
# 4) Bam Bird rack named only "Mahjong Rack & Pusher Set" (shows as "Racks" on cards). Real listing: Bam Bird
# "Mahjong Rack & Pusher Set", variants White / Blue; this key is the White acrylic set. Name only (photo handled elsewhere).
import json
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
rk = 'www.bambirdboutique.com/white-acrylic-rack-and-pusher-set-set-of-4'
if rk in D['racks'] and D['racks'][rk]['n'] != 'Bam Bird Boutique White Acrylic':
    D['racks'][rk]['n'] = 'Bam Bird Boutique White Acrylic'; n += 1
    h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
open(P, 'w').write(h); print('add-racks patches', n)
