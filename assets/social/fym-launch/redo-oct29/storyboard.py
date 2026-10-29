"""Launch reel REDO storyboard (Oct 29): numbered STILLS only, no video.
Real FYM screens from cap_redo.py (argv[1] = capture dir). The phone sits at ONE fixed spot on the stage in every frame;
the 'camera' only zooms (scale about a point), it never slides the phone sideways. On a swipe only the cut-out card moves.
Writes frames/NN.jpg (540x960) + storyboard.jpg (contact sheet) next to this file."""
import os, sys, json, math
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); R = '/home/claude/mahjmatchmaker-data'
CAP = sys.argv[1]; META = json.load(open(f'{CAP}/meta.json')); FR = f'{HERE}/frames'; os.makedirs(FR, exist_ok=True)
F = f'file://{R}/scripts/social/tileprofile/fonts/'
NAVY, PINK, CREAM, BLUSH, SLATE = '#062a55', '#e0547f', '#fdf6ee', '#f7b6c8', '#6f6280'
FYM = 'Find <span class="pf">Your</span> Mat&#8209;ch<sup style="font-size:.32em;vertical-align:super">&trade;</sup>'
CSS = f"""<style>@font-face{{font-family:Cap;src:url({F}Caprasimo.ttf)}}@font-face{{font-family:Bit;font-weight:700;src:url({F}bitter-latin-700-normal.woff2)}}
@font-face{{font-family:PF;font-style:italic;src:url({F}playfair-display-latin-600-italic.woff2)}}
*{{margin:0;padding:0;box-sizing:border-box}}body{{width:1080px;height:1920px;overflow:hidden}}
.w{{position:absolute;inset:0;overflow:hidden;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 70px}}
.cap{{font-family:Cap;line-height:1.04}}.pf{{font-family:PF;font-style:italic;font-weight:600}}.it{{font:italic 600 60px/1.3 PF}}
.hdr{{position:absolute;left:0;right:0;top:0;height:190px;z-index:50;display:flex;align-items:center;justify-content:center;gap:24px;background:linear-gradient({CREAM} 80%,rgba(253,246,238,0))}}
.hdr b{{background:{PINK};color:#fff;font:700 30px Bit;letter-spacing:.14em;padding:12px 24px;border-radius:40px}}.hdr div{{font-family:Cap;font-size:76px;color:{NAVY};white-space:nowrap}}
.call{{position:absolute;z-index:40;background:{PINK};color:#fff;font:700 38px/1.18 Bit;padding:16px 26px;border-radius:24px;box-shadow:0 14px 30px rgba(0,0,0,.25);text-align:left;white-space:nowrap}}
.call small{{display:block;font-size:30px;opacity:.92}}
.ring{{position:absolute;z-index:45;width:110px;height:110px;border-radius:50%;border:10px solid {PINK};box-shadow:0 0 0 8px rgba(255,255,255,.7)}}
.cam{{position:absolute;z-index:46;right:24px;bottom:24px;background:rgba(6,42,85,.85);color:#fff;font:700 26px Bit;padding:8px 16px;border-radius:14px}}
</style>"""
HEART = '<svg viewBox="0 0 48 48" width="100%" height="100%"><path d="M24 40 C10 30 6 23 6 17 C6 11 11 7 16 7 C20 7 22 9 24 12 C26 9 28 7 32 7 C37 7 42 11 42 17 C42 23 38 30 24 40 Z" fill="{c}"/></svg>'
u = lambda p: 'file://' + (p if p.startswith('/') else f'{CAP}/{p}')
def page(bg, body): return f'<!doctype html><html><head><meta charset=utf8>{CSS}</head><body style="background:{bg}"><div class="w" style="background:{bg};color:{NAVY}">{body}</div></body></html>'
# ---- fixed phone on the stage (never moves)
SW = 700; K = SW / 390; PX = (1080 - SW) // 2; PY = 330; BZ = 22
def P(x, y): return PX + x * K, PY + y * K            # app css px -> stage px
def phone(img):
    return (f'<div style="position:absolute;left:{PX-BZ}px;top:{PY-BZ-40}px;width:{SW+2*BZ}px;height:{844*K+2*BZ+80}px;border-radius:96px;background:#f4f3f1;box-shadow:0 40px 90px rgba(0,0,0,.35),inset 0 0 0 4px #d6d6d3"></div>'
            f'<div style="position:absolute;left:{PX}px;top:{PY}px;width:{SW}px;height:{844*K:.0f}px;border-radius:70px;overflow:hidden;background:#fff"><img src="{u(img)}" style="width:100%;display:block"></div>'
            f'<div style="position:absolute;left:{540-95}px;top:{PY-26}px;width:190px;height:44px;background:#111;border-radius:22px"></div>')
