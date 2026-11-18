# Brand Watch promo graphics (Tiffany Nov 17 2026 10:53pm): IG profile (pinned) post 1080x1350,
# story/reel frame 1080x1920, and a style-C highlight cover "Brand Watch" + profile-row preview.
import os, base64, sys
from playwright.sync_api import sync_playwright
HERE=os.path.dirname(os.path.abspath(__file__)); REPO=os.path.abspath(os.path.join(HERE,'../../..'))
OUT=os.path.join(REPO,'assets/social/brand-watch-promo'); os.makedirs(OUT,exist_ok=True)
F=os.path.join(REPO,'scripts/social/tileprofile/fonts')
def b64(p): return base64.b64encode(open(p,'rb').read()).decode()
def mime(p): return 'image/png' if p.endswith('.png') else ('font/ttf' if p.endswith('.ttf') else ('font/woff2' if p.endswith('woff2') else 'image/jpeg'))
def uri(p): return f"data:{mime(p)};base64,{b64(p)}"
FONTS=f"""@font-face{{font-family:Capra;src:url({uri(F+'/Caprasimo.ttf')})}}
@font-face{{font-family:PF;font-style:italic;font-weight:400;src:url({uri(F+'/playfair-display-latin-400-italic.woff2')})}}
@font-face{{font-family:Bitter;font-weight:700;src:url({uri(F+'/bitter-latin-700-normal.woff2')})}}
@font-face{{font-family:Bitter;font-weight:600;src:url({uri(F+'/bitter-latin-600-normal.woff2')})}}"""
LOGO=uri(os.path.join(REPO,'assets/brand/mahjmatchmaker-wordmark-notag.png'))
NAVY,DEEP,ROSE,PINK,CREAM='#054689','#062a55','#c8325f','#f56c8c','#f6e9df'
# (file, brand, tag, object-position)
ITEMS=[('img/ar-bloom.jpg','Anders Ruff','Back in stock','50% 50%'),
 ('img/cmc.jpg','Charleston Mahjong Club','New','50% 40%'),
 ('img/mm-lilac.png','Miss Mahjong','Coming soon','40% 50%'),
 ('img/maison.png','Maison Mahj','Holiday','50% 50%',1.1),
 ('img/mood-pearl.jpg','Mahj Mood','Back in stock','50% 50%'),
 ('img/bm-plumage.jpg','Britt Mills','New','50% 56%',1.75)]
def tiles(sz):
    h=''
    for it in ITEMS:
        f,b,t,pos=it[:4]; sc=it[4] if len(it)>4 else 1
        h+=f'''<div class="t" style="width:{sz}px;height:{sz}px"><img src="{uri(os.path.join(HERE,f))}" style="object-position:{pos};transform:scale({sc});transform-origin:{pos}">
        <span class="tag">{t}</span><span class="br">{b}</span></div>'''
    return h
