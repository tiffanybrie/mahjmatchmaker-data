"""Title-card skit reels ("silent movie" dialogue cards, Tinder-site style), Oct 19.
Big serif line on a full-bleed solid color, text in a brighter shade of the same color, one italic word for emphasis,
small speaker label under it. Navy = the Matchmaker. The tile set talks in its own color. Photos cut in between.
Usage: python3 scripts/social/titlecards/build.py   -> assets/social/titlecards/counseling-ep1-papaya/
"""
import os, asyncio, subprocess, json
from PIL import Image
from playwright.async_api import async_playwright

R = '/home/claude/mahjmatchmaker-data'
F = f'file://{R}/scripts/social/tileprofile/fonts'
G = 'file:///usr/share/fonts/truetype/google-fonts'
u = lambda p: f'file://{R}/{p}'
OUT = f'{R}/assets/social/titlecards/counseling-ep1-papaya'
# REEL=1 (Oct 21, v11): render the full hotline reel body into frames/v11/ so tracked frames stay untouched;
# reel.py then adds the animated ending (ending.py) and the v9-style soundtrack.
REEL = os.environ.get('REEL') == '1'
VER = os.environ.get('REEL_VER', 'v11')               # v12 (Oct 21): same build, X + heart profile card
FR = OUT + (f'/frames/{VER}' if REEL else '/frames')
os.makedirs(FR, exist_ok=True)

MM = ('#062a55', '#f7b6c8', 'The Matchmaker')            # navy, blush text
PS = ('#ec7a32', '#fff3e6', 'Papaya Spritz')              # papaya, cream text (Tiffany: papaya, not brown)
PAUSE = ('#141414', '#f2ece6', '')
END = ('#fbe3ea', '#d6336c', '')

HEAD = f"""<!doctype html><html><head><meta charset=utf8><style>
@font-face{{font-family:Lo;src:url('{G}/Lora-Variable.ttf')}}
@font-face{{font-family:Lo;font-style:italic;src:url('{G}/Lora-Italic-Variable.ttf')}}
@font-face{{font-family:Bit;font-weight:600;src:url('{F}/bitter-latin-600-normal.woff2')}}
@font-face{{font-family:Hand;src:url('{F}/Caveat-Bold.ttf')}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden}}
.wrap{{position:relative;width:1080px;height:1920px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 90px}}
.line{{font-family:Lo;font-weight:700;line-height:1.02;letter-spacing:-.015em}}
.line i{{font-style:italic;font-weight:600}}
.who{{font:600 40px Bit;margin-top:56px;opacity:.85}}
.mark{{position:absolute;bottom:90px;left:0;right:0;display:flex;justify-content:center;align-items:center;gap:14px;font:600 26px Bit;letter-spacing:.2em;text-transform:uppercase;opacity:.55}}
</style></head><body>"""

def card(pal, html, size=150, who=None, mark=True, q=True, pre='', clip=False):
    bg, fg, name = pal
    w = who if who is not None else name
    if q: html = f'&ldquo;{html}&rdquo;'
    pre = f'<div style="font-family:Lo;font-style:italic;font-size:64px;opacity:.8;margin-bottom:34px">{pre}</div>' if pre else ''
    av = AV.get(name)
    whohtml = ''
    if w and av:
        whohtml = (f'<div style="display:flex;align-items:center;gap:22px;margin-top:64px"><div style="width:120px;height:120px;border-radius:50%;{av};box-shadow:0 0 0 6px {fg}"></div>'
                   f'<div class="who" style="margin-top:0;text-align:left">{w}</div></div>')
    elif w: whohtml = f'<div class="who">{w}</div>'
    ctag = ('<div style="position:absolute;top:110px;left:90px;right:90px;bottom:220px;border:5px dashed rgba(247,182,200,.55);border-radius:40px"></div>'
            '<div style="position:absolute;top:140px;font:600 30px Bit;letter-spacing:.16em;text-transform:uppercase;background:#f7b6c8;color:#062a55;padding:10px 26px;border-radius:999px">&#9654; your phone clip</div>') if clip else ''
    return (HEAD + f'<div class="wrap" style="background:{bg};color:{fg}">{ctag}{pre}<div class="line" style="font-size:{size}px">{html}</div>'
            + whohtml
            + (f'<div class="mark">mahj matchmaker</div>' if mark else '') + '</div></body></html>')

def photo(img, label, note=None, pos='center'):
    return (HEAD + f'<div class="wrap" style="background:url({u(img)}) {pos}/cover;justify-content:flex-end;padding-bottom:150px">'
            + f'<div style="background:rgba(6,42,85,.88);color:#fff;font:600 38px Bit;padding:18px 34px;border-radius:999px">{label}</div>'
            + (f'<div style="margin-top:22px;background:#fff8;color:#062a55;font:600 28px Bit;padding:10px 24px;border-radius:14px">{note}</div>' if note else '')
            + '</div></body></html>')

TILE = 'assets/tiles/album/papaya-spritz.jpg'
# profile photos under each speaker. Matchmaker = logo placeholder until Tiffany's real headshot exists.
AV = {'Papaya Spritz': f"background:url({u(TILE)}) center/cover",
      'The Matchmaker': f"background:#f7b6c8 url({u('assets/brand/flame-heart.png')}) center/62% no-repeat"}
