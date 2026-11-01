"""Real Find Your Mat-ch screens (captured by cap_fym.py) shown ON A PHONE, zoomed in, with a moving camera between
actions and a FIXED camera during every swipe (FYM-REEL-RULES 20: the phone never moves on a swipe; only the card flies).
Screens are 1170x2532 (390x844 css @3x). Camera = (sx, sy, k): screenshot point (sx,sy) lands at canvas centre, scale k."""
import json, math
from PIL import Image, ImageDraw, ImageFilter
from common import *

SW, SH = 1170, 2532
BEZ = 46  # bezel in screenshot px
SLATE = (111, 98, 128)

class App:
    def __init__(self, capdir):
        self.d = capdir; self.meta = json.load(open(f'{capdir}/meta.json')); self._c = {}
        m = Image.new('L', (SW, SH), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, SW - 1, SH - 1), 120, fill=255); self.mask = m
    def img(self, n):
        if n not in self._c:
            im = Image.open(f'{self.d}/{n}.png').convert('RGB')
            if not n.endswith('-card'): im = im.resize((SW, SH)) if im.size != (SW, SH) else im
            self._c[n] = im
        return self._c[n]

    def phone(self, bg, scr, cam, overlay=None):
        """composite screenshot scr (PIL) on bg through camera cam=(sx,sy,k). overlay(c, to_canvas) draws on top."""
        sx, sy, k = cam; c = bg.copy()
        ox = W / 2 - sx * k; oy = H / 2 - sy * k   # canvas pos of screenshot (0,0)
        to = lambda x, y: (ox + x * k, oy + y * k)
        # bezel + shadow (visible only when zoomed out)
        x0, y0 = to(-BEZ, -BEZ); x1, y1 = to(SW + BEZ, SH + BEZ)
        if x0 > -400 or y0 > -400 or x1 < W + 400:
            sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
            sd.rounded_rectangle((x0 + 10, y0 + 30, x1 + 10, y1 + 30), int(150 * k), fill=(0, 0, 0, 120))
            sh = sh.filter(ImageFilter.GaussianBlur(30)); c.paste(sh, (0, 0), sh)
            d = ImageDraw.Draw(c); d.rounded_rectangle((x0, y0, x1, y1), int(160 * k), fill=(24, 22, 30), outline=(70, 66, 80), width=max(2, int(6 * k)))
        # visible crop of the screen
        cx0 = max(0, (0 - ox) / k); cy0 = max(0, (0 - oy) / k); cx1 = min(SW, (W - ox) / k); cy1 = min(SH, (H - oy) / k)
        if cx1 > cx0 and cy1 > cy0:
            box = (int(cx0), int(cy0), int(math.ceil(cx1)), int(math.ceil(cy1)))
            part = scr.crop(box); mk = self.mask.crop(box)
            tw = max(1, round((box[2] - box[0]) * k)); th = max(1, round((box[3] - box[1]) * k))
            part = part.resize((tw, th), Image.BILINEAR if k < 0.7 else Image.LANCZOS); mk = mk.resize((tw, th))
            c.paste(part, (round(ox + box[0] * k), round(oy + box[1] * k)), mk)
        if overlay: overlay(c, to, k)
        return c

    def swipe_frame(self, bg, i, tt, cam, kind, step='m', dur=0.62):
        """swipe i of deck step ('s' mats / 'r' racks). tt = seconds into the swipe. Before: card sits (0..0.18),
        stamp lands (0.18), card flies (0.26..dur). Underneath: the real AFTER screen."""
        pre = 's' if step == 'm' else 'r'
        before = self.img(f'{pre}{i}-b'); after = self.img(f'{pre}{i}-a'); card = self.img(f'{pre}{i}-card')
        bx, by, bw, bh = [v * 3 for v in self.meta[f'{pre}{i}']]
        go = 0.26
        if tt < go:
            scr = before
        else:
            scr = after
        def ov(c, to, k):
            d = ImageDraw.Draw(c)
            # button pulse
            if tt < go + 0.1:
                p = math.sin(clamp(tt / (go + 0.1)) * math.pi)
                bxc = bx + (bw * 0.89 if kind == 'yes' else bw * 0.11); byc = by + bh * (0.52 if step == 'm' else 0.55)
                X, Y = to(bxc, byc); r = (70 + 40 * p) * k
                d.ellipse((X - r, Y - r, X + r, Y + r), outline=PINK if kind == 'yes' else SLATE, width=int(10 * k) + 2)
            if tt >= go:
                u = clamp((tt - go) / (dur - go)); e = u * u
                dx = (1 if kind == 'yes' else -1) * (lerp(0, 1500, e)); rot = (1 if kind == 'yes' else -1) * lerp(0, 26, e)
                cw = max(4, int(card.width * k)); ch = max(4, int(card.height * k))
                ci = card.resize((cw, ch), Image.BILINEAR).convert('RGBA')
                stamp_on(ci, kind, 1.0)
                ci = ci.rotate(-rot, resample=Image.BICUBIC, expand=True)
                X, Y = to(bx + bw / 2, by + bh / 2)
                c.paste(ci, (int(X - ci.width / 2 + dx), int(Y - ci.height / 2 + abs(dx) * 0.08)), ci)
            elif tt >= 0.16:
                # stamp lands on the card in place
                cw = int(bw * k); ch = int(bh * k); X, Y = to(bx, by)
                lay = Image.new('RGBA', (cw, ch), (0, 0, 0, 0)); stamp_on(lay, kind, back_out(clamp((tt - 0.16) / 0.1)))
                c.paste(lay, (int(X), int(Y)), lay)
        return self.phone(bg, scr, cam, ov)

