"""Deco (Lagoon) (Bam Bird Boutique) album page code block, FINAL (Tiffany's review round 1, saved Nov 8 6:19pm, + her 6:20-6:25pm
bring-ins placed by colour). Built the way Juniper was (site/livepatch/juniper-album-nov07/build_block.py): template = the LIVE Juniper
block (juniper-codeblock.html: same CSS, hero, FAQ + JSON-LD, Colors & racks guides, lightbox with the Nov 8 pinch fix, Pinterest script).
Cards = assets/cards/deco-lagoon (manifest order = her order; holiday cards = her last 3, own section #holiday-matches, numbered 01..).
Links: FYM 1.18 build (shop + rack links, brand pages) for catalog mats; spec 'url' for the Nov 8 adds not in FYM yet (Silk Mahjong
Crane Cloud, Lemondrop Sapphire Blooms + Floral Affair: product links, route none; Lemondrop swaps to her affiliate link when approved,
config/link-routes.json). Mahjong Register = plain product link + its 10% note (as Juniper). Tiles are in stock (bambirdboutique.com
deco-tile-set.js Nov 8: Lagoon variants available) -> "available now". No pronoun for Deco (not asked yet; brand guide s3).
Usage: python3 build_block.py <image sha> [fym index.html]   -> deco-lagoon-codeblock.html (images pinned @sha) + urls.txt"""
import json, sys, re, html as H, urllib.parse as U
R = '/home/claude/mahjmatchmaker-data/'; HERE = R + 'site/livepatch/deco-lagoon-album-nov08/'
SHA = sys.argv[1]
FYM = sys.argv[2] if len(sys.argv) > 2 else '/tmp/claude-0/-home-claude/05549d34-8fe3-5ca9-a6a5-308991cb9a78/scratchpad/fym/b118/index.html'
h = open(FYM).read(); i = h.index('const D=') + 8; D, _ = json.JSONDecoder().raw_decode(h[i:])
CDN = f'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@{SHA}/'
e = lambda s: H.escape(s, quote=True)
man = json.load(open(R + 'assets/cards/deco-lagoon/manifest.json'))['cards']
spec = {m['name']: m for m in json.load(open(R + 'scripts/albumcard/specs/deco-lagoon_nov07.json'))['mats']}
PARTNERS = set(json.load(open(R + 'builder/fym_flags/nonpartner_allow.json'))['partners'])
RN = {v['n']: v for v in D['racks'].values()}
RN.setdefault('Bam Bird Boutique Olive', RN['Bam Bird Boutique Olive Green Wood']); RN.setdefault('Peace Love Mahjong Acrylic Burl', RN['Peace Love Mahjong Acrylic Burlwood'])
TILE_URL = D['tiles']['www.bambirdboutique.com/deco-tile-set']['u']
SET = 'Deco (Lagoon)'
def plain(u):
    p = U.urlparse(u); q = U.parse_qs(p.query)
    return f'{p.scheme}://{p.netloc}' + q['redirect'][0] if '/discount/' in p.path and 'redirect' in q else u
def brandpg(m):
    p = U.urlparse((m or {}).get('dc') or '').path
    return p if p.endswith('-discount-code') else None
def rack(n):
    v = RN.get(n)
    if not v: print('NO RACK LINK', n); return e(n)
    return f'<a href="{e(v["u"])}" target="_blank" rel="sponsored noopener">{e(n)}</a>'
def figure(n, c, hol):
    s = spec[c['mat']]; m = D['mats'].get(c.get('fym') or '') if c.get('fym') else None
    brand, mat, retired = c['brand'], c['mat'], c['retired_mat']
    if not m and not s.get('url'): raise SystemExit(f'NO LINK for {mat}')
    pg = (brandpg(m) if m else s.get('dc')) if brand in PARTNERS else None
    by = f'<a href="{pg}">{e(brand)}</a>' if pg else e(brand)
    ret = '<span class="mm3-ret">Retired</span>' if retired else ''
    label = mat if mat.lower().endswith(' mat') else mat + ' Mat'
    u = m['u'] if m else s['url']
    if brand == 'Mahjong Register': u = plain(u)
    btn = f'<a class="mm3-btn" href="{e(u)}" target="_blank" rel="sponsored noopener">Shop the {e(label)}</a>'
    if brand == 'Lemondrop Mahjong Co': code = '<span class="mm3-code" style="color:#8a8a8a">No code for Lemondrop Mahjong Co yet</span>'
    elif brand not in PARTNERS: code = f'<span class="mm3-code" style="color:#8a8a8a">No code for {e(brand)}</span>'
    elif brand == 'Mahjong Register': code = '<span class="mm3-code">10% off at Mahjong Register with MAHJMATCH (excludes racks and other brands\' products)</span>'
    else: code = '<span class="mm3-code">code MAHJMATCH</span>'
    take = ('<div class="mm3-take"><p>Pair mat: Bam Bird Boutique made the Deco Dragon mats to go with the Deco tiles.</p></div>'
            if mat.startswith('Deco Dragon') or mat == 'Deco Neoprene' else '')
    cap = 'Match the tiles: ' + ' · '.join(rack(x) for x in c['racks'])
    if c['mat_racks']: cap += '<br>Match the mat: ' + ' · '.join(rack(x) for x in c['mat_racks'])
    alt = f'Bam Bird Boutique Deco Lagoon mahjong tiles with {brand} {mat} {"holiday " if hol else ""}mahjong mat'
    cls = 'mm3-c mm3-hc' if hol else 'mm3-c'
    return (f'<figure class="{cls}"><div class="mm3-im"><img src="{CDN}assets/cards/deco-lagoon/{c["file"]}" data-lb="" alt="{e(alt)}" loading="lazy" width="750" height="938">'
            f'<a class="mm3-pin" href="#" target="_blank" rel="noopener" aria-label="Save to Pinterest">Save</a></div><figcaption>'
            f'<span class="mm3-n">{n:02d}</span><h3>{SET} + {e(mat)}</h3><span class="mm3-by">Mat by {by}{ret}</span>{take}'
            f'<div class="mm3-l">{btn}{code}</div><div class="mm3-rk" style="margin-top:8px;font-size:.82em;line-height:1.55">{cap}</div></figcaption></figure>')
