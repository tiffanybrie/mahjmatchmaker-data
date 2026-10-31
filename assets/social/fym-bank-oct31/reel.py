"""Compose the FYM screen-recording reel (1080x1920, silent-capable, captions on screen; Tiffany adds her love song by hand).
Input: rec.py frames (/dev/shm/w/rec/raw.mp4). Output: reel/fym-how-it-works-reel.mp4 + cover jpg. Usage: python3 reel.py"""
import os,subprocess,json
os.environ['TMPDIR']='/dev/shm/w'
from playwright.sync_api import sync_playwright
D=os.path.dirname(os.path.abspath(__file__)); R=os.path.abspath(D+'/../../..'); W='/dev/shm/w/reel'
F='file://'+R+'/scripts/social/tileprofile/fonts/'
NAVY,PINK,CREAM='#062a55','#e0547f','#faf3ea'
SP=1.2  # speed-up
VW,VH=630,1363; SB=48; BZ=22; SX=(1080-VW)//2; SY=410+BZ
CSS=f"""@font-face{{font-family:Cap;src:url({F}Caprasimo.ttf)}}@font-face{{font-family:PF;font-style:italic;src:url({F}playfair-display-latin-600-italic.woff2)}}
@font-face{{font-family:Bit;font-weight:700;src:url({F}bitter-latin-700-normal.woff2)}}*{{margin:0}}body{{width:1080px;height:1920px;position:relative;overflow:hidden;font-family:Bit;background:transparent}}
.c{{position:absolute;left:0;right:0;text-align:center}}.pf{{font-family:PF;font-style:italic;font-weight:600}}"""
FYM=lambda s:f'Find <span class="pf" style="font-size:{s*1.04:.0f}px">Your</span> Mat-ch<sup style="font-size:{s*.36:.0f}px">&trade;</sup>'
def top_html():
    ox,oy,ow,oh=SX-BZ,410,VW+2*BZ,SB+VH+2*BZ
    return f'''<svg width="1080" height="1920" style="position:absolute;inset:0"><defs><mask id="m"><rect width="1080" height="1920" fill="#fff"/><rect x="{SX}" y="{SY+SB}" width="{VW}" height="{VH}" rx="0" fill="#000"/></mask>
<filter id="sh" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="26" stdDeviation="26" flood-color="#062a55" flood-opacity=".16"/></filter></defs>
<rect width="1080" height="1920" fill="{CREAM}" mask="url(#m)"/>
<g mask="url(#m)"><rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" rx="96" fill="#f7f7f5" stroke="#d6d6d3" stroke-width="4" filter="url(#sh)"/>
<rect x="{SX}" y="{SY}" width="{VW}" height="{SB+40}" rx="0" fill="#fff"/></g></svg>
<div style="position:absolute;left:{SX+46}px;top:{SY+12}px;font:600 22px -apple-system,Helvetica,Arial;color:#111">9:41</div>
<div style="position:absolute;right:{1080-SX-VW+46}px;top:{SY+12}px;font:600 22px -apple-system,Helvetica,Arial;color:#111;letter-spacing:2px">&#9679;&#9679;&#9679; &#9646;</div>
<div style="position:absolute;left:{540-80}px;top:{SY+8}px;width:160px;height:34px;background:#000;border-radius:20px"></div>'''
# rounded inner screen corners: paint corner fillets over the video
def corners():
    r=70; s=''
    for (x,y,rot) in [(SX,SY,0),(SX+VW-r,SY,90),(SX+VW-r,SY+SB+VH-r,180),(SX,SY+SB+VH-r,270)]:
        s+=f'<svg width="{r}" height="{r}" style="position:absolute;left:{x}px;top:{y}px;transform:rotate({rot}deg)"><path d="M0 0H{r}A{r} {r} 0 0 0 0 {r}Z" fill="#f7f7f5"/></svg>'
    return s