CARDS = 'assets/cards/papaya-spritz/papaya-spritz-mahjong-tiles-'
def match(file, label, sub):
    return (HEAD + f'<div class="wrap" style="background:#f6e9df;justify-content:flex-start;padding-top:150px">'
            f'<div class="line" style="font-size:96px;color:#062a55">{label}</div>'
            f'<div style="font:600 36px Bit;color:#c8325f;margin:22px 0 50px;letter-spacing:.04em">{sub}</div>'
            f'<img src="{u(CARDS + file)}" style="width:900px;border-radius:26px;box-shadow:0 26px 60px rgba(6,42,85,.22)"></div></body></html>')
# Oct 21 (Tiffany): the Beige Felt mat is ONE recurring character asset, the same in Exhibit A and the swipe deck.
BEIGE_FELT = 'assets/social/characters/beige-felt-mat.png'   # scripts/social/characters/beige_felt.py
EVID = HEAD + f"""<div class="wrap" style="background:#efe4d6">
 <div style="background:#fff;color:#062a55;font:600 34px Bit;padding:18px 30px;border-radius:30px 30px 30px 6px;box-shadow:0 6px 18px rgba(0,0,0,.1);margin-bottom:46px;display:flex;align-items:center;gap:16px"><span style="width:56px;height:56px;border-radius:50%;background:url({u(TILE)}) center/cover;display:inline-block"></span>Papaya Spritz sent a photo</div><div style="font-family:Hand;font-size:110px;color:#062a55;margin-bottom:40px">Exhibit A</div>
 <div style="background:#fff;padding:30px 30px 120px;box-shadow:0 30px 60px rgba(0,0,0,.18);transform:rotate(-3deg)">
  <div style="width:720px;height:720px;background:#5d4a3a;display:flex;align-items:center;justify-content:center">
   <img src="{u(BEIGE_FELT)}" style="position:absolute;width:640px;height:640px;filter:drop-shadow(0 14px 18px rgba(0,0,0,.35))">
   <div style="position:relative;width:420px;height:420px;border-radius:50%;background:url({u(TILE)}) center/cover;-webkit-mask-image:radial-gradient(circle,#000 58%,transparent 72%)"></div></div>
  <div style="font-family:Hand;font-size:62px;color:#333;margin-top:22px">her + the beige felt mat</div></div>
 <div style="font:600 30px Bit;color:#062a55;opacity:.6;margin-top:70px;letter-spacing:.06em">(a made-up mat. no real mats were harmed.)</div>
</div></body></html>"""

SEARCH = ('<div style="width:900px;background:#fff;border-radius:999px;padding:26px 40px;display:flex;align-items:center;gap:24px;box-shadow:0 10px 26px rgba(6,42,85,.12);text-align:left">'
          '<svg width="54" height="54" viewBox="0 0 48 48"><circle cx="21" cy="21" r="13" fill="none" stroke="#062a55" stroke-width="5"/><path d="M31 31 L42 42" stroke="#062a55" stroke-width="5" stroke-linecap="round"/></svg>'
          '<span style="font:600 46px Bit;color:#062a55">Papaya Spritz</span><span style="margin-left:auto;font:600 28px Bit;color:#c8325f;letter-spacing:.1em">MATCHES</span></div>')
GRID = ''.join(f'<div style="width:190px;height:190px;border-radius:18px;background:url({u("assets/mats/gallery/" + f)}) center/cover"></div>' for f in sorted(os.listdir(R + '/assets/mats/gallery'))[::37][:20])
SEARCHING = HEAD + f"""<div class="wrap" style="background:#f6e9df;justify-content:flex-start;padding-top:200px">
  {SEARCH}
  <div style="font-family:Lo;font-weight:700;font-size:92px;color:#062a55;margin-top:70px">Searching <i>889 mats</i>&hellip;</div>
  <div style="font:600 32px Bit;color:#5a6b85;margin-top:16px;letter-spacing:.06em">the Mahj Matchmaker database</div>
  <div style="display:grid;grid-template-columns:repeat(4,190px);gap:20px;margin-top:70px;opacity:.55">{GRID}</div>
</div></body></html>"""

LAPTOP_IMG = 'assets/colorcards/papaya-spritz/00-papaya-spritz-mahjong-tiles-profile-a-desktop.jpg'
RESEARCH = HEAD + f"""<div class="wrap" style="background:{MM[0]};color:{MM[1]};justify-content:flex-start;padding-top:230px">
  <div style="font-family:Lo;font-style:italic;font-size:60px;opacity:.85">(searches database)</div>
  <div class="line" style="font-size:104px;margin-top:34px">&ldquo;You deserve someone who brings out your <i>best colors.</i>&rdquo;</div>
  <div style="display:flex;align-items:center;gap:20px;margin-top:40px"><div style="width:96px;height:96px;border-radius:50%;{AV['The Matchmaker']};box-shadow:0 0 0 5px {MM[1]}"></div><div class="who" style="margin-top:0">The Matchmaker</div></div>
  <div style="position:relative;margin-top:90px;width:960px">
    <div style="width:880px;margin:0 auto;background:#f4a7bd;border-radius:34px 34px 0 0;padding:22px 22px 26px;box-shadow:0 20px 50px rgba(0,0,0,.3)">
      <div style="position:relative;width:836px;height:470px;border-radius:14px;overflow:hidden;background:#fff url({u(LAPTOP_IMG)}) center/cover"></div></div>
    <div style="width:960px;height:44px;background:#f9c6d4;border-radius:0 0 40px 40px;position:relative;box-shadow:0 18px 40px rgba(0,0,0,.25)"><div style="position:absolute;left:50%;top:0;transform:translateX(-50%);width:170px;height:16px;background:#ec93ad;border-radius:0 0 14px 14px"></div></div>
  </div>
  <div style="position:absolute;bottom:90px;left:0;right:0;text-align:center;font:600 26px Bit;letter-spacing:.2em;text-transform:uppercase;opacity:.55">mahj matchmaker</div>
</div></body></html>"""

