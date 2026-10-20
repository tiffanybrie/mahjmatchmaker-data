"""'Introducing <set>' Instagram carousel (1080x1350): the set's PROFILE, black-book style (doc 81 DRAFT).
Oct 19 v2: 7 slides. Profile intro (hero / her colors / racks she's into) -> made for each other (official OMM pair) -> her OMM sisters
-> strong match potential (true top 3, every brand) -> see all + code. Non-OMM launches: no omm_launch block = no pair / sisters slides.
Usage: python3 carousel.py papaya-spritz <outdir>   -> writes slide HTML, then run shot.js to render JPGs."""
import sys, os, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

key = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
P, S = load(key)
ACC = S['col']; L = P['launch'] = {'hero': 'assets/launches/omm-papaya-spritz-tiles/05.jpg', 'single': 'assets/launches/omm-papaya-spritz-tiles/06.jpg',
                                    'all': 'assets/launches/omm-papaya-spritz-tiles/01.jpg'}
MATS = S['mat_imgs']; RACK = {'Bird & Bamboo Lavender': 'assets/colorcards/papaya-spritz/racks/bird-and-bamboo-lavender.png',
                              'Peace Love Mahjong Chartreuse': 'assets/racks/card/peace-love-mahjong-chartreuse.png',
                              'Peace Love Mahjong Oak': 'assets/racks/card/peace-love-mahjong-oak.png',
                              'Middle & Main Scalloped Beechwood': 'assets/racks/card/middle--main-scalloped-beechwood.png'}
LOGO = url('assets/brand/mahjmatchmaker-wordmark-notag.png'); TILE = url(S['tile'])
e = html.escape
OMM = P.get('omm_launch'); NS = 7 if OMM else 5

def page(i, body, extra=''):
    dots = ''.join(f'<i style="background:{ACC if j == i else "rgba(6,69,135,.2)"}"></i>' for j in range(1, NS + 1))
    return f"""<!doctype html><html><head><meta charset=utf8><style>{css(1080, 1350, ACC)}
.dots{{position:absolute;bottom:34px;left:0;right:0;display:flex;gap:10px;justify-content:center}}.dots i{{width:12px;height:12px;border-radius:50%;display:block}}
.hd{{position:absolute;top:58px;left:72px;right:72px;display:flex;justify-content:space-between;align-items:baseline}}
.hd .caps{{font-size:19px;color:#5a6b85}}{extra}</style></head><body><div style="position:relative;width:1080px;height:1350px">{body}
<div class="dots">{dots}</div></div></body></html>"""

def head(t):
    return f'<div class="hd"><span class="caps">{e(P["name"])} · her profile</span><span class="caps">{t}</span></div>'

def VER(n):  # verified-match heart badge (pink heart, white check)
    return f'<svg width="{n}" height="{n}" viewBox="0 0 24 24" style="flex:0 0 auto"><path d="M12 21.5C5.5 16.6 2 13.2 2 8.9 2 5.9 4.4 3.5 7.3 3.5c1.9 0 3.6 1 4.7 2.5 1.1-1.5 2.8-2.5 4.7-2.5 2.9 0 5.3 2.4 5.3 5.4 0 4.3-3.5 7.7-10 12.6z" fill="#d6608c" stroke="#fff" stroke-width="1.2"/><path d="M7.6 11.3l3 3 5.8-5.8" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def HT(n, c='var(--pink)'):
    return f'<svg width="{n}" height="{n}" viewBox="0 0 24 24" style="flex:0 0 auto;vertical-align:-3px"><path d="M12 21.5C5.5 16.6 2 13.2 2 8.9 2 5.9 4.4 3.5 7.3 3.5c1.9 0 3.6 1 4.7 2.5 1.1-1.5 2.8-2.5 4.7-2.5 2.9 0 5.3 2.4 5.3 5.4 0 4.3-3.5 7.7-10 12.6z" fill="{c}"/></svg>'

sw = [b[1] for b in P['her_colors']['backs']] + [f[1] for f in P['her_colors']['faces']]
l1, l2 = P['profile_line']

