"""Shared helpers for the brand-reshare holiday reels (Nov 1 2026, agent brand-reshare).
Frames are drawn with PIL at 1080x1920, 30 fps, into /dev/shm, then encoded with ffmpeg and deleted.
Photos: real brand product photos (fetched by fetch_photos.py) + FYM canonical tile photos. Nothing is pasted onto a mat:
tiles always sit in their own framed inset (match-card style: mat full, tiles inset)."""
import os, math, subprocess, shutil, wave, struct
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

REPO = '/home/claude/mahjmatchmaker-data'
PHOTOS = os.environ.get('BR_PHOTOS', '/tmp/claude-0/-home-claude/f4da3022-6ec8-595a-90aa-668aea191899/scratchpad/w/photos')
W, H, FPS = 1080, 1920, 30
FONT_CAP = f'{REPO}/assets/fonts/Caprasimo.ttf'
FONT_PLAY_I = f'{REPO}/assets/fonts/playfair-display-latin-700-italic.woff2'
FONT_CAVEAT = f'{REPO}/scripts/social/tileprofile/fonts/Caveat-Bold.ttf'
FONT_POP_B = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'
FONT_POP_M = '/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf'
NAVY = (6, 42, 85); PINK = (214, 51, 108); CREAM = (250, 243, 234); BLUSH = (247, 182, 200)
GOLD = (222, 180, 92); GOLD_D = (170, 128, 52); RED = (179, 32, 42); PINE = (31, 90, 58)

_fc = {}
def font(path, size):
    k = (path, size)
    if k not in _fc: _fc[k] = ImageFont.truetype(path, size)
    return _fc[k]

def photo(name, size=None):
    im = Image.open(os.path.join(PHOTOS, name)).convert('RGB')
    if size: im = cover(im, size)
    return im

def cover(im, size, cx=0.5, cy=0.5):
    tw, th = size; s = max(tw / im.width, th / im.height)
    r = im.resize((max(tw, round(im.width * s)), max(th, round(im.height * s))), Image.LANCZOS)
    x = int((r.width - tw) * cx); y = int((r.height - th) * cy)
    return r.crop((x, y, x + tw, y + th))

def trim_white(im, thr=242, pad=0):
    a = np.asarray(im.convert('L')); m = a < thr
    ys, xs = np.where(m)
    if len(xs) == 0: return im
    return im.crop((max(0, xs.min() - pad), max(0, ys.min() - pad), min(im.width, xs.max() + pad + 1), min(im.height, ys.max() + pad + 1)))

# easing
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease_out(t): t = clamp(t); return 1 - (1 - t) ** 3
def ease_in_out(t): t = clamp(t); return 3 * t * t - 2 * t * t * t
def back_out(t, s=1.7): t = clamp(t) - 1; return t * t * ((s + 1) * t + s) + 1
def lerp(a, b, t): return a + (b - a) * t

def text_w(txt, f):
    b = f.getbbox(txt); return b[2] - b[0]