# Oct 21 (Tiffany): Papaya's racks = B&B Lavender, PLM Chartreuse, Middle & Main Scalloped Beechwood (replaces PLM Oak),
# same order as the posted intro carousel (config/tile-racks-picks.json final_lists).
RACKS = [('assets/colorcards/papaya-spritz/racks/bird-and-bamboo-lavender.png', 'Bird &amp; Bamboo Lavender'),
         ('assets/racks/card/peace-love-mahjong-chartreuse.png', 'Peace Love Mahjong Chartreuse'),
         ('assets/racks/card/middle--main-scalloped-beechwood.png', 'Middle &amp; Main Scalloped Beechwood')]
def prof(mat, name, brand, label, top=False):
    racks = ''.join(f'<div style="display:flex;align-items:center;gap:16px;margin-top:10px"><img src="{u(r)}" style="width:330px;height:34px;object-fit:cover;border-radius:6px"><span style="font:600 24px Bit;color:#5a6b85;text-align:left">{n}</span></div>' for r, n in RACKS)
    pill = ('<div style="position:absolute;top:44px;right:34px;transform:rotate(8deg);border:7px solid #c8325f;color:#c8325f;background:rgba(255,255,255,.9);'
            'font:700 64px Lo;letter-spacing:.08em;padding:0 22px;border-radius:14px">MATCH</div>')
    return (HEAD + f"""<div class="wrap" style="background:#f6e9df;justify-content:flex-start;padding-top:120px">
      {SEARCH}
      <div style="font:600 30px Bit;color:#5a6b85;margin:22px 0 36px;letter-spacing:.08em;text-transform:uppercase">{label}</div>
      <div style="position:relative;width:900px;background:#fff;border-radius:40px;overflow:hidden;box-shadow:0 30px 70px rgba(6,42,85,.20);text-align:left">
        <div style="width:900px;height:860px;background:url({u(mat)}) center/cover"></div>{pill}
        <div style="position:absolute;top:740px;left:36px;width:200px;height:200px;border-radius:50%;background:url({u(TILE)}) center/cover;box-shadow:0 0 0 10px #fff,0 10px 24px rgba(0,0,0,.2)"></div>
        <div style="position:absolute;top:800px;left:250px;width:84px;height:84px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 6px 16px rgba(0,0,0,.15)"><svg width="46" height="46" viewBox="0 0 48 48"><path d="M24 40 C10 30 6 23 6 17 C6 11 11 7 16 7 C20 7 22 9 24 12 C26 9 28 7 32 7 C37 7 42 11 42 17 C42 23 38 30 24 40 Z" fill="#f56c8c"/></svg></div>
        <div style="padding:100px 44px 40px">
          <div style="font-family:Lo;font-weight:700;font-size:72px;color:#062a55;line-height:1">{name}</div>
          <div style="font:600 26px Bit;letter-spacing:.2em;text-transform:uppercase;color:#c8325f;margin-top:10px">{brand} · mat</div>
          <div style="font:600 24px Bit;letter-spacing:.16em;text-transform:uppercase;color:#062a55;margin-top:30px">Her racks</div>{racks}
        </div></div>
      <div style="display:flex;gap:40px;margin-top:44px"><div style="width:110px;height:110px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;font:400 60px Bit;color:#062a55;box-shadow:0 8px 20px rgba(0,0,0,.12)">&times;</div>
        <div style="width:110px;height:110px;border-radius:50%;background:#f56c8c;display:flex;align-items:center;justify-content:center;box-shadow:0 8px 20px rgba(0,0,0,.12)"><svg width="56" height="56" viewBox="0 0 48 48"><path d="M24 40 C10 30 6 23 6 17 C6 11 11 7 16 7 C20 7 22 9 24 12 C26 9 28 7 32 7 C37 7 42 11 42 17 C42 23 38 30 24 40 Z" fill="#fff"/></svg></div></div>
    </div></body></html>""")