def stage(inner, cam=(1.0, 195, 422, 540, 1010)):
    s, X, Y, fx, fy = cam; sx, sy = P(X, Y)
    return f'<div style="position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:0 0;transform:translate({fx - s*sx:.0f}px,{fy - s*sy:.0f}px) scale({s})">{inner}</div>'
def ring_at(x, y): X, Y = P(x, y); return f'<div class="ring" style="left:{X-55:.0f}px;top:{Y-55:.0f}px"></div>'
def call_at(t, x, y, rot=-3, bg=PINK, sub=''):
    X, Y = P(x, y); return f'<div class="call" style="left:{X:.0f}px;top:{Y:.0f}px;transform:rotate({rot}deg);background:{bg}">{t}{f"<small>{sub}</small>" if sub else ""}</div>'
def tstamp(kind):
    if kind == 'yes': return f'<div style="position:absolute;left:30px;top:70px;transform:rotate(-14deg);border:12px solid {PINK};color:{PINK};border-radius:28px;padding:4px 30px;font:400 120px/1 Cap;background:rgba(255,255,255,.9);z-index:3">&hearts;</div>'
    return f'<div style="position:absolute;right:30px;top:70px;transform:rotate(14deg);border:12px solid {SLATE};color:{SLATE};border-radius:28px;padding:4px 34px;font:400 110px/1 Cap;background:rgba(255,255,255,.9);z-index:3">&#10005;</div>'
def flying(cid, kind, label, sub, prog=.45, ly=300):
    bx, by, bw, bh = META[cid]; X, Y = P(bx, by); dx = (1 if kind == 'yes' else -1) * 360 * prog; rot = (1 if kind == 'yes' else -1) * 16 * prog
    lab = f'<div class="call" style="left:24px;top:{ly}px;transform:rotate(-3deg);background:{PINK if kind=="yes" else SLATE}">{label}<small>{sub}</small></div>'
    return (f'<div style="position:absolute;left:{X:.0f}px;top:{Y:.0f}px;width:{bw*K:.0f}px;z-index:20;transform-origin:50% 120%;transform:translateX({dx:.0f}px) rotate({rot:.1f}deg)">'
            f'<img src="{u(cid + "-card.png")}" style="width:100%;display:block;border-radius:26px;box-shadow:0 30px 70px rgba(0,0,0,.38)">{tstamp(kind)}{lab}</div>')
def tray(img, hl=None):
    return (f'<div style="position:absolute;left:200px;right:200px;bottom:30px;z-index:48;border-radius:28px;overflow:hidden;box-shadow:0 14px 34px rgba(0,0,0,.28);border:5px solid {PINK if hl else "#fff"}">'
            f'<img src="{u(img)}" style="width:100%;display:block"></div>' + (f'<div class="call" style="left:770px;bottom:60px;top:auto;transform:rotate(3deg);font-size:30px">{hl}</div>' if hl else ''))
def hdr(n, t): return f'<div class="hdr"><b>{n}</b><div>{t}</div></div>'
def cam(t): return f'<div class="cam">CAMERA: {t}</div>'
def bigbtns(kind):
    on = lambda k: 'transform:scale(1.22);box-shadow:0 0 0 12px rgba(224,84,127,.35),0 12px 30px rgba(0,0,0,.25);' if k == kind else ''
    return (f'<div style="position:absolute;left:0;right:0;bottom:250px;display:flex;justify-content:center;gap:110px;z-index:44">'
            f'<div style="{on("no")}width:150px;height:150px;border-radius:50%;background:#fff;box-shadow:0 12px 30px rgba(0,0,0,.25);display:grid;place-items:center;font:400 76px Cap;color:{SLATE}">&#10005;</div>'
            f'<div style="{on("yes")}width:150px;height:150px;border-radius:50%;background:{PINK};box-shadow:0 12px 30px rgba(0,0,0,.25);display:grid;place-items:center;font:400 80px Cap;color:#fff">&hearts;</div></div>')
