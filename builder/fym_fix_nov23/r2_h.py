"""FYM round 2h (Tiffany Nov 23 10:34pm): story-size match cards keep Instagram's safe zones (nothing in the top 250px or
bottom 340px): header starts at 280, footer sits 370 up, phone view starts at 290 and keeps its code pill above the
bottom zone. Applied in place to site-app/fym-r2-preview/index.html on Nov 23 (string swaps below)."""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
if 'R2H' in s: print('already applied'); sys.exit()
for a, b in [("let y=STORY?200:40;", "let y=STORY?280:40;/*R2H top safe zone*/"),
             ("const fh=60,fy=H-fh-(STORY?210:30)", "const fh=60,fy=H-fh-(STORY?370:30)/*R2H story bottom safe zone*/"),
             ("py=STORY?150:44,", "py=STORY?290:44,"),
             ("Math.min(sw-f(36),H-yy-textH))", "Math.min(sw-f(36),(STORY?H-400:H)-yy-textH))")]:
    if a in s: s = s.replace(a, b)
open(p, 'w', encoding='utf-8').write(s); print('ok')
