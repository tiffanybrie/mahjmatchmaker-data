"""The Tile Edit color cards (desktop moodboard 2000x1125 + mobile color guide 2000x3000).

Rebuilt Oct 19 as one self-contained script (the Oct 7-18 generator lived in /home/claude/newalb/tileedit/te.py + mob.py
and loose temp files). Same look as the approved cards (Amara v2, Coquette): Alfa Slab name, Lora italics, Poppins labels,
cream ground, round tile pile, backs as squares, faces as dots, rack panel, top 3 mats, navy code pill, MM badge.

Spec: config/colorcards.json -> sets.<key>. Fields used:
  name, brand, col (title color), tile (pile photo), sub (italic line under brand), backs [[NAME,#hex,role]], faces [[NAME,#hex]],
  racks [rack names]  (+ rack_imgs {name: png} for real rack photos; anything else draws as a Bird & Bamboo painted bar),
  mats [names] + mat_imgs {name: photo}, profile_line [line1, line2] (Oct 19: the short dating-profile tease that replaces
  the motif caption under the pile; falls back to 'tag'), shop (pill text).
Usage: python3 scripts/colorcards/build.py <key> [outdir]   (default outdir assets/colorcards/<key>/)
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/'
RES = R + 'scripts/colorcards/res/'
G = '/usr/share/fonts/truetype/google-fonts/'
BG = (245, 232, 220); PANEL = (251, 245, 240); EDGE = (236, 222, 210); NAVY = (31, 45, 92); GREY = (80, 80, 90)
BB_RGB = {'Lavender': (190, 175, 253), 'Dark Blue': (27, 73, 157), 'Ballet Pink': (241, 215, 251), 'Lime Green': (175, 231, 69)}  # Bird & Bamboo painted colours (from /home/claude/racks/rackpanel.py RGB table)

PINK = (214, 96, 140)
# Oct 19 (Tiffany): the cards are the set's dating PROFILE. V = None (classic Tile Edit wording), 'a' (minimal: profile wording only),
# 'b' (a bit more dating-app: verified-match heart badge on the photo, heart field labels, match count, pass/like buttons). Same look.
LAB = {None: {'hd': 'THE TILE EDIT', 'backs': 'THE BACKS', 'faces': 'THE FACES', 'racks': 'RACK MATCHES', 'mats': 'TOP MAT MATCHES'},
       'a': {'hd': 'HER PROFILE', 'backs': 'HER COLORS · BACKS', 'faces': 'HER COLORS · FACES', 'racks': "RACKS SHE'S INTO", 'mats': 'FIRST DATES'},
       'b': {'hd': 'HER PROFILE', 'backs': 'HER COLORS · BACKS', 'faces': 'HER COLORS · FACES', 'racks': "RACKS SHE'S INTO", 'mats': 'FIRST DATES'}}
V = None
def lab(k): return LAB[V][k]

def _ss(c, box, draw_fn, k=4):
    """Draw an antialiased shape: draw_fn(d, w, h) on a k-x RGBA layer, downsample, paste at box (x, y, w, h)."""
    x, y, w, h = [int(v) for v in box]
    L = Image.new('RGBA', (w * k, h * k), (0, 0, 0, 0)); draw_fn(ImageDraw.Draw(L), w * k, h * k)
    L = L.resize((w, h), Image.LANCZOS); c.paste(L, (x, y), L)
def _heart(d, cx, cy, s, fill):
    r = s * .27
    d.ellipse((cx - 1.9 * r, cy - 1.3 * r, cx, cy + .7 * r), fill=fill); d.ellipse((cx, cy - 1.3 * r, cx + 1.9 * r, cy + .7 * r), fill=fill)
    d.polygon([(cx - 1.86 * r, cy - .1 * r), (cx + 1.86 * r, cy - .1 * r), (cx, cy + 1.9 * r)], fill=fill)
def heart(c, cx, cy, s, fill=PINK):
    _ss(c, (cx - s / 2, cy - s / 2, s, s), lambda d, w, h: _heart(d, w / 2, h / 2, w, fill + (255,)))
def verified(c, cx, cy, s):
    """Verified-match badge: white-ringed pink heart with a white check."""
    def f(d, w, h):
        _heart(d, w / 2, h / 2 + w * .02, w * 1.0, (255, 255, 255, 255)); _heart(d, w / 2, h / 2 + w * .02, w * .82, PINK + (255,))
        d.line([(w * .33, h * .47), (w * .45, h * .6), (w * .68, h * .36)], fill=(255, 255, 255, 255), width=int(w * .075), joint='curve')
    _ss(c, (cx - s / 2, cy - s / 2, s, s), f)
def swipe_btns(c, cx, cy, gap, s):
    """Pass / like buttons, the dating-app swipe affordance, drawn small and refined (navy outline X, pink heart)."""
    def x(d, w, h):
        d.ellipse((4, 4, w - 4, h - 4), fill=(255, 255, 255, 255), outline=NAVY + (255,), width=int(w * .035))
        m = w * .36; d.line((m, m, w - m, h - m), fill=NAVY + (255,), width=int(w * .06)); d.line((w - m, m, m, h - m), fill=NAVY + (255,), width=int(w * .06))
    def hrt(d, w, h):
        d.ellipse((4, 4, w - 4, h - 4), fill=PINK + (255,)); _heart(d, w / 2, h / 2 + w * .02, w * .5, (255, 255, 255, 255))
    _ss(c, (cx - gap / 2 - s, cy - s / 2, s, s), x); _ss(c, (cx + gap / 2, cy - s / 2, s, s), hrt)
def label(c, d, x, y, t, f, fill, sp, center=False, hs=None):
    """Section label; in variant b a small pink heart leads it (field-label look)."""
    if V != 'b': return spaced(d, x, y, t, f, fill, sp, center)
    hs = hs or int(f.size * .9); tw = sum(d.textlength(ch, font=f) + sp for ch in t) - sp
    g = max(14, int(f.size * .42)); x0 = x - (tw + hs + g) / 2 if center else x
    heart(c, x0 + hs / 2, y + f.size * .62, hs); spaced(ImageDraw.Draw(c), x0 + hs + g, y, t, f, fill, sp)
def count_pill(c, cx, cy, n, fs):
    d = ImageDraw.Draw(c); t = f'{n} MATCHES & COUNTING'; f = P('Poppins-Bold.ttf', fs); sp = fs * .14
    tw = sum(d.textlength(ch, font=f) + sp for ch in t) - sp; hs = fs * 1.05; w = tw + hs + fs * 2.6; h = fs * 2.2
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), radius=h / 2, fill=(255, 255, 255), outline=PINK, width=max(2, int(fs * .12)))
    heart(c, cx - w / 2 + fs * 1.2 + hs / 2, cy, hs); spaced(ImageDraw.Draw(c), cx - w / 2 + fs * 1.2 + hs + fs * .5, cy - fs * .68, t, f, PINK, sp)

def P(n, s): return ImageFont.truetype(G + n, int(s))
def lora(s, w=400):
    f = ImageFont.truetype(G + 'Lora-Italic-Variable.ttf', int(s))
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f
def alfa(s): return ImageFont.truetype(RES + 'AlfaSlab.ttf', int(s))
def hx(h): h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
def pale(h): r, g, b = hx(h); return .299 * r + .587 * g + .114 * b > 215  # near-cream swatch: give it a thin edge so it reads on the cream ground
def spaced(d, x, y, t, f, fill, sp, center=False):
    tw = sum(d.textlength(ch, font=f) + sp for ch in t) - sp
    if center: x = x - tw / 2
    for ch in t: d.text((x, y), ch, font=f, fill=fill); x += d.textlength(ch, font=f) + sp
def sq(im, n):
    im = im.convert('RGB'); s = min(im.size)
    return im.crop(((im.width - s) // 2, (im.height - s) // 2, (im.width + s) // 2, (im.height + s) // 2)).resize((n, n), Image.LANCZOS)
def rmask(n, r):
    m = Image.new('L', (n, n), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, n - 1, n - 1), radius=r, fill=255); return m

def _bb_hex(nm):
    """Oct 21: any other B&B colour comes from builder/bbracks.json (the B&B paint table), never a grey placeholder bar."""
    try:
        for r in json.load(open(R + 'builder/bbracks.json')):
            if r.get('name') == nm: return hx(r['hex'])
    except Exception: pass
    return None

def rack_strip(S, name, w, h, maxh=None):
    """Real rack photo (rack_imgs) or a Bird & Bamboo painted bar, returned RGBA w x h.
    maxh (Oct 19): tall rack photos (scalloped, tortoise) are scaled down to fit the row so they never cover the next label."""
    p = (S.get('rack_imgs') or {}).get(name)
    if p:
        im = Image.open(R + p).convert('RGBA'); bb = im.getbbox(); im = im.crop(bb)
        nh = max(8, int(im.height * w / im.width))
        if maxh and nh > maxh: return im.resize((max(8, int(im.width * maxh / im.height)), maxh), Image.LANCZOS)
        return im.resize((w, nh), Image.LANCZOS)
    col = BB_RGB.get(name.replace('Bird & Bamboo ', '')) or _bb_hex(name.replace('Bird & Bamboo ', '')) or (200, 200, 200)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=5, fill=col)
    dk = tuple(max(0, int(v * .82)) for v in col); lt = tuple(min(255, int(v * 1.12)) for v in col)
    d.line((2, 3, w - 3, 3), fill=lt, width=3); d.line((2, h - 4, w - 3, h - 4), fill=dk, width=4); d.line((2, h // 2, w - 3, h // 2), fill=dk, width=2)
    return im

def rack_label(name):
    for b in ('Peace Love Mahjong', 'Bird & Bamboo', 'Middle & Main', 'Miss Mahjong', 'Oh My Mahjong', 'Bam Bird Boutique', 'Mahjong Row & Co.', 'Tigre de Tartán'):
        if name.startswith(b + ' '): return b, name[len(b) + 1:]
    return '', name

def pile_circle(c, S, cx, cy, R0):
    W, H = c.size
    pile = sq(Image.open(R + S['tile']), 2 * R0)
    ring = Image.new('L', (W, H), 0); ImageDraw.Draw(ring).ellipse((cx - R0 - 14, cy - R0 - 14, cx + R0 + 14, cy + R0 + 14), fill=255)
    sh = Image.new('L', (W, H), 0); ImageDraw.Draw(sh).ellipse((cx - R0 - 10, cy - R0 + 2, cx + R0 + 18, cy + R0 + 22), fill=90); sh = sh.filter(ImageFilter.GaussianBlur(12))
    c.paste((120, 100, 80), (0, 0), sh); c.paste((232, 216, 200), (0, 0), ring)
    m = Image.new('L', (2 * R0, 2 * R0), 0); ImageDraw.Draw(m).ellipse((0, 0, 2 * R0 - 1, 2 * R0 - 1), fill=255); c.paste(pile, (cx - R0, cy - R0), m)

def title(d, S, x, y, maxw, start, center=False):
    t = S['name'].upper(); size = start
    while d.textlength(t, font=alfa(size)) > maxw and size > 60: size -= 2
    f = alfa(size); tw = d.textlength(t, font=f); x0 = x - tw / 2 if center else x
    d.text((x0 + 6, y + 6), t, font=f, fill=(255, 255, 255), stroke_width=7, stroke_fill=(255, 255, 255))
    d.text((x0, y), t, font=f, fill=hx(S['col']))
    return size

def line2(S): return S.get('profile_line') or S.get('tag') or ['', '']

def rack_panel(c, S, x0, x1, y, rowh=150, fs=20):
    """Rack rows: small brand · colour label, then the rack. Returns y after the last row."""
    d = ImageDraw.Draw(c); w = x1 - x0
    for n in S['racks']:
        b, col = rack_label(n)
        d.text((x0 + 2, y), (b.upper() + '  ·  ' if b else ''), font=P('Poppins-Bold.ttf', fs * .8), fill=(160, 120, 140))
        bw = d.textlength((b.upper() + '  ·  ' if b else ''), font=P('Poppins-Bold.ttf', fs * .8))
        d.text((x0 + 2 + bw, y - 3), col, font=P('Poppins-Medium.ttf', fs * 1.15), fill=NAVY)
        st = rack_strip(S, n, w, int(rowh * .42), max(int(rowh * .42), rowh - int(fs * 1.9) - int(fs * 1.4))); c.paste(st, (x0 + (w - st.width) // 2, y + int(fs * 1.9)), st); d = ImageDraw.Draw(c)
        y += rowh
    return y

def mats_row(c, S, x0, y, n, gap, fs):
    d = ImageDraw.Draw(c)
    for i, name in enumerate(S['mats'][:3]):
        im = sq(Image.open(R + S['mat_imgs'][name]), n); X = x0 + i * (n + gap)
        c.paste(im, (X, y), rmask(n, 14)); d = ImageDraw.Draw(c); f = fs
        while d.textlength(name, font=P('Poppins-Regular.ttf', f)) > n + gap - 6 and f > 14: f -= 1
        d.text((X + n / 2, y + n + 22), name, font=P('Poppins-Regular.ttf', f), fill=NAVY, anchor='mm')

def desktop(S, out):
    W, H = 2000, 1125; c = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(c)
    label(c, d, 70, 66, lab('hd'), P('Poppins-Bold.ttf', 30), NAVY, 7); d = ImageDraw.Draw(c)
    ts = title(d, S, 60, 104, 690, 128)
    dy = 0 if ts >= 120 else int((120 - ts) * 1.1)  # long names set smaller: pull the brand lines up to close the gap
    d.text((66, 300 - dy), 'by ' + S['brand'], font=lora(44), fill=NAVY)
    d.text((66, 365 - dy), S['sub'], font=lora(29), fill=GREY)
    label(c, d, 70, 445, lab('backs'), P('Poppins-Bold.ttf', 26), NAVY, 6); d = ImageDraw.Draw(c)
    for i, (n, h, role) in enumerate(S['backs']):
        x = 70 + i * 190; d.rounded_rectangle((x, 482, x + 170, 652), radius=16, fill=hx(h), outline=EDGE if pale(h) else None, width=3)
        d.text((x + 85, 675), n, font=P('Poppins-Medium.ttf', 21), fill=NAVY, anchor='mm'); d.text((x + 85, 704), role, font=P('Poppins-Regular.ttf', 18), fill=(90, 90, 100), anchor='mm')
    label(c, d, 70, 757, lab('faces'), P('Poppins-Bold.ttf', 26), NAVY, 6); d = ImageDraw.Draw(c)
    F = S['faces']; per = 3 if len(F) > 4 else 2 if len(F) == 4 else 3
    for i, (n, h) in enumerate(F):
        cx = 125 + (i % per) * 190; cy = 838 + (i // per) * 150
        d.ellipse((cx - 46, cy - 46, cx + 46, cy + 46), fill=(255, 255, 255)); d.ellipse((cx - 42, cy - 42, cx + 42, cy + 42), fill=hx(h))
        d.text((cx, cy + 63), n, font=P('Poppins-Medium.ttf', 20), fill=NAVY, anchor='mm')
    pile_circle(c, S, 1030, 470, 300); d = ImageDraw.Draw(c)
    if V == 'b': verified(c, 1030 + 222, 470 + 222, 104); d = ImageDraw.Draw(c)
    d.line((900, 800, 1160, 800), fill=(225, 205, 185), width=3)
    l1, l2 = line2(S)
    d.text((1030, 828), l1, font=lora(31, 500), fill=NAVY, anchor='mm'); d.text((1030, 873), l2, font=lora(31, 500), fill=NAVY, anchor='mm')
    BD = Image.open(RES + 'mm_badge.png').convert('RGBA'); c.paste(BD, (840, 970), BD); d = ImageDraw.Draw(c)
    if V == 'b':
        count_pill(c, 1030, 930, S.get('matches', 50), 19); swipe_btns(c, 1030, 1040, 380 + 64, 84); d = ImageDraw.Draw(c)
    d.rounded_rectangle((1382, 42, 1954, 1084), radius=36, fill=PANEL, outline=EDGE, width=3)
    label(c, d, 1668, 66, lab('racks'), P('Poppins-Bold.ttf', 30), NAVY, 8, True); d = ImageDraw.Draw(c)
    rack_panel(c, S, 1418, 1918, 150, rowh=min(178, 534 // max(1, len(S['racks']))), fs=20)  # Oct 21: 4 racks (Brownstone) share the 3-rack height; d = ImageDraw.Draw(c)
    label(c, d, 1668, 690, lab('mats'), P('Poppins-Bold.ttf', 28), NAVY, 7, True); d = ImageDraw.Draw(c)
    mats_row(c, S, 1412, 742, 150, 20, 21); d = ImageDraw.Draw(c)
    d.rounded_rectangle((1420, 958, 1916, 1020), radius=31, fill=NAVY)
    t = S.get('shop', 'Shop OMM · code MAHJMATCH'); fs = 26
    while fs > 16 and d.textlength(t, font=P('Poppins-Bold.ttf', fs)) > 456: fs -= 1  # Oct 21: longer pill text shrinks to fit (desktop + mobile say the same thing)
    d.text((1668, 989), t, font=P('Poppins-Bold.ttf', fs), fill=(255, 255, 255), anchor='mm')
    c.save(out, quality=92)

def mobile(S, out):
    """Phone color guide, drawn at 2x (2000x3000), layout of the approved Coquette phone card."""
    K = 1.5; W, H = 2000, 3000; c = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(c)
    label(c, d, W / 2, 105, lab('hd'), P('Poppins-Bold.ttf', 30 * K), NAVY, 9 * K, True); d = ImageDraw.Draw(c)
    title(d, S, W / 2, 175, 1640, 250, center=True)
    d.text((W / 2, 510), 'by ' + S['brand'], font=lora(44 * K), fill=NAVY, anchor='mm')
    d.text((W / 2, 600), S['sub'], font=lora(29 * K), fill=GREY, anchor='mm')
    pile_circle(c, S, W // 2, 1140, 420); d = ImageDraw.Draw(c)
    if V == 'b':
        verified(c, W // 2 + 312, 1140 + 312, 140); swipe_btns(c, W // 2, 1140, 2 * 420 + 150, 132); count_pill(c, W // 2, 660, S.get('matches', 50), 22); d = ImageDraw.Draw(c)
    l1, l2 = line2(S)
    d.line((W / 2 - 200, 1640, W / 2 + 200, 1640), fill=(225, 205, 185), width=4)
    d.text((W / 2, 1695), l1, font=lora(34 * K, 500), fill=NAVY, anchor='mm'); d.text((W / 2, 1772), l2, font=lora(34 * K, 500), fill=NAVY, anchor='mm')
    # backs + faces panel
    d.rounded_rectangle((80, 1830, 1920, 2300), radius=48, fill=PANEL)
    label(c, d, 500, 1868, lab('backs').replace('HER COLORS · ', 'HER '), P('Poppins-Bold.ttf', 27 * K), NAVY, 7 * K, True); d = ImageDraw.Draw(c)
    for i, (n, h, role) in enumerate(S['backs']):
        x = 140 + i * 256; d.rounded_rectangle((x, 1940, x + 222, 2162), radius=22, fill=hx(h), outline=EDGE if pale(h) else None, width=4)
        d.text((x + 111, 2196), n, font=P('Poppins-Medium.ttf', 22 * K), fill=NAVY, anchor='mm'); d.text((x + 111, 2244), role, font=P('Poppins-Regular.ttf', 20 * K), fill=(90, 90, 100), anchor='mm')
    label(c, d, 1490, 1868, lab('faces').replace('HER COLORS · ', 'HER '), P('Poppins-Bold.ttf', 27 * K), NAVY, 7 * K, True); d = ImageDraw.Draw(c)
    F = S['faces']; per = 3 if len(F) > 4 else 2
    for i, (n, h) in enumerate(F):
        cx = (1250 + (i % per) * 240) if per == 3 else (1370 + (i % per) * 240); cy = 2000 + (i // per) * 182
        d.ellipse((cx - 56, cy - 56, cx + 56, cy + 56), fill=(255, 255, 255)); d.ellipse((cx - 52, cy - 52, cx + 52, cy + 52), fill=hx(h))
        d.text((cx, cy + 84), n, font=P('Poppins-Medium.ttf', 20 * K), fill=NAVY, anchor='mm')
    # racks + mats panel
    d.rounded_rectangle((80, 2340, 1920, 2960), radius=48, fill=PANEL)
    label(c, d, 540 if V is None else 516, 2380, lab('racks'), P('Poppins-Bold.ttf', 27 * K), NAVY, 7 * K, True); d = ImageDraw.Draw(c)
    rack_panel(c, S, 132, 900, 2452, rowh=min(158, 474 // max(1, len(S['racks']))), fs=28); d = ImageDraw.Draw(c)
    label(c, d, 1450, 2380, lab('mats'), P('Poppins-Bold.ttf', 27 * K), NAVY, 7 * K, True); d = ImageDraw.Draw(c)
    mats_row(c, S, 1035, 2470, 250, 42, 30); d = ImageDraw.Draw(c)
    d.rounded_rectangle((1040, 2812, 1860, 2896), radius=42, fill=NAVY)
    d.text((1450, 2854), S.get('shop_m', S.get('shop', 'Code MAHJMATCH')), font=P('Poppins-Bold.ttf', 34), fill=(255, 255, 255), anchor='mm')
    c.save(out, quality=92)

if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if not x.startswith('--profile=')]; pv = [x.split('=')[1] for x in sys.argv[1:] if x.startswith('--profile=')]
    key = a[0]; S = json.load(open(R + 'config/colorcards.json'))['sets'][key]
    out = a[1] if len(a) > 1 else R + f'assets/colorcards/{key}/'
    os.makedirs(out, exist_ok=True)
    if pv:  # --profile=a or --profile=b : the dating-PROFILE versions (Oct 19 DRAFT), written next to the classic files
        V = pv[0]
        desktop(S, out + f'00-{key}-mahjong-tiles-profile-{V}-desktop.jpg'); mobile(S, out + f'00-{key}-mahjong-tiles-profile-{V}-mobile.jpg')
    else:
        desktop(S, out + f'00-{key}-mahjong-tiles-tile-edit-moodboard.jpg'); mobile(S, out + f'00-{key}-mahjong-tiles-color-guide-mobile.jpg')
    print('ok', key, out)