# Incoming-call frame (Tiffany Oct 19): a real-looking phone receiving a call, generic (no brand marks).
PHONE_STATUS = ('<div style="position:absolute;top:0;left:0;right:0;height:120px;display:flex;align-items:center;justify-content:space-between;padding:26px 70px 0;color:#fff;font:600 38px Bit;z-index:5">'
    '<span>9:41</span><span style="display:flex;gap:14px;align-items:center">'
    '<svg width="48" height="30" viewBox="0 0 48 30"><rect x="0" y="20" width="8" height="10" rx="2" fill="#fff"/><rect x="13" y="14" width="8" height="16" rx="2" fill="#fff"/><rect x="26" y="7" width="8" height="23" rx="2" fill="#fff"/><rect x="39" y="0" width="8" height="30" rx="2" fill="#fff"/></svg>'
    '<svg width="42" height="32" viewBox="0 0 42 32"><path d="M21 30 L13 21 A12 12 0 0 1 29 21 Z" fill="#fff"/><path d="M6 14 A21 21 0 0 1 36 14" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round"/><path d="M1 7 A28 28 0 0 1 41 7" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round" opacity=".9"/></svg>'
    '<svg width="66" height="32" viewBox="0 0 66 32"><rect x="1.5" y="1.5" width="56" height="29" rx="8" fill="none" stroke="#fff" stroke-width="3" opacity=".6"/><rect x="6" y="6" width="44" height="20" rx="4" fill="#fff"/><rect x="60" y="11" width="5" height="10" rx="2" fill="#fff" opacity=".6"/></svg>'
    '</span></div>')
CALL = HEAD + f"""<div class="wrap" style="background:#f6e9df;padding:0">
  <div style="position:absolute;right:-220px;top:-160px;width:760px;height:760px;border-radius:50%;background:#f9dccf"></div>
  <div style="position:absolute;left:-240px;bottom:-220px;width:700px;height:700px;border-radius:50%;background:#fbe3ea"></div>
  <svg style="position:absolute;left:70px;top:180px;transform:rotate(-12deg)" width="70" height="70" viewBox="0 0 48 48"><path d="M24 40 C10 30 6 23 6 17 C6 11 11 7 16 7 C20 7 22 9 24 12 C26 9 28 7 32 7 C37 7 42 11 42 17 C42 23 38 30 24 40 Z" fill="#f56c8c"/></svg><svg style="position:absolute;left:930px;top:330px;transform:rotate(10deg)" width="54" height="54" viewBox="0 0 48 48"><path d="M24 40 C10 30 6 23 6 17 C6 11 11 7 16 7 C20 7 22 9 24 12 C26 9 28 7 32 7 C37 7 42 11 42 17 C42 23 38 30 24 40 Z" fill="#f7b6c8"/></svg><svg style="position:absolute;left:40px;top:1180px;transform:rotate(8deg)" width="58" height="58" viewBox="0 0 48 48"><path d="M24 40 C10 30 6 23 6 17 C6 11 11 7 16 7 C20 7 22 9 24 12 C26 9 28 7 32 7 C37 7 42 11 42 17 C42 23 38 30 24 40 Z" fill="#f7b6c8"/></svg><svg style="position:absolute;left:960px;top:1500px;transform:rotate(-10deg)" width="76" height="76" viewBox="0 0 48 48"><path d="M24 40 C10 30 6 23 6 17 C6 11 11 7 16 7 C20 7 22 9 24 12 C26 9 28 7 32 7 C37 7 42 11 42 17 C42 23 38 30 24 40 Z" fill="#f56c8c"/></svg><svg style="position:absolute;left:110px;top:1700px;transform:rotate(12deg)" width="44" height="44" viewBox="0 0 48 48"><path d="M24 40 C10 30 6 23 6 17 C6 11 11 7 16 7 C20 7 22 9 24 12 C26 9 28 7 32 7 C37 7 42 11 42 17 C42 23 38 30 24 40 Z" fill="#ffa868"/></svg><svg style="position:absolute;left:900px;top:820px;transform:rotate(-6deg)" width="40" height="40" viewBox="0 0 48 48"><path d="M24 40 C10 30 6 23 6 17 C6 11 11 7 16 7 C20 7 22 9 24 12 C26 9 28 7 32 7 C37 7 42 11 42 17 C42 23 38 30 24 40 Z" fill="#ffa868"/></svg>
  <div style="position:relative;width:780px;height:1600px;border-radius:120px;background:#f4a7bd;padding:24px;box-shadow:0 40px 80px rgba(200,50,95,.28),inset 0 0 0 6px #f9c6d4,inset 0 0 0 12px #f4a7bd">
   <div style="position:absolute;right:-16px;top:300px;width:10px;height:150px;border-radius:6px;background:#ec93ad"></div><div style="position:absolute;left:-16px;top:260px;width:10px;height:90px;border-radius:6px;background:#ec93ad"></div><div style="position:absolute;left:-16px;top:380px;width:10px;height:90px;border-radius:6px;background:#ec93ad"></div>
   <div style="position:relative;width:100%;height:100%;border-radius:100px;overflow:hidden;background:url({u(TILE)}) center/cover">
    <div style="position:absolute;inset:0;background:linear-gradient(to bottom,rgba(10,6,20,.62) 0%,rgba(10,6,20,.15) 38%,rgba(10,6,20,.25) 62%,rgba(10,6,20,.78) 100%)"></div>
    <div style="position:absolute;top:26px;left:50%;transform:translateX(-50%);width:230px;height:66px;border-radius:40px;background:#000;z-index:6"></div>
    {PHONE_STATUS}
    <div style="position:absolute;top:190px;left:0;right:0;text-align:center;color:#fff">
      <div style="font:400 34px Bit;opacity:.8">mobile</div>
      <div style="font-family:Lo,'Noto Color Emoji';font-weight:700;font-size:92px;line-height:1.05;margin-top:10px;padding:0 40px">Papaya Spritz<br><span style="font-family:'Noto Color Emoji';font-size:70px">&#x1F34A;&#x1F49C;&#x1F379;&#x1F49A;</span></div>
    </div>
    <div style="position:absolute;bottom:330px;left:0;right:0;display:flex;justify-content:space-between;padding:0 120px;color:#fff;font:600 30px Bit;text-align:center">
      <div><svg width="64" height="64" viewBox="0 0 48 48"><circle cx="24" cy="26" r="15" fill="none" stroke="#fff" stroke-width="3.5"/><path d="M24 18 V26 L30 30" stroke="#fff" stroke-width="3.5" fill="none" stroke-linecap="round"/><path d="M8 12 L14 6 M40 12 L34 6" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/></svg><div style="margin-top:8px">Remind Me</div></div>
      <div><svg width="64" height="64" viewBox="0 0 48 48"><path d="M8 10 H40 A3 3 0 0 1 43 13 V31 A3 3 0 0 1 40 34 H20 L11 41 V34 H8 A3 3 0 0 1 5 31 V13 A3 3 0 0 1 8 10 Z" fill="none" stroke="#fff" stroke-width="3.5" stroke-linejoin="round"/></svg><div style="margin-top:8px">Message</div></div>
    </div>
    <div style="position:absolute;bottom:90px;left:0;right:0;display:flex;justify-content:space-between;padding:0 90px;color:#fff;font:600 32px Bit;text-align:center">
      <div><div style="width:170px;height:170px;border-radius:50%;background:#e5484d;display:flex;align-items:center;justify-content:center"><svg width="86" height="86" viewBox="0 0 48 48" style="transform:rotate(135deg)"><path d="M14 8 L19 8 L22 16 L18 19 C20 24 24 28 29 30 L32 26 L40 29 L40 34 C40 37 37 40 34 40 C20 39 9 28 8 14 C8 11 11 8 14 8 Z" fill="#fff"/></svg></div><div style="margin-top:16px">Decline</div></div>
      <div><div style="width:170px;height:170px;border-radius:50%;background:#34c759;display:flex;align-items:center;justify-content:center"><svg width="86" height="86" viewBox="0 0 48 48"><path d="M14 8 L19 8 L22 16 L18 19 C20 24 24 28 29 30 L32 26 L40 29 L40 34 C40 37 37 40 34 40 C20 39 9 28 8 14 C8 11 11 8 14 8 Z" fill="#fff"/></svg></div><div style="margin-top:16px">Accept</div></div>
    </div>
   </div></div>
</div></body></html>"""