TILE = f'{R}/assets/tiles/album/sunday-tile-set-hd.jpg'; MAT = f'{R}/assets/mats/gallery/anders-ruff--brownstone-bloom-mahjong-mat.webp'
FLAME = f'{R}/assets/brand/flame-heart.png'
# camera presets: (scale, css X, css Y, frame x, frame y)
FULL = (0.92, 195, 430, 540, 1030)
DUO = (1.05, 195, 452, 540, 975)       # tile strip + mat card + the app's own ✕ / ♥ buttons
TOPUP = (1.55, 195, 300, 540, 1020)     # close on tiles + filter chips
CHIPS = (1.9, 210, 222, 540, 900)
MATC = (1.6, 195, 520, 540, 1060)       # close on the mat card (zoom +/−)
RACK = (1.12, 195, 470, 540, 1060)      # racks: zoomed mat preview + chips + rack card
RTOP = (1.75, 195, 240, 540, 900)
SHOP = (1.25, 195, 470, 540, 1060)
tray0, tray1, tray2 = 'tray-s0.png', 'tray-s0.png', 'tray-s3.png'
FR_ = []  # (html, seconds, caption)
def add(html, secs, cap): FR_.append((html, secs, cap))
# ---------------- OPENER
add(page(NAVY, f'<div class="cap" style="font-size:150px;color:#fff">The ever&#8209;burning question.</div>'), 1.5, 'Navy slam-in title, beat 1. "The ever-burning question."')
add(page(CREAM, f'<img src="{u(TILE)}" style="width:700px;height:560px;object-fit:cover;border-radius:24px;border:12px solid #fff;box-shadow:0 26px 60px rgba(0,0,0,.3);transform:rotate(-3deg);margin-bottom:60px"><div class="cap" style="font-size:112px">What mat goes with <span style="color:{PINK}">these</span> tiles?</div><div class="call" style="left:120px;top:250px;transform:rotate(-4deg)">Sunday tiles<small>@sunday_mahjong</small></div>'), 1.4, 'Real Sunday tile photo pops up (tilt -3). Label ON the tiles: Sunday @sunday_mahjong.')
add(page(CREAM, f'<img src="{u(MAT)}" style="width:680px;height:680px;object-fit:cover;border-radius:24px;border:12px solid #fff;box-shadow:0 26px 60px rgba(0,0,0,.3);transform:rotate(3deg);margin-bottom:60px"><div class="cap" style="font-size:112px">What tiles go with <span style="color:{PINK}">this</span> mat?</div><div class="call" style="right:110px;top:220px;transform:rotate(4deg)">Brownstone Bloom<small>@andersruffdesignco</small></div>'), 1.2, 'Real Brownstone Bloom mat photo (tilt +3), label on the mat.')
add(page(NAVY, f'<div class="cap" style="font-size:96px;color:#fff">Asked in every mahj Facebook group.</div><div class="cap" style="font-size:112px;color:{BLUSH};margin-top:50px">Every. Single. Day.</div>'), 1.5, 'Two lines, 2nd SLAMS on the beat ("Every. Single. Day.").')
add(page(NAVY, f'<div style="display:flex;gap:70px;align-items:center"><div class="cap" style="font-size:300px;color:#fff;opacity:.35">3</div><div class="cap" style="font-size:300px;color:#fff;opacity:.6">2</div><div style="position:relative;display:grid;place-items:center;width:420px;height:420px;border-radius:50%;border:16px solid {PINK}"><div class="cap" style="font-size:330px;color:#fff">1</div></div></div>'), 1.5, '3-2-1 countdown, one number per beat (0.5s each), pink ring pulses.')
add(page(NAVY, f'<img src="{u(FLAME)}" style="width:170px;margin-bottom:50px"><div class="cap" style="font-size:96px;color:#fff;white-space:nowrap">{FYM}</div><div class="cap" style="font-size:210px;color:{PINK};margin-top:30px">is HERE.</div><div style="font:700 40px Bit;color:{BLUSH};letter-spacing:.12em;margin-top:60px">WATCH ONE MATCH, START TO FINISH &darr;</div>' + ''.join(f'<div style="position:absolute;left:{540+sx*dx-35}px;top:{dy-35}px;width:70px;height:70px">{HEART.format(c=[PINK,BLUSH,"#fff"][a%3])}</div>' for a,(dx,dy) in enumerate([(300,300),(430,560),(440,1380),(300,1640)]) for sx in (-1,1))), 1.8, 'DROP: "Find Your Mat-ch(TM) is HERE." heart sparks burst.')
# ---------------- STEP 1 tiles
add(page(CREAM, hdr('STEP 1', 'Pick your tiles') + stage(phone('02-search.png') + ring_at(70, 662) + call_at('Sunday', 20, 735, -4, PINK, 'Sunday Mahjong @sunday_mahjong'), FULL) + cam('full phone')), 1.2, 'FULL PHONE: "Sunday" typed, ring taps the Sunday tile set. Label on the Sunday thumbnail.')
add(page(CREAM, hdr('STEP 2', 'Swipe the mats') + stage(phone('s0-b.png') + call_at('Your tiles', 30, 175, -3, NAVY, 'Sunday · @sunday_mahjong'), DUO) + cam('push in: tiles + mat')), 1.0, 'PUSH IN to tiles strip + mat card together (rule 22). Tile label sits on the tiles. First card: Ozark Carson Vintage.')
# ---------------- mats swipes (phone fixed, only the card flies)
def swipe(bg, cid, kind, label, sub, n, t, trayimg, hl=None, extra='', camv=DUO, prog=.45, note=''):  # extra = labels for the card underneath
    return page(CREAM, hdr(n, t) + stage(phone(bg) + flying(cid, kind, label, sub, prog) + extra, camv) + tray(trayimg, hl) + cam(note or 'hold: phone still, card flies'))