def draw_center(d, y, txt, f, fill, cx=W // 2, stroke=0, stroke_fill=None, shadow=None):
    b = d.textbbox((0, 0), txt, font=f); w = b[2] - b[0]
    x = cx - w // 2 - b[0]
    if shadow: d.text((x + shadow[0], y + shadow[1]), txt, font=f, fill=shadow[2])
    d.text((x, y), txt, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
    return b[3] - b[1]

def draw_runs_center(d, y, runs, fill, cx=W // 2, shadow=None):
    """runs = [(text, font), ...] laid out on one baseline, centred by ink (FYM 'Your' in Playfair italic)."""
    widths = [];
    for t, f in runs: widths.append(d.textlength(t, font=f))
    total = sum(widths); x = cx - total / 2
    asc = max(f.getmetrics()[0] for _, f in runs)
    for (t, f), w in zip(runs, widths):
        yy = y + asc - f.getmetrics()[0]
        if shadow: d.text((x + shadow[0], yy + shadow[1]), t, font=f, fill=shadow[2])
        d.text((x, yy), t, font=f, fill=fill); x += w

def pill(d, cx, y, txt, f, fill, bg, padx=34, pady=16, outline=None):
    b = d.textbbox((0, 0), txt, font=f); w = b[2] - b[0]; h = b[3] - b[1]
    x0 = cx - w // 2 - padx; y0 = y; x1 = cx + (w - w // 2) + padx; y1 = y + h + 2 * pady
    d.rounded_rectangle((x0, y0, x1, y1), radius=(y1 - y0) // 2, fill=bg, outline=outline, width=3 if outline else 0)
    d.text((cx, (y0 + y1) / 2), txt, font=f, fill=fill, anchor='mm')
    return y1 - y0

def shadow_paste(canvas, im, xy, radius=28, offset=(0, 18), alpha=110, blur=26, rot=0):
    """paste im with a soft drop shadow (and optional rotation) onto RGB canvas."""
    if rot:
        w0, h0 = im.size
        im = im.convert('RGBA').rotate(rot, resample=Image.BICUBIC, expand=True)
        xy = (xy[0] - (im.width - w0) / 2, xy[1] - (im.height - h0) / 2)
    else:
        im = im.convert('RGBA')
    sh = Image.new('RGBA', (im.width + blur * 4, im.height + blur * 4), (0, 0, 0, 0))
    a = im.split()[3].point(lambda v: v * alpha // 255)
    blk = Image.new('RGBA', im.size, (0, 0, 0, 255)); blk.putalpha(a)
    sh.paste(blk, (blur * 2, blur * 2), blk); sh = sh.filter(ImageFilter.GaussianBlur(blur))
    x, y = int(xy[0]), int(xy[1])
    canvas.paste(sh, (x - blur * 2 + offset[0], y - blur * 2 + offset[1]), sh)
    canvas.paste(im, (x, y), im)

def rounded(im, r):
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), r, fill=255)
    o = im.convert('RGBA'); o.putalpha(m); return o

def polaroid(im, inner, border=18, bottom=18, r=10, label=None, lf=None, lcol=NAVY):
    """white-framed photo (tile inset)."""
    ph = cover(im, inner)
    bh = bottom if not label else bottom + 54
    card = Image.new('RGB', (inner[0] + 2 * border, inner[1] + border + bh), 'white')
    card.paste(ph, (border, border))
    if label:
        d = ImageDraw.Draw(card); draw_center(d, inner[1] + border + 8, label, lf, lcol, cx=card.width // 2)
    return rounded(card, r)

def sparkles(d, t, n=40, seed=3, box=(0, 0, W, H), col=(255, 240, 200), maxr=7):
    if os.environ.get('NO_FX'): return
    rng = np.random.default_rng(seed)
    xs = rng.uniform(box[0], box[2], n); ys = rng.uniform(box[1], box[3], n)
    ph = rng.uniform(0, 6.28, n); sp = rng.uniform(2.0, 5.0, n); rr = rng.uniform(2, maxr, n)
    for i in range(n):
        a = 0.5 + 0.5 * math.sin(t * sp[i] + ph[i])
        if a < 0.35: continue
        r = rr[i] * a; x, y = xs[i], ys[i]
        c = tuple(int(v) for v in col)
        d.line((x - r * 2.2, y, x + r * 2.2, y), fill=c, width=2); d.line((x, y - r * 2.2, x, y + r * 2.2), fill=c, width=2)
        d.ellipse((x - r * 0.6, y - r * 0.6, x + r * 0.6, y + r * 0.6), fill=c)

def snow(d, t, n=70, seed=7, col=(255, 255, 255)):
    if os.environ.get('NO_FX'): return
    rng = np.random.default_rng(seed)
    x0 = rng.uniform(0, W, n); sp = rng.uniform(60, 160, n); r = rng.uniform(2, 6, n); ph = rng.uniform(0, H, n); sw = rng.uniform(10, 40, n)
    for i in range(n):
        y = (ph[i] + t * sp[i]) % (H + 40) - 20; x = x0[i] + sw[i] * math.sin(t * 1.3 + i)
        d.ellipse((x - r[i], y - r[i], x + r[i], y + r[i]), fill=col)

def vgrad(size, top, bot):
    w, h = size; a = np.linspace(0, 1, h)[:, None, None]
    arr = (np.array(top)[None, None, :] * (1 - a) + np.array(bot)[None, None, :] * a).astype(np.uint8)
    return Image.fromarray(np.repeat(arr, w, axis=1), 'RGB')

def radial(size, inner, outer, cx=0.5, cy=0.45, rad=0.85):
    w, h = size; yy, xx = np.mgrid[0:h, 0:w]
    dd = np.sqrt(((xx / w - cx) * (w / h)) ** 2 + (yy / h - cy) ** 2) / rad
    a = np.clip(dd, 0, 1)[..., None]
    arr = (np.array(inner) * (1 - a) + np.array(outer) * a).astype(np.uint8)
    return Image.fromarray(arr, 'RGB')

def plaid(size, base, stripes, scale=1.0):
    """simple tartan: base colour + list of (offset, width, colour, alpha) repeated every period on both axes."""
    w, h = size; period = int(180 * scale)
    arr = np.zeros((h, w, 3), float); arr[:] = base
    for axis in (0, 1):
        n = h if axis == 0 else w; idx = np.arange(n) % period
        for off, wid, col, al in stripes:
            m = ((idx >= off * scale) & (idx < (off + wid) * scale)).astype(float) * al
            if axis == 0: arr = arr * (1 - m[:, None, None]) + np.array(col) * m[:, None, None]
            else: arr = arr * (1 - m[None, :, None]) + np.array(col) * m[None, :, None]
    return Image.fromarray(arr.clip(0, 255).astype(np.uint8), 'RGB')

class Renderer:
    def __init__(self, name, dur):
        self.name = name; self.dur = dur; self.n = int(round(dur * FPS))
        self.dir = f'/dev/shm/brand-reshare/{name}'; shutil.rmtree(self.dir, ignore_errors=True); os.makedirs(self.dir)
    def run(self, draw_fn, only=None):
        rng = range(self.n) if only is None else only
        for i in rng:
            im = draw_fn(i / FPS)
            im.save(f'{self.dir}/f{i:05d}.jpg', quality=93)
    def encode(self, out_mp4, click_wav=None, test_mp4=None):
        cmd = ['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', f'{self.dir}/f%05d.jpg',
               '-c:v', 'libx264', '-preset', 'slow', '-crf', '19', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out_mp4]
        subprocess.run(cmd, check=True)
        if click_wav and test_mp4:
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', out_mp4, '-i', click_wav, '-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k',
                            '-shortest', test_mp4], check=True)
    def frame(self, t):
        return Image.open(f'{self.dir}/f{int(round(t * FPS)):05d}.jpg')
    def cleanup(self):
        shutil.rmtree(self.dir, ignore_errors=True)

def click_track(path, dur, bpm, offset=0.0, accent_every=4, marks=()):
    """self-generated metronome (no copyrighted audio): beat clicks, accented bar downbeats, extra 'cut' blips at marks."""
    sr = 44100; n = int(dur * sr); a = np.zeros(n)
    beat = 60.0 / bpm; t = offset; k = 0
    def blip(t0, f, amp, ln=0.035):
        i0 = int(t0 * sr); m = int(ln * sr)
        if i0 >= n: return
        tt = np.arange(min(m, n - i0)) / sr
        a[i0:i0 + len(tt)] += amp * np.sin(2 * np.pi * f * tt) * np.exp(-tt * 90)
    while t < dur:
        blip(t, 1700 if k % accent_every == 0 else 1100, 0.7 if k % accent_every == 0 else 0.45); t += beat; k += 1
    for m in marks: blip(m, 600, 0.35, 0.06)
    a = np.clip(a, -1, 1); pcm = (a * 32000).astype(np.int16)
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr); wf.writeframes(pcm.tobytes())

def contact_sheet(mp4, out, every=0.5, cols=8, tw=216):
    tmp = f'/dev/shm/brand-reshare/cs_{os.getpid()}'; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    subprocess.run(['ffmpeg', '-v', 'error', '-i', mp4, '-vf', f'fps={1/every},scale={tw}:-1', f'{tmp}/c%04d.jpg'], check=True)
    fs = sorted(os.listdir(tmp)); th = int(tw * 16 / 9)
    rows = (len(fs) + cols - 1) // cols; S = Image.new('RGB', (cols * tw, rows * (th + 22)), 'white'); d = ImageDraw.Draw(S)
    f = font(FONT_POP_M, 15)
    for i, fn in enumerate(fs):
        im = Image.open(f'{tmp}/{fn}'); x = (i % cols) * tw; y = (i // cols) * (th + 22); S.paste(im, (x, y))
        d.text((x + 4, y + th + 2), f'{i*every:.1f}s', font=f, fill='black')
    S.save(out, quality=82); shutil.rmtree(tmp, ignore_errors=True)
