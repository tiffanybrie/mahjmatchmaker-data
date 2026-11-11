#!/usr/bin/env python3
"""Preview copy of the Brand Watch page for the private claude.ai artifact (18JAJeZRLcZtcqVejgKHMs): the artifact viewer
blocks outside images, so every product photo is downloaded, shrunk to 480px and inlined as a data: URI.
The website copy (brand-watch.html) keeps the brand-hosted image URLs. Usage: site_brand_watch_preview.py"""
import re, os, io, base64, subprocess
from PIL import Image
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
src = R + 'site/livepatch/brand-watch/brand-watch.html'; out = R + 'site/livepatch/brand-watch/brand-watch-preview.html'
h = open(src).read(); cache = {}
def inline(m):
    u = m.group(1)
    if u not in cache:
        try:
            b = subprocess.run(['curl', '-sL', '--max-time', '20', u], capture_output=True).stdout
            im = Image.open(io.BytesIO(b)).convert('RGB'); im.thumbnail((480, 480))
            o = io.BytesIO(); im.save(o, 'JPEG', quality=80); cache[u] = 'data:image/jpeg;base64,' + base64.b64encode(o.getvalue()).decode()
        except Exception: cache[u] = u
    return 'src="' + cache[u] + '"'
h = re.sub(r'src="(https://[^"]+)"', inline, h)
open(out, 'w').write(h); print(out, sum(v.startswith('data:') for v in cache.values()), 'of', len(cache), 'images inlined')
