"""FYM v71 UI part 4 (render QA): Story 9:16 card fills the frame inside Instagram's safe zones; 'mat-ch' never breaks at the hyphen."""
import sys, json
P = sys.argv[1] + '/index.html'; h = open(P).read(); i = h.index('const D=') + 8; _, end = json.JSONDecoder().raw_decode(h[i:]); end += i
H, data, t = h[:i], h[i:end], h[end:]
def rep(s, a, b):
    assert s.count(a) == 1, a[:80]; return s.replace(a, b)
H = rep(H, ".deck.r .peekbar span{background:#7a6a85}\n</style>", ".deck.r .peekbar span{background:#7a6a85}\n.nw{white-space:nowrap}\n</style>")
t = rep(t, "head(2,'Your mat-ch'", "head(2,'Your <span class=\"nw\">mat-ch</span>'")
t = rep(t, "let y=40;", "const STORY=H/W>1.6;let y=STORY?200:40;")
t = rep(t, "const fh=62,fy=H-fh-30;", "const fh=62,fy=H-fh-(STORY?210:30);")
t = rep(t, "const ms=Math.min(W*(pin?.8:.74),availH*.86)", "const ms=STORY?Math.min(W*.86,availH*.7):Math.min(W*(pin?.8:.74),availH*.86)")
t = rep(t, "const ly2=pin?Math.min(ly,Math.max(cy+r,ry+ch)+70):ly;", "const ly2=pin&&!STORY?Math.min(ly,Math.max(cy+r,ry+ch)+70):ly;")
open(P, 'w').write(H + data + t); print('v71 ui4 patched')
