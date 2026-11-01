"""Ask Me Anything / FAQ carousel (Find Your Mat-ch edition), drafts for Tiffany, Nov 1 2026.

Renders 10 feed slides (1080x1350) + 11 story frames (1080x1920, incl. a question-sticker frame)
with HTML + Playwright, then a contact sheet. Real product photos + real crops of the LIVE tool
(Version 1.11, captured Nov 1 from mahjmatchmaker.com/find-your-match: src/ui/*.png).
Run: python3 assets/social/next-week-talk/src/build_ama.py
"""
import os, random, html
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
OUT = os.path.join(R, 'assets/social/next-week-talk/ama')
UI = os.path.join(R, 'assets/social/next-week-talk/src/ui')
F = 'file://' + os.path.join(R, 'scripts/social/tileprofile/fonts') + '/'
def P(rel): return 'file://' + os.path.join(R, rel)

NAVY, DEEP, ROSE, HPINK, HEART, BLUSH, PCREAM, PAPER = '#054689', '#062a55', '#c8325f', '#d6336c', '#f56c8c', '#f7b6c8', '#fbe3ea', '#faf3ea'

# ---------- content (US spelling; her voice; accurate to Version 1.11 as live Nov 1) ----------
SLIDES = [
  dict(q="Is it free? Do I have to download anything?",
       a="Free, and <b>nothing to download</b>. It works right in your browser at <b>mahjmatchmaker.com/find-your-match</b>. Tip: add it to your home screen so it's one tap away.",
       vis=[('ui', 'ui-title.png', None)]),
  dict(q="What's the difference between a partner brand and a <span style='white-space:nowrap'>non-partner</span> brand?",
       a="<b>Partner brands</b> are brands I'm affiliated with. I earn a small commission on anything you buy there with code <b>MAHJMATCH</b>, and you get a discount, usually <b>10% or more</b>.<p class=gap></p><b><span style='white-space:nowrap'>Non-partner</span> brands</b> simply aren't affiliates, but they're still listed. We separate them so you know where your code works.<p class=gap></p>We put partners first, and we'll keep bringing in <span style='white-space:nowrap'>non-partner</span> brands and cleaning up their catalogs.",
       vis=[], as0=(44, 50)),
  dict(q="How do I get the discount?",
       a="Use code <b>MAHJMATCH</b> at checkout on a partner brand's site. In <b>Shop by brand</b>, partners are listed first and labeled. If a brand has its own terms (like a minimum order), it's noted right there.",
       vis=[('code', None, None)]),
  dict(q="How did you match these?",
       a="By eye, by color. This all started with mockups I made for my own table. Turn on <b>Tiffany's picks</b> to see only mine. Everything else is sorted by color, so you can find your own favorites too.",
       vis=[('pair', 'assets/mats/gallery/bespoke-mahjong--double-sided-mat-double-the-fun-bespoke-x-corey-paige-holiday-love-mat-red-green.webp',
             'assets/tiles/holiday/dear-santa.jpg', 'Dear Santa · Anders Ruff  ♥  Holiday Love · Bespoke Mahjong')]),
  dict(q="Can I start with a mat I already own?",
       a="Yes! Tap <b>Start with a mat</b>, pick yours, and swipe tile sets on it. ♥ the ones you love, ✕ the rest, then add racks.",
       vis=[('ui', 'ui-doors.png', None), ('photo', 'assets/mats/holiday/hd/tartan-tidings-mahjong-mat.jpg', 'Tartan Tidings · Anders Ruff')]),
  dict(q="Does it show holiday mats?",
       a="Yes, holiday is here! Tap <b>Holiday</b> for Christmas, Hanukkah and snowy winter tile sets and mats, then add racks and see your whole table together. My holiday albums are on the site too.",
       vis=[('ui', 'ui-holiday-chips.png', None), ('photo', 'assets/mats/holiday/hd/ar-classic-very-merry-mahj.jpg', 'Classic Very Merry Mahj · Anders Ruff')]),
  dict(q="Can I save the ones I love?",
       a="Yes! Tap the <b>star</b> on any tile set, mat or rack and find it in <b>My stars</b>, top right. Right now they save on the device you're using. Sign-in is coming, so your stars can follow you everywhere.",
       vis=[('ui', 'ui-mystars-top.png', None)]),
  dict(q="Why don't I see my favorite brand?",
       a="We're still bringing in more brands, partner and non-partner. Want one we don't have yet? Scroll to the bottom of the tool and tap <b>Tell me here</b>. It's your tool!",
       vis=[('brands', ['Bougie Mahjong', 'Mahj &amp; Moon', 'Hutch &amp; Nook', 'Betty June &amp; Jeannette', 'Piper Chase Studios'], None),
            ('ui', 'ui-feedback-link.png', None)]),
]
N = len(SLIDES)

