# Card swaps: retired tagline + banned B&B woods (staged, NOT live)

Built Oct 18 from the site QA (work/qa/site-qa-2026-10-18.md, #9). Needs Tiffany's approval before any live edit.

## What changed (all in place, commit c3ae3a3)
- **Logo tab:** 695 Claude-built cards still said "MAHJONG SOCIAL CLUB". They're re-stamped with the current tab ("MATCHING MAHJONG TILES, MATS & RACKS"), pixel-copied from a Sunday v3 card.
  - Folders: logofix-v2 (209), codefooter-v1 (72), holiday (94), holiday-v4 (31), new-oct18 (35), larkspur-v6 (30), malachite-new (9), plus the not-yet-live albums: papaya-spritz, petalee, brownstone-bloom, from-the-vault, peony-and-parasol, spirit-of-christmas.
  - Her own 750x938 originals are untouched.
  - The generators (gen.py, gen2.py, gen_hol.py) now use card_navy_logo_v2.png, so new renders get the right tab.
- **B&B woods** (doc 57; Almond and Tudor added Oct 18): 87 wood racks were found by OCR plus an eye check across 77 cards and replaced:
  - Almond: 43
  - Tudor: 20
  - Red Mahogany: 16
  - Provincial: 5
  - Weathered Oak: 2
  - Dark Walnut: 1
  - Replacements:
    - Bird & Bamboo Cream: 43
    - Bam Bird Boutique Walnut: 36
    - Bird & Bamboo Cornflower Blue: 8
  - **Almond became B&B Cream**, the closest non-wood neutral. **Tudor on Blue Christmas became Cornflower Blue**, from the mat's blue bow. **Every other wood became Bam Bird Boutique Walnut**, using the real product photo, per doc 57's "for wood, use real photos".
  - The Tigre de Tartan Provincial cards are covered: Sierra and Nantucket on Caned Trompe and on Nantucket Basket, plus Sierra + El Tigre (Dark Walnut).

## How to apply
- Live pages pin jsDelivr card URLs to a commit. The swap is the same file path at `@c3ae3a324e57f45f24172fcebec938e1c0ebd70a`. Each `<page>.json` lists old URL → new URL, and the `fix` field says what changed on that card.
- **Pages with old-tagline or wood cards:** 40 pages, 258 card links.
- **Pending swaps re-pinned to the new commit, so they carry these fixes too:**
  - the 14 code-footer swaps (site/livepatch/codefooter/)
  - the pending album blocks: Brownstone Bloom, the vault albums, Papaya Spritz, Petalée
- **Overlap with codefooter:** 14 pages are also in the code-footer swap. Apply the code-footer block first, then this list for any cards it doesn't cover. Old URLs already replaced will simply not match.

| Page | Card links | With wood fix |
|---|---|---|
| /cypress-forest-mahjong-tile-matches | 29 | 0 |
| /gatsby-mahjong-tile-matches | 28 | 4 |
| /seabreeze-mahjong-tile-matches | 23 | 0 |
| /talulah-mahjong-tile-matches | 22 | 1 |
| /osler-mahjong-tile-matches | 19 | 2 |
| /heritage-mahjong-tile-matches | 13 | 5 |
| /tortoise-mahjong-tile-matches | 13 | 5 |
| /heritage-2-0-mahjong-tile-matches | 12 | 5 |
| /moonlight-mahjong-tile-matches | 7 | 3 |
| /holiday-mahjong-matches | 6 | 3 |
| /la-fete-mahjong-tile-matches | 6 | 0 |
| /tigre-de-tartan-discount-code | 6 | 2 |
| /amara-mahjong-tile-matches | 5 | 1 |
| /nantucket-mahjong-tile-matches | 5 | 3 |
| /palm-royale-mahjong-tile-matches | 5 | 2 |
| /sorbet-mahjong-tile-matches | 5 | 1 |
| /dandy-mahjong-tile-matches | 4 | 1 |
| /drake-mahjong-tile-matches | 4 | 1 |
| /luminaire-mahjong-tile-matches | 4 | 0 |
| /birdie-mahjong-tile-matches | 3 | 0 |
| /gemma-mahjong-tile-matches | 3 | 0 |
| /jasmine-mahjong-tile-matches | 3 | 2 |
| /lola-mahjong-tile-matches | 3 | 1 |
| /pearlescent-mahjong-tile-matches | 3 | 0 |
| /sierra-mahjong-tile-matches | 3 | 3 |
| /solara-mahjong-tile-matches | 3 | 1 |
| /willow-mahjong-tile-matches | 3 | 1 |
| /emerald-mahjong-tile-matches | 2 | 1 |
| /glow-wild-mahjong-tile-matches | 2 | 1 |
| /limoncello-mahjong-tile-matches | 2 | 0 |
| /pippa-mahjong-tile-matches | 2 | 0 |
| /taylor-mahjong-tile-matches | 2 | 0 |
| /britt-mills-discount-code | 1 | 0 |
| /charleston-mahjong-club-discount-code | 1 | 0 |
| /glitterville-mahjong-tile-matches | 1 | 1 |
| /jade-mahjong-tile-matches | 1 | 0 |
| /mac-and-miller-mahjong-discount-code | 1 | 0 |
| /mahj-mood-discount-code | 1 | 0 |
| /malachite-mahjong-tile-matches | 1 | 0 |
| /sunset-mahjong-tile-matches | 1 | 1 |

## Still needs attention
- **Rack captions:** they don't match the patched cards yet. The caption fix (site/livepatch/codefooter, rackcaptions) mirrored the old card labels, so about 25 holiday captions still name Tudor, Almond, Red Mahogany, Provincial or Weathered Oak. Regenerate those captions from scripts/albumcard/woodfix/woodpatched.json before the holiday swap goes live.
- **Holiday renders:** the holiday card specs (holiday_manifest.json and the picker picks) still list the woods. If the holiday set is ever re-rendered, update the picks first or the woods come back.
- **OCR coverage:** OCR plus an eye check of all 209 logofix-v2 panels found these. A few holiday or other cards may have been missed. Spot-check before swapping.
- **Cream and Walnut are stand-ins:** they keep each card's look (neutral → neutral, dark wood → real dark wood). Tiffany may prefer a different pick on any card.
