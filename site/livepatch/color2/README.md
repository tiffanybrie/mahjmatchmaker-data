# Site colors: rainbow order + separate Orange and Yellow (staged Oct 19, overnight). NOT live.
Tiffany (Oct 19, 2:39am): rainbow order, and stop lumping Yellow & Orange (browns/tortoise were bleeding in). Live edits need her Yes on the Ready to Ship item "Site colors: rainbow order + separate Yellow/Orange pages".

## Order everywhere
Red, Orange, Yellow, Green, Blue, Purple, Pink, Brown, Ivory, Holiday, Natural Patterns, Masculine (then Request / All albums).
- Black & White and Multicolor are MAT colors (the tagger); no tile-set albums use them, so no site chips for them.
- Holiday moved from first (it was the red, seasonal-highlight chip) to after Ivory, per the order she gave. It keeps its red fill. If she wants it first for the holiday season, move it back.

## Change (Oct 19, 3:49am, Tiffany): ONE continuous rainbow grid
- The "All Albums by Color" block on /mahjong-tile-matches and the home page is now ONE grid of covers in rainbow order, with no color headings and no breaks inside it. Nantucket (the only red) leads instead of sitting alone in a row.
- Order: Red, Orange, Yellow, Green, Blue, Purple, Pink, Brown, Ivory, Natural Patterns, Holiday (matches the chips). Albums cross-listed in Natural Patterns appear once, at their main color.
- The chips above still jump to each color page (Orange and Yellow pages as staged).
- The subtitle is now "Every tile set I've matched, in rainbow order by tile back color. Tap a color above to see just that color."
- Tested on the live page HTML: all 43 albums kept, idempotent, no sideways scroll at 390 or 1280. Before/after: rainbow_flat_before_after_1280.jpg, _390.jpg.

## Filing (tile back color + tone, config/tile-tones.json)
- Orange: Papaya Spritz, Solara, Sunset, Sierra (earthy cognac)
- Yellow: Pippa, Sorbet, Sunday Tile Set
- Brown: + Classic Tortoise (stays in Natural Patterns too)
- Nothing else was in the Yellow & Orange group.

## How to apply (in the Squarespace editor, CM6 dispatch like doc 59)
`transform.js` defines `window.MMCOLOR2` (idempotent string transforms on the editor source):
1. /mahjong-tile-matches, block-yui_3_17_2_1_1791149521478_3720: `MMCOLOR2.mtm(src)` (chips + grouped sections).
2. Home, block-yui_3_17_2_1_1791134152790_5194: `MMCOLOR2.home(src)` (color tiles grid → 6 per row; grouped sections).
3. Each existing color page (pink, red, blue, green, purple, ivory, neutral, masculine): the code block's bottom "Shop by color" row: `MMCOLOR2.colorPage(src)`.
4. /brown-mahjong-tile-matches: replace its code block with `brown-page.html` (adds Classic Tortoise; chips reordered).
5. New pages (duplicate /yellow-orange-mahjong-tile-matches, then replace its code block; set settings via the API AFTER the code-block save):
   - /orange-mahjong-tile-matches ← `orange-page.html`. Title "Orange Mahjong Tile Match Albums". SEO title "Orange Mahjong Tile Match Albums | Mat & Rack Pairings". SEO description "Citrus, papaya and sunset orange mahjong tile sets, from clean brights to warm cognac, each with an album of matching mats and racks."
   - /yellow-mahjong-tile-matches ← `yellow-page.html`. Title "Yellow Mahjong Tile Match Albums". SEO title "Yellow Mahjong Tile Match Albums | Mat & Rack Pairings". SEO description "Butter, sunshine and golden yellow mahjong tile sets, each with an album of matching mats and racks."
6. /yellow-orange-mahjong-tile-matches (keep the URL; it has links and ranking) ← `yellow-orange-page.html`: two sections, Orange and Yellow, linking the new pages. No chips point to it any more.
7. Verify with curl: chip order, sections, card counts. Then add the new pages to the sitemap/indexing requests.
All images are existing covers (already pinned and warm; re-warmed Oct 19).