M = 'assets/colorcards/papaya-spritz/mats/'
G2 = 'assets/mats/gallery/'

# ---- Animated swipe segment (Oct 19): teases Find Your Match without naming it. STATIC=1 env -> old static prof() frames (story version).
STATIC = os.environ.get('STATIC') == '1'
FPS = 30
BEIGE_CARD = f'<div style="width:900px;height:860px;background:#f3ece3 url({u(BEIGE_FELT)}) center/88% no-repeat"></div>'   # same asset as Exhibit A
# (mat image or None for beige, name, brand line, verdict, hold, swipe seconds)
SWIPES = [(None, 'Beige Felt', 'no brand', 'nope', 1.3, 0.55),
          (M + 'heiress-britt-mills.jpg', 'Heiress', 'Britt Mills', 'match', 1.2, 0.5),
          (G2 + 'anders-ruff--bams-bubbly.webp', 'Bams &amp; Bubbly', 'Anders Ruff', 'match', 1.0, 0.45),
          (M + 'greenly-mahj-and-vine.jpg', 'Greenly', 'Mahj &amp; Vine', 'match', 0.7, 0.4),
          (G2 + 'oh-my-mahjong--vivienne.webp', 'Vivienne', 'Oh My Mahjong', 'match', 0.7, 0.4),
          (M + 'press-for-mahjong-anders-ruff.jpg', 'Press for Mahjong', 'Anders Ruff', 'match', 0.7, 0.4),
          (G2 + 'oh-my-mahjong--goldie-retired.webp', 'Goldie', 'Oh My Mahjong', 'match', 1.6, 0)]
