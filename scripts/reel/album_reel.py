"""Catch-up album reel from an album's own match cards (Tiffany, Oct 13). Usage: album_reel.py "<tile>" outdir [n_cards]"""
import json,sys,os,subprocess,io,urllib.request
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'/home/claude/mahjmatchmaker-data/scripts/matcard')
import matcard as M
R='/home/claude/mahjmatchmaker-data/'
tile=sys.argv[1];out=sys.argv[2];N=int(sys.argv[3]) if len(sys.argv)>3 else 8
MUSIC=sys.argv[4] if len(sys.argv)>4 else None  # royalty-free track; cuts land on its beats
BEATS=None
if MUSIC:
    import librosa
    y,sr=librosa.load(MUSIC,sr=22050,duration=60);_,bf=librosa.beat.beat_track(y=y,sr=sr);BEATS=list(librosa.frames_to_time(bf,sr=sr))
os.makedirs(out,exist_ok=True)
A=[x for x in json.load(open(R+'work/albums.json')) if x['tile']==tile][0]
NOCODE=tile=='Coquette'  # Coquette isn't eligible for MAHJMATCH; never pair the code with it
W,H,FPS=1080,1920,30;CREAM=(246,233,223)
def fetch(u,fn):
    p=f'{out}/{fn}'
    if not os.path.exists(p): subprocess.run(['curl','-sS','-o',p,u+'?format=1500w'],check=True)
    return Image.open(p).convert('RGB')
cover=fetch(A['cover'],'cover.jpg')
cards=[fetch(c['img'],f'c{i:02d}.jpg') for i,c in enumerate(A['cards'][:N])]
slug=tile.lower().replace(' ','-')
# overlays rendered as HTML (brand fonts)
F=M.F
head=f"""<!doctype html><html><head><meta charset=utf8><style>
{M.font('Alfa','fontsource-alfa-slab-one-5.3.0/package/files/alfa-slab-one-latin-400-normal.woff2')}
{M.font('PlayI','fontsource-playfair-display-5.3.0/package/files/playfair-display-latin-400-italic.woff2')}
@font-face{{font-family:'BitterB';src:url(file://{F}fontsource-bitter-5.3.0/package/files/bitter-latin-700-normal.woff2)}}
@font-face{{font-family:'Bitter';src:url(file://{F}fontsource-bitter-5.3.0/package/files/bitter-latin-400-normal.woff2)}}
*{{margin:0;box-sizing:border-box}}body{{width:1080px;height:1920px;background:transparent;position:relative;font-family:Bitter}}
.t{{position:absolute;left:0;right:0;text-align:center;font-family:BitterB;color:#054689;letter-spacing:.22em;font-size:34px}}
.end{{position:absolute;inset:0;background:#f6e9df;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:34px;padding:220px 60px 300px}}
.end img{{width:760px}}.big{{font-family:Alfa;font-size:96px;color:#d9405d;text-shadow:4px 4px 0 #fff;text-align:center;line-height:1.02;text-transform:uppercase}}
.sm{{font-family:PlayI;font-size:46px;text-align:center;color:#2a2036}}.web{{font-family:BitterB;font-size:52px;color:#054689}}
.pill{{background:#054689;color:#fff;font-family:BitterB;font-size:36px;padding:16px 40px;border-radius:50px}}.bio{{font-family:BitterB;font-size:34px;color:#6b5a77;letter-spacing:.1em}}
</style></head><body>"""
logo=M.b64(R+'assets/brand/mahjmatchmaker-wordmark-notag.png',fmt='PNG')
n=len(A['cards'])
pages={'top':head+f"<div class=t style='top:150px'>TIFFANY'S {tile.upper()} MATCHES</div><div class=t style='top:1700px;font-size:30px;letter-spacing:.06em'>All {n} matches at mahjmatchmaker.com</div></body></html>",
 'end':head+f"<div class=end><img src='{logo}'><div class=sm>Every {tile} match, all in one place</div><div class=big>{n} MATCHES<br>FOR {tile}</div><div class=web>mahjmatchmaker.com</div>"+("" if NOCODE else "<div class=pill>Use code MAHJMATCH to save 10%</div>")+"<div class=bio>LINK IN BIO</div></div></body></html>"}
for k,h in pages.items(): open(f'{out}/ov-{k}.html','w').write(h)
js=f"""const {{ chromium }} = require('playwright');(async()=>{{const b=await chromium.launch();for(const k of ['top','end']){{const p=await b.newPage({{viewport:{{width:1080,height:1920}}}});await p.goto('file://{out}/ov-'+k+'.html');await p.waitForTimeout(500);await p.screenshot({{path:'{out}/ov-'+k+'.png',omitBackground:true}});await p.close();}}await b.close();}})();"""
open(f'{out}/ov.js','w').write(js);subprocess.run(['node',f'{out}/ov.js'],check=True)
top=Image.open(f'{out}/ov-top.png').convert('RGBA');end=Image.open(f'{out}/ov-end.png').convert('RGB')
ease=lambda x:1-(1-x)**3
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-movflags','+faststart',f'{out}/{slug}-reel.mp4'],stdin=subprocess.PIPE)
def emit(f): p.stdin.write(f.tobytes())
prev=None
def blend(a,b,t): return Image.blend(a,b,t)
# cover full-bleed with slow zoom (2.2s)
def dur(a,b,default):
    if not BEATS: return int(default*FPS)
    return int(round((BEATS[b]-BEATS[a])*FPS))
seg=[0,4]+[4+2*(k+1) for k in range(len(cards))];seg.append(seg[-1]+6)
frames=dur(0,4,2.2)
for i in range(frames):
    s=1920/cover.height*(1+0.05*i/frames);sz=(int(cover.width*s),int(cover.height*s));im=cover.resize(sz,Image.BILINEAR)
    l=(sz[0]-W)//2;t=(sz[1]-H)//2;f=im.crop((l,t,l+W,t+H));emit(f);prev=f
# cards (1.2s each), card full width centered, gentle zoom, 6-frame crossfade
for ci_,c in enumerate(cards):
    frames=dur(seg[ci_+1],seg[ci_+2],1.2)
    for i in range(frames):
        s=1+0.035*i/frames;cw,ch=int(W*s),int(1350*s);ci=c.resize((cw,ch),Image.BILINEAR)
        f=Image.new('RGB',(W,H),CREAM);f.paste(ci,((W-cw)//2,285-(ch-1350)//2));f.paste(top,(0,0),top)
        if i<6 and prev is not None: f=blend(prev,f,(i+1)/6)
        emit(f)
    prev=f
# end card fade in
frames=dur(seg[-2],seg[-1],2.8)+(int(1.0*FPS) if BEATS else 0)
for i in range(frames):
    f=end if i>=8 else blend(prev,end,(i+1)/8);emit(f)
p.stdin.close();p.wait()
if MUSIC:
    src=f'{out}/{slug}-reel.mp4';dst=f'{out}/{slug}-reel-music.mp4'
    d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',src]))
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',src,'-ss',str(BEATS[0]),'-i',MUSIC,'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-af',f'afade=t=in:d=0.3,afade=t=out:st={d-1.2}:d=1.2','-t',str(d),'-movflags','+faststart',dst],check=True);print(dst)
else: print(out+'/'+slug+'-reel.mp4')