main = [c for c in man if not c['holiday']]; hol = [c for c in man if c['holiday']]
assert [c['order'] for c in main] == list(range(1, len(main) + 1)) and len(hol) == 3
figs = ''.join(figure(n, c, False) for n, c in enumerate(main, 1))
hfigs = ''.join(figure(n, c, True) for n, c in enumerate(hol, 1))
nb = len({c['brand'] for c in man})
assert [c['mat'] for c in man[:3]] == ['Deco Dragon (Mulberry)', 'Reba', 'Viola'], [c['mat'] for c in man[:3]]
top = ("My top mat picks for Bam Bird Boutique's Deco (Lagoon) tiles are the Deco Dragon mat in Mulberry by Bam Bird Boutique, "
       'and Reba and Viola by Britt Mills.')
tpl = open(R + 'site/livepatch/juniper-album-nov07/juniper-codeblock.html').read()
css = tpl[tpl.index('</style>') + 8:tpl.index('<div class="mm3" id="juniper-album">')]  # drop Juniper's own launch-pill style block
lb = tpl[tpl.index('<div class="mm3-lb"'):]
HOLCSS = open(R + 'site/livepatch/missed-album-picks-nov07/holcss.html').read().strip()
CC = CDN + 'assets/colorcards/deco-lagoon/00-deco-lagoon-mahjong-tiles-'
BG = ('<style id="mmdecobg">.mm3-launch{display:inline-block;background:#0a4a56;color:#fff;font-size:12px;font-weight:700;letter-spacing:.12em;'
      'text-transform:uppercase;padding:4px 12px;border-radius:12px;margin:0 0 10px}</style>')
