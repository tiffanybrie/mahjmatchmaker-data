"""Build the one-page thin-album swipe review (♥/✕ per mat, votes in the artifact db collection `votes`)."""
import json, base64, io, html, re
from PIL import Image
R = '/home/claude/mahjmatchmaker-data/'
S = json.load(open('shortlist.json'))
COUNTS = {'sorbet': 8, 'sunset': 9, 'limoncello': 10, 'gemma': 11, 'taylor': 12, 'jasmine': 11, 'nantucket': 12, 'pippa': 17, 'osler': 19}
def uri(p, side, q=78):
    im = Image.open(R + p).convert('RGB'); im.thumbnail((side, side), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'WEBP', quality=q); return 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()
data = []
for s, v in S.items():
    tp = next(f'assets/tiles/album/{s}.{e}' for e in ('jpg', 'png', 'jpeg') if __import__('os').path.exists(R + f'assets/tiles/album/{s}.{e}'))
    data.append({'set': s, 'name': v['name'], 'col': v['tc'], 'album': v['album'], 'now': COUNTS[s], 'tile': uri(tp, 360),
                 'mats': [{'id': s + '__' + re.sub(r'[^a-z0-9]+', '-', (m['brand'] + ' ' + m['name']).lower()).strip('-'), 'key': m['key'],
                           'name': m['name'], 'brand': m['brand'], 'url': m['url'], 'img': uri(m['img'], 460)} for m in v['mats']]})
tpl = open('page.tpl.html').read()
open('thin-album-review.html', 'w').write(tpl.replace('__DATA__', json.dumps(data, ensure_ascii=False)))
print(len(open('thin-album-review.html').read()) // 1024, 'KB', sum(len(d['mats']) for d in data), 'mats')
