"""Full Instagram profile mock (Oct 19): seal option in the highlights, pastel highlight covers, Papaya pinned row,
rainbow grid of album covers (quiet 'Post only to profile' fill). Renders C and 2 side by side."""
import glob, os
from playwright.sync_api import sync_playwright
R='/home/claude/mahjmatchmaker-data/'
u=lambda p:'file://'+(p if p.startswith('/') else R+p)
def cover(s): return glob.glob(R+f'assets/covers/albums/w800/*{s}-mahjong-tiles-cover.jpg')[0]
PIN=['assets/social/papaya-spritz-launch/intro/1.jpg','assets/social/papaya-spritz-launch/grid/papaya-grid-1-its-a-match-heiress.jpg',cover('papaya-spritz')]
ROWS=[['amara','coquette','glitterville'],['sunset','sierra','pippa'],['limoncello','drake','emerald'],['lagoon','seabreeze','osler'],['luminaire','gemma','taylor'],['smith','cypress-forest','talulah']]
HL=[('SEAL','Matched'),('papaya','Papaya'),('assets/social/highlights/style-C/02-new-tiles.png','New Tiles'),('assets/social/highlights/style-C/03-albums.png','Albums'),
    ('assets/social/highlights/style-C/06-codes.png','Codes'),('assets/social/highlights/style-C/07-fb-group.png','FB Group'),('assets/social/highlights/style-C/08-about-2-0.png','About')]
def phone(seal,label):
    hl=''
    for src,lab in HL:
        if src=='SEAL': inner=f'<img src="{u(seal)}" style="object-fit:contain;background:#fff">'
        elif src=='papaya': inner=f'<div style="width:100%;height:100%;border-radius:50%;background:#de7e30;padding:7px;box-sizing:border-box"><img src="{u("assets/tiles/album/papaya-spritz.jpg")}" style="width:100%;height:100%;border-radius:50%"></div>'
        else: inner=f'<img src="{u(src)}">'
        hl+=f'<div class="h"><div class="ring">{inner}</div><span>{lab}</span></div>'
    pin=''.join(f'<div class="c" style="background-image:url({u(p)})"><svg class="pin" viewBox="0 0 24 24"><path d="M16 3l5 5-3 1-4 4 1 5-2 2-4-4-5 5-1-1 5-5-4-4 2-2 5 1 4-4z" fill="#fff"/></svg></div>' for p in PIN)
    grid=''.join(f'<div class="c" style="background-image:url({u(cover(s))})"></div>' for row in ROWS for s in row)
    return f'''<div class="ph"><div class="lab">{label}</div>
<div class="bar"><b>mahjmatchmaker ⌄</b><span>＋ &nbsp;☰</span></div>
<div class="top"><img class="av" src="{u('assets/brand/fb-page/mahj-matchmaker-page-profile-1080.jpg')}"><div class="st"><b>Mahj Matchmaker</b><div class="nums"><div><b>33</b><br>posts</div><div><b>410</b><br>followers</div><div><b>423</b><br>following</div></div></div></div>
<div class="bio"><span class="g">Digital creator</span><br>💕 Hooking Up Tiles, Mats &amp; Racks<br>✨ OMM Instructor<br>🛍️ Code MAHJMATCH saves at our partner brands<br>👇🏼 Find your match + join our FB group<br><b class="lk">🔗 mahjmatchmaker.com/links and 1 more</b></div>
<div class="btns"><div>Edit profile</div><div>Share profile</div></div>
<div class="hls">{hl}</div>
<div class="tabs"><span class="on">▦</span><span>▶</span><span>☺</span></div>
<div class="grid">{pin}{grid}</div></div>'''
css='''body{margin:0;background:#efe7df;font:14px -apple-system,"Helvetica Neue",Arial,sans-serif;display:flex;gap:40px;padding:40px;width:max-content}
.ph{width:430px;background:#fff;border-radius:34px;overflow:hidden;box-shadow:0 20px 50px rgba(0,0,0,.15);position:relative}
.lab{background:#054689;color:#fff;text-align:center;font-weight:700;padding:10px;font-size:16px}
.bar{display:flex;justify-content:space-between;padding:14px 16px 6px;font-size:18px}
.top{display:flex;gap:18px;align-items:center;padding:6px 16px}.av{width:86px;height:86px;border-radius:50%;border:1px solid #ddd}
.st b{font-size:15px}.nums{display:flex;gap:22px;margin-top:6px;font-size:13px;line-height:1.2}.nums b{font-size:16px}
.bio{padding:8px 16px;font-size:13.5px;line-height:1.38}.g{color:#737373}.lk{color:#00376b}
.btns{display:flex;gap:6px;padding:6px 16px}.btns div{flex:1;background:#efefef;border-radius:8px;text-align:center;padding:7px;font-weight:600;font-size:13px}
.hls{display:flex;gap:12px;padding:12px 14px 10px;overflow:hidden}.h{width:66px;flex:none;text-align:center}
.ring{width:62px;height:62px;border-radius:50%;border:1px solid #dbdbdb;padding:3px;margin:0 auto}.ring img{width:62px;height:62px;border-radius:50%;object-fit:cover;display:block}
.h span{display:block;font-size:11px;margin-top:5px;white-space:nowrap}
.tabs{display:flex;justify-content:space-around;border-top:1px solid #efefef;padding:8px;font-size:18px;color:#999}.tabs .on{color:#000}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:2px}.c{aspect-ratio:3/4;background-size:cover;background-position:center;position:relative}
.pin{position:absolute;top:6px;right:6px;width:16px;height:16px;filter:drop-shadow(0 1px 2px rgba(0,0,0,.5))}'''
html=f'<!doctype html><html><head><meta charset=utf8><style>{css}</style></head><body>{phone("assets/brand/seal/seal-C-ring-pastel.png","C · Color wheel ring")}{phone("assets/brand/seal/seal-full-pastel-navy-flame.png","2 · Full pastel wheel")}</body></html>'
out=R+'assets/social/profile-mock-seal-C-vs-2.png'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1000,'height':1000},device_scale_factor=2); hp=R+'scripts/social/feedmock/_profile_mock.html'; open(hp,'w').write(html); pg.goto('file://'+hp); pg.wait_for_timeout(2000)
    pg.screenshot(path=out,full_page=True); b.close()
print(out)