# 1 hero: full-bleed real product photo, cream profile card
s1 = page(1, f"""
<div class="ph" style="position:absolute;inset:0 0 520px 0;background-image:url({url(L['hero'])})"></div>
<div style="position:absolute;left:0;right:0;bottom:0;height:560px;background:var(--cream);border-radius:46px 46px 0 0;padding:58px 72px 0">
 <div style="display:flex;justify-content:space-between;align-items:center"><div class="caps" style="color:var(--pink);font-size:20px">The new girl on the block · {e(P['brand'])}</div>
 <div style="display:flex;align-items:center;gap:8px;border:2px solid var(--pink);border-radius:99px;padding:6px 16px 6px 10px;background:#fff">{VER(30)}<span style="font:700 17px Bit;letter-spacing:.14em;color:var(--pink)">{P['matches']} MATCHES</span></div></div>
 <div class="hand" style="font-size:66px;margin-top:10px;line-height:1">Introducing</div>
 <div class="cap" style="font-size:128px;color:var(--acc);margin-top:2px;white-space:nowrap">{e(P['name'])}</div>
 <div class="pf" style="font-size:38px;line-height:1.3;margin-top:20px">{e(l1)}<br>{e(l2)}</div>
 <div style="display:flex;gap:12px;margin-top:26px;align-items:center">{''.join(f'<span style="width:38px;height:38px;border-radius:50%;background:{c};box-shadow:0 0 0 3px #fff"></span>' for c in sw)}
  <span class="hand" style="font-size:40px;margin-left:auto;color:var(--navy)">swipe for her profile &rarr;</span></div>
</div>""", '.dots{bottom:30px}')

# 2 her colors: designer black-book chips
chips_b = ''.join(f"""<div class="chip" style="width:290px"><div class="sw" style="height:190px;background:{h}"></div><div class="t"><div class="n">{e(n.upper())}</div><div class="r">{e(r)}</div><div class="h">{h.upper()}</div></div></div>""" for n, h, r in P['her_colors']['backs'])
chips_f = ''.join(f"""<div class="chip" style="width:210px"><div class="sw" style="height:118px;background:{h}"></div><div class="t" style="padding:10px 12px 12px"><div class="n" style="font-size:21px">{e(n.upper())}</div><div class="h">{h.upper()}</div></div></div>""" for n, h in P['her_colors']['faces'])
s2 = page(2, head('1 · her colors') + f"""
<div style="position:absolute;top:120px;left:72px;right:72px">
 <div class="cap" style="font-size:96px">Her colors</div>
 <div class="pf" style="font-size:34px;margin-top:10px;color:#3c4f73;max-width:900px">Papaya backs, lavender and light lime layers. Clean brights, no dusty undertone.</div>
 <div class="caps" style="margin-top:44px;font-size:19px;color:#5a6b85">The backs</div>
 <div style="display:flex;gap:23px;margin-top:14px">{chips_b}</div>
 <div class="caps" style="margin-top:40px;font-size:19px;color:#5a6b85">The faces</div>
 <div style="display:flex;gap:13px;margin-top:14px">{chips_f}</div>
</div>
<div style="position:absolute;left:72px;right:72px;bottom:90px;display:flex;align-items:center;gap:34px">
 <div class="ph" style="flex:0 0 230px;height:230px;border-radius:50%;background-color:#fff;background-size:150%;background-image:url({url(L['single'])});box-shadow:0 0 0 8px #fff,0 10px 26px rgba(6,40,90,.16)"></div>
 <div><div class="hand" style="font-size:50px;line-height:1.05">see the layers?<br>lavender + light lime, under a papaya back.</div>
 <div style="font:400 24px/1.35 Bit;color:#2c3e63;margin-top:12px">Pull any of these into a mat or rack and she looks put-together.</div></div>
</div>""")

# 3 her type + why
rows = ''
for t in P['her_type']:
    rows += f"""<div style="display:flex;gap:34px;align-items:center;margin-top:30px">
 <div class="ph" style="flex:0 0 250px;height:250px;border-radius:18px;background-image:url({url(MATS[t['mat']])});box-shadow:0 8px 22px rgba(6,40,90,.16)"></div>
 <div style="flex:1">
  <div style="display:flex;gap:8px;align-items:center"><span style="width:30px;height:30px;border-radius:50%;background:{S['backs'][0][1]};box-shadow:0 0 0 3px #fff"></span><span style="font:700 26px Bit;color:var(--pink)">+</span>{''.join(f'<span style="width:30px;height:30px;border-radius:50%;background:{c};box-shadow:0 0 0 3px #fff"></span>' for c in t['chips'])}
   <span class="caps" style="font-size:19px;margin-left:8px">{e(t['label'])}</span></div>
  <div class="pf" style="font-size:36px;margin-top:10px;font-weight:600">{e(t['mat'])} <span style="font-weight:400;font-size:28px;color:#5a6b85">by {e(t['brand'])}</span></div>
  <div style="font:400 26px/1.35 Bit;margin-top:6px;color:#2c3e63">{e(t['why'])}</div>
 </div></div>"""
