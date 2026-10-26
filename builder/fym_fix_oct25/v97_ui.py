"""FYM v97 (Version 1.1) UI fixes from docs/MATCH-INBOX.md (Oct 26 evening). Idempotent. Usage: v97_ui.py <build>
1. Sticky search (Tiffany 5:37pm, found testing): a searched mat (S.mfront) stayed at the front of EVERY later deck, because
   resetFrom(level<=1) cleared S.seen but never S.mfront. Now: resetFrom(<=1) and tReset clear mfront; the search remembers the
   set it was searched on (S.mfset) and matDeck only fronts it for that set. Gate [82].
2. Accent-blind search (Tiffany 5:53pm: "soiree" found nothing, "soir" found SOIRÉE). Every search box (mat-door mdq, tile tsq,
   in-deck mat msq, rack rsq) folds accents + case on BOTH sides with NRM(). Gate [83].
3. Mat-door parity for Add racks (Tiffany Oct 26): on "Start with a mat", the chosen suitor tile set gets a big "Add racks ›"
   right under it (same as v95 tiles door), and tapping the chosen tile set card = Add racks. Gate [84]."""
import sys
P = sys.argv[1] + '/index.html'; h = open(P).read(); n = 0
def rep(old, new, count=1, done=None):
    global h, n
    if done and done in h: return
    c = h.count(old); assert c == count, (old[:80], c, count)
    h = h.replace(old, new); n += 1
# 1. sticky search
rep("function resetFrom(level){if(level<=1){Object.assign(S,{seen:{},",
    "function resetFrom(level){if(level<=1){Object.assign(S,{mfront:null,mfset:null,seen:{},", done='Object.assign(S,{mfront:null,mfset:null,')
rep("const tReset=()=>{S.tseen={};", "const tReset=()=>{S.mfront=null;S.mfset=null;S.tseen={};", done='const tReset=()=>{S.mfront=null;')
rep("if(M[id]){S.mfront=id;delete S.seen[id];", "if(M[id]){S.mfront=id;S.mfset=S.set;delete S.seen[id];", done='S.mfront=id;S.mfset=S.set;')
rep("if(S.mfront&&M[S.mfront]&&!S.seen[S.mfront])ids=", "if(S.mfront&&S.mfset===S.set&&M[S.mfront]&&!S.seen[S.mfront])ids=", done='S.mfset===S.set&&M[S.mfront]')
# 2. accent-blind search
NRM = "/*v97 accent-blind search*/const NRM=x=>String(x==null?'':x).normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').toLowerCase();"
rep("function colorPool(){", NRM + "function colorPool(){", done='/*v97 accent-blind search*/')
rep("const v=e.target.value.trim().toLowerCase(),", "const v=NRM(e.target.value.trim()),", count=4, done='const v=NRM(e.target.value.trim()),')
rep("const s=(M[id].n+' '+(M[id].bn||'')).toLowerCase();", "const s=NRM(M[id].n+' '+(M[id].bn||''));", count=2, done="const s=NRM(M[id].n+' '+(M[id].bn||''));")
rep("const h=(s.name+' '+s.maker).toLowerCase();", "const h=NRM(s.name+' '+s.maker);", done="const h=NRM(s.name+' '+s.maker);")
rep("const s=(R[id].n+' '+(R[id].bn||'')).toLowerCase();", "const s=NRM(R[id].n+' '+(R[id].bn||''));", done="const s=NRM(R[id].n+' '+(R[id].bn||''));")
rep("(M[a].n.toLowerCase().startsWith(toks[0])?0:1)-(M[b].n.toLowerCase().startsWith(toks[0])?0:1)",
    "(NRM(M[a].n).startsWith(toks[0])?0:1)-(NRM(M[b].n).startsWith(toks[0])?0:1)", done="(NRM(M[a].n).startsWith(toks[0])")
rep("(R[a].n.toLowerCase().startsWith(toks[0])?0:1)-(R[b].n.toLowerCase().startsWith(toks[0])?0:1)",
    "(NRM(R[a].n).startsWith(toks[0])?0:1)-(NRM(R[b].n).startsWith(toks[0])?0:1)", done="(NRM(R[a].n).startsWith(toks[0])")
# 3. mat-door Add racks under the chosen tile set + tap the chosen tile set = Add racks
rep("const acts=pk?`<div class=\"acts pk\"><button type=\"button\" class=\"pill\" data-tunpeek>",
    "const acts=pk?`<div class=\"acts pk\"><button type=\"button\" class=\"go pkgo\" data-tadd=\"${pk.i}\">Add racks ›</button><button type=\"button\" class=\"pill\" data-tunpeek>",
    done='class="go pkgo" data-tadd=')
rep("if(q('[data-tyes]')){tfly(true);return;}",
    "/*v97 tap chosen tiles = Add racks*/if(S.tpeek!=null&&q('#s-tiles .deck.t .scard.tk')&&!q('button')){const g=document.querySelector('.acts.pk [data-tadd]');if(g)g.click();return;}if(q('[data-tyes]')){tfly(true);return;}",
    done='/*v97 tap chosen tiles = Add racks*/')
css = "#s-tiles .deck.t .peekbar+.scard.tk{cursor:pointer}"
if css not in h:
    a = ".acts.pk{padding-left:0;flex-wrap:wrap;gap:8px}"; assert h.count(a) == 1; h = h.replace(a, a + " " + css, 1); n += 1
open(P, 'w').write(h); print('v97 ui patches', n)
