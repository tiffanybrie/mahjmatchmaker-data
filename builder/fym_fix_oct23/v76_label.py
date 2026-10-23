"""FYM v76 = v75 + a visible version label (Tiffany Oct 23 2:04pm: what I open must be called the version Claude names).
The build number now matches the claude.ai artifact version number. Usage: python3 v76_label.py <build_dir> <N>"""
import sys, re
B, N = sys.argv[1], sys.argv[2]; P = B + '/index.html'; h = open(P).read()
h, n1 = re.subn(r'<title>[^<]*</title>', f'<title>Find Your Mat-ch (Version {N})</title>', h, count=2)
old = 'Tell me here\xa0→</a></footer>'
assert h.count(old) == 1
h = h.replace(old, f'Tell me here\xa0→</a><small class="ver" style="display:block;margin-top:6px;font:600 11px var(--body);color:var(--mute)">Version {N}</small></footer>')
open(P, 'w').write(h); print('labelled', N, 'titles', n1)