add(swipe('s0-a.png', 's0', 'yes', '&hearts; Carson Vintage', 'Ozark Mahjongg @ozarkmahjongg', 'STEP 2', 'Love her? &hearts;', 'tray-s0.png', '+1 suitor!'), 1.2,
    '♥ Carson Vintage tilts RIGHT + flies off, ♥ stamp on the card, ♥ button pulses; next card (Mahj & Vine) underneath. Card drops into the SUITORS tray at the bottom.')
add(swipe('s1-a.png', 's1', 'no', '&#10005; Chinoiserie Songbird', 'Mahj &amp; Vine @mahjandvine', 'STEP 2', 'Not the one? &#10005;', 'tray-s0.png', extra=call_at('next: Sunday Premium', 170, 640, 3, NAVY, '@sunday_mahjong')), 1.0,
    '✕ Chinoiserie Songbird tilts LEFT + gone, ✕ stamp on card. Sunday Premium (Sunday Mahjong\'s own mat) shows underneath.')
add(page(CREAM, hdr('MENU', 'Shop by brand') + stage(phone('20-brand-menu.png') + ring_at(102, 352) + call_at('50+ brands', 210, 120, 3, NAVY), FULL) + cam('pull back: full phone')), 0.9, 'PULL BACK to full phone: Brand ▾ sheet slides up (menu change), ring on Anders Ruff, sheet closes.')
gx, gy = META['green']
add(page(CREAM, hdr('FILTER', 'Pick a colour') + stage(phone('22-colour-before.png') + ring_at(gx, gy) + call_at('tap Green', gx - 40, gy + 50, 3, NAVY), CHIPS) + cam('push in: colour chips')), 1.0, 'PUSH IN on the colour chips: the colour wheel opens into dots, ring taps GREEN.')
add(page(CREAM, hdr('FILTER', 'Green') + stage(phone('23-colour-green.png') + call_at(f'{META["n_green"]} green mats for Sunday', 150, 250, -3, NAVY), DUO) + cam('pull to tiles + mat')), 0.8, f'Deck changes: {META["n_green"]} green mats (from {META["n_all"]}). Top card: Mahjong Row & Co. Osmanthus Grove.')
add(swipe('s2-a.png', 's2', 'no', '&#10005; Osmanthus Grove', 'Mahjong Row &amp; Co. @mahjongrowandco', 'STEP 2', 'Not the one? &#10005;', 'tray-s0.png'), 1.0,
    '✕ Osmanthus Grove flies LEFT. Brownstone Bloom is underneath.')
