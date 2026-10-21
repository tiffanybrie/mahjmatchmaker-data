"""Season 2 trailer v5 (Oct 21) from ep00-trailer-s2-v4.mp4 (kept as-is).
- frames 0-557 (Mahj Matchmaker 2.0, vault, hundreds of mats, this week): v4 unchanged.
- frames 558-1049, the 16.4 s "dating profiles" scene (trailer-v4/s5.html): re-rendered with the matches in the
  order the brand guide asks for (official pair in the middle, never first): Chantilly, Fleur, Martha & Mae.
  Same jokes, same racks (Coquette's current picks: OMM Pink Quartz, M&M White Lace, B&B Lilac).
- frames 1050-1169 (Season 2, new episodes start this week): v4 unchanged.
- from 39.0 s: the hotline v12 end card (Hooking up tiles, / mats & racks . Find Your Mat-ch(TM) . 10.27 .
  mahjmatchmaker.com . Code MAHJMATCH . LINK IN BIO), replacing "COMING 10.27 / Find Your Match".
Silent; her song ("Love Shack") goes on in Edits from 0:00.
Usage: python3 scripts/reel/s2/v2/trailer.py  -> assets/reels/s2/ep00-trailer-s2-v5.mp4"""
import os, sys, re, asyncio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit
from kit import R, WORK
from playwright.async_api import async_playwright

V4 = f'{R}/assets/reels/s2/ep00-trailer-s2-v4.mp4'
S5 = f'{R}/scripts/reel/s2/trailer-v4/s5.html'
OUT = f'{R}/assets/reels/s2/ep00-trailer-s2-v5.mp4'


def reorder(html):
    blocks = re.findall(r' <div class="sui" id="s(\d)">(.*?)\n </div>\n', html, re.S)
    assert len(blocks) == 3, len(blocks)
    body = {k: v for k, v in blocks}
    new = {'1': body['3'], '2': body['1'], '3': body['2']}          # Chantilly, Fleur (official pair, middle), Martha & Mae
    for k in new:
        new[k] = re.sub(r'MATCH \d', f'MATCH {k}', new[k])
    for k, v in blocks:
        html = html.replace(f' <div class="sui" id="s{k}">{v}\n </div>\n', f' <div class="sui" id="s{k}">@@{k}@@\n </div>\n')
    for k in new:
        html = html.replace(f'@@{k}@@', new[k])
    return html


def render_s5(html, d, n=492):
    os.makedirs(d, exist_ok=True)
    tmp = os.path.dirname(S5) + '/_s5_v5.html'; open(tmp, 'w').write(html)    # same folder so img/ resolves
    async def go():
        async with async_playwright() as p:
            b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
            await pg.goto('file://' + tmp); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(400)
            for i in range(n):
                await pg.evaluate(f'render({i / 30})'); await pg.screenshot(path=f'{d}/{i:04d}.png')
            await b.close()
    asyncio.run(go()); os.remove(tmp)


if __name__ == '__main__':
    a = kit.cut(V4, f'{WORK}/tr-a.mp4', 0, 558)
    d = f'{WORK}/tr-s5'
    render_s5(reorder(open(S5).read()), d)
    s5 = kit.encode(d, f'{WORK}/tr-s5.mp4')
    c = kit.cut(V4, f'{WORK}/tr-c.mp4', 1050, 1170)
    end = kit.ending('tr', 'Coquette', 'assets/tiles/album/coquette.jpg', 'assets/mats/gallery/oh-my-mahjong--chantilly.webp',
                     'Code <span style="color:#d6336c">MAHJMATCH</span> at our partner brands', None, None, [], with_hook=False)
    kit.concat([a, s5, c] + end, OUT); print(OUT)