# Oct 21 (v11): the last card never swipes off. It holds with its MATCH stamp and the reel cuts straight to 'Hook me up!'
# (v9/v10 swiped Goldie away and showed ~0.6s of an EMPTY deck: header + buttons, no card). Same total length as before.
LEAD, TAIL_HOLD = 0.4, 0.0
HEART = '<svg width="{w}" height="{w}" viewBox="0 0 48 48"><path d="M24 40 C10 30 6 23 6 17 C6 11 11 7 16 7 C20 7 22 9 24 12 C26 9 28 7 32 7 C37 7 42 11 42 17 C42 23 38 30 24 40 Z" fill="{c}"/></svg>'
def swipe_card(i, mat, name, brand, verdict):
    racks = ''.join(f'<div style="display:flex;align-items:center;gap:16px;margin-top:10px"><img src="{u(r)}" style="width:330px;height:34px;object-fit:cover;border-radius:6px"><span style="font:600 24px Bit;color:#5a6b85">{n}</span></div>' for r, n in RACKS)
    top = BEIGE_CARD if mat is None else f'<div style="width:900px;height:860px;background:url({u(mat)}) center/cover"></div>'
    if verdict == 'nope':
        # Oct 21: no NOPE/pass wording anywhere (profile UI = X + heart only). The 'not for her' card gets an X stamp.
        stamp = ('<div class="stamp" style="position:absolute;top:56px;right:56px;transform:rotate(10deg);width:190px;height:190px;border-radius:50%;border:8px solid #062a55;'
                 'background:rgba(255,255,255,.9);display:flex;align-items:center;justify-content:center;opacity:0">'
                 '<svg width="96" height="96" viewBox="0 0 48 48"><path d="M13 13 L35 35 M35 13 L13 35" stroke="#062a55" stroke-width="7" stroke-linecap="round"/></svg></div>')
    else:
        stamp = ('<div class="stamp" style="position:absolute;top:60px;left:46px;transform:rotate(-10deg);border:8px solid #c8325f;color:#c8325f;background:rgba(255,255,255,.88);'
                 'font:700 92px Lo;letter-spacing:.08em;padding:0 26px;border-radius:16px;opacity:0">MATCH</div>')
    return f"""<div class="sc" id="c{i}" style="position:absolute;left:0;top:0;width:900px;background:#fff;border-radius:40px;overflow:hidden;box-shadow:0 30px 70px rgba(6,42,85,.20);text-align:left;transform-origin:50% 120%">
      {top}{stamp}
      <div style="position:absolute;top:740px;left:36px;width:200px;height:200px;border-radius:50%;background:url({u(TILE)}) center/cover;box-shadow:0 0 0 10px #fff,0 10px 24px rgba(0,0,0,.2)"></div>
      <div style="padding:100px 44px 40px">
        <div style="font-family:Lo;font-weight:700;font-size:72px;color:#062a55;line-height:1">{name}</div>
        <div style="font:600 26px Bit;letter-spacing:.2em;text-transform:uppercase;color:#c8325f;margin-top:10px">{brand} · mat</div>
        <div style="font:600 24px Bit;letter-spacing:.16em;text-transform:uppercase;color:#062a55;margin-top:30px">Her racks</div>{racks}
      </div></div>"""
def swipe_html():
    cards = ''.join(swipe_card(i, *c[:4]) for i, c in reversed(list(enumerate(SWIPES))))
    tl = json.dumps([[c[3], c[4], c[5]] for c in SWIPES])
    return HEAD + f"""<div class="wrap" style="background:#f6e9df;justify-content:flex-start;padding-top:120px">
      {SEARCH}
      <div id="ctr" style="font:600 30px Bit;color:#5a6b85;margin:22px 0 36px;letter-spacing:.08em;text-transform:uppercase">swiping&hellip;</div>
      <div style="position:relative;width:900px;height:1360px">{cards}</div>
      <div style="display:flex;gap:40px;margin-top:6px">
        <div id="bx" style="width:120px;height:120px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;font:400 66px Bit;color:#062a55;box-shadow:0 8px 20px rgba(0,0,0,.12)">&times;</div>
        <div id="bh" style="width:120px;height:120px;border-radius:50%;background:#f56c8c;display:flex;align-items:center;justify-content:center;box-shadow:0 8px 20px rgba(0,0,0,.12)">{HEART.format(w=60, c='#fff')}</div></div>
    </div>
    <script>
    const TL={tl}, LEAD={LEAD};
    const ease=x=>x<.5?2*x*x:1-Math.pow(-2*x+2,2)/2;
    function render(t){{
      let start=LEAD, matches=0, label='swiping&hellip;', bx=1, bh=1, xs='#fff', hs='#f56c8c';
      for(let i=0;i<TL.length;i++){{
        const [v,hold,sw]=TL[i]; const el=document.getElementById('c'+i); const st=el.querySelector('.stamp');
        const a=start, b=BC[i][0], c=BC[i][1]; const dir = v==='nope' ? -1 : 1;
        if(t<a){{ const depth=Math.max(0,Math.min(i-curIndex(t)-curProg(t),3)); el.style.transform=`translateY(${{depth*22}}px) scale(${{1-depth*.04}})`; st.style.opacity=0; el.style.opacity=Math.max(0,Math.min(1,3-depth)); }}
        else if(t<b){{ el.style.transform='none'; el.style.opacity=1;
          const s0 = sw===0 ? a+0.6 : b-0.35;   // last card (no swipe-off): stamp lands early and stays
          const sk=Math.max(0,(t-s0)/0.35); st.style.opacity=Math.min(sk,1);
          if(t>s0){{ const pr = sw===0 ? (sk<1 ? .12*sk : Math.max(0,.12-.12*(sk-1))) : .12*Math.min(sk,1);
            if(dir<0) bx=1-pr; else bh=1-pr; }}
          label = v==='nope' ? 'not her type' : `match ${{matches+1}} of 50`; }}
        else if(t<c){{ const k=ease((t-b)/sw); el.style.transform=`translateX(${{dir*1400*k}}px) rotate(${{dir*10*k}}deg)`; st.style.opacity=1; el.style.opacity=1;
          if(dir<0) bx=.88+.12*k; else bh=.88+.12*k;
          label = v==='nope' ? 'not her type' : `match ${{matches+1}} of 50`; }}
        else {{ el.style.opacity=0; if(v==='match') matches++; }}
        start=c;
      }}
      document.getElementById('ctr').innerHTML=label;
      document.getElementById('bx').style.transform=`scale(${{bx}})`; document.getElementById('bh').style.transform=`scale(${{bh}})`;
    }}
    // Oct 21 (v11): one shared timeline (same float sums as render) so the deck never disagrees with itself at a boundary
    // (v9 had a one-frame jump there); cards under the top card slide up smoothly while it swipes off.
    const BC=[]; {{ let s=LEAD; for(let i=0;i<TL.length;i++){{ const b=s+TL[i][1], c=b+TL[i][2]; BC.push([b,c]); s=c; }} }}
    function curIndex(t){{ for(let i=0;i<TL.length;i++){{ if(t<BC[i][1]) return i; }} return TL.length; }}
    function curProg(t){{ const i=curIndex(t); if(i>=TL.length) return 0; const [b,c]=BC[i]; return t<b?0:ease((t-b)/TL[i][2]); }}
    window.render=render;
    </script></body></html>"""
