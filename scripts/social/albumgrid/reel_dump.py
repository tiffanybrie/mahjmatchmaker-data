#!/usr/bin/env python3
"""Dynamic album teaser reel, photo-dump style (Tiffany Nov 9: reels for reach, several scenes,
movement, album cover, sell someone who knows nothing; NOT a flat card on a blur).
Scenes: brand lifestyle hook -> tiles -> mats tossed onto the table like a photo dump with a
running count -> album cover -> Find Your Mat-ch end card. 9:16, 24fps. Text kept in y 270-1440.
Usage: reel_dump.py <config.json> <out.mp4>"""
import json, sys, os, subprocess, shutil, base64, io
from PIL import Image
from playwright.sync_api import sync_playwright
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
F = R + '/scripts/social/tileprofile/fonts'
FPS = 24
cfg = json.load(open(sys.argv[1])); out = sys.argv[2]
DUR = cfg.get('dur', 15.0)

def uri(p, maxs=1300, trim=False):
    im = Image.open(p if p.startswith('/') else R + '/' + p).convert('RGB')
    if trim:  # cut white/flat margins so the mat fills its card
        from PIL import ImageChops
        bg = Image.new('RGB', im.size, im.getpixel((2, 2)))
        bb = ImageChops.difference(im, bg).convert('L').point(lambda v: 255 if v > 18 else 0).getbbox()
        if bb: im = im.crop(bb)
    im.thumbnail((maxs, maxs)); b = io.BytesIO(); im.save(b, 'JPEG', quality=86)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()

mats = cfg['mats'][:cfg.get('dump_n', 14)]
import random; random.seed(7)
pos = []
for i in range(len(mats)):
    pos.append(dict(x=random.randint(250, 830), y=random.randint(800, 1220), r=random.uniform(-14, 14)))
