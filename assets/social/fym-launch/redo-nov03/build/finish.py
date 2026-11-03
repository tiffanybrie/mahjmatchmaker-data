"""Launch reel redo finish (Nov 3): ORIGINAL calm-cut frames 0-575 + 621-721 (0.00-19.17s, 20.70-24.03s) + new depth wall 576-620 + new frames 722-1739 (24.06-57.97s) -> 58.0s silent mp4,
beat-test mp4 (click every 0.5s = the original cut's 120 bpm grid, accent each bar; first ♥ 27.71s marked by a high click), cover, contact sheet
(every 0.5s), safe-zone sheet. Outputs to assets/social/fym-launch/redo-nov03/."""
import os, subprocess, wave, struct, math, shutil
os.environ.setdefault('MAGICK_TMPDIR', '/dev/shm/lr'); W = '/dev/shm/lr'; D = '/home/claude/mahjmatchmaker-data/assets/social/fym-launch/redo-nov03'
ORIG = '/home/claude/mahjmatchmaker-data/assets/social/fym-launch/sunday-flow/fym-launch-reel-v5-calm-58s.mp4'
DUR, BEAT, SR, N = 58.0, 0.5, 44100, 1740
def run(*a): subprocess.run(a, check=True, capture_output=True)
os.makedirs(f'{W}/orig', exist_ok=True)
if len(os.listdir(f'{W}/orig')) < 722: run('ffmpeg', '-y', '-i', ORIG, '-frames:v', '722', '-q:v', '2', '-start_number', '0', f'{W}/orig/%04d.jpg')
shutil.rmtree(f'{W}/all', ignore_errors=True); os.makedirs(f'{W}/all')
for i in range(N):
    src = f'{W}/frames/{i:04d}.jpg' if (i >= 722 or 576 <= i <= 620) else f'{W}/orig/{i:04d}.jpg'  # 576-620 = new depth wall
    assert os.path.exists(src), src; os.symlink(src, f'{W}/all/{i:04d}.jpg')
n = int(DUR * SR); buf = [0.0] * n
def click(t, f0, amp):
    s0 = int(t * SR)
    for i in range(int(0.035 * SR)):
        if s0 + i < n: buf[s0 + i] += amp * math.sin(2 * math.pi * f0 * i / SR) * math.exp(-i / (0.008 * SR))
for b in range(int(DUR / BEAT)): click(b * BEAT, 1600 if b % 4 == 0 else 1000, 0.9 if b % 4 == 0 else 0.45)
for t in (27.71, 30.31): click(t, 2600, 0.8)   # ♥ Brownstone ('watching you kiss her') and ✕ Songbird
with wave.open(f'{W}/click.wav', 'w') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(b''.join(struct.pack('<h', int(max(-1, min(1, x)) * 32000)) for x in buf))
run('ffmpeg', '-y', '-framerate', '30', '-i', f'{W}/all/%04d.jpg', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '21', '-preset', 'slow', '-movflags', '+faststart', f'{W}/reel.mp4')
run('ffmpeg', '-y', '-i', f'{W}/reel.mp4', '-i', f'{W}/click.wav', '-vf', 'scale=540:960', '-c:v', 'libx264', '-crf', '26', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k', '-shortest', f'{W}/beat.mp4')
run('convert', f'{W}/all/1245.jpg', '-quality', '90', f'{W}/cover.jpg')  # 41.5s: the match card + "See it together, share it or shop it"
args = []
for i in range(116):
    t = i * 0.5; args += ['-label', f'{t:.1f}s', f'{W}/all/{int(round(t * 30)):04d}.jpg']
run('montage', *args, '-tile', '12x', '-geometry', '216x384+4+4', '-pointsize', '18', f'{W}/cs.jpg')
# safe zones: content band y 250-1500 (green), IG top bar + bottom caption/UI (red), right action rail (red)
sz = []
for t in [19.6, 24.3, 25.3, 27.75, 30.3, 32.2, 33.6, 35.0, 36.2, 37.3, 38.6, 40.5, 42.5, 44.8, 47.2, 48.5, 51.0, 54.0, 57.5]:
    f = f'{W}/all/{int(round(t * 30)):04d}.jpg'; o = f'{W}/sz_{t:05.2f}.jpg'
    run('convert', f, '-fill', 'rgba(255,0,0,0.28)', '-draw', 'rectangle 0,0 1080,250', '-draw', 'rectangle 0,1500 1080,1920', '-draw', 'rectangle 930,1100 1080,1500',
        '-stroke', '#00b050', '-strokewidth', '6', '-fill', 'none', '-draw', 'rectangle 40,250 1040,1500', o); sz += ['-label', f'{t:.2f}s', o]
run('montage', *sz, '-tile', '10x', '-geometry', '270x480+4+4', '-pointsize', '20', f'{W}/sz.jpg')
for src, dst in [('reel.mp4', 'launch-reel-redo.mp4'), ('beat.mp4', 'launch-reel-redo-beat-test.mp4'), ('cover.jpg', 'launch-reel-redo-cover.jpg'),
                 ('cs.jpg', 'launch-reel-redo-contact-sheet.jpg'), ('sz.jpg', 'launch-reel-redo-safezones.jpg')]:
    shutil.copy(f'{W}/{src}', f'{D}/.{dst}.tmp'); os.replace(f'{D}/.{dst}.tmp', f'{D}/{dst}')
print('ok')