SL = (OMM or {}).get('strong_label', 'Strong match potential')
s3 = page(NS - 1, head(('5' if OMM else '3') + ' · top matches') + f"""
<div style="position:absolute;top:120px;left:72px;right:72px">
 <div class="cap" style="font-size:{76 if len(SL) > 18 else 96}px;white-space:nowrap">{e(SL)}</div>
 <div class="pf" style="font-size:32px;margin-top:8px;color:#3c4f73">Her top 3 of {P['matches']} matches, every brand, and why.</div>
 {rows}
 <div style="margin-top:38px;border:2px dashed rgba(214,96,140,.55);border-radius:18px;padding:20px 24px;background:rgba(255,255,255,.55)">
  <span class="caps" style="color:var(--pink);font-size:19px">Dealbreaker</span>
  <div style="font:400 25px/1.35 Bit;margin-top:6px">{e(P['dealbreaker'])}</div></div>
</div>""")

# 4 racks she's into
rk = ''
for r in P['racks']:
    b = next((x for x in ('Bird & Bamboo', 'Peace Love Mahjong', 'Middle & Main', 'Miss Mahjong', 'Mahjong Row & Co.', 'Bam Bird Boutique') if r['name'].startswith(x)), r['name'].split()[0]); c = r['name'][len(b) + 1:]
    rk += f"""<div style="margin-top:56px"><div style="display:flex;align-items:baseline;gap:14px"><span class="caps" style="font-size:18px;color:#8a6a80">{e(b)}</span><span class="pf" style="font-size:44px;font-weight:600">{e(c)}</span></div>
<img src="{url(RACK[r['name']])}" style="display:block;width:936px;height:96px;object-fit:fill;margin-top:10px;filter:drop-shadow(0 8px 10px rgba(6,40,90,.18))">
<div style="font:400 27px Bit;margin-top:10px;color:#2c3e63">{e(r['why'])}</div></div>"""
s4 = page(3, head("2 · racks she's into") + f"""
<div style="position:absolute;top:120px;left:72px;right:72px">
 <div class="cap" style="font-size:96px">Racks she's into</div>
 <div class="pf" style="font-size:32px;margin-top:8px;color:#3c4f73">Pull a layer color, or let a light wood stay out of her way.</div>
 {rk}
 <div class="hand" style="font-size:44px;margin-top:40px;color:var(--navy)">all three picked for her, not just any rack &hearts;</div>
 <div class="hand" style="font-size:40px;margin-top:6px;color:var(--pink)">now, who she&rsquo;s dating &rarr;</div>
</div>""")

if OMM:
    pr = OMM['pair']; PM = url(pr['img']); TOG = url(pr['together'])
    sp = page(4, head('3 · made for each other') + f"""
<div style="position:absolute;top:120px;left:72px;right:72px">
 <div class="cap" style="font-size:84px;white-space:nowrap">Made for each other</div>
 <div class="pf" style="font-size:34px;margin-top:8px;color:#3c4f73">Her official {e(pr['brand'])} pair: <b style="font-weight:600;color:var(--navy)">{e(pr['mat'])}</b></div>
 <div class="ph" style="margin-top:30px;height:640px;border-radius:24px;background-image:url({TOG});background-size:{'cover' if pr.get('together_fit')=='cover' else '150%'};background-position:{'center' if pr.get('together_fit')=='cover' else '52% 42%'};box-shadow:0 10px 26px rgba(6,40,90,.16);position:relative">
  <div style="position:absolute;left:18px;bottom:18px;background:rgba(255,255,255,.92);border-radius:99px;padding:8px 18px;font:600 20px Bit;color:var(--navy)">{e(pr.get('together_caption') or (P['name']+' on '+pr['mat']+', in '+pr['brand']+'’s own photo'))}</div></div>
 <div style="display:flex;align-items:center;gap:18px;margin-top:34px">
  <div class="ph" style="flex:0 0 170px;height:170px;border-radius:50%;background:#fff url({url(pr['circle']) if pr.get('circle') else TILE}) center/{'112%' if pr.get('circle') else 'cover'} no-repeat;box-shadow:0 0 0 6px #fff,0 8px 20px rgba(6,40,90,.16)"></div>
  <div style="flex:0 0 auto">{HT(54)}</div>
  <div class="ph" style="flex:0 0 210px;height:210px;border-radius:18px;background-image:url({PM});background-size:114%;box-shadow:0 8px 22px rgba(6,40,90,.16)"></div>
  <div style="flex:1;padding-left:6px"><div style="display:flex;align-items:center;gap:8px">{VER(30)}<span class="caps" style="font-size:17px;color:var(--pink)">Official pair</span></div>
   <div style="font:400 25px/1.35 Bit;margin-top:8px;color:#2c3e63">{e(pr['why'])}</div></div>
 </div>
</div>""")
    rows2 = ''
    for t in OMM['sisters']:
        vt = '<span style="margin-left:12px;font:700 15px Bit;letter-spacing:.14em;background:var(--navy);color:#fff;border-radius:99px;padding:5px 12px;vertical-align:8px">FROM THE VAULT</span>' if t.get('vault') else ''
        rows2 += f"""<div style="display:flex;gap:34px;align-items:center;margin-top:30px">
 <div class="ph" style="flex:0 0 240px;height:240px;border-radius:18px;background-image:url({url(t['img'])});box-shadow:0 8px 22px rgba(6,40,90,.16)"></div>
 <div style="flex:1"><div class="pf" style="font-size:42px;font-weight:600">{e(t['mat'])}{vt}</div>
  <div style="font:400 26px/1.35 Bit;margin-top:6px;color:#2c3e63">{e(t['why'])}</div></div></div>"""
    ss = page(5, head('4 · her OMM sisters') + f"""
<div style="position:absolute;top:120px;left:72px;right:72px">
 <div class="cap" style="font-size:96px">Her OMM sisters</div>
 <div class="pf" style="font-size:32px;margin-top:8px;color:#3c4f73">More {e(P['brand'])} mats from her album, in my order.</div>
 {rows2}
 <div class="hand" style="font-size:40px;margin-top:34px;color:var(--navy)">already own a vault mat? she still works with it &hearts;</div>
</div>""")