CSS = f"""
@font-face{{font-family:Cap;src:url({F}Caprasimo.ttf)}}
@font-face{{font-family:PF;font-style:italic;src:url({F}playfair-display-latin-600-italic.woff2)}}
@font-face{{font-family:Bit;font-weight:600;src:url({F}bitter-latin-600-normal.woff2)}}
@font-face{{font-family:Bit;font-weight:700;src:url({F}bitter-latin-700-normal.woff2)}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:var(--w);height:var(--h);overflow:hidden}}
body{{position:relative;font-family:Bit;font-weight:600;color:{DEEP};background:{PAPER}}}
.conf{{position:absolute;inset:0;z-index:0}}
.conf i{{position:absolute;border-radius:50%}}
.conf s{{position:absolute;text-decoration:none;font-style:normal;font-family:Bit;font-weight:700;line-height:1}}
.wrap{{position:absolute;left:64px;right:64px;top:var(--top);bottom:var(--bot);display:flex;flex-direction:column;gap:30px;z-index:1}}
.head{{display:flex;justify-content:space-between;align-items:center}}
.pill{{background:{DEEP};color:{BLUSH};font:700 26px Bit;letter-spacing:.16em;padding:12px 26px;border-radius:999px}}
.num{{font:700 26px Bit;letter-spacing:.12em;color:{ROSE}}}
.q{{position:relative;background:{DEEP};color:{PCREAM};font-family:Cap;font-size:var(--qs);line-height:1.12;padding:36px 44px 40px;border-radius:44px 44px 44px 10px;align-self:flex-start;max-width:100%}}
.q:after{{content:"";position:absolute;left:0;bottom:-26px;border-left:34px solid {DEEP};border-bottom:26px solid transparent}}
.a{{position:relative;background:#fff;border:4px solid {BLUSH};font-size:var(--as);line-height:1.36;padding:30px 40px 34px;border-radius:44px 44px 10px 44px;margin-left:70px;margin-top:8px;margin-bottom:36px}}
.a .gap{{height:.55em}}
.a b{{color:{HPINK};font-weight:700}}
.a .who{{position:absolute;right:-6px;bottom:-62px;display:flex;align-items:center;gap:10px;font:700 22px Bit;letter-spacing:.14em;color:{ROSE}}}
.a .who img{{width:46px;height:auto}}
.vis{{flex:1;min-height:0;display:flex;align-items:center;justify-content:center;gap:34px;margin-top:40px}}
.card{{background:#fff;border-radius:30px;padding:14px;box-shadow:0 10px 30px rgba(6,42,85,.16);display:flex;flex-direction:column;align-items:center;max-height:100%}}
.card img{{display:block;max-width:100%;max-height:100%;border-radius:20px;object-fit:contain;min-height:0}}
.lab{{font:700 19px Bit;letter-spacing:.12em;text-transform:uppercase;color:{ROSE};padding:12px 6px 4px;text-align:center}}
.foot{{display:flex;justify-content:center;align-items:center}}
.foot img{{height:40px}}
.code{{border:5px dashed {HPINK};background:{PCREAM};border-radius:34px;padding:34px 64px;text-align:center;transform:rotate(-3deg)}}
.code .k{{font:700 24px Bit;letter-spacing:.2em;color:{ROSE}}}
.code .c{{font-family:Cap;font-size:96px;color:{DEEP};line-height:1.1;margin:8px 0}}
.code .s{{font:600 26px Bit;color:{DEEP}}}
.pairbox{{position:relative;height:100%;aspect-ratio:1/1;max-width:100%}}
.pairbox .mat{{width:100%;height:100%;object-fit:cover;border-radius:26px;box-shadow:0 10px 30px rgba(6,42,85,.16)}}
.pairbox .tile{{position:absolute;right:-22px;bottom:-22px;width:46%;aspect-ratio:1/1;border-radius:50%;object-fit:cover;border:8px solid #fff;box-shadow:0 8px 24px rgba(6,42,85,.2)}}
.pairlab{{font:700 19px Bit;letter-spacing:.1em;text-transform:uppercase;color:{ROSE};text-align:center;margin-top:30px}}
.bcol{{display:flex;flex-direction:column;align-items:center;gap:22px;max-width:100%}}
.bl{{font:700 22px Bit;letter-spacing:.16em;color:{ROSE}}}
.bp{{display:flex;flex-wrap:wrap;justify-content:center;gap:12px}}
.bp span{{background:#fff;border:3px solid {BLUSH};border-radius:999px;padding:10px 22px;font:700 27px Bit;color:{DEEP}}}
.tilt1{{transform:rotate(-3deg)}} .tilt2{{transform:rotate(3deg)}}
"""

