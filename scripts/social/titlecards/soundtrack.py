"""Synthesized soundtrack for title-card skits (no licensing: every sound is generated here).
Cues: phone ring -> cheesy hold music (lounge, electric piano + walking bass + brushes) -> dramatic sting ->
upbeat flirty swipe music (+ swipe whooshes, NOPE buzz, MATCH chimes) -> end button.
Usage: python3 soundtrack.py cues.json out.wav
cues.json: {"total": s, "ring": [0, 2.4], "hold": [2.4, t], "sting": t, "swipe": [t0, t1], "swipes": [[t, "nope"|"match"], ...], "end": t}
"""
import json, sys, numpy as np
SR = 44100

def t_(d): return np.arange(int(d * SR)) / SR
def env(n, a=.01, r=.2):
    e = np.ones(n); A = int(a * SR); Rr = min(int(r * SR), n)
    if A: e[:A] = np.linspace(0, 1, A)
    e[n - Rr:] *= np.linspace(1, 0, Rr); return e
def midi(m): return 440 * 2 ** ((m - 69) / 12)

def epiano(f, d, v=.25):
    t = t_(d); x = np.sin(2 * np.pi * f * t + 1.2 * np.exp(-3 * t) * np.sin(2 * np.pi * f * 14 * t))  # FM tine
    x += .3 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-2 * t)
    return v * x * np.exp(-1.6 * t) * env(len(t), .005, .08)
def bass(f, d, v=.35):
    t = t_(d); x = np.sin(2 * np.pi * f * t) + .25 * np.sin(2 * np.pi * 2 * f * t)
    return v * x * np.exp(-2.5 * t) * env(len(t), .004, .05)
def brush(d, v=.06):
    n = int(d * SR); x = np.random.randn(n); x = np.convolve(x, np.ones(8) / 8, 'same')
    return v * x * np.exp(-np.arange(n) / SR * 18)
def kick(v=.5):
    t = t_(.25); f = 110 * np.exp(-t * 18) + 45; return v * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)
def clap(v=.18):
    n = int(.15 * SR); x = np.random.randn(n); return v * x * np.exp(-np.arange(n) / SR * 30)

def put(buf, x, at):
    i = int(at * SR); j = min(len(buf), i + len(x))
    if i < len(buf) and j > i: buf[i:j] += x[:j - i]

def ring(buf, a, b):
    # modern trill: two-tone bursts, 0.9s on / 0.4s off
    t0 = a
    while t0 < b - .3:
        d = min(.9, b - t0); t = t_(d)
        tone = (np.sin(2 * np.pi * 1320 * t) + np.sin(2 * np.pi * 1660 * t)) * (np.sign(np.sin(2 * np.pi * 18 * t)) * .5 + .5)
        put(buf, .14 * tone * env(len(t), .01, .05), t0); t0 += 1.3

def hold(buf, a, b):
    # lounge / bossa hold music, 96 bpm, Fmaj7 - Em7 - Dm7 - G7 (2 bars each... 1 bar each)
    bpm = 96; beat = 60 / bpm; bar = 4 * beat
    prog = [(53, [57, 60, 64, 65]), (52, [55, 59, 62, 64]), (50, [53, 57, 60, 62]), (55, [53, 57, 59, 62])]
    mel = [72, 74, 76, None, 74, 72, 69, None, 71, 72, 74, None, 76, 74, 71, None]
    t0 = a; k = 0
    while t0 < b:
        root, ch = prog[k % 4]
        for s in (0, 1.5, 2.5):  # bossa comp hits
            for n in ch: put(buf, epiano(midi(n), beat * .9, .07), t0 + s * beat)
        for s, n in ((0, root), (1.5, root + 7), (2, root + 7), (3.5, root)):
            put(buf, bass(midi(n - 12), beat * .9, .28), t0 + s * beat)
        for s in range(8): put(buf, brush(beat / 2, .035 if s % 2 else .05), t0 + s * beat / 2)
        for s in range(4):
            n = mel[(k * 4 + s) % len(mel)]
            if n: put(buf, epiano(midi(n), beat * 1.2, .12), t0 + s * beat)
        t0 += bar; k += 1
    # fade the last 0.4s
    i, j = int((b - .4) * SR), int(b * SR); j = min(j, len(buf))
    if j > i > 0: buf[i:j] *= np.linspace(1, 0, j - i); buf[j:int(b * SR) + 1] *= 0

def sting(buf, at):
    # dun dun DUNNN: low brass-ish stacks + timpani roll
    for k, (d, notes) in enumerate([(.28, [38, 45, 50]), (.28, [37, 44, 49]), (1.6, [36, 43, 48, 51])]):
        st = at + k * .34
        for n in notes:
            t = t_(d); f = midi(n)
            x = sum(np.sin(2 * np.pi * f * h * t) / h for h in range(1, 7))
            put(buf, .09 * x * env(len(t), .02, .25 if k < 2 else .9), st)
        tt = t_(d); put(buf, .4 * np.sin(2 * np.pi * 55 * tt) * np.exp(-tt * 3), st)

