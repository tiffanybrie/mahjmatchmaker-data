#!/usr/bin/env python3
"""Homepage fix, Oct 21 (Tiffany 9:17 / 9:18 / 9:19). Builds the staged code blocks.

Inputs (committed in source/):
  before_block-yui_3_17_2_1_1791134152790_5194.html  live code of the big homepage block, Oct 21
  ticker_logos.json                                    partner logo ticker list, from /mahjong-discount-codes
Outputs:
  block-yui_3_17_2_1_1791134152790_5194.html   replacement code for the existing block
  new-block-mahjmatch-callout.html             NEW code block: MAHJMATCH callout + partner logo ticker
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'source')
BID = 'block-yui_3_17_2_1_1791134152790_5194'
LOGO_COMMIT = '604c093c0a854a0954b9b26e8bca90e5967c9a05'
# Oct 21 12:22 (Tiffany's homepage review): new Raven board card + How It Works step 3 image
ASSET_COMMIT = '9b3b68fe8ca3ab3c045a8e0f5563c8ca9045069b'
GH = f'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@{ASSET_COMMIT}/'
RAVEN_CARD = GH + 'assets/blog/night-of-the-raven/night-of-the-raven-shop-the-look-v7-card-1200x900.jpg'
STEP3_IMG = GH + 'assets/site/home/how-it-works-3-new-matches-first.jpg'
STEP3_SEC = '69b2303d5670f85709f47c87'
CDN = f'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@{LOGO_COMMIT}/assets/brands/ticker/'
SQ = 'https://images.squarespace-cdn.com/content/v1/69b1d01289d0f8016ee3d508/'


def div_end(s, start):
    depth = 0
    for m in re.finditer(r'<div\b|</div>', s[start:]):
        depth += 1 if m.group(0) == '<div' else -1
        if depth == 0:
            return start + m.end()
    raise ValueError('unbalanced div')


def section_span(s, marker):
    """Span of the top-level <section>...</section> that contains marker."""
    i = s.index(marker)
    a = s.rfind('<section>', 0, i)
    b = s.index('</section>', i) + len('</section>')
    return a, b


code = open(os.path.join(SRC, f'before_{BID}.html')).read()

# 1. Remove the whole "All Albums by Color" listing (div.mmalb-home, 71 album cards).
a = code.index('<div class="mmalb-home">')
code = code[:a] + code[div_end(code, a):]
assert 'All Albums by Color' not in code and 'class="mmalb-c"' not in code, 'album listing still present'

# 2. Colour swatches jump to the colour section on the Mahjong Matches page.
#    Holiday keeps its own page (the #color-holiday anchor there is only a link to it).
code = code.replace(
    '<p class="mmh-sub">Start with the colors you love and see every tile set I&rsquo;ve matched in that color.</p>',
    '<p class="mmh-sub">Start with the colors you love. Tap a color to jump to every tile set I&rsquo;ve matched in it.</p>')
n = 0
for slug in ['pink', 'red', 'blue', 'green', 'purple', 'yellow-orange', 'brown', 'ivory', 'neutral']:
    old = f'class="mmh-col" href="/{slug}-mahjong-tile-matches"'
    assert code.count(old) == 1, slug
    code = code.replace(old, f'class="mmh-col" href="/mahjong-tile-matches#color-{slug}"')
    n += 1
assert n == 9

# 3. Blog section: replace "Shop the Guides" and move it right under New Tile Match Albums.
POSTS = [  # (slug, kicker, title, teaser, image)
    ('halloween-mahjong-table', 'Halloween &middot; Styled table',
     'Night of the Raven: A Moody Halloween Mahjong Table',
     'Black-on-black tiles with pops of plum, styled on the Mahjong Row &amp; Co. Mocha Bloom Dark mat. Every piece is linked so you can shop the look.',
     '1792245124698-WBMYUEUDAFT8OPYOS12P/night-of-the-raven-shop-the-look-v3.jpg'),
    ('holiday-mahjong-table', 'Holiday &middot; Styled table',
     'A Holiday Mahjong Table Without a Christmas Mat',
     'The Polo Club mat and Heritage tiles, dressed up for the season.',
     '1792308112276-WDBXL8IIHKF1IOLI3TK2/holiday-mahjong-table-polo-club-shop-the-look.jpg'),
    ('christmas-mahjong-sets', 'Holiday guide',
     'Christmas Mahjong Tiles, Mats &amp; Racks',
     'The Christmas tiles, holiday mats and festive racks I love this season.',
     '1791261921630-DFKP8FGGFGLZT5P3BR6K/christmas-mahjong-tiles-virora-tinselle-ruby-red.jpg'),
    ('mahjong-buying-guide', 'Start here',
     'Mahjong Buying Guide: Tiles, Mat &amp; Racks That Go Together',
     'What to pick first, and how to make the pieces match.',
     '1791261975371-4LID6YHS1SWKS421STC7/mahjong-buying-guide-heritage-tiles-darjeeling-mat.jpg'),
    ('most-versatile-mahjong-tiles', 'Versatile picks',
     'My Most Versatile Tile Sets',
     'Wood, pearl, tortoise and stone sets that go with almost any mat.',
     '1773283757402-YTI0N7WW1EJ357M9IAKM/BamBird_New_Products_April_2025-138.webp'),
]
MORE = [  # quick links to the rest of the blog
    ('most-versatile-mahjong-mats', 'Most versatile mats'),
    ('my-favorite-mahjong-racks', 'Favorite racks'),
    ('my-favorite-pink-mahjong-tiles', 'Pink tiles'),
    ('my-favorite-blue-mahjong-tiles', 'Blue tiles'),
    ('my-favorite-green-mahjong-tiles', 'Green tiles'),
    ('my-favorite-yellow-orange-mahjong-tiles', 'Yellow &amp; orange tiles'),
    ('mahjong-tile-set-details-to-know', 'Tile set details to know'),
    ('best-mahjong-sets-for-men', 'Sets for men'),
    ('best-mahjong-sets-for-kids', 'Sets for kids'),
    # 'Spring & summer table' chip removed (Tiffany, Oct 21 12:22)
]
BLOG_CSS = (
    '<style>'
    '#mmhome .mmbl-feat{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);background:var(--cr);border-radius:16px;overflow:hidden;text-decoration:none!important;color:var(--n)!important;margin:0 0 22px;box-shadow:0 3px 14px rgba(0,0,0,.06)}'
    '#mmhome .mmbl-feat img{width:100%;height:auto;aspect-ratio:4/3;object-fit:contain;background:#faf3ea;display:block;align-self:center}'
    '#mmhome .mmbl-ft{padding:30px 32px;display:flex;flex-direction:column;justify-content:center;gap:10px}'
    '#mmhome .mmbl-k{display:block;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--p);font-weight:700}'
    '#mmhome .mmbl-now{display:inline-block;align-self:flex-start;background:var(--p);color:#fff;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;padding:4px 11px;border-radius:999px}'
    '#mmhome .mmbl-feat b{font-size:clamp(1.25rem,2.2vw,1.65rem);line-height:1.2}'
    '#mmhome .mmbl-feat p{margin:0;opacity:.85;line-height:1.5}'
    '#mmhome .mmbl-go{color:var(--p);font-weight:700;font-size:15px}'
    '#mmhome .mmbl-g{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:20px}'
    '#mmhome .mmbl-c{display:flex;flex-direction:column;background:var(--cr);border-radius:14px;overflow:hidden;text-decoration:none!important;color:var(--n)!important}'
    '#mmhome .mmbl-c img{width:100%;aspect-ratio:4/3;object-fit:cover;display:block;transition:transform .2s}'
    '#mmhome .mmbl-c:hover img,#mmhome .mmbl-feat:hover img{transform:scale(1.02)}'
    '#mmhome .mmbl-c .mmbl-k{padding:12px 14px 0}'
    '#mmhome .mmbl-c b{padding:4px 14px 4px;font-size:16px;line-height:1.3}'
    '#mmhome .mmbl-c p{margin:0;padding:0 14px 8px;font-size:14px;line-height:1.45;opacity:.85}'
    '#mmhome .mmbl-c .mmbl-go{padding:0 14px 14px;margin-top:auto;font-size:14px}'
    '#mmhome .mmbl-more{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;margin:24px auto 0;max-width:900px}'
    '#mmhome .mmbl-more span{width:100%;text-align:center;font-weight:700;font-size:14px;margin-bottom:2px}'
    '#mmhome .mmbl-more a{display:inline-block;border:1.5px solid #e7c3d0;border-radius:999px;padding:6px 13px;font-size:14px;font-weight:600;color:var(--n)!important;text-decoration:none!important;background:#fff}'
    '#mmhome .mmbl-more a:hover{border-color:var(--p);color:var(--p)!important}'
    '@media(max-width:900px){#mmhome .mmbl-g{grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}#mmhome .mmbl-feat{grid-template-columns:1fr}#mmhome .mmbl-feat img{height:auto;aspect-ratio:4/3}#mmhome .mmbl-ft{padding:18px 18px 20px}}'
    '@media(max-width:520px){#mmhome .mmbl-g{gap:12px}#mmhome .mmbl-c b{font-size:15px;padding:4px 12px}#mmhome .mmbl-c .mmbl-k{padding:10px 12px 0;font-size:11px}#mmhome .mmbl-c p{display:none}#mmhome .mmbl-c .mmbl-go{padding:2px 12px 12px;font-size:13px}#mmhome .mmbl-more a{font-size:13px;padding:5px 11px}}'
    '</style>')


def img(path, alt, eager=False):
    return f'<img src="{SQ}{path}?format=750w" alt="{alt}"{"" if eager else " loading=\"lazy\""}>'


f = POSTS[0]
blog = ['<section class="mmbl">', BLOG_CSS,
        '<h2>From the Blog</h2>',
        '<p class="mmh-sub">Styled tables, buying guides and my favorite picks, with every piece linked so you can shop the look.</p>',
        f'<a class="mmbl-feat" href="/blog/{f[0]}"><img src="{RAVEN_CARD}" alt="Night of the Raven Halloween mahjong table mood board: Mocha Bloom Dark mat, terracotta marble tiles, translucent plum rack, raven dice dish, cordless lamp, black lace and deep plum tablecloths" loading="lazy" width="1200" height="900">'
        f'<span class="mmbl-ft"><span class="mmbl-now">Featured now</span><span class="mmbl-k">{f[1]}</span><b>{f[2]}</b><p>{f[3]}</p><span class="mmbl-go">Read the post &rarr;</span></span></a>',
        '<div class="mmbl-g">']
for slug, k, t, teaser, im in POSTS[1:]:
    alt = re.sub(r'&amp;', '&amp;', t)
    blog.append(f'<a class="mmbl-c" href="/blog/{slug}">{img(im, alt)}<span class="mmbl-k">{k}</span><b>{t}</b><p>{teaser}</p><span class="mmbl-go">Read the post &rarr;</span></a>')
blog.append('</div>')
blog.append('<p class="mmbl-more"><span>More on the blog</span>' + ''.join(f'<a href="/blog/{s}">{t}</a>' for s, t in MORE) + '</p>')
blog.append('<p class="mmh-cta"><a class="mmh-btn alt" href="/blog">Read the blog &rarr;</a></p>')
blog.append('</section>')
blog = ''.join(blog)

ga, gb = section_span(code, '<h2>Shop the Guides</h2>')
code = code[:ga] + code[gb:]
anchor = '<!--holplug-->'
assert code.count(anchor) == 1
code = code.replace(anchor, blog + anchor)

# 4. Shop by Brand: drop its sprite logo ticker; the new MAHJMATCH callout block carries
#    the full partner ticker right under the hero, so the page shows one ticker, not two.
i = code.index('Plus more partner brands')
pa = code.rfind('<p class="mmh-sub"', 0, i)
ta = code.index('<div class="mmh-tick">', i)
code = code[:pa] + code[div_end(code, ta):]
assert 'mmh-tick"' not in code

# 5. Shop by Brand line: "10% or more" (Tiffany Oct 21 12:22); keep the number with its words on one line.
old = 'the <strong>MAHJMATCH</strong> code that saves you 10 to 20%.'
assert code.count(old) == 1
code = code.replace(old, 'the <strong>MAHJMATCH</strong> code that saves you <span style="white-space:nowrap">10% or more</span>.')
old = '<p class="mmh-sub">My partner brands, each'
assert code.count(old) == 1
code = code.replace(old, '<p class="mmh-sub" style="text-wrap:balance">My partner brands, each')

# 6. How It Works step 3 ("3. Get New Matches First") had no image. Add one in the empty left half,
#    same size/shape as step 1's image block on desktop (cols 2-13, 522x382 at 1280), and on top of
#    the step on phones like steps 1 and 2. Scoped to the step 3 section.
S3 = f'section[data-section-id="{STEP3_SEC}"]'
H = f'html body {S3} .fluid-engine '
step3 = (
    '<style>'
    f'{S3} .mmstep3{{position:relative;z-index:1;align-self:center;min-width:0}}'
    f'{S3} .mmstep3 img{{display:block;width:100%;height:auto;aspect-ratio:522/382;object-fit:cover}}'
    f'@media(min-width:768px){{{S3} .fluid-engine .mmstep3{{grid-area:2/2/16/13}}}}'
    f'@media(max-width:767px){{{S3} .fluid-engine .mmstep3{{grid-column:2/10;grid-row:1/3;margin-bottom:28px}}'
    f'{S3} .mmstep3 img{{aspect-ratio:343/409}}'
    f'{H}.fe-block-7a4922a2f12fa35d4063.fe-block{{grid-row:3/5!important}}'
    f'{H}.fe-block-30d6f603ced4992fce62.fe-block{{grid-row:5/11!important}}'
    f'{H}.fe-block-yui_3_17_2_1_1791134152790_4757.fe-block{{grid-row-start:11!important;grid-row-end:15!important}}'
    f'{H}.fe-block-yui_3_17_2_1_1773285173485_84366.fe-block{{grid-row-start:15!important;grid-row-end:17!important}}'
    f'{H}.fe-block-yui_3_17_2_1_1773297234466_4930.fe-block{{grid-row-start:17!important;grid-row-end:19!important}}}}'
    '</style>'
    '<script>(function(){function f(){var g=document.querySelector(\'' + S3.replace('"', '\\"') + ' .fluid-engine\');'
    'if(!g||g.querySelector(".mmstep3"))return;var d=document.createElement("div");d.className="mmstep3";'
    f'd.innerHTML=\'<img src="{STEP3_IMG}" alt="New mahjong tile match albums: Coquette, Seabreeze, Talulah, Osler and Smith" loading="lazy" width="1200" height="880">\';'
    'g.insertBefore(d,g.firstChild)}if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",f);else f();})();</script>'
)
code = code + step3

open(os.path.join(HERE, f'{BID}.html'), 'w').write(code)

# ---------------------------------------------------------------- new callout block
logos = json.load(open(os.path.join(SRC, 'ticker_logos.json')))


def clean(t):
    return t.replace('&amp;rsquo;', '&rsquo;')


css_logo = ''.join(
    f'#mmcode .mmcb-tk a.{l["k"]}{{background-image:url({CDN}{l["k"]}.{"png" if l["k"] == "b26" else "webp"});aspect-ratio:{l["ar"]}}}'
    for l in logos)


def row(dup):
    out = []
    for l in logos:
        t = clean(l['title'])
        extra = ' tabindex="-1" aria-hidden="true"' if dup else ''
        out.append(f'<a class="{l["k"]}{" dup" if dup else ""}" href="{l["href"]}" title="{t}" aria-label="{t}"{extra}></a>')
    return ''.join(out)


callout = (
    '<div class="mmcb-mark"></div>'
    '<style>'
    '.fe-block:has(.mmcb-mark){display:none!important}'
    '#mmcode{--n:#1f3a6b;--p:#c2547a;--cr:#fbf5ef;color:var(--n);background:#fff;width:100%;max-width:100%;position:relative;z-index:1;overflow:hidden;box-sizing:border-box}'
    '#mmcode *{box-sizing:border-box}'
    '#mmcode .mmcb-in{max-width:1180px;margin:0 auto;padding:40px 20px 0}'
    '#mmcode .mmcb-bar{display:flex;align-items:center;justify-content:center;flex-wrap:wrap;gap:12px 22px;background:var(--cr);border:2px dashed #e3b3c4;border-radius:18px;padding:18px 24px;text-align:center;text-decoration:none!important;color:var(--n)!important;transition:border-color .2s}'
    '#mmcode .mmcb-bar:hover{border-color:var(--p)}'
    '#mmcode .mmcb-t{font-size:clamp(1.05rem,1.9vw,1.3rem);font-weight:700;line-height:1.35;margin:0}'
    '#mmcode .mmcb-code{display:inline-block;background:var(--n);color:#fff;letter-spacing:.12em;padding:3px 12px;border-radius:8px;margin:0 2px;white-space:nowrap}'
    '#mmcode .mmcb-btn{display:inline-block;background:var(--p);color:#fff;font-weight:700;font-size:15px;padding:10px 20px;border-radius:999px;white-space:nowrap}'
    '#mmcode .mmcb-tk{overflow:hidden;padding:22px 0 6px;-webkit-mask-image:linear-gradient(90deg,transparent,#000 5%,#000 95%,transparent);mask-image:linear-gradient(90deg,transparent,#000 5%,#000 95%,transparent)}'
    '#mmcode .mmcb-tt{display:flex;align-items:center;width:max-content;animation:mmcbscroll 65s linear infinite}'
    '#mmcode .mmcb-tk:hover .mmcb-tt,#mmcode .mmcb-tk:focus-within .mmcb-tt{animation-play-state:paused}'
    '#mmcode .mmcb-tk a{flex:0 0 auto;display:block;margin:0 32px;height:60px;border:0!important;box-shadow:none!important;text-decoration:none!important;background-size:contain;background-position:center;background-repeat:no-repeat}'
    '@keyframes mmcbscroll{to{transform:translateX(-50%)}}'
    '#mmcode+#mmhome .mmh-in{padding-top:28px}#mmcode+#mmhome{padding-top:0}'
    '@media(max-width:767px){#mmcode .mmcb-in{padding:28px 16px 0}#mmcode .mmcb-bar{padding:16px 14px;border-radius:14px}#mmcode .mmcb-btn{font-size:14px;padding:9px 18px}#mmcode .mmcb-tk{padding:16px 0 4px}#mmcode .mmcb-tk a{height:42px;margin:0 20px}}'
    '@media(prefers-reduced-motion:reduce){#mmcode .mmcb-tt{animation:none;flex-wrap:wrap;justify-content:center;width:auto;row-gap:14px}#mmcode .mmcb-tt .dup{display:none}#mmcode .mmcb-tk{-webkit-mask-image:none;mask-image:none}}'
    + css_logo +
    '</style>'
    '<div id="mmcode"><div class="mmcb-in">'
    '<a class="mmcb-bar" href="/mahjong-discount-codes">'
    '<p class="mmcb-t">Use code <span class="mmcb-code">MAHJMATCH</span> to save at 30+ partner brands</p>'
    '<span class="mmcb-btn">Meet our partner brands &rarr;</span></a>'
    '</div>'
    '<div class="mmcb-tk" role="region" aria-label="Mahj Matchmaker partner brands"><div class="mmcb-tt">'
    + row(False) + row(True) +
    '</div></div></div>'
    # Place it right under the hero: before #mmhome (block 5194 moves #mmhome under the first
    # page section while the page parses), or after the first page section if #mmhome is missing.
    '<script>(function(){function mv(){var c=document.getElementById("mmcode");if(!c)return;'
    'var h=document.getElementById("mmhome");if(h&&h.parentNode&&!h.contains(c)){h.parentNode.insertBefore(c,h);return}'
    'var s=document.querySelector("article section.page-section, main section.page-section");if(s&&s.parentNode)s.parentNode.insertBefore(c,s.nextSibling)}'
    'if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",mv);else mv();})();</script>'
)
open(os.path.join(HERE, 'new-block-mahjmatch-callout.html'), 'w').write(callout)
# What is live is ONE code block: the callout pasted at the very top of block 5194 (Oct 21 morning).
open(os.path.join(HERE, f'live-paste_{BID}.html'), 'w').write(callout + '\n' + code)
print('ok', len(code), len(callout))