px, py = META['mz-plus']; mx, my = META['mz-minus']
add(page(CREAM, hdr('ZOOM', 'Tap + to zoom in') + stage(phone('mz2.png') + ring_at(px, py) + call_at('+ +', px - 120, py + 60, 3, NAVY), MATC) + cam('push in on the mat')), 1.1, 'PUSH IN on the mat card: + + taps (rings), the mat image zooms in for real (app zoom).')
cb = META['s3']
add(page(CREAM, hdr('ZOOM', 'Drag to the pattern') + stage(phone('mz3.png') + f'<div style="position:absolute;left:{P(150,520)[0]:.0f}px;top:{P(150,520)[1]:.0f}px;width:110px;height:110px;border-radius:50%;background:rgba(255,255,255,.75);border:6px solid {NAVY};z-index:45"></div><div style="position:absolute;left:{P(150,520)[0]-170:.0f}px;top:{P(150,520)[1]-110:.0f}px;font:400 120px Cap;color:{NAVY};z-index:45">&#8598;</div>', MATC) + cam('hold close')), 0.8, 'Finger drags (pan) across the leaves: brown, olive, rust up close.')
add(page(CREAM, hdr('ZOOM', 'Tap &minus; to zoom out') + stage(phone('mz4.png') + ring_at(mx, my) + call_at('&minus; &minus;', mx - 150, my + 60, -3, NAVY), DUO) + cam('pull back with the zoom')), 0.8, 'Taps − − : mat zooms back out; camera pulls back with it to tiles + mat.')
add(swipe('s3-a.png', 's3', 'yes', '&hearts; Brownstone Bloom', 'Anders Ruff @andersruffdesignco', 'STEP 2', 'Love her? &hearts;', 'tray-s3.png', '2 suitors!'), 1.2,
    '♥ Brownstone Bloom flies RIGHT, ♥ stamp, drops into the tray: 2 SUITORS (Brownstone + Carson).')
add(page(CREAM, hdr('STEP 3', 'Meet your suitors') + stage(phone('31-pick.png') + ring_at(143, 598) + call_at('Brownstone Bloom', 10, 718, -4, PINK, '@andersruffdesignco') + call_at('Carson Vintage', 205, 718, 4, PINK, '@ozarkmahjongg') + call_at('your suitors', 230, 300, 3, NAVY), (1.25, 195, 470, 540, 1040)) + cam('push in: suitor row')), 1.3, 'PUSH IN on the suitor row at the bottom of the mats step; both suitors labelled; tap Brownstone Bloom.')
# ---------------- racks
zx, zy = META['rz']
add(page(CREAM, hdr('STEP 4', 'Add racks: + + +') + stage(phone('40-rz3.png') + ring_at(zx, zy) + call_at('+ + +', zx - 140, zy + 50, 3, NAVY) + call_at('Brownstone Bloom, zoomed', 60, 28, -2, PINK, 'stays on while you pick racks'), RTOP) + cam('push in: mat preview')), 1.4, 'Racks step. PUSH IN on the mat preview above the racks: + + + (3 rings, 3 real zoom levels 40-rz0..rz3).')
add(page(CREAM, hdr('STEP 4', 'Drag to the pattern') + stage(phone('40-rz4.png') + f'<div style="position:absolute;left:{P(200,200)[0]:.0f}px;top:{P(200,200)[1]:.0f}px;width:100px;height:100px;border-radius:50%;background:rgba(255,255,255,.75);border:6px solid {NAVY};z-index:45"></div>' + call_at('dark walnut brown', 60, 28, -2, NAVY, 'golden oak + olive'), RTOP) + cam('hold close')), 0.8, 'Drag-pan to the leaves; callout names the 2 colours the racks will match (walnut brown, golden oak).')
wx, wy = 318, 390  # Wood chip as it sits in 46-wood-on (row scrolled after the tap)
add(page(CREAM, hdr('MENU', 'Pick a rack type') + stage(phone('46-wood-on.png') + ring_at(wx, wy) + call_at('Wood · Tortoise · Metallic · Clear', 20, 330, 2, NAVY), (1.6, 210, 300, 540, 900)) + cam('push in: rack chips')), 1.0, 'PUSH IN on rack-type chips, ring taps WOOD (chip turns brown); deck re-sorts.')
def rswipe(bg, cid, kind, label, sub, t, note, extra=''):
    return page(CREAM, hdr('STEP 4', t) + stage(phone(bg) + flying(cid, kind, label, sub, .4, 40) + extra, RACK) + bigbtns(kind) + cam('hold: mat stays zoomed')), note
