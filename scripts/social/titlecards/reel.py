"""Papaya hotline reel, one command (Oct 21, v11). Replaces the hand-patched v10.
body (build.py, REEL=1: profile card = current profile-c-story image, deck ends on a card)
+ animated ending (ending.py: one 'Hook me up!' card, one end card)
+ v9 soundtrack (ring + elevator music fading out by 0:28 so Tiffany can add her song).
v12 (Oct 21): identical build; the only change is the profile card (swipe_profile.py now draws X + heart only).
Usage: python3 scripts/social/titlecards/reel.py [out.mp4]          (REEL_VER=v12 for the v12 file + frames/v12/)
"""
import os, sys, json, subprocess
R = '/home/claude/mahjmatchmaker-data'
T = R + '/scripts/social/titlecards'
OUT = R + '/assets/social/titlecards/counseling-ep1-papaya'
VER = os.environ.get('REEL_VER', 'v11')
FR = OUT + '/frames/' + VER
dst = sys.argv[1] if len(sys.argv) > 1 else OUT + f'/papaya-hotline-{VER}.mp4'
env = dict(os.environ, REEL='1', REEL_VER=VER)
run = lambda *a: subprocess.run(list(a), check=True, env=env)

if not (os.environ.get('SKIP_BODY') == '1' and os.path.exists(FR + f'/{VER}-body-silent.mp4')): run('python3', T + '/build.py')
run('python3', T + '/ending.py')
dur = lambda f: float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]))
parts = [FR + f'/{VER}-body-silent.mp4', FR + '/end_hook.mp4', FR + '/end_card.mp4']
total = round(sum(dur(p) for p in parts), 6)
cues = json.load(open(OUT + '/frames/cues-v9.json')); cues['total'] = total
json.dump(cues, open(FR + f'/cues-{VER}.json', 'w'))
run('python3', T + '/soundtrack.py', FR + f'/cues-{VER}.json', FR + f'/st-{VER}.wav')
fc = ''.join(f'[{i}:v]fps=30,setsar=1,format=yuv420p[v{i}];' for i in range(3)) + '[v0][v1][v2]concat=n=3:v=1:a=0[v]'
run('ffmpeg', '-y', '-loglevel', 'error', *sum((['-i', p] for p in parts), []), '-i', FR + f'/st-{VER}.wav',
    '-filter_complex', fc, '-map', '[v]', '-map', '3:a', '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p',
    '-r', '30', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', dst)
print(dst, total)
