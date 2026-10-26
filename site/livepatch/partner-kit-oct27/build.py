#!/usr/bin/env python3
"""Build the hidden /partner-kit page block (Squarespace code block).

Each partner brand gets a section with its Find Your Mat-ch story (9:16) and
feed post (4:5), served from jsDelivr at a pinned commit. No discount code
anywhere (partner rule). Usage:
  python3 build.py <commit-sha>   -> page-block.html
Brands + files come from manifest.json (slug, brand, story, post), files under
assets/social/partner-kit/final/.
"""
import json, sys, html, pathlib

HERE = pathlib.Path(__file__).parent
sha = sys.argv[1]
base = f"https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@{sha}/assets/social/partner-kit/final/"
items = json.load(open(HERE / "manifest.json"))

css = """
<style>
#pk{--ink:#1d2a44;--rose:#c8325f;--line:#ecdfe3;--cream:#fbf8f6;font-family:Bitter,Georgia,serif;color:var(--ink);max-width:1080px;margin:0 auto;padding:8px 16px 48px}
#pk h1{font-family:Caprasimo,Georgia,serif;font-weight:400;font-size:clamp(30px,6vw,46px);margin:0 0 8px;text-align:center}
#pk h1 em{font-family:"Playfair Display",Georgia,serif;font-style:italic}
#pk .lede{text-align:center;max-width:60ch;margin:0 auto 18px;line-height:1.55}
#pk .jump{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:0 0 28px}
#pk .jump a{border:1px solid var(--line);border-radius:999px;padding:6px 12px;text-decoration:none;color:var(--ink);font-size:14px;background:#fff}
#pk section{border-top:1px solid var(--line);padding:28px 0;scroll-margin-top:90px}
#pk h2{font-family:Caprasimo,Georgia,serif;font-weight:400;font-size:28px;margin:0 0 14px;text-align:center}
#pk .two{display:grid;grid-template-columns:minmax(0,9fr) minmax(0,10fr);gap:18px;align-items:start}
@media(max-width:700px){#pk .two{grid-template-columns:1fr}}
#pk figure{margin:0;display:grid;gap:8px}
#pk figure img{width:100%;border-radius:12px;border:1px solid var(--line);background:#fff}
#pk .dl{display:inline-block;text-align:center;background:var(--rose);color:#fff;border-radius:999px;padding:10px 16px;text-decoration:none;font-weight:700}
#pk .tip{font-size:14px;text-align:center;opacity:.8;margin-top:6px}
</style>
"""

out = [css, '<div id="pk">',
       '<h1>Find <em>Your</em> Mat-ch&trade; is here</h1>',
       '<p class="lede">Thank you for being part of the launch! Here is a story and a feed post made with your pieces in the tool. '
       'Save the one you like and share it if you\'d like. Tag <b>@mahjmatchmaker</b> and we\'ll reshare you right back.</p>',
       '<nav class="jump">' + ''.join(f'<a href="#{i["slug"]}">{html.escape(i["brand"])}</a>' for i in items) + '</nav>']
for i in items:
    b = html.escape(i["brand"])
    s, p = base + i["story"], base + i["post"]
    out.append(f'''<section id="{i["slug"]}"><h2>{b}</h2><div class="two">
<figure><img src="{s}" alt="{b} Find Your Mat-ch story graphic" loading="lazy"><a class="dl" href="{s}" download target="_blank" rel="noopener">Save the story (9:16)</a></figure>
<figure><img src="{p}" alt="{b} Find Your Mat-ch feed post" loading="lazy"><a class="dl" href="{p}" download target="_blank" rel="noopener">Save the post (4:5)</a></figure>
</div><p class="tip">On a phone: open the image, then press and hold to save it to Photos.</p></section>''')
out.append('</div>')
(HERE / "page-block.html").write_text("\n".join(out))
print("wrote page-block.html with", len(items), "brands")
