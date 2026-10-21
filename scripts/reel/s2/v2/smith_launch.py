"""Ep 8 Smith for launch day (Tiffany, Oct 21 12:51): MINIMAL changes to assets/reels/s2/ep08-smith-s2.mp4, nothing else.
1. 11.5-12.5 s (frames 345-374): the red NOPE stamp on Hampton -> the hotline v12 X stamp (white disc, navy ring, navy X,
   tilted 10 deg, top-right corner of the mat), scaling in 1.6 -> 1 like the original stamp.
   The NOPE pixels are replaced with the clean card from frame 344 (static there; 373-374 shifted to the measured drift).
2. From 30.5 s (frame 915, the cut to the old "Let the MAT-ching begin / COMING 10.27 Find Your Match" card) to the end:
   the hotline v12 end card (kit.end_html: Hooking up tiles, / mats & racks . Find *Your* Mat-ch(TM) . 10.27 .
   mahjmatchmaker.com . Code MAHJMATCH at Oh My Mahjong . LINK IN BIO; deco Smith + heart + Duck Camp), same 7.0 s.
   All end-card text is checked inside x 90-860 and above y 1180.
3. Defect fix found in the full-fps review (not a design change): at 3.0 s the original cuts from the opener's fade to white
   to ONE BLACK FRAME (90), then fades up from black through a ghost of the old Season 1 "THE MAHJ MATCHMAKER" card
   (91-97). Frames 90-99 are replaced by a straight blend from frame 89 (the opener's white) into frame 100 (clean title).
Every other frame is the original (one re-encode). Silent: her song starts at 0:00 in Edits.
Usage: python3 scripts/reel/s2/v2/smith_launch.py  -> assets/reels/s2/ep08-smith-s2-v2.mp4"""
import os, sys, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit
from kit import R, WORK

IN = f'{R}/assets/reels/s2/ep08-smith-s2.mp4'
OUT = f'{R}/assets/reels/s2/ep08-smith-s2-v2.mp4'
CLEAN, FIRST, LAST, END0 = 344, 345, 374, 915
SWIPE = (375, 386)                   # the X rides on the card while it swipes off (v12: the stamp stays on the card)
BOX = (500, 700, 965, 1065)          # around the NOPE stamp (bbox 570-919 x 782-981)
CX, CY, D = 799, 896, 176            # v12 placement: top-right of the mat (mat ~x 134-950, y 745-1500), inset like v12
NAVY = (6, 42, 85)


def shift_of(ref, fr):
    best = (1e18, 0, 0); a = ref[760:1000, 150:480]
    for dy in range(-10, 11):
        for dx in range(-14, 15):
            s = np.abs(a - fr[760 + dy:1000 + dy, 150 + dx:480 + dx]).mean()
            if s < best[0]: best = (s, dx, dy)
    return best[1], best[2]


