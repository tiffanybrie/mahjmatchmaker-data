# Brand-page boxes (Oct 21, Tiffany 10:20pm + correction 10:31pm)

Not live yet: Chrome was not reachable. Publish steps are in docs/DESK.md.

## What she asked for (and only this)
1. Right profile photo (chambray) on every brand page box.
2. Bird & Bamboo pages stop promoting wood/stained racks (rule doc 57, Oct 15; Clear Stain dropped too).
Her original intro line ("Oh My Mahjong Mahji Mentor instructor...") and all other copy are UNCHANGED.

## Audit (live curl of 38 *-discount-code pages)
32 pages carry the box, all with the old `Tiffany+Headshot.png`. Six pages have no box: i-love-mahj, mahjong-co, wren-mats, mahjong-register, lets-be-besties, mahjong-discount-codes. /bird-and-bamboo-discount-code-2 is an unlinked duplicate of the B&B page (fixed identically).

## 1. All 32 pages (`pages/<slug>.before.html` / `.after.html`, regenerate with `build.py <live dir>`)
- Headshot -> `https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@efde3ef88b70a8797d97bdcdb8409faafe6bd62c/assets/brand/headshot/tiffany-chambray-headshot-square.jpg`, `object-position:50% 50%` (same pin as About).
- Headline never italic: append `.mmbg h1,.mmbg h2,.mmbg h3{font-style:normal}` after `.mmbg .me span{display:block;font-size:.88em;opacity:.8}` in the page's code block (the italic comes from the theme h2 style). The rack-colors page uses `.mmrc`, so add the same line with `.mmrc`.

## 2. B&B discount pages (`bb/<slug>.replacements.json`, exact old->new pairs; applies to the code block and its FAQ JSON-LD)
- Intro: "...from Harbor Blue and Jade to Hot Pink."
- Most-used: "French Blue, Hot Pink, Dark Navy and Kelly Green are some of my most-used shades."
- FAQ (visible + JSON-LD): "Neutrals like White, Cream and True Black go with the most sets. French Blue and Hot Pink are my favorite pops of color. Want a wood look? I pair real-wood racks like Peace Love Mahjong Oak or Bam Bird Boutique Walnut."
- Kept: rack color library link, Willow / Heritage 2.0 / Solara links, samples tip, verified code line.

## 3. /bird-and-bamboo-rack-colors (`bb/bird-and-bamboo-rack-colors.before/after.html` = the `.mmrc` region of the code block)
- 11 tiles removed (102 -> 91): Weathered Oak x2, Almond x2, Tudor, Provincial, Red Mahogany, Dark Walnut, Clear x2, plus the stain "White" (a paint White already sits in Neutrals, so it is dropped, not moved).
- Wood Stains section replaced by the "Wood looks" note (PLM Oak, Bam Bird Walnut, M&M Scalloped Beechwood); "Wood Stains" chip removed.
- H1 "Every Paint Color"; "94 paint colors and wood stains" -> "dozens of paint colors" (intro + FAQ); pick-a-color FAQ says neutral White/Cream/True Black.
- Squarespace page SEO fields (title, og/twitter title) still say "All 94 Paint Colors & Stains": change to "Bird & Bamboo Rack Colors: Every Paint Color" in page settings.

## Left as is, flag to Tiffany
- Hero/card text on the B&B discount pages still says "94 colors and stains" (hero dek, "20-inch Painted Wooden Racks" card, intro "94 paint colors and stains"). The Oct 18 draft did not cover it; she asked to keep the 94 paint colors wording. Her call.
- Oh My Mahjong page JSON-LD Person image is still the old headshot.

QA: `python3 qa.py` (passes): headshot swapped, nothing else in the box changed, B&B has no Weathered/Clear Stain and keeps its links, rack-colors has no wood names or "94 paint".