CSS=FONTS+f"""*{{box-sizing:border-box}}html,body{{margin:0;background:{CREAM}}}
.wrap{{position:relative;overflow:hidden;background:{CREAM};display:flex;flex-direction:column;align-items:center;text-align:center}}
.logo{{display:block}}
.kick{{font:700 26px Bitter;letter-spacing:.22em;color:{ROSE};text-transform:uppercase}}
h1{{font-family:Capra;color:{NAVY};margin:0;line-height:.98;font-weight:400}}
.sub{{font-family:PF;font-style:italic;color:{DEEP};line-height:1.28}}
.grid{{display:grid;gap:18px}}
.t{{position:relative;border-radius:22px;overflow:hidden;background:#fff;box-shadow:0 6px 18px rgba(6,42,85,.12)}}
.t img{{width:100%;height:100%;object-fit:cover;display:block}}
.tag{{position:absolute;top:14px;left:14px;background:{ROSE};color:#fff;font:700 19px Bitter;letter-spacing:.08em;text-transform:uppercase;padding:7px 13px;border-radius:999px}}
.br{{position:absolute;left:0;right:0;bottom:0;background:rgba(6,42,85,.86);color:#fff;font:600 21px Bitter;padding:9px 8px 10px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.url{{background:{NAVY};color:#fff;font:700 34px Bitter;border-radius:999px;padding:20px 40px;letter-spacing:.01em}}
.code{{font:600 28px Bitter;color:{DEEP}}} .code b{{color:{ROSE};letter-spacing:.06em}}
"""
def feed():
    return f"""<style>{CSS}</style><div class="wrap" style="width:1080px;height:1350px;padding:96px 70px 0">
<img class="logo" src="{LOGO}" style="width:300px">
<div class="kick" style="margin-top:26px">Updated every day</div>
<h1 style="font-size:96px;margin-top:10px">Partner Brand Watch</h1>
<div class="sub" style="font-size:34px;margin-top:16px;max-width:880px">New tile sets, mats &amp; racks, restocks and sales from our partner brands, all in one place</div>
<div class="grid" style="grid-template-columns:repeat(3,272px);margin-top:30px">{tiles(272)}</div>
<div class="url" style="margin-top:30px;font-size:32px;padding:16px 38px">mahjmatchmaker.com/brand-watch</div>
<div class="code" style="margin-top:14px">Link in bio · save with code <b>MAHJMATCH</b></div></div>"""
def story():
    return f"""<style>{CSS}</style><div class="wrap" style="width:1080px;height:1920px;padding:280px 80px 0">
<img class="logo" src="{LOGO}" style="width:360px">
<div class="kick" style="margin-top:38px;font-size:30px">Updated every day</div>
<h1 style="font-size:118px;margin-top:16px">Partner Brand<br>Watch</h1>
<div class="sub" style="font-size:42px;margin-top:24px;max-width:860px">New tile sets, mats &amp; racks, restocks and sales from our partner brands, all in one place</div>
<div class="grid" style="grid-template-columns:repeat(3,290px);margin-top:46px;gap:20px">{tiles(290)}</div>
<div class="url" style="margin-top:50px;font-size:38px">mahjmatchmaker.com/brand-watch</div>
<div class="code" style="margin-top:22px;font-size:32px">Save with code <b>MAHJMATCH</b></div></div>"""
# highlight cover, same recipe as assets/social/highlights style C (1080x1920, icon centered)
BG,INK,ACC='#cdeeea','#2b7a74','#f56c8c'
ICON='''<circle cx="74" cy="150" r="48"/><circle cx="166" cy="150" r="48"/>
<path d="M30 140L62 70Q70 56 86 60L104 66"/><path d="M210 140L178 70Q170 56 154 60L136 66"/>
<path d="M104 66Q120 58 136 66"/><line x1="113" y1="140" x2="127" y2="140"/>
<path class="a" d="M120 46C110 39 106 33 106 28C106 23 110 19 114 19C117 19 119 21 120 23C121 21 123 19 126 19C130 19 134 23 134 28C134 33 130 39 120 46Z" transform="translate(-48 28) scale(1.4) translate(0 0)"/>'''
ICON='''<circle cx="104" cy="104" r="64"/><line x1="152" y1="152" x2="206" y2="206" style="stroke-width:20"/>
<path class="a" d="M104 136C80 120 72 108 72 96C72 84 80 76 91 76C97 76 101 79 104 84C107 79 111 76 117 76C128 76 136 84 136 96C136 108 128 120 104 136Z"/>
<path class="a" d="M196 22L201 35L214 40L201 45L196 58L191 45L178 40L191 35Z"/>'''
def cover(guide=False):
    g='<div style="position:absolute;left:50%;top:50%;width:1080px;height:1080px;margin:-540px;border-radius:50%;border:4px dashed red"></div>' if guide else ''
    return f"""<style>html,body{{margin:0;width:1080px;height:1920px;background:{BG};overflow:hidden}}
svg{{position:absolute;left:50%;top:50%;width:420px;height:420px;margin:-210px}}
svg *{{fill:none;stroke:{INK};stroke-width:11;stroke-linecap:round;stroke-linejoin:round}} svg .a{{fill:{ACC};stroke:none}}</style>
<svg viewBox="0 0 240 240"><g transform="translate(120 120) scale(1.05) translate(-118 -116)">{ICON}</g></svg>{g}"""
def row(files):
    circ=''.join(f'<div class="c"><div class="ring"><img src="{uri(p)}"></div><div class="l">{l}</div></div>' for p,l in files)
    return f"""<style>body{{margin:0;font-family:-apple-system,Helvetica,Arial;background:#fff}}
.r{{display:flex;gap:26px;padding:36px 30px}} .c{{text-align:center;width:150px}}
.ring{{width:150px;height:150px;border-radius:50%;border:2px solid #ddd;padding:6px;box-sizing:border-box}}
.ring img{{width:100%;height:100%;border-radius:50%;object-fit:cover}} .l{{margin-top:12px;font-size:22px;color:#111}}</style><div class="r">{circ}</div>"""
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,html,w,h in [('brand-watch-profile-post-1080x1350',feed(),1080,1350),('brand-watch-story-reel-1080x1920',story(),1080,1920),('highlight-brand-watch',cover(),1080,1920)]:
        pg=b.new_page(viewport={'width':w,'height':h},device_scale_factor=1)
        pg.set_content(html); pg.wait_for_timeout(600)
        ext='png' if name.startswith('highlight') else 'jpg'
        kw={'type':'png'} if ext=='png' else {'type':'jpeg','quality':93}
        pg.screenshot(path=f'{OUT}/{name}.{ext}',**kw); pg.close()
    H=os.path.join(REPO,'assets/social/highlights/style-C')
    files=[(f'{H}/01-find-your-match.png','Find Match'),(f'{H}/02-new-tiles.png','New Tiles'),(f'{H}/03-albums.png','Albums'),(f'{H}/06-codes.png','Codes'),(f'{OUT}/highlight-brand-watch.png','Brand Watch'),(f'{H}/07-fb-group.png','FB Group')]
    pg=b.new_page(viewport={'width':1080,'height':260}); pg.set_content(row(files)); pg.wait_for_timeout(300)
    pg.screenshot(path=f'{OUT}/preview-highlight-row.png'); b.close()
print('ok')
