"""Render ONE email headline image (same style as render.py HEADS) and add it to the email manifest.
Usage: python3 scripts/fym_promo/head_one.py <stem> <h1|h2> "<text html>" """
import sys, json, os
from PIL import Image
from playwright.sync_api import sync_playwright
R = '/home/claude/mahjmatchmaker-data'; EM = f'{R}/site/email/assets/fym'
PINK, NAVY = '#d6336c', '#054689'
FONT = f"@font-face{{font-family:Cap;src:url('file://{R}/assets/fonts/Caprasimo.ttf')}}"
stem, kind, text = sys.argv[1:4]
st = f'font:400 80px/1.08 Cap;color:{PINK}' if kind == 'h1' else f'font:400 52px/1.1 Cap;color:{NAVY}'
html = f"""<!doctype html><meta charset=utf-8><style>{FONT}html,body{{margin:0;background:transparent}}#c{{display:inline-block;padding:6px 4px 10px;max-width:1060px;text-align:center;text-wrap:balance;{st}}}</style><div id=c>{text}</div>"""
f = '/dev/shm/fymh/render/one.html'; open(f, 'w').write(html)
out = f'{EM}/{stem}.png'
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1400, 'height': 1600})
    pg.goto('file://' + f); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(300)
    pg.locator('#c').screenshot(path=out, omit_background=True); b.close()
im = Image.open(out).convert('RGBA'); im.quantize(colors=64, method=Image.FASTOCTREE).save(out, optimize=True)
m = json.load(open(f'{EM}/manifest.json')); m['alt'][stem] = text.replace('&rsquo;', '’')
m['sizes'][f'{stem}.png'] = [*Image.open(out).size, os.path.getsize(out)]
json.dump(m, open(f'{EM}/manifest.json', 'w'), indent=1, ensure_ascii=False); print('ok', out, Image.open(out).size)
