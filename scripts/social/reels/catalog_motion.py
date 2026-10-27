"""Catalog in motion (Oct 27 3am, Tiffany: "carousels of mats moving past each other and tiles... bring the catalog
to life"). Rainbow wall: each row = one colour family of real visible FYM mats (app thumbnails), tile-set rows
between, rows sliding in alternate directions; big counts over it, ending on "Find Your Mat-ch is HERE."
Needs the local app served at http://localhost:8766 (fymlive). Usage: python3 catalog_motion.py <out.mp4>"""
import os, sys, json, random, subprocess
from playwright.sync_api import sync_playwright
R = '/home/claude/mahjmatchmaker-data'; F = f'file://{R}/scripts/social/tileprofile/fonts/'
FR = os.environ.get('FR', '/tmp/catmo'); os.makedirs(FR, exist_ok=True)
FPS, SECS = 30, float(os.environ.get('CM_SECS', 13.0))
TIMES = [(0.2,1.5),(1.6,2.9),(3.0,99),(99,99),(99,99)] if os.environ.get('CM_SHORT') else [(0.3, 2.6), (2.8, 5.1), (5.3, 7.6), (7.8, 10.0), (10.2, 99)]
NAVY, PINK, CREAM, BLUSH = '#062a55', '#e0547f', '#fdf6ee', '#f7b6c8'
random.seed(11)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.goto('http://localhost:8766/index.html?tour=off'); pg.wait_for_timeout(5000)
    data = pg.evaluate("""()=>{const M=D.mats,T=D.tiles,out={};
      const fam={pink:['pink'],warm:['orange','red','yellow'],green:['green'],blue:['blue','teal'],purple:['purple'],neutral:['neutral','dark','earthy']};
      for(const [f,cs] of Object.entries(fam)){out[f]=Object.keys(M).filter(k=>!M[k].hid&&!M[k].hol&&M[k].mf&&cs.includes(M[k].mf[0])&&IMG[M[k].th]).map(k=>IMG[M[k].th]);}
      out.tiles=Object.keys(T).filter(k=>!T[k].hid&&IMG[T[k].pile]).map(k=>IMG[T[k].pile]);
      out.counts=[Object.keys(M).filter(k=>!M[k].hid).length,Object.keys(T).filter(k=>!T[k].hid).length];return out}""")
    b.close()
print('families', {k: len(v) for k, v in data.items() if k != 'counts'}, 'counts', data['counts'])
ROWS = ['pink', 'tiles', 'warm', 'green', 'tiles', 'blue', 'purple', 'tiles', 'neutral']
S, GAP = 230, 26
rows_html = []
for i, fam in enumerate(ROWS):
    pool = data[fam][:]; random.shuffle(pool); pool = (pool * 3)[:14]
    circ = fam == 'tiles'
    items = ''.join(f'<img src="{u}" style="width:{S}px;height:{S}px;object-fit:cover;border-radius:{"50%" if circ else "20px"};'
                    f'border:7px solid #fff;box-shadow:0 10px 24px rgba(0,0,0,.35);flex:none">' for u in pool)
    span = 14 * (S + 14 + GAP)
    d = 1 if i % 2 else -1; spd = random.choice([300, 360, 420])   # px/s
    rows_html.append(f'<div class="row" style="--from:{(-span/2 if d > 0 else 0)}px;--to:{(0 if d > 0 else -span/2)}px;animation-duration:{span/2/spd:.2f}s">{items}{items}</div>')
FYM = 'Find <span class="pf">Your</span> Mat&#8209;ch<sup style="font-size:.32em;vertical-align:super">&trade;</sup>'
def beat(t0, t1, html):
    return (f'<div class="beat">'
            f'<div class="a" style="animation:pop .5s {t0:.2f}s forwards">{html}</div></div>')
nm, nt = data['counts']
B = [beat(*TIMES[0], f'<div class="big">{nm // 100 * 100}+</div><div class="lab">mats</div>'),
     beat(*TIMES[1], f'<div class="big">{nt // 100 * 100}+</div><div class="lab">tile sets</div>'),
     beat(*TIMES[2], '<div class="big">50+</div><div class="lab">brands</div>'),
     beat(*TIMES[3], f'<div class="cap" style="font-size:118px">One swipe<br>at a time.</div>'),
     beat(*TIMES[4], f'<div class="cap" style="font-size:92px;white-space:nowrap">{FYM}</div><div class="cap" style="font-size:170px;color:{PINK}">is HERE.</div>'
                      f'<div style="font:700 38px Bit;color:{NAVY};letter-spacing:.12em;margin-top:24px">MAHJMATCHMAKER.COM</div>')]
html = f"""<!doctype html><html><head><meta charset=utf8><style>
@font-face{{font-family:Cap;src:url({F}Caprasimo.ttf)}}@font-face{{font-family:Bit;font-weight:700;src:url({F}bitter-latin-700-normal.woff2)}}@font-face{{font-family:PF;font-style:italic;src:url({F}playfair-display-latin-600-italic.woff2)}}
*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1080px;height:1920px;overflow:hidden;background:{NAVY}}}
.wall{{position:absolute;left:-400px;top:-260px;width:1900px;transform:rotate(-8deg);display:flex;flex-direction:column;gap:{GAP}px}}
.row{{display:flex;gap:{GAP}px;animation-name:slide;animation-timing-function:linear;animation-iteration-count:infinite}}
@keyframes slide{{from{{transform:translateX(var(--from))}}to{{transform:translateX(var(--to))}}}}
.beat{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;opacity:0}}
.beat>div{{background:{CREAM};border-radius:48px;padding:56px 70px;text-align:center;color:{NAVY};box-shadow:0 30px 80px rgba(0,0,0,.45);min-width:620px}}
.a{{opacity:0;animation-fill-mode:forwards}}@keyframes pop{{0%{{transform:scale(.5);opacity:0}}60%{{transform:scale(1.06);opacity:1}}100%{{transform:scale(1);opacity:1}}}}
.big{{font-family:Cap;font-size:260px;line-height:1;color:{PINK}}}.lab{{font-family:Cap;font-size:110px;line-height:1.05}}.cap{{font-family:Cap;line-height:1.05}}.pf{{font-family:PF;font-style:italic}}
</style></head><body><div class="wall">{''.join(rows_html)}</div>{''.join(B)}</body></html>"""
# per-beat visibility done in JS below (simpler than keyframe %s)
open(f'{FR}/wall.html', 'w').write(html)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.goto(f'file://{FR}/wall.html'); pg.wait_for_timeout(1500); pg.evaluate('document.fonts.ready')
    pg.evaluate('document.getAnimations().forEach(a=>a.pause())')
    spans = TIMES
    import shutil; shutil.rmtree(f'{FR}/f', ignore_errors=True); os.makedirs(f'{FR}/f', exist_ok=True)
    for i in range(int(SECS * FPS)):
        t = i / FPS
        pg.evaluate(f"""()=>{{document.getAnimations().forEach(a=>a.currentTime={t*1000});
          const sp={json.dumps(spans)};document.querySelectorAll('.beat').forEach((e,k)=>{{const [a,b]=sp[k];e.style.opacity=(t=>t<a||t>b?0:Math.min(1,(t-a)/.15,(b-t)/.15))({t})}})}}""")
        pg.screenshot(path=f'{FR}/f/{i:04d}.png')
    b.close()
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', f'{FR}/f/%04d.png', '-c:v', 'libx264', '-crf', '19', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', sys.argv[1]], check=True)
print('ok')
