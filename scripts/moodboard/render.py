#!/usr/bin/env python3
"""Mahj Matchmaker MOOD BOARD STYLE generator.

One board JSON -> every format (Amazon/IG static, Pinterest pin, Story tap-to-reveal
frames, animated Reel). Layout zones live in layouts.json (by canvas + item count);
a board can override any zone. Rendered with Playwright (Chromium).

Usage (from repo root):
  python3 scripts/moodboard/render.py scripts/moodboard/boards/rackin-rudolph.json \
      --version amazon --canvas 1080x1350 [--frames] [--reel] [--debug] [--out DIR]

  --version  amazon | social | pinterest   (amazon = Amazon items only, no URL)
  --canvas   1080x1350 (IG/Amazon) | 1000x1500 (Pinterest) | 1080x1920 (Story/Reel)
  --frames   also write story frames: frame 1 = header + mat, then one item per tap
  --reel     also write an MP4 where items pop on one by one (needs ffmpeg)
  --debug    draw zone boxes (for tuning layouts)

See project doc "79 Mood Board Style - our standard layout" for the rules.
"""
import argparse, json, os, sys, html, subprocess, shutil, tempfile
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
FONTS = os.path.join(HERE, 'fonts')

BRAND = {
    'navy': '#054689', 'pink': '#f56c8c', 'cream': '#f6e9df',
    'ink': '#2b2623', 'paper': '#fffdfa',
}


def rp(p):
    return p if os.path.isabs(p) else os.path.join(REPO, p)


def load_layout(canvas, count, board):
    L = json.load(open(os.path.join(HERE, 'layouts.json')))
    W, H = map(int, canvas.split('x'))
    src_canvas, scale, dy = canvas, 1.0, 0.0
    if canvas not in L or not L[canvas].get('zones'):
        # derive from the 1080x1350 master: scale to width, centre vertically
        src_canvas = '1080x1350'
        scale = W / 1080.0
        dy = (H - 1350 * scale) / 2.0
    C = L[src_canvas]
    counts = sorted(int(k) for k in C['zones'])
    pick = min(counts, key=lambda c: (abs(c - count), -c))
    zones = json.loads(json.dumps(C['zones'][str(pick)]))
    header = json.loads(json.dumps(C['header']))
    ov = board.get('layout_overrides', {}).get(canvas, {})
    for role, z in ov.get('zones', {}).items():
        zones.setdefault(role, {}).update(z)
    header.update(ov.get('header', {}))
    return W, H, zones, header, scale, dy, pick


def item_list(board, version):
    out = []
    for it in board['items']:
        it = dict(it)
        if version == 'amazon':
            if it.get('amazon'):
                it.update(it['amazon'])
            elif it.get('partner'):
                continue  # partner piece with no Amazon swap -> leave it out
        if version in it.get('skip', []):
            continue
        out.append(it)
    return out


def font_css():
    f = lambda n: 'file://' + os.path.join(FONTS, n)
    return f"""
@font-face{{font-family:Caprasimo;src:url({f('Caprasimo.woff2')})}}
@font-face{{font-family:Playfair;font-style:italic;src:url({f('PlayfairDisplay.woff2')})}}
@font-face{{font-family:Bitter;src:url({f('Bitter.woff2')})}}
@font-face{{font-family:Hand;src:url({f('Allison.woff2')})}}
"""


