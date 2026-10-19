"""Color-wheel brand mark concepts (Oct 19): secondary marks that bring the color wheel into the flame-heart.
Navy + pink stay primary; these are for highlights, stickers, Find Your Match, color content."""
import os
from playwright.sync_api import sync_playwright
R='/home/claude/mahjmatchmaker-data/'
FL="M120 222C70 222 38 188 38 146C38 118 50 98 64 82C66 98 73 108 84 113C82 78 102 44 152 20C142 50 152 70 168 90C186 112 202 128 202 152C202 192 168 222 120 222Z"
HT="M120 192C95 175 86 162 86 148C86 135 96 126 107 126C113 126 117 129 120 134C123 129 127 126 133 126C144 126 154 135 154 148C154 162 145 175 120 192Z"
NAVY='#054689'; PINK='#f56c8c'
WHEEL='conic-gradient(from 0deg,#f7a1a8,#fbc39a,#fde59a,#c7e6a3,#a6dccb,#a9cdf0,#b9b5ee,#dcb3e8,#f7a1a8)'
WHEEL_B='conic-gradient(from 0deg,#ef5a6f,#f59a4a,#f5cf3d,#8cc85a,#3fb7a0,#4a8fe0,#7b6be0,#c062c9,#ef5a6f)'
def clip(path): return f"path('{path}')"
def mark(kind):
    s=380; k=s/240
    sp=lambda p: ' '.join(str(round(float(t)*k,1)) if t.replace('.','',1).isdigit() else t for t in p.replace('C',' C ').replace('M',' M ').replace('Z',' Z ').split())
    fl, ht = sp(FL), sp(HT)
    if kind=='A':   # pastel wheel flame, navy heart
        return f'<div style="width:{s}px;height:{s}px;position:relative"><div style="position:absolute;inset:0;background:{WHEEL};clip-path:{clip(fl)}"></div><svg width="{s}" height="{s}" style="position:absolute;inset:0"><path d="{ht}" fill="{NAVY}"/></svg></div>'
    if kind=='B':   # navy flame, color wheel heart
        return f'<div style="width:{s}px;height:{s}px;position:relative"><svg width="{s}" height="{s}" style="position:absolute;inset:0"><path d="{fl}" fill="{NAVY}"/></svg><div style="position:absolute;inset:0;background:{WHEEL_B};background-position:center;clip-path:{clip(ht)}"></div></div>'
    if kind=='C':   # color wheel ring seal, navy flame + pink heart inside
        return f'''<div style="width:{s}px;height:{s}px;border-radius:50%;background:{WHEEL};display:flex;align-items:center;justify-content:center">
<div style="width:{s-64}px;height:{s-64}px;border-radius:50%;background:#fbf6ef;display:flex;align-items:center;justify-content:center">
<svg width="{s-110}" height="{s-110}" viewBox="0 0 240 240"><path d="{FL}" fill="{NAVY}"/><path d="{HT}" fill="{PINK}"/></svg></div></div>'''
    if kind=='D':   # flame built from 8 color-chip slices
        return f'<div style="width:{s}px;height:{s}px;position:relative"><div style="position:absolute;inset:0;background:conic-gradient(from 0deg at 50% 62%,#f7a1a8 0 12.5%,#fbc39a 0 25%,#fde59a 0 37.5%,#c7e6a3 0 50%,#a6dccb 0 62.5%,#a9cdf0 0 75%,#b9b5ee 0 87.5%,#dcb3e8 0 100%);clip-path:{clip(fl)}"></div><svg width="{s}" height="{s}" style="position:absolute;inset:0"><path d="{ht}" fill="#fff"/><path d="{ht}" fill="none" stroke="{NAVY}" stroke-width="6"/></svg></div>'
labels={'A':'A · Wheel flame<br><small>pastel color wheel fills the flame, navy heart</small>',
        'B':'B · Wheel heart<br><small>our navy flame, the heart becomes the color wheel</small>',
        'C':'C · Color wheel seal<br><small>classic flame-heart inside a color wheel ring (sticker / badge)</small>',
        'D':'D · Chip flame<br><small>flame made of 8 color chips, like our color cards</small>'}
cells=''.join(f'<div class="c">{mark(k)}<p>{labels[k]}</p></div>' for k in 'ABCD')
html=f'''<!doctype html><html><head><style>@font-face{{font-family:Capra;src:url('file://{R}scripts/social/tileprofile/fonts/Caprasimo.ttf')}}
body{{margin:0;width:1800px;background:#f6e9df;font:22px Georgia;color:{NAVY}}}h1{{font-family:Capra;font-weight:400;font-size:64px;text-align:center;margin:50px 0 6px}}
.s{{text-align:center;font-size:24px;margin-bottom:30px}}.g{{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;padding:0 40px 60px}}
.c{{background:#fff;border-radius:28px;padding:40px 20px 28px;display:flex;flex-direction:column;align-items:center}}p{{text-align:center;font-weight:bold;line-height:1.3}}small{{font-weight:normal;font-size:18px}}</style></head>
<body><h1>Color wheel marks</h1><div class="s">Navy + pink stay the main logo. These are secondary marks to bring the color wheel in.</div><div class="g">{cells}</div></body></html>'''
out=R+'assets/brand/colorwheel-mark-concepts.png'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1800,'height':800}); pg.set_content(html); pg.wait_for_timeout(400)
    pg.screenshot(path=out,full_page=True); b.close()
print(out)
