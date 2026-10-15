"""Force Tiffany's canonical photos into a swipe book, every time a book is built or patched.

Why (Tiffany, Oct 15): Heritage 1.0 kept showing the Heritage 2.0 product photo in swipe books,
because books copied their tile list from an older book. Fix it at the source: run this on every
book before publishing (finish_patch.py calls it too).

Canonical photos (permanent):
- Heritage 1.0 (id 'heritage'): assets/tiles/album/heritage.jpg (burl backs, green layers). Never the 2.0 photo.
- Heritage 2.0 (id 'heritage-2-0'): assets/tiles/album/heritage-2-0.jpg
- Sunday Mahjong (ids 'sunday', 'sunday-*' tile sets): assets/tiles/album/sunday-tile-set.png
- OMM Spring Fling mat (ids 'spring-fling', 'omm-spring-fling', 'vault-spring-fling', 'ret-spring-fling'; NOT other brands' Spring Fling mats): assets/mats/omm-retired/spring-fling.png (Tiffany's photo, Oct 15)

Usage: python3 canon_tiles.py book.html [more.html ...]   (edits in place; also fixes relative image files next to the book)
"""
import sys, os, re, json, base64, io
from PIL import Image

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
RULES = [
    (re.compile(r'^(hol-)?heritage$'), 'assets/tiles/album/heritage.jpg'),
    (re.compile(r'^(hol-)?heritage-2-0$'), 'assets/tiles/album/heritage-2-0.jpg'),
    (re.compile(r'^(hol-)?sunday(-tile-set)?$'), 'assets/tiles/album/sunday-tile-set.png'),
    (re.compile(r'^(omm-|vault-|ret-)?spring-fling$|^omm-spring-fling'), 'assets/mats/omm-retired/spring-fling.png'),  # OMM only (Mahj Mood also has a 'Spring Fling Mat')
]

def canon_for(item_id):
    for rx, path in RULES:
        if rx.search(item_id or ''):
            p = os.path.join(REPO, path)
            if os.path.exists(p):
                return p
    return None

def encode(path, max_side):
    im = Image.open(path)
    im = im.convert('RGBA') if im.mode in ('RGBA', 'LA', 'P') else im.convert('RGB')
    im.thumbnail((max_side, max_side), Image.LANCZOS)
    buf = io.BytesIO()
    if im.mode == 'RGBA':
        bg = Image.new('RGB', im.size, (255, 255, 255)); bg.paste(im, mask=im.split()[3]); im = bg
    im.save(buf, 'JPEG', quality=86)
    return buf.getvalue()

def size_of_data_uri(uri):
    try:
        b = base64.b64decode(uri.split(',', 1)[1])
        return max(Image.open(io.BytesIO(b)).size)
    except Exception:
        return 800

def fix_book(path):
    s = open(path).read()
    i = s.find('const D=')
    if i < 0:
        print(path, ': no D, skipped'); return 0
    j = i + len('const D=')
    D, end = json.JSONDecoder().raw_decode(s, j)
    changed = 0
    base = os.path.dirname(path)
    for key in ('groups', 'items'):
        for it in D.get(key, []) or []:
            src = canon_for(it.get('id', ''))
            if not src:
                continue
            img = it.get('img') or ''
            if img.startswith('data:'):
                new = 'data:image/jpeg;base64,' + base64.b64encode(encode(src, size_of_data_uri(img))).decode()
                if new != img:
                    it['img'] = new; changed += 1
            elif img:
                fp = os.path.join(base, img)
                os.makedirs(os.path.dirname(fp) or '.', exist_ok=True)
                data = encode(src, 1600)
                if not os.path.exists(fp) or open(fp, 'rb').read() != data:
                    open(fp, 'wb').write(data); changed += 1
                    print('  rewrote file', fp)
    if changed:
        s = s[:j] + json.dumps(D, separators=(',', ':'), ensure_ascii=False) + s[end:]
        open(path, 'w').write(s)
    print(path, ':', changed, 'fixed')
    return changed

if __name__ == '__main__':
    for p in sys.argv[1:]:
        fix_book(p)
