"""Story frames (1080x1920) for every feed slide, with the brands' @mentions visible on each frame (CLAUDE.md social rule 8).
Slide scaled to 950x1188 inside the IG safe band (top 269px / bottom 384px clear), mention line under it."""
from playwright.sync_api import sync_playwright
R = '/home/claude/mahjmatchmaker-data'; O = f'{R}/assets/social/week-2026-11-02/final'
F = f'file://{R}/scripts/social/tileprofile/fonts'
AR, BB, PLM, MM, BAM, BES, MJ = '@andersruffdesignco', '@bird_and_bamboo', '@peacelovemahjong', '@middleandmainmahjong', '@bamletsmahjong', '@bespoke_mahjong', '@missmahjongofficial'
JOBS = {'thu-ds': [(f'slide{i}.jpg', (AR,) if i in (1, 9) else (AR, BB, PLM, MM)) for i in range(1, 10)],
        'sat-hj': [('slide1.jpg', (BAM, BES)), ('slide2.jpg', (BAM, BES, BB, MJ, MM)), ('slide3.jpg', (BAM, BES))],
        'sun-rr': [('slide1.jpg', ('Rackin\' Rudolph by Hip Hip Mahjong', AR)), ('slide2.jpg', (AR, BB, PLM, MM)), ('slide3.jpg', (AR,))]}
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    for d, items in JOBS.items():
        for n, (src, men) in enumerate(items, 1):
            html = f"""<meta charset=utf-8><style>@font-face{{font-family:Bit;src:url({F}/bitter-latin-700-normal.woff2);font-weight:700}}
*{{margin:0}}body{{width:1080px;height:1920px;background:#faf3ea;position:relative;font-family:Bit}}
img{{position:absolute;left:65px;top:270px;width:950px;height:1188px;border-radius:18px;box-shadow:0 10px 30px rgba(6,42,85,.18)}}
.m{{position:absolute;left:40px;right:40px;top:1478px;text-align:center;font:700 34px/1.35 Bit;color:#062a55}}</style>
<img src="file://{O}/{d}/{src}"><div class=m>{' '.join(men)}</div>"""
            open('/dev/shm/weekdrafts/_st.html', 'w').write(html); pg.goto('file:///dev/shm/weekdrafts/_st.html'); pg.wait_for_timeout(500)
            pg.screenshot(path=f'{O}/{d}/story-{n}.jpg', type='jpeg', quality=92)
    b.close()
print('ok')

# Wed new-arrivals carousel (7 square slides, already in Planoly draft 01a19e04): one story frame per slide, its brand @mention under it
NA = ['@andersruffdesignco', '@bambirdboutique', '@sunday_mahjong', '@sunday_mahjong', '@letsbebestiesmahjong', '@letsbebestiesmahjong', '@letsbebestiesmahjong']
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    for n, men in enumerate(NA, 1):
        html = f"""<meta charset=utf-8><style>@font-face{{font-family:Bit;src:url({F}/bitter-latin-700-normal.woff2);font-weight:700}}
*{{margin:0}}body{{width:1080px;height:1920px;background:#faf3ea;position:relative;font-family:Bit}}
img{{position:absolute;left:65px;top:420px;width:950px;height:950px;border-radius:18px;box-shadow:0 10px 30px rgba(6,42,85,.18)}}
.m{{position:absolute;left:40px;right:40px;top:1400px;text-align:center;font:700 40px/1.35 Bit;color:#062a55}}</style>
<img src="file://{O}/wed-newarrivals/na{n}.jpg"><div class=m>{men}</div>"""
        open('/dev/shm/weekdrafts/_st.html', 'w').write(html); pg.goto('file:///dev/shm/weekdrafts/_st.html'); pg.wait_for_timeout(500)
        pg.screenshot(path=f'{O}/wed-newarrivals/story-{n}.jpg', type='jpeg', quality=92)
    b.close()
print('na ok')
