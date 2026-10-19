"""Tile Set Profile episode reel (1080x1920, silent; doc 81 'new episode model', DRAFT):
  INTRO (value first): series tag -> full-screen hero photo -> her colors full-screen -> her color card full-screen -> dating profile
  SKIT (cheek second): 'Help me match <set>' -> she swipes right on her top 3 (isolated tile pile + flat mat photo, no match cards)
  -> fast flip of more album matches -> end card.
Usage: python3 reel.py papaya-spritz <outdir>  then  node render.js <outdir>/reel.html <outdir>/reel.json <out.mp4> 30"""
import sys, os, json, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
key = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
P, S = load(key); e = html.escape; ACC = S['col']
HERO = url('assets/launches/omm-papaya-spritz-tiles/05.jpg'); TILE = url(S['tile'])
CARD = url(f'assets/colorcards/{key}/00-{key}-mahjong-tiles-color-guide-mobile.jpg')
MATS = {k: url(v) for k, v in S['mat_imgs'].items()}
FLIPD = R + f'assets/colorcards/{key}/mats/flip/'
FLIP = [url(FLIPD + f) for f in ['haven-britt-mills.jpg', 'coralia-virora-mahjong.jpg', 'flora-belle-anders-ruff.jpg', 'bams-and-bubbly-anders-ruff.jpg',
                                  'enchanted-britt-mills.jpg', 'savannah-britt-mills.jpg', 'cheetah-couture-bespoke-mahjong.jpg', 'fruit-stand-middle-and-main-mahjong.jpg']]
FLIPN = ['Haven', 'Coralia', 'Flora Belle', 'Bams & Bubbly', 'Enchanted', 'Savannah', 'Cheetah Couture', 'Fruit Stand']
RACK = {'Bird & Bamboo Lavender': url(f'assets/colorcards/{key}/racks/bird-and-bamboo-lavender.png'),
        'Peace Love Mahjong Chartreuse': url('assets/racks/card/peace-love-mahjong-chartreuse.png'), 'Peace Love Mahjong Oak': url('assets/racks/card/peace-love-mahjong-oak.png')}
LOGO = url('assets/brand/mahjmatchmaker-wordmark-notag.png'); HEART = url('assets/brand/flame-heart.png')
backs = P['her_colors']['backs']; faces = P['her_colors']['faces']; l1, l2 = P['profile_line']
DUR = 40.0
short = {'Heiress': 'pink + papaya', 'Press for Mahjong': 'papaya, right in the middle', 'Greenly': 'opposites attract'}

bands = ''.join(f'<div class="band" style="background:{h};left:{i * 360}px"><div class="bl"><div class="bn">{e(n.upper())}</div><div class="br">{e(r)}</div><div class="bh">{h.upper()}</div></div></div>' for i, (n, h, r) in enumerate(backs))
fdots = ''.join(f'<div class="fd"><i style="background:{h}"></i><span>{e(n.upper())}</span></div>' for n, h in faces)
types = ''.join(f"""<div class="ty"><div class="tc"><i style="background:{S['backs'][0][1]}"></i><b>+</b>{''.join(f'<i style="background:{c}"></i>' for c in t['chips'])}</div>
<div><div class="tl">{e(t['label'])}</div><div class="tw">{e(t['mat'])}: {e(t['why'])}</div></div></div>""" for t in P['her_type'])
racks = ''.join(f'<div class="rk"><img src="{RACK[r["name"]]}"><span>{e(r["name"].replace("Peace Love Mahjong", "PLM").replace("Bird & Bamboo", "B&B"))}</span></div>' for r in P['racks'])
dates = ''.join(f"""<div class="mat" id="m{i}"><div class="mi" style="background-image:url({MATS[m]})"></div><div class="stamp">MATCH &hearts;</div>
<div class="mn"><span class="pf">{e(m)}</span><small>{e(next(t['brand'] for t in P['her_type'] if t['mat'] == m))}</small></div><div class="why">{e(short[m])}</div></div>""" for i, m in enumerate(P['first_dates']))
flips = ''.join(f'<div class="fl" id="f{i}"><div class="mi" style="background-image:url({u})"></div><div class="fln">{e(n)}</div></div>' for i, (u, n) in enumerate(zip(FLIP, FLIPN)))

