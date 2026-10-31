"""FYM v107 = public "Version 1.9.2" (Oct 31) code patch, applied to ANY copy of the v106 index
(b106 app index, pub106 artifact index, site-app/fym-v106 website index): same code, different data/paths.
1. Logo grid breathing room (Tiffany Oct 31 10:36am): wordmark logos that sit on the brand-name text (Mahjong Row & Co.,
   My Fair Mahjong, Oh My Mahjong, + any listed in WM) shrink a little; every card gets a gap between logo and name;
   "Mahjong Row / & Co." breaks cleanly; LSF card reads "LoveShackFancy ×" / "Oh My Mahjong".
2. v106 QA: (a) a step-2 searched mat only stays on top if it passes the active brand / colour filters;
   (b) Noli June option label = plain "Noli June (N)" (Tiffany 10:41am: no terms in the dropdown); (c) Noli June $100 minimum in the in-app shop list
   (NOT on the card image: rule 7);
   (d) '(retired)' stripped from the card MAT tag (mName) and the line under "It's a match!".
3. Aerial tile inset width = ONE CSS variable --onmat-w (Tiffany picked C = 40%, Oct 31). Change it in ONE place: ONMAT_W below.
Usage: python3 patch107.py <in index.html> <out index.html>"""
import sys
ONMAT_W = '40%'
SRC, OUT = sys.argv[1:3]
h = open(SRC).read()
def rep(a, b, n=1):
    global h
    c = h.count(a); assert c == n, (c, a[:90]); h = h.replace(a, b)
# 1. logos
rep("const one=m=>`<button type=\"button\" class=\"blg\"",
    "const WM=new Set(['Mahjong Row & Co.','My Fair Mahjong','Oh My Mahjong','Middle & Main Mahjong','Mahj Squad','Mac + Miller Mahjong']),BNM={'Mahjong Row & Co.':'Mahjong Row<br>&amp; Co.','LoveShackFancy x Oh My Mahjong':'LoveShackFancy \\u00d7<br>Oh My Mahjong'};/*v107 logo breathing room (Tiffany Oct 31)*/\n const one=m=>`<button type=\"button\" class=\"blg\"")
rep("<img src=\"${BLOGO[m]}\" alt=\"\" loading=\"lazy\">", "<img src=\"${BLOGO[m]}\" alt=\"\" loading=\"lazy\"${WM.has(m)?' class=\"wm\"':''}>")
rep("`<span class=\"blt\">${esc(m)}</span>`", "`<span class=\"blt\">${BNM[m]||esc(m)}</span>`")
rep("${BLOGO[m]?`<b>${esc(m)}</b>`:''}", "${BLOGO[m]?`<b>${BNM[m]||esc(m)}</b>`:''}")
CSS = (".tgrid .blg .bli{margin-bottom:9px}.tgrid .blg .bli img.wm{max-width:80%;max-height:76%}"
       ".tgrid .blg b{line-height:1.22}.tgrid .blgrid.np .blg .blt{font-size:13px;line-height:1.25}"
       f":root{{--onmat-w:{ONMAT_W}}}"
       ".cmp.aer .sbx,.deck.aer .sbx{top:30%}"  # aerial: lift the side X/heart so the 40% tile circle never covers the heart
       # v107 QA (website 544px iframe, short decks): size + place the circle against the MAT (the photo box's shorter side, the mat
       # is object-fit:contain), not the box width, so on short/wide decks it stays 40% of the mat, sits on the mat's bottom-right
       # corner and never reaches the side heart. On a phone (square box) it is the same 40% she picked.
       ".scard .ph:has(> .onmat){container-type:size}"
       f".scard .ph > .onmat{{--s:min(100cqw,100cqh);width:calc(var(--s)*{float(ONMAT_W.rstrip('%'))/100:g});"
       "right:calc((100cqw - var(--s))/2 + var(--s)*.03);bottom:calc((100cqh - var(--s))/2 + var(--s)*.03)}\n")
i = h.rindex('</style></head>'); h = h[:i] + CSS + h[i:]
# 2a. searched mat respects later filters
rep("if(S.mfront&&S.mfset===S.set&&M[S.mfront]&&!S.seen[S.mfront])ids=[S.mfront,",
    "if(S.mfront&&S.mfset===S.set&&M[S.mfront]&&!S.seen[S.mfront]&&((!f.brand&&!f.fam.length)||ids.includes(S.mfront)))/*v107 searched mat obeys brand/colour filters*/ids=[S.mfront,")
# 2b. shorter option label
rep("${BMIN[b]?' \\u00b7 '+BMIN[b]:''}", "")  # Tiffany Oct 31 10:41am: no terms in the brand dropdown, just "Noli June (N)"
# 2c. Noli June minimum on the card + shop list
# (card IMAGE code line stays "Use code MAHJMATCH to save": CLAUDE.md rule 7, no % or terms on the card)
rep("${o.dc?`<a class=\"dc\" href=\"${esc(o.dc)}\" target=\"_blank\" rel=\"noopener\">Discount code ›</a>`:''}",
    "${o.dc?`<a class=\"dc\" href=\"${esc(o.dc)}\" target=\"_blank\" rel=\"noopener\">Discount code ›</a>`:''}${BMIN[o.bn]?`<em class=\"alt\">${BMIN[o.bn]} with code MAHJMATCH</em>`:''}")
# (text-me list format is fixed by gate [54]; the $100 line lives in the on-screen shop list only)
# 2d. '(retired)' out of the card MAT tag and the "It's a match!" line
rep("const mName=(M[S.fav].dn||M[S.fav].n).replace(", "const mName=(M[S.fav].dn||M[S.fav].n).replace(/\\s*\\(retired\\)/i,'').replace(")
rep("${esc(s.name)} + ${esc(M[S.fav].n)}. Pick your view", "${esc(s.name)} + ${esc(M[S.fav].n.replace(/\\s*\\(retired\\)/i,''))}. Pick your view")
# 2e. (v107 QA) '(retired)' out of the "Shop your match" rows and the "Text or email me this list" text (the Retired button stays)
rep("const nm=T[id]?set().name:R[id]?o.n:o.n;", "const nm=String(T[id]?set().name:o.n).replace(/\\s*\\(retired\\)/i,'')/*v107 no (retired) on the card screen*/;")
rep("My mahjong match: ${s.name} + ${M[S.fav].n}\\n", "My mahjong match: ${s.name} + ${M[S.fav].n.replace(/\\s*\\(retired\\)/i,'')}\\n")
rep("const nm=T[id]?s.name:R[id]?shortR(id):o.n;","const nm=String(T[id]?s.name:R[id]?shortR(id):o.n).replace(/\\s*\\(retired\\)/i,'')/*v107*/;")
# 3. aerial inset width variable
rep("width:27%;aspect-ratio:1", "width:var(--onmat-w,40%);aspect-ratio:1")
rep('Version 1.9.1', 'Version 1.9.2', 2)
open(OUT, 'w').write(h); print('ok', len(h))
