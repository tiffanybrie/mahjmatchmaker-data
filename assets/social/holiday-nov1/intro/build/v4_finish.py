"""v4 (Nov 3): frames -> silent mp4, beat-test mp4 (click per 150 BPM beat, accent on bar downbeats), cover, contact sheet (every 0.5s).
Writes to temp names then moves into assets/social/holiday-nov1/intro/."""
import os, subprocess, wave, struct, math, shutil
W = '/dev/shm/introv4'; D = '/home/claude/mahjmatchmaker-data/assets/social/holiday-nov1/intro'
DUR, BEAT, SR = 42.8, 0.4, 44100
def run(*a): subprocess.run(a, check=True, capture_output=True)
n = int(DUR * SR); buf = [0.0] * n
for b in range(int(DUR / BEAT)):
    acc = b % 4 == 0; f0 = 1600 if acc else 1000; amp = 0.9 if acc else 0.45; s0 = int(b * BEAT * SR)
    for i in range(int(0.035 * SR)):
        if s0 + i < n: buf[s0 + i] += amp * math.sin(2 * math.pi * f0 * i / SR) * math.exp(-i / (0.008 * SR))
with wave.open(f'{W}/click.wav', 'w') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(b''.join(struct.pack('<h', int(max(-1, min(1, x)) * 32000)) for x in buf))
run('ffmpeg', '-y', '-framerate', '30', '-i', f'{W}/frames/%04d.jpg', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '19', '-preset', 'medium', '-movflags', '+faststart', f'{W}/v4.mp4')
run('ffmpeg', '-y', '-i', f'{W}/v4.mp4', '-i', f'{W}/click.wav', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k', '-shortest', f'{W}/v4-beat.mp4')
run('convert', f'{W}/frames/0066.jpg', '-quality', '90', f'{W}/v4-cover.jpg')  # t=2.2s: opener with HOLIDAY EDITION + "It's holiday time!"
os.makedirs(f'{W}/cs', exist_ok=True)
args = []
for i in range(86):
    t = i * 0.5; fn = f'{W}/frames/{int(round(t * 30)):04d}.jpg'; args += ['-label', f'{t:.1f}s', fn]
run('montage', *args, '-tile', '12x', '-geometry', '216x384+4+4', '-pointsize', '18', f'{W}/v4-cs.jpg')
for src, dst in [('v4.mp4', 'holiday-intro-reel-v4.mp4'), ('v4-beat.mp4', 'holiday-intro-reel-v4-beat-test.mp4'), ('v4-cover.jpg', 'holiday-intro-reel-v4-cover.jpg'), ('v4-cs.jpg', 'holiday-intro-reel-v4-contact-sheet.jpg')]:
    shutil.copy(f'{W}/{src}', f'{D}/.{dst}.tmp'); os.replace(f'{D}/.{dst}.tmp', f'{D}/{dst}')
print('ok')
