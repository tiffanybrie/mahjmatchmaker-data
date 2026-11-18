"""Read-only final album view (Tiffany Nov 17 2:55am: 'the final', no review round, no New box): cards in album order,
year-round then holiday, 5 across on a phone. Usage: final_view.py <set> <out.html>"""
import json, io, base64, sys
from PIL import Image
R = '/home/claude/mahjmatchmaker-data/'
SET, OUT = sys.argv[1], sys.argv[2]
rec = json.load(open(R + f'config/album-records/{SET}.json'))
man = json.load(open(R + rec['cards_dir'] + '/manifest.json')); spec = json.load(open(R + rec['spec']))
hol = {m['name'] for m in spec['mats'] if m.get('holiday')}
main = [c for c in man['cards'] if c['mat'] not in hol]; hl = [c for c in man['cards'] if c['mat'] in hol]
def card(c, i):
    im = Image.open(R + rec['cards_dir'] + '/' + c['file']).convert('RGB'); im.thumbnail((520, 650)); b = io.BytesIO(); im.save(b, 'JPEG', quality=78)
    return f'<figure><img loading="lazy" src="data:image/jpeg;base64,{base64.b64encode(b.getvalue()).decode()}" alt=""><figcaption><b>{i}</b> {c["mat"]}</figcaption></figure>'
name = rec.get('name', SET)
html = f'''<title>{name} Final</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>:root{{--bg:#faf7f2;--fg:#2a2f3a;--mut:#707684}}@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#17191e;--fg:#eceef2;--mut:#a3a8b4;color-scheme:dark}}}}:root[data-theme="dark"]{{--bg:#17191e;--fg:#eceef2;--mut:#a3a8b4;color-scheme:dark}}
body{{background:var(--bg);color:var(--fg);font:14px/1.4 system-ui,sans-serif;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:16px 40px}}
h1{{font-size:21px;margin:0 0 2px}}h2{{font-size:17px;margin:22px 0 8px}}p{{color:var(--mut);margin:0 0 10px}}
.g{{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:6px}}@media(min-width:700px){{.g{{grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px}}}}
figure{{margin:0;min-width:0}}img{{width:100%;display:block;border-radius:4px}}figcaption{{font-size:11px;color:var(--mut);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}</style>
<h1>{name}: final album order</h1><p>{len(main)} year-round cards, then {len(hl)} holiday cards. Read-only, nothing to answer.</p>
<div class="g">{"".join(card(c, i + 1) for i, c in enumerate(main))}</div>
<h2>Holiday</h2><div class="g">{"".join(card(c, i + 1) for i, c in enumerate(hl))}</div>'''
open(OUT, 'w').write(html); print(len(main), len(hl))