h, n = rswipe('r0-a.png', 'r0', 'no', '&#10005; Teal Wood', 'Bam Bird Boutique · no teal in this mat', 'Not the one? &#10005;', '')
add(h, 1.0, '✕ Bam Bird TEAL Wood flies LEFT (no teal in the zoomed mat); mat stays zoomed on top; ✕ button pulses.')
h, n = rswipe('r1-a.png', 'r1', 'yes', '&hearts; Walnut', 'Bam Bird Boutique @bambirdboutique', 'Love it? &hearts;', '')
add(h, 1.1, '♥ Bam Bird WALNUT flies RIGHT: matches the dark brown leaves seen in the zoomed mat.')
h, n = rswipe('r2-a.png', 'r2', 'yes', '&hearts; Oak', 'Peace Love Mahjong @peacelovemahjong', 'Love it? &hearts;', '', call_at('next: Natural Wood', 10, 600, -3, SLATE, 'My Fair Mahjong @myfairmahjong'))
add(h, 1.1, '♥ PLM OAK flies RIGHT: matches the golden/olive leaves.')
rmx, rmy = META['rzm']
add(page(CREAM, hdr('STEP 4', 'Zoom back out') + stage(phone('47-zoom-out.png') + ring_at(rmx, rmy) + call_at('&minus; &minus; &minus;', rmx - 190, rmy + 50, -3, NAVY), RTOP) + cam('pull back')), 0.7, 'Taps − − − on the mat preview: back to the full mat. Camera pulls back.')
add(page(CREAM, hdr('STEP 5', 'Make it official') + stage(phone('51-official.png') + call_at('Walnut + Oak', 20, 640, -3, PINK, '@bambirdboutique · @peacelovemahjong') + ring_at(316, 570) + call_at('Natural Wood', 110, 300, 3, SLATE, 'My Fair Mahjong @myfairmahjong'), (1.2, 195, 560, 540, 1050)) + cam('push in: suitors + button')), 1.0, 'PUSH IN on the 2 rack suitors + "Make it official ♥" button; ring taps it.')
# ---------------- match
circ = lambda src, x, pos='50% 40%': f'<div style="position:absolute;top:520px;left:{x}px;width:400px;height:400px;border-radius:50%;border:14px solid #fff;overflow:hidden;box-shadow:0 20px 50px rgba(0,0,0,.4)"><img src="{u(src)}" style="width:100%;height:100%;object-fit:cover;object-position:{pos}"></div>'
add(page(NAVY, f'<div class="pf" style="position:absolute;top:210px;left:0;right:0;font-size:150px;color:#fff">It&rsquo;s a match!</div>' + circ(TILE, 100) + circ(MAT, 580) + f'<div style="position:absolute;top:650px;left:480px;width:120px;height:120px;z-index:5">{HEART.format(c=PINK)}</div><div style="position:absolute;left:0;right:0;top:1000px;font:700 50px Bit;color:{BLUSH}">Sunday &times; Brownstone Bloom</div><div style="position:absolute;left:0;right:0;top:1080px;font:700 40px/1.5 Bit;color:#fff">+ Bam Bird Walnut &amp; Peace Love Mahjong Oak</div><div style="position:absolute;left:0;right:0;top:1250px;font-family:Cap;font-size:90px;color:{PINK}">4 brands. 1 match.</div>'), 1.5, 'Dating-app "It\'s a match!" moment: tiles circle + mat circle, heart pops between, sparks. "4 brands. 1 match."')
add(page(NAVY, f'<img src="{u("61-card-story-full.png")}" style="height:1760px;border-radius:30px;box-shadow:0 30px 70px rgba(0,0,0,.4)">'), 2.2, 'The TALL Story 9:16 match card (real app render, 2160x3840), full size. Slow push-in.')
add(page(CREAM, hdr('SHOP', 'Codes on every piece') + stage(phone('70-shop.png') + call_at('code MAHJMATCH', 150, 452, 3, PINK, 'Anders Ruff · Bam Bird · PLM') + call_at('No code available', 120, 352, -3, SLATE, 'Sunday (add line in render)'), SHOP) + cam('push in: shop list')), 1.6, 'Shop list: every piece with Shop ›; "Discount code ›" = MAHJMATCH. Sunday row gets the "No code available" line in the render (live app shows none).')
add(page(NAVY, f'<img src="{u(FLAME)}" style="width:150px"><div class="cap" style="font-size:150px;color:#fff;margin-top:40px">Never ask<br>again.</div><div style="margin-top:70px;background:{PINK};color:#fff;border-radius:999px;padding:34px 60px;font-family:Cap;font-size:78px;white-space:nowrap">{FYM}</div><div style="font:700 54px Bit;color:#fff;margin-top:60px;letter-spacing:.06em">LINK IN BIO</div><div style="font:700 40px Bit;color:{BLUSH};margin-top:24px">mahjmatchmaker.com &middot; code MAHJMATCH</div>'), 2.5, 'END CARD: "Never ask again." pill pulses, LINK IN BIO, mahjmatchmaker.com · code MAHJMATCH.')
# ---------------- render
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920}, device_scale_factor=0.5)
    for i, (h, s, c) in enumerate(FR_, 1):
        open(f'{FR}/_f.html', 'w').write(h); pg.goto(f'file://{FR}/_f.html'); pg.wait_for_timeout(350)
        pg.screenshot(path=f'{FR}/{i:02d}.jpg', type='jpeg', quality=86)
    b.close()