body = (
 f'<div class="mm3" id="deco-lagoon-album"><header class="mm3-hero mm3-hero-2"><div class="mm3-hero-img"><img src="{CDN}assets/covers/albums/00-deco-lagoon-mahjong-tiles-cover.jpg" data-lb="" alt="Bam Bird Boutique Deco Lagoon mahjong tiles" fetchpriority="high"></div>'
 '<div class="mm3-hero-t"><p class="mm3-kicker">Bam Bird Boutique</p><span class="mm3-launch">Available now</span><h1>Deco (Lagoon) Mahjong Tile Matches</h1><div class="mm3-intro">'
 "<p>Bam Bird Boutique's Deco tiles in Lagoon: deep teal backs with a gold-foil deco palm, and ivory faces in mulberry, rose, gold, teal and navy, "
 'matched to mats from across my favorite brands. Deco (Lagoon) is available now. My top picks come first. Tap any photo to see it bigger, and use code MAHJMATCH to save at our partner brands.</p></div>'
 f'<p class="mm3-cta"><a class="mm3-btn mm3-btn-l" href="{e(TILE_URL)}" target="_blank" rel="sponsored noopener">Shop Deco (Lagoon) at Bam Bird Boutique</a>'
 '<span>Save with <a href="/bam-bird-boutique-discount-code">Bam Bird Boutique discount code</a> <strong>MAHJMATCH</strong></span></p></div></header>'
 '<section class="mm3-faq" style="max-width:860px;margin:28px auto 8px;padding:0 20px;text-align:center"><h2>What mats match Deco (Lagoon) mahjong tiles?</h2>'
 f'<p>{e(top)} Below are {len(man)} Deco (Lagoon) mat matches from {nb} brands, and counting, including {len(hol)} holiday matches, each with rack picks and a link to shop.</p></section>'
 '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": "What mats match Deco (Lagoon) mahjong tiles?",
   "acceptedAnswer": {"@type": "Answer", "text": top + " Deco (Lagoon) by Bam Bird Boutique is available now. Save at partner brands with code MAHJMATCH."}}]}) + '</script>'
 '<section class="mm3-guides"><h2>Colors &amp; racks</h2><div class="mm3-gg">'
 f'<figure class="mm3-g"><picture><source media="(max-width: 640px)" srcset="{CC}color-guide-mobile.jpg"><img src="{CC}tile-edit-moodboard.jpg" data-lb="" '
 'alt="Bam Bird Boutique Deco Lagoon mahjong tiles color card: deep teal backs with a gold-foil palm, ivory faces in mulberry, rose, gold, teal, navy and periwinkle, rack and mat matches" loading="lazy"></picture>'
 '<figcaption><strong>The Tile Edit</strong><p>Deep Lagoon teal backs with a gold-foil deco palm on every tile, ivory faces, and mulberry, rose, gold, teal, navy and periwinkle on the faces. '
 "Bam Bird Boutique's own Lagoon Wood and Mulberry Wood racks pick up the backs and the mulberry crak frames.</p></figcaption></figure>"
 '<style>.mm3-gg>.mm3-g:has(img[src*="tile-edit-moodboard"]){grid-column:1/-1}.mm3-gg>.mm3-g:has(img[src*="tile-edit-moodboard"]) figcaption{max-width:860px;margin:0 auto;padding:20px 26px 12px;font-size:16px}</style>'
 f'<figure class="mm3-g mm3-fav2"><img src="{CDN}assets/social/deco-lagoon-launch/deco-lagoon-favorite-tiles.jpg" data-lb="" alt="My favorite Deco Lagoon mahjong tiles: the teal and mulberry dragons, the gold-winged crane bird bam, the peacock feather East wind, the gold and navy irises and the rose lion joker" loading="lazy">'
 f'<figcaption><a class="mm3-btn" href="{e(TILE_URL)}" target="_blank" rel="noopener">Shop Deco Tiles</a></figcaption></figure>'
 '<style>.mm3-gg>.mm3-g.mm3-fav2{grid-column:1/-1;max-width:540px;width:100%;margin:6px auto 0;background:none}.mm3-fav2 img{border-radius:14px}.mm3-fav2 figcaption{text-align:center;padding:14px 0 4px}</style>'
 f'<figure class="mm3-g mm3-wheel"><img src="{CDN}assets/colorwheels/deco-lagoon-color-wheel.jpg" data-lb="" alt="Deco Lagoon mahjong tiles on the color wheel: deep teal, gold, mulberry, rose, navy and periwinkle" loading="lazy">'
 '<figcaption><strong>The colors on the wheel</strong><p>Mulberry and rose sit straight across the wheel from deep teal. That is why a teal mat with a berry frame or berry flowers makes Deco (Lagoon) pop, and why an all-teal mat reads tone on tone, with the faces bringing the berry.</p>'
 '<p>Gold sits between them and ties both sides together, so a touch of gold on the mat always looks at home next to the gold-foil palms.</p></figcaption></figure>'
 '<style>.mm3-gg>.mm3-g.mm3-wheel{grid-column:1/-1;max-width:760px;width:100%;margin:6px auto 0}</style>'
 '</div></section>\n'
 f'<section><h2>My Deco (Lagoon) matches</h2><p class="mm3-sub">My top picks come first. Tap any photo to see it bigger.</p><div class="mm3-grid">{figs}</div></section>'
 f'{HOLCSS}<section class="mm3-hol" id="holiday-matches"><h2>Holiday matches for Deco (Lagoon)</h2><p class="mm3-sub">Christmas mats for Deco (Lagoon), with rack picks. '
 'See more holiday matches on the <a href="/holiday-mahjong-matches">Holiday Matches</a> page.</p>'
 f'<div class="mm3-grid">{hfigs}</div></section>'
 '<p class="mm3-foot">Deco (Lagoon) is available now at Bam Bird Boutique. Save with code <strong>MAHJMATCH</strong>. Browse more <a href="/mahjong-tile-matches">tile match albums</a> or see our <a href="/mahjong-discount-codes">mahjong discount codes</a>.</p></div>')
out = BG + css + body + lb
bad = [m.start() for m in re.finditer(r'(?i)juniper', out)]
assert not bad, out[bad[0] - 80:bad[0] + 80]
open(HERE + 'deco-lagoon-codeblock.html', 'w').write(out)
urls = sorted(set(re.findall(r'https://cdn\.jsdelivr\.net/gh/[^"\s)]+', out)))
open(HERE + 'urls.txt', 'w').write('\n'.join(urls) + '\n')
print(len(re.findall(r'<figure class="mm3-c', out)), 'cards (', len(main), 'main +', len(hol), 'holiday ),', nb, 'brands,', len(urls), 'cdn urls,', len(out), 'bytes')