def confetti(w, h, seed, dark=False):
    rnd = random.Random(seed)
    cols = [HEART, BLUSH, NAVY, HPINK] if not dark else [HEART, BLUSH, '#ffffff', HPINK]
    out = []
    for i in range(46):
        # keep to the margins: left/right 0-60 px or top band / bottom band
        side = rnd.random()
        if side < .3: x, y = rnd.uniform(4, 56), rnd.uniform(20, h - 20)
        elif side < .6: x, y = rnd.uniform(w - 58, w - 6), rnd.uniform(20, h - 20)
        elif side < .8: x, y = rnd.uniform(20, w - 20), rnd.uniform(8, 60)
        else: x, y = rnd.uniform(20, w - 20), rnd.uniform(h - 58, h - 8)
        c = rnd.choice(cols)
        if rnd.random() < .22:
            out.append(f'<s style="left:{x:.0f}px;top:{y:.0f}px;color:{c};font-size:{rnd.randint(22,34)}px;transform:rotate({rnd.randint(-25,25)}deg)">♥</s>')
        else:
            d = rnd.randint(8, 18)
            out.append(f'<i style="left:{x:.0f}px;top:{y:.0f}px;width:{d}px;height:{d}px;background:{c};opacity:{rnd.uniform(.55,.95):.2f}"></i>')
    return '<div class="conf">' + ''.join(out) + '</div>'

def vis_html(vis):
    if not vis: return '<div style="flex:1"></div>'
    parts = []
    for i, v in enumerate(vis):
        kind = v[0]
        tilt = '' if len(vis) == 1 else (' tilt1' if i == 0 else ' tilt2')
        if kind == 'ui':
            asp = Image.open(os.path.join(UI, v[1])).size; asp = asp[0] / asp[1]
            if len(vis) == 1 and asp < 2.2:   # tall-ish screen crop: fill the visual height
                parts.append(f'<div class="card" style="height:100%"><img src="file://{UI}/{v[1]}" style="height:100%;width:auto;max-width:none"></div>')
            else:
                parts.append(f'<div class="card{tilt}" style="max-width:{"100%" if len(vis)==1 else "56%"}"><img src="file://{UI}/{v[1]}"></div>')
        elif kind == 'photo':
            parts.append(f'<div class="card{tilt}" style="max-width:40%"><img src="{P(v[1])}"><div class="lab">{v[2]}</div></div>')
        elif kind == 'code':
            parts.append('<div class="code"><div class="k">AT CHECKOUT · PARTNER BRANDS</div><div class="c">MAHJMATCH</div><div class="s">a discount, usually 10% or more</div></div>')
        elif kind == 'pair':
            parts.append(f'<div style="height:100%;display:flex;flex-direction:column;align-items:center;min-height:0"><div class="pairbox" style="flex:1;min-height:0"><img class="mat" src="{P(v[1])}"><img class="tile" src="{P(v[2])}"></div><div class="pairlab">{v[3]}</div></div>')
        elif kind == 'brands':
            parts.append('<div class="bcol"><div class="bl">JUST ADDED</div><div class="bp">' + ''.join(f'<span>{b}</span>' for b in v[1]) + '</div></div>')
    if vis and vis[0][0] == 'brands':
        return '<div class="vis" style="flex-direction:column;gap:40px">' + ''.join(parts) + '</div>'
    return '<div class="vis">' + ''.join(parts) + '</div>'