def stamp_on(lay, kind, s):
    """dating-app stamp in the card's top corner (♥ right swipe = stamp top-left; ✕ = top-right)."""
    if s <= 0.05: return
    d = ImageDraw.Draw(lay); w = lay.width
    sz = int(w * 0.24 * (1.6 - 0.6 * s)); col = PINK if kind == 'yes' else SLATE
    x = int(w * 0.07) if kind == 'yes' else int(w * 0.93) - sz; y = int(w * 0.08)
    st = Image.new('RGBA', (sz, int(sz * 0.8)), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
    sd.rounded_rectangle((0, 0, sz - 1, int(sz * 0.8) - 1), int(sz * 0.18), fill=(255, 255, 255, 225), outline=col, width=max(3, sz // 14))
    cx, cy, r = sz / 2, sz * 0.4, sz * 0.24
    if kind == 'yes': heart_shape(sd, cx, cy, r, col)
    else:
        lw = max(4, sz // 9); sd.line((cx - r, cy - r, cx + r, cy + r), fill=col, width=lw); sd.line((cx - r, cy + r, cx + r, cy - r), fill=col, width=lw)
    st = st.rotate(-14 if kind == 'yes' else 14, resample=Image.BICUBIC, expand=True)
    lay.paste(st, (x, y), st)

def heart_shape(d, cx, cy, r, col):
    d.ellipse((cx - r, cy - r * 0.9, cx, cy + r * 0.1), fill=col); d.ellipse((cx, cy - r * 0.9, cx + r, cy + r * 0.1), fill=col)
    d.polygon([(cx - r * 0.98, cy - r * 0.25), (cx + r * 0.98, cy - r * 0.25), (cx, cy + r * 1.05)], fill=col)

def glyph_ok():
    f = font(FONT_CAP, 80); return f.getbbox('♥')[2] > 10 and f.getbbox('✕')[2] > 10

def caption(c, txt, y=258, bg=(255, 255, 255), fg=NAVY, size=40):
    d = ImageDraw.Draw(c); pill(d, W // 2, y, txt, font(FONT_POP_B, size), fg, bg, padx=40, pady=20)

def tap_ring(c, X, Y, p, col=PINK):
    d = ImageDraw.Draw(c); r = 40 + 60 * p; a = 1 - p
    if a <= 0: return
    d.ellipse((X - r, Y - r, X + r, Y + r), outline=col, width=int(4 + 8 * a))
    d.ellipse((X - 26, Y - 26, X + 26, Y + 26), fill=(255, 255, 255), outline=col, width=6)


MCAM = (585, 1138, 0.85)
RCAM = (585, 1150, 0.92)
def sticker(c, bb, cam, txt, kind, fy=0.10):
    sx, sy, k = cam; bx, by, bw, bh = [v * 3 for v in bb]
    Y = H / 2 + (by + bh * fy - sy) * k
    d = ImageDraw.Draw(c); pill(d, W // 2, int(Y), txt, font(FONT_POP_B, 34), (255, 255, 255), NAVY if kind == 'yes' else SLATE, padx=30, pady=14)

def smooth_cam(a, b, u):
    u = ease_in_out(u); return tuple(lerp(x, y, u) for x, y in zip(a, b))

class Flow:
    """Two app moments, timed in beats. flow1: phone in -> tap the tile set -> swipe mats (fixed camera).
    flow2: suitors -> racks step + + zoom -> swipe racks -> the match card (output) -> shop list."""
    def __init__(self, A, B, bg, labels, sc=1.0):
        self.A, self.B, self.bg, self.L, self.sc = A, B, bg, labels, sc
        self.kinds = [k for _, _, k in A.meta['swipes']]
    # ---- flow 1 ----
    def len1(self, nsw): return (2 + 1.25 * nsw) * self.sc
    def len2(self): return self.LEN2 * self.sc
    def f1(self, tb, nsw):
        A, B = self.A, self.B * self.sc; tb = tb / self.sc
        tx, ty = A.meta['tilebtn']; tx *= 3; ty *= 3
        if tb < 2:
            u = tb / 1.2
            cam = smooth_cam((SW / 2, SH / 2, 0.52), (tx, ty, 1.15), u)
            c = A.phone(self.bg, A.img('01-tiles'), cam)
            if tb > 1.15:
                X = W / 2 + (tx - cam[0]) * cam[2]; Y = H / 2 + (ty - cam[1]) * cam[2]
                tap_ring(c, X, Y, clamp((tb - 1.15) * B / 0.4))
            caption(c, self.L['tiles'])
            return c
        tb -= 2; i = min(nsw - 1, int(tb // 1.25)); tt = (tb - i * 1.25) * B
        cam = MCAM
        c = A.swipe_frame(self.bg, i, tt, cam, self.kinds[i], 'm', dur=min(0.62, 1.2 * B))
        caption(c, self.L['mats'])
        nm, bn = A.meta['swipes'][i][1]
        if tt < 0.26: sticker(c, A.meta[f's{i}'], cam, f'{nm} · {bn}', self.kinds[i])
        return c
    # ---- flow 2 ----
    LEN2 = 9.5
    def f2(self, tb):
        A, B = self.A, self.B * self.sc; tb = tb / self.sc
        if tb < 1.5:   # suitors row (lower part of the screen)
            cam = smooth_cam((585, 1950, 0.9), (585, 2230, 1.22), tb / 1.5)
            c = A.phone(self.bg, A.img('30-suitors'), cam); caption(c, self.L['suitors']); return c
        tb -= 1.5
        if tb < 2.0:   # racks step: + + zoom on the mat
            j = min(2, int(tb / 0.67)); u = (tb - j * 0.67) / 0.67
            cam = (RCAM[0], RCAM[1], RCAM[2] + 0.08 * (j + u) / 3)
            c = A.phone(self.bg, A.img(f'40-rz{j}'), cam)
            rz = A.meta.get('rz')
            if rz and j < 2 and u > 0.55:
                X = W / 2 + (rz[0] * 3 - cam[0]) * cam[2]; Y = H / 2 + (rz[1] * 3 - cam[1]) * cam[2]
                tap_ring(c, X, Y, clamp((u - 0.55) / 0.45))
            caption(c, self.L['zoom']); return c
        tb -= 2.0
        if tb < 3.0:   # rack swipes ✕ ♥ ♥
            j = min(2, int(tb)); tt = (tb - j) * B
            c = A.swipe_frame(self.bg, j, tt, RCAM, ['no', 'yes', 'yes'][j], 'r', dur=min(0.6, 0.95 * B))
            caption(c, self.L['racks'])
            if tt < 0.26: sticker(c, A.meta[f'r{j}'], RCAM, self.L['rack_names'][j], ['no', 'yes', 'yes'][j], fy=0.42)
            return c
        tb -= 3.0
        if tb < 2.0:   # the output: her match card in the app
            cam = smooth_cam((585, 1380, 0.85), (585, 1500, 1.1), tb / 2.0)
            c = A.phone(self.bg, A.img('60-card'), cam); caption(c, self.L['card'], bg=PINK, fg=(255, 255, 255)); return c
        tb -= 2.0
        cam = smooth_cam((585, 1050, 1.0), (585, 1000, 1.12), tb / 1.0)
        c = A.phone(self.bg, A.img('61-card2'), cam); caption(c, self.L['shop'], bg=PINK, fg=(255, 255, 255)); return c
