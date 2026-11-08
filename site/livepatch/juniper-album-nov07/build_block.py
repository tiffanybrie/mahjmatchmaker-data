"""Juniper (Oh My Mahjong) album page code block, FINAL (Tiffany's order Nov 7 11:21pm, 42 cards).
Template = the LIVE Papaya Spritz album block (papaya_live_template.html, curled Nov 7 from /papaya-spritz-mahjong-tile-matches:
same CSS, hero, FAQ + JSON-LD, Colors & racks guides with colour card + favourite faces, lightbox + Pinterest script).
Card captions = Brownstone Bloom style ("Match the tiles / Match the mat"); holiday cards go in their own holiday section
(id="holiday-matches", mm3-hol, holcss from site/livepatch/missed-album-picks-nov07/holcss.html, numbering 01.. inside it, her
relative order kept). Links = the FYM 1.18 build (shop + rack auto-apply links, brand pages); Mahjong Register uses the plain product
link (MAHJMATCH not set up there: cart test Nov 7). Pre-launch copy: Juniper tiles + Lotus Cove launch Wed Nov 11 at OMM.
No 'Tiffany's take' blurbs (her own words only; the review 'why' notes were written to her, not for the page). Lotus Cove gets the
Papaya-style 'Pair mat' note.
Usage: python3 build_block.py <sha> [fym index.html]   -> juniper-codeblock.html (images pinned @sha)"""
import json, sys, re, html as H, urllib.parse as U
R = '/home/claude/mahjmatchmaker-data/'; HERE = R + 'site/livepatch/juniper-album-nov07/'
SHA = sys.argv[1]
FYM = sys.argv[2] if len(sys.argv) > 2 else '/tmp/claude-0/-home-claude/05549d34-8fe3-5ca9-a6a5-308991cb9a78/scratchpad/fym/b118/index.html'
h = open(FYM).read(); i = h.index('const D=') + 8; D, _ = json.JSONDecoder().raw_decode(h[i:])
CDN = f'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@{SHA}/'
e = lambda s: H.escape(s, quote=True)
man = json.load(open(R + 'assets/cards/juniper-final/manifest.json'))['cards']
keys = json.load(open(R + 'config/picks/juniper-fym-m-2026-11-07.json'))['m']
assert len(man) == len(keys) == 42
PARTNERS = set(json.load(open(R + 'builder/fym_flags/nonpartner_allow.json'))['partners'])
RN = {v['n']: v for v in D['racks'].values()}
RN.setdefault('Miss Mahjong Scalloped Iridescent Opal', RN['Miss Mahjong Iridescent Opal Scalloped'])
TILE_URL = 'https://ohmymahjong.com/discount/MAHJMATCH?redirect=%2Fproducts%2Fjuniper-mahjong-tiles'
def plain(u):  # discount auto-apply link -> the product link it redirects to (Mahjong Register: code not set up)
    p = U.urlparse(u); q = U.parse_qs(p.query)
    return f'{p.scheme}://{p.netloc}' + q['redirect'][0] if '/discount/' in p.path and 'redirect' in q else u
def brandpg(m):
    dc = m.get('dc') or ''
    p = U.urlparse(dc).path
    return p if p.endswith('-discount-code') else None
def rack(n):
    v = RN.get(n)
    if not v: print('NO RACK LINK', n); return e(n)
    return f'<a href="{e(v["u"])}" target="_blank" rel="sponsored noopener">{e(n)}</a>'
