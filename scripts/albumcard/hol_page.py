"""Build (1) the Holiday Mahjong Matches page code block and (2) the holiday section HTML for each tile album.
Usage: python3 hol_page.py <payload.json> <manifest.json> <outdir>"""
import json, sys, os, re, html
R = '/home/claude/mahjmatchmaker-data/'
P = json.load(open(sys.argv[1])); man = json.load(open(sys.argv[2])); out = sys.argv[3]; os.makedirs(out, exist_ok=True)
e = lambda s: html.escape(s, quote=True)
css = open('/tmp/mm3_style.css').read()
lb = re.search(r'<div class="mm3-lb".*?</script>', open('/tmp/nant.html').read(), re.S).group(0)
albums = {a['slug']: a for a in json.load(open(R + 'work/albums.json'))}
N = len(man); NM = len({x['mat'] for x in man}); NT = len({x['tile'] for x in man}); NB = len({x['brand'] for x in man})

HOLCSS = """<style>
.mm3-hol{margin-top:56px;padding:34px 0 10px;border-top:3px dashed #e9c77b}
.mm3-hol h2{color:#a3192e}
.mm3-hstar{display:inline-block;width:fit-content;align-self:flex-start;background:#1f5a3c;color:#fff;font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;padding:2px 9px;border-radius:10px;margin:0 0 6px}
#holiday-matches{background:#fdf0e6;color:#1f3a6b;border-radius:24px;padding:40px 28px 30px}
#holiday-matches h1{color:#a3192e!important}
#holiday-matches h2{color:#a3192e}
#holiday-matches p,#holiday-matches .mm3-sub{color:#1f3a6b}
@media(max-width:700px){#holiday-matches{padding:28px 14px;border-radius:16px}}
.mmhol-nav{display:flex;flex-wrap:wrap;justify-content:center;gap:10px;margin:18px auto 8px;max-width:900px}
.mmhol-nav a{padding:7px 16px;border-radius:999px;border:2px solid #a3192e;color:#1f3a6b!important;text-decoration:none!important;font-weight:700;font-size:14px;background:#fff}
.mmhol-nav a.g{border-color:#1f5a3c}
.mmhol-stats{display:flex;flex-wrap:wrap;justify-content:center;gap:12px;margin:18px 0 6px}
.mmhol-stats span{background:#fbf1e3;border:2px solid #e9c77b;border-radius:14px;padding:10px 18px;font-weight:700;color:#a3192e}
.mmhol-stats b{font-size:1.5em;display:block;line-height:1.1}
.mmhol-alb{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
.mmhol-alb a{display:block;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,.07);text-decoration:none!important;color:#1f3a6b!important;text-align:center}
.mmhol-alb img{width:100%;aspect-ratio:4/5;object-fit:cover;display:block}
.mmhol-alb b{display:block;padding:10px 8px 2px}.mmhol-alb small{display:block;padding:0 8px 12px;opacity:.8}
@media(max-width:900px){.mmhol-alb{grid-template-columns:repeat(2,minmax(0,1fr))}}
</style>"""

def renum(figs, start=1):
    o = []
    for i, f in enumerate(figs):
        o.append(f.replace('<span class="mm3-n">00</span>', f'<span class="mm3-n">{start+i:02d}</span>', 1))
    return o

# ---- (1) album sections
sections = {}
for k, v in P.items():
    if k.startswith('_new'): continue
    t = v['tile']
    sec = (f'<section class="mm3-hol" id="holiday"><h2>Holiday matches for {e(t)}</h2>'
           f'<p class="mm3-sub">Christmas, Hanukkah and winter mats for {e(t)}, with rack picks. My favorites come first. '
           f'See every holiday match on the <a href="/holiday-mahjong-matches">Holiday Matches</a> page.</p>'
           f'<div class="mm3-grid">{"".join(renum(v["figs"], 1))}</div></section>')
    sections[k] = sec
json.dump({'css': HOLCSS, 'sections': sections}, open(os.path.join(out, 'album_sections.json'), 'w'))

# ---- (2) holiday page
ORDER = ['dear-santa', 'rackin-rudolph', 'holly-jolly-red', 'holly-jolly-green', 'holly-jolly-pink', 'tinselle-emerald', 'tinselle-ruby',
         'nivalee-blue', 'nutcracker-ballet', 'december-1994', 'cmc-apres-ski', 'sunday', 'hummingbird', 'nature-walk', 'sunday-blues']
MAKER = {}
for x in man: MAKER.setdefault(x['tile'], x['tileName'])
newsecs = []; nav = []
for t in ORDER:
    v = P.get('_new:' + t)
    if not v: continue
    name = v['tile']; anchor = t
    nav.append(f'<a href="#{anchor}">{e(name)}</a>')
    newsecs.append(f'<section class="mm3-hol" id="{anchor}" style="margin-top:40px"><h2>{e(name)} holiday matches</h2>'
                   f'<p class="mm3-sub">{len(v["figs"])} mat {"match" if len(v["figs"])==1 else "matches"}, with rack picks. My favorites come first.</p>'
                   f'<div class="mm3-grid">{"".join(renum(v["figs"]))}</div></section>')
alb_cards = []
for k, v in sorted(((k, v) for k, v in P.items() if not k.startswith('_new')), key=lambda kv: -len(kv[1]['figs'])):
    a = albums.get(k)
    if not a: continue
    alb_cards.append(f'<a href="/{k}#holiday"><img src="{a["cover"]}?format=500w" alt="{e(a["tile"])} mahjong tiles" loading="lazy">'
                     f'<b>{e(a["tile"])}</b><small>{len(v["figs"])} holiday {"match" if len(v["figs"])==1 else "matches"}</small></a>')
page = f"""<style>{css}</style>{HOLCSS}
<div class="mm3" id="holiday-matches"><header class="mm3-hero" style="text-align:center;max-width:900px;margin:0 auto">
<p class="mm3-kicker" style="color:#a3192e">Holiday 2026</p><h1>Holiday Mahjong Tile &amp; Mat Matches</h1>
<div class="mm3-intro"><p>Every Christmas, Hanukkah and winter mahjong mat I&rsquo;ve matched, paired with tile sets and racks. Start with your tile set below, or jump to the new holiday tile sets.</p></div>
<div class="mmhol-stats"><span><b>{N}</b>holiday matches</span><span><b>{NM}</b>mats</span><span><b>{NT}</b>tile sets</span><span><b>{NB}</b>brands</span></div>
<p class="mm3-sub">Use code <strong>MAHJMATCH</strong> to save at most brands. See every <a href="/mahjong-discount-codes">mahjong discount code</a>.</p>
<nav class="mmhol-nav" aria-label="Holiday tile sets">{''.join(nav)}<a class="g" href="#your-tiles">Tiles you already own</a></nav></header>
<section id="your-tiles" style="margin-top:36px"><h2>Holiday matches for the tiles you already own</h2>
<p class="mm3-sub">Tap your tile set to see its holiday mats, right in its album.</p><div class="mmhol-alb">{''.join(alb_cards)}</div></section>
{''.join(newsecs)}
<p class="mm3-foot">Looking for more? Browse every <a href="/mahjong-tile-matches">tile match album</a> or read my <a href="/blog">holiday guides</a>.</p>
{lb}</div>"""
open(os.path.join(out, 'holiday_page.html'), 'w').write(page)
print('album sections', len(sections), 'page KB', len(page) // 1024, 'new sections', len(newsecs))
