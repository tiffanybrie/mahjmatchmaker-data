# Brand-page "Why I love" boxes (Oct 21, 10:20pm, Tiffany yes)

Not live yet: Chrome was not reachable, so nothing is published (see docs/DESK.md).

## Audit (live, cache-busted curl of all 38 *-discount-code pages)
- 32 pages carry the Tiffany box (class `me`). ALL 32 use the OLD `Tiffany+Headshot.png` (squarespace-cdn). None used the chambray headshot.
- All 31 non-OMM boxes carry the intro "Oh My Mahjong Mahji Mentor instructor and the matchmaker behind Mahj Matchmaker."
- Headline italics come from the Squarespace theme's h2 style, not the box HTML. Fix = `.mmbg h1,.mmbg h2,.mmbg h3{font-style:normal}` appended after the `.mmbg .me span{...}` rule in each page's code block.
- Pages without a box (no change): i-love-mahj, mahjong-co, wren-mats, mahjong-register, lets-be-besties, mahjong-discount-codes.
- Duplicate page /bird-and-bamboo-discount-code-2 (same title and content; all links point to the non-2 page). Fixed identically; Tiffany may want it deleted/redirected.

## Changes (per page, in `pages/<slug>.before.html` / `.after.html`)
1. Headshot -> `https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@efde3ef88b70a8797d97bdcdb8409faafe6bd62c/assets/brand/headshot/tiffany-chambray-headshot-square.jpg` (same pin as About), `object-position:50% 50%` (square is pre-cropped).
2. Intro -> "Mahjong instructor and the matchmaker behind Mahj Matchmaker." (all but Oh My Mahjong's own page, where the credential is the brand's own and the body text uses it).
3. Headline italic: CSS line above (page-level, once per code block).
4. Bird & Bamboo copy tightened (both B&B pages); verified code line, links, "94 paint colors", samples tip untouched.

## Apply
Per page: in the page's code block apply the same three string replacements (img src+style, intro span, CSS line; B&B also the two paragraphs), diff vs live, save, exit, cache-busted curl: new headshot URL, no `<em>` in h2, new copy. `build.py <src dir>` regenerates before/after from live HTML; `qa.py` checks headshot, intro, links unchanged, code line, B&B copy.

## Not rewritten (listed only)
No copy rewrites beyond B&B. Other boxes were scanned for repeated phrases: nothing obvious automatically, but a human read of Anders Ruff (177 words), Middle & Main (202), Mahj Mood (197), Lets Mahj On (186), Tigre de Tartan (186) would be worthwhile for wordiness.
Schema.org Person JSON-LD on the Oh My Mahjong page still points at the old Tiffany+Headshot.png (SEO image; left alone).