FIT_JS = """() => {
  const wrap=document.querySelector('.wrap'); const vis=document.querySelector('.vis');
  const r=document.documentElement; let as=parseFloat(getComputedStyle(r).getPropertyValue('--as')); let qs=parseFloat(getComputedStyle(r).getPropertyValue('--qs'));
  const need = () => vis ? vis.getBoundingClientRect().height < parseFloat(r.dataset.minvis) : wrap.scrollHeight > wrap.clientHeight+1;
  let n=0; while(need() && n<40){ as-=1; qs-=1.2; r.style.setProperty('--as',as+'px'); r.style.setProperty('--qs',qs+'px'); n++; }
  return {as, qs, vis: vis ? Math.round(vis.getBoundingClientRect().height) : null};
}"""

def page(body, w, h, top, bot, qs, as_, minvis, bg=PAPER):
    return (f'<!doctype html><html style="--w:{w}px;--h:{h}px;--top:{top}px;--bot:{bot}px;--qs:{qs}px;--as:{as_}px" data-minvis="{minvis}">'
            f'<head><meta charset="utf-8"><style>{CSS}</style></head><body style="background:{bg}">{body}</body></html>')

def q_slide(i, s, w, h, story=False):
    top, bot = (269, 384) if story else (120, 120)
    vis = vis_html(s['vis'])
    body = (confetti(w, h, 100 + i) +
            f'<div class="wrap"><div class="head"><span class="pill">ASK ME ANYTHING</span><span class="num">{i+1} / {N}</span></div>'
            f'<div class="q">{s["q"]}</div>'
            f'<div class="a">{s["a"]}<div class="who"><img src="{P("assets/brand/flame-heart.png")}">TIFFANY</div></div>'
            f'{vis}'
            f'<div class="foot"><img src="{P("assets/brand/mahjmatchmaker-wordmark-notag.png")}"></div></div>')
    qs = 62 if not story else 74
    as_ = s.get('as0', (38, 46))[1 if story else 0]
    minvis = s.get('minvis', (330, 340))[1 if story else 0]
    return page(body, w, h, top, bot, qs, as_, minvis)

