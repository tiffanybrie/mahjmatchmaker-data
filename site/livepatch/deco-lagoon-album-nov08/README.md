# Deco (Lagoon) (Bam Bird Boutique) album: LIVE Nov 8, ~7:35pm ET

Tiffany's review round 1 (saved 6:19pm, "done") + her 6:20-6:25pm notes. Tiles in stock (bambirdboutique.com deco-tile-set.js:
Lagoon variants available) -> "Available now" copy. No pronoun for Deco (never asked; brand guide s3).

## What is live
- **Page** https://www.mahjmatchmaker.com/deco-lagoon-mahjong-tile-matches (Not Linked; duplicated from Juniper). Title "Deco (Lagoon)
  Mahjong Tile Matches", nav "Deco (Lagoon) Tile Matches", SEO title "Deco (Lagoon) Mahjong Tile Matches: Mats & Racks for Bam Bird
  Boutique Deco Lagoon", SEO description "Bam Bird Boutique Deco (Lagoon) tiles, available now, matched to 41 mats from 21 brands...".
  Social image = site default.
- **Code block** = `deco-lagoon-codeblock.html` (pin @a5cc037e; images @24f5e814), built by `build_block.py <image sha>` from the LIVE
  Juniper block (CSS, hero, FAQ + JSON-LD, Colors & racks, lightbox with the pinch fix). 41 cards: 38 in her order + holiday section
  `#holiday-matches` (Winter Jewel, Yuletide, Poinsettia Party = 01-03). Cover option 0, her 7 faces (favorites.py: 4 singles, irises
  as a pair), colour card + wheel. Links: FYM 1.18 build; spec `url` for mats not in 1.18 (Splash Lady Luck's, Dreamframer ShopMy pin,
  Silk Crane Cloud, Lemondrop Sapphire Blooms + Floral Affair). Lemondrop caption: "No code for Lemondrop Mahjong Co yet".
- Pasted with the CodeMirror dispatch method (doc length = file length 105442), Save black -> saved. curl: 200, 41 cards, 46/46 images
  200, 0 "Juniper", holiday_numbering 0 problems.
- **/mahjong-tile-matches**: first in Our Latest Albums + end of the Blue grid (block ...1478_3720).
- **/blue-mahjong-tile-matches**: mmcol-card first ("Bam Bird Boutique · 41 matches").
- **/bam-bird-boutique-discount-code**: "Where Bam Bird Boutique shows up" list: Deco (Lagoon) album first.
- **/links**: latest-album card = Deco (Lagoon) (feature-deco-lagoon.jpg = FYM faces|backs split; album-deco-lagoon.jpg = cover),
  strip first; FYM card stays first. Images @ba9cade1.
- **Google**: URL Inspection = unknown to Google; Request indexing done (priority crawl queue).
- **Pinterest**: config/pinterest/queue.json album-deco-lagoon, guide-deco-lagoon, card-deco-lagoon-01..04 (uniform-v3/deco-lagoon.jpg = cover).
- **HQ** hq/albums: Deco item -> Lagoon live, Mulberry + Indigo building (Juniper item also corrected to live).

## Cards (assets/cards/deco-lagoon, 41 + manifest.json)
Spec scripts/albumcard/specs/deco-lagoon_nov07.json (`_final_nov08`): her order + Sapphire Blooms #5 (Lemondrop, pending affiliate,
watermark: bottom-left corner box), Crane Cloud #11 (Silk Mahjong, non-partner), Floral Affair #26 (Lemondrop, research add).
Cocktail Club (Charleston) NOT added (Tiffany 6:24pm: wrong link). Build: record card_build commands (deco_build.py -> gen2.py).
Every card: inset columns 1-2 + backs, Bam Bird Lagoon Wood + Mulberry Wood tile racks, code band on (tiles are a partner).

## FYM 1.19 (ship with the next release)
1. Catalog adds: config/fym-catalog-adds-nov08-lagoon.json (Silk Mahjong whole line x8, Lemondrop Sapphire Blooms + Floral Affair,
   Splash Lady Luck's Teal Lounge) + config/fym-shopmy-catalog-refresh-nov08.json (Dreamframer fans). Normal photo gates.
2. `python3 builder/fym_fix_nov08/deco_lagoon_m119.py <b119>`: m-list (41 keys, her order) + album link for set bam-bird-boutique-deco.
3. Gallery rebuild picks the adds up (Silk leatherette/neoprene = one card each, one listing).

## Open
- Lemondrop approval -> swap 2 links (config/link-routes.json Lemondrop pending_swap).
- ShopMy/Etsy check for Silk Mahjong (docs/OVERDUE.md).
- Social row, FB group post, FYM tie-in, "new albums" email + album-request emails: DESK (social owner / Main).