SWIPE_LEN = LEAD + sum(c[4] + c[5] for c in SWIPES) + TAIL_HOLD
STATIC_PROFS = [(prof(M + 'heiress-britt-mills.jpg', 'Heiress', 'Britt Mills', 'match 1 of 50'), 2.0),
    (prof(G2 + 'anders-ruff--bams-bubbly.webp', 'Bams &amp; Bubbly', 'Anders Ruff', 'match 2 of 50'), 1.4),
    (prof(M + 'greenly-mahj-and-vine.jpg', 'Greenly', 'Mahj &amp; Vine', 'match 3 of 50'), 1.4),
    (prof(G2 + 'oh-my-mahjong--vivienne.webp', 'Vivienne', 'Oh My Mahjong', 'match 4 of 50'), 1.4),
    (prof(M + 'press-for-mahjong-anders-ruff.jpg', 'Press for Mahjong', 'Anders Ruff', 'match 5 of 50'), 1.4),
    (prof(G2 + 'oh-my-mahjong--goldie-retired.webp', 'Goldie', 'Oh My Mahjong', 'match 6 of 50'), 1.4)]
PACE = 1.35  # Tiffany Oct 19: slow it down a little
SHOTS = [
    (CALL, 2.4),
    (card(MM, 'Mahj Matchmaker. How can I <i>save your table?</i>', 120, clip=True), 2.6),
    (card(PS, 'Hey girl, it&rsquo;s me. I just don&rsquo;t know what <i>went wrong.</i>', 120), 3.0),
    (card(MM, 'Tell me <i>what happened.</i>', clip=True), 2.0),
    (EVID, 2.8),
    (card(MM, '<i>Wow.</i>', 220, clip=True), 1.4),
    (card(MM, 'It&rsquo;s not you&hellip;', 110, pre='(whispering)', clip=True), 1.9),
    (card(MM, '&hellip;it&rsquo;s your <i>mat.</i>', 110, pre='(whispering)', clip=True), 2.4),
    (card(PS, 'I feel like I have a lot <i>to offer.</i>', 130), 2.4),
    (HEAD + f"""<div class="wrap" style="background:url({u('assets/colorcards/papaya-spritz/00-papaya-spritz-mahjong-tiles-profile-c-story.jpg')}) center/cover"></div></body></html>""", 3.0),
    (RESEARCH, 3.6),
    'SWIPE',
]
# Old static ending ('Hook me up.' + static end card). Only the STATIC story version uses it; the reel uses the animated
# ending from ending.py (one 'Hook me up!' card, one end card), so the reel never shows two versions of a card.
OLD_ENDING = [
    (card(PS, 'Hook me <i>up.</i>', 190), 2.2),
    (HEAD + f"""<div class="wrap" style="background:{END[0]};color:{END[1]}">
      <img src="{u('assets/brand/flame-heart.png')}" style="width:150px;margin-bottom:40px">
      <img src="{u('assets/brand/mahjmatchmaker-wordmark-notag.png')}" style="width:720px">
      <div class="line" style="font-size:92px;margin-top:36px">Hooking up <i>tiles,</i><br><i>mats</i> &amp; <i>racks.</i></div>
      <div style="font-family:Lo;font-size:54px;color:#062a55;margin-top:60px;line-height:1.25">Swipe your own matches.<br>Every tile, mat &amp; rack, <i>swappable.</i></div>
      <div style="margin-top:56px;background:#062a55;color:#fff;border-radius:999px;padding:26px 54px;font:600 48px Bit">Find <i>Your</i> Mat-ch<sup style="font-size:.35em;vertical-align:super">&trade;</sup> &middot; 10.27</div>
      <div style="font:600 32px Bit;color:#062a55;opacity:.7;margin-top:26px">mahjmatchmaker.com</div></div></body></html>""", 3.6),
]

def make_ring(path, sr=44100):
    """Synthesized phone ring (no licensing): UK-style double ring, 400+450 Hz, two ring-rings, fading as the call is answered."""
    import wave, struct, math
    dur = 3.2; n = int(sr * dur); out = []
    for i in range(n):
        t = i / sr; m = t % 1.6
        on = (0 <= m < 0.4) or (0.6 <= m < 1.0)
        if t >= 3.2: on = False
        env = 1.0
        if t > 2.6: env = max(0.0, 1 - (t - 2.6) / 0.6)            # fade out as she answers
        # 20 ms attack/decay on each burst to avoid clicks
        edge = min(m if m < 0.4 else m - 0.6, (0.4 - m) if m < 0.4 else (1.0 - m))
        ramp = min(1.0, max(0.0, edge / 0.02))
        v = (math.sin(2 * math.pi * 400 * t) + math.sin(2 * math.pi * 450 * t)) * 0.22 * env * ramp if on else 0.0
        out.append(int(max(-1, min(1, v)) * 32767))
    with wave.open(path, 'w') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(struct.pack('<%dh' % len(out), *out))

