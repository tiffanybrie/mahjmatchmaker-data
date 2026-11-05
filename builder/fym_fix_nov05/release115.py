"""v115 label + usage tracking ON (gate [157]; Tiffany approved Oct 17, endpoint live Nov 4 2:25pm, config/fym-tracking.json).
Works on any copy (build / website / artifact). Idempotent. Usage: python3 release115.py <dir or index.html>"""
import sys, os, re, json, subprocess
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
P = sys.argv[1]; P = P if P.endswith('.html') else os.path.join(P, 'index.html'); h = open(P).read()
for v in set(re.findall(r'Version 1\.\d+(?:\.\d+)?', h)): h = h.replace(v, 'Version 1.15')
open(P, 'w').write(h)
url = json.load(open(R + 'config/fym-tracking.json'))['trk_url']; assert url.startswith('https://script.google.com/')
subprocess.run([sys.executable, R + 'builder/fym_track_oct17.py', P, P, url], check=True)
h = open(P).read(); assert f"const TRK_URL='{url}';" in h and 'Version 1.15' in h
print('release115 ok', P)
