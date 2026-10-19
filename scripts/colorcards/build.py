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
BB_RGB = {'Lavender': (190, 175, 253)}  # Bird & Bamboo painted colours (from /home/claude/racks/rackpanel.py RGB table)

def P(n, s): return ImageFont.truetype(G + n, int(s))
def lora(s, w=400):
    f = ImageFont.truetype(G + 'Lora-Italic-Variable.ttf', int(s))
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f
def alfa(s): return ImageFont.truetype(RES + 'AlfaSlab.ttf', int(s))
def hx(h): h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
def spaced(d, x, y, t, f, fill, sp, center=False):
    tw = sum(d.textlength(ch, font=f) + sp for ch in t) - sp
    if center: x = x - tw / 2
    for ch in t: d.text((x, y), ch, font=f, fill=fill); x += d.textlength(ch, font=f) + sp
def sq(im, n):
    im = im.convert('RGB'); s = min(im.size)
    return im.crop(((im.width - s) // 2, (im.height - s) // 2, (im.width + s) // 2, (im.height + s) // 2)).resize((n, n), Image.LANCZOS)
def rmask(n, r):
    m = Image.new('L', (n, n), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, n - 1, n - 1), radius=r, fill=255); return m

def rack_strip(S, name, w, h):
    """Real rack photo (rack_imgs) or a Bird & Bamboo painted bar, returned RGBA w x h."""
    p = (S.get('rack_imgs') or {}).get(name)
    if p:
        im = Image.open(R + p).convert('RGBA'); bb = im.getbbox(); im = im.crop(bb)
        return im.resize((w, max(8, int(im.height * w / im.width))), Image.LANCZOS)
    col = BB_RGB.get(name.replace('Bird & Bamboo ', ''), (200, 200, 200))
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=5, fill=col)
    dk = tuple(max(0, int(v * .82)) for v in col); lt = tuple(min(255, int(v * 1.12)) for v in col)
    d.line((2, 3, w - 3, 3), fill=lt, width=3); d.line((2, h - 4, w - 3, h - 4), fill=dk, width=4); d.line((2, h // 2, w - 3, h // 2), fill=dk, width=2)
    return im

def rack_label(name):
    for b in ('Peace Love Mahjong', 'Bird & Bamboo', 'Middle & Main', 'Miss Mahjong', 'Oh My Mahjong'):
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
        st = rack_strip(S, n, w, int(rowh * .42)); c.paste(st, (x0, y + int(fs * 1.9)), st); d = ImageDraw.Draw(c)
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
    spaced(d, 70, 66, 'THE TILE EDIT', P('Poppins-Bold.ttf', 30), NAVY, 7)
    ts = title(d, S, 60, 104, 690, 128)
    dy = 0 if ts >= 120 else int((120 - ts) * 1.1)  # long names set smaller: pull the brand lines up to close the gap
    d.text((66, 300 - dy), 'by ' + S['brand'], font=lora(44), fill=NAVY)
    d.text((66, 365 - dy), S['sub'], font=lora(29), fill=GREY)
    spaced(d, 70, 445, 'THE BACKS', P('Poppins-Bold.ttf', 26), NAVY, 6)
    for i, (n, h, role) in enumerate(S['backs']):
        x = 70 + i * 190; d.rounded_rectangle((x, 482, x + 170, 652), radius=16, fill=hx(h))
        d.text((x + 85, 675), n, font=P('Poppins-Medium.ttf', 21), fill=NAVY, anchor='mm'); d.text((x + 85, 704), role, font=P('Poppins-Regular.ttf', 18), fill=(90, 90, 100), anchor='mm')
    spaced(d, 70, 757, 'THE FACES', P('Poppins-Bold.ttf', 26), NAVY, 6)
    F = S['faces']; per = 3 if len(F) > 4 else 2 if len(F) == 4 else 3
    for i, (n, h) in enumerate(F):
        cx = 125 + (i % per) * 190; cy = 838 + (i // per) * 150
        d.ellipse((cx - 46, cy - 46, cx + 46, cy + 46), fill=(255, 255, 255)); d.ellipse((cx - 42, cy - 42, cx + 42, cy + 42), fill=hx(h))
        d.text((cx, cy + 63), n, font=P('Poppins-Medium.ttf', 20), fill=NAVY, anchor='mm')
    pile_circle(c, S, 1030, 470, 300); d = ImageDraw.Draw(c)
    d.line((900, 800, 1160, 800), fill=(225, 205, 185), width=3)
    l1, l2 = line2(S)
    d.text((1030, 828), l1, font=lora(31, 500), fill=NAVY, anchor='mm'); d.text((1030, 873), l2, font=lora(31, 500), fill=NAVY, anchor='mm')
    BD = Image.open(RES + 'mm_badge.png').convert('RGBA'); c.paste(BD, (840, 970), BD); d = ImageDraw.Draw(c)
    d.rounded_rectangle((1382, 42, 1954, 1084), radius=36, fill=PANEL, outline=EDGE, width=3)
    spaced(d, 1668, 66, 'RACK MATCHES', P('Poppins-Bold.ttf', 30), NAVY, 8, True)
    rack_panel(c, S, 1418, 1918, 150, rowh=178, fs=20); d = ImageDraw.Draw(c)
    spaced(d, 1668, 690, 'TOP MAT MATCHES', P('Poppins-Bold.ttf', 28), NAVY, 7, True)
    mats_row(c, S, 1412, 742, 150, 20, 21); d = ImageDraw.Draw(c)
    d.rounded_rectangle((1420, 958, 1916, 1020), radius=31, fill=NAVY)
    d.text((1668, 989), S.get('shop', 'Shop OMM · code MAHJMATCH'), font=P('Poppins-Bold.ttf', 26), fill=(255, 255, 255), anchor='mm')
    c.save(out, quality=92)

def mobile(S, out):
    """Phone color guide, drawn at 2x (2000x3000), layout of the approved Coquette phone card."""
    K = 1.5; W, H = 2000, 3000; c = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(c)
    spaced(d, W / 2, 105, 'THE TILE EDIT', P('Poppins-Bold.ttf', 30 * K), NAVY, 9 * K, True)
    title(d, S, W / 2, 175, 1640, 250, center=True)
    d.text((W / 2, 510), 'by ' + S['brand'], font=lora(44 * K), fill=NAVY, anchor='mm')
    d.text((W / 2, 600), S['sub'], font=lora(29 * K), fill=GREY, anchor='mm')
    pile_circle(c, S, W // 2, 1140, 420); d = ImageDraw.Draw(c)
    l1, l2 = line2(S)
    d.line((W / 2 - 200, 1640, W / 2 + 200, 1640), fill=(225, 205, 185), width=4)
    d.text((W / 2, 1695), l1, font=lora(34 * K, 500), fill=NAVY, anchor='mm'); d.text((W / 2, 1772), l2, font=lora(34 * K, 500), fill=NAVY, anchor='mm')
    # backs + faces panel
    d.rounded_rectangle((80, 1830, 1920, 2300), radius=48, fill=PANEL)
    spaced(d, 500, 1868, 'THE BACKS', P('Poppins-Bold.ttf', 27 * K), NAVY, 7 * K, True)
    for i, (n, h, role) in enumerate(S['backs']):
        x = 140 + i * 256; d.rounded_rectangle((x, 1940, x + 222, 2162), radius=22, fill=hx(h))
        d.text((x + 111, 2196), n, font=P('Poppins-Medium.ttf', 22 * K), fill=NAVY, anchor='mm'); d.text((x + 111, 2244), role, font=P('Poppins-Regular.ttf', 20 * K), fill=(90, 90, 100), anchor='mm')
    spaced(d, 1490, 1868, 'THE FACES', P('Poppins-Bold.ttf', 27 * K), NAVY, 7 * K, True)
    F = S['faces']; per = 3 if len(F) > 4 else 2
    for i, (n, h) in enumerate(F):
        cx = (1250 + (i % per) * 240) if per == 3 else (1370 + (i % per) * 240); cy = 2000 + (i // per) * 182
        d.ellipse((cx - 56, cy - 56, cx + 56, cy + 56), fill=(255, 255, 255)); d.ellipse((cx - 52, cy - 52, cx + 52, cy + 52), fill=hx(h))
        d.text((cx, cy + 84), n, font=P('Poppins-Medium.ttf', 20 * K), fill=NAVY, anchor='mm')
    # racks + mats panel
    d.rounded_rectangle((80, 2340, 1920, 2960), radius=48, fill=PANEL)
    spaced(d, 540, 2380, 'RACK MATCHES', P('Poppins-Bold.ttf', 27 * K), NAVY, 7 * K, True)
    rack_panel(c, S, 132, 900, 2452, rowh=158, fs=28); d = ImageDraw.Draw(c)
    spaced(d, 1450, 2380, 'TOP MAT MATCHES', P('Poppins-Bold.ttf', 27 * K), NAVY, 7 * K, True)
    mats_row(c, S, 1035, 2470, 250, 42, 30); d = ImageDraw.Draw(c)
    d.rounded_rectangle((1040, 2812, 1860, 2896), radius=42, fill=NAVY)
    d.text((1450, 2854), S.get('shop_m', S.get('shop', 'Code MAHJMATCH')), font=P('Poppins-Bold.ttf', 34), fill=(255, 255, 255), anchor='mm')
    c.save(out, quality=92)

if __name__ == '__main__':
    key = sys.argv[1]; S = json.load(open(R + 'config/colorcards.json'))['sets'][key]
    out = sys.argv[2] if len(sys.argv) > 2 else R + f'assets/colorcards/{key}/'
    os.makedirs(out, exist_ok=True)
    desktop(S, out + f'00-{key}-mahjong-tiles-tile-edit-moodboard.jpg'); mobile(S, out + f'00-{key}-mahjong-tiles-color-guide-mobile.jpg')
    print('ok', key, out)
