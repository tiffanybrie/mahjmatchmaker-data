#!/usr/bin/env python3
"""Three Juniper practice reels (Tiffany Nov 12 8:14am): find the repeatable Find Your Mat-ch reel format.
  A  brand-on-brand: Juniper + only Oh My Mahjong mats (new + retired) and OMM racks ("Same brand as my tiles")
  B  "Playing the field with Juniper": photo-dump hook, then fast cross-brand Table/Aerial snippets + match cards
  C  short "Which mat would you pick?" 4-up vote reel that ends on the comment-for-the-link ask
1080x1920 @30fps, no audio (she adds the song). Phone screens are real app captures (white iPhone, iphone_white.py).
Usage: fym_reels_nov12.py <A|B|C|all> <outdir>"""
import sys, os, math, subprocess, glob
from PIL import Image, ImageDraw, ImageFont, ImageFilter
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) + '/'
sys.path.insert(0, R + 'scripts/social/phone'); import iphone_white as IW
W, H, FPS = 1080, 1920, 30
NAVY, PINK, HEART, BLUSH = (5, 70, 137), (200, 50, 95), (245, 108, 140), (253, 238, 243)
FD = R + 'scripts/social/tileprofile/fonts/'
CAP = lambda s: ImageFont.truetype(FD + 'Caprasimo.ttf', s)
SANS = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', s)
CAPT = '/tmp/jr/'   # raw captures (cap2.py / fym_capture.py), 1170x2532
eo = lambda x: 1 - (1 - min(max(x, 0), 1)) ** 3
def eb(x):
    x = min(max(x, 0), 1); c1 = 1.70158; return 1 + (c1 + 1) * (x - 1) ** 3 + c1 * (x - 1) ** 2

# ---------- phone ----------
SX, SY = IW.BT + IW.FR + IW.BZ, IW.FR + IW.BZ
_blank = '/tmp/jr/_blank.png'; Image.new('RGB', (1170, 2532), 'white').save(_blank)
IW.phone(_blank, '/tmp/jr/_frame.png'); FRAME = Image.open('/tmp/jr/_frame.png').convert('RGBA')
MASK = Image.new('L', (IW.SW * 2, IW.SH * 2), 0); ImageDraw.Draw(MASK).rounded_rectangle([0, 0, IW.SW * 2 - 1, IW.SH * 2 - 1], radius=IW.SR * 2, fill=255)
MASK = MASK.resize((IW.SW, IW.SH), Image.LANCZOS)
ISL = Image.new('RGBA', (378, 111), (0, 0, 0, 0)); ImageDraw.Draw(ISL).rounded_rectangle([0, 0, 377, 110], radius=56, fill=(0, 0, 0, 255))
PSC = 960 / FRAME.width          # big phone, bottom runs off the frame: the mat card is the hero
_sc = {}
def screen(path):
    """raw 1170x2532 capture (or a framed fym-phones png) -> screen content with status bar"""
    if path not in _sc:
        im = Image.open(path).convert('RGBA')
        if im.size != (IW.SW, IW.SH):   # already framed: cut the screen back out (it has its status bar)
            _sc[path] = im.crop((SX, SY, SX + IW.SW, SY + IW.SH))
        else: _sc[path] = IW.statusbar(im)
    return _sc[path]