mat_html = ''.join(f'<div class="pc" id="p{i}"><img src="{uri(m, 700, True)}"></div>' for i, m in enumerate(mats))
html = f'''<html><head><meta charset="utf-8"><style>
@font-face{{font-family:Cap;src:url({F}/Caprasimo.ttf)}}
@font-face{{font-family:PF;font-style:italic;src:url({F}/playfair-display-latin-400-italic.woff2)}}
@font-face{{font-family:Bit;font-weight:700;src:url({F}/bitter-latin-700-normal.woff2)}}
body{{margin:0}}.c{{width:1080px;height:1920px;position:relative;overflow:hidden;background:#f6e9df}}
.sc{{position:absolute;inset:0;opacity:0}}
.bg{{position:absolute;inset:0;background-size:cover;background-position:center}}
.shade{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.45) 0%,rgba(0,0,0,0) 38%,rgba(0,0,0,0) 62%,rgba(0,0,0,.35) 100%)}}
.big{{position:absolute;left:0;right:0;text-align:center;font:104px/1.02 Cap;color:#fff;text-shadow:0 4px 24px rgba(0,0,0,.45);padding:0 70px}}
.it{{font:italic 54px/1.15 PF;color:#fff;text-shadow:0 3px 16px rgba(0,0,0,.5)}}
.lbl{{position:absolute;left:0;right:0;text-align:center}}
.pill{{display:inline-block;background:#b3152b;color:#fff;font:700 36px Bit;padding:16px 38px;border-radius:60px}}
.pc{{position:absolute;width:380px;height:380px;margin:-190px 0 0 -190px;background:#fff;padding:14px;box-sizing:border-box;border-radius:10px;box-shadow:0 14px 34px rgba(60,20,20,.32);opacity:0}}
.pc img{{width:100%;height:100%;object-fit:cover;border-radius:4px;display:block}}
.cnt{{z-index:99;position:absolute;top:300px;left:0;right:0;text-align:center;font:150px/1 Cap;color:#b3152b}}
.cntl{{position:absolute;z-index:99;top:460px;left:0;right:0;text-align:center;font:700 40px Bit;letter-spacing:6px;color:#0d4a2d}}
.cov{{position:absolute;left:90px;top:420px;width:900px;height:900px;border-radius:18px;background-size:cover;background-position:center;box-shadow:0 20px 50px rgba(0,0,0,.3)}}
.end h1{{font:96px/1.02 Cap;color:#0d4a2d;margin:0}}.end .y{{font:italic 96px/1 PF;color:#0d4a2d}}
.end .s{{font:italic 46px/1.25 PF;color:#3b2a2a;margin-top:26px}}.end .tm{{font:40px Cap;vertical-align:top}}
</style></head><body><div class="c">
<div class="sc" id="s1"><div class="bg" id="b1" style="background-image:url({uri(cfg['hook'],1500)})"></div><div class="shade"></div>
 <div class="big" style="top:300px">{cfg['hook_text']}</div><div class="lbl" style="top:1300px" id="h1b"><span class="pill" style="background:rgba(13,74,45,.92);font:italic 44px PF">{cfg['hook_sub']}</span></div></div>
<div class="sc" id="s2"><div class="bg" id="b2" style="background-image:url({uri(cfg['tiles'],1500)})"></div><div class="shade"></div>
 <div class="big" style="top:300px;font-size:92px">{cfg['tiles_text']}</div><div class="lbl" style="top:1300px"><span class="pill">{cfg['tiles_pill']}</span></div></div>
<div class="sc" id="s3" style="background:#f6e9df">{mat_html}<div class="cnt" id="cnt">0</div><div class="cntl">{cfg['count_label']}</div></div>
<div class="sc" id="s4" style="background:#0d4a2d"><div class="cov" id="cov" style="background-image:url({uri(cfg['cover'],1300)})"></div></div>
<div class="sc end" id="s5" style="background:#f6e9df"><div class="lbl" style="top:470px"><div class="s" style="margin:0 0 30px">{cfg['end_kicker']}</div>
 <h1>Find <span class="y">Your</span><br>Mat-ch<span class="tm">™</span></h1><div class="s">{cfg['end_sub']}</div>
 <div style="margin-top:60px"><span class="pill">Link in bio</span></div><div style="font:700 34px Bit;color:#0d4a2d;margin-top:30px">{cfg['code_line']}</div></div></div>
</div><script>
const P={json.dumps(pos)}, N={len(mats)}, TOTAL={cfg['count']};
const E=x=>{{x=Math.min(1,Math.max(0,x));return 1-Math.pow(1-x,3)}};
const B=x=>{{x=Math.min(1,Math.max(0,x));const c=1.6;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)}};
const S=[[0,2.6],[2.6,5.0],[5.0,10.6],[10.6,12.6],[12.6,{DUR}]];
function vis(id,t,a,b){{const f=.25;let o=Math.min(E((t-a)/f), b>={DUR}-.01?1:E((b-t)/f));document.getElementById(id).style.opacity=o;return o}}
window.step=function(t){{
 vis('s1',t,0,2.6); document.getElementById('b1').style.transform=`scale(${{1.12-0.1*t/2.6}})`;
 vis('s2',t,2.6,5.0); document.getElementById('b2').style.transform=`scale(${{1.0+0.08*(t-2.6)/2.4}}) translateY(${{-20*(t-2.6)/2.4}}px)`;
 vis('s3',t,5.0,10.6);
 const per=4.6/N;
 for(let i=0;i<N;i++){{const st=5.15+i*per, x=(t-st)/0.32, e=document.getElementById('p'+i), p=P[i];
  e.style.opacity=x>0?1:0; const sc=1.6-0.6*B(x); e.style.left=p.x+'px'; e.style.top=(p.y-120*(1-E(x)))+'px';
  e.style.transform=`rotate(${{p.r+(1-E(x))*18}}deg) scale(${{sc}})`; e.style.zIndex=i;}}
 const k=Math.max(0,Math.min(1,(t-5.15)/4.8)); document.getElementById('cnt').textContent=Math.round(E(k)*TOTAL);
 vis('s4',t,10.6,12.6); document.getElementById('cov').style.transform=`scale(${{0.92+0.08*E((t-10.6)/0.6)}}) rotate(${{-2+2*E((t-10.6)/0.6)}}deg)`;
 vis('s5',t,12.6,{DUR});
}};</script></body></html>'''
tmp = os.path.splitext(out)[0] + '_frames'; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
hp = tmp + '/r.html'; open(hp, 'w').write(html)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.goto('file://' + hp); pg.wait_for_timeout(1200)
    for i in range(int(DUR * FPS)):
        pg.evaluate(f'step({i / FPS})'); pg.screenshot(path=f'{tmp}/{i:04d}.jpg', type='jpeg', quality=88)
    b.close()
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', f'{tmp}/%04d.jpg', '-c:v', 'libx264',
                '-pix_fmt', 'yuv420p', '-crf', '19', '-movflags', '+faststart', out], check=True)
for s, f in [(1.3, 'a'), (3.8, 'b'), (8.0, 'c'), (10.5, 'd'), (11.8, 'e'), (14.2, 'f')]:
    shutil.copy(f'{tmp}/{int(s * FPS):04d}.jpg', os.path.splitext(out)[0] + f'-check-{f}.jpg')
shutil.rmtree(tmp); print('ok', out)