def build_html(board, version, canvas, debug=False, upto=None, animate=False):
    items = item_list(board, version)
    W, H, zones, header, s, dy, pick = load_layout(canvas, len(items), board)
    theme = board.get('theme', {})
    title_c = theme.get('title', BRAND['navy'])
    tag_c = theme.get('tagline', BRAND['ink'])
    ink = theme.get('ink', BRAND['ink'])
    bg = theme.get('paper', BRAND['paper'])
    X = lambda v: v * s
    Y = lambda v: v * s + dy

    parts, svg = [], []
    missing = []
    for i, it in enumerate(items):
        z = zones.get(it['role'])
        if not z:
            missing.append(it['role']); continue
        path = rp(it['src'])
        iw, ih = Image.open(path).size
        w = z['w']; h = w * ih / iw
        if z.get('h'):  # optional height cap
            if h > z['h']:
                h = z['h']; w = h * iw / ih
        x = z['x'] + (z['w'] - w) * z.get('ax', 0.5) if z.get('h') else z['x']
        y = z['y']
        kind = it.get('kind', 'cutout')
        vis = (upto is None or i < upto)
        delay = f'animation-delay:{0.35 + i * 0.7:.2f}s;' if animate else ''
        cls = f'it {kind}' + (' anim' if animate else '')
        style = (f'left:{X(x):.1f}px;top:{Y(y):.1f}px;width:{X(w):.1f}px;height:{X(h):.1f}px;'
                 f'transform:rotate({z.get("rot", 0)}deg);z-index:{z.get("z", 10)};'
                 f'{"" if vis else "visibility:hidden;"}{delay}')
        parts.append(f'<div class="{cls}" style="{style}"><img src="file://{path}"></div>')
        if debug:
            parts.append(f'<div class="dbg" style="left:{X(x)}px;top:{Y(y)}px;width:{X(w)}px;height:{X(h)}px">{it["role"]} {int(w)}x{int(h)}</div>')
        lab = z.get('label'); text = it.get('label')
        if lab and text and vis:
            fs = lab.get('size', 50) * s
            al = lab.get('align', 'left')
            lstyle = (f'left:{X(lab["x"]):.1f}px;top:{Y(lab["y"]):.1f}px;width:{X(lab.get("w", 340)):.1f}px;'
                      f'font-size:{fs:.1f}px;text-align:{al};transform:rotate({lab.get("rot", 0)}deg);'
                      f'color:{ink};{delay}')
            t = html.escape(text).replace('\\n', '<br>').replace('\n', '<br>')
            parts.append(f'<div class="lab{" anim" if animate else ""}" style="{lstyle}">{t}</div>')
            if lab.get('arrow'):
                a = lab['arrow']  # [x1,y1, cx,cy, x2,y2] quadratic, ends at the item
                p = [X(a[0]), Y(a[1]), X(a[2]), Y(a[3]), X(a[4]), Y(a[5])]
                anim = f' class="anim" style="{delay}"' if animate else ''
                svg.append(f'<path{anim} d="M{p[0]:.1f},{p[1]:.1f} Q{p[2]:.1f},{p[3]:.1f} {p[4]:.1f},{p[5]:.1f}" '
                           f'fill="none" stroke="{ink}" stroke-width="{2.6 * s:.2f}" stroke-linecap="round" marker-end="url(#ah)"/>')
    if missing:
        print('WARNING: no zone for roles', missing, 'in', canvas, 'layout', pick, file=sys.stderr)

    # header: wordmark + title + tagline (+ kicker)
    hd = []
    show_brand = board.get('brand_mark', {}).get(version, True)
    if show_brand:
        wm = rp(header.get('wordmark', 'assets/brand/mahjmatchmaker-wordmark-notag.png'))
        hd.append(f'<img class="wm" src="file://{wm}" style="top:{Y(header["wm_y"]):.1f}px;width:{X(header["wm_w"]):.1f}px">')
    if board.get('title'):
        hd.append(f'<div class="title" style="top:{Y(header["title_y"]):.1f}px;font-size:{X(header["title_size"]):.1f}px;color:{title_c}">{html.escape(board["title"])}</div>')
    if board.get('tagline'):
        hd.append(f'<div class="tag" style="top:{Y(header["tag_y"]):.1f}px;font-size:{X(header["tag_size"]):.1f}px;color:{tag_c}">{html.escape(board["tagline"])}</div>')
    kick = board.get('kicker', {}).get(version)
    if kick and header.get('kicker_y') is not None:
        hd.append(f'<div class="kick" style="top:{Y(header["kicker_y"]):.1f}px;font-size:{X(header.get("kicker_size", 15)):.1f}px;color:{BRAND["navy"]}">{html.escape(kick)}</div>')

    doc = f"""<!doctype html><html><head><meta charset="utf-8"><style>
{font_css()}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:{W}px;height:{H}px;background:{bg};overflow:hidden}}
.board{{position:relative;width:{W}px;height:{H}px}}
.it{{position:absolute;transform-origin:50% 50%}}
.it img{{width:100%;height:100%;display:block}}
.it.cutout img,.it.round img{{filter:drop-shadow(0 {6*s:.1f}px {9*s:.1f}px rgba(60,40,30,.16))}}
.it.photo{{background:#fff;padding:{9*s:.1f}px;border-radius:{6*s:.1f}px;box-shadow:0 {8*s:.1f}px {22*s:.1f}px rgba(60,40,30,.16)}}
.it.photo img{{object-fit:cover;border-radius:{3*s:.1f}px}}
.it.flat img{{border-radius:{8*s:.1f}px;box-shadow:0 {8*s:.1f}px {20*s:.1f}px rgba(60,40,30,.18)}}
.lab{{position:absolute;font-family:Hand,cursive;line-height:.9;z-index:60;white-space:nowrap}}
svg.arrows{{position:absolute;left:0;top:0;z-index:59;pointer-events:none}}
.wm{{position:absolute;left:50%;transform:translateX(-50%);z-index:70}}
.title{{position:absolute;left:0;right:0;text-align:center;font-family:Caprasimo;line-height:1;z-index:70}}
.tag{{position:absolute;left:0;right:0;text-align:center;font-family:Playfair;font-style:italic;line-height:1;z-index:70}}
.kick{{position:absolute;left:0;right:0;text-align:center;font-family:Bitter;letter-spacing:.32em;text-transform:uppercase;z-index:70}}
.dbg{{position:absolute;outline:2px dashed #e33;color:#e33;font:12px monospace;z-index:99}}
@keyframes pop{{0%{{opacity:0;transform:scale(.82)}}70%{{opacity:1;transform:scale(1.03)}}100%{{opacity:1}}}}
@keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
.it.anim{{opacity:0;animation:pop .55s ease-out forwards}}
.lab.anim,path.anim{{opacity:0;animation:fade .4s ease-out forwards}}
</style></head><body><div class="board">
{''.join(hd)}
{''.join(parts)}
<svg class="arrows" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs>
<marker id="ah" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="{7*s:.1f}" markerHeight="{7*s:.1f}" markerUnits="userSpaceOnUse" orient="auto-start-reverse">
<path d="M1,1 L8,5 L1,9" fill="none" stroke="{ink}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>
{''.join(svg)}</svg>
</div></body></html>"""
    return doc, W, H, len(items), pick