def phone_img(scr):
    ph = FRAME.copy(); ph.paste(scr, (SX, SY), MASK); ph.alpha_composite(ISL, (SX + (IW.SW - 378) // 2, SY + 33)); return ph
def paste(cv, im, cx, cy, s, a=1.0, rot=0):
    if s <= 0.01 or a <= 0.01: return
    r = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)
    if rot: r = r.rotate(rot, resample=Image.BICUBIC, expand=True)
    if a < 1: r.putalpha(r.getchannel('A').point(lambda v: int(v * a)))
    cv.alpha_composite(r, (int(cx - r.width / 2), int(cy - r.height / 2)))
def tap(scr, x, y, k):
    """finger-tap ring on a screen (x,y in 390pt coords) at progress k 0..1"""
    s = scr.copy(); d = ImageDraw.Draw(s); r = 40 + 70 * k; a = int(170 * (1 - k))
    ov = Image.new('RGBA', s.size, (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.ellipse([x * 3 - r, y * 3 + IW.SB - r, x * 3 + r, y * 3 + IW.SB + r], fill=(200, 50, 95, a // 2), outline=(255, 255, 255, a), width=8)
    s.alpha_composite(ov); return s

# ---------- text ----------
def text_img(lines, size, color=NAVY, bg=None, pad=34, sub=None, subsize=44, subcolor=PINK, maxw=980):
    f = CAP(size); fs = SANS(subsize)
    while max(f.getlength(l) for l in lines) > maxw - 2 * pad: size -= 4; f = CAP(size)
    lh = int(size * 1.05); w = int(max([f.getlength(l) for l in lines] + ([fs.getlength(sub)] if sub else []))) + 2 * pad
    h = lh * len(lines) + 2 * pad + (int(subsize * 1.6) if sub else 0)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if bg: d.rounded_rectangle([0, 0, w - 1, h - 1], radius=44, fill=bg)
    for i, l in enumerate(lines): d.text((w / 2, pad + i * lh), l, font=f, fill=color, anchor='ma')
    if sub: d.text((w / 2, pad + len(lines) * lh + 10), sub, font=fs, fill=subcolor, anchor='ma')
    return im
def pill(t, size=46, fg=(255, 255, 255), bg=PINK):
    f = SANS(size); w = int(f.getlength(t)) + 70; im = Image.new('RGBA', (w, size + 44), (0, 0, 0, 0))
    d = ImageDraw.Draw(im); d.rounded_rectangle([0, 0, w - 1, size + 43], radius=(size + 44) // 2, fill=bg); d.text((w / 2, (size + 44) / 2), t, font=f, fill=fg, anchor='mm'); return im
HEARTI = Image.new('RGBA', (300, 270), (0, 0, 0, 0)); _h = ImageDraw.Draw(HEARTI)
_h.ellipse([0, 0, 160, 160], fill=HEART + (255,)); _h.ellipse([140, 0, 300, 160], fill=HEART + (255,)); _h.polygon([(12, 115), (288, 115), (150, 268)], fill=HEART + (255,))
def card_img(path, maxw=900, maxh=1500, border=18):
    """a match card / profile card, trimmed of white margins, in a white frame with a soft shadow (never edge to edge)"""
    im = Image.open(path).convert('RGBA')
    bg = Image.new('RGBA', im.size, (255, 255, 255, 255)); diff = Image.eval(Image.alpha_composite(bg, im).convert('L'), lambda v: 255 if v < 246 else 0)
    bb = diff.getbbox()
    if bb: im = im.crop(bb)
    s = min(maxw / im.width, maxh / im.height); im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    out = Image.new('RGBA', (im.width + 2 * border + 60, im.height + 2 * border + 60), (0, 0, 0, 0))
    sh = Image.new('RGBA', out.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([30, 40, out.width - 30, out.height - 20], radius=30, fill=(20, 30, 60, 70))
    out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)))
    ImageDraw.Draw(out).rounded_rectangle([30, 30, out.width - 30, out.height - 30], radius=26, fill=(255, 255, 255, 255))
    out.alpha_composite(im, (30 + border, 30 + border)); return out

# ---------- timeline engine ----------
class Reel:
    def __init__(s): s.items = []   # (t0, t1, fn(cv, t_local, k))
    def add(s, t0, dur, fn): s.items.append((t0, t0 + dur, fn)); return t0 + dur
    def render(s, out, dur, bg=BLUSH):
        p = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                              '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '19', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
        for n in range(int(dur * FPS)):
            t = n / FPS; cv = Image.new('RGBA', (W, H), bg + (255,))
            for t0, t1, fn in s.items:
                if t0 <= t < t1: fn(cv, t - t0, (t - t0) / (t1 - t0))
            p.stdin.write(cv.convert('RGB').tobytes())
            if n % 60 == 0: cv.convert('RGB').save(out.replace('.mp4', f'-f{n // FPS:02d}.jpg'), quality=70)
        p.stdin.close(); p.wait()

def phone_track(rl, t0, shots, cy=None, rise=True):
    """shots: list of (screen RGBA or callable(k)->RGBA, dur, transition 'cut'|'fade'|'swipe'|'swipeL', heart)"""
    cy = cy or 430 + FRAME.height * PSC / 2
    T = [t0]
    for sh in shots: T.append(T[-1] + sh[1])
    total = T[-1] - t0
    def fn(cv, tl, k):
        t = t0 + tl; i = max(j for j in range(len(shots)) if T[j] <= t + 1e-9); sh = shots[i]
        kk = (t - T[i]) / sh[1]; cur = sh[0](kk) if callable(sh[0]) else sh[0]
        img = cur; tr = sh[2]; hz = 0; trd = 0.22
        if i > 0 and (t - T[i]) < trd and tr != 'cut':
            prev = shots[i - 1][0](1.0) if callable(shots[i - 1][0]) else shots[i - 1][0]; q = max(0.0, (t - T[i]) / trd)
            if tr == 'fade': img = Image.blend(prev, cur, eo(q))
            else:
                img = cur.copy(); sgn = 1 if tr == 'swipe' else -1; dx = int(sgn * q ** 1.5 * IW.SW * 1.15)
                img.alpha_composite(prev.rotate(-9 * sgn * q, resample=Image.BICUBIC), (dx, int(70 * q))); hz = q if (tr == 'swipe') else 0
        r = eo(tl / 0.55) if rise else 1; push = 1 + 0.05 * k
        paste(cv, phone_img(img), W / 2, cy + (1 - r) * 1100, PSC * push)
        if sh[3] or hz:
            q = hz or min(1, kk * 3); paste(cv, HEARTI, W / 2 + 330, 900, 0.45 + 0.5 * q, math.sin(math.pi * min(q, 1)))
    rl.add(t0, total, fn); return t0 + total
def caption(rl, t0, dur, img, cy=300, pop=True):
    def fn(cv, tl, k):
        s = eb(tl / 0.35) if pop else 1; a = min(1, tl / 0.15, (dur - tl) / 0.15)
        paste(cv, img, W / 2, cy, 0.6 + 0.4 * s, a)
    return rl.add(t0, dur, fn)
def end_card(rl, t0, dur, kicker, big, small, cta='Comment MATCH'):
    K = text_img([kicker], 64, PINK); B = text_img(big, 128, NAVY); S = text_img(small, 52, NAVY)
    P = pill(cta, 64, (255, 255, 255), NAVY)
    def fn(cv, tl, k):
        ImageDraw.Draw(cv).rectangle([0, 0, W, H], fill=BLUSH)
        paste(cv, K, W / 2, 640, 1, min(1, tl / 0.2)); paste(cv, B, W / 2, 820, 0.7 + 0.3 * eb(tl / 0.4))
        paste(cv, P, W / 2, 1080, eb((tl - 0.3) / 0.4)); paste(cv, HEARTI, W / 2 + P.width / 2 + 20, 1050, 0.28 * eb((tl - 0.5) / 0.4), 1, -12)
        paste(cv, S, W / 2, 1260, 1, min(1, max(0, (tl - 0.5) / 0.3)))
    return rl.add(t0, dur, fn)

O2 = CAPT + 'omm2/'; O1 = CAPT + 'omm/raw/'
JL = R + 'assets/social/juniper-launch/fym-phones/juniper-fym-phone-'
CARD = R + 'assets/cards/juniper-final/juniper-mahjong-tiles-'
TILES = R + 'assets/tiles/album/juniper.jpg'

def fullbleed(path):
    im = Image.open(path).convert('RGBA'); s = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * s) + 2, int(im.height * s) + 2), Image.LANCZOS)
    return im.crop(((im.width - W) // 2, (im.height - H) // 2, (im.width - W) // 2 + W, (im.height - H) // 2 + H))

def reel_A(out):
    """Brand-on-brand: Juniper x Oh My Mahjong"""
    rl = Reel(); t = 0
    # HOOK 0-2.2s: Juniper tiles, OMM match cards pile on (new + retired)
    tiles = fullbleed(TILES)
    cards = [card_img(CARD + f'oh-my-mahjong-{k}-mat.jpg', 760, 950) for k in ('lotus-cove', 'camellia', 'birdie-green', 'esme', 'yuletide')]
    def hook(cv, tl, k):
        cv.alpha_composite(tiles)
        for i, c in enumerate(cards):
            q = (tl - 0.25 - i * 0.3) / 0.25
            if q > 0: paste(cv, c, W / 2 + (-1) ** i * 40, 1080 + i * 18, 0.95 + 0.25 * (1 - eo(q)), min(1, q * 2), (-1) ** i * (3 + i))
    t = rl.add(0, 2.2, hook)
    head = text_img(['Juniper + your', 'Oh My Mahjong mats'], 92, NAVY, (255, 255, 255, 235), sub='new ones + retired favorites')
    caption(rl, 0.1, 2.1, head, 300)
    # PHONE: same brand as my tiles -> deck of OMM mats
    s1, s2 = screen(O2 + '01-before.png'), screen(O2 + '02-samebrand.png')
    shots = [(s1, 0.55, 'cut', 0), (lambda k: tap(s1, 129, 612, k), 0.35, 'cut', 0), (s2, 0.6, 'cut', 0)]
    deck = sorted(glob.glob(O2 + '1*-deck.png'))[:10]
    shots += [(screen(p), 0.36, 'swipeL', 0) for p in deck]
    typing = [O2 + f'2{k}-type.png' for k in (1, 2, 3, 4, 5)]
    shots += [(screen(p), 0.22, 'cut', 0) for p in typing] + [(screen(O2 + '30-camellia.png'), 0.5, 'cut', 0), (screen(O2 + '31-heart.png'), 0.6, 'cut', 1)]
    shots += [(screen(O2 + f'4{k}-rack.png'), 0.55, 'fade', 0) for k in range(6)]
    shots += [(screen(O1 + p), 0.75, 'swipe', 0) for p in ('1-1-table-lotus-cove.png', '3-1-table-birdie-green.png', '4-1-table-esme.png')]
    t2 = phone_track(rl, t, shots)
    T = t; caps = [(1.5, 'Tap "Same brand as my tiles"'), (3.6, 'Only Oh My Mahjong mats'), (1.6, 'Own an old one? Search it'), (3.3, 'Table view · try every OMM rack'), (t2 - t - 10.0, 'Set the table')]
    for d, c in caps: caption(rl, T, d, text_img([c], 70, NAVY, (255, 255, 255, 235)), 250); T += d
    t = end_card(rl, t2, 2.6, 'Find Your Mat-ch', ['Style Juniper with', 'your OMM mats'], ['Comment for the link', 'Code MAHJMATCH at Oh My Mahjong'])
    rl.render(out, t)

def reel_B(out):
    """Playing the field with Juniper: photo dump, then fast cross-brand snippets"""
    rl = Reel(); tiles = fullbleed(TILES)
    keys = ['mahj-tile-haus-palm-royale', 'anders-ruff-flora-belle', 'oh-my-mahjong-lotus-cove', 'bespoke-mahjong-garden-glow-emerald-green', 'miss-mahjong-cherry-blossom-jade',
            'bespoke-mahjong-jungle-hot-pink', 'betty-june-and-jeannette-the-kerry', 'mahj-and-vine-zesty-plume', 'britt-mills-emerald-mirage', 'that-mahjong-moment-evergreen',
            'lets-be-besties-paint-feathers', 'oh-my-mahjong-camellia', 'britt-mills-reba', 'mahj-mood-emerald-cove']
    cards = [card_img(CARD + k + '-mat.jpg', 700, 875) for k in keys]
    def hook(cv, tl, k):
        cv.alpha_composite(tiles)
        for i, c in enumerate(cards):
            q = (tl - 0.3 - i * 0.14) / 0.18
            if q > 0: paste(cv, c, W / 2 + ((i * 137) % 260 - 130), 1050 + ((i * 89) % 220 - 110), 0.95 + 0.3 * (1 - eo(q)), min(1, q * 2), ((i * 53) % 18) - 9)
    t = rl.add(0, 2.6, hook)
    caption(rl, 0.1, 2.5, text_img(['Playing the field', 'with Juniper'], 110, NAVY, (255, 255, 255, 235), sub='42 mats matched'), 300)
    # profile card 'but she likes to play the field', fitted to the frame
    pc = card_img(R + 'assets/social/juniper-launch/profile-cards-png/juniper-profile-card-7-but-she-likes-to-play-the-field.png', 940, 1640, 0)
    t = rl.add(t, 1.3, lambda cv, tl, k: paste(cv, pc, W / 2, H / 2 + 20, 0.92 + 0.08 * eb(tl / 0.35)))
    mats = ['palm-royale', 'flora-belle', 'lotus-cove', 'garden-glow', 'cherry-blossom-jade', 'zesty-plume']
    ck = {'palm-royale': keys[0], 'flora-belle': keys[1], 'lotus-cove': keys[2], 'garden-glow': keys[3], 'cherry-blossom-jade': keys[4], 'zesty-plume': keys[7]}
    for j, m in enumerate(mats):
        shots = [(screen(JL + f'2-aerial-{m}.png'), 0.5, 'cut' if j == 0 else 'swipe', 0), (screen(JL + f'1-table-{m}.png'), 0.75, 'fade', 0)]
        t = phone_track(rl, t, shots, rise=(j == 0))
        if j % 2 == 1 or j == len(mats) - 1:   # match card snippet every other mat
            c = card_img(CARD + ck[m] + '-mat.jpg', 900, 1125)
            t = rl.add(t, 0.75, lambda cv, tl, k, c=c: (paste(cv, c, W / 2, H / 2 + 40, 0.9 + 0.1 * eb(tl / 0.3)), paste(cv, HEARTI, W / 2 + 360, 470, 0.35 * eb(tl / 0.3), 1, -12)))
    caption(rl, 3.9, t - 3.9, text_img(['Find Your Mat-ch'], 84, NAVY, (255, 255, 255, 235), sub='Aerial · Table · racks'), 250, pop=False)
    t = end_card(rl, t, 2.6, 'Your tiles, every mat', ['Find Your Mat-ch'], ['Comment for the link', 'Code MAHJMATCH at partner shops'])
    rl.render(out, t)

def reel_C(out):
    """Which would you pick? 4 mats, numbered, comment your number"""
    rl = Reel(); tiles = fullbleed(TILES)
    t = rl.add(0, 1.4, lambda cv, tl, k: cv.alpha_composite(tiles))
    caption(rl, 0.05, 1.35, text_img(['Which mat would', 'you pick for Juniper?'], 100, NAVY, (255, 255, 255, 235)), 1500)
    mats = ['palm-royale', 'lotus-cove', 'cherry-blossom-jade', 'flora-belle']
    for j, m in enumerate(mats):
        t0 = t; t = phone_track(rl, t, [(screen(JL + f'1-table-{m}.png'), 1.5, 'cut' if j == 0 else 'swipe', 0)], rise=(j == 0))
        num = text_img([str(j + 1)], 190, (255, 255, 255), PINK, pad=40)
        caption(rl, t0, 1.5, num, 330)
    t = end_card(rl, t, 2.8, 'Your vote', ['1, 2, 3 or 4?'], ["I'll send you the link to", 'try it with your own tiles'], cta='Comment 1, 2, 3 or 4')
    rl.render(out, t)

if __name__ == '__main__':
    which, od = sys.argv[1], sys.argv[2]; os.makedirs(od, exist_ok=True)
    for k, f in (('A', reel_A), ('B', reel_B), ('C', reel_C)):
        if which in (k, 'all'): f(f'{od}/juniper-reel-{k}.mp4'); print('done', k, flush=True)
