"""Inline img/*.jpg into src.html -> index.html (self-contained storyboard). Run from this folder."""
import base64, re, pathlib
here = pathlib.Path(__file__).parent
src = (here / 'src.html').read_text()
def rep(m):
    return 'data:image/jpeg;base64,' + base64.b64encode((here / 'img' / (m.group(1) + '.jpg')).read_bytes()).decode()
out = re.sub(r'\{\{([a-z0-9-]+)\}\}', rep, src)
(here / 'index.html').write_text(out)
print('index.html', len(out) // 1024, 'KB')