H = f"""<!doctype html><html><head><meta charset=utf8><style>{css(1080, 1920, ACC)}
.sc{{position:absolute;inset:0;opacity:0;overflow:hidden}}
#tag{{background:var(--cream);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}}
#hero .ph{{position:absolute;inset:0}}
#hero .cd{{position:absolute;left:0;right:0;bottom:0;height:720px;background:var(--cream);border-radius:56px 56px 0 0;padding:70px 80px;text-align:left}}
.band{{position:absolute;top:0;width:360px;height:1920px}}
.bl{{position:absolute;left:34px;bottom:520px;color:#fff;text-shadow:0 2px 10px rgba(0,0,0,.12)}}
.bn{{font:700 46px Bit;letter-spacing:.08em}}.br{{font:400 32px Bit}}.bh{{font:600 30px Bit;opacity:.9;letter-spacing:.06em;margin-top:6px}}
#colors .top{{position:absolute;top:230px;left:0;right:0;text-align:center}}
#colors .strip{{position:absolute;left:60px;right:60px;bottom:200px;background:var(--cream);border-radius:34px;padding:34px 30px;display:flex;justify-content:space-around}}
.fd{{text-align:center}}.fd i{{display:block;width:120px;height:120px;border-radius:50%;margin:0 auto 12px;box-shadow:0 0 0 6px #fff}}.fd span{{font:700 26px Bit;letter-spacing:.06em}}
#card{{background:var(--cream)}}#card img{{position:absolute;left:0;top:150px;width:1080px;height:1620px}}
#prof .bg{{position:absolute;inset:-40px;background:url({HERO}) center/cover;filter:blur(18px) saturate(1.1);opacity:.85}}
#prof .pc{{position:absolute;left:60px;right:60px;top:160px;bottom:200px;background:var(--paper);border-radius:40px;padding:56px 56px;box-shadow:0 20px 60px rgba(6,40,90,.25)}}
.lab{{font:700 28px Bit;letter-spacing:.2em;color:var(--pink);text-transform:uppercase;margin-top:44px}}
.ty{{display:flex;gap:20px;align-items:flex-start;margin-top:20px}}.tc{{display:flex;gap:6px;align-items:center;flex:0 0 170px;padding-top:8px}}.tc i{{width:40px;height:40px;border-radius:50%;box-shadow:0 0 0 3px #fff}}.tc b{{font:700 26px Bit;color:var(--pink)}}
.tl{{font:700 36px Bit}}.tw{{font:400 32px/1.32 Bit;color:#2c3e63;margin-top:2px}}
.rk{{display:flex;align-items:center;gap:18px;margin-top:14px}}.rk img{{width:560px;height:70px;object-fit:fill}}.rk span{{font:600 30px Bit;color:#2c3e63}}
#help{{background:var(--cream);text-align:center;display:flex;flex-direction:column;align-items:center;justify-content:center}}
#swipe{{background:var(--cream)}}
#swipe .tile{{position:absolute;left:50%;top:250px;width:300px;height:300px;margin-left:-150px;border-radius:50%;background:url({TILE}) center/cover;box-shadow:0 0 0 10px #fff,0 14px 34px rgba(6,40,90,.2)}}
#swipe .tn{{position:absolute;top:580px;left:0;right:0;text-align:center}}
.mat{{position:absolute;left:150px;top:720px;width:780px;opacity:0}}.mat .mi,.fl .mi{{width:780px;height:780px;border-radius:30px;background-size:cover;background-position:center;box-shadow:0 18px 44px rgba(6,40,90,.22)}}
.stamp{{position:absolute;top:40px;right:-20px;transform:rotate(12deg);background:var(--pink);color:#fff;font:400 54px Capra;padding:10px 30px;border-radius:16px;border:5px solid #fff;opacity:0}}
.mn{{text-align:center;margin-top:30px}}.mn .pf{{font-size:66px;font-weight:600}}.mn small{{display:block;font:400 30px Bit;color:#5a6b85}}
.why{{text-align:center;font:400 52px Hand;color:var(--pink);margin-top:6px}}
.fl{{position:absolute;left:150px;top:720px;width:780px;opacity:0}}.fln{{text-align:center;font:600 54px PF;font-style:italic;margin-top:28px}}
#cnt{{position:absolute;left:0;right:0;top:1640px;text-align:center;font:400 64px Capra;color:var(--acc);opacity:0}}
#end{{background:var(--cream);text-align:center}}
#end .cc{{position:absolute;top:470px;left:0;right:0;display:flex;justify-content:center;align-items:center;gap:30px}}
#end .c{{width:330px;height:330px;border-radius:50%;background-size:cover;background-position:center;box-shadow:0 0 0 10px #fff,0 14px 34px rgba(6,40,90,.2)}}
</style></head><body>
<div class="sc" id="tag"><img src="{HEART}" style="width:120px"><div class="caps" style="margin-top:30px;font-size:30px">Mahj Matchmaker 2.0 · Season 2</div>
 <div class="cap" style="font-size:92px;margin-top:22px">The new girl<br>on the block</div><div class="hand" style="font-size:58px;margin-top:22px">just moved in this week</div></div>
<div class="sc" id="hero"><div class="ph" id="hp" style="background-image:url({HERO})"></div>
 <div class="cd" id="hc"><div class="caps" style="color:var(--pink);font-size:26px">New from {e(P['brand'])}</div><div class="hand" style="font-size:90px;line-height:1;margin-top:14px">Introducing</div>
 <div class="cap" style="font-size:122px;color:var(--acc);white-space:nowrap;margin-top:6px">{e(P['name'])}</div><div class="pf" style="font-size:46px;margin-top:26px">{e(P['bio'])}</div></div></div>
<div class="sc" id="colors">{bands}<div class="top" id="ct"><div class="cap" style="font-size:120px;color:#fff;text-shadow:0 4px 18px rgba(0,0,0,.18)">Her colors</div></div>
 <div class="strip" id="cs">{fdots}</div></div>
<div class="sc" id="card"><div class="caps" style="position:absolute;top:70px;left:0;right:0;text-align:center;font-size:26px">The Tile Edit · her color card</div><img id="ci" src="{CARD}"></div>
<div class="sc" id="prof"><div class="bg"></div><div class="pc">
 <div class="caps" style="font-size:24px;color:#5a6b85">{e(P['name'])} · the dating profile</div>
 <div class="pf" style="font-size:46px;line-height:1.22;margin-top:16px;font-weight:600" id="p0">{e(l1)}<br>{e(l2)}</div>
 <div id="p1"><div class="lab">Her type, and why</div>{types}</div>
 <div id="p2"><div class="lab">Racks she's into</div>{racks}</div>
 <div id="p3"><div class="lab">Dealbreaker</div><div class="tw" style="font-size:32px;margin-top:10px">{e(P['dealbreaker'])}</div></div>
</div></div>
<div class="sc" id="help"><div class="caps" style="font-size:28px">Now the fun part</div><div class="cap" style="font-size:120px;margin-top:24px">Help me match<br><span style="color:var(--acc)">{e(P['name'])}</span></div><div class="hand" style="font-size:60px;margin-top:26px">she's new here. be nice.</div></div>
<div class="sc" id="swipe"><div class="tile"></div><div class="tn"><span class="caps" style="font-size:26px">{e(P['name'])} swipes right on&hellip;</span></div>{dates}{flips}<div id="cnt">and she kept swiping&hellip;<br>{P['matches']} matches and counting</div></div>
<div class="sc" id="end"><div class="caps" style="position:absolute;top:240px;left:0;right:0;font-size:28px">Got a tile set looking for love?</div>
 <div class="cap" style="position:absolute;top:300px;left:0;right:0;font-size:76px;white-space:nowrap">Let the MAT-ching begin</div>
 <div class="cc"><div class="c" id="e1" style="background-image:url({TILE})"></div><div style="font:400 100px Capra;color:var(--pink)" id="eh">&hearts;</div><div class="c" id="e2" style="background-image:url({MATS[P['first_dates'][0]]})"></div></div>
 <div style="position:absolute;top:900px;left:0;right:0"><div class="pill" style="background:var(--pink);font-size:36px">See all of {e(P['name'].split()[0])}'s matches now · link in bio</div></div>
 <div style="position:absolute;top:1050px;left:0;right:0;font:700 40px Bit">Code <span style="color:var(--pink)">MAHJMATCH</span> at {e(P['brand'])}</div>
 <div style="position:absolute;top:1170px;left:140px;right:140px;background:#fff;border-radius:26px;padding:26px 30px;box-shadow:0 6px 18px rgba(6,40,90,.1)"><div style="font:700 30px Bit;letter-spacing:.06em">COMING 10.27 · FIND YOUR MATCH</div><div style="font:400 28px Bit;color:#2c3e63;margin-top:6px">match YOUR tiles to their perfect mat at mahjmatchmaker.com</div></div>
 <img src="{LOGO}" style="position:absolute;top:1400px;left:50%;width:600px;margin-left:-300px"></div>
<script>
const $=id=>document.getElementById(id);
const cl=(x,a,b)=>Math.max(a,Math.min(b,x)); const ease=x=>x<.5?2*x*x:1-Math.pow(-2*x+2,2)/2;
function vis(id,t,a,b,f){{f=f||.35;let o=0;if(t>=a&&t<=b)o=Math.min(1,(t-a)/f,(b-t)/f);$(id).style.opacity=cl(o,0,1);return t>=a&&t<=b}}
function render(t){{
 vis('tag',t,0,2.6);
 if(vis('hero',t,2.4,6.4)){{const k=(t-2.4)/4;$('hp').style.transform=`scale(${{1.04+k*.1}})`;$('hc').style.transform=`translateY(${{(1-ease(cl((t-2.6)/.6,0,1)))*700}}px)`}}
 if(vis('colors',t,6.2,10.4)){{document.querySelectorAll('.band').forEach((b,i)=>{{const p=ease(cl((t-6.3-i*.25)/.6,0,1));b.style.transform=`translateY(${{(1-p)*1920}}px)`}});
  $('ct').style.opacity=cl((t-7.0)/.4,0,1);const q=ease(cl((t-8.0)/.5,0,1));$('cs').style.transform=`translateY(${{(1-q)*500}}px)`}}
 if(vis('card',t,10.2,14.6)){{const k=(t-10.2)/4.4;$('ci').style.transform=`scale(${{1+k*.06}})`}}
 if(vis('prof',t,14.4,22.0)){{['p0','p1','p2','p3'].forEach((id,i)=>{{const a=14.6+[0,1.2,3.6,5.2][i];const p=ease(cl((t-a)/.5,0,1));$(id).style.opacity=p;$(id).style.transform=`translateY(${{(1-p)*30}}px)`}})}}
 vis('help',t,21.8,24.0);
 if(vis('swipe',t,23.8,35.4)){{
  for(let i=0;i<3;i++){{const a=24.0+i*2.9,b=a+2.9;const el=$('m'+i);let x=0,o=0;
   if(t>=a&&t<b){{const pin=ease(cl((t-a)/.45,0,1));const pout=ease(cl((t-(b-.4))/.4,0,1));x=(1-pin)*1100-pout*1100;o=1}}
   el.style.opacity=o;el.style.transform=`translateX(${{x}}px) rotate(${{x/60}}deg)`;
   const st=el.querySelector('.stamp');const s=cl((t-a-.9)/.25,0,1);st.style.opacity=s;st.style.transform=`rotate(12deg) scale(${{1.6-.6*s}})`}}
  const f0=32.7;for(let i=0;i<8;i++){{const a=f0+i*.32;$('f'+i).style.opacity=(t>=a&&(t<a+.32||(i==7&&t<35.4)))?1:0}}
  $('cnt').style.opacity=cl((t-32.8)/.3,0,1)}}
 if(vis('end',t,35.2,{DUR})){{const w=Math.sin(t*5);$('e1').style.transform=`rotate(${{w*5}}deg) translateY(${{w*8}}px)`;$('e2').style.transform=`rotate(${{-w*5}}deg) translateY(${{-w*8}}px)`;$('eh').style.transform=`scale(${{1+.12*Math.abs(Math.sin(t*4))}})`}}
}}
render(0);
</script></body></html>"""
open(OUT + '/reel.html', 'w').write(H); json.dump({'dur': DUR}, open(OUT + '/reel.json', 'w'))
print('ok', OUT)