# 5 first dates: isolated characters (tile pile circle + flat mat photo), no match cards (Oct 17 rule)
fd = ''
for i, m in enumerate(P['first_dates']):
    t = next(x for x in P['her_type'] if x['mat'] == m)
    fd += f"""<div style="display:flex;align-items:center;gap:22px;margin-top:{26 if i else 34}px">
 <div class="ph" style="flex:0 0 170px;height:170px;border-radius:50%;background:#fff url({url(pr['circle']) if pr.get('circle') else TILE}) center/{'112%' if pr.get('circle') else 'cover'} no-repeat;box-shadow:0 0 0 6px #fff,0 8px 20px rgba(6,40,90,.16)"></div>
 <div style="font:400 54px Capra;color:var(--pink)">&hearts;</div>
 <div class="ph" style="flex:0 0 260px;height:260px;border-radius:18px;background-image:url({url(MATS[m])});box-shadow:0 8px 22px rgba(6,40,90,.16)"></div>
 <div style="flex:1;padding-left:8px"><div class="caps" style="font-size:18px;color:var(--pink)">Match #{i + 1}</div>
  <div class="pf" style="font-size:40px;font-weight:600;line-height:1.1;margin-top:4px">{e(m)}</div><div style="font:400 23px Bit;color:#5a6b85;margin-top:4px">{e(t['brand'])}</div></div></div>"""
s5 = page(5, head('4 · first dates') + f"""
<div style="position:absolute;top:120px;left:72px;right:72px">
 <div class="cap" style="font-size:96px">First dates</div>
 <div class="pf" style="font-size:32px;margin-top:8px;color:#3c4f73">My top three of her {P['matches']} matches (and counting).</div>
 {fd}
</div>""")

# 6 end card
s6 = page(NS, f"""
<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;text-align:center;padding:120px 80px 0">
 <div class="caps" style="font-size:20px;color:#5a6b85">{e(P['bio'])}</div>
 <div style="display:flex;align-items:center;gap:26px;margin-top:56px">
  <div class="ph" style="width:300px;height:300px;border-radius:50%;background-image:url({TILE});box-shadow:0 0 0 8px #fff,0 10px 26px rgba(6,40,90,.18)"></div>
  <div style="font:400 84px Capra;color:var(--pink)">&hearts;</div>
  <div class="ph" style="width:300px;height:300px;border-radius:50%;background-image:url({url(MATS[P['first_dates'][0]])});box-shadow:0 0 0 8px #fff,0 10px 26px rgba(6,40,90,.18)"></div></div>
 <div class="cap" style="font-size:92px;margin-top:64px;line-height:1">See all of<br><span style="color:var(--acc)">her matches</span></div><div class="hand" style="font-size:46px;margin-top:14px">{P['matches']} and counting</div>
 <div class="pill" style="margin-top:28px;background:var(--pink)">link in bio &rarr;</div>
 <div style="margin-top:40px;background:#fff;border-radius:22px;padding:22px 34px;box-shadow:0 6px 18px rgba(6,40,90,.1)"><div style="font:700 32px Bit">Code <span style="color:var(--pink)">MAHJMATCH</span> at {e(P['brand'])}</div></div>
 <img src="{LOGO}" style="width:560px;margin-top:56px">
 <div style="font:600 22px Bit;margin-top:14px;letter-spacing:.06em">COMING 10.27 · FIND YOUR MATCH</div>
</div>""")

SLIDES = [s1, s2, s4] + ([sp, ss] if OMM else []) + [s3, s6]
for i, s in enumerate(SLIDES, 1):
    open(f'{OUT}/s{i}.html', 'w').write(s)
print('wrote', len(SLIDES), 'slides', OUT)
