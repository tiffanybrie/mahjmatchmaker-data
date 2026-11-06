"""Week Nov 9-15 FINAL media for the Planoly drafts (Friday next-week prep task, Nov 6).
Feed slides = the finished Oct 31 FYM content bank (assets/social/fym-bank-oct31) + Wed's Juniper It's a mat-ch!
(build_juniper.py) + Sat's color-filter copy with the mat name fixed (fix_p3_name.py).
Story frames are rebuilt from the FEED slides (scaled 950x1188 in the IG safe band, every brand's @mention printed
under it, CLAUDE.md social rule 8), because the Oct 31 bank story frames had no @mentions and story-01 of
how-it-works had its sub line hidden behind the phones."""
import os, shutil
from playwright.sync_api import sync_playwright
R = '/home/claude/mahjmatchmaker-data'; B = f'{R}/assets/social/fym-bank-oct31'; O = f'{R}/assets/social/week-2026-11-09/final'
F = f'file://{R}/scripts/social/tileprofile/fonts'
OMM, BM, MM, VIR, AR, BB, MV, MTH = '@ohmymahjong', '@brittmillsdesign', '@middleandmainmahjong', '@viroramahjongofficial', '@andersruffdesignco', '@bird_and_bamboo', '@mahjandvine', '@mahjtilehaus'
LUXE, HIP = 'Polo Club by Luxe Mahjong', "Rackin' Rudolph by Hip Hip Mahjong"
DAYS = {  # out dir: (source dir, [mentions per slide])
 'mon-how':    (f'{B}/p1-how-it-works', [(OMM, BM, MM), (OMM,), (OMM, BM), (BM, MM), (OMM, BM, MM), ()]),
 'tue-xmas30': (f'{B}/p2-holiday-30s', [(VIR, AR, LUXE), (VIR, LUXE), (LUXE,), (VIR, AR), (AR, BB), (VIR, AR, BB), ()]),
 'wed-juniper':(f'{O}/wed-juniper', [(OMM, MTH)]),
 'thu-tartan': (f'{B}/p6-tartan-tidings-matdoor', [(AR, VIR, HIP), (AR, VIR), (AR,), (AR, HIP), ()]),
 'fri-doors':  (f'{B}/p4-two-doors', [(OMM, BM), (OMM, BM), (OMM, BM), ()]),
 'sat-color':  (f'{O}/sat-color', [(OMM, AR, MV), (OMM, AR), (OMM, AR), (OMM,), (OMM, MV), ()]),
}
os.makedirs('/dev/shm/wk', exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    for d, (src, men) in DAYS.items():
        od = f'{O}/{d}'; os.makedirs(od, exist_ok=True)
        for i, m in enumerate(men, 1):
            s = f'{src}/slide1.jpg' if d == 'wed-juniper' else f'{src}/feed-{i:02d}.jpg'
            if d != 'wed-juniper': shutil.copy(s, f'{od}/slide{i}.jpg')
            html = f"""<meta charset=utf-8><style>@font-face{{font-family:Bit;src:url({F}/bitter-latin-700-normal.woff2);font-weight:700}}
*{{margin:0}}body{{width:1080px;height:1920px;background:#faf3ea;position:relative;font-family:Bit}}
img{{position:absolute;left:65px;top:270px;width:950px;height:1188px;border-radius:18px;box-shadow:0 10px 30px rgba(6,42,85,.18)}}
.m{{position:absolute;left:40px;right:40px;top:1478px;text-align:center;font:700 34px/1.35 Bit;color:#062a55}}</style>
<img src="file://{s}"><div class=m>{' · '.join(m)}</div>"""
            open('/dev/shm/wk/st.html', 'w').write(html); pg.goto('file:///dev/shm/wk/st.html'); pg.wait_for_timeout(350)
            pg.screenshot(path=f'{od}/story-{i}.jpg', type='jpeg', quality=90)
    b.close()
# Sun 11/15 story-only recap = frame 1 of each day's story (Mon, Tue, Wed, Thu, Sat)
os.makedirs(f'{O}/sun-recap', exist_ok=True)
for n, d in enumerate(['mon-how', 'tue-xmas30', 'wed-juniper', 'thu-tartan', 'sat-color'], 1):
    shutil.copy(f'{O}/{d}/story-1.jpg', f'{O}/sun-recap/story-{n}.jpg')
print('ok')
