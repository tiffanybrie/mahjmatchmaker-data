"""Beat-marker click track (self-generated, no copyrighted audio): 160 BPM, accent on every 4th beat. Muxes onto a reel.
Usage: python3 click.py <in.mp4> <out.mp4>"""
import sys, subprocess, json, wave, numpy as np
src, out = sys.argv[1], sys.argv[2]
dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src], capture_output=True, text=True).stdout)
sr = 44100; B = 60 / 160; a = np.zeros(int(dur * sr) + sr, np.float32); t = np.arange(int(.05 * sr)) / sr
for i in range(int(dur / B) + 1):
    f, g = (1760, .9) if i % 4 == 0 else (1100, .5)
    s = int(i * B * sr); c = g * np.sin(2 * np.pi * f * t) * np.exp(-t * 70); a[s:s + len(c)] += c[:len(a) - s]
w = wave.open('/dev/shm/fym-holiday/click.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
w.writeframes((np.clip(a[:int(dur * sr)], -1, 1) * 32000).astype(np.int16).tobytes()); w.close()
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-i', '/dev/shm/fym-holiday/click.wav', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '96k', '-shortest', out], check=True)
print('ok', out)