def swipe_music(buf, a, b):
    # upbeat flirty: 118 bpm four-on-floor, bright plucky chords C - Am - F - G
    bpm = 118; beat = 60 / bpm; bar = 4 * beat
    prog = [[60, 64, 67], [57, 60, 64], [53, 57, 60], [55, 59, 62]]
    t0 = a; k = 0
    while t0 < b:
        ch = prog[k % 4]
        for s in range(4):
            put(buf, kick(.42), t0 + s * beat)
            if s % 2: put(buf, clap(.12), t0 + s * beat)
        for s in (.5, 1.5, 2.5, 3.5):
            for n in ch: put(buf, epiano(midi(n + 12), beat * .5, .06), t0 + s * beat)
        put(buf, bass(midi(ch[0] - 24), bar * .9, .3), t0)
        t0 += bar; k += 1
    i, j = int((b - .3) * SR), min(int(b * SR), len(buf))
    if j > i > 0: buf[i:j] *= np.linspace(1, 0, j - i); buf[j:int((b + 4) * SR)] *= 0

def whoosh(buf, at):
    n = int(.35 * SR); x = np.random.randn(n); x = np.convolve(x, np.ones(30) / 30, 'same')
    put(buf, .22 * x * np.hanning(n), at)
def nope(buf, at):
    t = t_(.3); put(buf, .05 * np.sin(2 * np.pi * 150 * t) * env(len(t), .005, .1), at)
def chime(buf, at):
    for k, n in enumerate((79, 84)):
        t = t_(.6); put(buf, .07 * np.sin(2 * np.pi * midi(n) * t) * np.exp(-t * 4), at + k * .09)
def end_button(buf, at):
    for k, n in enumerate((72, 76, 79, 84)):
        put(buf, epiano(midi(n), 1.2, .14), at + k * .11)

def rhodes(f, d, v):
    t = t_(d); x = np.sin(2 * np.pi * f * t) + .18 * np.sin(2 * np.pi * 2 * f * t) + .05 * np.sin(2 * np.pi * 3 * f * t)
    x *= 1 + .12 * np.sin(2 * np.pi * 4.5 * t)  # soft tremolo
    return v * x * np.exp(-.9 * t) * env(len(t), .03, .4)
def vibe(f, d, v):
    t = t_(d); x = np.sin(2 * np.pi * f * t) * (1 + .25 * np.sin(2 * np.pi * 6 * t))
    return v * x * np.exp(-1.8 * t) * env(len(t), .005, .3)

def elevator(buf, a, b):
    """Quiet, slow elevator / hold music (Oct 19 v2: Tiffany found v1 busy and loud)."""
    bpm = 80; beat = 60 / bpm; bar = 4 * beat
    prog = [(41, [57, 60, 64, 67]), (40, [55, 59, 62, 67]), (38, [53, 57, 60, 64]), (43, [53, 57, 59, 64])]
    mel = [(0, 76), (1.5, 74), (2, 72), None, (0, 74), (2, 71), None, (0, 72), (1, 69), (2, 67), None, None]
    t0 = a; k = 0
    while t0 < b:
        root, ch = prog[k % 4]
        for n in ch: put(buf, rhodes(midi(n), bar * 1.05, .028), t0)
        put(buf, rhodes(midi(root), bar, .06), t0); put(buf, rhodes(midi(root + 7), beat * 2, .035), t0 + 2 * beat)
        m = mel[k % len(mel)]
        if m: put(buf, vibe(midi(m[1]), beat * 2.5, .05), t0 + m[0] * beat)
        t0 += bar; k += 1

def seg(buf, fn, a, b, fin=0.0, fout=0.6):
    tmp = np.zeros_like(buf); fn(tmp, a, b + 2)
    i, j = int(a * SR), min(int(b * SR), len(buf))
    e = np.zeros(len(buf)); e[i:j] = 1
    if fin: k = int(fin * SR); e[i:i + k] = np.linspace(0, 1, k)
    k = int(fout * SR); e[j - k:j] *= np.linspace(1, 0, k)
    buf += tmp * e

def main(cues_path, out):
    c = json.load(open(cues_path)); buf = np.zeros(int(c['total'] * SR) + SR)
    ring(buf, *c['ring'])
    hr = c['hold'] if isinstance(c['hold'][0], list) else [c['hold']]
    style = c.get('style', 'elevator')
    if style == 'sfx':
        pass  # post version: ring + swipe sounds only; Instagram music goes on top
    else:
        for k, (a, b) in enumerate(hr): seg(buf, elevator, a, b, fin=0.4 if k == 0 else 1.5, fout=0.25 if k == 0 else 0.6)
    if c.get('sting') is not None: sting(buf, c['sting'])
    for at, kind in c.get('swipes', []):
        whoosh(buf, at); (nope if kind == 'nope' else chime)(buf, at + .15)
    end_button(buf, c['end'])
    buf = buf[:int(c['total'] * SR)]
    buf = np.tanh(buf * 1.2) * .8
    import wave
    with wave.open(out, 'w') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((buf * 32767).astype(np.int16).tobytes())

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
