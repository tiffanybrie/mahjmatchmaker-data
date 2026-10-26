import os
from playwright.sync_api import sync_playwright
F='file:///home/claude/mahjmatchmaker-data/scripts/social/tileprofile/fonts/'
CSS=f'''@font-face{{font-family:Cap;src:url({F}Caprasimo.ttf)}}@font-face{{font-family:Bit;src:url({F}bitter-latin-700-normal.woff2);font-weight:700}}@font-face{{font-family:PF;src:url({F}playfair-display-latin-400-italic.woff2);font-style:italic}}
*{{margin:0;box-sizing:border-box}}body{{width:1080px;height:1920px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 90px}}
.cap{{font-family:Cap;line-height:1.02}}.it{{font:italic 54px/1.3 PF}}.sm{{font:700 34px Bit;letter-spacing:5px}}'''
NAVY='#062a55';PINK='#e0547f';CREAM='#fdf3f3';SOFT='#f9dde6'
TILE='file://'+os.path.abspath('tile.jpg')
C={
'q1':(NAVY,f'<div class="it" style="color:#f7b6c8;font-size:64px;margin-bottom:30px">Presenting…</div><div class="cap" style="font-size:124px;color:#fff">The ever-burning question.</div>'),
'q2':(SOFT,f'<img src="{TILE}" style="width:420px;height:420px;object-fit:cover;border-radius:50%;border:12px solid #fff;box-shadow:0 20px 50px rgba(6,42,85,.25);margin-bottom:70px"><div class="cap" style="font-size:110px;color:{NAVY}">What mat goes with these tiles?</div>'),
'q3':(CREAM,f'<div class="it" style="color:{PINK};margin-bottom:30px">No, really.</div><div class="cap" style="font-size:118px;color:{NAVY}">What mat goes with <span style="color:{PINK}">THESE</span> tiles?</div>'),
'q4':(NAVY,f'<div class="cap" style="font-size:96px;color:#fff">Asked in every mahj group.</div><div class="cap" style="font-size:96px;color:#f7b6c8;margin-top:40px">Every. Single. Day.</div>'),
'end':(SOFT,f'<div class="cap" style="font-size:120px;color:{NAVY}">Never ask again.</div><div class="it" style="color:{PINK};margin:40px 0 50px">Your tiles are about to meet their match.</div><div class="cap" style="font-size:92px;color:{PINK};white-space:nowrap">Find Your Mat-ch&trade;</div><div style="margin-top:44px;background:{NAVY};color:#fff;font:700 40px Bit;letter-spacing:6px;padding:18px 44px;border-radius:60px">TOMORROW · 10.27</div><div style="margin-top:60px;font:700 36px Bit;color:{NAVY}">mahjmatchmaker.com</div>'),
}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1920})
    for k,(bg,h) in C.items():
        open('_c.html','w').write(f'<html><head><meta charset=utf-8><style>{CSS}</style></head><body style="background:{bg}">{h}</body></html>')
        pg.goto('file://'+os.path.abspath('_c.html')); pg.wait_for_timeout(700); pg.screenshot(path=f'card_{k}.png')
    b.close()