def cover(w, h, story=False):
    top, bot = (120, 120) if not story else (269, 384)
    big = 150 if not story else 170
    body = (confetti(w, h, 7, dark=True) +
      f'<div class="wrap" style="align-items:center;justify-content:space-between;text-align:center;gap:0">'
      f'<span class="pill" style="background:{HPINK};color:#fff">FIND <span style="font-family:PF;font-style:italic;letter-spacing:.06em">YOUR</span> MAT-CH™ EDITION</span>'
      f'<div><div style="font-family:Cap;font-size:{big}px;line-height:.95;color:{PCREAM}">Ask me<br><span style="color:{HEART}">anything</span></div>'
      f'<div style="font:600 34px Bit;color:{BLUSH};margin-top:22px">Free? Partners? Holiday? Swipe for the answers →</div></div>'
      f'<div style="position:relative;width:{860 if not story else 900}px;height:{560 if not story else 700}px">'
      f'<img src="{P("assets/mats/holiday/hd/tartan-tidings-mahjong-mat.jpg")}" style="position:absolute;left:40px;top:10px;width:{470 if not story else 560}px;border-radius:26px;transform:rotate(-5deg);border:10px solid #fff">'
      f'<img src="{P("assets/tiles/holiday/dear-santa.jpg")}" style="position:absolute;right:30px;top:40px;width:{330 if not story else 380}px;border-radius:50%;border:10px solid #fff;transform:rotate(4deg)">'
      f'<img src="{P("assets/tiles/holiday/tinselle-emerald-3x3.jpg")}" style="position:absolute;right:{170 if not story else 190}px;bottom:0;width:{230 if not story else 270}px;border-radius:22px;border:8px solid #fff;transform:rotate(-3deg)">'
      f'</div>'
      f'<div style="font:700 21px Bit;letter-spacing:.12em;color:{BLUSH}">TARTAN TIDINGS + DEAR SANTA · ANDERS RUFF &nbsp;·&nbsp; TINSELLE (EMERALD GREEN) · VIRORA MAHJONG</div>'
      f'</div>')
    return page(body, w, h, top, bot, 60, 35, 0, bg=DEEP)

def endslide(w, h, story=False):
    top, bot = (120, 120) if not story else (269, 384)
    body = (confetti(w, h, 9) +
      f'<div class="wrap" style="align-items:center;justify-content:space-between;text-align:center;gap:0">'
      f'<span class="pill">YOUR TURN</span>'
      f'<div style="font-family:Cap;font-size:{96 if not story else 92}px;line-height:1.02;color:{DEEP};white-space:nowrap">Find <span style="font-family:PF;font-style:italic;font-size:.95em">Your</span> Mat-ch™</div>'
      f'<div style="font:600 36px Bit;line-height:1.35">Free, right in your browser:<br><b style="color:{HPINK}">mahjmatchmaker.com/find-your-match</b></div>'
      f'<div class="code" style="transform:rotate(-2deg);padding:24px 50px"><div class="s" style="font-size:30px">Use code</div><div class="c" style="font-size:78px">MAHJMATCH</div><div class="s" style="font-size:28px">at our partner brands</div></div>'
      f'<div style="font:600 32px Bit;line-height:1.35">Got a question I didn\'t answer?<br>Ask me in the comments!</div>'
      f'<div class="card" style="max-width:92%"><img src="file://{UI}/ui-feedback-link.png"><div class="lab">at the bottom of the tool</div></div>'
      f'<img src="{P("assets/brand/mahjmatchmaker-wordmark-notag.png")}" style="height:46px">'
      f'</div>')
    return page(body, w, h, top, bot, 60, 35, 0, bg=PCREAM)

def sticker_frame(w, h):
    body = (confetti(w, h, 11, dark=True) +
      f'<div class="wrap" style="top:269px;bottom:384px;align-items:center;justify-content:space-between;text-align:center;gap:0">'
      f'<span class="pill" style="background:{HPINK};color:#fff">ASK ME ANYTHING</span>'
      f'<div style="font-family:Cap;font-size:104px;line-height:1;color:{PCREAM}">What do you<br><span style="color:{HEART}">want to know?</span></div>'
      f'<div style="font:600 36px Bit;color:{BLUSH};line-height:1.35">Find <i style="font-family:PF">Your</i> Mat-ch™, holiday, brands, codes:<br>ask away and I\'ll answer in stories</div>'
      f'<div style="position:relative;width:900px;height:560px">'
      f'<img src="{P("assets/mats/holiday/hd/ar-classic-very-merry-mahj.jpg")}" style="position:absolute;left:150px;top:0;width:560px;border-radius:26px;border:10px solid #fff;transform:rotate(-3deg)">'
      f'<img src="{P("assets/tiles/holiday/dear-santa.jpg")}" style="position:absolute;right:40px;bottom:-10px;width:300px;border-radius:50%;border:10px solid #fff">'
      f'</div>'
      f'<div style="font:700 21px Bit;letter-spacing:.12em;color:{BLUSH}">CLASSIC VERY MERRY MAHJ + DEAR SANTA · ANDERS RUFF</div>'
      f'</div>')
    return page(body, w, h, 269, 384, 60, 35, 0, bg=DEEP)