def shoot(doc, W, H, out_png, video_dir=None, seconds=None):
    from playwright.sync_api import sync_playwright
    tmp = tempfile.NamedTemporaryFile('w', suffix='.html', delete=False, dir=HERE)
    tmp.write(doc); tmp.close()
    try:
        with sync_playwright() as p:
            b = p.chromium.launch()
            kw = dict(viewport={'width': W, 'height': H}, device_scale_factor=1)
            if video_dir:
                kw['record_video_dir'] = video_dir
                kw['record_video_size'] = {'width': W, 'height': H}
            ctx = b.new_context(**kw)
            pg = ctx.new_page()
            pg.goto('file://' + tmp.name)
            pg.evaluate('document.fonts.ready')
            pg.wait_for_timeout(int((seconds or 0.6) * 1000))
            if out_png:
                pg.screenshot(path=out_png)
            vid = pg.video.path() if video_dir else None
            ctx.close(); b.close()
            return vid
    finally:
        os.unlink(tmp.name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('board')
    ap.add_argument('--version', default='amazon')
    ap.add_argument('--canvas', default='1080x1350')
    ap.add_argument('--out', default=None)
    ap.add_argument('--frames', action='store_true')
    ap.add_argument('--reel', action='store_true')
    ap.add_argument('--debug', action='store_true')
    a = ap.parse_args()
    board = json.load(open(a.board))
    out = rp(a.out or board.get('out_dir', f'assets/moodboards/{board["slug"]}'))
    os.makedirs(out, exist_ok=True)
    base = f'{board["slug"]}-{a.version}-{a.canvas}'
    doc, W, H, n, pick = build_html(board, a.version, a.canvas, debug=a.debug)
    png = os.path.join(out, base + ('-debug' if a.debug else '') + '.png')
    shoot(doc, W, H, png)
    jpg = png[:-4] + '.jpg'
    Image.open(png).convert('RGB').save(jpg, quality=92)
    print(f'{jpg}  ({n} items, layout {pick})')
    if a.frames:
        fd = os.path.join(out, base + '-frames'); os.makedirs(fd, exist_ok=True)
        for k in range(1, n + 1):
            d, *_ = build_html(board, a.version, a.canvas, upto=k)
            f = os.path.join(fd, f'frame-{k:02d}.png'); shoot(d, W, H, f)
            Image.open(f).convert('RGB').save(f[:-4] + '.jpg', quality=90); os.unlink(f)
        print(f'{fd}/ ({n} frames)')
    if a.reel:
        d, *_ = build_html(board, a.version, a.canvas, animate=True)
        vd = tempfile.mkdtemp()
        secs = 0.35 + n * 0.7 + 2.5
        vid = shoot(d, W, H, None, video_dir=vd, seconds=secs)
        mp4 = os.path.join(out, base + '-reel.mp4')
        if shutil.which('ffmpeg') and vid:
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', vid, '-c:v', 'libx264',
                            '-pix_fmt', 'yuv420p', '-r', '30', mp4], check=True)
            print(mp4)
        else:
            shutil.copy(vid, mp4[:-4] + '.webm'); print(mp4[:-4] + '.webm')
        shutil.rmtree(vd, ignore_errors=True)


if __name__ == '__main__':
    main()