def figure(n, c, k, hol):
    m = D['mats'][k['key']]; brand = c['brand']; mat = c['mat']; retired = c['retired_mat']
    pg = brandpg(m) if brand in PARTNERS else None
    by = f'<a href="{pg}">{e(brand)}</a>' if pg else e(brand)
    ret = '<span class="mm3-ret">Retired</span>' if retired else ''
    retn = '<p class="mm3-retn">This mat is retired. Look for it secondhand in mahjong buy/sell groups.</p>' if retired else ''
    label = mat if mat.lower().endswith(' mat') else mat + ' Mat'
    if retired:
        btn = f'<a class="mm3-btn" href="{e(m["u"])}" target="_blank" rel="sponsored noopener">Shop Current OMM Mats</a>'
    else:
        u = plain(m['u']) if brand == 'Mahjong Register' else m['u']
        btn = f'<a class="mm3-btn" href="{e(u)}" target="_blank" rel="sponsored noopener">Shop the {e(label)}</a>'
    if brand not in PARTNERS: code = f'<span class="mm3-code" style="color:#8a8a8a">No code for {e(brand)}</span>'
    elif brand == 'Mahjong Register': code = '<span class="mm3-code" style="color:#8a8a8a">No code at Mahjong Register right now</span>'
    else: code = '<span class="mm3-code">code MAHJMATCH</span>'
    take = ('<div class="mm3-take"><p>Pair mat: Oh My Mahjong made Lotus Cove to go with Juniper. Both launch Wednesday, November 11.</p></div>'
            if mat == 'Lotus Cove' else '')
    cap = 'Match the tiles: ' + ' · '.join(rack(x) for x in c['racks'])
    if c['mat_racks']: cap += '<br>Match the mat: ' + ' · '.join(rack(x) for x in c['mat_racks'])
    alt = f'Oh My Mahjong Juniper mahjong tiles with {brand} {mat} {"holiday " if hol else ""}mahjong mat'
    cls = 'mm3-c mm3-hc' if hol else 'mm3-c'
    return (f'<figure class="{cls}"><div class="mm3-im"><img src="{CDN}assets/cards/juniper-final/{c["file"]}" data-lb="" alt="{e(alt)}" loading="lazy" width="750" height="938">'
            f'<a class="mm3-pin" href="#" target="_blank" rel="noopener" aria-label="Save to Pinterest">Save</a></div><figcaption>'
            f'<span class="mm3-n">{n:02d}</span><h3>Juniper + {e(mat)}</h3><span class="mm3-by">Mat by {by}{ret}</span>{retn}{take}'
            f'<div class="mm3-l">{btn}{code}</div><div class="mm3-rk" style="margin-top:8px;font-size:.82em;line-height:1.55">{cap}</div></figcaption></figure>')
main = [(c, k) for c, k in zip(man, keys) if not c['holiday']]
hol = [(c, k) for c, k in zip(man, keys) if c['holiday']]
assert [c['order'] for c, _ in main] == list(range(1, 38)) and len(hol) == 5  # her order: holiday cards are her last 5
figs = ''.join(figure(n, c, k, False) for n, (c, k) in enumerate(main, 1))
hfigs = ''.join(figure(n, c, k, True) for n, (c, k) in enumerate(hol, 1))
nb = len({c['brand'] for c in man})
top = 'My top mat picks for Juniper are Palm Royale by Mahj Tile Haus, Flora Belle by Anders Ruff and Lotus Cove by Oh My Mahjong.'
assert [c['mat'] for c in man[:3]] == ['Palm Royale', 'Flora Belle', 'Lotus Cove']
tpl = open(HERE + 'papaya_live_template.html').read()
css = tpl[:tpl.index('<div class="mm3" id="papaya-spritz-album">')]
lb = tpl[tpl.index('<div class="mm3-lb"'):]
HOLCSS = open(R + 'site/livepatch/missed-album-picks-nov07/holcss.html').read().strip()
CC = CDN + 'assets/colorcards/juniper/00-juniper-mahjong-tiles-'
BG = ('<style id="mmjunbg">section:has(.mm3) .section-background{background:#fff!important}section:has(.mm3){background:#fff}'
      'section:has(.mm3) .mm3 h1,section:has(.mm3) .mm3 h2{color:var(--ink,#1f3a6b)!important}section:has(.mm3) .mm3-cta a:not(.mm3-btn){color:var(--ink,#1f3a6b)!important}'
      '.mm3-launch{display:inline-block;background:#225d36;color:#fff;font-size:12px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;padding:4px 12px;border-radius:12px;margin:0 0 10px}</style>')