async def main():
    shots = []
    for x in SHOTS + ([] if REEL else OLD_ENDING):
        if x == 'SWIPE': shots.extend(STATIC_PROFS if STATIC else ['SWIPE'])
        else: shots.append(x)
    entries, stills = [], []   # (png, seconds, paced?)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        for i, x in enumerate(shots, 1):
            if x == 'SWIPE':
                hp = f'{FR}/f{i:02d}-swipe.html'; open(hp, 'w').write(swipe_html())
                await pg.goto('file://' + hp); await pg.wait_for_load_state('networkidle'); await pg.evaluate('document.fonts.ready')
                os.makedirs(f'{FR}/swipe', exist_ok=True)
                n = int(round(SWIPE_LEN * FPS))
                for k in range(n):
                    await pg.evaluate(f'render({k / FPS})')
                    fp = f'{FR}/swipe/s{k:04d}.png'; await pg.screenshot(path=fp)
                    entries.append((f'swipe/s{k:04d}.png', 1 / FPS, False))
                for tt in (1.6, 3.25, 6.2):   # contact-sheet stills: NOPE, MATCH 1, later match
                    k = min(int(tt * FPS), n - 1); stills.append(f'{FR}/swipe/s{k:04d}.png')
                continue
            h, d = x
            hp = f'{FR}/f{i:02d}.html'; open(hp, 'w').write(h)
            await pg.goto('file://' + hp); await pg.wait_for_load_state('networkidle'); await pg.evaluate('document.fonts.ready')
            await pg.screenshot(path=f'{FR}/f{i:02d}.png')
            entries.append((f'f{i:02d}.png', d, True)); stills.append(f'{FR}/f{i:02d}.png')
        await b.close()
    lst = f'{FR}/list.txt'
    with open(lst, 'w') as f:
        for fn, d, paced in entries:
            f.write(f"file '{fn}'\nduration {round(max(d * PACE, 1.8), 2) if paced else round(d, 5)}\n")
        f.write(f"file '{entries[-1][0]}'\n")
    name = f'{VER}-body' if REEL else 'counseling-session-1-papaya-spritz' + ('-static' if STATIC else '')
    if REEL:
        # Oct 21 (v11): frame-exact body. Every still gets an exact frame count (cut points on the 1/30 s grid, cumulative
        # rounding) and the swipe frames are encoded 1:1, so no swipe frame is ever dropped or doubled (the concat-demuxer
        # path with 0.03333 s durations dropped/duplicated frames in v9).
        segs, cum, done, k = [], 0.0, 0, 0
        while k < len(entries):
            fn, d, paced = entries[k]
            if paced:
                cum += round(max(d * PACE, 1.8), 2); nf = round(cum * FPS) - done; done += nf
                seg = f'{FR}/seg{k:03d}.mp4'
                subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-framerate', str(FPS), '-i', f'{FR}/{fn}', '-frames:v', str(nf),
                                '-vf', 'format=yuv420p', '-c:v', 'libx264', '-crf', '16', '-r', str(FPS), seg], check=True)
                segs.append(seg); k += 1
            else:
                j = k
                while j < len(entries) and not entries[j][2]: j += 1
                seg = f'{FR}/seg{k:03d}-swipe.mp4'
                subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-start_number', '0', '-i', f'{FR}/swipe/s%04d.png',
                                '-frames:v', str(j - k), '-vf', 'format=yuv420p', '-c:v', 'libx264', '-crf', '16', '-r', str(FPS), seg], check=True)
                segs.append(seg); cum += (j - k) / FPS; done += j - k; k = j
        with open(f'{FR}/segs.txt', 'w') as f: f.write(''.join(f"file '{x}'\n" for x in segs))
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{FR}/segs.txt', '-c', 'copy', f'{FR}/{name}-silent.mp4'], check=True)
        return
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-vf', 'fps=30,format=yuv420p',
                    '-c:v', 'libx264', '-crf', '18', f'{FR}/{name}-silent.mp4'], check=True)
    # ring over the first frame only; the rest stays silent so Tiffany can add Instagram music on top
    make_ring(f'{FR}/ring.wav')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{FR}/{name}-silent.mp4', '-i', f'{FR}/ring.wav',
                    '-filter_complex', '[1:a]apad[a]', '-map', '0:v', '-map', '[a]', '-shortest', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k',
                    f'{OUT}/{name}.mp4'], check=True)
    ims = [Image.open(f).convert('RGB').resize((270, 480)) for f in stills]
    cols = 7; rows = (len(ims) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * 280 + 10, rows * 490 + 10), (240, 236, 230))
    for k, im in enumerate(ims): sheet.paste(im, (10 + (k % cols) * 280, 10 + (k // cols) * 490))
    sheet.save(f'{OUT}/contact-sheet' + ('-static' if STATIC else '') + '.jpg', quality=90)

if __name__ == '__main__':
    asyncio.run(main()); print(OUT)