os.remove(f'{FR}/_f.html')
# timing + contact sheet
t = 0; rows = []
for i, (h, s, c) in enumerate(FR_, 1): rows.append((i, t, s, c)); t += s
json.dump([dict(n=i, start=round(a, 1), secs=s, caption=c) for i, a, s, c in rows], open(f'{HERE}/frames/timing.json', 'w'), indent=1)
print('frames', len(rows), 'total', round(t, 1))
COLS = 6; TW, TH = 360, 640; CH = 190; PAD = 24
nrow = math.ceil(len(rows) / COLS); W = COLS * (TW + PAD) + PAD; H = 150 + nrow * (TH + CH + PAD)
sheet = Image.new('RGB', (W, H), CREAM); d = ImageDraw.Draw(sheet)
fb = ImageFont.truetype(f'{R}/scripts/social/tileprofile/fonts/Caprasimo.ttf', 54); fs = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 17); fn = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
d.text((PAD, 40), f'Launch reel REDO storyboard: {len(rows)} frames, ~{round(t)}s', fill=NAVY, font=fb)
import textwrap
for k, (i, a, s, c) in enumerate(rows):
    x = PAD + (k % COLS) * (TW + PAD); y = 150 + (k // COLS) * (TH + CH + PAD)
    sheet.paste(Image.open(f'{FR}/{i:02d}.jpg').resize((TW, TH)), (x, y))
    d.rounded_rectangle((x + 8, y + TH - 46, x + 70, y + TH - 8), 10, fill=PINK); d.text((x + 16, y + TH - 42), f'{i:02d}', fill='white', font=fn)
    d.text((x, y + TH + 8), f'{a:0.1f}s - {a+s:0.1f}s  ({s}s)', fill=PINK, font=fn)
    d.multiline_text((x, y + TH + 38), '\n'.join(textwrap.wrap(c, 38)[:6]), fill=NAVY, font=fs, spacing=3)
sheet.save(f'{HERE}/storyboard.jpg', quality=84); print('sheet', sheet.size)