CAPS=[ # (start,end in RAW seconds, headline, sub)
 (0.0,6.9,'Got your tiles?','Type them in. We&rsquo;ll find the mat.'),
 (6.9,9.0,'Your tiles + real mats','swiped together, right on your phone'),
 (9.0,12.3,'Tap Holiday + Green','the deck narrows to Christmas mats'),
 (12.3,13.2,'&#10005; Not the one','swipe it away'),
 (13.2,14.6,'&#9829; Evergreen &amp; Tartan','by Anders Ruff'),
 (14.6,20.4,'Pick your suitor','then make it a love triangle'),
 (20.4,28.0,'Now swipe the racks','&#9829; red &middot; &#10005; navy &middot; &#9829; green'),
 (28.0,31.6,'Make it official','&#9829;'),
 (31.6,99,'It&rsquo;s a match!','Save it, share it, shop it with code MAHJMATCH'),
]
def cap_html(h,s): return f'<div class="c" style="top:96px;color:{NAVY}"><div style="font:400 84px/1.04 Cap">{h}</div><div style="font:600 40px/1.25 PF;font-style:italic;color:{PINK};margin-top:16px;padding:0 60px">{s}</div></div>'
def foot_html(): return f'<div class="c" style="top:1872px;color:{NAVY};font:700 30px Bit;letter-spacing:.06em">mahjmatchmaker.com/find-your-match</div>'
os.makedirs(W,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':1920})
    def r(name,body,omit=True):
        open(W+'/_t.html','w').write(f'<html><head><meta charset=utf8><style>{CSS}</style></head><body>{body}</body></html>')
        pg.goto('file://'+W+'/_t.html'); pg.wait_for_timeout(500); pg.screenshot(path=f'{W}/{name}.png',omit_background=omit)
    r('top',top_html()+corners()+foot_html())
    for i,(a,e,h,s) in enumerate(CAPS): r(f'cap{i}',cap_html(h,s))
    # end card
    open(W+'/_t.html','w').write(f'<html><head><meta charset=utf8><style>{CSS}</style></head><body style="background:{NAVY}"><div class="c" style="top:640px;color:#fff"><div style="font:700 30px Bit;letter-spacing:6px;color:#f7b6c8">TRY IT FREE</div><div style="font:400 120px/1.05 Cap;margin-top:30px">{FYM(120)}</div><div style="font:600 46px/1.3 PF;font-style:italic;color:#f7b6c8;margin-top:30px;padding:0 90px">Your tiles. The mats that love them.<br>Racks too.</div><div style="font:700 38px Bit;margin-top:70px">mahjmatchmaker.com</div><div style="font:700 30px Bit;margin-top:18px;color:#f7b6c8">link in bio</div></div></body></html>')
    pg.goto('file://'+W+'/_t.html'); pg.wait_for_timeout(500); pg.screenshot(path=W+'/end.png')
    b.close()
raw='/dev/shm/w/rec/raw.mp4'
dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',raw]))
T=dur/SP
inp=['-f','lavfi','-i',f'color=c={CREAM}:s=1080x1920:r=30:d={T}','-i',raw,'-i',W+'/top.png']+sum([['-i',f'{W}/cap{i}.png'] for i in range(len(CAPS))],[])
fc=f"[1:v]setpts=PTS/{SP},scale={VW}:{VH}[v];[0:v][v]overlay={SX}:{SY+SB}:shortest=1[a];[a][2:v]overlay=0:0[b0]"
for i,(a,e,h,s) in enumerate(CAPS):
    fc+=f";[b{i}][{i+3}:v]overlay=0:0:enable='between(t,{a/SP:.2f},{min(e,dur)/SP:.2f})'[b{i+1}]"
subprocess.run(['ffmpeg','-loglevel','error','-y',*inp,'-filter_complex',fc,'-map',f'[b{len(CAPS)}]','-t',f'{T:.2f}','-c:v','libx264','-crf','20','-pix_fmt','yuv420p',W+'/main.mp4'],check=True)
subprocess.run(['ffmpeg','-loglevel','error','-y','-loop','1','-t','2.5','-i',W+'/end.png','-vf','fps=30,format=yuv420p','-c:v','libx264','-crf','20',W+'/end.mp4'],check=True)
open(W+'/cat.txt','w').write(f"file '{W}/main.mp4'\nfile '{W}/end.mp4'\n")
os.makedirs(D+'/reel',exist_ok=True)
subprocess.run(['ffmpeg','-loglevel','error','-y','-f','concat','-safe','0','-i',W+'/cat.txt','-c:v','libx264','-crf','23','-preset','slow','-pix_fmt','yuv420p','-movflags','+faststart',D+'/reel/fym-how-it-works-reel.mp4'],check=True)
print('ok',T+2.5)