def xstamp(scale, alpha):
    """v12 X stamp (scripts/social/titlecards/build.py swipe_card 'nope' branch), drawn 4x and downsampled."""
    k = 4; size = int(D * 1.8 * k); im = Image.new('RGBA', (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    c = size / 2; r = D / 2 * scale * k; bw = 8 * D / 190 * scale * k
    d.ellipse((c - r, c - r, c + r, c + r), fill=(255, 255, 255, int(230 * alpha)), outline=NAVY + (int(255 * alpha),), width=int(bw))
    m = r * (96 / 190) * (22 / 48); w = int(7 / 48 * (96 / 190) * 2 * r)   # the v12 96px X glyph inside the 190px disc
    for (x0, y0, x1, y1) in ((c - m, c - m, c + m, c + m), (c + m, c - m, c - m, c + m)):
        d.line((x0, y0, x1, y1), fill=NAVY + (int(255 * alpha),), width=w)
        for (x, y) in ((x0, y0), (x1, y1)):
            d.ellipse((x - w / 2, y - w / 2, x + w / 2, y + w / 2), fill=NAVY + (int(255 * alpha),))
    im = im.rotate(-10, resample=Image.BICUBIC)          # v12: rotate(10deg) in CSS = clockwise
    return im.resize((size // k, size // k), Image.LANCZOS)


def patch_stamp(src, out):
    fd = f'{WORK}/smith-stamp'; os.makedirs(fd, exist_ok=True)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', src, '-vf', f"select='between(n,{CLEAN},{LAST})'", '-vsync', '0',
                    '-start_number', str(CLEAN), f'{fd}/%05d.png'], check=True)
    L = lambda n: np.asarray(Image.open(f'{fd}/{n:05d}.png').convert('RGB'), dtype=np.int16)
    ref = L(CLEAN); ease = lambda x: 0 if x < 0 else 1 if x > 1 else 1 - (1 - x) ** 3
    x0, y0, x1, y1 = BOX
    for n in range(FIRST, LAST + 1):
        fr = L(n); dx, dy = (0, 0) if n <= 372 else shift_of(ref, fr)
        cl = np.roll(np.roll(ref, dy, 0), dx, 1)
        diff = np.abs(fr - cl).sum(2); m = np.zeros(diff.shape, bool); m[y0:y1, x0:x1] = diff[y0:y1, x0:x1] > 45
        m = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(13))) > 0
        fr[m] = cl[m]
        im = Image.fromarray(fr.astype(np.uint8)).convert('RGBA')
        p = ease((n - FIRST + .5) / 7.5); st = xstamp(1.6 - .6 * p, min(1, p * 1.4))
        im.alpha_composite(st, (CX + dx - st.width // 2, CY + dy - st.height // 2))
        im.convert('RGB').save(f'{fd}/{n:05d}.png')
    # swipe-off frames: follow the card (template match on the clean card art around the stamp, translation + tilt)
    import cv2
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', src, '-vf', f"select='between(n,{SWIPE[0]},{SWIPE[1] - 1})'", '-vsync', '0',
                    '-start_number', str(SWIPE[0]), f'{fd}/%05d.png'], check=True)
    tx0, ty0, tx1, ty1 = 600, 760, 940, 1040
    tpl = ref[ty0:ty1, tx0:tx1].astype(np.uint8)
    last = SWIPE[0]; track = []
    for n in range(SWIPE[0], SWIPE[1]):
        fr = np.asarray(Image.open(f'{fd}/{n:05d}.png').convert('RGB'))
        best = (-1, 0, 0, 0)
        for ang in range(0, -16, -1):
            M = cv2.getRotationMatrix2D(((tx1 - tx0) / 2, (ty1 - ty0) / 2), -ang, 1.0)
            t = cv2.warpAffine(tpl, M, (tx1 - tx0, ty1 - ty0), borderMode=cv2.BORDER_REFLECT)[30:-30, 30:-30]
            r = cv2.matchTemplate(fr, t, cv2.TM_CCOEFF_NORMED); _, mv, _, ml = cv2.minMaxLoc(r)
            if mv > best[0]: best = (mv, ml[0] - 30 - tx0, ml[1] - 30 - ty0, ang)
        sc, dx, dy, ang = best
        if sc < .55 and len(track) >= 3:                       # card art leaving the frame: extrapolate its motion
            (x1, y1, a1), (x2, y2, a2), (x3, y3, a3) = track[-3:]
            dx, dy, ang = 2 * x3 - x2 + (x3 - 2 * x2 + x1), 2 * y3 - y2 + (y3 - 2 * y2 + y1), 2 * a3 - a2
            if CX + dx + D < 0: break
        elif sc < .55: break
        track.append((dx, dy, ang))
        print('swipe', n, round(sc, 2), dx, dy, ang)
        im = Image.fromarray(fr).convert('RGBA'); st = xstamp(1, 1).rotate(-ang, resample=Image.BICUBIC, expand=True)
        cx = (tx0 + tx1) / 2 + dx; cy = (ty0 + ty1) / 2 + dy; a = np.deg2rad(ang)     # rotate the stamp centre about the patch centre
        ox, oy = CX - (tx0 + tx1) / 2, CY - (ty0 + ty1) / 2
        px = cx + ox * np.cos(a) + oy * np.sin(a); py = cy - ox * np.sin(a) + oy * np.cos(a)
        im.alpha_composite(st, (int(round(px - st.width / 2)), int(round(py - st.height / 2))))
        im.convert('RGB').save(f'{fd}/{n:05d}.png'); last = n + 1
    for n in range(last, SWIPE[1] + 2):                     # unused extracted frames must not join the image sequence
        if os.path.exists(f'{fd}/{n:05d}.png'): os.remove(f'{fd}/{n:05d}.png')
    fc = (f"[0:v]split[s0][s1];[s0]trim=start_frame=0:end_frame={FIRST},setpts=PTS-STARTPTS[a];"
          f"[1:v]fps=30,setpts=N/30/TB,format=yuv420p[b];[s1]trim=start_frame={last}:end_frame={END0},setpts=PTS-STARTPTS[c];[a][b][c]concat=n=3:v=1:a=0[v]")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-framerate', '30', '-start_number', str(FIRST), '-i', f'{fd}/%05d.png',
                    '-filter_complex', fc, '-map', '[v]', '-c:v', 'libx264', '-preset', 'slow', '-crf', '14', '-pix_fmt', 'yuv420p', '-r', '30', out], check=True)
    return out


