"""Story swipe-through frames for a new mat (Tiffany, Oct 13). 1080x1920, text kept out of top 200 / bottom 220.
Usage: story_seq.py spec.json takes.json outdir"""
import json,sys,os
sys.path.insert(0,os.path.dirname(__file__))
import matcard as M
c=json.load(open(sys.argv[1])); T=json.load(open(sys.argv[2]))['takes']; out=sys.argv[3]
mat=M.b64(c['mat_path'],'JPEG',1400); logo=M.b64(M.ROOT+'/assets/brand/mahjmatchmaker-wordmark-notag.png',fmt='PNG'); flame=M.b64(M.ROOT+'/assets/brand/flame-heart.png',size=120)
IDX=json.load(open(M.ROOT+'/assets/tiles/album/index.json'))
def tile(n): return M.b64(M.ROOT+'/'+IDX[n]['file'],size=900)
F=M.F;col=c['color']
css=f"""<!doctype html><html><head><meta charset=utf8><style>
{M.font('Alfa','fontsource-alfa-slab-one-5.3.0/package/files/alfa-slab-one-latin-400-normal.woff2')}
{M.font('PlayI','fontsource-playfair-display-5.3.0/package/files/playfair-display-latin-400-italic.woff2')}
{M.font('Bitter','fontsource-bitter-5.3.0/package/files/bitter-latin-400-normal.woff2')}
@font-face{{font-family:'BitterB';src:url(file://{F}fontsource-bitter-5.3.0/package/files/bitter-latin-700-normal.woff2)}}
*{{box-sizing:border-box;margin:0}}body{{width:1080px;height:1920px;background:#f6e9df;font-family:Bitter;color:#2a2036;overflow:hidden;position:relative}}
.wrap{{position:absolute;left:0;right:0;top:200px;bottom:220px;padding:0 40px;display:flex;flex-direction:column;align-items:center;justify-content:space-between}}
.logo{{height:62px}}.eb{{font-family:BitterB;letter-spacing:.26em;font-size:32px;color:#054689;display:flex;align-items:center;gap:12px;text-align:center}}.eb img{{height:38px}}
h1{{font-family:Alfa;font-size:132px;line-height:.95;color:{col};text-shadow:5px 5px 0 #fff;text-transform:uppercase;text-align:center}}
h2{{font-family:Alfa;font-size:92px;line-height:1;color:{col};text-shadow:4px 4px 0 #fff;text-transform:uppercase;text-align:center}}
.by{{font-family:PlayI;font-size:44px;text-align:center}}
.mat{{border-radius:24px;background:url({mat}) center/cover;box-shadow:0 12px 34px rgba(42,32,54,.2);position:relative;flex:none}}
.pile{{position:absolute;right:-18px;bottom:-26px;border-radius:22px;background:center/cover;border:8px solid #fff;box-shadow:0 12px 30px rgba(42,32,54,.3)}}
.q{{font-family:PlayI;font-size:46px;line-height:1.25;text-align:center;max-width:960px}}.q b{{font-family:BitterB;font-style:normal}}
.nm{{font-family:BitterB;font-size:44px;text-align:center}}.nm small{{display:block;font-family:Bitter;font-size:30px;color:#6b5a77;margin-top:4px}}
.sig{{font-family:BitterB;font-size:30px;color:#054689;letter-spacing:.08em}}
.cue{{font-family:BitterB;font-size:32px;color:#054689;background:#fff8f2;border-radius:40px;padding:14px 34px}}
.pill{{background:#054689;color:#fff;font-family:BitterB;font-size:30px;padding:14px 34px;border-radius:40px}}
.retired{{display:inline-block;background:#6b5a77;color:#fff;font-family:BitterB;font-size:26px;letter-spacing:.18em;padding:6px 16px;border-radius:8px;margin-top:8px}}
"""
def page(body,extra=''): return css+extra+"</style></head><body><div class=wrap>"+body+"</div></body></html>"
eb=lambda t:f"<div class=eb><img src='{flame}'>{t}<img src='{flame}'></div>"
frames={}
# 1 hook
frames['1-hook']=page(f"""<img class=logo src='{logo}'>{eb('NEW FROM OH MY MAHJONG')}<h1>{c['name']}</h1>
<div class=mat style='width:900px;height:900px'></div><div class=cue>What tiles go with it? Tap for my matches →</div>""")
# 2/4/5 match frames
def match(key,label,eyebrow,quote,retired=False):
    return page(f"""{eb(eyebrow)}<h2>{c['name']} + {label}</h2>
<div class=mat style='width:790px;height:790px;margin-right:30px'><div class=pile style='width:390px;height:390px;background-image:url({tile(key)})'></div></div>
<div><div class=nm>{label} <small>Oh My Mahjong tiles</small></div>{"<div style='text-align:center'><span class=retired>RETIRED · FROM THE VAULT</span></div>" if retired else ""}</div>
<div class=q>“{quote}”</div><div class=sig>— Tiffany, your Mahj Matchmaker</div>""")
frames['2-limoncello']=match('Limoncello','Limoncello',"TIFFANY'S TOP PICK","Oh Limoncello, you are missed. It's almost as though this mat was made for you.",True)
# 3 matching secret
frames['3-secret']=page(f"""{eb('THE MATCHING SECRET')}<h2 style='font-size:84px'>Why it pops</h2>
<div style='display:flex;align-items:center;gap:40px'>
 <div style='width:380px;height:380px;border-radius:50%;background:conic-gradient(#e8344a,#f08a24,#f7d33c,#a8d63a,#2fae5f,#22a6b3,#3a6fd8,#7b4fc9,#c23fa0,#e8344a);position:relative;box-shadow:0 10px 26px rgba(0,0,0,.18)'>
  <div style='position:absolute;inset:95px;border-radius:50%;background:#f6e9df'></div>
  <div style='position:absolute;left:186px;top:6px;width:8px;height:368px;background:#2a2036;transform:rotate(-40deg);transform-origin:center;border-radius:4px'></div>
 </div>
 <div style='display:flex;flex-direction:column;gap:22px'>
  <div style='display:flex;align-items:center;gap:18px'><i style='width:96px;height:96px;border-radius:50%;background:#e04a6a;display:block'></i><div class=nm style='text-align:left;font-size:38px'>Magenta<small>the mat's center</small></div></div>
  <div style='font-family:BitterB;font-size:40px;color:#054689;padding-left:26px'>↕ opposites</div>
  <div style='display:flex;align-items:center;gap:18px'><i style='width:96px;height:96px;border-radius:50%;background:#AFE745;display:block'></i><div class=nm style='text-align:left;font-size:38px'>Lime green<small>maximum pop</small></div></div>
 </div></div>
<div class=q style='font-size:42px'>Find the main color in the center of the mat, jump to its <b>opposite on the color wheel</b>, then match how light or bright it is.</div>
<div style='display:flex;gap:22px;align-items:center'><div style='width:250px;height:250px;border-radius:18px;background:url({tile('Limoncello')}) center/cover;border:6px solid #fff;box-shadow:0 8px 20px rgba(0,0,0,.2)'></div>
<div style='display:flex;flex-direction:column;gap:12px'><div style='background:#AFE745;border-radius:10px;padding:16px 24px;font-family:BitterB;font-size:34px;box-shadow:inset 0 -6px 0 rgba(0,0,0,.12)'>Lime Green racks</div><div class=nm style='font-size:32px;text-align:left'>+ Limoncello tiles<small>both land opposite magenta</small></div></div></div>""")
frames['4-moonlight']=match('Moonlight','Moonlight',"TIFFANY'S TOP PICK","Moonlight's blues pick up Larkspur's periwinkle border and the deep blue birds.")
frames['5-vault']=match('Spring Love (retired)','Spring Love',"HAVE AN OLDER SET?",T['vault-spring-love']['short'],True)
os.makedirs(out,exist_ok=True)
for k,h in frames.items(): open(f"{out}/larkspur-{k}.html",'w').write(h)