body = (
 f'<div class="mm3" id="juniper-album"><header class="mm3-hero mm3-hero-2"><div class="mm3-hero-img"><img src="{CDN}assets/covers/albums/00-juniper-mahjong-tiles-cover.jpg" data-lb="" alt="Oh My Mahjong Juniper mahjong tiles" fetchpriority="high"></div>'
 '<div class="mm3-hero-t"><p class="mm3-kicker">Oh My Mahjong</p><span class="mm3-launch">Launches Wed 11/11</span><h1>Juniper Mahjong Tile Matches</h1><div class="mm3-intro">'
 "<p>Oh My Mahjong's Juniper, with her Forest Green Jade backs and chartreuse and teal layers, matched to mats from across my favorite brands. "
 'Juniper launches Wednesday, November 11, so you can plan her table now. My top picks come first. Tap any photo to see it bigger, and use code MAHJMATCH to save at our partner brands.</p></div>'
 f'<p class="mm3-cta"><a class="mm3-btn mm3-btn-l" href="{e(TILE_URL)}" target="_blank" rel="sponsored noopener">See Juniper at Oh My Mahjong</a>'
 '<span>Save with <a href="/oh-my-mahjong-discount-code">Oh My Mahjong discount code</a> <strong>MAHJMATCH</strong></span></p></div></header>'
 '<section class="mm3-faq" style="max-width:860px;margin:28px auto 8px;padding:0 20px;text-align:center"><h2>What mats match Juniper mahjong tiles?</h2>'
 f'<p>{e(top)} Below are {len(man)} Juniper mat matches from {nb} brands, and counting, including {len(hol)} holiday matches, each with rack picks and a link to shop.</p></section>'
 '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": "What mats match Juniper mahjong tiles?",
   "acceptedAnswer": {"@type": "Answer", "text": top + " Juniper by Oh My Mahjong launches November 11. Save at partner brands with code MAHJMATCH."}}]}) + '</script>'
 '<section class="mm3-guides"><h2>Colors &amp; racks</h2><div class="mm3-gg">'
 f'<figure class="mm3-g"><picture><source media="(max-width: 640px)" srcset="{CC}color-guide-mobile.jpg"><img src="{CC}tile-edit-moodboard.jpg" data-lb="" '
 'alt="Oh My Mahjong Juniper mahjong tiles color card: Forest Green Jade backs with chartreuse and teal layers, hot pink, coral and mint faces, rack and mat matches" loading="lazy"></picture>'
 '<figcaption><strong>The Tile Edit</strong><p>Forest Green Jade backs with a jade-look stone pattern, chartreuse and teal layers, and hot pink, coral, mint and gold faces. '
 "Oh My Mahjong's own Hot Pink and Agate racks pick up her pink faces and her green stone backs.</p></figcaption></figure>"
 '<style>.mm3-gg>.mm3-g:has(img[src*="tile-edit-moodboard"]){grid-column:1/-1}.mm3-gg>.mm3-g:has(img[src*="tile-edit-moodboard"]) figcaption{max-width:860px;margin:0 auto;padding:20px 26px 12px;font-size:16px}</style>'
 f'<figure class="mm3-g mm3-fav2"><img src="{CDN}assets/social/juniper-launch/juniper-favorite-tiles.jpg" data-lb="" alt="My favorite Juniper mahjong tiles: the emerald dragon and her pink twin, the peacock bird bam, the hot pink lotus by a green pagoda and the 7 bam" loading="lazy">'
 f'<figcaption><a class="mm3-btn" href="{e(TILE_URL)}" target="_blank" rel="noopener">See Juniper Tiles</a></figcaption></figure>'
 '<style>.mm3-gg>.mm3-g.mm3-fav2{grid-column:1/-1;max-width:540px;width:100%;margin:6px auto 0;background:none}.mm3-fav2 img{border-radius:14px}.mm3-fav2 figcaption{text-align:center;padding:14px 0 4px}</style>'
 f'<figure class="mm3-g mm3-wheel"><img src="{CDN}assets/colorwheels/juniper-color-wheel.jpg" data-lb="" alt="Juniper mahjong tiles on the color wheel: Forest Green Jade, chartreuse, teal, hot pink, coral, mint and gold" loading="lazy">'
 '<figcaption><strong>Her colors on the wheel</strong><p>Pink sits straight across the wheel from her greens. That is why a pink-and-green mat makes Juniper pop, and why an all-green mat reads tone on tone, with the faces bringing the pink.</p>'
 '<p>Light colors sit toward the center and dark ones toward the rim, so Forest Green Jade sits out near the edge, while her hot pink and coral sit closer in.</p></figcaption></figure>'
 '<style>.mm3-gg>.mm3-g.mm3-wheel{grid-column:1/-1;max-width:760px;width:100%;margin:6px auto 0}</style>'
 '</div></section>\n'
 f'<section><h2>My Juniper matches</h2><p class="mm3-sub">My top picks come first. Tap any photo to see it bigger.</p><div class="mm3-grid">{figs}</div></section>'
 f'{HOLCSS}<section class="mm3-hol" id="holiday-matches"><h2>Holiday matches for Juniper</h2><p class="mm3-sub">Christmas mats for Juniper, with rack picks. '
 'See more holiday matches on the <a href="/holiday-mahjong-matches">Holiday Matches</a> page.</p>'
 f'<div class="mm3-grid">{hfigs}</div></section>'
 '<p class="mm3-foot">Juniper launches November 11 at Oh My Mahjong. Save with code <strong>MAHJMATCH</strong>. Browse more <a href="/mahjong-tile-matches">tile match albums</a> or see our <a href="/mahjong-discount-codes">mahjong discount codes</a>.</p></div>')
out = BG + css + body + lb
assert 'papaya' not in out.lower().replace('papaya-spritz-album', ''), [m.start() for m in re.finditer('apaya', out)][:5]
open(HERE + 'juniper-codeblock.html', 'w').write(out)
urls = sorted(set(re.findall(r'https://cdn\.jsdelivr\.net/gh/[^"\s)]+', out)))
open(HERE + 'urls.txt', 'w').write('\n'.join(urls) + '\n')
print(len(re.findall(r'<figure class="mm3-c', out)), 'cards (', len(main), 'main +', len(hol), 'holiday ),', nb, 'brands,', len(urls), 'cdn urls,', len(out), 'bytes')