def patch_fade(src, out, a=89, b=100):
    fd = f'{WORK}/smith-fade'; os.makedirs(fd, exist_ok=True)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', src, '-vf', f"select='eq(n,{a})+eq(n,{b})'", '-vsync', '0', f'{fd}/k%d.png'], check=True)
    A = np.asarray(Image.open(f'{fd}/k1.png').convert('RGB'), float); B = np.asarray(Image.open(f'{fd}/k2.png').convert('RGB'), float)
    for n in range(a + 1, b):
        t = (n - a) / (b - a); t = t * t * (3 - 2 * t)
        Image.fromarray((A * (1 - t) + B * t).round().astype(np.uint8)).save(f'{fd}/{n:05d}.png')
    fc = (f"[0:v]split[s0][s1];[s0]trim=start_frame=0:end_frame={a + 1},setpts=PTS-STARTPTS[x];"
          f"[1:v]fps=30,setpts=N/30/TB,format=yuv420p[y];[s1]trim=start_frame={b},setpts=PTS-STARTPTS[z];[x][y][z]concat=n=3:v=1:a=0[v]")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-framerate', '30', '-start_number', str(a + 1), '-i', f'{fd}/%05d.png',
                    '-filter_complex', fc, '-map', '[v]', '-c:v', 'libx264', '-preset', 'slow', '-crf', '14', '-pix_fmt', 'yuv420p', '-r', '30', out], check=True)
    return out


if __name__ == '__main__':
    n_total = int(subprocess.check_output(['ffprobe', '-v', 'error', '-count_frames', '-show_entries', 'stream=nb_read_frames', '-of', 'csv=p=0', IN]).strip())
    body = patch_fade(patch_stamp(IN, f'{WORK}/smith-body-stamp.mp4'), f'{WORK}/smith-body-0-{END0}.mp4')
    eh = kit.end_html('assets/tiles/album/smith.jpg', 'assets/mats/gallery/mahjong-moxie--duck-camp.webp',
                      'Code <span style="color:#d6336c">MAHJMATCH</span> at Oh My Mahjong')
    kit.check_end(eh)
    end = kit.shoot_css(eh, 'smith-launch-end', (n_total - END0) / 30, t0=300)
    kit.concat([body, end], OUT); print(OUT)