def main():
    os.makedirs(OUT + '/feed', exist_ok=True); os.makedirs(OUT + '/story', exist_ok=True)
    jobs = [('feed/feed-01-cover', cover(1080, 1350), 1080, 1350),
            ('story/story-01-cover', cover(1080, 1920, True), 1080, 1920)]
    for i, s in enumerate(SLIDES):
        jobs.append((f'feed/feed-{i+2:02d}', q_slide(i, s, 1080, 1350), 1080, 1350))
        jobs.append((f'story/story-{i+2:02d}', q_slide(i, s, 1080, 1920, True), 1080, 1920))
    jobs.append((f'feed/feed-{N+2:02d}-end', endslide(1080, 1350), 1080, 1350))
    jobs.append((f'story/story-{N+2:02d}-end', endslide(1080, 1920, True), 1080, 1920))
    jobs.append((f'story/story-{N+3:02d}-question-sticker', sticker_frame(1080, 1920), 1080, 1920))
    tmp = os.path.join(OUT, '_tmp.html')
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--allow-file-access-from-files'])
        for name, htm, w, h in jobs:
            open(tmp, 'w').write(htm)
            pg = b.new_page(viewport={'width': w, 'height': h})
            pg.goto('file://' + tmp); pg.wait_for_load_state('networkidle'); pg.evaluate('document.fonts.ready')
            pg.wait_for_timeout(250)
            fit = pg.evaluate(FIT_JS)
            # overflow check: wrap content must fit
            ov = pg.evaluate("()=>{const w=document.querySelector('.wrap');return w.scrollHeight-w.clientHeight}")
            pg.screenshot(path=os.path.join(OUT, name + '.png'))
            Image.open(os.path.join(OUT, name + '.png')).convert('RGB').save(os.path.join(OUT, name + '.jpg'), quality=92)
            os.remove(os.path.join(OUT, name + '.png'))
            print(name, fit, 'OVERFLOW' if ov > 1 else 'ok')
            pg.close()
        b.close()
    os.remove(tmp)
    sheet()

def sheet():
    import glob
    fnt = ImageFont.truetype(os.path.join(R, 'scripts/social/tileprofile/fonts/Caprasimo.ttf'), 30)
    feed = sorted(glob.glob(OUT + '/feed/*.jpg')); story = sorted(glob.glob(OUT + '/story/*.jpg'))
    tw, th = 300, 375; sw, sh = 211, 375
    W = max(len(feed[:5]) * (tw + 14), 6 * (sw + 14)) + 14
    rows = [feed[:5], feed[5:], story[:6], story[6:]]
    H = 70 + 2 * (th + 14) + 60 + 2 * (sh + 14) + 14
    im = Image.new('RGB', (W, H), '#fbe3ea'); d = ImageDraw.Draw(im)
    d.text((14, 16), 'Ask Me Anything · feed 1080x1350 (10)', font=fnt, fill=DEEP)
    y = 70
    for r in rows[:2]:
        for k, f in enumerate(r):
            t = Image.open(f); t.thumbnail((tw, th)); im.paste(t, (14 + k * (tw + 14), y))
        y += th + 14
    d.text((14, y + 10), 'Stories 1080x1920 (11, last = question-sticker frame)', font=fnt, fill=DEEP); y += 60
    for r in rows[2:]:
        for k, f in enumerate(r):
            t = Image.open(f); t.thumbnail((sw, sh)); im.paste(t, (14 + k * (sw + 14), y))
        y += sh + 14
    im.save(OUT + '/ama-contact-sheet.jpg', quality=88)
    print('sheet', im.size)

if __name__ == '__main__':
    main()
